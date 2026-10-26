"""careerlab command line.

    uv run careerlab doctor                      # versions, paths, account, gate
    uv run careerlab isolation                   # official-interface isolation checks
    uv run careerlab bench --slots 16 --episodes 96
    uv run careerlab register lab/policies-src/F1-steady-balance/f1-v1
    uv run careerlab enqueue --policy <id> --actor scripted:quarterly-wellbeing --n 20 --purpose pilot
    uv run careerlab run --kind scripted --slots 8
    uv run careerlab recover                     # reconcile jobs with real processes
    uv run careerlab status
    uv run careerlab export                      # registry -> lab/registry/*.jsonl for Git
"""

from __future__ import annotations

import argparse
import asyncio
import json
import subprocess
import sys
from importlib.metadata import version
from pathlib import Path

from careerlab.config import OFFICIAL_ENGINE_ENV, load_settings
from careerlab.store import Registry


def _env_fingerprint(environment: str) -> dict:
    return {
        "environment": environment,
        "engine": version("career-emulator-engine"),
        "dataset": version("career-emulator-techarena"),
        "fastmcp": version("fastmcp"),
        "engine_env": dict(OFFICIAL_ENGINE_ENV),
        "split": "dev",
        "transport": "stdio",
        "runner": "careerlab-pool",
    }


def cmd_doctor(args: argparse.Namespace) -> int:
    s = load_settings()
    info = {
        "data_dir": str(s.data_dir), "lab_dir": str(s.lab_dir), "runner_dir": str(s.runner_dir),
        "mcp_executable": s.mcp_executable, "claude_executable": s.claude_executable,
        "versions": {p: version(p) for p in ("career-emulator-engine", "career-emulator-techarena", "fastmcp", "mcp")},
        "engine_env": OFFICIAL_ENGINE_ENV,
        "official_runner_present": (s.runner_dir / "career_sim_runner").is_dir(),
        "gate": json.loads((s.lab_dir / "gate.json").read_text())["environments"]["real-dev"]["actors"],
    }
    try:
        auth = json.loads(subprocess.run([s.claude_executable, "auth", "status"], capture_output=True, text=True, timeout=30).stdout)
        info["claude_cli"] = {k: auth.get(k) for k in ("loggedIn", "authMethod", "subscriptionType")}
    except Exception as exc:  # the CLI is optional for scripted work
        info["claude_cli"] = f"unavailable: {exc!r}"
    print(json.dumps(info, indent=2))
    return 0


def cmd_isolation(args: argparse.Namespace) -> int:
    from careerlab.diagnostics import check_isolation

    print(json.dumps(asyncio.run(check_isolation(load_settings())), indent=2))
    return 0


def cmd_bench(args: argparse.Namespace) -> int:
    from careerlab.bench import bench

    print(json.dumps(asyncio.run(bench(load_settings(), args.slots, args.per_slot, args.episodes, actor=args.actor)), indent=2))
    return 0


def cmd_register(args: argparse.Namespace) -> int:
    s = load_settings()
    reg = Registry(s.registry_path)
    src = Path(args.path).resolve()
    meta = json.loads((src / "policy.json").read_text())
    errors = []
    if not (src / "bundle" / "scripted.json").exists():
        from careerlab.compliance import lint_bundle

        errors = [f for f in lint_bundle(src / "bundle") if f.severity == "error"]
    if errors and not args.allow_lint_errors:
        print("compliance errors:\n" + "\n".join(map(str, errors)))
        return 2
    parents = []
    for parent in meta.get("parents", []):  # policy.json may name parents; the registry stores ids
        row = reg.db.execute("SELECT policy_id FROM policies WHERE policy_id=? OR name=?", (parent, parent)).fetchone()
        if row is None:
            print(f"unknown parent {parent!r}: register it first")
            return 2
        parents.append(row[0])
    policy_id = reg.register_policy(src / "bundle", meta["family"], meta["name"], parents,
                                    meta["hypothesis"], meta.get("change", ""), created_by=args.by, meta=meta)
    print(policy_id)
    return 0


def _actor(reg: Registry, spec: str) -> tuple[str, str]:
    kind, _, name = spec.partition(":")
    if kind == "scripted":
        import hashlib

        import careerlab.actors.scripted as scripted

        code = hashlib.sha256(Path(scripted.__file__).read_bytes()).hexdigest()[:16]
        return reg.register_actor("scripted", {"name": name or "python-executor", "code_sha256": code}), kind
    if kind == "claude-cli":
        # <model>[@effort][~autocompact][#plugin]  e.g. opus@low~100k, haiku#plugin
        from careerlab.actors.claude_cli import ClaudeWorkerConfig, cli_version

        skills_mode = "plugin" if name.endswith("#plugin") else "inline"
        name = name.removesuffix("#plugin")
        name, _, compact = name.partition("~")
        model, _, effort = name.partition("@")
        cfg = ClaudeWorkerConfig(model=model, effort=effort or None, autocompact=compact or None,
                                 skills_mode=skills_mode, cli_version=cli_version(load_settings()))
        return reg.register_actor("claude-cli", cfg.record()), kind
    raise SystemExit(f"unknown actor kind {kind}")


