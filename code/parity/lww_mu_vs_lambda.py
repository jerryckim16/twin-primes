#!/usr/bin/env python3
"""Session 50 (2026-11-24): which properties of the TARGET mu does the Lu-Wang-Wu argument
(arXiv:2610.20242v2, Sections 2-3, 4.1, 5.3) use?  Toy-scale check of model functions against
the three target properties identified in notes/parity-attempts/2026-11-24-lww-mu-vs-lambda.md:

  P1  |f| <= 1 (or <= L^C)
  P2  sign-multiplicativity at the auxiliary primes R = (exp(L^0.1), exp(2 L^0.2)]:
      f(d v) = sigma^{omega(d)} f(v) for squarefree R-composed d, (d, v) = 1, sigma fixed
  P3  Bombieri-Vinogradov with ZERO main term, as in their (3.1)

and of the correlation  sum_{p <= x} f(p + 2) / pi(x).

Toy scale only (Y = 1e7, window (5e6, 1e7], R = {5,...,31}); this is an illustration of the reading, NOT a verification
of anything asymptotic.  Usage: /usr/bin/python3 -I lww_mu_vs_lambda.py [Y] [M]
(Y = 1e7, M = 100: about 2 minutes, < 1.5 GB).
"""
import sys, math
import numpy as np

Y = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10**7
M = int(sys.argv[2]) if len(sys.argv) > 2 else 100
L = math.log(Y)
rng = np.random.default_rng(20261124)

# ---- smallest-prime-factor sieve on [0, Y] ----
spf = np.zeros(Y + 1, np.int32)
for i in range(2, math.isqrt(Y) + 1):
    if spf[i] == 0:
        blk = spf[i * i::i]
        blk[blk == 0] = i
spf_idx = np.nonzero(spf == 0)[0]
spf[spf_idx] = spf_idx            # primes (and 0, 1)
spf[0] = 0; spf[1] = 1
isprime = np.zeros(Y + 1, bool)
isprime[2:] = spf[2:] == np.arange(2, Y + 1)
primes = np.nonzero(isprime)[0]

# ---- mu, lambda via repeated division by spf ----
n = np.arange(Y + 1, dtype=np.int64)
rem = n.copy(); rem[0] = 1
mu = np.ones(Y + 1, np.int8); lam = np.ones(Y + 1, np.int8)
last = np.zeros(Y + 1, np.int64)
while True:
    act = rem > 1
    if not act.any():
        break
    p = spf[rem[act]].astype(np.int64)
    idx = np.nonzero(act)[0]
    lam[idx] = -lam[idx]
    sq = last[idx] == p
    mu[idx[sq]] = 0
    mu[idx[~sq]] = -mu[idx[~sq]]
    last[idx] = p
    rem[idx] //= p
mu[0] = 0; lam[0] = 0
del rem, last

# Lambda(n) on prime powers
Lam = np.zeros(Y + 1)
for p in primes:
    pk = int(p)
    while pk <= Y:
        Lam[pk] = math.log(p)
        pk *= int(p)

# ---- auxiliary primes R and the R-part ----
lo_R, hi_R = math.exp(L ** 0.1), math.exp(2 * L ** 0.2)
R = [int(p) for p in primes if lo_R < p <= hi_R]
nR = np.ones(Y + 1, np.int64); omR = np.zeros(Y + 1, np.int8); sqfR = np.ones(Y + 1, bool)
for p in R:
    pk = p
    while pk <= Y:
        nR[pk::pk] *= p
        pk *= p
    omR[p::p] += 1
    sqfR[p * p::p * p] = False
nRp = n // nR                      # R'-part (R-free part); index 0 -> 0
nRp[0] = 0

# ---- dyadic window (X0, 2 X0], X0 = Y // 2: all statistics are taken for N in this window ----
X0 = Y // 2
win = np.arange(X0 + 1, 2 * X0 + 1)

# ---- model 1 (small-level sieve model): Lambda*(m) = kappa_D 1[(m, P(D)) = 1], D = 30 ----
D = 30
small = [int(p) for p in primes if p < D]
kappa = 1.0
for p in small:
    kappa /= (1 - 1 / p)
Lstar = np.full(Y + 1, kappa)
for p in small:
    Lstar[::p] = 0.0
Lstar[0] = 0.0

