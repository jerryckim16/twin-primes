#!/usr/bin/env python3
"""Rung 182 (Session 14 follow-up): independent evaluation of the denominator I(F) = ||F||^2 of the 182 trial of
GPT-6 Astra / R. Sharifi (bundle [M] Sec. 7.3-7.5; data: code/data182/, from formal/TrialData182.lean), compared with the
published enclosure trialDenominatorLower <= I <= trialDenominatorUpper ([M] (7.5)).

Definition used (from notes/sources-182.md, Sec. 3-4, read from the bundle):
  k = 39 coordinates, grid N = 393216, h = S/N, n0 = N - 39 = 393177 cells j < n0, t_j = (j + 1/2) h.
  F(X) = 1_{H_O}(X) prod_i g(t_{j_i}) sum_{c in A} 1_{M0(X) <= c} sum_sigma sum_{d<22} coeff[c][sigma][d] B_{d,3}(s) P_sigma(t),
  s = (r + 39/2) h (r = index sum), B_{d,3} cubic B-splines (Cox-de Boor, right-continuous, the 26 knots),
  A = component caps {141720, 177528, 246256} h, M0 = largest fragment over all coordinates, H_O = outer domain:
  r in 0:352697 / 352698:376449 / 376450:393176 with M0 <= 246256 / 196608 / 186253 h.
  Normalisation: divide by (hZ)^39, Z = sum_{j<n0} g_j^2  =>  coordinate weight K_j(b) = g_j^2 d_b(j) / Z,
  d_b(j) = (1/h) int_{C_j} rho_D(t/b) dt (the cap-b fragment law restricted coordinatewise; nu_c|{max<=b} = nu_b).
Own derivation of the contraction:
  Split by the layer (b_{a-1}, b_a] of M0 over the cap values b_1 < ... < b_5 = 141720, 177528, 186253, 196608, 246256.
  On that layer the active coefficients are v_a = sum of the components with cap >= b_a, and the row r is allowed iff
  its outer shell cap is >= b_a. With M^b_eta = 39-coordinate moment arrays of K(b) (set-partition formula, as in
  code/oai186_IH.py) and Delta M^a = M^{b_a} - M^{b_{a-1}}:
      I = sum_a sum_{r allowed for a} sum_eta Q^{v_a}_eta(r) [X^r] Delta M^a_eta,
      Q^v_eta(r) = sum_{ordered (sigma,tau): sigma+tau = eta} p^v_sigma(r) p^v_tau(r),  p^v_sigma(r) = sum_d v[sigma][d] B_d(s_r).
  By linearity each cap b = b_a enters twice: + with (v_a, mask_a) and - with (v_{a+1}, mask_{a+1}), so every cap is
  processed independently (no differences of rounded arrays).
Arithmetic: B-splines are exact rational cubics in r on each knot span (exact integer evaluation after clearing the
span's denominator); rho_D (closed forms with log and Li2, u <= 393177/141720 < 3), g, Z in mpmath at 110 digits;
coordinate arrays floored at scale 2^B; exact GMP products (Kronecker substitution), floored; exact final integer sums.
So the result is accurate far beyond the 3e-8 relative width of the published enclosure, but it is NOT a rigorous
interval enclosure (floor-only rounding, mpmath special functions). One program.
usage: sharifi182_I.py [--bits 224] [--caps 141720,...] [--out f.json]   (--caps: only these caps; partial results
       are written to code/data182/I_cap_<b>.json and combined when all five exist)"""
import sys, json, time, os
from fractions import Fraction as Fr
from math import lcm
import gmpy2
from gmpy2 import mpz
from mpmath import mp, mpf, log, polylog
sys.path.insert(0, "code")
import sharifi182_data as sd

mp.dps = 110
B = int(sys.argv[sys.argv.index("--bits") + 1]) if "--bits" in sys.argv else 224
D = sd.load()
KD = 39
N = D["N"]
n = N - KD                      # 393177 cells
S = D["trialRadius"]
h = S / N
SIGS = D["signatures"]
CAPS = [141720, 177528, 186253, 196608, 246256]
COMP = [141720, 177528, 246256]
OUTER = [((0, 352697), 246256), ((352698, 376449), 196608), ((376450, 393176), 186253)]

# ---------- Dickman ----------
KCONST = log(2) ** 2 / 2 + polylog(2, mpf(1) / 2)
def G(u):
    return 2 * u - u * log(u) + u * (log(u) ** 2 - 2 * log(u) + 2) / 2 + u * polylog(2, 1 / u) - (u - 1) * log(u - 1) + u * log(u) - KCONST * u
PHI2 = 3 - 2 * log(2)
G2 = G(mpf(2))
def Phi(u):
    assert u <= 3
    if u <= 1: return u
    if u <= 2: return 2 * u - u * log(u) - 1
    return PHI2 + G(u) - G2
