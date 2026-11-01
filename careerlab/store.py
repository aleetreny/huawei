"""Registry of policies, actors, environments, jobs, evaluations and decisions.

One integrator process writes the SQLite registry (WAL mode). Workers only write
inside their own run directory; the integrator validates ``result.json`` and
ingests it. Policies are immutable bundles addressed by the SHA-256 of their
exact bytes. JSONL exports in ``lab/registry/`` are what we commit to Git.

Each registry belongs to one origin ('' for the canonical race, or a machine
name). Jobs and decisions carry their origin; a registry only leases, recovers
and decides on its own origin's jobs, and other origins get disjoint job ids
and replicate numbers, so exports from several machines merge without clashes.
"""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

SCHEMA = """
CREATE TABLE IF NOT EXISTS policies (
  policy_id TEXT PRIMARY KEY, family TEXT NOT NULL, name TEXT NOT NULL, parents TEXT NOT NULL,
  hypothesis TEXT NOT NULL, change TEXT NOT NULL, bundle_path TEXT NOT NULL, created_at REAL NOT NULL,
  created_by TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'active', status_reason TEXT, review_trigger TEXT, meta TEXT);
CREATE TABLE IF NOT EXISTS actors (actor_id TEXT PRIMARY KEY, kind TEXT NOT NULL, config TEXT NOT NULL, created_at REAL NOT NULL);
CREATE TABLE IF NOT EXISTS environments (env_id TEXT PRIMARY KEY, fingerprint TEXT NOT NULL, created_at REAL NOT NULL);
CREATE TABLE IF NOT EXISTS jobs (
  job_id TEXT PRIMARY KEY, policy_id TEXT NOT NULL, actor_id TEXT NOT NULL, env_id TEXT NOT NULL,
  purpose TEXT NOT NULL, replicate INTEGER NOT NULL, attempt INTEGER NOT NULL DEFAULT 1,
  status TEXT NOT NULL, priority REAL NOT NULL DEFAULT 0, lease_owner TEXT, lease_expires REAL,
  pid INTEGER, session_id TEXT, db_root TEXT, run_dir TEXT, note TEXT, created_at REAL NOT NULL, updated_at REAL NOT NULL,
  UNIQUE (policy_id, actor_id, env_id, purpose, replicate, attempt));
CREATE TABLE IF NOT EXISTS evaluations (
  job_id TEXT PRIMARY KEY REFERENCES jobs(job_id), policy_id TEXT NOT NULL, actor_id TEXT NOT NULL, env_id TEXT NOT NULL,
  purpose TEXT NOT NULL, outcome TEXT NOT NULL, survival_months INTEGER, completed INTEGER, score REAL,
  dims TEXT, steps INTEGER, rejected_actions INTEGER, tokens TEXT, wall_s REAL,
  trajectory_path TEXT, trajectory_sha256 TEXT, interruption TEXT, ingested_at REAL NOT NULL,
  resumed INTEGER NOT NULL DEFAULT 0, launch_index INTEGER);
CREATE TABLE IF NOT EXISTS decisions (
  decision_id INTEGER PRIMARY KEY AUTOINCREMENT, at REAL NOT NULL, kind TEXT NOT NULL, subject TEXT,
  payload TEXT NOT NULL, rationale TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS jobs_status ON jobs(status);
CREATE INDEX IF NOT EXISTS evals_cell ON evaluations(policy_id, actor_id, env_id, purpose);
CREATE TABLE IF NOT EXISTS target_budget_accounts (account TEXT PRIMARY KEY,config TEXT NOT NULL,created_at REAL NOT NULL);
CREATE TABLE IF NOT EXISTS target_budget_events (
 event_id TEXT PRIMARY KEY,account TEXT NOT NULL REFERENCES target_budget_accounts(account),job_id TEXT NOT NULL,
 kind TEXT NOT NULL,payload TEXT NOT NULL,at REAL NOT NULL);
"""

