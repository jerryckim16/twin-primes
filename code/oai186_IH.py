#!/usr/bin/env python3
"""Rung 186, second sub-step (Session 14): independent evaluation of the normalised trial norm I_H of [14]
(OpenAI, short_gaps_numerics.pdf), formula (2.12), and comparison with its Lemma 2.5 enclosure
    23685317816e-24 <= I_H <= 23685317890e-24.
Everything is taken from notes/sources-186-forms.md (transcription of [14]); nothing from the authors' repository
is used. Own derivation of (2.12) (checked against the transcription):
  F on a 40-cell (j_1..j_40), r = sum j_i < n:  F = prod_i g(t_{j_i}) * sum_sigma p_sigma(r) P_sigma(t),
  p_sigma(r) = sum_d c_{sigma,d} x_r^d,  x_r = (r + 20) h - 9/10,  t_j = (j + 1/2) h.
  Cell weight (one coordinate, cap c): h d_c(j);  normalisation (hZ)^40  =>  K_j(c) = g(t_j)^2 d_c(j) / Z.
  F^2 = prod g^2 * sum_eta Q_eta(r) P_eta(t),  Q_eta = sum_{sigma, tau ordered, sigma+tau = eta} p_sigma p_tau,
  and sum over 40-cells with index sum r of prod K_{j_i} P_eta(t) = [X^r] M_{40,eta}[K],
  M_{d,eta}[K] = sum_{set partitions pi of the labels of eta} (d)_{|pi|} P_0[K]^{d - |pi|} prod_B P_{e(B)}[K],
  P_e[K](X) = sum_{j<n} K_j t_j^e X^j  (expand prod_{e in eta} sum_i t_i^e over maps labels -> coordinates).
  I_H = sum_{shells s} sum_{r in shell s} Q_eta(r) [X^r] M^{c_s}_{40,eta}, shells/caps from table (1.5), outer domain.
Arithmetic: rho_D (closed forms with log, Li2) and Z in mpmath at 110 digits (high precision, NOT interval
arithmetic); the coordinate arrays are then rounded down/up to integers at scale 2^B (with one extra unit of slack),
all polynomial products are exact integer products by Kronecker substitution in GMP (gmpy2), rounded down for the
lower array and up for the upper array (all entries are >= 0, so this gives rigorous enclosures given the inputs);
the final signed sums are exact integer sums (Q_eta scaled to integers), lower/upper chosen by the sign of Q_eta.
usage: oai186_IH.py [--bits 256] [--caps 68225,49152,46580] [--out f.json]"""
import sys, json, time, itertools
from fractions import Fraction as Fr
import gmpy2
from gmpy2 import mpz
from mpmath import mp, mpf, log, polylog

mp.dps = 110
B = int(sys.argv[sys.argv.index("--bits") + 1]) if "--bits" in sys.argv else 256

# ---------------- parameters of [14] (notes/sources-186-forms.md, Sec. 2) ----------------
S = Fr(2742997, 2624989)
NGRID = 98304
h = S / NGRID
n = NGRID - 40                       # 98264 cells, indices 0..n-1, radial index r < n
KDIM = 40
SIGS = [(), (2,), (3,), (4,), (5,), (6,), (2, 2), (2, 3), (2, 4), (3, 3), (2, 2, 2)]
CTAB = json.load(open("code/oai186_table11.json"))           # Table 1.1 integers C_{sigma,d}
C = {tuple(row["sigma"]): [int(v) for v in row["C"]] for row in CTAB}
assert sorted(C) == sorted(SIGS) and all(len(v) == 7 for v in C.values())
# outer domain H_O, (1.5): (r-range inclusive, cap in units of h)
SHELLS = [((0, 89196), 68225), ((89197, 95598), 49152), ((95599, 98263), 46580)]
if "--caps" in sys.argv:
    cs = [int(x) for x in sys.argv[sys.argv.index("--caps") + 1].split(",")]
    SHELLS = [(SHELLS[i][0], cs[i]) for i in range(3)]

# ---------------- Dickman function and cell masses ----------------
KCONST = log(2) ** 2 / 2 + polylog(2, mpf(1) / 2)
def G(u):
    return 2 * u - u * log(u) + u * (log(u) ** 2 - 2 * log(u) + 2) / 2 + u * polylog(2, 1 / u) - (u - 1) * log(u - 1) + u * log(u) - KCONST * u
