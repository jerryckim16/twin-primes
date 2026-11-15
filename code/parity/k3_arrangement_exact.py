"""PM8b (arXiv:1407.4897) Theorem 3.14 ratio at k = 3, eps = 1/4, over SYMMETRIC F that are piecewise constant
on the cells of the hyperplane arrangement {t_i = m/n}, {t_i + t_j = m/n}, {t_1+...+t_k = m/n} restricted to
D = {t >= 0, sum t <= S}  (k = 3: S = 3/2;  k = 2 sanity test: S = 2).

What it computes (all geometry EXACT, in scaled coordinates x = n t, so every plane has integer offset):
  * 3D cells: inside a unit cube p + [0,1)^k a cell is fixed by (p, bits[y_i+y_j > 1], floor(sum y)), y = x - p.
  * f_1(u) = int F dx_1, u = (x_2,...,x_k).  Along the x_1 fibre the cell walls sit at x_1 = m, m - x_j,
    m - x_2 - x_3.  Pairwise differences of these are u_j, u_2 + u_3 AND u_2 - u_3 (mod integers), so the fibre
    length of a 3D cell is affine on the cells of the REFINED 2D arrangement {u_j = m, u_2 + u_3 = m, u_2 - u_3 = m}
    (four triangles per unit square), NOT in general on the cells of {u_j = m, u_2 + u_3 = m} alone (the
    script exhibits a counterexample).  For k = 2 the breakpoints are u = m (unit intervals).
  * I(F) = sum_P c_P^2 vol(P), vol(P) = int of fibre length (exact: area * value at centroid).
  * J(F) = k * int_{sum u <= a} f_1^2 (symmetry), exact simplex formula for products of affine functions.
  * marginal condition: f_1 = 0 at the vertices of every refined u-cell inside {sum u >= B} (exact linear rows).
  * exact rational RREF of the constraint matrix (python-flint) -> exact null-space parametrisation
    (pivot vars = -R * free vars); exact rational Gram data A (diagonal) and B (integer matrix times a scalar).
  * "Heuristic": floating generalized eigenproblem on the null space for the max of J/I.
  * "Computed (exact certificate)": eigenvector rounded to rationals in the free coordinates, pivots solved
    exactly, J/I evaluated exactly (two independent exact evaluations of J), compared with 2 in fmpq/Fraction.
Sanity tests run first: (1) k = 2 must give max exactly 2 (extremal step function checked exactly);
(2) k = 3 total cell volume = S^3/6 and F = 1 gives f_1 = S - u_1 - u_2 on every refined cell vertex;
plus exact re-check of affinity of fibre lengths at random interior points; (3) Monte Carlo check of I, J at n = 4.

Results (see .out): Heuristic max J/I = 1.99546 (n=4), 2.000186 (8), 2.001549 (12), 2.002107 (16), 2.002387 (20),
2.002547 (24); exact certificate at n = 8 with J/I = 7734228819/3866758832 = 2 + 711155/3866758832.

Run:  /usr/bin/python3 -I code/parity/k3_arrangement_exact.py [--eps p/q] [--cert-each] [n ...]
      (default eps = 1/4, n = 4 8 12 16; n must be even with n*eps integer.  The k = 2 test is run at the same eps:
      its extremal F = 1 on [0,a]^2, 1/2 on the strips gives exactly 2 for every eps.)
      k3_arrangement_exact.out:  ... k3_arrangement_exact.py 4 8 12 16 20 24
      k3_arrangement_eps.out:    --eps 1/8 --cert-each 8 16 24 32 ; --eps 3/8 --cert-each 8 16 24 ;
                                 --eps 1/4 --cert-each 24   (concatenated)
Output is written to stdout (redirect to code/parity/k3_arrangement_exact.out); a certificate, if the exact
ratio exceeds 2 for some n, goes to code/parity/k3_arrangement_cert.json.
"""
import sys, os, math, time, json, random, itertools
from fractions import Fraction as Fr
from collections import defaultdict
os.environ.setdefault("OMP_NUM_THREADS", "2"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
import numpy as np
import scipy.linalg as sla
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import flint

EPS = Fr(1, 4)   # default; set by --eps
HERE = os.path.dirname(os.path.abspath(__file__))


def log(*a):
    print(*a, flush=True)


class Problem:
    def __init__(self, k, n, eps=None):
        eps = EPS if eps is None else Fr(eps)
        assert k in (2, 3) and n % 2 == 0 and (n * eps).denominator == 1, \
            "need n even and n*eps integer (planes 1-eps, 1+eps, 1/2-eps, 3/2 in the arrangement)"
        AA, BB = 1 - eps, 1 + eps
        self.k, self.n, self.eps = k, n, eps
        self.S = Fr(2) if k == 2 else Fr(3, 2)
        self.N = int(self.S * n)                 # scaled sum bound (integer)
        self.Aj = int(AA * n); self.Bc = int(BB * n)
        self.pairs = list(itertools.combinations(range(k), 2))
        self.perms = list(itertools.permutations(range(k)))
        self.canon_cache = {}
        self.orbit_index = {}; self.orbit_rep = []; self.orbit_pt = []

    # ---------- 3D (kD) cells ----------
    def cell_key(self, x):
        p = tuple(math.floor(v) for v in x)
        y = [v - q for v, q in zip(x, p)]
        bits = tuple(int(y[i] + y[j] > 1) for i, j in self.pairs)
        lev = math.floor(sum(y))
        return (p, bits, lev)

    def canon(self, key):
        c = self.canon_cache.get(key)
        if c is not None:
            return c
        p, bits, lev = key
        bd = dict(zip(self.pairs, bits))
        best = None
        for s in self.perms:
            p2 = tuple(p[s[i]] for i in range(self.k))
            b2 = tuple(bd[tuple(sorted((s[i], s[j])))] for i, j in self.pairs)
            kk = (p2, b2, lev)
            if best is None or kk < best:
                best = kk
        self.canon_cache[key] = best
        return best

    def orbit_of_point(self, x):
        c = self.canon(self.cell_key(x))
        o = self.orbit_index.get(c)
        if o is None:
            o = len(self.orbit_rep); self.orbit_index[c] = o
            # store an interior point of the canonical representative cell itself
            xp = next(y for y in (tuple(x[s[i]] for i in range(self.k)) for s in self.perms)
                      if self.cell_key(y) == c)
            self.orbit_rep.append(c); self.orbit_pt.append(xp)
        return o

    # ---------- refined u-cells ----------
    def ucells(self):
        """list of (vertices, measure); vertices are tuples of Fractions (dimension k-1)."""
        out = []
        N = self.N
        if self.k == 2:
            for q in range(N):
                out.append((((Fr(q),), (Fr(q + 1),)), Fr(1)))
            return out
        h = Fr(1, 2)
        for q2 in range(N):
            for q3 in range(N - q2):
                c = (q2 + h, q3 + h)
                P = [(Fr(q2), Fr(q3)), (Fr(q2 + 1), Fr(q3)), (Fr(q2 + 1), Fr(q3 + 1)), (Fr(q2), Fr(q3 + 1))]
                for t in range(4):
                    V = (P[t], P[(t + 1) % 4], c)
                    if max(sum(v) for v in V) <= N:
                        out.append((V, Fr(1, 4)))
        return out

    def crossings(self):
        """affine functions of u (const, coeffs) at which x_1 meets a wall (incl. x_1 = 0 and the top face)."""
        k, N = self.k, self.N
        ex = []
        for m in range(0, 2 * N + 2):
            ex.append((m,) + (0,) * (k - 1))
            for j in range(k - 1):
                e = [m] + [0] * (k - 1); e[1 + j] = -1; ex.append(tuple(e))
            if k == 3:
                ex.append((m, -1, -1))
        return ex

    @staticmethod
    def ev(e, u):
        return e[0] + sum(c * x for c, x in zip(e[1:], u))

    def fibre_at(self, u, exprs):
        """decompose the x_1 fibre over u: list of (orbit, cell key, length expr) ordered by x_1, using the
        combinatorial order at u (u must be generic)."""
        top = (self.N,) + (-1,) * (self.k - 1)
        tv = self.ev(top, u)
        vals = sorted(((self.ev(e, u), e) for e in exprs if 0 <= self.ev(e, u) <= tv))
        for (v1, e1), (v2, e2) in zip(vals, vals[1:]):
            assert v1 != v2, "non-generic point"
        segs = []
        for (v1, e1), (v2, e2) in zip(vals, vals[1:]):
            x = ((v1 + v2) / 2,) + tuple(u)
            key = self.cell_key(x)
            o = self.orbit_of_point(x)
            segs.append((o, key, tuple(a - b for a, b in zip(e2, e1))))
        return segs

    # ---------- assembly ----------
    def assemble(self, verify_frac=1.0, rng=None):
        k = self.k
        exprs = self.crossings()
        UC = self.ucells()
        d = k - 1
        nv = d + 1
        simp = Fr(1, (d + 1) * (d + 2))          # int_T g h = meas*simp*(sum g_i h_i + sum g * sum h)
        A = defaultdict(Fr)                      # orbit -> sum of cell volumes
        Jcells = []                              # (meas, {orbit: [vertex values]})
        Crows = []                               # {orbit: value}
        tot_vol = Fr(0); nverif = 0
        for (V, meas) in UC:
            cen = tuple(sum(v[i] for v in V) / nv for i in range(d))
            segs = self.fibre_at(cen, exprs)
            L = defaultdict(lambda: [Fr(0)] * nv)
            for o, key, le in segs:
                vals = L[o]
                for i, v in enumerate(V):
                    vals[i] += self.ev(le, v)
            # sanity (2): F = 1 marginal is S n - sum u at every vertex
            for i, v in enumerate(V):
                assert sum(L[o][i] for o in L) == self.N - sum(v), "F=1 marginal check failed"
            for o, vals in L.items():
                vol = meas * sum(vals) / nv
                A[o] += vol; tot_vol += vol
            # verify affinity of fibre lengths of every individual cell at a random interior point
            if rng is not None and rng.random() < verify_frac:
                w = [Fr(rng.randint(1, 997)) for _ in range(nv)]; sw = sum(w)
                up = tuple(sum(w[j] * V[j][i] for j in range(nv)) / sw for i in range(d))
                segs2 = self.fibre_at(up, exprs)
                direct = defaultdict(Fr)
                for o, key, le in segs2:
                    direct[key] += self.ev(le, up)
                pred = defaultdict(Fr)
                for o, key, le in segs:
                    pred[key] += self.ev(le, up)
                assert {a: b for a, b in direct.items() if b} == {a: b for a, b in pred.items() if b}, \
                    "fibre length not affine on refined cell"
                nverif += 1
            su = [sum(v) for v in V]
            if max(su) <= self.Aj:
                Jcells.append((meas, dict(L)))
            elif min(su) >= self.Bc:
                for i in range(nv):
                    row = {o: vals[i] for o, vals in L.items() if vals[i] != 0}
                    if row:
                        Crows.append(row)
        vol_expected = Fr(self.N ** k, math.factorial(k))
        assert tot_vol == vol_expected, (tot_vol, vol_expected)
        self.A = dict(A); self.Jcells = Jcells; self.Crows = Crows; self.simp = simp
        return dict(ucells=len(UC), orbits=len(self.orbit_rep), Jcells=len(Jcells), Crows=len(Crows),
                    vol=tot_vol, nverif=nverif)

    def build_B(self):
        """exact J-Gram: B_x = scal * Bint (Bint integer, on J-active orbits); vertex values are in (1/2)Z."""
        act = sorted({o for _, L in self.Jcells for o in L})
        pos = {o: i for i, o in enumerate(act)}
        m = len(act)
        R, C, V = [], [], []
        meas0 = None
        for meas, L in self.Jcells:
            if meas0 is None: meas0 = meas
            assert meas == meas0
            idx = np.array([pos[o] for o in L])
            for o in L:
                assert all((2 * v).denominator == 1 for v in L[o])
            G = np.array([[int(2 * v) for v in L[o]] for o in L], dtype=np.int64)
            s = G.sum(axis=1)
            blk = G @ G.T + np.outer(s, s)
            R.append(np.repeat(idx, len(idx))); C.append(np.tile(idx, len(idx))); V.append(blk.ravel())
        Bint = sp.coo_matrix((np.concatenate(V), (np.concatenate(R), np.concatenate(C))),
                             shape=(m, m), dtype=np.int64).tocsr()   # duplicates summed exactly in int64
        Bint.sum_duplicates()
        assert abs(Bint.data).max() < 2 ** 62
        scal = self.k * meas0 * self.simp / 4    # x-units; factor k for the k marginals
        self.Bact, self.Bint, self.Bscal = act, Bint, scal

    # exact J from coefficients by direct integration over refined cells (independent of Bint)
    def J_exact_direct(self, c):
        J = Fr(0)
        for meas, L in self.Jcells:
            f = [Fr(0)] * (self.k)
            for o, vals in L.items():
                co = c.get(o, 0)
                if co:
                    for i, v in enumerate(vals):
                        f[i] += co * v
            J += meas * self.simp * (sum(x * x for x in f) + sum(f) ** 2)
        return self.k * J

    def I_exact(self, c):
        return sum(co * co * self.A[o] for o, co in c.items())

    def check_constraints(self, c):
        return all(sum(v * c.get(o, 0) for o, v in row.items()) == 0 for row in self.Crows)

    def to_t(self, I, J):
        return I / Fr(self.n) ** self.k, J / Fr(self.n) ** (self.k + 1)


def solve(P, log_prefix=""):
    t0 = time.time()
    act = sorted(set(P.Bact) | {o for r in P.Crows for o in r})
    pos = {o: i for i, o in enumerate(act)}
    m = len(act)
    ccols = sorted({o for r in P.Crows for o in r})
    cpos = {o: i for i, o in enumerate(ccols)}
    nr = len(P.Crows)
    if nr:
        # rows are in (1/2)Z -> multiply by 2, exact integer matrix
        Mq = flint.fmpq_mat(nr, len(ccols))
        for r, row in enumerate(P.Crows):
            for o, v in row.items():
                Mq[r, cpos[o]] = int(2 * v)
        R, rank = Mq.rref()
        pivots = []
        for r in range(rank):
            j = next(j for j in range(len(ccols)) if R[r, j] != 0)
            pivots.append(j)
    else:
        R, rank, pivots = None, 0, []
    pivot_orb = [ccols[j] for j in pivots]
    pset = set(pivot_orb)
    free = [o for o in act if o not in pset]
    fpos = {o: i for i, o in enumerate(free)}
    # exact parametrisation: c_pivot(r) = - sum_{free j in ccols} R[r,j] c_j
    Rdep = []
    for r in range(rank):
        dep = {}
        for j in range(len(ccols)):
            if j == pivots[r]: continue
            x = R[r, j]
            if x != 0:
                dep[ccols[j]] = -Fr(int(x.p), int(x.q))
        Rdep.append(dep)
    t_rref = time.time() - t0
    # float Z (act x free)
    rows, cols, vals = [], [], []
    for o in free:
        rows.append(pos[o]); cols.append(fpos[o]); vals.append(1.0)
    for r, po in enumerate(pivot_orb):
        for o, x in Rdep[r].items():
            rows.append(pos[po]); cols.append(fpos[o]); vals.append(float(x))
    Z = sp.csr_matrix((vals, (rows, cols)), shape=(m, len(free)))
    Afl = np.array([float(P.A[o]) for o in act]) / P.n ** P.k
    bi = np.array([pos[o] for o in P.Bact])
    Bc = P.Bint.tocoo()
    Bfl = sp.csr_matrix((Bc.data.astype(float) * float(P.Bscal) / P.n ** (P.k + 1), (bi[Bc.row], bi[Bc.col])),
                        shape=(m, m))
    Zc = Z.tocsc()
    K = (Zc.T @ Bfl @ Zc).tocsc(); K = (K + K.T) / 2
    M = (Zc.T @ sp.diags(Afl) @ Zc).tocsc(); M = (M + M.T) / 2
    nf = len(free)
    if nf <= 4500:
        lam, vec = sla.eigh(K.toarray(), M.toarray(), subset_by_index=[nf - 1, nf - 1], driver="gvx")
        how = "dense eigh"
    else:
        lu = spla.splu(M)
        Minv = spla.LinearOperator(M.shape, matvec=lu.solve, dtype=float)
        lam, vec = spla.eigsh(K, k=1, M=M, Minv=Minv, which="LA", tol=1e-13, maxiter=20000)
        how = "sparse eigsh"
    lam = float(lam[0]); w = vec[:, 0]
    t_eig = time.time() - t0 - t_rref
    return dict(act=act, free=free, pivot_orb=pivot_orb, Rdep=Rdep, rank=rank, nrows=nr, lam=lam, w=w,
                t_rref=t_rref, t_eig=t_eig, m=m, how=how)


def exact_from_free(P, sol, wq):
    c = dict(wq)
    for r, po in enumerate(sol["pivot_orb"]):
        c[po] = sum((x * c.get(o, 0) for o, x in sol["Rdep"][r].items()), Fr(0))
    c = {o: v for o, v in c.items() if v != 0}
    return c


def J_exact_gram(P, c):
    """c^T B c with the exact integer Gram matrix (common denominator, python ints)."""
    den = 1
    for v in c.values(): den = den * v.denominator // math.gcd(den, v.denominator)
    z = [int(c.get(o, 0) * den) for o in P.Bact]
    Bc = P.Bint.tocoo()
    tot = sum(int(v) * z[i] * z[j] for i, j, v in zip(Bc.row.tolist(), Bc.col.tolist(), Bc.data.tolist())
              if z[i] and z[j])
    return Fr(tot, den * den) * P.Bscal


def round_and_certify(P, sol, dens=(10**2, 10**3, 10**4, 10**5, 10**6, 10**7)):
    w = sol["w"]; w = w / w[np.argmax(np.abs(w))]
    results = []
    for D in dens:
        wq = {o: Fr(int(round(x * D)), D) for o, x in zip(sol["free"], w)}
        c = exact_from_free(P, sol, wq)
        assert P.check_constraints(c)
        Ix = P.I_exact(c); Jx = P.J_exact_direct(c)
        Jg = J_exact_gram(P, c)
        assert Jg == Jx, "exact J mismatch between Gram and direct integration"
        It, Jt = P.to_t(Ix, Jx)
        results.append((D, c, It, Jt, Jt / It))
    return results


def mc_check(P, c, rng, nI=300000, nu=20000, nq=200):
    """Monte Carlo spot check of I and J (in t-units) for coefficient dict c (orbit -> Fraction).
    F is evaluated pointwise from the cell definition; f_1 by a midpoint rule along the fibre.
    Returns (I_mc, I_stderr, J_mc, J_stderr)."""
    cf = {o: float(v) for o, v in c.items()}
    N = P.N; k = P.k
    def Fval(x):
        key = P.canon(P.cell_key(x))
        o = P.orbit_index.get(key)
        return cf.get(o, 0.0) if o is not None else 0.0
    vals = []
    while len(vals) < nI:
        x = [rng.random() * N for _ in range(k)]
        if sum(x) > N: continue
        vals.append(Fval(x) ** 2)
    volx = N ** k / math.factorial(k); sc = volx / P.n ** k
    I_mc = sc * float(np.mean(vals)); I_se = sc * float(np.std(vals)) / math.sqrt(nI)
    vals = []; areaJ = P.Aj ** (k - 1) / math.factorial(k - 1)
    while len(vals) < nu:
        u = [rng.random() * P.Aj for _ in range(k - 1)]
        if sum(u) > P.Aj: continue
        top = N - sum(u); h = top / nq
        f = sum(Fval([(i + 0.5) * h] + u) for i in range(nq)) * h
        vals.append(f * f)
    sc = k * areaJ / P.n ** (k + 1)
    return I_mc, I_se, sc * float(np.mean(vals)), sc * float(np.std(vals)) / math.sqrt(nu)


def cert_checks(P, c, rng, npts=300):
    """independent checks of a candidate: (i) f_1(u) = 0 EXACTLY at random rational u in {B < u1+u2 < S}
    computed from the fibre at u itself (no affine extrapolation); (ii) Monte Carlo I and J (float)."""
    ex = P.crossings(); worst = Fr(0)
    for _ in range(npts):
        while True:
            u = (Fr(rng.randint(0, 10 ** 6), 10 ** 6) * P.N, Fr(rng.randint(0, 10 ** 6), 10 ** 6) * P.N)
            if P.Bc < sum(u) < P.N: break
        f = sum((c.get(o, 0) * P.ev(le, u) for o, key, le in P.fibre_at(u, ex)), Fr(0))
        worst = max(worst, abs(f))
    return worst


def J_pointwise_quadrature(P, c):
    """exact J (x-units) recomputed from f_1 evaluated pointwise (fibre at the point itself) at the interior
    3-point rule (barycentric 2/3,1/6,1/6), exact for quadratics on each refined triangle (k = 3 only)."""
    ex = P.crossings(); J = Fr(0)
    for (V, meas) in P.ucells():
        if max(sum(v) for v in V) > P.Aj: continue
        acc = Fr(0)
        for w in ((Fr(2, 3), Fr(1, 6), Fr(1, 6)), (Fr(1, 6), Fr(2, 3), Fr(1, 6)), (Fr(1, 6), Fr(1, 6), Fr(2, 3))):
            u = tuple(sum(w[j] * V[j][i] for j in range(3)) for i in range(2))
            f = sum((c.get(o, 0) * P.ev(le, u) for o, key, le in P.fibre_at(u, ex)), Fr(0))
            acc += f * f
        J += meas * acc / 3
    return P.k * J


def nonaffine_demo():
    """show that fibre lengths are NOT affine on the unrefined 2D cell {u2,u3 in (0,1), u2+u3 < 1}."""
    P = Problem(3, 4, Fr(1, 4)); ex = P.crossings()   # eps-independent geometry
    # parallelogram P1 + P2 = P3 + P4 inside the triangle, no point on u2 = u3 (generic for the walls)
    pts = [(Fr(1, 10), Fr(3, 10)), (Fr(3, 10), Fr(1, 10)), (Fr(1, 10), Fr(1, 5)), (Fr(3, 10), Fr(1, 5))]
    D = []
    for u in pts:
        dd = defaultdict(Fr)
        for o, key, le in P.fibre_at(u, ex): dd[key] += P.ev(le, u)
        D.append(dd)
    keys = set().union(*D)
    bad = []
    # affine on the triangle => f(P1) + f(P2) = f(P3) + f(P4)
    for key in sorted(keys):
        v = [D[i][key] for i in range(4)]
        if v[0] + v[1] != v[2] + v[3]:
            bad.append((key, [str(x) for x in v]))
    return bad


def k2_test(ns, eps):
    AA, BB = 1 - eps, 1 + eps
    log(f"=== Sanity test (1): k = 2, D = {{x+y <= 2}}, a = {AA}, B = {BB} ===")
    ok = True
    for n in ns:
        t0 = time.time()
        P = Problem(2, n, eps); st = P.assemble(verify_frac=1.0, rng=random.Random(1)); P.build_B()
        sol = solve(P)
        # known extremal: F = 1 on [0,a]^2, 1/2 on the strips [0,a]x(a,B], (a,B]x[0,a], 0 elsewhere
        c = {}
        for o, x in enumerate(P.orbit_pt):
            t = [Fr(v) / n for v in x]
            if max(t) < AA: c[o] = Fr(1)
            elif min(t) < AA and max(t) < BB: c[o] = Fr(1, 2)
        assert P.check_constraints(c)
        It, Jt = P.to_t(P.I_exact(c), P.J_exact_direct(c))
        assert J_exact_gram(P, c) == P.J_exact_direct(c)
        log(f"k=2 n={n}: orbits={st['orbits']} constraint rows={st['Crows']} rank={sol['rank']} free={len(sol['free'])}"
            f"  Heuristic max J/I = {sol['lam']:.12f}   extremal step F: exact I={It}, J={Jt}, J/I={Jt/It}"
            f"   affinity checks={st['nverif']}  ({time.time()-t0:.2f}s)")
        ok &= abs(sol["lam"] - 2) < 1e-9 and Jt / It == 2
    log("k=2 test", "PASSED" if ok else "FAILED")
    return ok


def write_cert(path, P, c, It, Jt, r, D):
    n = P.n
    cells = []
    for o, key in enumerate(P.orbit_rep):
        if o in c:
            cells.append(dict(orbit=o, rep_key=dict(cube=list(key[0]), pair_bits=list(key[1]), level=key[2]),
                              rep_point_scaled=[str(Fr(x)) for x in P.orbit_pt[o]],
                              orbit_volume=str(P.A[o] / Fr(n) ** 3), coef=str(c[o])))
    out = dict(label="Computed (exact certificate)", k=3, eps=str(P.eps), n=n,
               cell_convention="scaled x = n t; cell = {x: floor(x)=cube, [y_i+y_j>1]=pair_bits for pairs "
                               "(0,1),(0,2),(1,2), floor(y1+y2+y3)=level}, y=x-cube; orbit = all permutations;"
                               " F = coef on every cell of the orbit, 0 on orbits not listed",
               rounding_denominator=D, cells=cells, I=str(It), J=str(Jt), ratio=str(r),
               ratio_minus_2=str(r - 2), ratio_float=float(r))
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1)


