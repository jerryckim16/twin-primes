#!/usr/bin/env python3
"""Heuristic illustration for the parity paper, Remark rem:lt22 (Session 30).

Usage: /usr/bin/python3 -I code/parity/hybrid_shifted_primes.py [X] [HMAX]   (defaults 2e7, 64; ~1 min, < 1 GB)

Context. Lichtman-Teravainen (arXiv:2111.08912v3, Cor. 1.4) prove sum_{p<=X} mu(p+h) = o(pi(X)) for all but o(H)
shifts h <= H once H >= (log X)^{1+eps} (the same for the Liouville function lambda). Their input on mu/lambda is a
bound for short exponential sums on average over x (their Prop. 2.1, (2.3)-(2.4)). The elementary "conspiracy"
lemma of the remark says: if f' agrees with f off U = {p + h : p in P, 1 <= h <= H} and f' = +1 on U, then
   (a) sum_{h<=H} sum_{p in P} f'(p+h) = H |P|                         (total failure of cancellation), and
   (b) for every alpha:  sum_{0<=x<X} |B_x(alpha)| <= 18 H^2 |P|,  sum_x |B_x(alpha)|^2 <= 108 H^3 |P|,
       where B_x(alpha) = sum_{x<=n<=x+2H} (f'(n) - f(n)) e(n alpha).
So a short-interval input that saves only H^{-delta} cannot exclude f' when H^{1+delta} << log X.

What the script does (counts exact; normalisations floating point):
 1. Computes lambda(n) = (-1)^Omega(n) for n <= X + 3*HMAX by a sieve, and the primes P = {p <= X}.
 2. For 1 <= h <= HMAX: S(h) = sum_{p<=X} lambda(p+h) exactly; prints S(h)/pi(X), and the mean of |S(h)|/pi(X)
    over odd and over even h, against the random-sign scale pi(X)^{-1/2}.
 3. For H in {2,4,...,HMAX}: builds the conspiracy f' = lambda modified on U, and prints, at alpha in
    {0, 1/2, 1/3, 1/4, 1/5}, the normalised L^1 averages A(f) = sum_x |sum_{x<=n<=x+2H} f(n) e(n alpha)| / (H X)
    for f = lambda and f = f', the exact checks of (b) for B = f' - lambda, and the targets
    T(f) = sum_{h<=H} sum_p f(p+h) / (H pi(X)).
 4. Exploration (Session 30): sign pattern of S(h) across h (Polya-type bias on shifted primes?).
"""
import sys, math, cmath
import numpy as np

X = int(float(sys.argv[1])) if len(sys.argv) > 1 else 2 * 10**7
HMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 64
N = X + 3 * HMAX + 2

# --- lambda by sieve: Omega(n) mod 2 -------------------------------------------------------------
rem = np.arange(N + 1, dtype=np.int64)
par = np.zeros(N + 1, dtype=np.int8)
r = int(math.isqrt(N))
small = np.ones(r + 1, dtype=bool); small[:2] = False
for p in range(2, int(math.isqrt(r)) + 1):
    if small[p]:
        small[p * p::p] = False
for p in np.nonzero(small)[0].tolist():
    pk = p
    while pk <= N:
        rem[pk::pk] //= p
        par[pk::pk] ^= 1
        pk *= p
par ^= (rem > 1).astype(np.int8)        # one remaining prime factor > sqrt(N)
lam = (1 - 2 * par.astype(np.int64))    # lambda(n), n >= 1 (index 0 unused)
lam[0] = 0
is_prime = (rem == np.arange(N + 1)) & (par == 1)   # n = rem means no small factor; parity 1 means one factor
is_prime[:2] = False
for p in np.nonzero(small)[0].tolist():
    is_prime[p] = True
del rem
P = np.nonzero(is_prime[: X + 1])[0]
piX = len(P)
print(f"X = {X}, pi(X) = {piX}, log X = {math.log(X):.3f}, HMAX = {HMAX}")
assert piX == {10**6: 78498, 10**7: 664579, 2 * 10**7: 1270607, 10**8: 5761455}.get(X, piX), "pi(X) mismatch"

