#!/usr/bin/env python3
"""Rigorous a priori bound for the j = 3 ("thin") inclusion-exclusion pieces of capped_exact.py (Session 13).

Each piece of capped_exact.py (kind, n, m, j) is (-1)^j C(n,m) C(n-m,j) times an integral of an integrand
over a region of R^n_{>=0}.  In the shifted coordinates (z = u - g on the m + j forced coordinates) the region
is described by r_A = |z_A| (m coordinates) and rho = |z_B| + |y| (the other n - m coordinates):
  Icorr, Corr1, Corr2b (T1):  lo <= r_A <= hi,  rho <= Lam - r_A
      vol <= int_lo^hi r^(m-1)/(m-1)! (Lam - r)^(n-m)/(n-m)! dr          (m >= 1)
  Corr2c (T2):               0 <= r_A <= a,  0 <= rho <= rc
      vol <= a^m/m! * rc^(n-m)/(n-m)!                                       (m = 0: first factor 1)
(the code's regions may carry further constraints -- per-coordinate caps -- which only shrink them).
Integrands: Icorr P^2 <= M^2;  Corr1 Q(R)^2 <= (L M)^2;  Corr2 |Q(R)^2 - Q(U)^2| <= max(Q(R)^2, Q(U)^2) <= (L M)^2,
where on {u >= 0, |u| <= L}: 0 <= R = L - |u| <= L, 0 <= P_j(u) = sum u_i^j <= |u|^j <= L^j, hence
  |P(u)| <= M := sum_i |c_i| L^(a_i + w(b_i)),   |Q(u', x)| <= x M <= L M  (0 <= x <= R <= L).
So |piece| <= C(n,m) C(n-m,j) * vol * sup|integrand|.  All arithmetic exact (fractions); output also as floats.
usage: thin_bound.py P_u.json [--j 3] [--jonly] [--ref capped_exact_result.json] [--pieces pieces.jsonl] [--volcheck] [--out f.json]
  --pieces: compare with the exact values of finished pieces (each |exact| must be <= its bound)
  --volcheck: recompute each region volume with capped_exact.T1 / T2 (integrand 1) and check vol_code <= vol_formula
"""
import sys, json
from fractions import Fraction as Fr
from math import comb, factorial
sys.path.insert(0, "code")

def F(s):
    return Fr(s)

def wt(b):
    return sum((j + 2) * x for j, x in enumerate(b))

def rint(lo, hi, Lam, al, N):
    """int_lo^hi r^al (Lam - r)^N dr, exact."""
    def G(x):
        h = Lam - x
        return sum(comb(al, i) * Lam ** (al - i) * (-1) ** i * h ** (N + i + 1) / (N + i + 1) for i in range(al + 1))
    return G(lo) - G(hi)

def main():
    data = json.load(open(sys.argv[1]))
    jj = int(sys.argv[sys.argv.index("--j") + 1]) if "--j" in sys.argv else 3
    # reuse capped_exact's piece list (same parameters, same regions)
    import capped_exact as ce
    c = ce.Capped(data)
    k, L = c.k, F(str(c.L))
    M = sum(abs(F(x)) * L ** (a + wt(b)) for (a, b), x in zip(data["basis"], data["coeffs"]))
    c.jonly = "--jonly" in sys.argv
    ts = c.tasks()
    q = lambda z: F(str(z))
    out, tot = [], {}
    for kind, n, m, j, args in ts:
        if j != jj:
            continue
        if kind == "Corr2c":
            a, rc, cp = map(q, args)
            vol = (a ** m / factorial(m) if m > 0 else Fr(1)) * rc ** (n - m) / factorial(n - m)
        else:
            lo, hi, Lam = map(q, args)
            vol = rint(lo, hi, Lam, m - 1, n - m) / (factorial(m - 1) * factorial(n - m))
        sup = M ** 2 if kind == "Icorr" else (L * M) ** 2
        bnd = comb(n, m) * comb(n - m, j) * vol * sup
        out.append(dict(kind=kind, m=m, j=j, vol=vol, bound=bnd))
        tot[kind] = tot.get(kind, Fr(0)) + bnd
    # cap-free I, J (exact) for the relative size: from a capped_exact result file (--ref) or recomputed
    if "--ref" in sys.argv:
        r = json.load(open(sys.argv[sys.argv.index("--ref") + 1]))
        I, J = F(r["I"]), F(r["J"])
    else:
        c.prepare()
        I, J = map(q, c.capfree())
    rep = {kd: float(v / (I if kd == "Icorr" else J)) for kd, v in tot.items()}
    print("M = %.6e ; pieces with j = %d: %d" % (float(M), jj, len(out)))
    print("bound / (cap-free I or J) per kind:", {kd: "%.3e" % v for kd, v in rep.items()})
    BI = tot.get("Icorr", Fr(0))
    BJ = sum(v for kd, v in tot.items() if kd != "Icorr")
    print("total: B_I/I = %.3e, B_J/J = %.3e" % (float(BI / I), float(BJ / J)))
    if "--pieces" in sys.argv:
        ex = {}
        for line in open(sys.argv[sys.argv.index("--pieces") + 1]):
            if line.strip():
                r = json.loads(line)
                ex[(r["kind"], r["m"], r["j"])] = Fr(r["v"])
        worst, ok, cnt = 0.0, True, 0
        for o in out:
            key = (o["kind"], o["m"], o["j"])
            if key in ex:
                cnt += 1
                if abs(ex[key]) > o["bound"]:
                    ok = False
                    print("VIOLATION", key, float(ex[key]), float(o["bound"]))
                if ex[key] != 0:
                    worst = max(worst, float(abs(ex[key]) / o["bound"]))
        print("checked %d exact pieces against their bounds: all within = %s; max |exact|/bound = %.3e" % (cnt, ok, worst))
    if "--volcheck" in sys.argv:
        from flint import fmpq_poly
        zero = tuple(0 for _ in range(c.blen + 0))
        bad = 0
        for t, o in zip([t for t in ts if t[3] == jj], out):
            kind, n, m, j, args = t
            if kind == "Corr2c":
                one = {zero: ce.BiPoly({(0, 0): ce.fmpq(1)})}
                v = c.T2(n, m, j, *args, one)
            else:
                v = c.T1(n, m, j, *args, {zero: fmpq_poly([1])})
            v = q(v)
            if not (0 <= v <= o["vol"]):
                bad += 1
                print("VOLCHECK FAIL", kind, m, j, float(v), float(o["vol"]))
        print("volcheck: %d pieces, failures %d" % (len(out), bad))
    if "--out" in sys.argv:
        json.dump(dict(source=sys.argv[1], j=jj, M=str(M), BI=str(BI), BJ=str(BJ), BI_over_I=float(BI / I),
                       BJ_over_J=float(BJ / J), pieces=[dict(kind=o["kind"], m=o["m"], j=o["j"], bound=str(o["bound"]),
                       bound_float=float(o["bound"])) for o in out]), open(sys.argv[sys.argv.index("--out") + 1], "w"), indent=1)

if __name__ == "__main__":
    main()
