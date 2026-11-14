#!/usr/bin/env python3
"""Combine the per-cap J workers of code/oai186_check2.py (code/cap6/oai186_check2_J_b<b>.json) and its I_H value
into J_0, J_+, J_t, J_{lambda,H} and rho* J / I_H, in ball arithmetic, and compare with the first program
(code/oai186_IH.json, code/oai186_J.json) and with [14, Lemma 2.5].  Session 14.
usage: oai186_check2_combine.py IH_ball_string [--out f.json]
  (IH_ball_string: the "I_H = [...]" ball printed by `oai186_check2.py --only I`, e.g. "[2.36853178533... +/- 1e-28]")"""
import sys, json, re
from flint import arb, fmpq, ctx
ctx.prec = 320
NG = 98304; n = NG - 40
h = fmpq(2742997, 2624989) / NG
A = lambda q: arb(q.p) / arb(q.q)
def gq(t):
    return fmpq(21, 200) / (1 + t / 100) + fmpq(179, 200) / (1 + fmpq(907, 5) * t)
Z = arb(0)
for j in range(n):
    g = A(gq((j + fmpq(1, 2)) * h)); Z += g * g
BV = [35265, 35419, 44781, 44976, 46580, 49152, 68225]
tot = {"0": arb(0), "+": arb(0), "t": arb(0)}
for b in BV:
    d = json.load(open("code/cap6/oai186_check2_J_b%d.json" % b))
    for F in tot:
        mid, rad = d[F]
        tot[F] += arb(mid, rad)
fac = 40 * A(h) / Z
J0, Jp, Jt = tot["0"] * fac, tot["+"] * fac, tot["t"] * fac
ah, bh = A(fmpq(2479900401, 2500000000)), A(fmpq(-843183, 10 ** 9))
Jl = J0 + (ah + bh) * Jp + bh * Jt
m = re.match(r"\[([0-9.e+-]+) \+/- ([0-9.e+-]+)\]", sys.argv[1].strip())
IH = arb(m.group(1), m.group(2))
ratio = A(fmpq(2624989, 10 ** 7)) * Jl / IH
p1I = json.load(open("code/oai186_IH.json")); p1J = json.load(open("code/oai186_J.json"))
out = dict(I_H=IH.str(15, radius=True), J0=J0.str(15, radius=True), Jplus=Jp.str(12, radius=True), Jt=Jt.str(12, radius=True),
           J_lambda=Jl.str(15, radius=True), ratio=ratio.str(12, radius=True),
           I_H_inside_ref=bool(IH > arb(23685317816) / 10 ** 24 and IH < arb(23685317890) / 10 ** 24),
           J_ge_ref=bool(Jl > arb(90248755123) / 10 ** 24), ratio_gt=bool(ratio > arb(500103) / 500000),
           rel_diff_I_vs_program1=float(abs(IH.mid() / arb(p1I["I_H_lo"]) - 1)),
           rel_diff_J_vs_program1=float(abs(Jl.mid() / arb(p1J["J_lambda"]) - 1)))
print(json.dumps(out, indent=1))
if "--out" in sys.argv:
    json.dump(out, open(sys.argv[sys.argv.index("--out") + 1], "w"), indent=1)
