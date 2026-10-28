"""Print one line whenever an official DeepSeek game of the given policies changes level, blows up, ends."""
import glob, os, re, sys, time
pols = sys.argv[1].split(",")  # policy id prefixes (8 hex)
seen = {}
while True:
    for pol in pols:
        for d in sorted(glob.glob(os.path.expanduser(f"~/careerlab-data/huawei-deepseek/runs/deepseek-pilo-{pol}*"))):
            try:
                t = open(f"{d}/play.log", errors="ignore").read()
            except OSError:
                continue
            lv = (re.findall(r"^ (L\d+) ", t, re.M) or ["?"])[-1]
            m = (re.findall(r"Month (\d+) ·", t) or ["0"])[-1]
            key = (lv, t.count("landmines"), t.count("Eliminated"), os.path.exists(f"{d}/result.json"))
            if seen.get(d) != key:
                seen[d] = key
                print(f"{d.split('pilo-')[1][:8]}-{d[-8:-3]} month {m} {lv} blowups={key[1]} eliminated={key[2]} "
                      f"{'DONE' if key[3] else 'playing'}", flush=True)
    time.sleep(30)