def main():
    global EPS
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("ns", nargs="*", type=int, default=[4, 8, 12, 16])
    ap.add_argument("--eps", default="1/4", help="eps as p/q (default 1/4)")
    ap.add_argument("--cert-each", action="store_true",
                    help="write code/parity/k3_arrangement_cert_<p>_<q>_n<n>.json for EVERY n whose exact rounded "
                         "ratio exceeds 2 (instead of the legacy k3_arrangement_cert.json, eps = 1/4 only)")
    args = ap.parse_args()
    EPS = Fr(args.eps); ns = args.ns
    assert 0 < EPS < Fr(1, 2)
    for n in ns:
        assert n % 2 == 0 and (n * EPS).denominator == 1, f"n={n}: need n even and n*eps integer"
    n2 = [m for m in (4, 8, 12, 16) if (m * EPS).denominator == 1] or ns[:2]
    T0 = time.time()
    log(f"PM8b Thm 3.14, k=3, eps={EPS}: symmetric F piecewise constant on the {{t_i, t_i+t_j, sum t}} = m/n arrangement")
    if not k2_test(n2, EPS):
        log("k = 2 sanity test failed; aborting"); return
    bad = nonaffine_demo()
    log(f"Geometry check: on the UNREFINED 2D cell (0,1)^2 cap {{u2+u3<1}} (n=4 scaled), {len(bad)} 3D cells have "
        f"non-affine fibre length, e.g. {bad[:2]}  -> the u2-u3 = m lines are needed (refined triangles used).")
    best = None
    for n in ns:
        t0 = time.time()
        P = Problem(3, n, EPS)
        rng = random.Random(n)
        st = P.assemble(verify_frac=1.0 if n <= 8 else 0.2, rng=rng)
        P.build_B()
        t_as = time.time() - t0
        log(f"\n=== k=3 n={n}: refined u-cells={st['ucells']} orbits={st['orbits']} J-cells={st['Jcells']} "
            f"constraint rows={st['Crows']}  assembly {t_as:.1f}s")
        log(f"  sanity (2): total cell volume (t-units) = {st['vol'] / Fr(n)**3} (expected {Fr(3,2)**3/6});"
            f" F=1 marginal = 3/2-u1-u2 at all refined-cell vertices: OK; exact affinity re-checks: {st['nverif']}")
        sol = solve(P)
        log(f"  constraint rank={sol['rank']}  active orbits={sol['m']}  free={len(sol['free'])}"
            f"  rref {sol['t_rref']:.1f}s  eig ({sol['how']}) {sol['t_eig']:.1f}s")
        log(f"  Heuristic: max J/I = {sol['lam']:.12f}")
        if n == ns[0]:
            rr = random.Random(7)
            c = {o: Fr(rr.randint(-20, 20), 10) for o in range(len(P.orbit_rep))}
            It, Jt = P.to_t(P.I_exact(c), P.J_exact_direct(c))
            Imc, Ise, Jmc, Jse = mc_check(P, c, random.Random(11))
            log(f"  sanity (3) Monte Carlo at n={n}, random c (not constrained): exact I={float(It):.6f} MC I={Imc:.6f}+-{Ise:.6f}"
                f" ({(Imc-float(It))/Ise:+.2f} sigma);  exact J={float(Jt):.6f} MC J={Jmc:.6f}+-{Jse:.6f}"
                f" ({(Jmc-float(Jt))/Jse:+.2f} sigma)")
        res = round_and_certify(P, sol)
        for D, c, It, Jt, r in res:
            log(f"  rounded (free-coordinate denominator {D}): exact J/I = {float(r):.15f}  (J/I - 2 = {float(r-2):.3e})"
                f"  constraints exact: OK")
        D, c, It, Jt, r = max(res, key=lambda z: z[4])
        log(f"  best exact rounded ratio at n={n}: {float(r):.15f}  > 2 ? {r > 2}")
        if r > 2:
            worst = cert_checks(P, c, random.Random(100 + n))
            log(f"  candidate check: max |f_1(u)| over 300 random rational u in {{{1+EPS} < u1+u2 < 3/2}} (exact, fibre at u) = {worst}")
            Jq = J_pointwise_quadrature(P, c) / Fr(n) ** 4
            log(f"  candidate check: J from pointwise f_1 + exact interior quadrature == exact J ? {Jq == Jt}")
            if n <= 8:
                Imc, Ise, Jmc, Jse = mc_check(P, c, random.Random(1000 + n))
                log(f"  candidate Monte Carlo: I exact {float(It):.6e} MC {Imc:.6e}+-{Ise:.1e} ({(Imc-float(It))/Ise:+.2f} sigma);"
                    f" J exact {float(Jt):.6e} MC {Jmc:.6e}+-{Jse:.1e} ({(Jmc-float(Jt))/Jse:+.2f} sigma)")
        if r > 2 and args.cert_each:
            Dm, cm, Im, Jm, rm = next(z for z in res if z[4] > 2)
            fn = f"k3_arrangement_cert_{EPS.numerator}_{EPS.denominator}_n{n}.json"
            write_cert(os.path.join(HERE, fn), P, cm, Im, Jm, rm, Dm)
            log(f"  Computed (exact certificate): eps={EPS}, n={n}, rounding denominator {Dm}: exact J/I = {rm} "
                f"= 2 + {rm-2} ({float(rm):.15f}); I = {Im}, J = {Jm}  -> code/parity/{fn}")
        if r > 2 and best is None and not args.cert_each and EPS == Fr(1, 4):
            # certificate = smallest n reaching > 2, with the SMALLEST rounding denominator that still gives > 2
            D, c, It, Jt, r = next(z for z in res if z[4] > 2)
            best = (n, P, c, It, Jt, r, D)
        log(f"  n={n} total {time.time()-t0:.1f}s")
    if best is not None:
        n, P, c, It, Jt, r, D = best
        log(f"\nComputed (exact certificate): n={n}, exact J/I = {r} = {float(r):.15f} > 2 "
            f"(J/I - 2 = {r-2}); I = {It}, J = {Jt}")
        write_cert(os.path.join(HERE, "k3_arrangement_cert.json"), P, c, It, Jt, r, D)
        log("certificate written to code/parity/k3_arrangement_cert.json")
    elif not args.cert_each:
        log("\nNo exact certificate written (none reached J/I > 2, or eps != 1/4 without --cert-each).")
    log(f"total runtime {time.time()-T0:.1f}s")


if __name__ == "__main__":
    main()
