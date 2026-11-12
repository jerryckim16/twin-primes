#!/usr/bin/env python3
r"""capped_check.py -- independent EXACT evaluator of I_T, J_T for a capped support T.

usage:  python3 code/capped_check.py P.json [--out result.json] [--procs 4] [--quiet]

Input JSON: k, L, tau, g, caps {"1":..,"2":..,"3+":..}, basis [[a,[b_2,b_3,..]],..], coeffs.
  P(u) = sum_i c_i (L-P1)^{a_i} prod_{j>=2} P_j^{b_i[j-2]},  F = P * 1_T,
  T = {u>=0, |u|<=L, s(u) <= C_{m(u)}},  I(u)={i: u_i>g}, m=|I(u)|, s(u)=sum_{I(u)} u_i.
Output: I_T = int_T P^2,  J_T = int_{u' in tau*Simplex_{k-1}} (int F du_k)^2,  ratio = k J_T / I_T.

METHOD (direct sum over the exact large set; no "cap-free minus correction"):

 (1) Exact large set by inclusion-exclusion.  1[exactly A large] = sum_{B} (-1)^{|B|} 1[A>g, B>g]
     (B ranges over the other coordinates).  Hence
        I_T = sum_m C(k,m) sum_r (-1)^r C(k-m,r) G(m,r),
        G(m,r) = int_{u_A>g (|A|=m), u_B>g (|B|=r), u_Z>=0, |u|<=L, s_A<=C_m} P^2,
     and likewise for J over u' (k-1 coordinates) with the fibre integral below.
     Only (m+r) g < L (resp. < tau) contributes.

 (2) Three groups A (shifted by g, carries the cap), B (shifted by g), Z (free).  In shifted
     coordinates x, put s = |x_A|, sigma = |x_B|+|x_Z|, y = L - |u| (so s+sigma+y = L' := L-(m+r)g).
     For a power-sum monomial P^F (F = multiplicity vector, P_j summed over all coordinates)
        E[P^F(u)]  with u_A = g+lam X_A, u_B = g+mu X_B, u_Z = mu X_Z,  X iid Exp(1)
        = F! [z^F] phi(z;lam)^m * phi(z;mu)^r * Zeta_n(z;mu),
     phi(z;x) = sum_F z^F/F! E[(g+xX)^{w(F)}],  Zeta_n = (sum_F z^F w(F)!/F! x^{w(F)})^n.
     The coefficient of lam^a mu^d is the sum of coefficient*beta! over monomials x^beta of
     bidegree (a,d); the Dirichlet slice integrals turn it into the density
        s^{m-1+a}/(m-1+a)!  *  sigma^{|R|-1+d}/(|R|-1+d)!       (R = B u Z),
     with the convention s^{-1}/(-1)! = delta(s) for an empty group.

 (3) Regions in (s,sigma,y) and kernels.  With e_n(x) = x^n/n! (e_n * e_p = e_{n+p+1}):
     * I:  int_{s<=c, sigma,y>=0} s^i/i! sigma^j/j! y^alpha = alpha! int_0^{c} s^i/i! e_{j+alpha+1}(L'-s) ds.
     * J:  G(u') = int_0^U P dt with U = min(y, max(g, C_{m'+1}-s')), expanded as a polynomial
           Q(u';y,v) = sum q_{F,beta,gamma} P'^F y^beta v^gamma, v = U.  With c1 = C_{m'}-m'g,
           c2 = C_{m'+1}-m'g, delta = L - tau (requires C_{m+1} <= C_m + g and g >= L - tau):
             J(m',r) = Base(s in [0,c1],        y >= delta, v=y)
                     + Base(s in (c2-g, c1],    y >= g,     v=g)  - Base(same, v=y)
                     + Rect(s in [0,min(c1,c2-g)], sigma < L'-c2, v=c2-s) - Rect(same, v=y)
           Base = {s-range, sigma>=0, y>=y0}: shift y=y0+y', then
                int sigma^j/j! (y0+y')^b = sum_l b!/(b-l)! y0^{b-l} e_{j+l+1}(L'-y0-s).
           Rect: u~ = c2-s, y~ = L'-c2-sigma, y = u~ + y~ (two independent segments):
                int_0^{L'-c2} sigma^j/j! y~^l = l! e_{j+l+1}(L'-c2),  s-kernel int s^i/i! (c2-s)^e ds.

 (4) Contractions.  Base parts:  V_{F'}(T) = sum_{F''} B_{F''}(T) * eta_{F'+F''}(T) (integer polynomial
     products, T-index = d + l), W_a = sum_{F'} A_{F'}[a] V_{F'}, then pairing with the 1-D kernels.
     Rect part: the s-kernel is applied to A first (A~_{F'}[e]), then per F the integer matrix
     contraction sum_{F'+F''=F} Bt_{F''}^T eta_F A~_{F'}.  Every family is scaled to integers by one
     common denominator; all arithmetic is exact (python-flint).
"""
import sys, json, time, argparse, itertools, os
from math import comb, factorial
from flint import fmpq, fmpq_poly, fmpq_mat, fmpz, fmpz_poly, fmpz_mat


