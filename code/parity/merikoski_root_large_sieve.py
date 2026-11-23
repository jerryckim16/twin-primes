"""Large-sieve constants for roots of quadratic congruences (Session 48 route card,
notes/parity-attempts/2026-11-23-merikoski-large-sieve.md).

Merikoski (arXiv:2112.03617v3, Lemma 6, quoting FI98 Lemma 3.2) uses
    sum_{d<=D} sum_{nu^2+1=0 (d)} |sum_{n<=N} g_n e(nu n/d)|^2 << (D+N) sum |g_n|^2.
We compute the best constant Delta(P,N) = ||M||_op^2, M[p,n] = e(n x_p), 1<=n<=N, for point sets
    P(F, D) = { nu/d : d <= D, F(nu) = 0 mod d }
and compare with D + N (the Lemma 6 shape) and with the trivial bound #P * N.
F = x^2+1 (anisotropic, definite: Gaussian), x^2-2 (anisotropic, indefinite), x^2-1 (isotropic,
split: the twin polynomial n(n+2) = (n+1)^2 - 1).  For x^2-1 the roots are split into
'trivial' (nu = +-1 mod d, i.e. d | n or d | n+2) and 'mixed' (d = d1 d2, nu = 1 mod d1, -1 mod d2,
both d1, d2 > 2), and the mixed ones further by min(d1', d2') >= D^{1/4} (odd parts).
Deterministic; run with /usr/bin/python3 -I code/parity/merikoski_root_large_sieve.py
"""
import math
import sys
import numpy as np


def roots(F, d):
    return [v for v in range(d) if F(v) % d == 0]


def odd_part(m):
    while m % 2 == 0:
        m //= 2
    return m


def classify_split_root(v, d):
    """For nu^2 = 1 mod d return (d1, d2) with d1 = gcd(nu-1, d), d2 = gcd(nu+1, d)."""
    return math.gcd(v - 1, d), math.gcd(v + 1, d)


def delta(points, N):
    x = np.asarray(points, dtype=float)
    n = np.arange(1, N + 1, dtype=float)
    M = np.exp(2j * np.pi * np.outer(x, n))
    G = M.conj().T @ M  # N x N Hermitian
    return float(np.linalg.eigvalsh(G)[-1])


def main():
    out = []
    pr = lambda s: (out.append(s), print(s))
    D = 1000
    fams = {
        "x^2+1": lambda v: v * v + 1,
        "x^2-2": lambda v: v * v - 2,
        "x^2-1": lambda v: v * v - 1,
    }
    sets = {}
    for name, F in fams.items():
        sets[name] = [(v / d, d, v) for d in range(1, D + 1) for v in roots(F, d)]
    triv, mixed, mixed_bal = [], [], []
    q = D ** 0.25
    for (x, d, v) in sets["x^2-1"]:
        d1, d2 = classify_split_root(v, d)
        o1, o2 = odd_part(d1), odd_part(d2)
        if o1 == 1 or o2 == 1:
            triv.append((x, d, v))  # d | 2^a n or d | 2^b (n+2): one linear factor carries all odd part
        else:
            mixed.append((x, d, v))
            if min(o1, o2) >= q:
                mixed_bal.append((x, d, v))
    sets["x^2-1 trivial (odd part of d divides one factor)"] = triv
    sets["x^2-1 mixed"] = mixed
    sets["x^2-1 mixed, min odd factor >= D^(1/4)"] = mixed_bal

    pr(f"D = {D}")
    pr(f"{'point set':52s} {'#P':>6s} {'N':>5s} {'Delta':>11s} {'Delta/(D+N)':>12s} {'Delta/(#P*N)':>13s}")
    for name, P in sets.items():
        pts = [p[0] for p in P]
        for N in (30, 100, 300, 1000):
            dl = delta(pts, N)
            pr(f"{name:52s} {len(pts):6d} {N:5d} {dl:11.1f} {dl/(D+N):12.3f} {dl/(len(pts)*N):13.4f}")
    # spacing: smallest gap between distinct points mod 1, times D^2 and times D
    pr("")
    pr("minimal gap between distinct points of P mod 1; share of points within 5/D of a rational a/q with q <= 5")
    pr("(for uniformly spread points that share would be about 0.1):")
    rats = sorted(set(a / qq for qq in range(1, 6) for a in range(qq + 1)))
    for name, P in sets.items():
        allx = [p[0] % 1.0 for p in P]
        xs = sorted(set(round(x, 15) for x in allx))
        gaps = [b - a for a, b in zip(xs, xs[1:])] + [1 - xs[-1] + xs[0]]
        g = min(gaps)
        near = sum(1 for x in allx if min(abs(x - r) for r in rats) <= 5 / D)
        pr(f"{name:52s} min gap = {g:.3e} (= {g*D*D:.3f}/D^2); near-rational share = {near/len(allx):.3f}")
    with open(sys.argv[1] if len(sys.argv) > 1 else "code/parity/merikoski_root_large_sieve.out", "w") as fh:
        fh.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
