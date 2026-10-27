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
    uv run careerlab origin set leah             # this machine plays as origin 'leah' (T11)
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
        "origin": s.origin or "(canonical race)", "registry_export_dir": str(s.registry_export_dir),
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


def _register(reg: Registry, src: Path, by: str, allow_lint_errors: bool = False, titles: set[str] | None = None) -> str:
    """Lint and register a policy folder; returns its id or raises ValueError with the reason."""
    meta = json.loads((src / "policy.json").read_text())
    errors = []
    if not (src / "bundle" / "scripted.json").exists():
        from careerlab.compliance import lint_bundle

        errors = [f for f in lint_bundle(src / "bundle", titles) if f.severity == "error"]
    if errors and not allow_lint_errors:
        raise ValueError("compliance errors:\n" + "\n".join(map(str, errors)))
    parents = []
    for parent in meta.get("parents", []):  # policy.json may name parents; the registry stores ids
        row = reg.db.execute("SELECT policy_id FROM policies WHERE policy_id=? OR name=?", (parent, parent)).fetchone()
        if row is None:
            raise ValueError(f"unknown parent {parent!r}: register it first")
        parents.append(row[0])
    return reg.register_policy(src / "bundle", meta["family"], meta["name"], parents,
                               meta["hypothesis"], meta.get("change", ""), created_by=by, meta=meta)


def _known_titles(s) -> set[str]:
    """Story-event titles from local runs plus the committed teacher digests (as scripts/cloud-run/lint.py)."""
    import re

    from careerlab.compliance import collect_titles

    titles = set(collect_titles(s.runs_dir)) if s.runs_dir.exists() else set()
    for f in (s.lab_dir / "reports" / "teacher-digests").rglob("*-a[0-9].md"):
        for line in f.read_text(encoding="utf-8").splitlines():
            m = re.match(r"- M\d+ \[[^\]]*\] (.+?) → ", line)
            if m and not m.group(1).startswith("Quarterly "):
                titles.add(m.group(1).strip())
    return titles


def cmd_register(args: argparse.Namespace) -> int:
    s = load_settings()
    try:
        print(_register(s.registry(), Path(args.path).resolve(), args.by, args.allow_lint_errors))
    except ValueError as exc:
        print(exc)
        return 2
    return 0


def _actor(reg: Registry, spec: str) -> tuple[str, str]:
    kind, _, name = spec.partition(":")
    if kind == "scripted":
        import hashlib

        import careerlab.actors.scripted as scripted

        code = hashlib.sha256(Path(scripted.__file__).read_bytes()).hexdigest()[:16]
        return reg.register_actor("scripted", {"name": name or "python-executor", "code_sha256": code}), kind
    if kind == "claude-cli":
        # <model>[@effort][~autocompact][#plugin][^stop month]  e.g. opus@low~100k, haiku#plugin, haiku^6
        from careerlab.actors.claude_cli import ClaudeWorkerConfig, cli_version

        name, _, stop = name.partition("^")
        skills_mode = "plugin" if name.endswith("#plugin") else "inline"
        name = name.removesuffix("#plugin")
        name, _, compact = name.partition("~")
        model, _, effort = name.partition("@")
        cfg = ClaudeWorkerConfig(model=model, effort=effort or None, autocompact=compact or None,
                                 skills_mode=skills_mode, cli_version=cli_version(load_settings()),
                                 stop_at_month=int(stop) if stop else None)
        return reg.register_actor("claude-cli", cfg.record()), kind
    raise SystemExit(f"unknown actor kind {kind}")


def cmd_lint(args: argparse.Namespace) -> int:
    from careerlab.compliance import collect_titles, lint_bundle

    s = load_settings()
    titles = collect_titles(s.runs_dir) if s.runs_dir.exists() else set()
    findings = lint_bundle(Path(args.path) / "bundle", titles)
    print("\n".join(map(str, findings)) or "no findings")
    return 2 if any(f.severity == "error" for f in findings) else 0


def cmd_enqueue(args: argparse.Namespace) -> int:
    from careerlab.scheduler import check_gate

    s = load_settings()
    reg = s.registry()
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
    sched = Scheduler(s, s.registry())
    print("recovered:", sched.recover())
    if args.kind == "scripted":
        print(asyncio.run(sched.run_scripted(slots=args.slots, limit=args.limit, purpose=args.purpose)))
    elif args.continuous:
        stop = Path(args.stop_file) if args.stop_file else s.data_dir / "fastloop" / "STOP-SCHEDULER"
        print(asyncio.run(sched.run_claude_continuous(args.slots, stop, max_five_hour=args.max_five_hour, purpose=args.purpose)))
    else:
        print(asyncio.run(sched.run_claude(concurrency=args.slots, limit=args.limit, purpose=args.purpose,
                                           max_five_hour=args.max_five_hour)))
    return 0


