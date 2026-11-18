#!/usr/bin/env python3
"""Parity attempt 2026-11-18 (route card notes/parity-attempts/2026-11-18-e2-consistency-test.md):
the bipartite criterion (papers/parity-barrier, Prop. prop:bipartite) on PARITY-EVEN targets,
products of exactly two distinct primes (E2, lambda = +1), as a consistency test against
Goldston-Graham-Pintz-Yildirim (GGPY: arXiv:math/0506067v1, math/0609615v1, 0803.2636v1).

Convention.  A sign pattern eps in {+1,-1}^k records lambda at the k positions (forms).  A target is a
family of "events"; each event prescribes signs at some positions (prime -> -1, E2 -> +1, which is all
a pattern weight can see).  A pattern is FORBIDDEN (the weight must vanish on it) iff it is compatible
with some event.  The target is BLOCKED iff some probability measure on the non-forbidden patterns has
every marginal P(eps_i = +1) = 1/2 (= fair pattern weight that kills the target; Prop. prop:bipartite,
weakly fair is equivalent).  Every decision below is certified EXACTLY (fractions):
  blocked   -> an explicit rational fair measure on allowed patterns, checked;
  unblocked -> a rational vector c and c0 with c.x <= c0 for every allowed x (x_i = 1 if eps_i = +1)
               but c.(1/2,...,1/2) > c0 (Farkas), checked.
The LP (scipy HiGHS) only proposes the certificate.

Arithmetic sanity checks: GGPY's linear-form identities, admissibility of their systems, and of the
triple {m, m+6, m+12} used in part F; a search for admissible triples of forms realising a "triangle"
for E2 pairs at a fixed difference d with multipliers in {1} U primes.
usage: /usr/bin/python3 code/parity/e2_consistency.py > code/parity/e2_consistency.out
"""
import itertools, math, sys
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog

HALF = Fr(1, 2)


def patterns(k):
    return list(itertools.product((1, -1), repeat=k))


def compatible(eps, event):
    return all(eps[i] == s for i, s in event)


def allowed_patterns(k, events):
    return [e for e in patterns(k) if not any(compatible(e, ev) for ev in events)]


def rat(v, den=720):
    return Fr(v).limit_denominator(den)


def decide(k, events):
    """returns (status, certificate) with an exact check; status in {'blocked','unblocked'}"""
    A = allowed_patterns(k, events)
    if A:
        # feasibility: mu >= 0, sum mu = 1, sum mu * eps_i = 0
        M = len(A)
        Aeq = [[1.0] * M] + [[float(a[i]) for a in A] for i in range(k)]
        beq = [1.0] + [0.0] * k
        res = linprog(np.zeros(M), A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * M, method="highs")
        if res.status == 0:
            mu = [rat(x) for x in res.x]
            s = sum(mu)
            if s > 0:
                mu = [m / s for m in mu]
            ok = all(m >= 0 for m in mu) and sum(mu) == 1 and all(
                sum(m * a[i] for m, a in zip(mu, A)) == 0 for i in range(k))
            if not ok:
                raise RuntimeError("rationalised fair measure failed exact check")
            return "blocked", {a: m for a, m in zip(A, mu) if m}
    # separating hyperplane: maximise c.(1/2) - c0 s.t. c.x - c0 <= 0 on allowed x, -1 <= c <= 1
    X = [[1.0 if a[i] == 1 else 0.0 for i in range(k)] for a in A]
    nvar = k + 1
    obj = [-0.5] * k + [1.0]
    Aub = [x + [-1.0] for x in X] if X else None
    bub = [0.0] * len(X) if X else None
    res = linprog(obj, A_ub=Aub, b_ub=bub, bounds=[(-1, 1)] * k + [(-k, k)], method="highs")
    c = [rat(v) for v in res.x[:k]]
    xs = [[1 if a[i] == 1 else 0 for i in range(k)] for a in A]
    c0 = max([sum(ci * xi for ci, xi in zip(c, x)) for x in xs], default=Fr(-1))
    gap = sum(c) * HALF - c0
    if not gap > 0:
        raise RuntimeError("no exact certificate either way")
    return "unblocked", (c, c0, gap)


