"""Temporal extraction from saved official replies, without invoking the game.

No model thoughts, notes or named-event answers are exported. Behaviour labels
refer only to published quarterly actions. Story choices remain unclassified.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any

STATE_KEYS = ("health", "dignity", "skill", "network", "level", "output", "wealth", "energy", "duration_in_level")
LABELS = {
    ("main", "Apply for a key project"): "growth",
    ("energy", "Prepare report materials"): "report",
    ("energy", "Defuse legacy risk"): "risk",
    ("energy", "Health recovery"): "recovery",
}
GRADE = re.compile(r"Half-year performance bonus \(([A-E][+-]?)\)")


def fingerprint(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def numeric_status(status: dict) -> dict:
    out = {}
    for key in STATE_KEYS:
        value = status.get(key)
        if key == "level" and isinstance(value, str) and re.fullmatch(r"L\d+", value):
            value = int(value[1:])
        out[key] = value if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) else None
    return out


def phase(obs: dict) -> str:
    title = (obs.get("current_event") or {}).get("title", "")
    return {"Quarterly energy allocation": "energy", "Quarterly main action": "main", "New hire handbook": "handbook"}.get(title, "story")


def label(stage: str, choice: dict) -> str:
    return LABELS.get((stage, choice.get("action")), "other_quarterly" if stage in {"energy", "main"} else "unclassified")


def _text(content: Any) -> str:
    if isinstance(content, str):
        return content
    return "".join(b.get("text", "") for b in content if isinstance(b, dict)) if isinstance(content, list) else ""


def _json_reply(block: dict) -> dict:
    try:
        reply = json.loads(_text(block.get("content")))
    except (ValueError, TypeError):
        return {}
    return reply if isinstance(reply, dict) else {}


def extract_streams(paths: list[Path]) -> tuple[list[dict], list[dict], dict]:
    """Consume observation once per action; match replies by call ID and session.

    An observation requested before an intervening action cannot become fresh
    on arrival. Multiple action calls without observing are never attributed to
    the same pre-state. State differences are next-observation changes, not
    isolated action effects, even when the month is unchanged.
    """
    pending = {}
    observations: list[dict] = []
    actions: list[dict] = []
    current = None
    generation = 0
    waiting_post = None
    problems = Counter()
    seen_call_ids = set()
    for path in paths:
        for line in path.read_text().splitlines():
            if not line.strip():
                continue
            entry = json.loads(line)
            content = (entry.get("message") or {}).get("content")
            for block in content if isinstance(content, list) else []:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "tool_use":
                    call_id = block["id"]
                    if call_id in seen_call_ids:
                        raise ValueError(f"Repeated call ID in transcript: {call_id}")
                    seen_call_ids.add(call_id)
                    tool = block["name"].split("__")[-1]
                    args = block.get("input") or {}
                    item = {"tool": tool, "generation": generation, "args": args}
                    if tool == "new_game":
                        generation += 1
                        current = None
                        waiting_post = None
                    if tool == "take_action":
                        state = current
                        item["pre"] = state
                        item["index"] = len(actions)
                        # The call itself invalidates the old observation, even
                        # if the action is later rejected or unanswered.
                        generation += 1
                        item["generation"] = generation
                        current = None
                        waiting_post = None
                        aligned = state is not None
                        if aligned and args.get("session_id") != state["session_id"]:
                            aligned = False
                            problems["session_mismatch"] += 1
                        obs = state["obs"] if aligned else {}
                        stage = phase(obs) if aligned else "unknown"
                        options = obs.get("choices") or []
                        chosen = next((c for c in options if c.get("choice") == args.get("choice")), None)
                        row = {
                            "index": len(actions), "call_key": fingerprint(call_id)[:20],
                            "aligned": aligned, "applied": None, "phase": stage,
                            "month": state["month"] if aligned else None,
                            "pre": state["status"] if aligned else None,
                            "observation_index": state["index"] if aligned else None,
                            "category": label(stage, chosen) if chosen else "unknown",
                            "energy_cost": chosen.get("energy_cost", 0) if chosen else None,
                            "choice_listed": chosen is not None,
                            "event_key": fingerprint((obs.get("current_event") or {}).get("title", ""))[:20] if aligned else None,
                            "option_set_key": fingerprint(options)[:20] if aligned else None,
                            "available_categories": sorted({label(stage, c) for c in options}),
                            "post": None, "post_month": None,
                        }
                        actions.append(row)
                    pending[call_id] = item
                elif block.get("type") == "tool_result":
                    item = pending.pop(block.get("tool_use_id"), None)
                    if item is None:
                        problems["unmatched_result"] += 1
                        continue
                    reply = _json_reply(block)
                    if item["tool"] == "observe":
                        state = reply.get("current_state") or {}
                        month = (state.get("time") or {}).get("current_month")
                        status = state.get("status")
                        session = state.get("session_id")
                        flags = state.get("simulation_flags") or {}
                        if not isinstance(month, int) or not isinstance(status, dict) or not session:
                            problems["invalid_observation"] += 1
                            continue
                        if item["args"].get("session_id") != session:
                            problems["session_mismatch"] += 1
                            continue
                        record = {
                            "index": len(observations), "month": month,
                            "status": numeric_status(status), "session_key": fingerprint(session)[:20],
                            "grades": GRADE.findall(reply.get("events") or ""),
                            "terminal": bool(reply.get("ending_score")) or flags.get("alive") is False,
                        }
                        observations.append(record)
                        if item["generation"] != generation:
                            problems["stale_observation_result"] += 1
                            continue
                        if waiting_post is not None:
                            previous = actions[waiting_post]
                            if previous.get("session_key") == record["session_key"]:
                                previous["post"] = record["status"]
                                previous["post_month"] = month
                            waiting_post = None
                        current = None if record["terminal"] else {
                            **record, "session_id": session, "obs": reply,
                        }
                    elif item["tool"] == "take_action":
                        row = actions[item["index"]]
                        row["applied"] = reply.get("success") if isinstance(reply.get("success"), bool) else None
                        if row["aligned"]:
                            row["session_key"] = fingerprint(item["pre"]["session_id"])[:20]
                        if row["applied"] and row["aligned"] and generation == item["generation"]:
                            waiting_post = item["index"]
    problems["unanswered_calls"] = len(pending)
    problems["unaligned_action_calls"] = sum(not r["aligned"] for r in actions)
    problems["unknown_action_results"] = sum(r["applied"] is None for r in actions)
    problems["listed_choice_misses"] = sum(r["aligned"] and not r["choice_listed"] for r in actions)
    return actions, observations, dict(problems)


def behaviour_features(actions: list[dict]) -> dict:
    accepted = [a for a in actions if a["aligned"] and a["applied"] and a["choice_listed"]]
    main = [a for a in accepted if a["phase"] == "main"]
    energy = [a for a in accepted if a["phase"] == "energy"]
    spent = sum(a["energy_cost"] or 0 for a in energy)
    result = {"prior_main_actions": len(main), "prior_energy_spent": spent}
    result["growth_share"] = sum(a["category"] == "growth" for a in main) / len(main) if main else None
    for category in ("report", "risk", "recovery"):
        result[category + "_share"] = sum((a["energy_cost"] or 0) for a in energy if a["category"] == category) / spent if spent else None
    return result


def build_episode(evaluation: dict, policy: dict, actions: list[dict], observations: list[dict], diagnostics: dict, landmarks: list[int]) -> dict:
    valid = [a for a in actions if a["aligned"] and a["choice_listed"] and a["applied"]]
    snapshots = {}
    for month in landmarks:
        at = next((a for a in actions if a["aligned"] and a["choice_listed"] and a["month"] == month), None)
        if at is not None:
            snapshots[str(month)] = {
                **at["pre"], **behaviour_features(actions[:at["index"]]),
                "observation_index": at["observation_index"], "action_index": at["index"],
                "behaviour_prefix_complete": all(a["aligned"] and a["choice_listed"] and a["applied"] is not None for a in actions[:at["index"]]),
            }
    grades = sorted({(o["month"], g) for o in observations for g in o["grades"]})
    start = observations[0] if observations else None
    quality = bool(start and start["month"] == 1 and start["status"]["level"] == 1 and len({o["session_key"] for o in observations}) == 1)
    # Missing states later in a game must not select the early prediction cohort.
    # Each snapshot is fresh by construction. Behaviour has its own prefix gate.
    quality = quality and not diagnostics.get("session_mismatch", 0)
    quality = quality and len(actions) == evaluation.get("steps")
    story = [a for a in valid if a["phase"] == "story" and a["post"] is not None and a["post_month"] == a["month"]]
    drops = [a for a in story if any(a["pre"].get(k) is not None and a["post"].get(k) is not None and a["post"][k] < a["pre"][k] for k in ("output", "network"))]
    return {
        "job_id": evaluation["job_id"], "actor_id": evaluation["actor_id"], "env_id": evaluation["env_id"],
        "policy_id": evaluation["policy_id"], "policy": policy["name"], "family": policy["family"],
        "purpose": evaluation["purpose"], "outcome": evaluation["outcome"],
        "Q": evaluation["score"], "completed": bool(evaluation["completed"]), "survival_months": evaluation["survival_months"],
        "quality_for_prediction": quality, "action_calls": len(actions), "accepted_aligned": len(valid),
        "whole_game_behaviour_complete": all(a["aligned"] and a["choice_listed"] and a["applied"] is not None for a in actions),
        "rejected": sum(a["applied"] is False for a in actions), "diagnostics": diagnostics,
        "first_observed_promotion_month": next((o["month"] for o in observations if (o["status"]["level"] or 0) > 1), None),
        "review_grades": [[m, g] for m, g in grades], "landmarks": snapshots,
        "behaviour_whole_game_descriptive_only": behaviour_features(actions),
        "same_month_story_transitions": len(story), "same_month_story_output_or_network_drop": len(drops),
    }


def ending_losses(result_path: Path, evaluation: dict) -> dict | None:
    if not result_path.is_file():
        return None
    result = json.loads(result_path.read_text())
    if result.get("job_id") != evaluation["job_id"] or abs((result.get("quantitative_score") or 0) - evaluation["score"]) > 0.011:
        raise ValueError("Result identity/score disagrees with evaluation")
    dims = (result.get("ending_score") or {}).get("dimensions") or []
    if not dims:
        return None
    # These weights come from saved public replies; they never enter a Skill.
    return {d["name"]: round(100 * d["weight"] - d["weighted_score"], 5) for d in dims}
