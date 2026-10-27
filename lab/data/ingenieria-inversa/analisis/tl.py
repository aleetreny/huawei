"""Timeline: align each decision step with its log entry and the logs that follow it."""
import sys, json, re, gzip, glob, collections
sys.path.insert(0, "/home/user/huawei/scripts/ingenieria-inversa")
import os
os.environ.setdefault("BB_DATA", "/home/user/bbdata")
from bbdata import Batch, parse_choice_entry, deltas, IDX, STATS

def timeline(b, g):
    """Return list of (step, choice_entry, [following (code,text)]) or None if misaligned."""
    logs = b.log_entries(g)
    # indices of choice entries
    ci = [i for i,(c,m) in enumerate(logs) if c in ("A","F") and "Chose #" in m]
    init = [i for i,(c,m) in enumerate(logs) if c=="F" and "Initialization" in m]
    steps = g["steps"]
    dsteps = [s for s in steps if s[1] in ("e","q","m")]
    if len(dsteps) != len(ci): return None
    out=[]
    for k,(s,i) in enumerate(zip(dsteps, ci)):
        j = ci[k+1] if k+1 < len(ci) else len(logs)
        out.append((s, parse_choice_entry(logs[i][1]), logs[i+1:j]))
    pre = logs[:ci[0]] if ci else logs
    return pre, out