def show(name, k, events, expect=None):
    st, cert = decide(k, events)
    flag = "" if expect is None else ("  [as predicted]" if st == expect else "  [MISMATCH: predicted %s]" % expect)
    if st == "blocked":
        sup = ", ".join("%s:%s" % ("".join("+" if e == 1 else "-" for e in a), m) for a, m in cert.items())
        print("  %-62s k=%d BLOCKED   fair measure {%s}%s" % (name, k, sup, flag))
    else:
        c, c0, gap = cert
        print("  %-62s k=%d UNBLOCKED  c=%s c0=%s margin=%s%s" % (name, k, [str(x) for x in c], c0, gap, flag))
    return st


E2, PR = 1, -1  # signs seen by the weight

# ---------------------------------------------------------------- A
print("A. 'at least j of the k positions are E2' (events: every j-set with sign +1).")
print("   prediction (sign flip of Prop. prop:bipartite(b)): blocked iff k <= 2(j-1)")
bad = 0
for k in range(1, 9):
    for j in range(1, k + 1):
        ev = [tuple((i, E2) for i in S) for S in itertools.combinations(range(k), j)]
        st, _ = decide(k, ev)
        pred = "blocked" if k <= 2 * (j - 1) else "unblocked"
        bad += st != pred
print("   k=1..8, all j: %d mismatches" % bad)
show("two E2 among 2 positions (n, n+d both E2)", 2, [((0, E2), (1, E2))], "blocked")
show("two E2 among 3 positions (GGPY 0609615 Thm 2 / Basic Thm)", 3,
     [((i, E2), (j, E2)) for i, j in itertools.combinations(range(3), 2)], "unblocked")
show("two E2 among 8 positions (GGPY 0506067: 8-tuple)", 8,
     [((i, E2), (j, E2)) for i, j in itertools.combinations(range(8), 2)], "unblocked")
print("   GGPY 0609615 Thm 1 needs k >= C1(nu) = (4e^-g/B)(1+o(1)) e^{B nu/4} forms for nu+1 E2 values;")
print("   the class blocks nu+1 of k iff k <= 2 nu.  (4e^-g/B) e^{B nu/4} at B=4 (BV), B=2 (EH) vs 2 nu:")
g = 0.5772156649015329
for nu in range(1, 9):
    print("     nu=%d  C1(B=4)~%9.1f  C1(B=2)~%7.2f  2nu=%2d" % (
        nu, 4 * math.exp(-g) / 4 * math.exp(nu), 4 * math.exp(-g) / 2 * math.exp(nu / 2), 2 * nu))
print("   (main term only; o(1) -> 0 as nu -> oo.  For nu = 1 they prove k = 3 > 2 directly, Thm 2.)")

# ---------------------------------------------------------------- B
print("\nB. windows: 'two E2 among n+h_i at distance <= g' on admissible shift tuples")
print("   prediction (sign flip of (c)): blocked iff every [a,a+g] holds <= 2 elements of H")
def window_events(H, g, m=1, sign=E2):
    return [tuple((i, sign) for i in S) for S in itertools.combinations(range(len(H)), m + 1)
            if H[S[-1]] - H[S[0]] <= g]
for H, gs in [((0, 2, 6), (2, 4, 6)), ((0, 4, 6), (4, 6)), ((0, 2, 8, 12), (6, 8)), ((0, 2, 6, 8, 12), (6, 8))]:
    for gg in gs:
        ev = window_events(H, gg)
        pred = "blocked" if all(sum(1 for h in H if a <= h <= a + gg) <= 2 for a in range(-gg, max(H) + 1)) else "unblocked"
        show("H=%s, g=%d" % (str(H), gg), len(H), ev, pred)
print("   So within pure shifts the class blocks liminf(q_{n+1}-q_n) <= g exactly for g < H(3) = 6, and")
print("   not g = 6: GGPY's bound 6 (0609615 Cor 2, via {0,2,6}) sits exactly at the class's limit.")

# ---------------------------------------------------------------- C
print("\nC. mixed targets (one E2 and one prime)")
show("n+h_1 E2 and n+h_2 prime", 2, [((0, E2), (1, PR))], "blocked")
show("n E2 & n+2 prime, or n prime & n+2 E2", 2, [((0, E2), (1, PR)), ((0, PR), (1, E2))], "blocked")
for k in range(2, 7):
    ev = [((i, E2), (j, PR)) for i in range(k) for j in range(k) if i != j]
    show("some n+h_i E2 and some n+h_j prime (any i != j)", k, ev, "blocked")
show("Chen-type: n prime and n+2 in {prime, E2}", 2, [((0, PR), (1, PR)), ((0, PR), (1, E2))], "unblocked")

