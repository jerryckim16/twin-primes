"""Heuristic (floating point). For 1/4 < eps < 1/2 (a = 1-eps <= 3/2 - a), the unconstrained k = 3 supremum
lambda_unc(eps) = 3/2 + mu*, where mu* is the value of mu at which the positive operator
   (M_mu phi)(y) = [ int_0^{a-y} phi(t)/(mu+t+y) dt ] / [ 1 - log((mu+a)/(mu+y)) ]      on [0, a]
has spectral radius 1 (equivalently: phi(y) = int_0^{a-y} (phi(t)+phi(y))/(mu+t+y) dt has a positive solution).
Nystrom with Gauss-Legendre nodes on [0,a] (the kernel's cut at t = a-y handled by splitting); bisection in mu.
Run: /usr/bin/python3 code/parity/k3_unc_1d.py eps [N]
"""
import sys, numpy as np
eps = float(sys.argv[1]); N = int(sys.argv[2]) if len(sys.argv) > 2 else 400; a = 1-eps
assert 0.25 < eps < 0.5
def rho(mu, N=N):
    # piecewise-linear phi on a uniform grid; exact integrals of hat functions against 1/(mu+t+y) over [0, a-y]
    ys = np.linspace(0, a, N+1); h = a/N
    M = np.zeros((N+1, N+1))
    for r, y in enumerate(ys):
        top = a-y; s = mu+y
        for k in range(N):
            lo, hi = k*h, min((k+1)*h, top)
            if hi <= lo: break
            # on [lo,hi]: phi = phi_k*(t_{k+1}-t)/h + phi_{k+1}*(t-t_k)/h
            I0 = np.log((s+hi)/(s+lo)); I1 = (hi-lo) - s*I0          # int 1/(s+t), int t/(s+t)
            tk = k*h
            M[r, k] += ((tk+h)*I0 - I1)/h; M[r, k+1] += (I1 - tk*I0)/h
        M[r] /= (1-np.log((mu+a)/(mu+y)))
    return max(abs(np.linalg.eigvals(M)))
lo, hi = a/(np.e-1)+1e-9, 2.0
for _ in range(60):
    mid = (lo+hi)/2
    if rho(mid) > 1: lo = mid
    else: hi = mid
print(f"eps={eps} N={N} mu*={hi:.8f} lambda_unc={1.5+hi:.8f}")