def cmd_recover(args: argparse.Namespace) -> int:
    from careerlab.scheduler import Scheduler

    s = load_settings()
    print(Scheduler(s, s.registry()).recover())
    return 0


def cmd_resume(args: argparse.Namespace) -> int:
    from careerlab.scheduler import Scheduler

    s = load_settings()
    sched = Scheduler(s, s.registry())
    print("recovered:", sched.recover())
    print("resumed:", asyncio.run(sched.resume_scripted()))
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    s = load_settings()
    reg = s.registry()
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
    rep = cell_report(s.registry(), purpose=args.purpose, all_origins=args.all_origins)
    print(markdown(rep) if args.markdown else json.dumps(rep, indent=2))
    return 0


def cmd_package(args: argparse.Namespace) -> int:
    from careerlab.package import package

    s = load_settings()
    rec = package(s, s.registry(), args.policy, Path(args.out), Path(args.design),
                  Path(args.video) if args.video else None, Path(args.readme) if args.readme else None)
    print(json.dumps(rec, indent=2))
    return 0 if rec["validator_exit"] == 0 else 3


def cmd_import(args: argparse.Namespace) -> int:
    from careerlab.store import import_jsonl

    s = load_settings()
    print(import_jsonl(s.registry(), Path(args.dir or s.lab_dir / "registry"), s.data_dir, s.lab_dir))
    return 0


def cmd_digest(args: argparse.Namespace) -> int:
    from careerlab.digest import digest

    s = load_settings()
    rows = digest(s.registry(), args.model, Path(args.out))
    print(json.dumps([{k: r[k] for k in ("job_id", "policy", "actor", "outcome", "Q", "grades")} for r in rows], indent=2))
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    from careerlab.store import ExportWouldDropRows

    s = load_settings()
    try:
        print(s.registry_export_dir, s.registry().export_jsonl(s.registry_export_dir, force=args.force))
    except ExportWouldDropRows as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 4
    return 0


def cmd_ladder(args: argparse.Namespace) -> int:
    """Fast race (lab/fastloop/README.md): init, add, step, status."""
    import time

    from careerlab import ladder

    s = load_settings()
    reg = s.registry()
    path = s.lab_dir / "fastloop" / "state.json"
    cfg = ladder.LadderConfig()
    now = time.time()
    if args.action == "init":
        if path.exists() and not args.force:
            print(f"{path} exists; use --force to start over")
            return 2
        actor = args.actor or "08e9167a965ed82c"
        state = ladder.new_state(reg, actor, cfg, now, ladder.resolve_policy(reg, args.ref) if args.ref else None)
        if args.cancel_others:  # nothing else plays: only the champion and the challengers added next
            for (pid,) in reg.db.execute("SELECT DISTINCT policy_id FROM jobs WHERE status='queued' AND actor_id=? AND origin=?",
                                         (actor, reg.origin)).fetchall():
                if pid != state["champion"]:
                    jobs = reg.cancel_queued(pid, actor, "fast race started: only the champion and its challengers play")
                    reg.decide("ladder_cancel", pid, {"jobs": jobs}, "fast race started (fastloop-v2)")
        reg.decide("ladder_init", state["champion"], {"actor_id": actor, "env_id": state["env_id"]}, args.why or "fast race started (fastloop-v2)")
        ladder.save_state(path, state)
        print(json.dumps({"champion": state["entries"][state["champion"]]["name"], "state": str(path)}))
        return 0
    state = ladder.load_state(path)
    if args.action == "add":
        src = Path(args.ref)
        try:
            if (src / "policy.json").exists():
                from careerlab.compliance import _lint_policy_json

                bad = [f for f in _lint_policy_json(src.resolve(), src.resolve() / "bundle", (s.lab_dir / "policies-src").resolve())
                       if f.severity == "error"]
                if bad:
                    raise ValueError("compliance errors:\n" + "\n".join(map(str, bad)))
                pid = _register(reg, src.resolve(), "fastloop", titles=_known_titles(s))
            else:
                pid = ladder.resolve_policy(reg, args.ref)
        except ValueError as exc:
            print(exc)
            return 2
        name = ladder.policy_names(reg)[pid]
        state = ladder.add(state, pid, name, args.kind, now, first=args.first, note=args.why or "")
        reg.decide("ladder_add", pid, {"kind": args.kind, "first": args.first}, args.why or f"{args.kind} challenger")
        ladder.save_state(path, state)
        print(json.dumps({"policy_id": pid, "name": name, "kind": args.kind}))
        return 0
    if args.action == "step":
        new, actions = ladder.run_step(reg, path, cfg, apply_changes=args.apply, in_flight=args.in_flight or [], now=now)
        print(json.dumps([vars(a) for a in actions], indent=1))
        return 0
    if args.action == "status":
        page = ladder.report_es(state, cfg, now)
        if args.write:
            (s.lab_dir / "reports" / "carrera-rapida.md").write_text(page, encoding="utf-8")
            (s.lab_dir / "fastloop" / "history.md").write_text(ladder.history_md(state, reg), encoding="utf-8")
        print(page)
        return 0
    return 2


