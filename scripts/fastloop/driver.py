"""Fast race driver (fastloop-v2): keeps the Haiku slots busy, decides after every game, writes new challengers.

Every POLL seconds until $FASTLOOP_DIR/STOP exists:
1. keep one continuous scheduler alive (`careerlab run --kind claude-cli --continuous`);
2. run a ladder step and apply it (games to queue, challengers out, a new champion);
3. start designers (scripts/fastloop/design.py) for the step's design requests, at most MAX_DESIGNERS at once,
   and only while the five-hour window is under the cap;
4. put each finished design on the ladder (`careerlab ladder add`, which lints with known event titles and
   registers); one repair round if the linter rejects it, otherwise the folder moves to $FASTLOOP_DIR/rejected/;
5. every REPORT_S, rewrite lab/reports/carrera-rapida.md and lab/fastloop/history.md.

The driver never commits: the organiser session commits lab/ and pushes, as before.
Start (from the repository root, after the CLI pin in scripts/fastloop/README.md):
    setsid nohup uv run python scripts/fastloop/driver.py >> ~/careerlab-data/huawei/fastloop/driver.out 2>&1 < /dev/null &
Stop: touch ~/careerlab-data/huawei/fastloop/STOP (games in flight finish; the scheduler stops leasing).
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from careerlab import ladder  # noqa: E402
from careerlab.config import load_settings  # noqa: E402
from careerlab.scheduler import latest_quota  # noqa: E402

SLOTS = int(os.environ.get("FASTLOOP_SLOTS", 8))
CAP = float(os.environ.get("FASTLOOP_MAX_FIVE_HOUR", 0.85))
MAX_DESIGNERS = int(os.environ.get("FASTLOOP_MAX_DESIGNERS", 2))
POLL, REPORT_S = 60, 600


def utc(y: int, m: int, d: int, h: int = 0) -> float:
    return datetime(y, m, d, h, tzinfo=timezone.utc).timestamp()


# Seven-day pace for the fast race (Alejandro, 26 Oct: put resources where we see value, sooner): spend more before
# cut 1 and cut 2, keep a tail for the last days and about 10 % for the team's own chats.
FAST_PACE = {"knots": [[utc(2026, 10, 26, 16), 0.10], [utc(2026, 10, 28), 0.45], [utc(2026, 10, 31), 0.75], [utc(2026, 11, 2), 0.90]]}


def now_s() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


class Driver:
    def __init__(self) -> None:
        self.s = load_settings()
        self.dir = self.s.data_dir / "fastloop"
        self.dir.mkdir(parents=True, exist_ok=True)
        self.state_path = self.s.lab_dir / "fastloop" / "state.json"
        self.sched: subprocess.Popen | None = None
        self.designers: list[tuple[subprocess.Popen, str, Path, float]] = []  # (process, kind, stdout file, started)
        self.last_report = 0.0

    def log(self, msg: str) -> None:
        with (self.dir / "driver.log").open("a") as fh:
            fh.write(f"[{now_s()}] {msg}\n")

    def write_pace(self) -> None:
        cap_file = self.s.data_dir / "quota_cap.json"
        cfg = json.loads(cap_file.read_text()) if cap_file.exists() else {}
        cfg.update(max_five_hour=CAP, weekly_pace=FAST_PACE)
        cap_file.write_text(json.dumps(cfg, indent=1))

    def ensure_scheduler(self) -> None:
        if self.sched is not None and self.sched.poll() is None:
            return
        if self.sched is not None:
            self.log(f"scheduler exited rc={self.sched.returncode}; restarting")
        other = subprocess.run(["pgrep", "-f", "careerlab run --kind claude-cli"], capture_output=True, text=True).stdout.split()
        if other:  # an old batch driver or an orphaned scheduler: never run two schedulers on one registry
            self.log(f"another claude-cli scheduler is running (pids {other}); not starting one")
            return
        stop = self.dir / "STOP-SCHEDULER"
        stop.unlink(missing_ok=True)
        out = (self.dir / "scheduler.out").open("a")
        self.sched = subprocess.Popen(["uv", "run", "careerlab", "run", "--kind", "claude-cli", "--continuous", "--slots", str(SLOTS),
                                       "--max-five-hour", str(CAP), "--stop-file", str(stop)], cwd=REPO, stdout=out, stderr=subprocess.STDOUT)
        self.log(f"scheduler started pid={self.sched.pid} slots={SLOTS} cap={CAP}")

    def five_hour_ok(self) -> bool:
        util, resets = latest_quota(self.s.runs_dir)
        return util is None or util < CAP or bool(resets and time.time() > resets)

    def step(self) -> list[str]:
        reg = self.s.registry()
        try:
            new, actions = ladder.run_step(reg, self.state_path, apply_changes=True, in_flight=[k for _, k, _, _ in self.designers])
        finally:
            reg.db.close()
        for a in actions:
            if a.kind != "design":
                self.log(f"{a.kind} {a.policy_id or ''} {a.status or ''} n={a.n}: {a.why}")
        return [a.design for a in actions if a.kind == "design"]

    def start_designers(self, kinds: list[str]) -> None:
        for kind in kinds:
            if len(self.designers) >= MAX_DESIGNERS or not self.five_hour_ok():
                return
            out = self.dir / "design-logs" / f"{kind}-{int(time.time())}.json"
            out.parent.mkdir(parents=True, exist_ok=True)
            proc = subprocess.Popen(["uv", "run", "python", "scripts/fastloop/design.py", "--kind", kind], cwd=REPO,
                                    stdout=out.open("w"), stderr=subprocess.DEVNULL)
            self.designers.append((proc, kind, out, time.time()))
            self.log(f"designer started kind={kind} pid={proc.pid}")

    def collect_designers(self) -> None:
        still = []
        for proc, kind, out, started in self.designers:
            if proc.poll() is None:
                still.append((proc, kind, out, started))
                continue
            try:
                res = json.loads(out.read_text().strip().splitlines()[-1])
            except (ValueError, IndexError):
                res = {"ok": False, "error": "no result line"}
            if not res.get("ok"):
                self.log(f"designer {kind} failed: {str(res.get('error'))[:300]}")
                self.reject(res.get("out"))
                continue
            self.add(Path(res["out"]), kind, res.get("summary", ""))
        self.designers = still

    def add(self, folder: Path, kind: str, summary: str, repaired: bool = False) -> None:
        why = " ".join(summary.split())[:400] or f"{kind} design"
        proc = subprocess.run(["uv", "run", "careerlab", "ladder", "add", str(folder), "--kind", kind, "--why", why],
                              cwd=REPO, capture_output=True, text=True)
        if proc.returncode == 0:
            self.log(f"added {folder.name} ({kind}): {proc.stdout.strip()[-200:]}")
            return
        self.log(f"ladder add refused {folder.name}: {(proc.stdout + proc.stderr)[-400:]}")
        if repaired:
            self.reject(str(folder))
            return
        errors = self.dir / "design-logs" / f"{folder.name}-lint.txt"
        errors.write_text(proc.stdout + proc.stderr)
        rep = subprocess.run(["uv", "run", "python", "scripts/fastloop/design.py", "--repair", str(folder), "--errors", str(errors)],
                             cwd=REPO, capture_output=True, text=True, timeout=45 * 60)
        if rep.returncode == 0:
            self.add(folder, kind, summary, repaired=True)
        else:
            self.reject(str(folder))

    def reject(self, folder: str | None) -> None:
        if folder and Path(folder).exists():
            dest = self.dir / "rejected" / Path(folder).name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(folder, dest)
            self.log(f"rejected design moved to {dest}")

    def report(self) -> None:
        subprocess.run(["uv", "run", "careerlab", "ladder", "status", "--write"], cwd=REPO, capture_output=True, text=True)
        self.last_report = time.time()

    def run(self) -> None:
        self.log(f"driver start pid={os.getpid()}")
        self.write_pace()
        self.report()  # history.md exists before the first designer reads it
        while not (self.dir / "STOP").exists():
            try:
                self.ensure_scheduler()
                self.collect_designers()
                self.start_designers(self.step())
                if time.time() - self.last_report > REPORT_S:
                    self.report()
            except Exception as exc:  # keep the race alive; the log says what broke
                self.log(f"error: {exc!r}")
            time.sleep(POLL)
        (self.dir / "STOP-SCHEDULER").touch()
        self.log("STOP: scheduler told to stop leasing; waiting for designers")
        for proc, *_ in self.designers:
            proc.wait()
        self.collect_designers()
        self.report()
        self.log("driver exit")


if __name__ == "__main__":
    Driver().run()
