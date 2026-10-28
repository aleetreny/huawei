"""El mismo juez que judge.py, pero con deepseek-v4-flash (la clave del reto, en el Mac de Alejandro).

Si la organizacion puntua la calidad con el modelo designado, este es el sustituto mas fiel. Usa el
cliente de scripts/deepseek/ds.py (lee la clave del .env del programa oficial, nunca la imprime, no fija
proveedor) con un tope propio: solo suma las llamadas con etiqueta 'calidad-judge' en calls.jsonl.

    uv run python scripts/calidad-skills/ds_judge.py --out lab/reports/calidad-skills/data/j03-deepseek.jsonl \
        --reps 5 --budget 0.40 lab/policies-src/deepseek/t13-read-v4 lab/policies-src/calidad/v4-c2
Coste previsto: ~16 mil fichas de entrada por llamada; 5 lecturas x 4 manuales ~ 0,1-0,2 USD.
"""
from __future__ import annotations

import argparse, asyncio, hashlib, json, os, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parents[1] / "scripts" / "deepseek"))
from judge import PROMPT, ROOT, parse, public_rules, rubric, skill_files  # noqa: E402
import ds  # noqa: E402

TAG = "calidad-judge"


def my_spend() -> float:
    if not ds.CALLS.exists():
        return 0.0
    tot = 0.0
    for line in ds.CALLS.read_text().splitlines():
        try:
            r = json.loads(line)
        except ValueError:
            continue
        if str(r.get("tag", "")).startswith(TAG):
            tot += float(r.get("cost") or 0.0)
    return tot


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("targets", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--reps", type=int, default=5)
    ap.add_argument("--budget", type=float, default=0.40, help="USD maximos de este juez (acumulado)")
    a = ap.parse_args()
    client = ds.DeepSeek(concurrency=4, stop_usd=1e9)  # el tope de la linea no aplica: usamos el nuestro
    rub, rules = rubric(), public_rules()
    out = open(a.out, "a")
    try:
        for t in a.targets:
            for f in skill_files(t):
                text = f.read_text(); rel = os.path.relpath(f, ROOT)
                async def one(r: int):
                    if my_spend() >= a.budget:
                        raise SystemExit(f"tope del juez alcanzado: {my_spend():.3f} USD")
                    t0 = time.time()
                    msg = await client.chat([{"role": "user", "content": PROMPT.format(rubric=rub, rules=rules, path=rel, skill=text)}],
                                            tag=f"{TAG}:{rel}:{r}", temperature=0.0 if r == 0 else ds.TEMPERATURE)
                    res = parse(msg.get("content") or "")
                    return {"target": t, "file": rel, "sha": hashlib.sha1(text.encode()).hexdigest()[:10], "words": len(text.split()),
                            "model": "deepseek-v4-flash", "rep": r, "label": "j03", "sec": round(time.time() - t0, 1),
                            "cost": msg["_usage"].get("cost"), "ok": res is not None, **(res or {"raw": (msg.get("content") or "")[-500:]})}
                for row in await asyncio.gather(*(one(r) for r in range(a.reps))):
                    out.write(json.dumps(row, ensure_ascii=False) + "\n"); out.flush()
                    print(rel, row.get("score"), row.get("cost"), file=sys.stderr)
    finally:
        await client.close()
        print(f"gasto acumulado del juez: {my_spend():.4f} USD", file=sys.stderr)


if __name__ == "__main__":
    asyncio.run(main())
