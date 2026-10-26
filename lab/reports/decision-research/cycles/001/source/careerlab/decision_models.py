"""Small nested grouped ridge comparisons for historical prediction, not causality."""

from __future__ import annotations

from collections import Counter

import numpy as np


def grouped_folds(groups, n_splits: int, seed: int):
    """Keep complete groups together; deterministic size balance without outcomes."""
    groups = np.asarray(groups)
    counts = Counter(groups.tolist())
    if len(counts) < 2:
        raise ValueError("At least two groups required")
    n_splits = min(n_splits, len(counts))
    rng = np.random.default_rng(seed)
    keys = list(counts)
    rng.shuffle(keys)
    keys.sort(key=lambda key: -counts[key])
    bins, sizes = [set() for _ in range(n_splits)], [0] * n_splits
    for key in keys:
        slot = int(np.argmin(sizes))
        bins[slot].add(key)
        sizes[slot] += counts[key]
    for held in bins:
        test = np.flatnonzero(np.isin(groups, list(held)))
        train = np.flatnonzero(~np.isin(groups, list(held)))
        yield train, test


def ridge_fit(X, y, alpha: float) -> dict:
    X, y = np.asarray(X, dtype=float), np.asarray(y, dtype=float)
    # Fit every preprocessing parameter on this training partition only.
    median = np.array([np.nanmedian(col) if np.isfinite(col).any() else 0.0 for col in X.T])
    filled = np.where(np.isfinite(X), X, median)
    mean, scale = filled.mean(axis=0), filled.std(axis=0)
    scale = np.where(scale > 1e-12, scale, 1.0)
    z = (filled - mean) / scale
    intercept = float(y.mean())
    beta = np.linalg.solve(z.T @ z + alpha * np.eye(z.shape[1]), z.T @ (y - intercept))
    return {"median": median, "mean": mean, "scale": scale, "intercept": intercept, "beta": beta}


def ridge_predict(fit: dict, X):
    X = np.asarray(X, dtype=float)
    filled = np.where(np.isfinite(X), X, fit["median"])
    return fit["intercept"] + (filled - fit["mean"]) / fit["scale"] @ fit["beta"]


def tune_alpha(X, y, groups, grid, folds: int, seed: int) -> float:
    partitions = list(grouped_folds(groups, folds, seed))
    losses = []
    for alpha in grid:
        squared = []
        for train, test in partitions:
            pred = ridge_predict(ridge_fit(X[train], y[train], alpha), X[test])
            squared.extend((pred - y[test]) ** 2)
        losses.append(float(np.mean(squared)))
    return float(grid[int(np.argmin(losses))])


def nested_predictions(X, y, groups, spec: dict) -> dict:
    X, y, groups = np.asarray(X, float), np.asarray(y, float), np.asarray(groups)
    if len(y) < spec["minimum_games"] or len(set(groups)) < spec["minimum_groups"]:
        return {"status": "insufficient_support", "n": len(y), "groups": len(set(groups))}
    pred, baseline = np.full(len(y), np.nan), np.full(len(y), np.nan)
    fold_ids = np.full(len(y), -1)
    details = []
    for fold_id, (train, test) in enumerate(grouped_folds(groups, spec["outer_folds"], spec["seed"])):
        if len(set(groups[train])) < 2:
            return {"status": "insufficient_inner_groups", "n": len(y)}
        alpha = tune_alpha(X[train], y[train], groups[train], spec["ridge_alpha_grid"], spec["inner_folds"], spec["seed"] + fold_id + 1)
        fit = ridge_fit(X[train], y[train], alpha)
        pred[test] = ridge_predict(fit, X[test])
        baseline[test] = y[train].mean()
        fold_ids[test] = fold_id
        details.append({"fold": fold_id, "alpha": alpha, "train_n": len(train), "test_n": len(test),
                        "held_groups": sorted(set(groups[test])), "standardized_beta": fit["beta"].tolist()})
    if not np.isfinite(pred).all():
        raise ValueError("Missing out-of-fold predictions")
    return {
        "status": "ok", "n": len(y), "groups": len(set(groups)),
        "rmse": float(np.sqrt(np.mean((pred - y) ** 2))), "mae": float(np.mean(abs(pred - y))),
        "baseline_rmse": float(np.sqrt(np.mean((baseline - y) ** 2))),
        "baseline_mae": float(np.mean(abs(baseline - y))),
        "prediction": pred.tolist(), "baseline_prediction": baseline.tolist(), "fold_ids": fold_ids.tolist(), "folds": details,
    }


def bootstrap_difference(rows: list[dict], key: str, seed: int, repetitions: int = 2000) -> dict:
    """Exploratory episode bootstrap for two observed landmark groups."""
    groups = [[r for r in rows if bool(r[key]) == flag] for flag in (False, True)]
    if any(len(g) < 2 for g in groups):
        return {"status": "insufficient_support"}
    rng = np.random.default_rng(seed)
    diffs = []
    for _ in range(repetitions):
        samples = [rng.choice([r["Q"] for r in g], len(g), replace=True).mean() for g in groups]
        diffs.append(samples[1] - samples[0])
    return {"status": "descriptive_only", "difference_mean_Q": float(np.mean([r["Q"] for r in groups[1]]) - np.mean([r["Q"] for r in groups[0]])),
            "episode_bootstrap_interval_95": np.quantile(diffs, [0.025, 0.975]).tolist(),
            "groups": [{"promoted": flag, "n": len(g), "mean_Q": float(np.mean([r["Q"] for r in g])),
                        "completed": sum(r["completed"] for r in g)} for flag, g in zip((False, True), groups)],
            "warning": "Conditional historical association; bootstrap does not remove policy confounding, adaptive allocation or selection."}
