#!/usr/bin/env python3
"""Search for odd cycles of linear forms realising 'x, x+d both E2' (route card 2026-11-18-e2-odd-cycles).

A vertex is a form L(m) = a m + b (a > 0).  An edge (L, c, L', c', s) means the polynomial identity
    c L(m) + s d = c' L'(m),  s = +-1, c, c' in MULT (default {1, 3, 5, 7, 11, 13}; pass a list such as 1,2,3,5,7,11,13 to include 2).
On the edge event, x = c L(m) and x + s d = c' L'(m) are both E2 when:
    c = 1 -> L(m) is E2 (lambda = +1);  c prime -> L(m) is a prime != c (lambda = -1).
So the edge requires the sign pair (sigma, sigma') = ((-1)^{Omega(c)}, (-1)^{Omega(c')}).
We look for cycles of odd length through a start vertex, with the vertex set an admissible system of forms
(no prime p has p | prod L_i(m) for every m), gcd(a_i, b_i) = 1, distinct forms.
Usage: e2_odd_cycles.py [d] [maxlen] [A0]   (defaults 2 7 12)
"""
import sys, itertools, math
from collections import defaultdict

d = int(sys.argv[1]) if len(sys.argv) > 1 else 2
MAXLEN = int(sys.argv[2]) if len(sys.argv) > 2 else 7
A0 = int(sys.argv[3]) if len(sys.argv) > 3 else 12
MULT = [int(x) for x in sys.argv[4].split(",")] if len(sys.argv) > 4 else [1, 3, 5, 7, 11, 13]
AMAX = 10**5

def primes_upto(n):
    return [p for p in range(2, n + 1) if all(p % q for q in range(2, int(p ** 0.5) + 1))]

def nbrs(v):
    a, b = v
    out = []
    for c in MULT:
        for c2 in MULT:
            if (c * a) % c2:
                continue
            a2 = c * a // c2
            if a2 > AMAX:
                continue
            for s in (1, -1):
                num = c * b + s * d
                if num % c2:
                    continue
                b2 = num // c2
                if (a2, b2) == (a, b):
                    continue
                out.append(((a2, b2), (c, c2, s)))
    return out

def admissible(forms):
    k = len(forms)
    ps = set(primes_upto(max(k, 2)))
    for a, b in forms:
        g = math.gcd(a, b)
        if g != 1:
            return False
    for p in ps:
        if all(any((a * m + b) % p == 0 for a, b in forms) for m in range(p)):
            return False
    return True

def paths_from(start, L):
    """dict length -> dict endpoint -> list of (vertex path, edge labels)."""
    layers = {0: {start: [((start,), ())]}}
    for l in range(1, L + 1):
        nxt = defaultdict(list)
        for w, plist in layers[l - 1].items():
            nb = nbrs(w)
            for path, labs in plist:
                for (u, lab) in nb:
                    if u in path:
                        continue
                    nxt[u].append((path + (u,), labs + (lab,)))
        layers[l] = nxt
    return layers

def sign(c):
    return 1 if c == 1 else -1

found = []
seen = set()
for a0 in range(1, A0 + 1):
    for b0 in range(0, a0):
        if math.gcd(a0, b0) != 1:
            continue
        start = (a0, b0)
        half = (MAXLEN + 1) // 2
        layers = paths_from(start, half)
        for ell in range(3, MAXLEN + 1, 2):
            p1 = ell // 2          # shorter arm
            p2 = ell - p1          # longer arm (p2 = p1 + 1)
            for w, A in layers[p1].items():
                B = layers[p2].get(w)
                if not B:
                    continue
                for (pa, la) in A:
                    for (pb, lb) in B:
                        if set(pa[1:-1]) & set(pb[1:-1]) or len(set(pa) | set(pb)) != ell:
                            continue
                        verts = tuple(sorted(set(pa) | set(pb)))
                        key = (ell, verts)
                        if key in seen:
                            continue
                        seen.add(key)
                        if admissible(list(verts)):
                            found.append((ell, pa, la, pb, lb))
print(f"d = {d}, odd cycles of length <= {MAXLEN} through starts a0 <= {A0}, multipliers {MULT}")
print(f"distinct odd-cycle vertex sets examined: {len(seen)}")
bylen = defaultdict(int)
for f in found:
    bylen[f[0]] += 1
print("admissible odd cycles found, by length:", dict(bylen))
for f in found[:20]:
    ell, pa, la, pb, lb = f
    print(ell, "arm1", pa, la, "| arm2", pb, lb)

# --- Check of the 2-adic colouring (Prop. in the route card) on every edge met from the starts above ---
def v2(n):
    n = abs(n); t = 0
    while n % 2 == 0:
        n //= 2; t += 1
    return t

def chi(v):
    a, b = v
    ao = a >> v2(a)
    t = v2(d)
    mod = 1 << (t + 1)
    return ((b * pow(ao, -1, mod)) % mod) >> t

if all(c % 2 for c in MULT):
    checked = 0
    for a0 in range(1, A0 + 1):
        for b0 in range(0, a0):
            frontier = {(a0, b0)}
            ball = set(frontier)
            for _ in range(3):
                new = set()
                for w in frontier:
                    for (u, lab) in nbrs(w):
                        assert chi(u) != chi(w), (w, u, lab)
                        checked += 1
                        if u not in ball:
                            new.add(u)
                ball |= new
                frontier = new
    print(f"2-adic colouring: bit v2(d) of b * (odd part of a)^-1 flips on all {checked} edges checked (odd multipliers)")
else:
    print("multiplier set contains 2: colouring check skipped")