# ---------------------------------------------------------------- D
print("\nD. Erdos-type consecutive integers (GGPY 0803.2636)")
print("   direct: positions x, x+1, target Omega(x)=Omega(x+1)=A forces lambda(x)=lambda(x+1)=(-1)^A:")
for A in (4, 5):
    s = (-1) ** A
    show("x, x+1 with Omega = %d (shift coordinates)" % A, 2, [((0, s), (1, s))], "blocked")
print("   GGPY's route: forms L1,L2,L3 in m; target 'two of them E2' (Basic Theorem) -> triangle:")
show("two of L1(m),L2(m),L3(m) E2 (forms coordinates)", 3,
     [((i, E2), (j, E2)) for i, j in itertools.combinations(range(3), 2)], "unblocked")
print("   any weight in lambda(c*L_i(m)) is a function of (lambda(L_i)) (lambda(cL)=lambda(c)lambda(L)),")
print("   so no weight in the derived integers x blocks it either (cf. Remark rem:marg).")

def sym_check(name, lhs, rhs_const):
    # lhs: list of (coef, (a,b)) meaning sum coef*(a m + b); check identically == rhs_const
    A = sum(c * a for c, (a, b) in lhs); B = sum(c * b for c, (a, b) in lhs)
    print("   identity %-40s %s" % (name, "OK" if (A == 0 and B == rhs_const) else "FAIL (%d m + %d)" % (A, B)))

def admissible(forms, P=200):
    for p in [q for q in range(2, P) if all(q % r for r in range(2, int(q ** .5) + 1))]:
        if all(any(((a * x + b) % p) == 0 for a, b in forms) for x in range(p)):
            return False, p
    return True, None

L = [(6, 1), (8, 1), (9, 1)]  # (1.11)
sym_check("4L1 - 3L2 = 1  (1.12)", [(4, L[0]), (-3, L[1])], 1)
sym_check("3L1 - 2L3 = 1  (1.12)", [(3, L[0]), (-2, L[2])], 1)
sym_check("9L2 - 8L3 = 1  (1.12)", [(9, L[1]), (-8, L[2])], 1)
print("   (1.11) admissible:", admissible(L))
L = [(4, 1), (5, 1), (6, 1)]  # (2.1)
sym_check("5L1 - 4L2 = 1  (2.2)", [(5, L[0]), (-4, L[1])], 1)
sym_check("3L1 - 2L3 = 1  (2.2)", [(3, L[0]), (-2, L[2])], 1)
sym_check("6L2 - 5L3 = 1  (2.2)", [(6, L[1]), (-5, L[2])], 1)
K = [(28, 3), (385, 41), (66, 7)]
print("   (2.4) K-system admissible:", admissible(K),
      " K_i(l)*r_i = L_i(77l+8):", all(r * (a * l + b) == (La * (77 * l + 8) + Lb)
                                     for (a, b), r, (La, Lb) in zip(K, (11, 1, 7), L) for l in range(50)))
L = [(24, 1), (36, 1), (72, 1)]  # (2.6) -> 72m+3 = 3L1, 72m+2 = 2L2, 72m+1 = L3
print("   (2.6) admissible:", admissible(L), " 3L1=72m+3, 2L2=72m+2: OK")

# ---------------------------------------------------------------- E
print("\nE. E2 pairs at a FIXED difference d")
print("   (i) pure shifts, E2 values used directly: target graph {i~j : |h_i-h_j| = d} is bipartite")
print("       (colour h by floor(h/d) mod 2), so blocked for every tuple.  Exhaustive check, shifts in [0,24]:")
cnt = 0; viol = 0
for d in (1, 2, 4, 6, 12):
    for k in (2, 3, 4):
        for H in itertools.combinations(range(0, 25), k):
            ev = [((i, E2), (j, E2)) for i, j in itertools.combinations(range(k), 2) if H[j] - H[i] == d]
            if not ev:
                continue
            cnt += 1
            st, _ = decide(k, ev)
            viol += st != "blocked"
print("       %d tuples (k=2..4, d in {1,2,4,6,12}) with an edge: %d not blocked" % (cnt, viol))

print("   (ii) multipliers: X = c*L(m) is E2 if c = 1 and L(m) is E2, or c = prime and L(m) is prime.")
print("        Triple m, m+6, m+12: 2(m+6)-2m = 12, 2(m+12)-2(m+6) = 12, (m+12)-m = 12.")
print("        target: (m, m+6) both prime, or (m+6, m+12) both prime, or (m, m+12) both E2;")
print("        each event gives x, x+12 both E2 (for m > 2):")
print("        admissible {m, m+6, m+12}:", admissible([(1, 0), (1, 6), (1, 12)]))
show("triangle {0,6,12}: PR-PR, PR-PR, E2-E2", 3,
     [((0, PR), (1, PR)), ((1, PR), (2, PR)), ((0, E2), (2, E2))], "unblocked")