# ---- model 2 (sifted to z = X0^{2/5}, the Type I level): fake primes = semiprimes p1 p2, z < p1 <= p2,
#      weighted by a blockwise constant so that their mass matches Lambda on blocks of length 10^5 ----
z = X0 ** 0.4
mm = np.arange(Y + 1, dtype=np.int64)
s_ = spf.astype(np.int64); s_[s_ == 0] = 1
q_ = mm // s_
semi = (s_ > z) & (s_ != mm) & isprime[np.minimum(q_, Y)] & (q_ >= s_)
semi[:2] = False
Lflat = np.zeros(Y + 1)
BL = 10**5
for b0 in range(0, Y + 1, BL):
    sl = slice(b0, min(b0 + BL, Y + 1))
    ns = semi[sl].sum()
    if ns:
        Lflat[sl] = semi[sl] * (Lam[sl].sum() / ns)
del mm, s_, q_

def v_of(h, model, hmin=0):
    """v(h) = (Lambda(h-2) - model(h-2)) / L for h - 2 > hmin, and 0 otherwise."""
    out = np.zeros(h.shape)
    ok = h > max(2, hmin + 2)
    out[ok] = (Lam[h[ok] - 2] - model[h[ok] - 2]) / L
    return out

chi4 = np.zeros(Y + 1, np.int8); chi4[1::4] = 1; chi4[3::4] = -1
muR = np.where(omR % 2 == 0, 1.0, -1.0) * sqfR

funcs = {}
funcs['mu'] = mu.astype(np.float64)
funcs['lambda'] = lam.astype(np.float64)
funcs['mu*chi_-4'] = (mu * chi4).astype(np.float64)
funcs['mu^2'] = (mu.astype(np.int16) ** 2).astype(np.float64)
funcs['one'] = np.ones(Y + 1); funcs['one'][0] = 0
funcs['(-1)^omega_R'] = np.where(omR % 2 == 0, 1.0, -1.0); funcs['(-1)^omega_R'][0] = 0
funcs['g3 (sieve D=30)'] = v_of(n, Lstar)
funcs['g3\' (semiprime fake)'] = v_of(n, Lflat)
g5 = muR * v_of(nRp, Lstar); g5[0] = 0; funcs['g5 (sieve D=30)'] = g5
HMIN = X0 ** 0.9     # below this size no semiprime p1 p2 with p1 > z can compensate the primes: set v = 0
g5p = muR * v_of(nRp, Lflat, HMIN); g5p[0] = 0; funcs['g5\' (semiprime fake)'] = g5p
rs = rng.choice([-1.0, 1.0], size=Y + 1); rs[0] = 0; funcs['random +-1'] = rs
# noise baselines with the same sparsity and weights: |g| times independent random signs
for nm in ['g3 (sieve D=30)', 'g3\' (semiprime fake)', 'g5 (sieve D=30)', 'g5\' (semiprime fake)']:
    funcs['|' + nm.split()[0] + '|*random'] = np.abs(funcs[nm]) * rng.choice([-1.0, 1.0], size=Y + 1)

print(f"Y = {Y}; window N in (X0, 2 X0], X0 = {X0}; L = log Y = {L:.4f}; M = {M}")
print(f"R = primes in ({lo_R:.3f}, {hi_R:.3f}] = {R}")
print(f"model 1: D = {D}, kappa_D = {kappa:.5f};  model 2: semiprimes p1 p2 with p1 > z = X0^0.4 = {z:.1f}, "
      f"max weight/L = {Lflat.max() / L:.3f} overall, {Lflat[int(X0**0.9):].max() / L:.3f} on m >= X0^0.9, "
      f"{Lflat[X0 - 1:2 * X0].max() / L:.3f} on the window; g5' uses v(h) = 0 for h - 2 <= X0^0.9 = {X0**0.9:.0f}")

# ---- (1) correlation with shifted primes: sum_{X0 < p + 2 <= 2 X0} f(p + 2) / #p ----
P = primes[(primes + 2 > X0) & (primes + 2 <= 2 * X0)]
pix = len(P)
A2 = 1.0
for p in primes[primes > 2]:
    if p > 10**5: break
    A2 *= 1 - 1 / (p * (p - 1))
