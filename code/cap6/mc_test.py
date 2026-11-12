#!/usr/bin/env python3
"""Monte Carlo sanity test of capped_exact.py at small k (Stadlmann's L, tau, g, caps)."""
import sys, json, subprocess
import numpy as np
from math import factorial
k = int(sys.argv[1]); N = int(sys.argv[2])
L, tau, g = 1.042, 0.982, 0.112
C = lambda m: 0.6 if m <= 2 else 0.68
# P = 3 P2^2 - 2 (L-P1)^2 P2 + (L-P1)^4 + 5 P4   (D = 4, b over j = 2..8)
basis = [[0, [2, 0, 0, 0, 0, 0, 0]], [2, [1, 0, 0, 0, 0, 0, 0]], [4, [0] * 7], [0, [0, 0, 1, 0, 0, 0, 0]]]
coeffs = ["3", "-2", "1", "5"]
json.dump(dict(k=k, L="521/500", tau="491/500", g="14/125", caps={"1": "3/5", "2": "3/5", "3+": "17/25"},
               basis=basis, coeffs=coeffs), open("code/cap6/P_test_k%d.json" % k, "w"))
def P(u):
    P1 = u.sum(-1); P2 = (u ** 2).sum(-1); P4 = (u ** 4).sum(-1)
    return 3 * P2 ** 2 - 2 * (L - P1) ** 2 * P2 + (L - P1) ** 4 + 5 * P4
def admissible(u):
    big = u > g
    m = big.sum(-1); s = (u * big).sum(-1)
    cap = np.where(m <= 2, 0.6, 0.68)
    return (m == 0) | (s <= cap)
rng = np.random.default_rng(1)
Is, Js = [], []
for rep in range(N // 200000):
    e = rng.exponential(size=(200000, k + 1)); u = L * e[:, :k] / e.sum(1, keepdims=True)
    Is.append((P(u) ** 2 * admissible(u)).mean() * L ** k / factorial(k))
    e = rng.exponential(size=(200000, k)); up = tau * e[:, :k - 1] / e.sum(1, keepdims=True)
    big = up > g; m = big.sum(-1); s = (up * big).sum(-1); R = L - up.sum(-1)
    Cn = np.where(m + 1 <= 2, 0.6, 0.68)
    U = np.minimum(R, np.maximum(g, Cn - s))
    ok = admissible(up)
    xs, ws = np.polynomial.legendre.leggauss(6)
    Q = np.zeros(len(up))
    for xi, wi in zip(xs, ws):
        t = U * (xi + 1) / 2
        Q += wi * U / 2 * P(np.concatenate([up, t[:, None]], 1))
    Js.append((Q ** 2 * ok).mean() * tau ** (k - 1) / factorial(k - 1))
Is, Js = np.array(Is), np.array(Js)
print("MC  I_T = %.6e +- %.1e   J_T = %.6e +- %.1e" % (Is.mean(), Is.std() / len(Is) ** .5, Js.mean(), Js.std() / len(Js) ** .5))