def cmd_origin(args: argparse.Namespace) -> int:
    from careerlab.config import ORIGIN_FILE, check_origin

    if args.action == "set":
        if not args.name:
            print("usage: careerlab origin set <name>", file=sys.stderr)
            return 2
        ORIGIN_FILE.write_text(check_origin(args.name) + "\n")
    elif args.action == "clear":
        ORIGIN_FILE.unlink(missing_ok=True)
    s = load_settings()
    print(json.dumps({"origin": s.origin or "(canonical race)", "data_dir": str(s.data_dir),
                      "registry_export_dir": str(s.registry_export_dir)}, indent=2))
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
    lt = sub.add_parser("lint", help="check a policy folder (policy.json + bundle/) against the compliance rules, without registering it")
    lt.add_argument("path")
    lt.set_defaults(fn=cmd_lint)
    e = sub.add_parser("enqueue")
    e.add_argument("--policy", required=True)
    e.add_argument("--actor", required=True, help="scripted[:python-executor] | claude-cli:<model>[@effort][~autocompact][#plugin][^stop month]")
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
    run.add_argument("--continuous", action="store_true", help="claude-cli: lease one job per free slot until --stop-file exists (fast race)")
    run.add_argument("--stop-file", help="default: <data dir>/fastloop/STOP-SCHEDULER")
    run.set_defaults(fn=cmd_run)
    ld = sub.add_parser("ladder", help="fast race: one champion, challengers climb 2/4/8/12 games (lab/fastloop/README.md)")
    ld.add_argument("action", choices=["init", "add", "step", "status"])
    ld.add_argument("ref", nargs="?", help="init: champion name or id (default: best expected score with 8+ games); add: policy folder or name/id")
    ld.add_argument("--kind", default="targeted", choices=["targeted", "stretch", "bold", "external"])
    ld.add_argument("--first", type=int, default=2, choices=[2, 4], help="add: 4 for a manual with strong evidence from elsewhere")
    ld.add_argument("--actor", help="init: race actor id (default: the Haiku race cell 08e9167a965ed82c)")
    ld.add_argument("--cancel-others", action="store_true", help="init: cancel every other queued job of the race actor")
    ld.add_argument("--force", action="store_true")
    ld.add_argument("--apply", action="store_true", help="step: write the actions to the registry and the state file")
    ld.add_argument("--in-flight", nargs="*", help="step: kinds of designs already being written")
    ld.add_argument("--write", action="store_true", help="status: also write lab/reports/carrera-rapida.md and lab/fastloop/history.md")
    ld.add_argument("--why")
    ld.set_defaults(fn=cmd_ladder)
    sub.add_parser("recover").set_defaults(fn=cmd_recover)
    sub.add_parser("resume").set_defaults(fn=cmd_resume)
    sub.add_parser("status").set_defaults(fn=cmd_status)
    rp = sub.add_parser("report")
    rp.add_argument("--purpose")
    rp.add_argument("--markdown", action="store_true")
    rp.add_argument("--all-origins", action="store_true", help="include runs imported from other machines")
    rp.set_defaults(fn=cmd_report)
    pk = sub.add_parser("package")
    pk.add_argument("--policy", required=True)
    pk.add_argument("--out", required=True)
    pk.add_argument("--design", required=True, help="directory with skills_design.md and decision_report.md")
    pk.add_argument("--video")
    pk.add_argument("--readme")
    pk.set_defaults(fn=cmd_package)
    dg = sub.add_parser("digest", help="compact digests of one worker model's finished games, for trace-driven children")
    dg.add_argument("--model", required=True)
    dg.add_argument("--out", required=True)
    dg.set_defaults(fn=cmd_digest)
    ex = sub.add_parser("export", help="registry -> lab/registry/ (race) or lab/registry-origins/<origin>/")
    ex.add_argument("--force", action="store_true", help="overwrite even if the folder has rows this registry lacks")
    ex.set_defaults(fn=cmd_export)
    og = sub.add_parser("origin", help="show, set or clear this machine's origin (T11)")
    og.add_argument("action", nargs="?", choices=["show", "set", "clear"], default="show")
    og.add_argument("name", nargs="?")
    og.set_defaults(fn=cmd_origin)
    im = sub.add_parser("import", help="load lab/registry/*.jsonl into this machine's registry (hand-off)")
    im.add_argument("--dir")
    im.set_defaults(fn=cmd_import)
    args = parser.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
