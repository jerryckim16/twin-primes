#!/usr/bin/env python3
"""EXACT capped functionals I_T(P) and J_T(P 1_T) on Stadlmann's one-band support (Session 6).

Coordinates u (Polymath scaling, u = 4t of [Sta26]): support
  T = {u >= 0 : |u| <= L, s(u) <= C_{m(u)}},  I(u) = {i : u_i > g}, m(u) = |I(u)|, s(u) = sum_{I(u)} u_i,
criterion k J_T(F) / I_T(F) > 4 with J_T(F) = int_{|u'| <= tau} (int F(u', t) dt)^2 du'.
F = P 1_T with P(u) = sum_b prod_l P_l(u)^{b_l} p_b(R), R = L - |u| (input format: code/to_ucoords.py).

Organisation ("cap-free minus exact corrections"):
  I_T = I(P) - int_V P^2,             V = {|u| <= L} \\ T,
  J_T = J(P) - Corr1 - Corr2,         Q(u', x) = int_0^x P(u', t) dt, R = L - |u'|,
    Corr1 = int_{|u'| <= tau, u' not admissible} Q(u', R)^2,
    Corr2 = int_{u' admissible, U < R} [Q(R)^2 - Q(U)^2],  U = min(R, max(g, C_{m'+1} - s(u'))).
Every piece is "exactly the set A (|A| = m) is large" with a condition on s = sum_A u, handled by
inclusion-exclusion over j further coordinates forced > g (sign (-1)^j, C(n, m) C(n - m, j) copies).
Given m, j: z = u - g on the m + j forced coordinates, r_A = |z_A|, rho = |z_B| + |y|; the shape integral of
prod_l P_l(u)^{B_l} at fixed (r_A, rho) is sum_{e_A + e_R = B} mult * dA(m, e_A)(r_A) * dRest(j, n', e_R)(rho),
dA = density of the m shifted coordinates (caps_exact.CapPieces.density), dRest = convolution of the j shifted
coordinates with the n' = n - m - j free ones (Dirichlet: E_{n'}[e] r^{n'-1+w}/(n'-1+w)!).
Regions in the (r_A, rho) plane:
  T1 (I-correction, Corr1, Corr2 case b): lo <= r_A <= hi, 0 <= rho <= Lam - r_A, integrand H(Lam - r_A - rho);
     int rho^b (Lam - r_A - rho)^p drho = b! p!/(b+p+1)! (Lam - r_A)^{b+p+1}.
  T2 (Corr2 case c): 0 <= r_A <= a, 0 <= rho <= rc, x = c' - r_A, R = x + (rc - rho), integrand h(R, x).
All arithmetic is exact (flint fmpq / fmpq_poly).

usage: capped_exact.py P_u.json [--out result.json] [--direct] [--jonly] [--ckpt pieces.jsonl] [--split] [--bonf]
       --split (Session 14): Corr2 = (Q(R)^2 part) - (Q(U)^2 part), pieces kept apart (exact; same totals);
       --bonf: implies --split; one-sided certificate, Icorr j <= 1, Corr1 j <= 2, Q(R)^2 parts j <= 2, Q(U)^2 parts j <= 1;   (--direct: also compute I_T directly, test;
       --jonly: only the J corrections; then "I_T" in the output is the CAP-FREE I and "ratio" is k J_T / I)
"""
import sys, json, time
from math import comb, factorial
sys.path.insert(0, "code")
import mk_general as mg
from caps_exact import CapPieces
from flint import fmpq, fmpq_poly, fmpq_mat

Fq = lambda s: fmpq(*map(int, s.split("/"))) if "/" in str(s) else fmpq(int(s))


def fl(z):
    from fractions import Fraction
    return float(Fraction(int(z.p), int(z.q)))


def padd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def psub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def wt(b):
    return sum((j + 2) * x for j, x in enumerate(b))


def mult(B, e):
    m = 1
    for u, v in zip(B, e):
        m *= comb(u, v)
    return m


