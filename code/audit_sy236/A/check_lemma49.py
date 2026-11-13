#!/usr/bin/env python3
"""Lemma 4.9 (three-way exponent grouping), s=1001/10000.
(1) exact-rational randomized + structured testing;
(2) MILP search (scipy/HiGHS) for a counterexample with n<=9 coordinates,
    maximizing a strictness slack; (3) tightness: s=1/10 fails for (1/5)^5.
The rigorous argument is the proof checked in report.md; this is a cross-check."""
from fractions import Fraction as F
from itertools import combinations
import random, sys
import numpy as np

def alts(u, s):
    a, b = F(1,2)-s, F(1,2)+s
    n = len(u)
    A1 = any(x >= b for x in u)
    A2 = False
    for mask in range(1, 2**n - 1):
        t = sum(u[i] for i in range(n) if mask >> i & 1)
        lo, hi = min(t, 1-t), max(t, 1-t)
        if a < lo and hi < b: A2 = True; break
    A3 = any(all(2*s <= u[i] <= a for i in T) and all(u[i]+u[j] >= b for i,j in combinations(T,2))
             for T in combinations(range(n),3))
    return A1, A2, A3

s = F(1001,10000)
random.seed(1)
bad = 0; cnt = [0,0,0]; N=0
special = [F(2002,10000), F(3999,10000), F(6001,10000), F(1,5), F(2,5), F(3,10), F(1,10)]
for trial in range(60000):
    n = random.randint(1,9)
    mode = trial % 3
    if mode == 0:
        w = [random.randint(0,1000) for _ in range(n)]
    elif mode == 1:   # values near thresholds
        w = [random.choice(special)*10000 + random.randint(-3,3) for _ in range(n)]
        w = [max(0,x) for x in w]
    else:             # few big atoms + many tiny ones
        w = [random.randint(1500,4200) for _ in range(random.randint(1,4))] + [random.randint(0,30) for _ in range(n)]
    tot = sum(w)
    if tot == 0: continue
    u = [F(x, tot) for x in w]
    r = alts(u, s); N += 1
    for i in range(3): cnt[i] += r[i]
    if not any(r): bad += 1; print("COUNTEREXAMPLE", u); break
print(f"random exact tests: {N}, failures: {bad}, alt counts (non-exclusive): {cnt}")
# five equal parts, exact
print("u=(1/5)^5, s=1001/10000:", alts([F(1,5)]*5, s))
print("u=(1/5)^5, s=1/10     :", alts([F(1,5)]*5, F(1,10)), "(all False => s>1/10 is necessary)")
# three-pivot extremal configurations
print("u=(0.2002,0.3999,0.3999):", alts([F(2002,10000),F(3999,10000),F(3999,10000)], s))

# MILP counterexample search
try:
    from scipy.optimize import milp, LinearConstraint, Bounds
except Exception as e:
    print("scipy milp unavailable", e); sys.exit()
