"""Smallest k with a certified M_k > 4 for the symmetric basis of degree D.  usage: scan_general.py D lo hi [--even]"""
import sys, json
sys.path.insert(0, "code")
import mk_general
mk_general.EVEN_ONLY = "--even" in sys.argv
from mk_general import run
D, lo, hi = map(int, sys.argv[1:4])
tag = " even" if mk_general.EVEN_ONLY else ""   # assume fails at lo, succeeds at hi
info, *_ = run(hi, D); print(json.dumps(info), flush=True); assert info["gt4"]
while hi - lo > 1:
    mid = (lo + hi) // 2
    info, *_ = run(mid, D); print(json.dumps(info), flush=True)
    if info["gt4"]: hi = mid
    else: lo = mid
print("SMALLEST D=%d%s k=%d" % (D, tag, hi), flush=True)