predR = 1.0; densRfree = 1.0
for p in R:
    predR *= 1 - 2 / (p - 1); densRfree *= 1 - 1 / (p - 1)
print(f"\n(1) correlations over the {pix} primes p with p + 2 in the window")
print(f"    predictions: mu^2 -> A2 = {A2:.5f};  (-1)^omega_R -> prod_R (1 - 2/(l-1)) = {predR:.5f};")
print(f"    density of p with p+2 R-free: prod_R (1 - 1/(l-1)) = {densRfree:.5f} "
      f"(Mertens-type asymptotic L^0.1/(2 L^0.2) = {L**0.1/(2*L**0.2):.5f}; crude at this size)")
Rfree = nR[P + 2] == 1
for name, f in funcs.items():
    tot = f[P + 2].sum() / pix
    extra = ''
    if name.startswith('g5'):
        extra = (f"   [p+2 R-free part {f[P + 2][Rfree].sum() / pix:+.6f}, cross terms {f[P + 2][~Rfree].sum() / pix:+.6f};"
                 f" observed R-free fraction {Rfree.mean():.5f}]")
    print(f"    {name:24s} sum_p f(p+2)/#p = {tot:+.6f}{extra}")

# ---- (2) P2 check on random samples ----
print("\n(2) P2 (sign -1) on 200000 random pairs (d, v), d squarefree R-composed (1-3 primes), (d, v) = 1, d v <= Y:")
Rarr = np.array(R)
ds, vs = [], []
while len(ds) < 200000:
    k = rng.integers(1, 4)
    d = int(np.prod(rng.choice(Rarr, size=k, replace=False)))
    vmax = Y // d
    if vmax < 3: continue
    v = int(rng.integers(1, vmax + 1))
    if math.gcd(d, v) != 1: continue
    ds.append(d); vs.append(v)
ds = np.array(ds, np.int64); vs = np.array(vs, np.int64)
sgn = np.where(omR[ds] % 2 == 0, 1.0, -1.0)
for name, f in funcs.items():
    lhs = f[ds * vs]; rhs = sgn * f[vs]
    nz = (lhs != 0) | (rhs != 0)
    print(f"    {name:24s} fraction with f(dv) = (-1)^omega(d) f(v): {np.mean(np.isclose(lhs, rhs)):.4f}"
          f"   (among pairs with a nonzero side: {np.mean(np.isclose(lhs[nz], rhs[nz])):.4f})")

# ---- (3) P3 statistics on the window, relative to the mass sum |f| over the window ----
#  S_red: sum_{3<=m<=M} max_{(c,m)=1} max_y |sum_{X0<N<=y, N=c (m)} f(N)|   (reduced classes, as in (3.1))
#  S_2  : sum_{3<=q<=M, q odd} max_y |sum_{X0<N<=y, N=2 (q)} f(N)|      (the classes N = qk + 2 of T_1, T_2, q > 1)
#  NOTE: S_2 starts at q = 3; the q = 1 (d = 1) term of T_1, sum_k R_Z(k) log k f(k+2) W(k+2), is not tested here
#  directly; it needs f to have zero mean in reduced classes mod d | P, which S_red covers only for d <= M.
#  P2 column (2) tests sigma = -1 only (mu^2 and 1 satisfy P2 with sigma = +1).
print(f"\n(3) BV-type statistics on the window, divided by sum_window |f|; moduli 3..{M}")
print("    zero-main-term BV predicts both small (random +-1 = square-root baseline; f = 1 has S_red ~ sum 1/phi(m))")
for name, f in funcs.items():
    fw = f[X0 + 1:2 * X0 + 1]
    mass = np.abs(fw).sum()
    Sred = 0.0; S2 = 0.0
    for m in range(3, M + 1):
        Wm = (len(fw) // m) * m
        A = fw[:Wm].reshape(-1, m)                 # column j holds N = X0 + 1 + j (mod m)
        mx = np.abs(np.cumsum(A, axis=0)).max(axis=0)
        cls = (X0 + 1 + np.arange(m)) % m
        red = np.array([math.gcd(int(c), m) == 1 for c in cls])
        Sred += mx[red].max()
        if m % 2 == 1:
            S2 += mx[cls == 2 % m][0]
    print(f"    {name:24s} S_red/mass = {Sred / mass:.5f}   S_2/mass = {S2 / mass:.5f}")
