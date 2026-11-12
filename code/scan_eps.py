#!/usr/bin/env python3
"""Certified lower bounds for M_{k,eps} on a grid of (k, D, eps), for the degree-extrapolation
experiment of Session 4 (paper, Remark on the threshold of the eps-enlarged simplex).

Every value printed is an exact Rayleigh quotient of a rational vector (so a rigorous lower bound
for M_{k,eps}); the extrapolation in D done afterwards by extrapolate_eps.py is NOT rigorous.

usage: scan_eps.py k D1,D2,... e1,e2,... out.jsonl
"""
import sys, json, time
sys.path.insert(0, "code")
import mk_general as mg
from flint import fmpq

mg.EVEN_ONLY = True
k = int(sys.argv[1])
Ds = [int(x) for x in sys.argv[2].split(",")]
eps_list = [fmpq(*map(int, e.split("/"))) if "/" in e else fmpq(int(e)) for e in sys.argv[3].split(",")]
out = open(sys.argv[4], "a")
for D in Ds:
    for e in eps_list:
        info, exact, basis, q = mg.run(k, D, eps=e, prec=300)
        info["eps"] = str(e)
        out.write(json.dumps(info) + "\n"); out.flush()
