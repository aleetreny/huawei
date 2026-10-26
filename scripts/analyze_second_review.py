"""Archive quota-free twelve-month research and catalogue only months 7–12."""
from collections import Counter, defaultdict
import csv
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from careerlab.mcp_client import is_terminal, month_index
from scripts.first_review_search import node_key


def level(obs):
    return int(obs["current_state"]["status"]["level"][1:])


def confirmed(step):
    return step.get("applied") is True and not step.get("ambiguous") and step.get("reply", {}).get("success") is True


def summarize_record(r):
    observations = [o for s in r["steps"] for o in (s["before"], s["after"])] + ([r["final"]] if "final" in r else [])
    entry = next((o for o in observations if month_index(o) == 7 and not is_terminal(o)), None)
    promoted_steps = [s for s in r["steps"] if confirmed(s) and level(s["after"]) > level(s["before"])]
    first = any(month_index(s["after"]) <= 6 for s in promoted_steps)
    second = any(level(s["before"]) == 2 and level(s["after"]) >= 3 and month_index(s["after"]) <= 12 for s in promoted_steps)
    survived = r["outcome"] == "twelve_month_window"
    return {"run": r["run"], "arm": r["arm"], "outcome": r["outcome"],
        "reached_7": entry is not None, "entry_7": entry["current_state"] if entry else None,
        "first_promotion_by_6": first, "first_promoted_alive_at_7": first and entry is not None,
        "second_promotion_by_12": second, "second_promotion_and_alive": second and survived,
        "alive_through_12": survived, "error": r.get("error")}


