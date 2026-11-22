#!/usr/bin/python3
"""Rung 3 of the sifting-dimension ladder at level 1/2: sifting to z = x^{1/u}, u in (2, 3], plus a switching bound.

Route card: notes/parity-attempts/2026-11-22-switching-rung3.md   (Session 45; the "first unresolved implication" of
the Session 44 card notes/parity-attempts/2026-11-22-level-ladder.md)
Run: /usr/bin/python3 -I code/parity/switch_ladder.py [X]     (default X = 1e8; ~2 min, ~1.5 GB)

Setting (Session 43/44 cards): q prime, H < (Z/q)^* of index m, "good" primes l with l mod q in H, "bad" primes the
others (l != q; 2 never divides p + 2). A_H = {p + 2 : p <= x prime, p + 2 mod q in H}. Sifting A_H by the bad primes
below z is a sieve of dimension kappa = 1 - 1/m. For z = x^{1/u}, 2 < u <= 3, a survivor has at most two bad prime
factors (counted with multiplicity), never exactly one (the congruence), so

    S(A_H, z) = T_H(x) + W(x),   W = #{p : p + 2 = g b1 b2, b1 < b2 bad, b_i >= z, b1 b2 in H, g all good}

(b^2 g with b >= z is O(x/z) in total and is ignored; for index m = 3 it cannot occur at all, since b^2 is not in H).

(i)   Lower bound (beta-sieve, level x^{1/2} from Bombieri-Vinogradov): S(A_H, z) >= |A_H| V(z) (f_kappa(u/2) - o(1)),
      f_kappa by the Session 43/44 solver (floating point, three step sizes).
(ii)  The main terms in units of |A_H| V(z), from the Selberg-Delange asymptotic for all-good integers
      (#{n <= y all good, n = h mod q} ~ (m / phi(q)) * c * y (log y)^{-kappa} for h in H) and Mertens:
        Z(u) = m e^{gamma kappa} / Gamma(1 - kappa) * u^{-kappa}                       (expected T_H)
        Z(u) R(u),  R(u) = (kappa / (2m)) * int int_{t1, t2 >= 1/u, t1 + t2 <= 1} (1 - t1 - t2)^{-kappa} dt1 dt2 / (t1 t2)
                                                                                      (expected W)
      HEURISTIC IDENTIFICATION of constants (Kubilius model: local factors of "n - 2 prime" agree on the two sets);
      checked against data in part (iii), not proved here.
(iii) Switching (also with three bad primes for u > 3, c_3 = probability their product lies in H): an upper-bound linear sieve for the primes p = n - 2, n in B = {g b1 b2}, at level x^{1/2}
      (Bombieri-Vinogradov for the convolution b1 * (b2 g), b1 a prime in [x^{1/u}, x^{1/2}]) gives
      W <= (4 + o(1)) * (expected W). Success test: margin(u) = f_kappa(u/2) - 4 Z(u) (R2 + R3)(u) > 0. Consistency test: m = 2 (kappa = 1/2, Iwaniec).
(v)   C_need(m) = max over u of the switching constant that would suffice, m = 2..5 (computed before (iv)).
(iv)  Finite-X data for q = 7, H = {1, 6} (m = 3) at z = X^{1/u}, u = 3, 2.5, 3.5: S, T_H, W in units of |A_H| V(z),
      against Z(u) and Z(u) R(u). Finite-X data only; proves nothing.
"""
import sys, time, math
import numpy as np
from scipy import integrate
from scipy.special import gamma as Gamma

t0 = time.time()
GAMMA = 0.5772156649015329


# ---------- (i) the beta-sieve functions (same solver as code/parity/level_ladder.py) ----------
def solve(kappa, beta, smax, h):
    n = int(round(smax / h))
    s = np.arange(n + 1) * h
    F = np.zeros(n + 1)
    f = np.zeros(n + 1)
    F[1:] = s[1:] ** (-kappa)
    ib, ib1, i1 = int(round(beta / h)), int(round((beta + 1) / h)), int(round(1 / h))
    G = 0.0
    Hh = 1.0
    sk1 = kappa * np.concatenate(([0.0], s[1:] ** (kappa - 1)))
    skk = np.concatenate(([1.0], s[1:] ** kappa))
    for i in range(ib + 1, n + 1):
        G += h * (sk1[i - 1] * F[i - 1 - i1] + sk1[i] * F[i - i1]) / 2
        f[i] = G / skk[i]
        if i > ib1:
            Hh += h * (sk1[i - 1] * f[i - 1 - i1] + sk1[i] * f[i - i1]) / 2
            F[i] = Hh / skk[i]
    return s, F, f


def cest(kappa, beta, h, smax=40.0):
    s, F, f = solve(kappa, beta, smax, h)
    def g(S):
        i = int(round(S / h))
        return (F[i] - f[i]) * S ** (2 * kappa)
    return (smax * g(smax) - smax / 2 * g(smax / 2)) / (smax / 2), s, F, f