class BiPoly:
    """Bivariate polynomial in (R, x): dict (i, t) -> fmpq for R^i x^t."""
    def __init__(self, d=None):
        self.d = d or {}

    def add(self, o, c=1):
        for kk, v in o.d.items():
            self.d[kk] = self.d.get(kk, fmpq(0)) + c * v
        return self

    def mul(self, o):
        r = {}
        for (i, t), v in self.d.items():
            for (i2, t2), v2 in o.d.items():
                kk = (i + i2, t + t2)
                r[kk] = r.get(kk, fmpq(0)) + v * v2
        return BiPoly(r)

    def at_x(self, xval=None):
        """x = R if xval is None, else x = constant: univariate fmpq_poly in R."""
        c = {}
        for (i, t), v in self.d.items():
            if xval is None:
                c[i + t] = c.get(i + t, fmpq(0)) + v
            else:
                c[i] = c.get(i, fmpq(0)) + v * xval ** t
        n = max(c) + 1 if c else 0
        return fmpq_poly([c.get(i, fmpq(0)) for i in range(n)])


class Capped:
    def __init__(self, data):
        self.k = data["k"]
        self.L, self.tau, self.g = Fq(data["L"]), Fq(data["tau"]), Fq(data["g"])
        cp = data["caps"]
        self.caps = {str(kk): Fq(v) for kk, v in cp.items()}   # "m": C_m, and "m+": C_m' for all m' >= m
        self.basis = [(a, tuple(b)) for a, b in data["basis"]]
        self.coef = [Fq(x) for x in data["coeffs"]]
        self.D = max(a + wt(b) for a, b in self.basis)
        self.W = 2 * self.D
        self.blen = max(len(b) for _, b in self.basis)
        self.basis = [(a, b + (0,) * (self.blen - len(b))) for a, b in self.basis]
        mg.EVEN_ONLY = True
        self.cp0 = CapPieces(self.k, self.W, self.L, self.g)   # densities dA and moments E_n
        self.Ecache = {}
        self.MM = 1
        while self.MM * self.g < self.L:
            self.MM += 1
        self.MM += 1                                            # m, j range(0, MM) covers (m + j) g < L
        for m in range(1, self.MM + 1):
            assert self.C(m + 1) <= self.C(m) + self.g, "need C_{m+1} <= C_m + g"

    def C(self, m):
        if str(m) in self.caps:
            return self.caps[str(m)]
        best = None
        for kk, v in self.caps.items():
            if kk.endswith("+") and int(kk[:-1]) <= m and (best is None or int(kk[:-1]) > best[0]):
                best = (int(kk[:-1]), v)
        if best is None:
            raise ValueError("no cap for m = %d" % m)
        return best[1]

    # ---------- polynomial data ----------
    def prepare(self):
        R = fmpq_poly([0, 1])
        pb = {}
        for (a, b), c in zip(self.basis, self.coef):
            pb[b] = pb.get(b, fmpq_poly([0])) + c * R ** a
        self.pb = pb
        # P^2 = sum_B prod P^B H_I[B](R)
        HI = {}
        for b1, p1 in pb.items():
            for b2, p2 in pb.items():
                B = padd(b1, b2)
                HI[B] = HI.get(B, fmpq_poly([0])) + p1 * p2
        self.HI = HI
        # Q(u', x) = sum_{b'} prod P(u')^{b'} q_{b'}(R, x);  int_0^x t^w (R - t)^a dt
        from flint import fmpq_mpoly_ctx
        ctx = fmpq_mpoly_ctx.get(('R', 'x'), 'lex')
        self.ctx = ctx
        qd = {}
        for b, p in pb.items():
            coeffs = [p[i] for i in range(p.degree() + 1)]
            for e in mg.submultis(b):
                e = tuple(e)
                bp = psub(b, e)
                w = wt(e)
                mu = mult(b, e)
                bi = qd.setdefault(bp, {})
                for a, ca in enumerate(coeffs):
                    if ca == 0:
                        continue
                    for i in range(a + 1):
                        kk = (a - i, w + i + 1)
                        bi[kk] = bi.get(kk, fmpq(0)) + mu * ca * comb(a, i) * (-1) ** i * fmpq(1, w + i + 1)
        qb = {b: ctx.from_dict(d) for b, d in qd.items()}
        self.qb = qb
        R_, x_ = ctx.gens()
        g = self.g
        def uni(mp, xval):
            c = {}
            for (i, t), v in mp.to_dict().items():
                if xval is None:
                    c[i + t] = c.get(i + t, fmpq(0)) + v
                else:
                    c[i] = c.get(i, fmpq(0)) + v * xval ** t
            n = max(c) + 1 if c else 0
            return fmpq_poly([c.get(i, fmpq(0)) for i in range(n)])
        QR = {b: uni(q, None) for b, q in qb.items()}
        Qg = {b: uni(q, g) for b, q in qb.items()}
        HR, Hg, Hx = {}, {}, {}
        items = list(qb.items())
        for b1, q1 in items:
            for b2, q2 in items:
                B = padd(b1, b2)
                HR[B] = HR.get(B, fmpq_poly([0])) + QR[b1] * QR[b2]
                Hg[B] = Hg.get(B, fmpq_poly([0])) + Qg[b1] * Qg[b2]
                Hx[B] = Hx[B] + q1 * q2 if B in Hx else q1 * q2
        Hx = {B: BiPoly(dict(v.to_dict())) for B, v in Hx.items()}
        self.HR, self.Hg, self.Hx = HR, Hg, Hx

    # ---------- densities ----------
    def E(self, n, e):
        key = (n, e)
        if key not in self.Ecache:
            self.Ecache[key] = self.cp0.Mbig(n).E[self.padW(e)]
        return self.Ecache[key]

    def padW(self, e):
        L = self.W - 1
        return tuple(e) + (0,) * (L - len(e)) if len(e) < L else tuple(e[:L])

    def dA(self, m, e):
        """density of r_A as dict alpha -> coeff (m >= 1); m = 0: point mass {0: 1} if e = 0."""
        if m == 0:
            return {0: fmpq(1)} if not any(e) else {}
        return self.cp0.density(m, self.padW(e))

    def dRest(self, j, n1, e, cache):
        key = (j, n1, e)
        if key in cache:
            return cache[key]
        out = {}
        if j == 0:
            w = wt(e)
            g_ = n1 - 1 + w
            out[g_] = fmpq(self.E(n1, e), factorial(g_))
        else:
            for eB in mg.submultis(e):
                eB = tuple(eB)
                eY = psub(e, eB)
                mu = mult(e, eB)
                wY = wt(eY)
                gam = n1 - 1 + wY
                cy = fmpq(self.E(n1, eY), factorial(gam))
                for al, dv in self.dA(j, eB).items():
                    kk = al + gam + 1
                    out[kk] = out.get(kk, fmpq(0)) + mu * cy * dv * fmpq(factorial(al) * factorial(gam), factorial(al + gam + 1))
        cache[key] = out
        return out

    # ---------- region integrals ----------
    def T1(self, n, m, j, lo, hi, Lam, Hdict):
        """sum_B int_{lo<=r_A<=hi, rho<=Lam-r_A} shape-density * H_B(Lam - r_A - rho)  (one copy, no sign)."""
        n1 = n - m - j
        dcache, mucache = {}, {}
        rcache = {}

        def r1(al, N):
            kk = (al, N)
            if kk not in rcache:
                if m == 0:
                    rcache[kk] = Lam ** N if al == 0 else fmpq(0)
                else:
                    rcache[kk] = rint(lo, hi, Lam, al, N)
            return rcache[kk]

        def mu(eA, N):
            kk = (eA, N)
            if kk not in mucache:
                tot = fmpq(0)
                for al, dv in self.dA(m, eA).items():
                    tot += dv * r1(al, N)
                mucache[kk] = tot
            return mucache[kk]

        total = fmpq(0)
        for B, H in Hdict.items():
            if H == 0:
                continue
            Ht = fmpq_poly([H[p] * factorial(p) for p in range(H.degree() + 1)])
            for eA in (mg.submultis(B) if m > 0 else [tuple(0 for _ in B)]):
                eA = tuple(eA)
                eR = psub(B, eA)
                dr = self.dRest(j, n1, eR, dcache)
                if not dr:
                    continue
                bmax = max(dr)
                Dt = fmpq_poly([dr.get(b, fmpq(0)) * factorial(b) for b in range(bmax + 1)])
                prod = Dt * Ht           # coefficient of z^{N-1} times 1/N! gives the weight of (Lam - r_A)^N
                s = fmpq(0)
                for Nm1 in range(prod.degree() + 1):
                    c = prod[Nm1]
                    if c == 0:
                        continue
                    s += c / factorial(Nm1 + 1) * mu(eA, Nm1 + 1)
                total += mult(B, eA) * s
        return total

    def T2(self, n, m, j, a, rc, cprime, Hbi):
        """sum_B int_{0<=r_A<=a, 0<=rho<=rc} shape-density * h_B(R, x), x = c' - r_A, R = x + (rc - rho)."""
        n1 = n - m - j
        dcache, nucache, kapcache = {}, {}, {}
        rcache = {}

        def nu(eA, t):
            kk = (eA, t)
            if kk not in nucache:
                if m == 0:
                    nucache[kk] = cprime ** t
                else:
                    tot = fmpq(0)
                    for al, dv in self.dA(m, eA).items():
                        k2 = (al, t)
                        if k2 not in rcache:
                            rcache[k2] = rint(fmpq(0), a, cprime, al, t)
                        tot += dv * rcache[k2]
                    nucache[kk] = tot
            return nucache[kk]

        def kap(eR, i):
            kk = (eR, i)
            if kk not in kapcache:
                tot = fmpq(0)
                for b, dv in self.dRest(j, n1, eR, dcache).items():
                    tot += dv * fmpq(factorial(b) * factorial(i), factorial(b + i + 1)) * rc ** (b + i + 1)
                kapcache[kk] = tot
            return kapcache[kk]

        total = fmpq(0)
        for B, h in Hbi.items():
            # eta[i, t]: h(x + wbar, x) = sum eta[i,t] wbar^i x^t
            eta = {}
            for (p, q), v in h.d.items():
                if v == 0:
                    continue
                for i in range(p + 1):
                    kk = (i, p - i + q)
                    eta[kk] = eta.get(kk, fmpq(0)) + v * comb(p, i)
            eta = {kk: v for kk, v in eta.items() if v != 0}
            if not eta:
                continue
            for eA in (mg.submultis(B) if m > 0 else [tuple(0 for _ in B)]):
                eA = tuple(eA)
                eR = psub(B, eA)
                s = fmpq(0)
                for (i, t), v in eta.items():
                    s += v * kap(eR, i) * nu(eA, t)
                total += mult(B, eA) * s
        return total

    # ---------- the functionals ----------
    def capfree(self):
        k, L, tau = self.k, self.L, self.tau
        I = self.T1(k, 0, 0, None, None, L, self.HI)
        # J: R = (tau - |u'|) + (L - tau)
        d = L - tau
        HRs = {B: H(fmpq_poly([d, 1])) for B, H in self.HR.items()}
        J = self.T1(k - 1, 0, 0, None, None, tau, HRs)
        return I, J

    def ranges(self, n, Lam_tot):
        """(m, j) with m + j forced coordinates > g possible below total Lam_tot."""
        g = self.g
        out = []
        for m in range(0, 13):
            for j in range(0, self.MM):
                if (m + j) * g < Lam_tot:
                    out.append((m, j))
        return out

    def build_H(self):
        g, d = self.g, self.L - self.tau
        self.HRs = {B: H(fmpq_poly([d, 1])) for B, H in self.HR.items()}
        Hb = {}
        for B in set(self.HR) | set(self.Hg):
            Hb[B] = (self.HR.get(B, fmpq_poly([0])) - self.Hg.get(B, fmpq_poly([0])))(fmpq_poly([g, 1]))
        self.Hb = Hb
        Hc = {}
        for B in set(self.HR) | set(self.Hx):
            h = BiPoly()
            HRB = self.HR.get(B)
            if HRB is not None:
                for i in range(HRB.degree() + 1):
                    if HRB[i] != 0:
                        h.d[(i, 0)] = h.d.get((i, 0), fmpq(0)) + HRB[i]
            if B in self.Hx:
                h.add(self.Hx[B], -1)
            Hc[B] = h
        self.Hc = Hc
        if getattr(self, "split", False):          # --split (Session 14): keep Q(R)^2 and Q(U)^2 apart (each >= 0)
            self.HbR = {B: H(fmpq_poly([g, 1])) for B, H in self.HR.items()}
            self.HbU = {B: H(fmpq_poly([g, 1])) for B, H in self.Hg.items()}
            HcR = {}
            for B, HRB in self.HR.items():
                h = BiPoly()
                for i in range(HRB.degree() + 1):
                    if HRB[i] != 0:
                        h.d[(i, 0)] = HRB[i]
                HcR[B] = h
            self.HcR, self.HcU = HcR, dict(self.Hx)

    def tasks(self):
        """All (kind, m, j, args) pieces; each value enters with weight (-1)^j C(n, m) C(n - m, j)."""
        k, L, tau, g = self.k, self.L, self.tau, self.g
        out = []
        for m in (range(1, self.MM) if not getattr(self, "jonly", False) else []):   # I correction: int_V P^2, n = k
            alo = max(self.C(m) - m * g, fmpq(0))
            for j in range(0, self.MM):
                Lam = L - (m + j) * g
                if Lam > alo and m + j <= k:
                    out.append(("Icorr", k, m, j, (alo, Lam, Lam)))
        n = k - 1
        assert L - g <= tau, "Corr2 pieces assume L - g <= tau (|u'| <= tau automatic where R > g)"
        for m in range(1, self.MM):                       # Corr1: u' not admissible, |u'| <= tau
            alo = max(self.C(m) - m * g, fmpq(0))
            for j in range(0, self.MM):
                T0 = tau - (m + j) * g
                if T0 > alo and m + j <= n:
                    out.append(("Corr1", n, m, j, (alo, T0, T0)))
        for m in range(1, self.MM):                  # Corr2 (b): r_A >= r*, R > g
            amax = self.C(m) - m * g
            rstar = self.C(m + 1) - (m + 1) * g
            lo = rstar if rstar > 0 else fmpq(0)
            for j in range(0, self.MM):
                Lam = L - (m + j + 1) * g
                hi = amax if amax < Lam else Lam
                if hi > lo and m + j <= n:
                    out.append(("Corr2b", n, m, j, (lo, hi, Lam)))
        for m in range(0, self.MM):                  # Corr2 (c): r_A < r*, rho < rc
            amax = self.C(m) - m * g if m > 0 else fmpq(0)
            rstar = self.C(m + 1) - (m + 1) * g
            a = rstar if rstar < amax else amax
            if (m > 0 and a <= 0) or rstar <= 0:
                continue
            cprime = self.C(m + 1) - m * g
            for j in range(0, self.MM):
                rc = L - self.C(m + 1) - j * g
                if rc > 0 and m + j <= n:
                    out.append(("Corr2c", n, m, j, (a, rc, cprime)))
        for t in out:
            assert t[1] - t[2] - t[3] >= 1, "n' = 0 piece not supported"
        if getattr(self, "split", False):         # Corr2b = Corr2bR - Corr2bU, Corr2c = Corr2cR - Corr2cU
            o2 = []
            for t in out:
                if t[0] in ("Corr2b", "Corr2c"):
                    o2.append((t[0] + "R",) + t[1:])
                    o2.append((t[0] + "U",) + t[1:])
                else:
                    o2.append(t)
            out = o2
        if getattr(self, "bonf", False):          # Bonferroni truncation (paper Prop. bonf and its split form)
            jmax = {"Icorr": 1, "Corr1": 2, "Corr2bR": 2, "Corr2cR": 2, "Corr2bU": 1, "Corr2cU": 1}
            out = [t for t in out if t[3] <= jmax[t[0]]]
        return out

    def run_task(self, t):
        kind, n, m, j, args = t
        t0 = time.time()
        if kind == "Icorr":
            v = self.T1(n, m, j, *args, self.HI)
        elif kind == "Corr1":
            v = self.T1(n, m, j, *args, self.HRs)
        elif kind == "Corr2b":
            v = self.T1(n, m, j, *args, self.Hb)
        elif kind == "Corr2c":
            v = self.T2(n, m, j, *args, self.Hc)
        elif kind == "Corr2bR":
            v = self.T1(n, m, j, *args, self.HbR)
        elif kind == "Corr2bU":
            v = self.T1(n, m, j, *args, self.HbU)
        elif kind == "Corr2cR":
            v = self.T2(n, m, j, *args, self.HcR)
        else:
            assert kind == "Corr2cU"
            v = self.T2(n, m, j, *args, self.HcU)
        v = (-1) ** j * comb(n, m) * comb(n - m, j) * v
        return kind, m, j, v, time.time() - t0

    def corrections(self, log=print, procs=1):
        res = {kk: fmpq(0) for kk in ("Icorr", "Corr1", "Corr2b", "Corr2c", "Corr2bR", "Corr2bU", "Corr2cR", "Corr2cU")}
        self.build_H()
        ts = self.tasks()
        ck = getattr(self, "ckpt", None)          # --ckpt file: exact value of every finished piece (JSON lines)
        if ck:
            import os
            done = {}
            if os.path.exists(ck):
                for line in open(ck):
                    if line.strip():
                        r = json.loads(line)
                        done[(r["kind"], r["m"], r["j"])] = r["v"]
            for t in ts:
                key = (t[0], t[2], t[3])
                if key in done:
                    res[t[0]] += Fq(done[key])
            log("checkpoint %s: %d of %d pieces already done" % (ck, sum((t[0], t[2], t[3]) in done for t in ts), len(ts)))
            ts = [t for t in ts if (t[0], t[2], t[3]) not in done]
            ckf = open(ck, "a")
        ts.sort(key=lambda t: -(t[3] * 10 + (1 if t[2] else 0)))     # expensive (large j) first
        if procs == 1:
            it = map(_run, ts)
        else:
            import multiprocessing as mp
            pool = mp.get_context("fork").Pool(procs)
            it = pool.imap_unordered(_run, ts)
        for kind, m, j, v, sec in it:
            if isinstance(v, str):
                v = Fq(v)
            res[kind] += v
            if ck:
                ckf.write(json.dumps(dict(kind=kind, m=m, j=j, v=str(v), sec=round(sec))) + "\n"); ckf.flush()
            log("%s m=%d j=%d: %+.6e (%.0f s)" % (kind, m, j, fl(v), sec))
        return res

    def direct_I(self, log=print):
        """I_T = sum_m C(k,m) int_{exactly m large, s <= C_m} P^2 (second code path inside this file; tests)."""
        k, L, g = self.k, self.L, self.g
        tot = fmpq(0)
        for m in range(0, self.MM):
            amax = self.C(m) - m * g if m > 0 else None
            for j in range(0, self.MM):
                Lam = L - (m + j) * g
                if Lam <= 0 or m + j > k:
                    continue
                if m == 0:
                    v = self.T1(k, 0, j, None, None, Lam, self.HI)
                else:
                    if amax <= 0:
                        continue
                    hi = amax if amax < Lam else Lam
                    v = self.T1(k, m, j, fmpq(0), hi, Lam, self.HI)
                tot += (-1) ** j * comb(k, m) * comb(k - m, j) * v
        return tot


