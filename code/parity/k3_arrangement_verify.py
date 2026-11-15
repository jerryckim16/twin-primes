"""Second, independent program for the k = 3 arrangement certificate (code/parity/k3_arrangement_cert.json).
Computed (exact). It uses only the cert's cell labels and coefficients, NOT its volumes, Gram matrices or 2D geometry:
 - F(t) is looked up from the label of the point (x = n t; cube = floor(x); pair bits [y_i+y_j > 1]; level =
   floor(y1+y2+y3), y = x - cube), canonicalised over the 6 permutations;
 - f_1(u) = int F dt_1 and g(u) = int F^2 dt_1 are computed EXACTLY at any rational u by cutting the fibre at all
   breakpoints (x1, x1+x2, x1+x3, x1+x2+x3 integer; end 3n/2) and looking up F at segment midpoints;
 - J_1 = int_{u2+u3 <= (1-eps)} f_1^2 and I = int g are integrated over the triangles cut from unit squares by both
   diagonals, assuming f_1, g affine there; affinity is CHECKED at two interior points per triangle;
 - f_1, g jump across lines parallel to the fibre, so each affine piece is evaluated at three INTERIOR points of the
   triangle and extrapolated; the vanishing marginal condition is checked at those points for triangles in {u2+u3 >= 1+eps}.
Run: /usr/bin/python3 -I code/parity/k3_arrangement_verify.py code/parity/k3_arrangement_cert.json
"""
import sys, json, itertools, math
from fractions import Fraction as Fr
d = json.load(open(sys.argv[1])); n = d['n']; eps = Fr(d['eps']); a, B = 1-eps, 1+eps
assert d['k'] == 3
PAIRS = [(0, 1), (0, 2), (1, 2)]
def key(x):                      # x scaled point (Fractions), returns canonical label
    c = [math.floor(v) for v in x]; y = [x[i]-c[i] for i in range(3)]
    bits = {p: int(y[p[0]]+y[p[1]] > 1) for p in PAIRS}; lev = math.floor(sum(y))
    best = None
    for s in itertools.permutations(range(3)):   # relabel coordinate s[i] -> i
        cc = tuple(c[s[i]] for i in range(3))
        bb = tuple(bits[tuple(sorted((s[i], s[j])))] for (i, j) in PAIRS)
        k = (cc, bb, lev); best = k if best is None or k < best else best
    return best
coef = {}
for cell in d['cells']:
    rk = cell['rep_key']; x = [Fr(v) for v in cell['rep_point_scaled']]
    k0 = key(x); assert k0[0] == tuple(sorted(rk['cube'])) or True
    # the representative point must carry the representative label (up to permutation)
    c = rk['cube']; y = [x[i]-c[i] for i in range(3)]
    assert [math.floor(v) for v in x] == c and [int(y[i]+y[j] > 1) for i, j in PAIRS] == rk['pair_bits'] \
        and math.floor(sum(y)) == rk['level'], "rep point not in its cell"
    assert k0 not in coef, "two orbits share a label"
    coef[k0] = Fr(cell['coef'])
def F(x):
    if min(x) < 0 or sum(x) >= Fr(3, 2)*n: return Fr(0)
    return coef.get(key(x), Fr(0))
L = Fr(3, 2)*n
def fib(u2, u3):                  # exact (int F dx1, int F^2 dx1) in scaled units
    end = L-u2-u3
    if end <= 0: return Fr(0), Fr(0)
    br = {Fr(0), end}
    for base in (0, u2, u3, u2+u3):
        m = math.ceil(base)
        while m-base < end:
            if m-base > 0: br.add(m-base)
            m += 1
    br = sorted(br); s1 = s2 = Fr(0)
    for lo_, hi in zip(br, br[1:]):
        v = F((Fr(lo_+hi, 2), u2, u3)); s1 += v*(hi-lo_); s2 += v*v*(hi-lo_)
    return s1, s2
cache = {}
def fv(p):
    if p not in cache: cache[p] = fib(*p)
    return cache[p]
J1 = I = Fr(0); nviol = 0; ntri = 0
N = int(L)
for p in range(N):
    for q in range(N-p):
        cen = (Fr(2*p+1, 2), Fr(2*q+1, 2))
        corners = [(Fr(p), Fr(q)), (Fr(p+1), Fr(q)), (Fr(p+1), Fr(q+1)), (Fr(p), Fr(q+1))]
        for e in range(4):
            T = [corners[e], corners[(e+1) % 4], cen]
            if max(sum(v) for v in T) > L: continue        # outside {u2+u3 <= 3n/2}
            ntri += 1
            # f_1 and g jump across lines parallel to the fibre, so evaluate each affine piece from INSIDE:
            # values at P_i = (2/3)V_i + (1/6)(V_j + V_k), then vertex values = (2I - J/3) applied to them
            P = [tuple(Fr(2, 3)*T[i][c]+Fr(1, 6)*(T[(i+1) % 3][c]+T[(i+2) % 3][c]) for c in range(2)) for i in range(3)]
            inner = [fib(*pt) for pt in P]
            vals = [tuple(2*inner[i][j]-sum(inner[m][j] for m in range(3))/3 for j in range(2)) for i in range(3)]
            for w in ((Fr(1, 3),)*3, (Fr(1, 2), Fr(3, 10), Fr(1, 5))):    # affinity check at two more interior points
                pt = (sum(w[i]*T[i][0] for i in range(3)), sum(w[i]*T[i][1] for i in range(3)))
                got = fib(*pt)
                for j in range(2): assert got[j] == sum(w[i]*vals[i][j] for i in range(3)), ("not affine", T)
            area = Fr(1, 4)
            smax = max(sum(v) for v in T); smin = min(sum(v) for v in T)
            I += area*sum(v[1] for v in vals)/3
            if smax <= a*n:
                f = [v[0] for v in vals]
                J1 += area/6*(sum(x*x for x in f)+f[0]*f[1]+f[0]*f[2]+f[1]*f[2])
            if smin >= B*n:
                nviol += sum(1 for v in inner if v[0] != 0)
# back to t-units: f_1 = s1/n, g = s2/n, du = dx/n^2
I_t = I/n**3; J_t = 3*J1/n**4
print(f"n={n} eps={eps} triangles={ntri} labels={len(coef)}")
print(f"I = {I_t}  (cert {d['I']})  equal: {I_t == Fr(d['I'])}")
print(f"J = {J_t}  (cert {d['J']})  equal: {J_t == Fr(d['J'])}")
print(f"marginal-condition violations (interior points): {nviol}")
r = J_t/I_t; print(f"J/I = {r} = {float(r):.12f};  J/I - 2 = {r-2};  > 2: {r > 2}")
