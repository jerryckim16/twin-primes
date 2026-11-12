import sys, json
sys.path.insert(0, "code")
from admissible import search, is_admissible
out = {}
for k, start in ((102, 576), (105, 600)):
    d = start; H = None
    while H is None:
        for seed in range(6):
            H = search(k, d, node_limit=400000, seed=seed)
            if H: break
        if H is None: d += 2
    out[k] = H
    print(k, "found diameter", H[-1], "target", start, is_admissible(H), flush=True)
json.dump({str(k): v for k, v in out.items()}, open("code/tuples_big.json", "w"))