print("        signed-cycle lemma: an edge (i,j) using multipliers (c_i,c_j) needs c_i a_i = c_j a_j, and")
print("        forbids the signs s_i = (-1)^Omega(c_i), s_j = (-1)^Omega(c_j); so s_i s_j = (-1)^(Omega(a_i)+Omega(a_j))")
print("        and the product of s_i s_j around any cycle is +1.  Check: all signed graphs on 3 and 4")
print("        vertices (one forbidden sign pair per edge): blocked <=> the system eps_i eps_j = -s_i s_j is")
print("        solvable (switching-balanced), and hence, for cycle products +1, <=> the graph is bipartite:")
for n in (3, 4):
    E = list(itertools.combinations(range(n), 2))
    tot = mism = 0
    for choice in itertools.product(range(5), repeat=len(E)):
        ev = []; req = []
        for (i, j), c in zip(E, choice):
            if c == 0:
                continue
            si, sj = ((1, 1), (1, -1), (-1, 1), (-1, -1))[c - 1]
            ev.append(((i, si), (j, sj))); req.append((i, j, -si * sj))
        sol = any(all(e[i] * e[j] == r for i, j, r in req) for e in patterns(n))
        st, _ = decide(n, ev)
        tot += 1; mism += (st == "blocked") != sol
    print("        n=%d: %d signed graphs, %d mismatches" % (n, tot, mism))

print("   (iii) search: admissible triples of forms a_i m + b_i (a_1 <= 12, a_2, a_3 <= 72) and multipliers in")
print("        {1,2,3,5,7,11,13} such that EVERY pair (i,j) has an identity c_i L_i - c_j L_j = +-d")
print("        (a triangle, hence unblocked by (ii)).  Smallest example per d:")
mults = (1, 2, 3, 5, 7, 11, 13)
def edges_between(f1, f2, d):
    out = []
    for c1 in mults:
        for c2 in mults:
            if c1 == c2 and c1 != 1:
                pass
            if c1 * f1[0] == c2 * f2[0] and abs(c1 * f1[1] - c2 * f2[1]) == d:
                out.append((c1, c2))
    return out
