"""Exploration (Session 49): Hardy-Littlewood prediction for the variance of twin-prime counts in
blocks of length H near x, compared with the measurements of code/explore/twin_short_variance.py (S48).

Model (heuristic): N = #{n in block : n, n+2 prime}. With S2 = 2 C_2 and S4(h) = S({0,2,h,h+2}),
  E N = H S2 / L^2,   Var N = E N + 2 sum_{h=1}^{H-1} (H-h) (S4(h) - S2^2) / L^4,
so ratio = Var/E = 1 + 2 sum_{h<H} (H-h)(S4(h) - S2^2) / (H S2 L^2), L = log x.
(S4(2) = S({0,2,4}) = 0; the h = 2 term then subtracts S2^2/L^4 as it should.)
S4(h) is an Euler product truncated at P = 10^6 (tail factor exp(-6/(P log P)) ignored, < 1e-6 relative).
Usage: /usr/bin/python3 -I twin_variance_prediction.py   (~10 s)
Heuristic / exploratory only.
"""
import math
import numpy as np

P = 10**6
sieve = np.ones(P + 1, bool); sieve[:2] = False
for i in range(2, int(P**0.5) + 1):
    if sieve[i]: sieve[i*i::i] = False
primes = np.nonzero(sieve)[0]

def nu(p, h):
    return len({0 % p, 2 % p, h % p, (h + 2) % p})

# base: product over p >= 5 of (1-4/p)/(1-1/p)^4
pl = primes[primes >= 5].astype(float)
logbase = np.sum(np.log1p(-4 / pl) - 4 * np.log1p(-1 / pl))
C2 = math.exp(np.sum(np.log1p(-1 / (primes[primes >= 3].astype(float) - 1) ** 2)))
S2 = 2 * C2

def factor_set(n, small=primes[:2000]):
    out = set()
    for p in small:
        p = int(p)
        if p * p > n: break
        while n % p == 0:
            out.add(p); n //= p
    if n > 1: out.add(n)
    return out

def S4(h):
    if h % 2: return 0.0
    val = logbase
    for p in (2, 3):
        v = nu(p, h)
        if v >= p: return 0.0
        val += math.log(1 - v / p) - 4 * math.log(1 - 1 / p)
    ps = set()
    for m in (h, h - 2, h + 2):
        if m > 0: ps |= factor_set(m)
    for p in ps:
        if p < 5: continue
        v = nu(p, h)
        if v >= p: return 0.0
        val += math.log(1 - v / p) - math.log(1 - 4 / p)
    return math.exp(val)

Hmax = 2**18
s4 = np.array([0.0] + [S4(h) for h in range(1, Hmax)])
d = s4 - S2**2
d[0] = 0.0
h = np.arange(Hmax, dtype=float)
cum_d = np.cumsum(d); cum_hd = np.cumsum(h * d)

L = math.log(0.75e9)   # midpoint of (X/2, X], X = 1e9, as in the S48 run
meas = {16: 0.9690, 32: 0.9578, 64: 0.9516, 128: 0.9378, 256: 0.9221, 512: 0.9089, 1024: 0.8923,
        2048: 0.8737, 4096: 0.8556, 8192: 0.8366, 16384: 0.8086, 32768: 0.7839, 65536: 0.7522,
        131072: 0.7102, 262144: 0.6914}
print(f"S2 = 2C2 = {S2:.10f};  L = log(0.75e9) = {L:.4f}")
print("check: mean of S4(h) over even h <= 2^18, divided by S2^2:", f"{s4[2::2].mean()/S2**2:.6f}")
print("     H    sum_{h<H}(S4-S2^2)   pred ratio   meas ratio (S48, X=1e9)   (1-pred)L/(1-meas)L")
xs, ys = [], []
for H in sorted(meas):
    tot = H * cum_d[H - 1] - cum_hd[H - 1]   # sum_{h<H} (H-h) d(h)
    pred = 1 + 2 * tot / (H * S2 * L**2)
    print(f"{H:7d} {cum_d[H-1]:20.3f} {pred:12.4f} {meas[H]:12.4f} {(1-pred)/(1-meas[H]):24.3f}")
    if 64 <= H <= 2**14: xs.append(math.log(H)); ys.append((1 - pred) * L)
c, b = np.polyfit(xs, ys, 1)
print(f"fit of the prediction like S48: (1 - ratio) log x ~ {c:.3f} log H + {b:.3f}   (S48 measured: 0.513 log H - 1.256)")
# the singular-series sum itself: compare sum_{h<H}(S4 - S2^2) with -a log H type behaviour
for H in (2**8, 2**10, 2**12, 2**14, 2**16, 2**18):
    print(f"H = {H:7d}: (1/H) sum_(h<H)(H-h)(S4-S2^2) = {(H*cum_d[H-1]-cum_hd[H-1])/H:12.4f},  / log H = {(H*cum_d[H-1]-cum_hd[H-1])/H/math.log(H):9.4f}")