def cellmass(M):
    out = [mpf(1)] * n
    prev = Phi(mpf(1))
    for j in range(M, n):
        cur = Phi(mpf(j + 1) / M)
        out[j] = M * (cur - prev)
        prev = cur
    return out

def gq(t):
    return Fr(21, 200) / (1 + t / 100) + Fr(179, 200) / (1 + Fr(907, 5) * t)

# ---------- Kronecker products ----------
def pack(arr, W):
    return mpz(int.from_bytes(b"".join(int(x).to_bytes(W, "little") for x in arr), "little"))
def unpack(z, W, m):
    by = int(z).to_bytes(W * (2 * m + 1), "little")
    return [int.from_bytes(by[i * W:(i + 1) * W], "little") for i in range(m)]
def pmul(a, b):
    W = (max(a).bit_length() + max(b).bit_length() + n.bit_length() + 8) // 8 + 1
    c = unpack(pack(a, W) * pack(b, W), W, n)
    return [x >> B for x in c]
def ppow(a, e):
    res, base = None, a
    while e:
        if e & 1:
            res = base if res is None else pmul(res, base)
        e >>= 1
        if e:
            base = pmul(base, base)
    return res

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

# ---------- B-splines as exact cubics in r on each knot span ----------
def polymul(a, b):
    c = [Fr(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return c
def polyadd(a, b):
    m = max(len(a), len(b))
    return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(m)]
def bspline_span_polys(knots, i):
    """polynomials (in x) of B_{j,3}, j = 0..21, on the span [knots[i], knots[i+1])."""
    T = knots
    nb = len(T) - 1
    Bk = [[Fr(1)] if j == i else [Fr(0)] for j in range(nb)]
    for k in range(1, 4):
        nxt = []
        for j in range(nb - k):
            term = [Fr(0)]
            if T[j + k] != T[j]:
                term = polyadd(term, polymul([-T[j] / (T[j + k] - T[j]), 1 / (T[j + k] - T[j])], Bk[j]))
            if T[j + k + 1] != T[j + 1]:
                term = polyadd(term, polymul([T[j + k + 1] / (T[j + k + 1] - T[j + 1]), -1 / (T[j + k + 1] - T[j + 1])], Bk[j + 1]))
            nxt.append(term)
        Bk = nxt
    return Bk[:22]
def to_r(poly):
    """substitute x = h (r + 39/2): returns coefficients in r."""
    lin = [h * Fr(KD, 2), h]
    out = [Fr(0)]
    pw = [Fr(1)]
    for c in poly:
        out = polyadd(out, [c * x for x in pw])
        pw = polymul(pw, lin)
    return out

def main():
    t0 = time.time()
    log_ = lambda s: print("[%6.0f s] %s" % (time.time() - t0, s), flush=True)
    knots = D["knots"]
    coeff = D["coeff"]                                     # [comp][sigma][d]
    vec = {}
    for b in CAPS:
        comps = [ci for ci, c in enumerate(COMP) if c >= b]
        vec[b] = [[sum(coeff[ci][s][d] for ci in comps) for d in range(22)] for s in range(11)]
    # spans in r
    spans = []
    for i in range(len(knots) - 1):
        if knots[i] < knots[i + 1]:
            lo = knots[i] / h - Fr(KD, 2)
            hi = knots[i + 1] / h - Fr(KD, 2)
            rlo = max(0, -((-lo.numerator) // lo.denominator))          # ceil
            rhi = min(n - 1, -((-hi.numerator) // hi.denominator) - 1)  # r with x_r < knots[i+1]
            if rlo <= rhi:
                spans.append((i, rlo, rhi))
    log_("%d knot spans with cells; first r = %d" % (len(spans), spans[0][1]))
    # exact integer p arrays per distinct coefficient vector
    vkeys = sorted({tuple(tuple(r) for r in vec[b]) for b in CAPS}, key=str)
    vid = {b: vkeys.index(tuple(tuple(r) for r in vec[b])) for b in CAPS}
    pint = {}            # (vi, sigma) -> list over r (0 outside spans)
    den = [0] * n        # common denominator D_span per r (as span id)
    span_den = {}
    for vi, vk in enumerate(vkeys):
        for s in range(11):
            pint[(vi, s)] = [0] * n
    for (i, rlo, rhi) in spans:
        bp = [to_r(p) for p in bspline_span_polys(knots, i)]
        polys = {}
        for vi, vk in enumerate(vkeys):
            for s in range(11):
                pp = [Fr(0)] * 4
                for d in range(22):
                    if vk[s][d] != 0:
                        for k, c in enumerate(bp[d]):
                            pp[k] += vk[s][d] * c
                polys[(vi, s)] = pp
        Dsp = 1
        for pp in polys.values():
            for c in pp:
                Dsp = lcm(Dsp, c.denominator)
        span_den[i] = Dsp
        for key, pp in polys.items():
            ic = [int(c * Dsp) for c in pp]
            arr = pint[key]
            for r in range(rlo, rhi + 1):
                arr[r] = ((ic[3] * r + ic[2]) * r + ic[1]) * r + ic[0]
        for r in range(rlo, rhi + 1):
            den[r] = i
    log_("p arrays ready (%d distinct coefficient vectors)" % len(vkeys))
    # eta and set-partition forms
    pairs = {}
    for a in range(11):
        for b in range(11):
            pairs.setdefault(tuple(sorted(SIGS[a] + SIGS[b])), []).append((a, b))
    etas = sorted(pairs)
    Mform = {}
    for eta in etas:
        f = {}
        for pi in set_partitions(list(range(len(eta)))):
            E = tuple(sorted(sum(eta[i] for i in blk) for blk in pi))
            f[E] = f.get(E, 0) + falling(KD, len(pi))
        Mform[eta] = f
    allE = sorted({E for f in Mform.values() for E in f}, key=lambda E: (len(E), E))
    # profile, Z
    tq = [(j + Fr(1, 2)) * h for j in range(n)]
    g2 = []
    for t in tq:
        v = gq(t)
        x = mpf(v.numerator) / v.denominator
        g2.append(x * x)
    Z = mp.fsum(g2)
    tj = [mpf(t.numerator) / t.denominator for t in tq]
    log_("Z = %s" % mp.nstr(Z, 25))
    SC = mpf(2) ** B
    def mask_end(b):          # last allowed r for layer value b (rows whose outer shell cap >= b)
        return max(r1 for (r0, r1), c in OUTER if c >= b)
    todo = [int(x) for x in sys.argv[sys.argv.index("--caps") + 1].split(",")] if "--caps" in sys.argv else CAPS
    for b in todo:
        a = CAPS.index(b)
        d = cellmass(b)
        K = [g2[j] * d[j] / Z for j in range(n)]
        P = {}
        for e in [0] + list(range(2, 13)):
            P[e] = [max(int(mp.floor(K[j] * tj[j] ** e * SC)), 0) for j in range(n)]
        log_("cap %d: coordinate arrays" % b)
        p0 = {KD - 6: ppow(P[0], KD - 6)}
        for k in range(KD - 5, KD + 1):
            p0[k] = pmul(p0[k - 1], P[0])
        prod = {}
        def getprod(E):
            if E not in prod:
                prod[E] = P[E[0]] if len(E) == 1 else pmul(getprod(E[:-1]), P[E[-1]])
            return prod[E]
        ME = {}
        for E in allE:
            ME[E] = p0[KD - len(E)] if not E else pmul(p0[KD - len(E)], getprod(E))
        prod.clear(); p0.clear(); P.clear()
        log_("cap %d: %d moment products done" % (b, len(ME)))
        # contraction: + (v_a, mask_a), - (v_{a+1}, mask_{a+1})
        terms = [(+1, vid[b], mask_end(b))]
        if a + 1 < len(CAPS):
            terms.append((-1, vid[CAPS[a + 1]], mask_end(CAPS[a + 1])))
        acc = {}      # span id -> integer
        for eta in etas:
            M = [0] * n
            for E, cf in Mform[eta].items():
                arr = ME[E]
                for r in range(n):
                    M[r] += cf * arr[r]
            for sgn, vi, rend in terms:
                for (i, rlo, rhi) in spans:
                    hi_ = min(rhi, rend)
                    if hi_ < rlo:
                        continue
                    tot = 0
                    pl = [(pint[(vi, x)], pint[(vi, y)]) for (x, y) in pairs[eta]]
                    for r in range(rlo, hi_ + 1):
                        q = 0
                        for (u, v) in pl:
                            q += u[r] * v[r]
                        if q:
                            tot += q * M[r]
                    acc[i] = acc.get(i, 0) + sgn * tot
        val = sum(Fr(v, span_den[i] ** 2) for i, v in acc.items()) / (1 << B)
        json.dump(dict(cap=b, value=str(val), value_float=float(val), bits=B), open("code/data182/I_cap_%d.json" % b, "w"), indent=1)
        log_("cap %d: contribution %.15e" % (b, float(val)))
        ME.clear()
    if all(os.path.exists("code/data182/I_cap_%d.json" % b) for b in CAPS):
        I = sum(Fr(json.load(open("code/data182/I_cap_%d.json" % b))["value"]) for b in CAPS)
        lo, up = D["trialDenominatorLower"], D["trialDenominatorUpper"]
        out = dict(I=float(I), I_exact_of_floored=str(I), ref_lo=float(lo), ref_up=float(up), inside=bool(lo <= I <= up),
                   rel_pos_in_enclosure=float((I - lo) / (up - lo)), bits=B)
        log_(json.dumps({k: v for k, v in out.items() if k != "I_exact_of_floored"}))
        if "--out" in sys.argv:
            json.dump(out, open(sys.argv[sys.argv.index("--out") + 1], "w"), indent=1)

if __name__ == "__main__":
    main()