def toq(x):
    s = str(x).strip()
    if "/" in s:
        p, q = s.split("/")
        return fmpq(int(p), int(q))
    return fmpq(int(s))


def efac(x, n):
    """e_n(x) = x^n / n!"""
    return x ** n / factorial(n)


ZERO = fmpq_poly()


# ----------------------------------------------------------------------------------------------
class Index:
    """All multiplicity vectors F over the given parts with weight w(F) <= W, sorted by weight,
    together with the list of pairs (F',F'') with w(F')+w(F'') <= W."""

    def __init__(self, parts, W):
        self.parts, self.W = parts, W
        idx = []

        def rec(t, rem, cur):
            if t == len(parts):
                idx.append(tuple(cur)); return
            j = parts[t]
            for e in range(rem // j + 1):
                cur.append(e); rec(t + 1, rem - e * j, cur); cur.pop()

        rec(0, W, [])
        wt = lambda f: sum(j * e for j, e in zip(parts, f))
        idx.sort(key=lambda f: (wt(f), f))
        self.idx = idx
        self.pos = {f: i for i, f in enumerate(idx)}
        self.wt = [wt(f) for f in idx]
        self.fact = []
        for f in idx:
            v = 1
            for e in f: v *= factorial(e)
            self.fact.append(v)
        self.pairs = []
        for i1, f1 in enumerate(idx):
            lst = []
            w1 = self.wt[i1]
            for i2, f2 in enumerate(idx):
                if w1 + self.wt[i2] > W: break
                lst.append((i2, self.pos[tuple(a + b for a, b in zip(f1, f2))]))
            self.pairs.append(lst)
        self.npairs = sum(len(l) for l in self.pairs)
        self.bysum = [[] for _ in idx]
        for i1, lst in enumerate(self.pairs):
            for i2, isum in lst: self.bysum[isum].append((i1, i2))

    def __len__(self): return len(self.idx)


def series_mul(S1, S2, ix):
    """product of two series with fmpq_poly coefficients (ordinary coefficients)."""
    out = [fmpq_poly() for _ in range(len(ix))]
    for i1, a in enumerate(S1):
        if a.is_zero(): continue
        for i2, isum in ix.pairs[i1]:
            b = S2[i2]
            if b.is_zero(): continue
            out[isum] += a * b
    return out


def scalar_series_mul(S1, S2, ix):
    out = [fmpq(0)] * len(ix)
    for i1, a in enumerate(S1):
        if a == 0: continue
        for i2, isum in ix.pairs[i1]:
            b = S2[i2]
            if b == 0: continue
            out[isum] += a * b
    return out


# ----------------------------------------------------------------------------------------------
class Problem:
    def __init__(self, data):
        self.k = int(data["k"])
        self.L, self.tau, self.g = toq(data["L"]), toq(data["tau"]), toq(data["g"])
        self.caps = {str(kk): toq(v) for kk, v in data["caps"].items()}
        self.delta = self.L - self.tau
        coeffs = [toq(c) for c in data["coeffs"]]
        basis = data["basis"]
        parts = sorted({jj + 2 for a, b in basis for jj, e in enumerate(b) if e})
        if not parts: parts = [2]
        self.parts = parts
        terms = []
        for (a, b), c in zip(basis, coeffs):
            if c == 0: continue
            bb = [0] * (max(len(b), parts[-1] - 1))
            bb[:len(b)] = b
            F = tuple(bb[j - 2] for j in parts)
            terms.append((int(a), F, c))
        self.terms = terms
        self.deg = max(a + sum(j * e for j, e in zip(parts, F)) for a, F, c in terms)
        self.W = 2 * self.deg
        assert self.g >= self.delta, "need g >= L - tau"
        assert self.delta >= 0
        m = 1
        while (m) * self.g < self.L + 1:
            if self.cap(m + 1) > self.cap(m) + self.g:
                raise ValueError("need C_{m+1} <= C_m + g")
            m += 1

    def cap(self, m):
        if m <= 0: return None
        if str(m) in self.caps: return self.caps[str(m)]
        best = None
        for kk, v in self.caps.items():
            if kk.endswith("+") and int(kk[:-1]) <= m:
                if best is None or int(kk[:-1]) > best[0]: best = (int(kk[:-1]), v)
        if best is None: raise ValueError("no cap for m=%d" % m)
        return best[1]

    # ------------------------------------------------------------------ coefficient data
    def prepare(self, log=print):
        t0 = time.time()
        ix = Index(self.parts, self.W)
        self.ix = ix
        N, W, g = len(ix), self.W, self.g
        log("index: %d multi-indices, %d pairs, W=%d, parts=%s" % (N, ix.npairs, W, self.parts))
        # ---- I side: P = sum_F p_F(y) P^F, y = L - P1
        pF = {}
        for a, F, c in self.terms:
            i = ix.pos[F]
            pF[i] = pF.get(i, fmpq_poly()) + fmpq_poly([0] * a + [c])
        keys = sorted(pF)
        kapI = [fmpq_poly() for _ in range(N)]
        for i1 in keys:
            f1 = ix.idx[i1]
            for i2 in keys:
                isum = ix.pos[tuple(x + y for x, y in zip(f1, ix.idx[i2]))]
                kapI[isum] += pF[i1] * pF[i2]
        self.etaI = []
        for i in range(N):
            cs = kapI[i].coeffs()
            self.etaI.append(fmpq_poly([cs[al] * factorial(al) * ix.fact[i] for al in range(len(cs))]))
        # ---- J side: Q(u';y,v) = int_0^v P(u',t) dt, packed y^beta v^gamma -> X^(beta + SY*gamma)
        SY = W + 3
        self.SY = SY
        cache = {}

        def inner(a, Wd):   # int_0^v (y-t)^a t^Wd dt = sum_q C(a,q)(-1)^q y^(a-q) v^(Wd+q+1)/(Wd+q+1)
            key = (a, Wd)
            if key not in cache:
                cs = [fmpq(0)] * (a + SY * (Wd + a + 1) + 1)
                for q in range(a + 1):
                    cs[(a - q) + SY * (Wd + q + 1)] += fmpq((-1) ** q * comb(a, q), Wd + q + 1)
                cache[key] = fmpq_poly(cs)
            return cache[key]

        qF = {}
        for a, F, c in self.terms:
            for e in itertools.product(*[range(x + 1) for x in F]):
                mult = 1
                for x, y in zip(F, e): mult *= comb(x, y)
                Wd = sum(j * x for j, x in zip(self.parts, e))
                rest = tuple(x - y for x, y in zip(F, e))
                i = ix.pos[rest]
                qF[i] = qF.get(i, fmpq_poly()) + inner(a, Wd) * (c * mult)
        keys = sorted(qF)
        kapJ = [fmpq_poly() for _ in range(N)]
        for i1 in keys:
            f1 = ix.idx[i1]
            for i2 in keys:
                isum = ix.pos[tuple(x + y for x, y in zip(f1, ix.idx[i2]))]
                kapJ[isum] += qF[i1] * qF[i2]
        LM = W + 2                 # max power of y (or v) in Q^2
        S2 = 2 * LM + 1
        self.LM, self.S2 = LM, S2
        SA = W + 3                 # packing stride for the (I | J_delta | J_g) bundle
        self.SA = SA
        delta = self.delta
        etaP, etaII = [], []
        fl = [factorial(n) for n in range(2 * LM + 2)]
        for i in range(N):
            Ff = ix.fact[i]
            cs = kapJ[i].coeffs()
            kap = {}
            for pidx, val in enumerate(cs):
                if val != 0:
                    kap[(pidx % SY, pidx // SY)] = val
            ky = {}   # v = y : merged power
            kg = {}   # v = g
            for (b, gm), val in kap.items():
                ky[b + gm] = ky.get(b + gm, 0) + val
                kg[b] = kg.get(b, 0) + val * g ** gm
            # eta_delta(T) = F! sum_b ky[b] sum_l b!/(b-l)! delta^(b-l) T^l
            ed = [fmpq(0)] * (LM + 1)
            for b, val in ky.items():
                for l in range(b + 1):
                    ed[l] += val * fmpq(fl[b], fl[b - l]) * delta ** (b - l)
            eg = [fmpq(0)] * (LM + 1)
            for b in set(ky) | set(kg):
                val = kg.get(b, 0) - ky.get(b, 0)
                if val == 0: continue
                for l in range(b + 1):
                    eg[l] += val * fmpq(fl[b], fl[b - l]) * g ** (b - l)
            # packed bundle: I (stride 0) + T^SA J_delta + T^(2SA) J_g
            cI = self.etaI[i].coeffs()
            bundle = [fmpq(0)] * (3 * SA)
            for n, v in enumerate(cI): bundle[n] = v
            for n in range(LM + 1):
                bundle[SA + n] = ed[n] * Ff
                bundle[2 * SA + n] = eg[n] * Ff
            etaP.append(fmpq_poly(bundle))
            # Rect part: eta_II[l,e] packed at e*S2 + (LM-l)
            eII = {}
            for (b, gm), val in kap.items():          # v = c2 - s : + C(b,l) l! at e = b-l+gm
                for l in range(b + 1):
                    key = (l, b - l + gm)
                    eII[key] = eII.get(key, 0) + val * fmpq(fl[b], fl[b - l])
            for b, val in ky.items():                 # v = y : - C(b,l) l! at e = b-l
                for l in range(b + 1):
                    key = (l, b - l)
                    eII[key] = eII.get(key, 0) - val * fmpq(fl[b], fl[b - l])
            etaII.append([(l, e, val * Ff) for (l, e), val in sorted(eII.items()) if val != 0])
        self.etaP, self.etaII = etaP, etaII
        self.etaPz = to_int(etaP)
        import math
        DII = 1
        for lst in etaII:
            for l, e, v in lst: DII = math.lcm(DII, int(v.q))
        mats = []
        for i, lst in enumerate(etaII):
            if not lst: mats.append(None); continue
            nn = W + 3 - ix.wt[i]
            M = fmpz_mat(nn, nn)
            for l, e, v in lst: M[l, e] = int(v * DII)
            mats.append(M)
        self.etaIIm = (mats, fmpz(DII))
        # ---- base series phi(z;x) = sum_F z^F/F! E[(g+xX)^w(F)]
        def Mw(wd):
            return fmpq_poly([fmpq(comb(wd, l) * factorial(l)) * g ** (wd - l) for l in range(wd + 1)])
        Mcache = {}
        self.phi = []
        for i in range(N):
            wd = ix.wt[i]
            if wd not in Mcache: Mcache[wd] = Mw(wd)
            self.phi.append(Mcache[wd] * fmpq(1, ix.fact[i]))
        self.zeta = [fmpq(factorial(ix.wt[i]), ix.fact[i]) for i in range(N)]
        log("prepare: %.1fs" % (time.time() - t0))

    # ------------------------------------------------------------------ combos
    def combos(self):
        """list of (kind, m, r, nZ) with nonzero contribution; kind 'I' or 'J'."""
        out = []
        k, L, g, tau = self.k, self.L, self.g, self.tau
        for m in range(0, k + 1):
            if m >= 1 and self.cap(m) - m * g <= 0: continue
            for r in range(0, k - m + 1):
                if L - (m + r) * g <= 0: break
                out.append(("I", m, r, k - m - r))
        for m in range(0, k):
            if m >= 1 and self.cap(m) - m * g <= 0: continue
            for r in range(0, k - 1 - m + 1):
                if tau - (m + r) * g <= 0: break
                out.append(("J", m, r, k - 1 - m - r))
        return out

    def prepare_powers(self, combos, log=print):
        t0 = time.time()
        ix = self.ix
        need_phi = max(max(c[1], c[2]) for c in combos)
        self.phipow = [None] * (need_phi + 1)
        unit = [fmpq_poly([1]) if i == 0 else fmpq_poly() for i in range(len(ix))]
        self.phipow[0] = unit
        for j in range(1, need_phi + 1):
            self.phipow[j] = series_mul(self.phipow[j - 1], self.phi, ix)
        self.phipowz = [to_int(P) for P in self.phipow]
        nset = sorted({c[3] for c in combos})
        self.Zn = {}
        sunit = [fmpq(1) if i == 0 else fmpq(0) for i in range(len(ix))]
        n0 = nset[0]
        res, base, e = sunit, self.zeta, n0
        while e:
            if e & 1: res = scalar_series_mul(res, base, ix)
            e >>= 1
            if e: base = scalar_series_mul(base, base, ix)
        cur, curn = res, n0
        for n in nset:
            while curn < n:
                cur = scalar_series_mul(cur, self.zeta, ix); curn += 1
            self.Zn[n] = cur
        log("powers: phi^0..%d, Zeta_n for n in %s: %.1fs" % (need_phi, nset, time.time() - t0))

    def Bseries(self, r, nZ):
        ix = self.ix
        Z = self.Zn[nZ]
        Zp = [fmpq_poly([0] * ix.wt[i] + [Z[i]]) if Z[i] != 0 else fmpq_poly() for i in range(len(ix))]
        return series_mul(self.phipow[r], Zp, ix)

    # ------------------------------------------------------------------ kernels
    class Kern:
        """K(i,n) = int_{s0}^{s1} s^i/i! e_n(Lam-s) ds (i>=0), via the exact antiderivative
           -sum_{t=0}^{i} e_{i-t}(s) e_{n+1+t}(Lam-s);  i=-1: delta at s=0 (included iff inc0)."""

        def __init__(self, Lam, s0, s1, inc0, nmax):
            self.Lam, self.inc0, self.cache = Lam, inc0, {}
            s0 = max(s0, fmpq(0)); s1 = min(s1, Lam)
            self.empty = not (s1 > s0)
            self.ends = []
            if not self.empty:
                for s, sg in ((s1, 1), (s0, -1)):
                    es = [fmpq(1)]
                    el = [fmpq(1)]
                    for j in range(1, nmax + 2):
                        es.append(es[-1] * s / j)
                        el.append(el[-1] * (Lam - s) / j)
                    self.ends.append((sg, es, el))

        def __call__(self, i, n):
            if i == -1:
                return efac(self.Lam, n) if self.inc0 else fmpq(0)
            if self.empty: return fmpq(0)
            key = (i, n)
            v = self.cache.get(key)
            if v is None:
                v = fmpq(0)
                for sg, es, el in self.ends:
                    acc = fmpq(0)
                    for t in range(i + 1):
                        acc += es[i - t] * el[n + 1 + t]
                    v -= sg * acc
                self.cache[key] = v
            return v

    # ------------------------------------------------------------------ one group (r, nZ)
    def run_group(self, r, nZ, todo):
        """todo: list of (kind, m).  Returns dict {(kind,m,r): fmpq}.
        Inner loops run on integer polynomials (each family scaled by one common denominator)."""
        ix = self.ix
        N = len(ix)
        k, L, g, delta = self.k, self.L, self.g, self.delta
        SA, LM, W = self.SA, self.LM, self.W
        Bz, DB = to_int(self.Bseries(r, nZ))
        Ez, DE = self.etaPz
        # V_{F'} = sum_{F''} B_{F''} * etaP_{F'+F''}       (scaled by DB*DE)
        V = []
        for i1 in range(N):
            acc = fmpz_poly()
            for i2, isum in ix.pairs[i1]:
                b = Bz[i2]
                if b.is_zero(): continue
                e = Ez[isum]
                if e.is_zero(): continue
                acc += b * e
            V.append(acc)

        def Wform(Az, Vlist):
            Ws = {}
            for i1 in range(N):
                v = Vlist[i1]
                if v.is_zero(): continue
                for a, ca in enumerate(Az[i1].coeffs()):
                    if ca == 0: continue
                    Ws[a] = Ws.get(a, fmpz_poly()) + v * ca
            return Ws

        res = {}
        nmax = k + 4 * self.W + 20
        for kind, m in todo:
            A = self.phipow[m]
            Az, DA = self.phipowz[m]
            Ws = Wform(Az, V)
            scale = fmpq(1) / (DA * DB * DE)
            if kind == "I":
                Lp = L - (m + r) * g
                nR = k - m
                s1 = self.cap(m) - m * g if m >= 1 else fmpq(0)
                tot = fmpq(0)
                K = self.Kern(Lp, fmpq(0), s1, True, nmax)
                for a, Wp in Ws.items():
                    cs = Wp.coeffs()[:SA]
                    for n, val in enumerate(cs):
                        if val == 0: continue
                        tot += val * K(m - 1 + a, nR + n)
                res[("I", m, r)] = tot * scale
                continue
            Lp = L - (m + r) * g
            nR = k - 1 - m
            c1 = self.cap(m) - m * g if m >= 1 else None
            c2 = self.cap(m + 1) - m * g
            tot = fmpq(0)
            # Base(s in [0,c1], y >= delta, v = y)
            Lam = Lp - delta
            s1 = c1 if m >= 1 else fmpq(0)
            K = self.Kern(Lam, fmpq(0), s1, True, nmax)
            for a, Wp in Ws.items():
                cs = Wp.coeffs()
                for n in range(SA, min(2 * SA, len(cs))):
                    val = cs[n]
                    if val == 0: continue
                    tot += val * K(m - 1 + a, nR + n - SA)
            # Base(s in (c2-g, c1], y >= g, v=g) - Base(same, v=y)
            Lam = Lp - g
            if Lam > 0:
                s0 = c2 - g
                s1 = c1 if m >= 1 else fmpq(0)
                K = self.Kern(Lam, s0, s1, (c2 - g < 0), nmax)
                for a, Wp in Ws.items():
                    cs = Wp.coeffs()
                    for n in range(2 * SA, len(cs)):
                        val = cs[n]
                        if val == 0: continue
                        tot += val * K(m - 1 + a, nR + n - 2 * SA)
            tot *= scale
            # Rect(s in [0, min(c1,c2-g)], sigma < L'-c2): v = c2-s minus v = y
            Sig = Lp - c2
            s1 = (min(c1, c2 - g) if m >= 1 else fmpq(0))
            if Sig > 0 and c2 - g >= 0:
                # beta~_{F''}[l] = sum_d B[d] e_{nR+d+l}(Sig)  via one product with a reversed table
                H = 2 * LM + 2
                hz, Dh = to_int([fmpq_poly([efac(Sig, nR + H - t) if nR + H - t >= 0 else 0
                                            for t in range(H + 1)])])
                hz = hz[0]
                Btz = []
                for i2 in range(N):
                    b = Bz[i2]
                    if b.is_zero():
                        Btz.append(fmpz_poly()); continue
                    prod = (b * hz).coeffs()
                    nF = W + 2 - ix.wt[i2]
                    Btz.append(fmpz_poly([prod[H - l] if H - l < len(prod) else 0 for l in range(nF + 1)]))
                # A~_{F'}[e] = sum_a A_{F'}[a] e! K(m-1+a, e)   (s-kernel applied first)
                K = self.Kern(c2, fmpq(0), s1, True, nmax)
                SX = LM + 1
                amax = W + 2
                Kmat = fmpq_mat(amax + 1, LM + 1, [factorial(e) * K(m - 1 + a, e)
                                                   for a in range(amax + 1) for e in range(LM + 1)])
                Amat = fmpq_mat(N, amax + 1)
                for i1 in range(N):
                    for a, ca in enumerate(A[i1].coeffs()):
                        Amat[i1, a] = ca
                AK = Amat * Kmat
                AKl = [[AK[i, e] for e in range(W + 3 - ix.wt[i])] for i in range(N)]
                import math
                DAK = 1
                for row in AKl:
                    for v in row: DAK = math.lcm(DAK, int(v.q))
                AKz = [[int(v * DAK) for v in row] for row in AKl]
                Btl = [[int(c) for c in b.coeffs()] for b in Btz]
                Iz, DII = self.etaIIm
                # rect = sum_F sum_{F'+F''=F} Bt_{F''}^T eta_F A~_{F'}   (per F: two integer matrix products)
                acc = fmpz(0)
                for i in range(N):
                    M = Iz[i]
                    if M is None: continue
                    nn = W + 3 - ix.wt[i]
                    r1, r2 = [], []
                    for i1, i2 in ix.bysum[i]:
                        bt = Btl[i2]
                        if not bt: continue
                        r1.extend(bt[:nn] + [0] * (nn - min(nn, len(bt))))
                        r2.extend(AKz[i1][:nn])
                    if not r1: continue
                    p = len(r1) // nn
                    M1 = fmpz_mat(p, nn, r1)
                    M2 = fmpz_mat(p, nn, r2)
                    Y = M1 * M
                    Z = Y.transpose() * M2
                    for j in range(nn): acc += Z[j, j]
                tot += fmpq(acc) / (DB * Dh * DAK * DII)
            res[("J", m, r)] = tot
        return res


def to_int(polys):
    """scale a family of fmpq_poly by the lcm D of their denominators -> (fmpz_polys, D)"""
    import math
    D = 1
    for p in polys:
        if not p.is_zero(): D = math.lcm(D, int(p.denom()))
    D = fmpz(D)
    return [(p * D).numer() if not p.is_zero() else fmpz_poly() for p in polys], D


# ----------------------------------------------------------------------------------------------
_PB = None


def _worker(task):
    r, nZ, todo = task
    t0 = time.time()
    res = _PB.run_group(r, nZ, todo)
    return [(kk[0], kk[1], kk[2], str(v)) for kk, v in res.items()], time.time() - t0, (r, nZ)


def evaluate(data, procs=1, log=print):
    global _PB
    pb = Problem(data)
    pb.prepare(log=log)
    cmb = pb.combos()
    pb.prepare_powers(cmb, log=log)
    groups = {}
    for kind, m, r, nZ in cmb:
        groups.setdefault((r, nZ), []).append((kind, m))
    tasks = [(r, nZ, todo) for (r, nZ), todo in groups.items()]
    tasks.sort(key=lambda t: -len(t[2]))
    _PB = pb
    vals = {}
    t0 = time.time()
    if procs > 1 and len(tasks) > 1:
        import multiprocessing as mp
        ctx = mp.get_context("fork")
        with ctx.Pool(procs) as pool:
            for out, dt, key in pool.imap_unordered(_worker, tasks):
                for kind, m, r, v in out: vals[(kind, m, r)] = toq(v)
                log("  group r=%d nZ=%d done in %.1fs (elapsed %.1fs)" % (key[0], key[1], dt, time.time() - t0))
    else:
        for task in tasks:
            out, dt, key = _worker(task)
            for kind, m, r, v in out: vals[(kind, m, r)] = toq(v)
            log("  group r=%d nZ=%d done in %.1fs" % (key[0], key[1], dt))
    k = pb.k
    IT, JT = fmpq(0), fmpq(0)
    for (kind, m, r), v in vals.items():
        if kind == "I":
            IT += comb(k, m) * (-1) ** r * comb(k - m, r) * v
        else:
            JT += comb(k - 1, m) * (-1) ** r * comb(k - 1 - m, r) * v
    return IT, JT, vals, pb


def fq(x):
    from fractions import Fraction
    return float(Fraction(int(x.p), int(x.q)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pjson")
    ap.add_argument("--out")
    ap.add_argument("--procs", type=int, default=1)
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    log = (lambda *x: None) if a.quiet else (lambda *x: print(*x, flush=True))
    data = json.load(open(a.pjson))
    t0 = time.time()
    IT, JT, vals, pb = evaluate(data, procs=a.procs, log=log)
    ratio = pb.k * JT / IT
    from fractions import Fraction
    rf = Fraction(int(ratio.p), int(ratio.q))
    out = dict(input=a.pjson, k=pb.k, I_T=str(IT), J_T=str(JT), I_T_float=fq(IT), J_T_float=fq(JT),
               ratio_float=float(rf), ratio_12=("%.12f" % float(rf)), ratio_gt_4=bool(ratio > 4),
               seconds=round(time.time() - t0, 1),
               parts={"%s_m%d_r%d" % kk: str(v) for kk, v in sorted(vals.items())})
    print(json.dumps({x: out[x] for x in out if x != "parts"}, indent=1), flush=True)
    if a.out:
        json.dump(out, open(a.out, "w"), indent=1)


if __name__ == "__main__":
    main()
