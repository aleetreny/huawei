"""T11: several machines play at once without clashing with the race's results."""

import json
import shutil

import pytest

from careerlab.store import ExportWouldDropRows, Registry, import_jsonl
from test_core import FakeClient, run


def _setup(tmp_path, name, origin):
    reg = Registry(tmp_path / f"{name}.sqlite3", origin=origin)
    bundle = tmp_path / "bundle"
    if not bundle.exists():
        bundle.mkdir()
        (bundle / "scripted.json").write_text('{"rule_set": "first"}')
    pid = reg.register_policy(bundle, "fam", "p", [], "h", "c", "test")
    aid = reg.register_actor("scripted", {"name": "x"})
    eid = reg.register_environment({"environment": "test"})
    return reg, pid, aid, eid


def _play(reg, tmp_path, job):
    reg.lease("owner", 1)
    run(FakeClient(), tmp_path, job)
    reg.ingest(job, tmp_path / job)


def test_origins_get_disjoint_job_ids_and_replicates(tmp_path):
    cloud, pid, aid, eid = _setup(tmp_path, "cloud", "")
    leah, *_ = _setup(tmp_path, "leah", "leah")
    c = cloud.enqueue(pid, aid, eid, "screen", 2)
    l = leah.enqueue(pid, aid, eid, "screen", 2)
    assert not set(c) & set(l) and all(j.startswith("leah-scre-") for j in l)
    reps = lambda reg: {r[0] for r in reg.db.execute("SELECT replicate FROM jobs")}
    assert reps(cloud) == {0, 1} and not reps(cloud) & reps(leah)
    assert leah.requeue_interrupted(l[0], "x").startswith("leah-") and leah.db.execute(
        "SELECT origin FROM jobs WHERE attempt=2").fetchone()[0] == "leah"


def test_merge_keeps_both_machines_and_never_runs_or_decides_foreign_jobs(tmp_path):
    from careerlab.decisions import collect

    cloud, pid, aid, eid = _setup(tmp_path, "cloud", "")
    leah, *_ = _setup(tmp_path, "leah", "leah")
    cj = cloud.enqueue(pid, aid, eid, "screen", 1)
    lj = leah.enqueue(pid, aid, eid, "screen", 2)
    _play(cloud, tmp_path, cj[0])
    _play(leah, tmp_path, lj[0])
    leah.decide("note", aid, {}, "local")
    cloud.decide("block_decision", aid, {}, "race")

    cloud.export_jsonl(tmp_path / "registry")
    import_jsonl(leah, tmp_path / "registry", tmp_path / "d", tmp_path / "lab")  # Leah picks up the race
    leah.export_jsonl(tmp_path / "registry-origins" / "leah")
    jobs = [json.loads(x) for x in (tmp_path / "registry-origins" / "leah" / "jobs.jsonl").read_text().splitlines()]
    assert {j["job_id"] for j in jobs} == set(lj)  # only her own jobs travel

    counts = import_jsonl(cloud, tmp_path / "registry-origins" / "leah", tmp_path / "d", tmp_path / "lab")
    assert counts["conflicts"] == 0
    assert cloud.db.execute("SELECT COUNT(*) FROM evaluations").fetchone()[0] == 2
    assert [r["job_id"] for r in cloud.lease("cloud-owner", 10)] == []  # Leah's queued job is not the race's to run
    assert len(collect(cloud, aid)[pid]["launches"]) == 1  # prereg decisions see only the race's launches
    kinds = cloud.db.execute("SELECT kind, origin FROM decisions ORDER BY decision_id").fetchall()
    assert [tuple(k) for k in kinds] == [("block_decision", ""), ("note", "leah")]
    import_jsonl(cloud, tmp_path / "registry-origins" / "leah", tmp_path / "d", tmp_path / "lab")  # idempotent
    assert cloud.db.execute("SELECT COUNT(*) FROM decisions").fetchone()[0] == 2


def test_export_refuses_to_drop_rows_it_does_not_have(tmp_path):
    cloud, pid, aid, eid = _setup(tmp_path, "cloud", "")
    cloud.enqueue(pid, aid, eid, "screen", 2)
    cloud.export_jsonl(tmp_path / "registry")
    stale, *_ = _setup(tmp_path, "stale", "")  # a second machine without the race's rows
    with pytest.raises(ExportWouldDropRows):
        stale.export_jsonl(tmp_path / "registry")
    assert len((tmp_path / "registry" / "jobs.jsonl").read_text().splitlines()) == 2
    import_jsonl(stale, tmp_path / "registry", tmp_path / "d", tmp_path / "lab")
    stale.export_jsonl(tmp_path / "registry")  # fine once it has them


def test_old_registry_is_migrated_in_place(tmp_path):
    reg, pid, aid, eid = _setup(tmp_path, "old", "")
    reg.enqueue(pid, aid, eid, "screen", 1)
    reg.db.close()
    shutil.copy(tmp_path / "old.sqlite3", tmp_path / "copy.sqlite3")
    again = Registry(tmp_path / "copy.sqlite3")
    assert again.db.execute("SELECT origin FROM jobs").fetchone()[0] == ""


def test_origin_names_are_checked(monkeypatch):
    from careerlab import config

    with pytest.raises(ValueError):
        config.check_origin("Leah/../x")
    monkeypatch.setenv("CAREERLAB_ORIGIN", "leah")
    monkeypatch.delenv("CAREERLAB_DATA", raising=False)
    s = config.Settings()
    assert s.origin == "leah" and s.data_dir.name == "huawei-leah" and s.registry_export_dir.parts[-2:] == ("registry-origins", "leah")