# --- 2. S(h) -----------------------------------------------------------------------------------------
Sh = np.array([int(lam[P + h].sum()) for h in range(1, HMAX + 1)])
print("\n[2] S(h)/pi(X) for h = 1..HMAX (exact S(h) in parentheses for h <= 8):")
print("   ", " ".join(f"{h}:{Sh[h-1]/piX:+.4f}({Sh[h-1]})" for h in range(1, 9)))
odd = np.abs(Sh[0::2]) / piX; even = np.abs(Sh[1::2]) / piX
print(f"    mean |S(h)|/pi(X): odd h {odd.mean():.5f}, even h {even.mean():.5f}; pi(X)^(-1/2) = {piX**-0.5:.5f}")
print(f"    mean S(h)/pi(X): odd h {Sh[0::2].mean()/piX:+.5f}, even h {Sh[1::2].mean()/piX:+.5f}")
k = int(np.argmax(np.abs(Sh))); print(f"    max_h |S(h)|/pi(X) = {abs(Sh[k])/piX:.5f} at h = {k+1}")
print(f"    number of h with S(h) < 0: {(Sh < 0).sum()} of {HMAX} (odd h: {(Sh[0::2] < 0).sum()}, even h: {(Sh[1::2] < 0).sum()})")

# --- 3. conspiracy -----------------------------------------------------------------------------------
def window_sums(v, H, alpha):
    """sum_{x<=n<=x+2H} v(n) e(n alpha) for 0 <= x < X, via prefix sums (complex for alpha != 0)."""
    n = np.arange(len(v))
    w = v * np.exp(2j * np.pi * alpha * n) if alpha else v.astype(np.float64)
    c = np.concatenate(([0], np.cumsum(w)))
    x = np.arange(0, X)
    return c[x + 2 * H + 1] - c[x]

alphas = [0.0, 1 / 2, 1 / 3, 1 / 4, 1 / 5]
print("\n[3] conspiracy f' (= +1 on U = P + [1,H], = lambda elsewhere):")
print("    H   |U|/X    T(lam)    T(f')   A(lam)@alphas            A(f')@alphas             L1(B)/(18H^2|P|)  L2(B)/(108H^3|P|)")
H = 2
while H <= HMAX:
    fp = lam.copy()
    for h in range(1, H + 1):
        fp[P + h] = 1
    Uset = np.zeros(N + 1, dtype=bool)
    for h in range(1, H + 1):
        Uset[P + h] = True
    Tl = sum(int(lam[P + h].sum()) for h in range(1, H + 1)) / (H * piX)
    Tf = sum(int(fp[P + h].sum()) for h in range(1, H + 1)) / (H * piX)
    assert sum(int(fp[P + h].sum()) for h in range(1, H + 1)) == H * piX     # (a), exactly
    Al, Af, l1r, l2r = [], [], 0.0, 0.0
    for a in alphas:
        wl = window_sums(lam, H, a); wf = window_sums(fp, H, a)
        Al.append(np.abs(wl).sum() / (H * X)); Af.append(np.abs(wf).sum() / (H * X))
        B = wf - wl
        l1 = np.abs(B).sum(); l2 = (np.abs(B) ** 2).sum()
        assert l1 <= 18 * H**2 * piX * (1 + 1e-12) and l2 <= 108 * H**3 * piX * (1 + 1e-12)   # (b)
        l1r = max(l1r, l1 / (18 * H**2 * piX)); l2r = max(l2r, l2 / (108 * H**3 * piX))
    print(f"   {H:3d}  {Uset.sum()/X:.4f}  {Tl:+.5f}  {Tf:+.5f}  " + " ".join(f"{v:.3f}" for v in Al)
          + "  " + " ".join(f"{v:.3f}" for v in Af) + f"   {l1r:.4f}            {l2r:.4f}")
    H *= 2
print("\n    (a) and (b) asserted exactly for every H and alpha above. A(.) is only an alpha-sample, not the sup.")
