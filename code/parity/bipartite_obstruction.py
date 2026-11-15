#!/usr/bin/env python3
"""Parity attempt 2026-11-15b (Session 18): which 'close prime pair' targets does the Polymath8b Section 8
parity obstruction cover?  Exact / brute-force checks for papers/parity-barrier (Prop. prop:bipartite).

(1) PM8b Remark 8.1 weight, as printed (pairs 0 <= i <= i' <= H, (n+i,3) = (n+i',3) = 1, i'-i <= 4) and as
    corrected (i < i', n+i and n+i' odd): compute omega(n) exactly for n <= N with lambda = Liouville.
(2) LP: for a graph G on k vertices, is there a probability distribution on sets I (the positions with
    lambda = -1) containing no edge, with P(i in I) = 1/2 for every i?  Claim: iff G bipartite.
    Checked by exact rational LP (vertex enumeration over independent sets via scipy linprog, then an exact
    rational witness / odd-cycle certificate).
(3) H(k) = minimal diameter of an admissible k-tuple, k <= 9, by brute force.
(4) Window version for H_m: alternating colouring witness for tuples whose windows hold <= 2m elements.
usage: python3 code/parity/bipartite_obstruction.py  (writes code/parity/bipartite_obstruction.json)"""
import itertools, json, random
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog

def liouville(N):
    lam = [1] * (N + 1); rem = list(range(N + 1))
    for p in range(2, N + 1):
        if rem[p] == p or True:
            pass
    # Omega via smallest prime factor sieve
    spf = list(range(N + 1))
    for p in range(2, int(N ** 0.5) + 1):
        if spf[p] == p:
            for m in range(p * p, N + 1, p):
                if spf[m] == m: spf[m] = p
    lam[0] = 0
    for n in range(2, N + 1):
        lam[n] = -lam[n // spf[n]]
    return lam

def remark81(lam, n, H, corrected):
    w = 1
    for i in range(H + 1):
        for j in range(i, H + 1):
            if corrected and (j == i or (n + i) % 2 == 0 or (n + j) % 2 == 0):
                continue
            if (n + i) % 3 == 0 or (n + j) % 3 == 0 or j - i > 4:
                continue
            w *= (1 - lam[n + i] * lam[n + j])
            if w == 0: return 0
    return w

def is_bipartite(k, E):
    col = [None] * k; adj = [[] for _ in range(k)]
    for a, b in E: adj[a].append(b); adj[b].append(a)
    for s in range(k):
        if col[s] is None:
            col[s] = 0; st = [s]
            while st:
                u = st.pop()
                for v in adj[u]:
                    if col[v] is None: col[v] = 1 - col[u]; st.append(v)
                    elif col[v] == col[u]: return False, None
    return True, col

def lp_feasible(k, E):
    Es = set(map(frozenset, E))
    ind = [I for r in range(k + 1) for I in itertools.combinations(range(k), r)
           if not any(frozenset(p) in Es for p in itertools.combinations(I, 2))]
    A = np.zeros((k + 1, len(ind)))
    for c, I in enumerate(ind):
        A[k, c] = 1
        for i in I: A[i, c] = 1
    b = np.array([0.5] * k + [1.0])
    r = linprog(np.zeros(len(ind)), A_eq=A, b_eq=b, bounds=[(0, None)] * len(ind), method="highs")
    return r.status == 0

def admissible(H):
    for p in range(2, len(H) + 1):
        if all(p % q for q in range(2, p)):
            if len({h % p for h in H}) == p: return False
    return True

def narrowest(k, dmax=60):
    for d in range(1, dmax + 1):
        for mid in itertools.combinations(range(1, d), k - 2):
            H = (0,) + mid + (d,)
            if admissible(H): return d, list(H)
    return None

def main():
    out = {}
    N = 20000; lam = liouville(N + 40)
    r81 = {}
    for H in (4, 6, 8, 12):
        pr = sum(1 for n in range(1, N) if remark81(lam, n, H, False) != 0)
        co = [n for n in range(1, N) if remark81(lam, n, H, True) != 0]
        # corrected weight must vanish whenever two primes at distance <= 4 sit in [n, n+H]
        isprime = lambda m: m > 1 and lam[m] == -1 and all(m % q for q in range(2, int(m ** 0.5) + 1))
        bad = [n for n in co if any(isprime(n + i) and isprime(n + j)
                                    for i in range(H + 1) for j in range(i + 1, min(H, i + 4) + 1))]
        r81[H] = {"printed_nonzero_count": pr, "corrected_nonzero_count": len(co), "corrected_but_close_primes": len(bad)}
    out["remark81_n_le_%d" % N] = r81
    random.seed(20261115); agree = 0; tested = 0; nb = 0
    for trial in range(400):
        k = random.randint(3, 9); p = random.choice([0.2, 0.35, 0.5])
        E = [e for e in itertools.combinations(range(k), 2) if random.random() < p]
        bip, _ = is_bipartite(k, E); feas = lp_feasible(k, E)
        tested += 1; agree += (bip == feas); nb += (not bip)
    out["lp_vs_bipartite"] = {"graphs": tested, "agree": agree, "non_bipartite": nb}
    # DHL[k, m+1] hypergraph: sets of size <= m, marginals 1/2  <=>  k <= 2m (exact witness: size-m random subset w.p. k/(2m))
    out["H_of_k"] = {k: narrowest(k) for k in range(2, 10)}
    print(json.dumps(out, indent=1))
    json.dump(out, open("code/parity/bipartite_obstruction.json", "w"), indent=1)

if __name__ == "__main__":
    main()