_G = {}


def _run(t):
    kind, m, j, v, sec = _G["c"].run_task(t)
    return kind, m, j, str(v), sec


def rint(lo, hi, Lam, al, N):
    """int_lo^hi r^al (Lam - r)^N dr, exact (expansion in h = Lam - r)."""
    def F(x):   # int_x^Lam r^al (Lam - r)^N dr = sum_i C(al,i) Lam^(al-i) (-1)^i h^(N+i+1)/(N+i+1), h = Lam - x
        h = Lam - x
        tot = fmpq(0)
        for i in range(al + 1):
            tot += comb(al, i) * Lam ** (al - i) * (-1) ** i * h ** (N + i + 1) / (N + i + 1)
        return tot
    return F(lo) - F(hi)


def main():
    data = json.load(open(sys.argv[1]))
    t0 = time.time()
    c = Capped(data)
    c.prepare()
    print("prepared %d keys (I), %d keys (J) in %.0f s" % (len(c.HI), len(c.HR), time.time() - t0), flush=True)
    log = lambda s: print(s, flush=True)
    I, J = c.capfree()
    k = c.k
    log("cap-free: I = %.10e, J = %.10e, k J / I = %.10f" % (fl(I), fl(J), fl(k * J / I)))
    _G["c"] = c
    c.ckpt = sys.argv[sys.argv.index("--ckpt") + 1] if "--ckpt" in sys.argv else None
    c.jonly = "--jonly" in sys.argv     # skip the I correction (I_T then not computed; ratio uses cap-free I)
    procs = int(sys.argv[sys.argv.index("--procs") + 1]) if "--procs" in sys.argv else 1
    c.split = "--split" in sys.argv or "--bonf" in sys.argv
    c.bonf = "--bonf" in sys.argv       # one-sided: J_T >= J - (truncated sums), I_T <= I - (truncated sum)
    res = c.corrections(log, procs)
    if c.split:
        res["Corr2b"] = res["Corr2bR"] - res["Corr2bU"]
        res["Corr2c"] = res["Corr2cR"] - res["Corr2cU"]
    IT = I - res["Icorr"] if not c.jonly else I
    JT = J - res["Corr1"] - res["Corr2b"] - res["Corr2c"]
    ratio = k * JT / IT
    out = dict(k=k, I=str(I), J=str(J), Icorr=str(res["Icorr"]), Corr1=str(res["Corr1"]), Corr2b=str(res["Corr2b"]),
               Corr2c=str(res["Corr2c"]), I_T=str(IT), J_T=str(JT), ratio=str(ratio), ratio_float=fl(ratio),
               capfree_ratio_float=fl(k * J / I), gt4=bool(ratio > 4), source=sys.argv[1], seconds=round(time.time() - t0))
    if c.split:
        out.update({kk: str(res[kk]) for kk in ("Corr2bR", "Corr2bU", "Corr2cR", "Corr2cU")})
    if c.bonf:
        out["onesided"] = True
        out["note"] = ("BONFERRONI ONE-SIDED: J_T here is a LOWER bound and I_T an UPPER bound for the true values "
                       "(Icorr j<=1, Corr1 j<=2, Q(R)^2 parts j<=2, Q(U)^2 parts j<=1); ratio is a lower bound")
    log(json.dumps({kk: v for kk, v in out.items() if kk not in ("I", "J", "Icorr", "Corr1", "Corr2b", "Corr2c", "I_T", "J_T", "ratio")}))
    log("relative: Icorr/I = %.4e, Corr1/J = %.4e, Corr2b/J = %.4e, Corr2c/J = %.4e" % (
        fl(res["Icorr"] / I), fl(res["Corr1"] / J), fl(res["Corr2b"] / J), fl(res["Corr2c"] / J)))
    if "--direct" in sys.argv:
        Id = c.direct_I(log)
        log("direct I_T = %.12e, corrected I_T = %.12e, equal: %s" % (fl(Id), fl(IT), Id == IT))
        out["direct_I_equal"] = bool(Id == IT)
    if "--out" in sys.argv:
        json.dump(out, open(sys.argv[sys.argv.index("--out") + 1], "w"), indent=1)


if __name__ == "__main__":
    main()
