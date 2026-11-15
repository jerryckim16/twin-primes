"""Exploration (Heuristic). The 1D Schur problem of parity paper Prop. prop:unc-ceiling is scale-invariant, so its critical mu
is kappa*(1-eps), lambda_unc(eps) = 3/2 + kappa (1-eps). Compute kappa (a = 1) by piecewise-linear Nystrom at several N,
Richardson-extrapolate (error ~ N^-2), and try mpmath.identify on the result.
Run: /usr/bin/python3 code/explore/kappa_closed_form.py
"""
import numpy as np, mpmath
def rho(mu, N):
    a = 1.0; ys = np.linspace(0, a, N+1); h = a/N; M = np.zeros((N+1, N+1))
    for r, y in enumerate(ys):
        s = mu+y
        k = np.arange(N); lo = k*h; hi = np.minimum((k+1)*h, a-y); m = hi > lo
        k, lo, hi = k[m], lo[m], hi[m]
        I0 = np.log((s+hi)/(s+lo)); I1 = (hi-lo)-s*I0; tk = k*h
        np.add.at(M[r], k, ((tk+h)*I0-I1)/h); np.add.at(M[r], k+1, (I1-tk*I0)/h)
        M[r] /= (1-np.log((mu+a)/(mu+y)))
    return max(abs(np.linalg.eigvals(M)))
def kappa(N):
    lo, hi = 1/(np.e-1)+1e-9, 2.0
    for _ in range(55):
        mid = (lo+hi)/2
        if rho(mid, N) > 1: lo = mid
        else: hi = mid
    return hi
ks = {N: kappa(N) for N in (100, 200, 400, 800)}
for N, k in ks.items(): print(N, f"{k:.12f}")
r1 = (4*ks[400]-ks[200])/3; r2 = (4*ks[800]-ks[400])/3
print(f"Richardson: {r1:.12f} {r2:.12f}; eps* = 1 - 1/(2 kappa) = {1-1/(2*r2):.9f}")
mpmath.mp.dps = 15
print("identify:", mpmath.identify(r2, ['pi', 'log(2)', 'log(3)', 'e', 'sqrt(2)', 'sqrt(3)']))
print("identify 1/kappa:", mpmath.identify(1/r2, ['pi', 'log(2)', 'log(3)', 'e']))