PHI2 = 3 - 2 * log(2)
G2 = G(mpf(2))
def Phi(u):                     # int_0^u rho_D, valid for u <= 3
    assert u <= 3
    if u <= 1: return u
    if u <= 2: return 2 * u - u * log(u) - 1
    return PHI2 + G(u) - G2

def cellmass(M):
    """d_c(j) = A_j(c)/h for c = M h, j < n: M (Phi((j+1)/M) - Phi(j/M)); = 1 for j + 1 <= M."""
    out = [mpf(1)] * n
    prev = Phi(mpf(M) / M)
    for j in range(M, n):
        cur = Phi(mpf(j + 1) / M)
        out[j] = M * (cur - prev)
        prev = cur
    return out

# ---------------- profile ----------------
def gfun(t):
    return Fr(21, 200) / (1 + t / 100) + Fr(179, 200) / (1 + Fr(907, 5) * t)

# ---------------- Kronecker products with directed rounding ----------------
def pack(arr, W):
    return mpz(int.from_bytes(b"".join(int(x).to_bytes(W, "little") for x in arr), "little"))

def unpack(z, W, m):
    by = int(z).to_bytes(W * (2 * m + 1), "little")
    return [int.from_bytes(by[i * W:(i + 1) * W], "little") for i in range(m)]

def pmul(a, b, up):
    """low n coefficients of a*b / 2^B, rounded down (up=False) or up (up=True); a, b >= 0 integer arrays."""
    ma, mb = max(a), max(b)
    W = (ma.bit_length() + mb.bit_length() + n.bit_length() + 8) // 8 + 1
    c = unpack(pack(a, W) * pack(b, W), W, n)
    if up:
        return [(x + (1 << B) - 1) >> B for x in c]
    return [x >> B for x in c]

def ppow(a, e, up):
    res = None
    base = a
    while e:
        if e & 1:
            res = base if res is None else pmul(res, base, up)
        e >>= 1
        if e:
            base = pmul(base, base, up)
    return res

# ---------------- set partitions ----------------
def set_partitions(lst):
    if not lst:
        yield []
        return
    first, rest = lst[0], lst[1:]
    for p in set_partitions(rest):
        yield [[first]] + p
        for i in range(len(p)):
            yield p[:i] + [[first] + p[i]] + p[i + 1:]

def falling(d, r):
    out = 1
    for i in range(r):
        out *= d - i
    return out