TERMINAL_OUTCOMES = ("completed", "eliminated")
CUT_OUTCOME = "truncated"  # short game stopped on purpose: stored, never scored (careerlab.truncate)
EXPORT_KEYS = {"policies": "policy_id", "actors": "actor_id", "environments": "env_id", "jobs": "job_id",
               "evaluations": "job_id", "decisions": "decision_id",
               "target_budget_accounts":"account","target_budget_events":"event_id"}


class ExportWouldDropRows(RuntimeError):
    """The export folder holds rows this registry does not have; writing would delete them."""


def origin_replicate_base(origin: str) -> int:
    """First replicate number of an origin: 0 for the race, a stable disjoint block for every other machine."""
    if not origin:
        return 0
    return 1_000_000 * (1 + int(hashlib.sha256(origin.encode()).hexdigest(), 16) % 9000)


def canonical_hash(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def bundle_hash(bundle_dir: Path) -> str:
    """SHA-256 over relative paths and exact bytes of every file in a policy bundle."""
    digest = hashlib.sha256()
    for path in sorted(p for p in bundle_dir.rglob("*") if p.is_file() and p.name != ".DS_Store"):
        digest.update(str(path.relative_to(bundle_dir)).encode() + b"\0")
        digest.update(path.read_bytes() + b"\0")
    return digest.hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


class Registry:
    def __init__(self, path: Path, origin: str = ""):
        from careerlab.config import check_origin

        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        self.origin = check_origin(origin)
        self.db = sqlite3.connect(path, timeout=30, isolation_level=None)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.executescript(SCHEMA)
        if "evidence" not in {r[1] for r in self.db.execute("PRAGMA table_info(evaluations)")}:
            self.db.execute("ALTER TABLE evaluations ADD COLUMN evidence TEXT")
        for table in ("jobs", "decisions"):  # added for T11; existing rows are the race's
            if "origin" not in {r[1] for r in self.db.execute(f"PRAGMA table_info({table})")}:
                self.db.execute(f"ALTER TABLE {table} ADD COLUMN origin TEXT NOT NULL DEFAULT ''")

    @contextmanager
    def tx(self) -> Iterator[sqlite3.Connection]:
        self.db.execute("BEGIN IMMEDIATE")
        try:
            yield self.db
            self.db.execute("COMMIT")
        except BaseException:
            self.db.execute("ROLLBACK")
            raise

    # -- identities -------------------------------------------------------
    def register_actor(self, kind: str, config: dict[str, Any]) -> str:
        actor_id = canonical_hash({"kind": kind, **config})[:16]
        self.db.execute("INSERT OR IGNORE INTO actors VALUES (?,?,?,?)", (actor_id, kind, json.dumps(config, sort_keys=True), time.time()))
        return actor_id

    def register_environment(self, fingerprint: dict[str, Any]) -> str:
        env_id = canonical_hash(fingerprint)[:16]
        self.db.execute("INSERT OR IGNORE INTO environments VALUES (?,?,?)", (env_id, json.dumps(fingerprint, sort_keys=True), time.time()))
        return env_id

    def register_policy(self, bundle_dir: Path, family: str, name: str, parents: list[str], hypothesis: str,
                        change: str, created_by: str, meta: dict[str, Any] | None = None) -> str:
        """Register an immutable policy bundle; identical bytes map to the same id."""
        policy_id = bundle_hash(bundle_dir)[:16]
        existing = self.db.execute("SELECT policy_id FROM policies WHERE policy_id=?", (policy_id,)).fetchone()
        if existing:
            return policy_id
        missing = [p for p in parents if not self.db.execute("SELECT 1 FROM policies WHERE policy_id=?", (p,)).fetchone()]
        if missing:
            raise ValueError(f"unknown parent policies {missing}")
        self.db.execute(
            "INSERT INTO policies (policy_id,family,name,parents,hypothesis,change,bundle_path,created_at,created_by,meta) VALUES (?,?,?,?,?,?,?,?,?,?)",
            (policy_id, family, name, json.dumps(parents), hypothesis, change, str(bundle_dir), time.time(), created_by, json.dumps(meta or {})),
        )
        return policy_id

    def verify_policy(self, policy_id: str) -> bool:
        row = self.db.execute("SELECT bundle_path FROM policies WHERE policy_id=?", (policy_id,)).fetchone()
        return bool(row) and bundle_hash(Path(row["bundle_path"]))[:16] == policy_id

    def set_policy_status(self, policy_id: str, status: str, reason: str, review_trigger: str | None = None) -> None:
        assert status in ("active", "dormant", "frozen", "invalid", "retired")
        with self.tx():
            self.db.execute("UPDATE policies SET status=?, status_reason=?, review_trigger=? WHERE policy_id=?", (status, reason, review_trigger, policy_id))
            self.decide("policy_status", policy_id, {"status": status, "review_trigger": review_trigger}, reason, in_tx=True)

    # -- jobs -------------------------------------------------------------
    def enqueue(self, policy_id: str, actor_id: str, env_id: str, purpose: str, replicates: int, priority: float = 0.0) -> list[str]:
        """Add replicates beyond those already queued or done for this cell; idempotent."""
        created = []
        for table, key, value in (("policies", "policy_id", policy_id), ("actors", "actor_id", actor_id), ("environments", "env_id", env_id)):
            if not self.db.execute(f"SELECT 1 FROM {table} WHERE {key}=?", (value,)).fetchone():
                raise ValueError(f"unknown {key} {value!r}")
        with self.tx():
            base = origin_replicate_base(self.origin)
            top = self.db.execute("SELECT COALESCE(MAX(replicate),?) FROM jobs WHERE policy_id=? AND actor_id=? AND env_id=? AND purpose=? AND origin=?",
                                  (base - 1, policy_id, actor_id, env_id, purpose, self.origin)).fetchone()[0]
            prefix = f"{self.origin}-" if self.origin else ""
            for r in range(top + 1, top + 1 + replicates):
                job_id = f"{prefix}{purpose[:4]}-{policy_id[:8]}-{actor_id[:6]}-{env_id}-{r - base:05d}-a1"
                now = time.time()
                self.db.execute("INSERT INTO jobs (job_id,policy_id,actor_id,env_id,purpose,replicate,attempt,status,priority,created_at,updated_at,origin) VALUES (?,?,?,?,?,?,1,'queued',?,?,?,?)",
                                (job_id, policy_id, actor_id, env_id, purpose, r, priority, now, now, self.origin))
                created.append(job_id)
        return created

    def lease(self, owner: str, limit: int, lease_s: float = 3600.0, actor_kind: str | None = None,
              purpose: str | None = None) -> list[sqlite3.Row]:
        with self.tx():
            query = "SELECT j.* FROM jobs j JOIN actors a USING(actor_id) WHERE j.status='queued' AND j.origin=?"
            args: list[Any] = [self.origin]  # never run another machine's queue
            if actor_kind:
                query += " AND a.kind=?"
                args.append(actor_kind)
            if purpose:
                query += " AND j.purpose=?"
                args.append(purpose)
            rows = self.db.execute(query + " ORDER BY j.priority DESC, j.replicate, j.created_at LIMIT ?", (*args, limit)).fetchall()
            for row in rows:
                self.db.execute("UPDATE jobs SET status='leased', lease_owner=?, lease_expires=?, updated_at=? WHERE job_id=? AND status='queued'",
                                (owner, time.time() + lease_s, time.time(), row["job_id"]))
        return rows

    def mark_running(self, job_id: str, pid: int, run_dir: str, owner: str | None = None) -> bool:
        """Claim a leased job for execution; False if another scheduler owns or ran it (no duplicate runs)."""
        if owner is None:
            self.db.execute("UPDATE jobs SET status='running', pid=?, run_dir=?, updated_at=? WHERE job_id=?", (pid, run_dir, time.time(), job_id))
            return True
        cur = self.db.execute("UPDATE jobs SET status='running', pid=?, run_dir=?, updated_at=? WHERE job_id=? AND status='leased' AND lease_owner=?",
                              (pid, run_dir, time.time(), job_id, owner))
        return cur.rowcount == 1

    def set_session(self, job_id: str, session_id: str, db_root: str | None = None) -> None:
        self.db.execute("UPDATE jobs SET session_id=?, db_root=COALESCE(?, db_root), updated_at=? WHERE job_id=?",
                        (session_id, db_root, time.time(), job_id))

    def ingest(self, job_id: str, run_dir: Path) -> str:
        """Validate a worker's result.json and record it. Interruptions are kept but never scored."""
        result = json.loads((run_dir / "result.json").read_text())
        if result["job_id"] != job_id:
            raise ValueError(f"result belongs to {result['job_id']}, not {job_id}")
        job = self.db.execute("SELECT * FROM jobs WHERE job_id=?", (job_id,)).fetchone()
        outcome = result["outcome"]
        score = result.get("quantitative_score") if outcome in TERMINAL_OUTCOMES else None
        if outcome in TERMINAL_OUTCOMES and score is None:
            outcome, result["interruption"] = "interrupted", "terminal state without ending_score"
        traj = Path(result["trajectory_path"]) if result.get("trajectory_path") else None
        dims = {d["name"]: d.get("normalized_score") for d in (result.get("ending_score") or {}).get("dimensions", [])}
        from careerlab.evidence import build_evidence
        from careerlab.episode import atomic_write_json
        evidence = build_evidence(result,run_dir)
        atomic_write_json(run_dir/"evidence.json",evidence)
        with self.tx():
            self.db.execute(
                "INSERT OR REPLACE INTO evaluations (job_id,policy_id,actor_id,env_id,purpose,outcome,survival_months,completed,score,"
                "dims,steps,rejected_actions,tokens,wall_s,trajectory_path,trajectory_sha256,interruption,ingested_at,resumed,launch_index,evidence) "
                "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (job_id, job["policy_id"], job["actor_id"], job["env_id"], job["purpose"], outcome,
                 result.get("survival_months"), int(bool((result.get("ending_score") or {}).get("completed"))), score,
                 json.dumps(dims), result.get("steps"), result.get("rejected_actions"), json.dumps(result.get("actor_usage") or {}),
                 result.get("wall_seconds"), str(traj) if traj else None, file_sha256(traj) if traj and traj.exists() else None,
                 result.get("interruption"), time.time(), int(bool(result.get("resumed"))), job["replicate"],json.dumps(evidence)))
            self.db.execute("UPDATE jobs SET status=?, session_id=COALESCE(session_id, ?), updated_at=? WHERE job_id=?",
                            ("done" if outcome in TERMINAL_OUTCOMES or outcome == CUT_OUTCOME else "interrupted", result.get("session_id"), time.time(), job_id))
        return outcome

    def cancel_queued(self, policy_id: str, actor_id: str, note: str) -> list[str]:
        """Withdraw this origin's queued jobs of one manual and actor (fast race: a challenger that left plays no more)."""
        args = (policy_id, actor_id, self.origin)
        with self.tx():
            jobs = [r[0] for r in self.db.execute("SELECT job_id FROM jobs WHERE status='queued' AND policy_id=? AND actor_id=? AND origin=?", args)]
            self.db.execute("UPDATE jobs SET status='cancelled', note=?, updated_at=? WHERE status='queued' AND policy_id=? AND actor_id=? AND origin=?",
                            (note, time.time(), *args))
        return jobs

    def requeue_interrupted(self, job_id: str, note: str) -> str:
        """A new attempt for the same replicate slot; the interrupted attempt stays on record."""
        job = self.db.execute("SELECT * FROM jobs WHERE job_id=?", (job_id,)).fetchone()
        new_id = job_id.rsplit("-a", 1)[0] + f"-a{job['attempt'] + 1}"
        now = time.time()
        with self.tx():
            self.db.execute("INSERT OR IGNORE INTO jobs (job_id,policy_id,actor_id,env_id,purpose,replicate,attempt,status,priority,note,created_at,updated_at,origin) VALUES (?,?,?,?,?,?,?,'queued',?,?,?,?,?)",
                            (new_id, job["policy_id"], job["actor_id"], job["env_id"], job["purpose"], job["replicate"], job["attempt"] + 1, job["priority"], note, now, now, job["origin"]))
        return new_id

    def recover(self, owner_alive: callable) -> dict[str, int]:  # type: ignore[valid-type]
        """Reconcile leased/running jobs with real processes after a restart."""
        counts = {"ingested": 0, "interrupted": 0, "still_running": 0, "released": 0}
        for job in self.db.execute("SELECT * FROM jobs WHERE status IN ('leased','running') AND origin=?", (self.origin,)).fetchall():
            if owner_alive(job["lease_owner"]):
                counts["still_running"] += 1  # a live scheduler owns it, leased or running: never touch
                continue
            run_dir = Path(job["run_dir"]) if job["run_dir"] else None
            if run_dir and (run_dir / "result.json").exists():
                self.ingest(job["job_id"], run_dir)
                counts["ingested"] += 1
            elif job["status"] == "leased" and not job["pid"]:
                self.db.execute("UPDATE jobs SET status='queued', lease_owner=NULL, lease_expires=NULL, updated_at=? WHERE job_id=?", (time.time(), job["job_id"]))
                counts["released"] += 1
            else:
                self.db.execute("UPDATE jobs SET status='interrupted', note=?, updated_at=? WHERE job_id=?",
                                ("worker process gone without result.json", time.time(), job["job_id"]))
                counts["interrupted"] += 1
        return counts

    # -- decisions and exports ---------------------------------------------
    def decide(self, kind: str, subject: str | None, payload: dict[str, Any], rationale: str, in_tx: bool = False) -> None:
        self.db.execute("INSERT INTO decisions (at,kind,subject,payload,rationale,origin) VALUES (?,?,?,?,?,?)",
                        (time.time(), kind, subject, json.dumps(payload, sort_keys=True), rationale, self.origin))

    def cell_scores(self, policy_id: str, actor_id: str, env_id: str | None = None, purpose: str | None = None) -> list[float]:
        query = "SELECT score FROM evaluations WHERE policy_id=? AND actor_id=? AND outcome IN ('completed','eliminated')"
        args: list[Any] = [policy_id, actor_id]
        if env_id:
            query += " AND env_id=?"
            args.append(env_id)
        if purpose:
            query += " AND purpose=?"
            args.append(purpose)
        return [r[0] for r in self.db.execute(query, args).fetchall()]

    def export_jsonl(self, out_dir: Path, force: bool = False) -> dict[str, int]:
        """Write the registry as JSONL. Another origin exports only its own jobs, evaluations and decisions.

        Refuses (``ExportWouldDropRows``) when the folder already holds rows this
        registry lacks, e.g. a stale machine exporting over the race's results,
        unless ``force``. Run ``careerlab import`` first to pick those rows up.
        """
        own = {
            "jobs": "SELECT * FROM jobs WHERE origin=? ORDER BY rowid",
            "evaluations": "SELECT e.* FROM evaluations e JOIN jobs j USING(job_id) WHERE j.origin=? ORDER BY e.rowid",
            "decisions": "SELECT * FROM decisions WHERE origin=? ORDER BY rowid",
        }
        tables = {}
        for table in ("policies", "actors", "environments", "jobs", "evaluations", "decisions"):
            if self.origin and table in own:
                tables[table] = [dict(r) for r in self.db.execute(own[table], (self.origin,)).fetchall()]
            else:
                tables[table] = [dict(r) for r in self.db.execute(f"SELECT * FROM {table} ORDER BY rowid").fetchall()]
        if not self.origin:
            for table in ("target_budget_accounts","target_budget_events"):
                rows = [dict(r) for r in self.db.execute(f"SELECT * FROM {table} ORDER BY rowid")]
                if rows:
                    tables[table] = rows
        if not force:
            missing = {}
            for table, rows in tables.items():
                path, key = out_dir / f"{table}.jsonl", EXPORT_KEYS[table]
                if path.exists():
                    old = {json.loads(line)[key] for line in path.read_text().splitlines() if line.strip()}
                    lost = old - {r[key] for r in rows}
                    if lost:
                        missing[table] = len(lost)
            if missing:
                raise ExportWouldDropRows(f"{out_dir} has rows this registry lacks {missing}; run `careerlab import --dir {out_dir}` first")
        out_dir.mkdir(parents=True, exist_ok=True)
        counts = {}
        for table, rows in tables.items():
            for row in rows:
                for key in ("trajectory_path", "run_dir", "bundle_path", "db_root"):
                    if row.get(key):
                        row[key] = _portable(row[key])
            path = out_dir / f"{table}.jsonl"
            tmp = path.with_suffix(".tmp")
            tmp.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows))
            os.replace(tmp, path)
            counts[table] = len(rows)
        return counts