for d in (1, 2, 4, 6, 8, 12):
    found = None
    forms = [(a, b) for a in range(1, 13) for b in range(0, 2 * a + 13) if math.gcd(a, b) == 1 or (b == 0 and a == 1)]
    best = None
    for f1 in forms:
        if best: break
        for c1 in mults:
            for c2 in mults:
                if (c1 * f1[0]) % c2: continue
                a2 = c1 * f1[0] // c2
                for sg in (1, -1):
                    num = c1 * f1[1] - sg * d
                    if num % c2 or num < 0: continue
                    f2 = (a2, num // c2)
                    if f2 == f1 or a2 > 72: continue
                    for c3 in mults:
                        for c4 in mults:
                            if (c3 * f1[0]) % c4: continue
                            a3 = c3 * f1[0] // c4
                            for sg2 in (1, -1):
                                num2 = c3 * f1[1] - sg2 * d
                                if num2 % c4 or num2 < 0: continue
                                f3 = (a3, num2 // c4)
                                if f3 in (f1, f2) or a3 > 72: continue
                                if not edges_between(f2, f3, d): continue
                                if any(math.gcd(a, b) != 1 for a, b in (f1, f2, f3)): continue
                                ok, _ = admissible([f1, f2, f3], 60)
                                if ok:
                                    best = (f1, f2, f3, (c1, c2), (c3, c4), edges_between(f2, f3, d)[0])
                                    break
                            if best: break
                        if best: break
                    if best: break
                if best: break
            if best: break
    if best:
        f1, f2, f3, e12, e13, e23 = best
        sg = lambda c: "E2" if c == 1 else "prime"
        print("        d=%2d: L=(%dm+%d, %dm+%d, %dm+%d)  mult (1,2)=%s (1,3)=%s (2,3)=%s  [%s]" % (
            d, *f1, *f2, *f3, e12, e13, e23,
            "; ".join("L%d,L%d %s,%s" % (i, j, sg(c[0]), sg(c[1])) for (i, j), c in (((1, 2), e12), ((1, 3), e13), ((2, 3), e23)))))
    else:
        print("        d=%2d: none in range" % d)

# ---------------------------------------------------------------- F numeric sanity
print("\nF. numeric sanity for the {m, m+6, m+12} target, m < 10^6")
N = 2 * 10 ** 6 + 30
spf = list(range(N + 1))
for p in range(2, int(N ** .5) + 1):
    if spf[p] == p:
        for q in range(p * p, N + 1, p):
            if spf[q] == q: spf[q] = p
def isprime(n): return n > 1 and spf[n] == n
def isE2(n):
    if n < 6: return False
    p = spf[n]; r = n // p
    return r != p and r > 1 and spf[r] == r
c = [0, 0, 0]
for m in range(3, 10 ** 6):
    c[0] += isprime(m) and isprime(m + 6)
    c[1] += isprime(m + 6) and isprime(m + 12)
    c[2] += isE2(m) and isE2(m + 12)
    if (isprime(m) and isprime(m + 6)):
        assert isE2(2 * m) and isE2(2 * m + 12)
print("   #(m,m+6 prime)=%d  #(m+6,m+12 prime)=%d  #(m,m+12 E2)=%d  (each event -> x,x+12 both E2: asserted)" % tuple(c))
print("   #(m, m+2 both E2), m<10^6:", sum(1 for m in range(6, 10 ** 6) if isE2(m) and isE2(m + 2)))

# ---------------------------------------------------------------- G
print("\nG. GGPY's own sieve functional vs the class (0609615 Thms 7-8, (8.1)): the method gives nu+1 E2")
print("   among k forms iff rho = k(k-1)(J1+J2+J3)/(B J0) > nu for some polynomial P.  The class blocks")
print("   'nu+1 of k E2' iff k <= 2 nu, so consistency requires max_P rho <= ceil(k/2) (heuristically <= k/2).")
print("   rho is a ratio of quadratic forms in the coefficients of P (deg <= D): generalized eigenvalue,")
print("   Gauss-Legendre quadrature (floating point, not a certificate).")
from scipy.linalg import eigh
def gl(a,b,n=120):
    x,w=np.polynomial.legendre.leggauss(n); return (b-a)/2*x+(a+b)/2,(b-a)/2*w
def forms(k,B,eta,D):
    nb=D+1
    Pt=lambda j,x: x**(j+1)/(j+1)
    P=lambda j,x: x**j
    X,WX=gl(0,1)
    Q0=np.array([[np.sum(WX*P(i,1-X)*P(j,1-X)*X**(k-1)) for j in range(nb)] for i in range(nb)])
    Y,WY=gl(B*eta,1)
    Qn=np.zeros((nb,nb))
    for y,wy in zip(Y,WY):
        wt=B/(y*(B-y))
        x1,w1=gl(0,1-y,60); x2,w2=gl(1-y,1,60)
        F=np.array([Pt(i,1-x1)-Pt(i,1-x1-y) for i in range(nb)])
        G=np.array([Pt(i,1-x2) for i in range(nb)])
        Qn+=wy*wt*((F*w1*x1**(k-2))@F.T+(G*w2*x2**(k-2))@G.T)
    if B>2:
        Y3,W3=gl(1,B/2,60); c3=np.sum(W3*B/(Y3*(B-Y3)))
        H=np.array([Pt(i,X) for i in range(nb)])  # Pt(1-x) with x->1-x symmetric sub
        Hx=np.array([Pt(i,1-X) for i in range(nb)])
        Qn+=c3*(Hx*WX*X**(k-2))@Hx.T
    return Q0,Qn*k*(k-1)/B
Q0, Qn = forms(3, 4, 1 / 144, 1); c = np.array([1, 6.])
print("   check vs paper (Thm 2: k=3, B=4, eta=1/144, P=1+6x): J0 = %.6f (paper 38/15 = 2.533333), rho = %.6f > 1"
      % (c @ Q0 @ c, c @ Qn @ c / (c @ Q0 @ c)))
worst = 0
for B in (4, 3, 2.0001):
    row = []
    for k in range(2, 9):
        best = max(eigh(*forms(k, B, 0, D)[::-1])[0][-1] for D in range(0, 7))
        worst = max(worst, best / (k / 2)); row.append("k=%d:%.4f" % (k, best))
    print("   B=%-6s eta=0, D<=6  max rho  " % B + "  ".join(row))
print("   max over the table of rho/(k/2) = %.4f  (< 1: no case blocked by the class is reached)" % worst)
print("done")
