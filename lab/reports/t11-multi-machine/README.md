# T11: several machines play at once without overwriting each other

Leah, 26 Oct 2026, branch `leah/workspace`. Code in `careerlab/`; usage in [lab/README.md](../../README.md#playing-from-a-second-machine-t11).

## Problem

Before this change every machine numbered its games the same way: `<purpose>-<policy>-<actor>-<replicate>-a<attempt>`, with replicates counted from 0 in each registry. Two machines produced identical job ids and replicate slots for different games. On `import`, `INSERT OR IGNORE` silently kept one and dropped the other. `export` also rewrote `lab/registry/*.jsonl` from the local database alone, so a machine that had not imported the race would delete the race's rows in Git. Decision ids (autoincrement) collided as well.

## What changed

- **Origin.** `CAREERLAB_ORIGIN` or `careerlab origin set <name>` (untracked `.careerlab-origin`). No origin means the canonical race, so the cloud keeps working unchanged.
- **Registry.** `jobs` and `decisions` gain an `origin` column. It is added in place to existing databases with default `''`, so all current rows count as the race's.
  - Job ids get the origin as prefix.
  - Replicates start at a stable per-origin block (`origin_replicate_base`), so the `UNIQUE` replicate slot never clashes on merge.
  - `lease`, `recover`, scripted `resume` and `requeue_interrupted` stay inside the registry's own origin.
- **Decisions and reports.** `decisions.collect` (prereg-v1 launch order) and `report` count one origin only. Another machine's games can neither block nor enter the race's prefix. The frozen protocol is untouched.
- **Export.** Another origin exports only its own jobs, evaluations and decisions to `lab/registry-origins/<origin>/`. Every export refuses to write when the folder has rows the registry lacks (`ExportWouldDropRows`, CLI exit 4; `--force` overrides).
- **Import.** Rows keep their origin. Foreign decisions get new ids and are de-duplicated, so re-importing is idempotent. The result reports `conflicts`, which must be 0.
- **Data directory.** Defaults to `~/careerlab-data/huawei-<origin>`.

## Evidence

- `uv run pytest -q`: 230 passed. Five new tests are in `tests/test_origins.py`: disjoint ids and replicates, a two-way merge that never leases or decides foreign jobs, the export guard, in-place migration, and origin validation.
- End-to-end check on Leah's Mac (origin `leah`, throwaway data directory):
  - imported `lab/registry` (293 jobs, 249 evaluations, 0 conflicts);
  - ran 2 scripted `quarterly-wellbeing` games through the real engine: `leah-infr-ab6aa813-1cc25a-00002/3-a1`, replicates 254000002/3, eliminated, Q 15.87 and 10.75;
  - the race's 22 imported queued jobs stayed queued;
  - the origin export held only Leah's 4 jobs;
  - exporting over a copy of `lab/registry` was refused.
- First attempt interrupted (2 jobs, kept on record, never scored). The fresh venv lacked the dataset; `uv run career-emulator-engine update --source distribution --split dev` from the install section fixes it.

## Relevo

1. **Done.** T11 implemented as above. The decision: separate origins rather than a shared database or a lock, because the race runs in a cloud container that the Macs cannot reach. Merging stays an organiser action.
2. **Results.** Test numbers and the end-to-end run are above. No result files were committed; that check was infrastructure only, in a scratch data folder.
3. **Open.**
   - The cloud has not picked this up yet. Once `main` has it, the cloud's registry migrates itself on first open with no change of behaviour.
   - `scripts/cloud-run/*.py` on `cloud-lab-run` build their own SQL; they still see every origin. That is harmless until another origin's rows are imported into the race. The organiser should add `AND j.origin=''` to `queued` and `requeue_interrupted` in `driver.py` before merging any `lab/registry-origins/` folder.
   - The gate cap in `scheduler.check_gate` still counts every origin's jobs (conservative on purpose).
4. **Next for the organiser.**
   - Review and merge the PR from `leah/workspace`.
   - Then update ESTADO section 6, *Partidas*: other machines may play with an origin set.
   - Merge a machine's results with:

     ```sh
     uv run careerlab import --dir lab/registry-origins/<origin>
     ```
5. **ESTADO line.** T11: Leah, done on `leah/workspace`, waiting for review.