def import_jsonl(registry: "Registry", in_dir: Path, data_root: Path, lab_root: Path) -> dict[str, int]:
    """Load a JSONL export into an empty or older registry (cloud hand-off); existing rows are kept.

    Rows from another origin keep their origin, so they are never leased,
    recovered or counted in this registry's decisions; their decisions get new
    ids here. ``conflicts`` counts rows refused because a different row already
    holds their key or replicate slot (it should stay 0).

    Portable paths are re-rooted on this machine. Trajectory files stay on the
    machine that produced them; their SHA-256 in the evaluation rows keeps them
    verifiable when they are copied later.
    """
    counts: dict[str, int] = {}
    conflicts = 0
    for table in ("policies", "actors", "environments", "jobs", "evaluations", "decisions","target_budget_accounts","target_budget_events"):
        path = in_dir / f"{table}.jsonl"
        if not path.exists():
            continue
        if table.startswith("target_budget_") and registry.origin:
            raise ValueError("shared paid ledger may only be imported by the canonical cloud origin")
        cols = [r[1] for r in registry.db.execute(f"PRAGMA table_info({table})").fetchall()]
        n = 0
        with registry.tx():
            for line in path.read_text().splitlines():
                row = json.loads(line)
                for key in ("trajectory_path", "run_dir", "db_root", "bundle_path"):
                    value = row.get(key)
                    if value and value.startswith("careerlab-data/"):
                        row[key] = str(data_root / value.split("/", 2)[2]) if value.count("/") >= 2 else value
                    elif value and value.startswith("lab/"):
                        row[key] = str(lab_root / value[len("lab/"):])
                if table == "jobs" and row.get("status") in ("leased", "running"):
                    row.update(status="queued", lease_owner=None, lease_expires=None, pid=None)  # leases never travel
                if table in ("jobs", "decisions"):
                    row.setdefault("origin", "")
                if table == "decisions" and row["origin"] != registry.origin:
                    if registry.db.execute("SELECT 1 FROM decisions WHERE origin=? AND at=? AND kind=? AND subject IS ?",
                                           (row["origin"], row["at"], row["kind"], row.get("subject"))).fetchone():
                        continue
                    row.pop("decision_id", None)
                keys = [k for k in cols if k in row]
                cur = registry.db.execute(f"INSERT OR IGNORE INTO {table} ({','.join(keys)}) VALUES ({','.join('?' * len(keys))})",
                                          [row[k] for k in keys])
                if cur.rowcount == 0 and table in ("jobs", "evaluations"):
                    same = registry.db.execute(f"SELECT 1 FROM {table} WHERE job_id=? AND policy_id=?", (row["job_id"], row["policy_id"])).fetchone()
                    conflicts += 0 if same else 1
                n += 1
        counts[table] = n
    counts["conflicts"] = conflicts
    return counts


def _portable(path: str) -> str:
    """Store paths relative to the data or repository root so exports move between machines."""
    for marker in ("/careerlab-data/", "/lab/"):
        if marker in path:
            return path[path.index(marker) + 1:]
    return path


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False