def beta_kappa(kappa, h, lo=1.0 + 1e-9, hi=2.6):
    clo = cest(kappa, lo, h)[0]
    assert (cest(kappa, hi, h)[0] > 0) != (clo > 0)
    for _ in range(36):
        mid = (lo + hi) / 2
        c = cest(kappa, mid, h)[0]
        if (c > 0) == (clo > 0):
            lo, clo = mid, c
        else:
            hi = mid
    b = (lo + hi) / 2
    _, s, F, f = cest(kappa, b, h)
    A = 1.0 / F[-1]
    return b, s, A * F, A * f


# ---------- (ii) main terms ----------
def Z(u, m):
    k = 1 - 1 / m
    return m * math.exp(GAMMA * k) / Gamma(1 - k) * u ** (-k)


def R(u, m):
    k = 1 - 1 / m
    a = 1 / u
    # inner: int_{a}^{1-t1} (1-t1-t2)^{-k} dt2/t2 ; substitute w = 1-t1-t2 = v^{1/(1-k)}, w^{-k} dw = dv/(1-k)
    def inner(t1):
        W = 1 - t1 - a
        if W <= 0:
            return 0.0
        V = W ** (1 - k)
        val, _ = integrate.quad(lambda v: 1.0 / ((1 - k) * (1 - t1 - v ** (1 / (1 - k)))), 0, V, limit=200)
        return val
    val, _ = integrate.quad(lambda t1: inner(t1) / t1, a, 1 - a, limit=200)
    return k / (2 * m) * val


def R_check(u, m, N=4000):
    """Independent crude check of R by a midpoint rule in (t1, w) with the w^{-k} singularity integrated exactly per cell."""
    k = 1 - 1 / m
    a = 1 / u
    tot = 0.0
    h1 = (1 - 2 * a) / N
    for i in range(N):
        t1 = a + (i + 0.5) * h1
        W = 1 - t1 - a
        if W <= 0:
            continue
        M = 200
        hw = W / M
        for j in range(M):
            w0, w1 = j * hw, (j + 1) * hw
            wm = (w0 + w1) / 2
            tot += h1 / t1 * (w1 ** (1 - k) - w0 ** (1 - k)) / (1 - k) / (1 - t1 - wm)
    return k / (2 * m) * tot


def cj(j, m):
    """Probability that a product of j bad primes (independent, uniform over the m-1 bad cosets of the cyclic
    quotient (Z/q)^*/H of order m) lies in H: ((m-1)^j + (-1)^j (m-1)) / (m (m-1)^j)."""
    return ((m - 1) ** j + (-1) ** j * (m - 1)) / (m * (m - 1) ** j)


def R3(u, m):
    """kappa^3/3! * c_3 * int_{t_i >= 1/u, t1+t2+t3 <= 1} (1 - sum t)^{-kappa} prod dt_i / t_i (zero for u <= 3)."""
    k = 1 - 1 / m
    a = 1 / u
    if 3 * a >= 1:
        return 0.0
    def inner(t1, t2):
        W = 1 - t1 - t2 - a
        if W <= 0:
            return 0.0
        V = W ** (1 - k)
        return integrate.quad(lambda v: 1.0 / ((1 - k) * (1 - t1 - t2 - v ** (1 / (1 - k)))), 0, V, limit=100)[0]
    def mid(t1):
        hi = 1 - t1 - a
        if hi <= a:
            return 0.0
        return integrate.quad(lambda t2: inner(t1, t2) / t2, a, hi, limit=100, epsabs=1e-9)[0]
    val = integrate.quad(lambda t1: mid(t1) / t1, a, 1 - 2 * a, limit=100, epsabs=1e-9)[0]
    return k ** 3 / 6 * cj(3, m) * val


print("(i)-(iii) margin(u) = f_kappa(u/2) - 4 Z(u) (R2(u) + R3(u)) at level 1/2 (BV), z = x^(1/u)")
print("  (R2 = R of the docstring = kappa^2/2 * c_2 * integral, c_2 = 1/(m-1); R3 = three bad primes, only for u > 3)")
for m in (2, 3, 4):
    k = 1 - 1 / m
    assert abs(cj(2, m) * k * k / 2 - k / (2 * m)) < 1e-15
    res = {}
    for h in (1e-3, 5e-4, 2.5e-4):
        if m == 2:   # beta_{1/2} = 1 exactly (Iwaniec's half-dimensional sieve); no bisection
            _, s_, F_, f_ = cest(k, 1.0, h)
            b, s, f = 1.0, s_, f_ / F_[-1]
        else:
            b, s, F, f = beta_kappa(k, h)
        res[h] = (b, s, f)
    print(f"  m = {m}, kappa = {k:.5f}: beta_kappa = " + " ".join(f"{res[h][0]:.5f}" for h in res))
    us = (2.2, 2.5, 2.8, 3.0, 3.25, 3.5, 3.75, 4.0) if m != 4 else (2.8, 3.0, 3.5, 4.0)
    for u in us:
        fs = [float(np.interp(u / 2, res[h][1], res[h][2])) for h in res]
        z, r2, r3 = Z(u, m), R(u, m), R3(u, m)
        zr = z * (r2 + r3)
        need = fs[-1] / zr if zr > 0 else float("inf")
        print(f"    u = {u:.2f}: s = {u/2:.3f}, f = " + " ".join(f"{x:.5f}" for x in fs)
              + f" | Z = {z:.5f}, R2 = {r2:.5f}, R3 = {r3:.5f}, 4 Z (R2+R3) = {4*zr:.5f}, margin = {fs[-1] - 4*zr:+.5f}"
              + f" | switching constant needed < {need:.3f}")
    rc = R_check(3.0, m, N=2000)
    print(f"    R2(3) cross-check (midpoint rule, singularity integrated per cell): {rc:.5f} vs quad {R(3.0, m):.5f}")