def cmd_enqueue(args: argparse.Namespace) -> int:
    from careerlab.scheduler import check_gate

    s = load_settings()
    reg = Registry(s.registry_path)
    actor_id, kind = _actor(reg, args.actor)
    env_id = reg.register_environment(_env_fingerprint(args.environment))
    check_gate(s, reg, kind, args.environment, args.n)
    jobs = reg.enqueue(args.policy, actor_id, env_id, args.purpose, args.n, priority=args.priority)
    reg.decide("enqueue", args.policy, {"actor": args.actor, "n": args.n, "purpose": args.purpose, "jobs": jobs}, args.why)
    print(json.dumps(jobs))
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    from careerlab.scheduler import Scheduler

    s = load_settings()
    sched = Scheduler(s, Registry(s.registry_path))
    print("recovered:", sched.recover())
    if args.kind == "scripted":
        print(asyncio.run(sched.run_scripted(slots=args.slots, limit=args.limit, purpose=args.purpose)))
    else:
        print(asyncio.run(sched.run_claude(concurrency=args.slots, limit=args.limit, purpose=args.purpose,
                                           max_five_hour=args.max_five_hour)))
    return 0


def cmd_recover(args: argparse.Namespace) -> int:
    from careerlab.scheduler import Scheduler

    s = load_settings()
    print(Scheduler(s, Registry(s.registry_path)).recover())
    return 0


def cmd_resume(args: argparse.Namespace) -> int:
    from careerlab.scheduler import Scheduler

    s = load_settings()
    sched = Scheduler(s, Registry(s.registry_path))
    print("recovered:", sched.recover())
    print("resumed:", asyncio.run(sched.resume_scripted()))
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    s = load_settings()
    reg = Registry(s.registry_path)
    rows = reg.db.execute(
        "SELECT p.name, a.kind, json_extract(a.config,'$.name') AS actor, e.purpose, COUNT(*) AS n, "
        "SUM(e.outcome='completed') AS completed, SUM(e.outcome='interrupted') AS interrupted, "
        "ROUND(AVG(CASE WHEN e.outcome!='interrupted' THEN e.score END),2) AS mean_q, ROUND(AVG(e.survival_months),1) AS months "
        "FROM evaluations e JOIN policies p USING(policy_id) JOIN actors a USING(actor_id) GROUP BY 1,2,3,4 ORDER BY 1").fetchall()
    jobs = reg.db.execute("SELECT status, COUNT(*) FROM jobs GROUP BY status").fetchall()
    print(json.dumps({"jobs": {r[0]: r[1] for r in jobs}, "cells": [dict(r) for r in rows]}, indent=2))
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    from careerlab.report import cell_report, markdown

    s = load_settings()
    rep = cell_report(Registry(s.registry_path), purpose=args.purpose)
    print(markdown(rep) if args.markdown else json.dumps(rep, indent=2))
    return 0


def cmd_package(args: argparse.Namespace) -> int:
    from careerlab.package import package

    s = load_settings()
    rec = package(s, Registry(s.registry_path), args.policy, Path(args.out), Path(args.design),
                  Path(args.video) if args.video else None, Path(args.readme) if args.readme else None)
    print(json.dumps(rec, indent=2))
    return 0 if rec["validator_exit"] == 0 else 3


def cmd_export(args: argparse.Namespace) -> int:
    s = load_settings()
    print(Registry(s.registry_path).export_jsonl(s.lab_dir / "registry"))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="careerlab")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("doctor").set_defaults(fn=cmd_doctor)
    sub.add_parser("isolation").set_defaults(fn=cmd_isolation)
    b = sub.add_parser("bench")
    b.add_argument("--slots", type=int, default=8)
    b.add_argument("--per-slot", type=int, default=1)
    b.add_argument("--episodes", type=int, default=64)
    b.add_argument("--actor", default="uniform-affordable")
    b.set_defaults(fn=cmd_bench)
    r = sub.add_parser("register")
    r.add_argument("path")
    r.add_argument("--by", default="orchestrator")
    r.add_argument("--allow-lint-errors", action="store_true")
    r.set_defaults(fn=cmd_register)
    e = sub.add_parser("enqueue")
    e.add_argument("--policy", required=True)
    e.add_argument("--actor", required=True, help="scripted[:python-executor] | claude-cli:<model>[@effort][~autocompact][#plugin]")
    e.add_argument("--n", type=int, required=True)
    e.add_argument("--purpose", default="pilot", choices=["pilot", "screen", "calibrate", "audit", "confirm", "infra"])
    e.add_argument("--environment", default="real-dev", choices=["real-dev", "synthetic"])
    e.add_argument("--priority", type=float, default=0.0)
    e.add_argument("--why", required=True, help="decision rationale recorded in the registry")
    e.set_defaults(fn=cmd_enqueue)
    run = sub.add_parser("run")
    run.add_argument("--kind", choices=["scripted", "claude-cli"], default="scripted")
    run.add_argument("--slots", type=int, default=8)
    run.add_argument("--limit", type=int)
    run.add_argument("--purpose")
    run.add_argument("--max-five-hour", type=float, default=0.75, help="pause new Claude episodes above this five-hour utilisation")
    run.set_defaults(fn=cmd_run)
    sub.add_parser("recover").set_defaults(fn=cmd_recover)
    sub.add_parser("resume").set_defaults(fn=cmd_resume)
    sub.add_parser("status").set_defaults(fn=cmd_status)
    rp = sub.add_parser("report")
    rp.add_argument("--purpose")
    rp.add_argument("--markdown", action="store_true")
    rp.set_defaults(fn=cmd_report)
    pk = sub.add_parser("package")
    pk.add_argument("--policy", required=True)
    pk.add_argument("--out", required=True)
    pk.add_argument("--design", required=True, help="directory with skills_design.md and decision_report.md")
    pk.add_argument("--video")
    pk.add_argument("--readme")
    pk.set_defaults(fn=cmd_package)
    sub.add_parser("export").set_defaults(fn=cmd_export)
    args = parser.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