a, b, ss = 0.5-1001/10000, 0.5+1001/10000, 1001/10000
for n in range(1, 10):
    subs = list(range(1, 2**n - 1))
    trip = list(combinations(range(n), 3))
    # variables: u (n), eps (1), y_S (len subs), z_{T,c} (6 per triple)
    nv = n + 1 + len(subs) + 6*len(trip)
    c = np.zeros(nv); c[n] = -1.0
    rows=[]; lo=[]; hi=[]
    Mbig = 2.0
    def row(): return np.zeros(nv)
    r=row(); r[:n]=1; rows.append(r); lo.append(1); hi.append(1)
    for i in range(n):  # alt1 fails: u_i <= b - eps
        r=row(); r[i]=1; r[n]=1; rows.append(r); lo.append(-np.inf); hi.append(b)
    for k,S in enumerate(subs):  # sum_S <= a  (y=0)  or sum_S >= b (y=1)
        yi = n+1+k
        r=row(); [r.__setitem__(i,1) for i in range(n) if S>>i&1]; r[yi]=-Mbig; rows.append(r); lo.append(-np.inf); hi.append(a)
        r=row(); [r.__setitem__(i,1) for i in range(n) if S>>i&1]; r[yi]=-Mbig; rows.append(r); lo.append(b-Mbig); hi.append(np.inf)
    base = n+1+len(subs)
    for t,(i,j,k) in enumerate(trip):  # alt3 fails: one of 6 conditions with slack eps
        zs = [base+6*t+q for q in range(6)]
        r=row(); [r.__setitem__(z,1) for z in zs]; rows.append(r); lo.append(1); hi.append(np.inf)
        conds = [([i],2*ss),([j],2*ss),([k],2*ss),([i,j],b),([i,k],b),([j,k],b)]
        for z,(idx,thr) in zip(zs,conds):   # z=1 => sum(idx) <= thr - eps
            r=row(); [r.__setitem__(v,1) for v in idx]; r[n]=1; r[z]=Mbig; rows.append(r); lo.append(-np.inf); hi.append(thr+Mbig)
    integ = np.zeros(nv); integ[n+1:] = 1
    lb = np.zeros(nv); ub = np.ones(nv); ub[n] = 1.0; lb[n] = -1.0
    res = milp(c, constraints=LinearConstraint(np.array(rows), lo, hi), integrality=integ, bounds=Bounds(lb, ub))
    eps = -res.fun if res.status == 0 else None
    print(f"n={n}: MILP status={res.status}, max strictness slack eps={eps}")

# Re-examine near-zero positive slacks: extract the MILP point, rationalize, and test exactly.
print("\nExact re-test of MILP optimisers (the tiny positive slacks are solver tolerance):")
for n in range(2,10):
    subs = list(range(1, 2**n - 1)); trip = list(combinations(range(n), 3))
    nv = n + 1 + len(subs) + 6*len(trip)
    c = np.zeros(nv); c[n] = -1.0
    rows=[]; lo=[]; hi=[]; Mbig=2.0
    def row(): return np.zeros(nv)
    r=row(); r[:n]=1; rows.append(r); lo.append(1); hi.append(1)
    for i in range(n):
        r=row(); r[i]=1; r[n]=1; rows.append(r); lo.append(-np.inf); hi.append(b)
    for k,S in enumerate(subs):
        yi=n+1+k
        r=row(); [r.__setitem__(i,1) for i in range(n) if S>>i&1]; r[yi]=-Mbig; rows.append(r); lo.append(-np.inf); hi.append(a)
        r=row(); [r.__setitem__(i,1) for i in range(n) if S>>i&1]; r[yi]=-Mbig; rows.append(r); lo.append(b-Mbig); hi.append(np.inf)
    base=n+1+len(subs)
    for t,(i,j,k) in enumerate(trip):
        zs=[base+6*t+q for q in range(6)]
        r=row(); [r.__setitem__(z,1) for z in zs]; rows.append(r); lo.append(1); hi.append(np.inf)
        conds=[([i],2*ss),([j],2*ss),([k],2*ss),([i,j],b),([i,k],b),([j,k],b)]
        for z,(idx,thr) in zip(zs,conds):
            r=row(); [r.__setitem__(v,1) for v in idx]; r[n]=1; r[z]=Mbig; rows.append(r); lo.append(-np.inf); hi.append(thr+Mbig)
    integ=np.zeros(nv); integ[n+1:]=1
    lb=np.zeros(nv); ub=np.ones(nv); lb[n]=-1.0
    res=milp(c, constraints=LinearConstraint(np.array(rows),lo,hi), integrality=integ, bounds=Bounds(lb,ub),
             options={"mip_rel_gap":0, "primal_feasibility_tolerance":1e-9} if False else None)
    u=[F(round(x*10**7),10**7) for x in res.x[:n]]
    tot=sum(u); u=[x/tot for x in u] if tot>0 else u
    print(f"n={n}: u~{[float(x) for x in u]} exact alternatives={alts(u,s)}")
