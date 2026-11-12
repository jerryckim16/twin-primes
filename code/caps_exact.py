#!/usr/bin/env python3
"""Exact integrals of symmetric polynomials over the cap-violation pieces of Stadlmann's support.

For m >= 1, g >= 0, c and the simplex {t >= 0, sum t <= L} in k variables, let
  R_m(g, c) = {t : t_1, ..., t_m > g, t_1 + ... + t_m >= c}.
For the basis integrands (L - P1)^A prod_j P_j^{B_j} (B on even j) we compute
  int_{R_m(g,c)} (L - P1)^A prod_j P_j^{B_j}  exactly, as follows.
x = (t_1..t_m) = g + z, y = the other k - m coordinates, r = |z|, L' = L - m g.
  * y-integral: (L - |x| - |y|)^A prod P_j(y)^{B_j - e_j} over the simplex of size L - |x| = L' - r gives
    S_{k-m}(A, B - e) (L' - r)^{k - m + A + w(B - e)}   (Lemma 3 after scaling);
  * P_j(x) = sum_l C(j, l) g^{j-l} P_l(z), with P_0(z) = m and P_1(z) = r;
  * z-integral at fixed r: int_{|z| = r} prod_l P_l(z)^{f_l} = r^{m-1+w(f)} E_m[f] / (m-1+w(f))!  (all parts l >= 2);
  * r-integral: int_{max(c - m g, 0)}^{L'} r^alpha (L' - r)^N dr, exactly.
With g = 0 and c = 0 the piece is the whole simplex: self-test against Lemma 3.
"""
import sys
from math import comb, factorial
sys.path.insert(0, "code")
import mk_general as mg
from flint import fmpq


class CapPieces:
    def __init__(self, k, W, L, g):
        self.k, self.W, self.L, self.g = k, W, L, g
        self.mom_small, self.mom_big = {}, {}
        self.dens, self.rc, self.Sc = {}, {}, {}

    def Mbig(self, n):
        if n not in self.mom_big:
            old = mg.EVEN_ONLY; mg.EVEN_ONLY = True
            self.mom_big[n] = mg.Moments(n, self.W)
            mg.EVEN_ONLY = old
        return self.mom_big[n]

    def Msmall(self, m):
        if m not in self.mom_small:
            old = mg.EVEN_ONLY; mg.EVEN_ONLY = False
            self.mom_small[m] = mg.Moments(m, self.W)
            mg.EVEN_ONLY = old
        return self.mom_small[m]

    def S(self, n, A, b):
        key = (n, A, b)
        if key not in self.Sc:
            self.Sc[key] = fmpq(factorial(A) * self.Mbig(n).E[b], factorial(n + A + mg.w(b)))
        return self.Sc[key]

    def density(self, m, e):
        """Coefficients d_alpha with int_{|z|=r} prod_j P_j(g+z)^{e_j} = sum_alpha d_alpha r^alpha."""
        key = (m, e)
        if key in self.dens:
            return self.dens[key]
        W, g = self.W, self.g
        zero = (0,) * (W - 1)
        poly = {(zero, 0): fmpq(1)}          # (f over l = 2..W, power of r) -> coefficient
        for jj, cnt in enumerate(e):
            j = jj + 2
            if not cnt:
                continue
            lin = []
            for l in range(j + 1):
                cf = comb(j, l) * g ** (j - l)
                if l == 0:
                    lin.append((None, 0, cf * m))
                elif l == 1:
                    lin.append((None, 1, cf))
                else:
                    lin.append((l, 0, cf))
            for _ in range(cnt):
                new = {}
                for (f, rho), c0 in poly.items():
                    for l, dr, cf in lin:
                        if cf == 0:
                            continue
                        if l is None:
                            nk = (f, rho + dr)
                        else:
                            fl_ = list(f); fl_[l - 2] += 1; nk = (tuple(fl_), rho)
                        new[nk] = new.get(nk, fmpq(0)) + c0 * cf
                poly = new
        M = self.Msmall(m)
        d = {}
        for (f, rho), c0 in poly.items():
            wf = mg.w(f)
            Ef = M.E[f]
            if not Ef:
                continue
            a = m - 1 + wf + rho
            d[a] = d.get(a, fmpq(0)) + c0 * fmpq(Ef, factorial(m - 1 + wf))
        self.dens[key] = d
        return d

    def rint(self, lo, Lp, alpha, N):
        key = (lo, Lp, alpha, N)
        if key not in self.rc:
            h = Lp - lo
            tot = fmpq(0)
            for i in range(alpha + 1):
                tot += comb(alpha, i) * Lp ** (alpha - i) * (-1) ** i * h ** (N + i + 1) / (N + i + 1)
            self.rc[key] = tot
        return self.rc[key]

    def piece(self, m, c, A, B):
        k, Lp = self.k, self.L - m * self.g
        lo = c - m * self.g
        if lo < 0:
            lo = fmpq(0)
        if lo >= Lp:
            return fmpq(0)
        tot = fmpq(0)
        for e in mg.submultis(B):
            e = tuple(e)
            mult = 1
            for u, v in zip(B, e):
                mult *= comb(u, v)
            rest = tuple(u - v for u, v in zip(B, e))
            N = k - m + A + mg.w(rest)
            Sv = self.S(k - m, A, rest)
            for alpha, dv in self.density(m, e).items():
                tot += mult * Sv * dv * self.rint(lo, Lp, alpha, N)
        return tot


