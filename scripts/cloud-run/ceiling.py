"""T13 ceiling lane: run queued claude-cli 'pilot' jobs (Opus ceiling games) with at most 2 concurrent workers.

Same quota governor as the main lane. Interrupted attempts get a replacement in this lane
(prereg-v1 3.4) and are never scored. Stops at END, when STOP or CEILING_STOP exists.
"""

import json
import subprocess
import time

from driver import END, LOGS, REPO, SP, STOP, log, now, queued, requeue_interrupted

from careerlab.config import load_settings
from careerlab.store import Registry

CEILING_STOP = SP / "CEILING_STOP"


def main() -> None:
    s = load_settings()
    run = len(list(LOGS.glob("ceiling-*.done.json")))
    log(f"ceiling lane start, runs so far={run}")
    while time.time() < END and not STOP.exists() and not CEILING_STOP.exists():
        reg = Registry(s.registry_path)
        n = queued(reg, pilot=True)
        reg.db.close()
        if n == 0:
            time.sleep(60)
            continue
        run += 1
        log(f"ceiling run {run}: {n} pilot jobs queued")
        with (LOGS / f"ceiling-{run}.log").open("w") as out:
            rc = subprocess.run(["uv", "run", "careerlab", "run", "--kind", "claude-cli", "--slots", "2", "--purpose", "pilot",
                                 "--max-five-hour", "0.95"], cwd=REPO, stdout=out, stderr=subprocess.STDOUT).returncode
        reg = Registry(s.registry_path)
        requeued = requeue_interrupted(reg, pilot=True)
        (LOGS / f"ceiling-{run}.done.json").write_text(json.dumps({"run": run, "rc": rc, "finished_utc": now(), "requeued": requeued}))
        log(f"ceiling run {run} done rc={rc}; requeued {len(requeued)}")
        reg.db.close()
        if rc != 0:
            time.sleep(120)
    log("ceiling lane exit")


if __name__ == "__main__":
    main()