def analyze(source_root, output):
    output.mkdir(parents=True, exist_ok=True)
    questions, edges, chains = {}, Counter(), Counter()
    reviews, outcomes, witnesses, effects = [], [], {}, []
    failures, batch_summaries = Counter(), {}
    for batch in sorted(source_root.iterdir()):
        paths = sorted(batch.glob("run-*.json")) if batch.is_dir() else []
        if not paths:
            continue
        dest = output / batch.name
        dest.mkdir(exist_ok=True)
        retained = [json.loads(path.read_text()) for path in paths]
        archive = dest / "public-trajectories.jsonl.gz"
        # Stable gzip metadata for reproducible repeated analysis.
        with archive.open("wb") as raw:
            with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
                for r in retained:
                    compressed.write((json.dumps(r, ensure_ascii=False)+"\n").encode())
        (dest / "archive-sha256.txt").write_text(hashlib.sha256(archive.read_bytes()).hexdigest()+"  "+archive.name+"\n")
        for name in ("manifest.json", "runner-source.py", "manual.md", "coverage-status.json", "initial-effects.json", "handbook.json"):
            if (batch/name).exists():
                shutil.copyfile(batch/name, dest/name)
        bc = Counter()
        for r in retained:
            outcome = {"batch": batch.name, **summarize_record(r)}
            outcomes.append(outcome)
            bc[r["outcome"]] += 1
            for metric in ("reached_7", "first_promotion_by_6", "first_promoted_alive_at_7", "second_promotion_by_12", "second_promotion_and_alive", "alive_through_12"):
                bc[metric] += outcome[metric]
            if r["outcome"] == "eliminated":
                final = r["final"]
                failures[f"month-{month_index(final)}/"+str(final["current_state"]["simulation_flags"].get("failure_reason"))] += 1
            previous_title = {}
            for index, s in enumerate(r["steps"]):
                before, after = s["before"], s["after"]
                month = month_index(before)
                text = after.get("events", "")
                if "Half-year performance bonus" in text and confirmed(s):
                    grade = text.split("Half-year performance bonus (")[1].split(")")[0]
                    reviews.append({"batch": batch.name, "run": r["run"], "step": index,
                        "before_month": month, "after_month": month_index(after),
                        "before": before["current_state"]["status"], "after": after["current_state"]["status"],
                        "choice": s["choice"], "promoted": level(after)>level(before), "grade": grade,
                        "review_events": text, "outcome": r["outcome"]})
                key = node_key(before)
                if s["phase"] == "event" and confirmed(s):
                    title = before["current_event"]["title"]
                    if title in previous_title and 7 <= month <= 12:
                        old_key, old_choice, old_month = previous_title[title]
                        chains[old_key, old_choice, key, old_month, month] += 1
                    previous_title[title] = (key, s["choice"]["choice"], month)
                if not 7 <= month <= 12:
                    continue
                event = before.get("current_event") or {}
                q = questions.setdefault(key, {"id": key, "phase": s["phase"], "event": event,
                    "choices": before["choices"], "seen": 0, "months": Counter(), "levels": Counter(), "answers": {}})
                q["seen"] += 1
                q["months"][month] += 1
                q["levels"][before["current_state"]["status"]["level"]] += 1
                if not confirmed(s):
                    continue
                choice = s["choice"]
                b, a = before["current_state"]["status"], after["current_state"]["status"]
                delta = {k: a[k]-v for k,v in b.items() if isinstance(v,(int,float)) and isinstance(a.get(k),(int,float))}
                ans = q["answers"].setdefault(str(choice["choice"]), {"action": choice["action"], "count": 0,
                    "delta_counts": Counter(), "successors": Counter(), "episode_outcomes": Counter(),
                    "second_promotion_episodes": 0, "examples": []})
                ans["count"] += 1
                ans["delta_counts"][json.dumps(delta,sort_keys=True)] += 1
                ans["successors"][node_key(after)] += 1
                ans["episode_outcomes"][r["outcome"]] += 1
                ans["second_promotion_episodes"] += outcome["second_promotion_by_12"]
                witness = {"batch": batch.name,"run": r["run"],"step": index,"month":month,"before": b,"after": a}
                if len(ans["examples"]) < 2:
                    ans["examples"].append(witness)
                witnesses.setdefault((key,choice["choice"]),witness)
                edges[key,choice["choice"],node_key(after)] += 1
                if s["phase"] in ("energy","main_action") and b["level"]==a["level"]:
                    for stat, advertised in choice.get("status_updates",{}).items():
                        if stat.lower() in delta:
                            effects.append({**witness,"action":choice["action"],"stat":stat,"advertised":advertised,"actual":delta[stat.lower()]})
        batch_summaries[batch.name]=dict(bc)
    ordered=sorted(questions.values(),key=lambda q:(q["phase"]!="event",q["event"].get("title",""),q["id"]))
    for q in ordered:
        q["untried_choices"]=[c["choice"] for c in q["choices"] if str(c["choice"]) not in q["answers"]]
    stories=[q for q in ordered if q["phase"]=="event"]
    all_pairs={(q["id"],c["choice"]) for q in ordered for c in q["choices"]}
    old=json.loads(Path("lab/reports/first-review-search/questions.json").read_text())
    old_titles={q["event"].get("title") for q in old if q["phase"]=="event"}
    old_keys={q["id"] for q in old}
    summary={"records":len(outcomes),"batches":batch_summaries,"outcomes":dict(Counter(r["outcome"] for r in outcomes)),
        "titles":len({q["event"]["title"] for q in stories}),"story_questions":len(stories),"questions":len(ordered),
        "story_available_answers":sum(len(q["choices"]) for q in stories),"story_tried_answers":sum(len(q["answers"]) for q in stories),
        "available_answers":len(all_pairs),"tried_answers":len(witnesses),
        "untried":[{"question":q["id"],"title":q["event"].get("title"),"choices":q["untried_choices"]} for q in ordered if q["untried_choices"]],
        "new_titles_vs_first_six": sorted({q["event"]["title"] for q in stories}-old_titles),
        "new_story_stages_vs_first_six":sum(q["id"] not in old_keys for q in stories),
        "failures":dict(failures),"review_clocks":dict(Counter(f"{r['before_month']}->{r['after_month']}" for r in reviews)),
        "second_review_grades":dict(Counter(r["grade"] for r in reviews if r["before_month"]>6)),
        "metrics":{k:sum(r[k] for r in outcomes) for k in ("reached_7","first_promotion_by_6","first_promoted_alive_at_7","second_promotion_by_12","second_promotion_and_alive","alive_through_12")},
        "conditional_first_promoted_alive_at_7": {"n":sum(r["first_promoted_alive_at_7"] for r in outcomes),
            "second_promotion":sum(r["second_promotion_by_12"] and r["first_promoted_alive_at_7"] for r in outcomes),
            "second_promotion_and_alive":sum(r["second_promotion_and_alive"] and r["first_promoted_alive_at_7"] for r in outcomes)},
        "limits":["Coverage of encountered questions only, not all hidden states or possible histories",
            "Adaptive research bots approximate the manual and consult public empirical effects; no Skill evaluation",
            "Associations and temporal edges do not establish causal effects",
            "Full raw prefixes retained; catalogue coverage restricted to action-before month 7–12",
            "Technical interruptions remain separate from failures"]}
    for name,obj in (("questions",ordered),("summary",summary),("reviews",reviews),("outcomes",outcomes),("quarterly-effects",effects)):
        (output/(name+".json")).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n")
    (output/"coverage-witnesses.json").write_text(json.dumps({"required":len(all_pairs),"witnessed":len(witnesses),
        "missing":[{"question":k,"choice":c} for k,c in sorted(all_pairs-set(witnesses))],
        "evidence":[{"question":k,"choice":c,**w} for (k,c),w in sorted(witnesses.items())]},indent=2,ensure_ascii=False)+"\n")
    for filename,header,rows in (("observed-edges.csv",["from","choice","to","count"],edges),
        ("same-title-chains.csv",["from","choice","to","from_month","to_month","count"],chains)):
        with (output/filename).open("w") as stream:
            w=csv.writer(stream);w.writerow(header);w.writerows((*k,v) for k,v in sorted(rows.items()))
    lines=["# Encountered month 7–12 questions", "", "Research catalogue; temporal branches and mixed-context effects are not causal treatment estimates.",""]
    for q in ordered:
        lines += [f"## {q['event'].get('title','?')} — {q['id']}","",q["event"].get("description",""),"",
            f"Phase: {q['phase']}; months: {dict(q['months'])}; levels: {dict(q['levels'])}.",""]
        for c in q["choices"]:
            a=q["answers"].get(str(c["choice"]))
            lines += [f"- {c['choice']}: {c['action']} — "+(f"{a['count']} executions; witnesses {a['examples']}" if a else "**UNTRIED**")]
        lines += [""]
    (output/"catalogue.md").write_text("\n".join(lines))
    print(json.dumps({k:v for k,v in summary.items() if k not in ("untried","failures","batches")},indent=2))


if __name__=="__main__":
    analyze(Path(sys.argv[1]),Path(sys.argv[2]))