def selftest():
    """g = 0, c = 0: every m gives the whole-simplex integral (Lemma 3); and a k = 3 sympy check with g > 0."""
    import sympy as sp
    mg.EVEN_ONLY = True
    k, D = 6, 4
    L = fmpq(26, 25)
    cp = CapPieces(k, 2 * D, L, fmpq(0))
    Mk = mg.Moments(k, 2 * D)
    for A, B in [(0, (0,) * 7), (3, (1,) + (0,) * 6), (1, (2,) + (0,) * 6), (0, (0, 0, 1) + (0,) * 4)]:
        full = fmpq(factorial(A) * Mk.E[B], factorial(k + A + mg.w(B))) * L ** (k + A + mg.w(B))
        for m in (1, 2, 3):
            assert cp.piece(m, fmpq(0), A, B) == full, (m, A, B)
    # sympy, k = 3, m = 2, g = 1/10, c = 1/2, L = 1: integrand (L - P1)^A P2^b
    t1, t2, t3 = sp.symbols("t1 t2 t3", nonnegative=True)
    Ls, gs, cs = sp.Integer(1), sp.Rational(1, 10), sp.Rational(1, 2)
    cp = CapPieces(3, 4, fmpq(1), fmpq(1, 10))
    for A, b in [(0, 0), (1, 0), (0, 1), (2, 1), (1, 2)]:
        f = (Ls - t1 - t2 - t3) ** A * (t1 ** 2 + t2 ** 2 + t3 ** 2) ** b
        inner = sp.integrate(f, (t3, 0, Ls - t1 - t2))
        # region t1 > g, t2 > g, t1 + t2 >= c, t1 + t2 <= L
        part1 = sp.integrate(sp.integrate(inner, (t2, cs - t1, Ls - t1)), (t1, gs, cs - gs))
        part2 = sp.integrate(sp.integrate(inner, (t2, gs, Ls - t1)), (t1, cs - gs, Ls - gs))
        ref = sp.nsimplify(part1 + part2)
        B = (b, 0, 0)
        got = cp.piece(2, fmpq(1, 2), A, B)
        assert sp.Rational(int(got.p), int(got.q)) == ref, (A, b, got, ref)
        # m = 1: t1 > 3/5
        ref1 = sp.integrate(sp.integrate(inner, (t2, 0, Ls - t1)), (t1, sp.Rational(3, 5), Ls))
        got1 = cp.piece(1, fmpq(3, 5), A, B)
        assert sp.Rational(int(got1.p), int(got1.q)) == ref1, (A, b, got1, ref1)
    print("caps_exact self-test passed (Lemma 3 identity for m = 1..3; sympy for k = 3, m = 1, 2, g = 1/10)")


if __name__ == "__main__":
    selftest()
