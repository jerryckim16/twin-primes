import sys, json
sys.path.insert(0, "code")
from mk_bound import run
res = []
for D in (11, 15, 19):
    lo, hi = 51, 105          # invariant: fails at lo-ish, succeeds at hi
    info, *_ = run(hi, D)
    assert info["gt4"]
    while hi - lo > 1:
        mid = (lo + hi)//2
        info, *_ = run(mid, D)
        print(json.dumps(info), flush=True)
        if info["gt4"]: hi = mid
        else: lo = mid
    info, *_ = run(hi, D); res.append(info)
    print("SMALLEST for D=%d: k=%d  M_k >= %s" % (D, hi, info["certified"]), flush=True)
json.dump(res, open("code/scan_results.json", "w"))
