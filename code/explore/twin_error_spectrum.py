"""Exploration (Session 42): do the zeros of zeta show up in the error term of the twin-prime sum?

E2(x) = sum_{p <= x, p+2 prime} log p log(p+2) - 2 C2 x   (prime powers ignored: O(sqrt x log^2 x) effect)
E1(x) = theta(x) - x                                      (control: the explicit formula puts peaks at gamma)
For each, F(t) = | int_{u0}^{U} E(e^u) e^{-u/2} w(u) e^{-i t u} du |, w a Hann window, t in [5, 50].
Usage: /usr/bin/python3 -I twin_error_spectrum.py [X]   (default 2e8; ~1 min, ~0.6 GB)
Heuristic / exploratory only.
"""
import sys, numpy as np
X = int(float(sys.argv[1])) if len(sys.argv) > 1 else 2 * 10**8
s = np.ones(X + 3, dtype=bool); s[:2] = False
for i in range(2, int((X + 2) ** 0.5) + 1):
    if s[i]: s[i*i::i] = False
P = np.nonzero(s[:X + 1])[0]
lp = np.log(P.astype(float))
tw = s[P + 2]
C2 = 0.6601618158468695739
cum1 = np.cumsum(lp); cum2 = np.cumsum(np.where(tw, lp * np.log((P + 2).astype(float)), 0.0))
u0, U, M = np.log(1e4), np.log(X), 40000
u = np.linspace(u0, U, M); x = np.exp(u)
idx = np.searchsorted(P, x, side='right') - 1
E1 = cum1[idx] - x; E2 = cum2[idx] - 2 * C2 * x
w = 0.5 - 0.5 * np.cos(2 * np.pi * (u - u0) / (U - u0)); du = u[1] - u[0]
ts = np.arange(5.0, 50.0, 0.05)
def spec(E):
    g = E * np.exp(-u / 2) * w
    return np.array([abs(np.sum(g * np.exp(-1j * t * u)) * du) for t in ts])
F1, F2 = spec(E1), spec(E2)
gam = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351, 37.5862, 40.9187, 43.3271, 48.0052, 49.7738]
print(f"X = {X:.3g}; pi(X) = {len(P)}; twin pairs = {int(tw.sum())}")
print(f"rms E1/sqrt x = {np.sqrt(np.mean((E1/np.sqrt(x))**2)):.3f}; rms E2/sqrt x = {np.sqrt(np.mean((E2/np.sqrt(x))**2)):.3f}")
def peaks(F):
    pk = [i for i in range(1, len(F) - 1) if F[i] > F[i-1] and F[i] >= F[i+1]]
    pk.sort(key=lambda i: -F[i]); return [(round(ts[i], 2), round(F[i], 3)) for i in pk[:10]]
print("top peaks theta:", peaks(F1))
print("top peaks twin :", peaks(F2))
for g in gam:
    i = int(round((g - 5) / 0.05))
    print(f"gamma = {g:8.4f}: F_theta = {F1[i]:.3f}  F_twin = {F2[i]:.3f}  (median F_twin = {np.median(F2):.3f})")
# correlation of the two spectra (does the twin error inherit the prime error?)
print(f"corr(F_theta, F_twin) over t in [5,50]: {np.corrcoef(F1, F2)[0,1]:.3f}")
