"""Unattended batch driver for the cloud lab run (26-27 Oct 2026).

Loop: run every queued claude-cli job with the quota governor, queue replacement
attempts for interrupted slots (prereg-v1 3.4), record the pre-registered block
decision for the Haiku actor, and drop a marker file so the orchestrator wakes up.
Stops at END, or when STOP exists.
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("/home/user/huawei")
SP = Path(os.environ.get("CLOUD_RUN_DIR", Path.home() / "careerlab-data" / "huawei" / "cloud-run"))  # logs, next.md, teacher.md, relevo.md
LOGS = SP / "logs"
STOP = SP / "STOP"
END = datetime(2026, 10, 27, 7, 0, tzinfo=timezone.utc).timestamp()
HAIKU = "08e9167a965ed82c"
ROUND_S = 18 * 60  # one round of 6 slots, generous for Haiku
MAX_ATTEMPT = 3

sys.path.insert(0, str(REPO))
from careerlab import decisions  # noqa: E402
from careerlab.config import load_settings  # noqa: E402
from careerlab.scheduler import latest_quota  # noqa: E402
from careerlab.store import Registry  # noqa: E402


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def log(msg: str) -> None:
    with (LOGS / "driver.log").open("a") as fh:
        fh.write(f"[{now()}] {msg}\n")


def queued(reg: Registry, pilot: bool = False) -> int:
    """Queued claude-cli jobs of the main lane (pilot=False) or the T13 ceiling lane (pilot=True, purpose 'pilot')."""
    return reg.db.execute("SELECT COUNT(*) FROM jobs j JOIN actors a USING(actor_id) WHERE j.status='queued' AND a.kind='claude-cli' AND j.origin='' "
                          "AND (j.purpose='pilot') = ?", (int(pilot),)).fetchone()[0]


def requeue_interrupted(reg: Registry, pilot: bool = False) -> list[str]:
    """Replacement attempt for each claude-cli slot of one lane whose latest attempt is interrupted (keeps its priority)."""
    out = []
    rows = reg.db.execute(
        "SELECT j.* FROM jobs j JOIN actors a USING(actor_id) WHERE a.kind='claude-cli' AND j.status='interrupted' AND j.origin='' "
        f"AND (j.purpose='pilot') = {int(pilot)} "
        "AND j.attempt = (SELECT MAX(k.attempt) FROM jobs k WHERE k.policy_id=j.policy_id AND k.actor_id=j.actor_id "
        "AND k.env_id=j.env_id AND k.purpose=j.purpose AND k.replicate=j.replicate)").fetchall()
    for job in rows:
        if job["attempt"] >= MAX_ATTEMPT:
            continue
        new = reg.requeue_interrupted(job["job_id"], "replacement attempt after interruption (prereg-v1 3.4)")
        reg.decide("requeue", job["job_id"], {"new_job": new}, "interrupted Claude attempt kept on record, never scored; same slot gets a replacement attempt")
        out.append(new)
    return out


def main() -> None:
    LOGS.mkdir(parents=True, exist_ok=True)
    s = load_settings()
    batch = len(list(LOGS.glob("batch-*.done.json")))
    log(f"driver start pid={os.getpid()} batches so far={batch}")
    while time.time() < END and not STOP.exists():
        reg = Registry(s.registry_path)
        n = queued(reg)
        reg.db.close()
        if n == 0:
            time.sleep(60)
            continue
        rounds_left = int((END - time.time() - 20 * 60) // ROUND_S)
        if rounds_left < 1:
            log("no time left for another round; stopping")
            break
        batch += 1
        slots, override = 6, SP / "batch.json"  # one-shot override for the next batch, e.g. {"slots": 8, "limit": 24}
        limit = min(n, 6 * rounds_left)  # ceiling (pilot) jobs have priority -100 and sort last, so --limit n never leases them
        if override.exists():
            cfg = json.loads(override.read_text())
            override.unlink()
            slots, limit = int(cfg.get("slots", slots)), min(n, int(cfg.get("limit", limit)))
        log(f"batch {batch}: {n} queued, limit {limit}, slots {slots}")
        started = time.time()
        with (LOGS / f"batch-{batch}.log").open("w") as out:
            rc = subprocess.run(["uv", "run", "careerlab", "run", "--kind", "claude-cli", "--slots", str(slots), "--max-five-hour", "0.80",
                                 "--limit", str(limit)], cwd=REPO, stdout=out, stderr=subprocess.STDOUT).returncode
        reg = Registry(s.registry_path)
        requeued = requeue_interrupted(reg)
        out = decisions.block_decision(reg, HAIKU, record=True)
        util, resets = latest_quota(s.runs_dir)
        (LOGS / f"decision-{batch}.md").write_text(decisions.markdown(out) + "\n")
        marker = {"batch": batch, "rc": rc, "started": started, "finished": time.time(), "finished_utc": now(), "requeued": requeued,
                  "five_hour": util, "resets_at": resets,
                  "leader": out["rows"][0]["policy"] if out["rows"] else None,
                  "jobs": {r[0]: r[1] for r in reg.db.execute("SELECT status, COUNT(*) FROM jobs GROUP BY status")}}
        (LOGS / f"batch-{batch}.done.json").write_text(json.dumps(marker, indent=1))
        log(f"batch {batch} done rc={rc} in {(time.time() - started) / 60:.1f} min; requeued {len(requeued)}; leader {marker['leader']}; five_hour {util}")
        reg.db.close()
        if rc != 0:
            time.sleep(120)
    log("driver exit")


if __name__ == "__main__":
    main()