def main():
    t0 = time.time()
    log_ = lambda s: print("[%6.0f s] %s" % (time.time() - t0, s), flush=True)
    # eta = sigma + tau (sorted concatenation), ordered pairs
    pairs = {}
    for s1 in SIGS:
        for s2 in SIGS:
            eta = tuple(sorted(s1 + s2))
            pairs.setdefault(eta, []).append((s1, s2))
    etas = sorted(pairs)
    log_("%d distinct eta" % len(etas))
    # M_{40,eta} = sum over multisets E of block sums: coef(E) * P0^{40-|E|} prod_{e in E} P_e
    Mform = {}
    for eta in etas:
        f = {}
        for pi in set_partitions(list(range(len(eta)))):
            E = tuple(sorted(sum(eta[i] for i in blk) for blk in pi))
            f[E] = f.get(E, 0) + falling(KDIM, len(pi))
        Mform[eta] = f
    allE = sorted({E for f in Mform.values() for E in f}, key=lambda E: (len(E), E))
    log_("%d distinct block-sum multisets; %d set partitions in total" % (
        len(allE), sum(sum(1 for _ in set_partitions(list(range(len(e))))) for e in etas)))
    # exact integer-scaled Q_eta(r): x_r = X_r / Dx
    Dx = 2624989 * NGRID * 10
    # x_r = (r+20) h - 9/10 = ((r+20) * 2742997 * 10 - 9 * 2624989 * 98304) / Dx
    Xr = [(r + 20) * 2742997 * 10 - 9 * 2624989 * NGRID for r in range(n)]
    assert Fr(Xr[5], Dx) == (5 + 20) * h - Fr(9, 10)
    Dpow = [Dx ** (6 - d) for d in range(7)]
    psig = {}
    for s in SIGS:
        cs = C[s]
        psig[s] = [sum(cs[d] * (x ** d) * Dpow[d] for d in range(7)) for x in Xr]   # = 1e10 Dx^6 p_sigma(r)
    DEN = (10 ** 10 * Dx ** 6) ** 2
    log_("p_sigma(r) ready")
    # profile, Z (high precision)
    tj = [(j + Fr(1, 2)) * h for j in range(n)]
    g2 = [mpf((gv := gfun(t)).numerator) / gv.denominator for t in tj]
    g2 = [v * v for v in g2]
    Z = mp.fsum(g2)
    log_("Z = %s" % mp.nstr(Z, 25))
    tjf = [mpf(t.numerator) / t.denominator for t in tj]
    emax = 12
    caps_done = {}
    total_lo, total_up = Fr(0), Fr(0)
    per_shell = []
    SC = mpf(2) ** B
    for (r0, r1), M in SHELLS:
        log_("cap M = %d (shell r = %d..%d): cell masses" % (M, r0, r1))
        d = cellmass(M)
        K = [g2[j] * d[j] / Z for j in range(n)]
        Plo, Pup = {}, {}
        for e in [0] + list(range(2, emax + 1)):
            vals = [K[j] * tjf[j] ** e * SC for j in range(n)]
            Plo[e] = [max(int(mp.floor(v)) - 1, 0) for v in vals]
            Pup[e] = [int(mp.ceil(v)) + 1 for v in vals]
        log_("  coordinate arrays at 2^%d" % B)
        res = {}
        for up in (False, True):
            P = Pup if up else Plo
            p0pow = {34: ppow(P[0], 34, up)}
            for k in range(35, 41):
                p0pow[k] = pmul(p0pow[k - 1], P[0], up)
            prod = {(): None}
            ME = {}
            for E in allE:
                if E and E[:-1] in prod and prod[E[:-1]] is not None:
                    prod[E] = pmul(prod[E[:-1]], P[E[-1]], up)
                elif E:
                    # build from scratch (prefix missing)
                    a = P[E[0]]
                    for e in E[1:]:
                        a = pmul(a, P[e], up)
                    prod[E] = a
                base = p0pow[KDIM - len(E)]
                ME[E] = base if not E else pmul(base, prod[E], up)
            res[up] = ME
            log_("  %s products done (%d multisets)" % ("upper" if up else "lower", len(ME)))
        # signed sums
        lo_num, up_num = 0, 0
        for eta in etas:
            Qr = [0] * (r1 - r0 + 1)
            for (s1, s2) in pairs[eta]:
                a, b = psig[s1], psig[s2]
                for i, r in enumerate(range(r0, r1 + 1)):
                    Qr[i] += a[r] * b[r]
            f = Mform[eta]
            Mlo = [0] * (r1 - r0 + 1); Mup = [0] * (r1 - r0 + 1)
            for E, cf in f.items():
                lo_a, up_a = res[False][E], res[True][E]
                for i, r in enumerate(range(r0, r1 + 1)):
                    Mlo[i] += cf * lo_a[r]; Mup[i] += cf * up_a[r]
            for i in range(r1 - r0 + 1):
                q = Qr[i]
                if q >= 0:
                    lo_num += q * Mlo[i]; up_num += q * Mup[i]
                else:
                    lo_num += q * Mup[i]; up_num += q * Mlo[i]
        lo = Fr(lo_num, DEN << B); upv = Fr(up_num, DEN << B)
        per_shell.append(dict(cap=M, r0=r0, r1=r1, lo=float(lo), up=float(upv)))
        total_lo += lo; total_up += upv
        log_("  shell contribution in [%.15e, %.15e]" % (float(lo), float(upv)))
    ref_lo, ref_up = Fr(23685317816, 10 ** 24), Fr(23685317890, 10 ** 24)
    out = dict(I_H_lo=float(total_lo), I_H_up=float(total_up), I_H_lo_exact=str(total_lo), I_H_up_exact=str(total_up),
               ref_lo=float(ref_lo), ref_up=float(ref_up),
               inside_ref=bool(total_lo >= ref_lo and total_up <= ref_up),
               overlaps_ref=bool(total_up >= ref_lo and total_lo <= ref_up),
               width=float(total_up - total_lo), bits=B, shells=per_shell, seconds=round(time.time() - t0))
    log_(json.dumps({k: v for k, v in out.items() if not k.endswith("exact")}))
    if "--out" in sys.argv:
        json.dump(out, open(sys.argv[sys.argv.index("--out") + 1], "w"), indent=1)

if __name__ == "__main__":
    main()
