#!/usr/bin/env python3
"""Search for narrow admissible k-tuples and verify admissibility.

A finite set H of integers is admissible if for every prime p it misses at
least one residue class mod p.  Only primes p <= |H| need checking.
"""
import sys, json, random

def primes_upto(n):
    return [p for p in range(2, n + 1) if all(p % q for q in range(2, int(p**0.5) + 1))]

def is_admissible(H):
    for p in primes_upto(len(H)):
        if len({h % p for h in H}) == p:
            return False
    return True

def search(k, d, node_limit=200000, seed=0):
    """Try to find an admissible k-tuple inside [0, d] (d even). Returns sorted list or None."""
    rng = random.Random(seed)
    m = d // 2                      # work with even numbers 0,2,...,d  ->  0..m
    full = (1 << (m + 1)) - 1
    ps = [p for p in primes_upto(k) if p > 2]
    cls = {p: [sum(1 << x for x in range(m + 1) if x % p == r) for r in range(p)] for p in ps}
    nodes = 0
    def dfs(i, mask):
        nonlocal nodes
        nodes += 1
        if nodes > node_limit:
            return None
        if bin(mask).count("1") < k:
            return None
        if i == len(ps):
            return mask
        p = ps[i]
        opts = sorted(range(p), key=lambda r: (bin(mask & cls[p][r]).count("1"), rng.random()))
        for r in opts:
            res = dfs(i + 1, mask & ~cls[p][r])
            if res is not None:
                return res
            if nodes > node_limit:
                return None
        return None
    mask = dfs(0, full)
    if mask is None:
        return None
    xs = [2 * x for x in range(m + 1) if mask >> x & 1]
    # choose the k consecutive survivors with smallest spread, shift to start at 0
    best = min((xs[j + k - 1] - xs[j], j) for j in range(len(xs) - k + 1))
    H = [x - xs[best[1]] for x in xs[best[1]:best[1] + k]]
    assert is_admissible(H) and len(H) == k
    return H

# Diameters H(k) of narrowest admissible k-tuples, from the literature
# (Engelsma's tables / Polymath8 database). Used only as search targets.
TARGET = {2:2,3:6,4:8,5:12,6:16,7:20,8:26,9:30,10:32,11:36,12:42,13:48,14:50,15:56,
 16:60,17:66,18:70,19:76,20:80,21:84,22:90,23:94,24:100,25:110,26:114,27:120,28:126,
 29:130,30:136,31:140,32:146,33:152,34:156,35:158,36:162,37:168,38:176,39:182,40:186,
 41:188,42:196,43:200,44:210,45:212,46:216,47:226,48:236,49:240,50:246,51:252,52:254,
 53:264,54:270,55:272}

if __name__ == "__main__":
    out = {}
    for k in range(2, 56):
        d = TARGET[k]
        H = None
        for seed in range(40):
            H = search(k, d, seed=seed)
            if H: break
        dd = d
        while H is None:           # fall back: widen until found
            dd += 2
            for seed in range(10):
                H = search(k, dd, seed=seed)
                if H: break
        out[k] = H
        print(k, d, H[-1], "OK" if H[-1] <= d else "WIDER", flush=True)
    json.dump({str(k): v for k, v in out.items()}, open("code/tuples.json", "w"))
