#!/usr/bin/env python3
"""Exploration (Session 37): weighted almost-prime targets sum_i a_i Omega(L_i(n)) <= r in the Liouville-pattern class.

Compatible sign patterns: x in {0,1}^k (x_i = 1 for sign +1, i.e. Omega_i even >= 2) with sum a_i (1 + x_i) <= r, i.e.
a.x <= r - A (A = sum a_i). Blocked iff (1/2,...,1/2) lies in conv{x : a.x > r - A} (fair) [weakly fair: some point of
that hull with every coordinate <= 1/2 ... i.e. marginal P(+) <= 1/2]. Compare with the naive 'mean test':
A/2 > r - A  (necessary for fair blocking, since a.x has mean A/2 under any fair measure).
Question: is the mean test also sufficient? Are there weighted targets whose class answer is NOT a DHL-type count?
"""
import itertools, sys
import numpy as np
from scipy.optimize import linprog

def blocked(a, r, weak=False):
    k = len(a); A = sum(a)
    free = [x for x in itertools.product((0, 1), repeat=k) if sum(ai * xi for ai, xi in zip(a, x)) > r - A]
    if not free:
        return False
    M = np.array(free, dtype=float).T  # k x n, P(+ at i)
    n = M.shape[1]
    if weak:
        res = linprog(np.zeros(n), A_ub=M, b_ub=[0.5] * k, A_eq=np.ones((1, n)), b_eq=[1], bounds=[(0, None)] * n, method="highs")
    else:
        res = linprog(np.zeros(n), A_eq=np.vstack([M, np.ones((1, n))]), b_eq=[0.5] * k + [1], bounds=[(0, None)] * n, method="highs")
    return res.status == 0

def main(kmax=5, amax=4):
    total = 0; mismatch_mean = []; weak_diff = 0
    for k in range(2, kmax + 1):
        for a in itertools.combinations_with_replacement(range(1, amax + 1), k):
            A = sum(a)
            for r in range(A, 2 * A + 1):
                b = blocked(a, r); bw = blocked(a, r, weak=True)
                mean_test = (A / 2 > r - A)
                total += 1
                weak_diff += (b != bw)
                if b != mean_test:
                    mismatch_mean.append((a, r, b, mean_test))
    print(f"targets tested: {total}; fair != weakly fair: {weak_diff}; class != mean test: {len(mismatch_mean)}")
    for a, r, b, m in mismatch_mean[:25]:
        A = sum(a)
        print(f"  a={a} r={r} (slack r-A={r-A}, A/2={A/2}): blocked={b}, mean test says {m}")

if __name__ == "__main__":
    main(*(int(x) for x in sys.argv[1:]))
