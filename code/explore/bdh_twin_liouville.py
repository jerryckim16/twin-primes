"""Exploration (Heuristic), 15 Nov 2026: Barban-Davenport-Halberstam variance for f(n) = lambda(n)lambda(n+2).

V(Q) = sum_{W<=Q} sum_{b mod W} |sum_{n<=N, n=b (W)} f(n)|^2 equals
  Q*sum f^2 + 2 sum_{1<=d<N} floor-count(W<=Q : W|d) * C(d),  C(d) = sum_{n+d<=N} f(n) f(n+d),
so it is governed by the 'parallelogram' four-point Liouville correlations C(d).
Random-sign model: E V(Q) = Q*N (diagonal only).  We compute C(d), d <= D, and V(Q) directly for small Q.
Usage: python3 bdh_twin_liouville.py [N] [D] [Q]
"""
import sys, numpy as np

def liouville(N):
    # lambda(n) for 0..N via smallest-prime-factor sieve on Omega parity
    om = np.zeros(N + 1, dtype=np.int8)
    rem = np.arange(N + 1, dtype=np.int64)
    for p in range(2, int(N ** 0.5) + 1):
        if rem[p] == p and om[p] == 0:  # p prime (not yet divided)
            pk = p
            while pk <= N:
                idx = np.arange(pk, N + 1, pk)
                om[idx] ^= 1
                rem[idx] //= p
                pk *= p
    om[rem > 1] ^= 1  # one remaining prime factor > sqrt(N)
    lam = 1 - 2 * om.astype(np.int64)
    lam[0] = 0
    return lam

def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 10**7
    D = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
    Q = int(sys.argv[3]) if len(sys.argv) > 3 else 300
    lam = liouville(N + 2)
    assert lam[1] == 1 and lam[2] == -1 and lam[4] == 1 and lam[12] == -1 and lam[30] == -1
    f = lam[1:N + 1] * lam[3:N + 3]          # f(n), n = 1..N
    print(f"N={N}: sum f / N = {f.sum()/N:.3e}  (sqrt(N)/N = {N**-0.5:.1e})")
    C = np.array([int(np.dot(f[:-d], f[d:])) for d in range(1, D + 1)])
    z = C / np.sqrt(N)
    print(f"C(d)/sqrt(N), d=1..{D}: mean {z.mean():+.3f}, rms {np.sqrt((z**2).mean()):.3f}, max|.| {np.abs(z).max():.2f} at d={np.abs(z).argmax()+1}")
    for d in (1, 2, 3, 4, 6, 12, 30, 60):
        print(f"  C({d})/N = {C[d-1]/N:+.2e}")
    # even vs odd d (n and n+d same parity class mod 2 matters for lambda(n+2)?)
    print(f"  rms over even d: {np.sqrt((z[1::2]**2).mean()):.3f}; odd d: {np.sqrt((z[0::2]**2).mean()):.3f}")
    # direct variance V(Q)/(Q N) for small Q
    V = 0
    for W in range(1, Q + 1):
        s = np.bincount(np.arange(1, N + 1) % W, weights=f, minlength=W)
        V += float((s ** 2).sum())
    print(f"V(Q)/(Q N) at Q={Q}: {V/(Q*N):.4f}  (random-sign model: 1)")

if __name__ == "__main__":
    main()