print(f"  [{time.time()-t0:.1f}s]")

# ---------- (v) the best u for each rung: max over u of the switching constant that would be needed ----------
print("(v) C_need(m) = max over u in [2.05, 4] (step 0.05) of f_kappa(u/2) / (Z(u) (R2 + R3)(u)), h = 2.5e-4")
print("    (an upper-bound sieve for primes cannot beat 2 times the expected count: Selberg's parity example;")
print("     at level theta for the switched set the linear sieve gives 2/theta: 4 at BV, 3.5 at 4/7, 3.43 at 7/12)")
for m in (2, 3, 4, 5):
    k = 1 - 1 / m
    if m == 2:
        _, s_, F_, f_ = cest(k, 1.0, 2.5e-4)
        sg, fg = s_, f_ / F_[-1]
    else:
        _, sg, _, fg = beta_kappa(k, 2.5e-4)
    best = (0.0, None)
    for i in range(41, 81):
        u = i * 0.05
        fv = float(np.interp(u / 2, sg, fg))
        zr = Z(u, m) * (R(u, m) + R3(u, m))
        c = fv / zr
        if c > best[0]:
            best = (c, u)
    print(f"  m = {m} (kappa = {k:.4f}): C_need = {best[0]:.3f} at u = {best[1]:.2f}; theta needed for the switched set "
          f"(2/theta < C_need): theta > {2/best[0] if best[0] > 0 else float('inf'):.3f}")
print(f"  [{time.time()-t0:.1f}s]")

# ---------- (iv) data ----------
X = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10 ** 8
q, Hset = 7, {1, 6}
m = 3
N = X + 3
spf = np.zeros(N + 1, dtype=np.int32)
lim = int(N ** 0.5) + 1
sv = np.ones(N + 1, dtype=bool)
sv[:2] = False
for p in range(2, lim + 1):
    if sv[p]:
        sv[p * p::p] = False
primes_all = np.nonzero(sv)[0]
# smallest prime factor via descending assignment over primes <= sqrt(N)
spf[:] = 0
for p in primes_all[primes_all <= lim][::-1]:
    spf[p::p] = p
idx = np.nonzero(spf == 0)[0]
spf[idx] = idx                                   # remaining n >= 2 are primes (and 0, 1 are junk)
print(f"(iv) data at X = {X:.0e}: q = 7, H = {{1, 6}} (m = 3) [tables {time.time()-t0:.1f}s]")
P = primes_all[(primes_all >= 3) & (primes_all <= X)]
nA = P + 2
nA = nA[np.isin(nA % q, list(Hset))]
Asize = len(nA)
good = lambda l: (l % q) in Hset
for u in (3.0, 2.5, 3.5):
    z = (X + 2) ** (1 / u)
    V = 1.0
    for l in primes_all[(primes_all >= 3) & (primes_all < z)]:
        if l != q and not good(int(l)):
            V *= 1 - 1 / (l - 1)
    S = T = Wc = W3 = other = 0
    for n in nA.tolist():
        bad = []
        x = n
        while x > 1:
            l = int(spf[x])
            x //= l
            if l % q not in Hset:
                bad.append(l)
        if any(b < z for b in bad):
            continue
        S += 1
        if not bad:
            T += 1
        elif len(bad) == 2 and bad[0] != bad[1]:
            Wc += 1
        elif len(bad) == 3 and len(set(bad)) == 3:
            W3 += 1
        else:
            other += 1
    U = Asize * V
    zz, rr, rr3 = Z(u, m), R(u, m), R3(u, m)
    print(f"  u = {u}: |A_H| = {Asize}, V(z) = {V:.6f}; S = {S}, T_H = {T}, W = {Wc}, W3 = {W3}, other = {other}")
    if W3:
        print(f"    three bad primes: W3/T = {W3/T:.4f} (pred. R3 = {rr3:.4f})")
    print(f"    units of |A_H| V(z): S = {S/U:.4f}, T_H = {T/U:.4f} (pred. Z = {zz:.4f}), W = {Wc/U:.4f} (pred. Z R = {zz*rr:.4f});"
          f" W/T = {Wc/T:.4f} (pred. R = {rr:.4f})")
print(f"  [{time.time()-t0:.1f}s]")
