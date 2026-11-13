#!/usr/bin/env python3
r"""capped_gram.py -- Gram matrices of the capped functionals I_T, J_T (adjoint of capped_check.py),
and optimisation of the test function P on the capped support T itself.

usage:  python3 code/capped_gram.py P_u.json [--procs 4] [--out P_opt_u.json] [--bits 256]
                                    [--sigma 4.3] [--gram out.gram.json]

Idea.  capped_check.py computes I_T(P) and J_T(P) as LINEAR functionals of the coefficient
products  kapI[F](y) = sum p_{F1}(y) p_{F2}(y)  and  kapJ[F](y,v) = sum q_{F1} q_{F2}  (F = F1 + F2),
followed by a long chain of exact linear maps (eta -> bundle -> contractions with the
geometric series A, B and the kernels K).  Running that chain backwards (reverse mode)
gives exact weight vectors
        wI[F][alpha]   = d I_T / d kapI[F][y^alpha],
        wJ[F][(b,g)]   = d J_T / d kapJ[F][y^b v^g],
at the cost of about one forward evaluation.  Then
        I_T(c) = c^T GI c,   GI[t1,t2] = wI[F1+F2][a1+a2]                 (exact),
        J_T(c) = c^T GJ c,   GJ = Q^T H Q,  H[(i1,b1,g1),(i2,b2,g2)] = wJ[i1+i2][(b1+b2,g1+g2)],
where Q maps basis terms to the coefficients of q_F(y,v) = int_0^v P dt.
SELF-TEST (exact): for the input vector c0,  sum <kapI, wI> == I_T(c0)  and  sum <kapJ, wJ> == J_T(c0),
both compared with capped_check's own forward value computed in the same run.
GI is exact; GJ is assembled in fixed point with 2^-PREC absolute accuracy (only used to FIND a
vector; the found vector is then rounded and certified by the exact evaluators
capped_check.py and capped_exact.py, never by these matrices).
"""
import sys, os, json, time, argparse, itertools, math
from math import comb, factorial
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import capped_check as cc
from flint import fmpq, fmpz, fmpq_poly, fmpz_poly, fmpz_mat, fmpq_mat, arb_mat, arb
import flint

toq = cc.toq


# ------------------------------------------------------------------------------------------------
def group_adjoint(pb, r, nZ, todo, wI_comb, wJ_comb):
    """Reverse-mode derivative of  sum_{(kind,m) in todo} weight * value(kind,m,r)  with respect to
    the bundle etaP[F][n] and the rect matrices etaII[F][l,e].  Returns (Gb, GII):
       Gb[F]  : list of fmpq of length 3*SA      (d/d etaP[F][n])
       GII[F] : fmpq_mat nn x nn or None         (d/d etaII[F][l,e], etaII unscaled by DII)"""
    ix = pb.ix
    N = len(ix)
    k, L, g, delta = pb.k, pb.L, pb.g, pb.delta
    SA, LM, W = pb.SA, pb.LM, pb.W
    Bser = pb.Bseries(r, nZ)
    Bz, DB = cc.to_int(Bser)
    nmax = k + 4 * W + 20
    maxdegB = max((b.degree() for b in Bz if not b.is_zero()), default=0)
    NMAX = 3 * SA + maxdegB + 2
    amax = W + 2
    # --- base part: Kt_{F'}[n] = sum_m weight_m sum_a A^m_{F'}[a] Kseg_m(a, n)
    prods = []     # list of (fmpz_mat N x NMAX, rational scale)
    rect_jobs = []
    for kind, m in todo:
        Az, DA = pb.phipowz[m]
        Kmat = [[fmpq(0)] * NMAX for _ in range(amax + 1)]
        Lp = L - (m + r) * g
        if kind == "I":
            wgt = wI_comb(m, r)
            nR = k - m
            s1 = pb.cap(m) - m * g if m >= 1 else fmpq(0)
            K = pb.Kern(Lp, fmpq(0), s1, True, nmax)
            for a in range(amax + 1):
                for n in range(min(SA, NMAX)):
                    Kmat[a][n] = K(m - 1 + a, nR + n)
        else:
            wgt = wJ_comb(m, r)
            nR = k - 1 - m
            c1 = pb.cap(m) - m * g if m >= 1 else None
            c2 = pb.cap(m + 1) - m * g
            Lam = Lp - delta
            s1 = c1 if m >= 1 else fmpq(0)
            K = pb.Kern(Lam, fmpq(0), s1, True, nmax)
            for a in range(amax + 1):
                for n in range(SA, min(2 * SA, NMAX)):
                    Kmat[a][n] = K(m - 1 + a, nR + n - SA)
            Lam = Lp - g
            if Lam > 0:
                s0 = c2 - g
                K = pb.Kern(Lam, s0, s1, (c2 - g < 0), nmax)
                for a in range(amax + 1):
                    for n in range(2 * SA, NMAX):
                        Kmat[a][n] = K(m - 1 + a, nR + n - 2 * SA)
            Sig = Lp - c2
            if Sig > 0 and c2 - g >= 0:
                rect_jobs.append((m, wgt, Lp, nR, c1, c2, Sig))
        DK = 1
        for row in Kmat:
            for v in row:
                if v != 0: DK = math.lcm(DK, int(v.q))
        Kz = fmpz_mat(amax + 1, NMAX, [int(v * DK) for row in Kmat for v in row])
        Am = fmpz_mat(N, amax + 1)
        for i1 in range(N):
            for a, ca in enumerate(Az[i1].coeffs()):
                Am[i1, a] = ca
        prods.append((Am * Kz, fmpq(wgt) / (DA * DK)))
    D = 1
    for _, sc in prods: D = math.lcm(D, int(sc.q))
    Kt = None
    for P, sc in prods:
        f = sc * D
        assert f.q == 1
        term = P * fmpz(int(f.p))
        Kt = term if Kt is None else Kt + term
    # reversed rows as integer polys: Rv_{F'}(x) = sum_n Kt[n] x^{NMAX-1-n}
    Rv = []
    for i1 in range(N):
        row = [Kt[i1, NMAX - 1 - e] for e in range(NMAX)]
        Rv.append(fmpz_poly(row))
    Gacc = [fmpz_poly() for _ in range(N)]
    for i1 in range(N):
        rv = Rv[i1]
        if rv.is_zero(): continue
        for i2, isum in ix.pairs[i1]:
            b = Bz[i2]
            if b.is_zero(): continue
            Gacc[isum] += b * rv
    den = DB * D
    Gb = []
    for F in range(N):
        cs = Gacc[F].coeffs()
        out = []
        for p in range(3 * SA):
            e = NMAX - 1 - p
            out.append(fmpq(cs[e], 1) / den if 0 <= e < len(cs) else fmpq(0))
        Gb.append(out)
    # --- rect part
    GII = [None] * N
    for (m, wgt, Lp, nR, c1, c2, Sig) in rect_jobs:
        A = pb.phipow[m]
        s1 = (min(c1, c2 - g) if m >= 1 else fmpq(0))
        H = 2 * LM + 2
        hz, Dh = cc.to_int([fmpq_poly([cc.efac(Sig, nR + H - t) if nR + H - t >= 0 else 0
                                       for t in range(H + 1)])])
        hz = hz[0]
        Btl = []
        for i2 in range(N):
            b = Bz[i2]
            if b.is_zero():
                Btl.append([]); continue
            prod = (b * hz).coeffs()
            nF = W + 2 - ix.wt[i2]
            Btl.append([int(prod[H - l]) if H - l < len(prod) else 0 for l in range(nF + 1)])
            # trailing zeros are kept (forward strips them via fmpz_poly; padding below is equivalent)
        K = pb.Kern(c2, fmpq(0), s1, True, nmax)
        Kmat = fmpq_mat(amax + 1, LM + 1, [factorial(e) * K(m - 1 + a, e)
                                           for a in range(amax + 1) for e in range(LM + 1)])
        Amat = fmpq_mat(N, amax + 1)
        for i1 in range(N):
            for a, ca in enumerate(A[i1].coeffs()):
                Amat[i1, a] = ca
        AK = Amat * Kmat
        AKl = [[AK[i, e] for e in range(W + 3 - ix.wt[i])] for i in range(N)]
        DAK = 1
        for row in AKl:
            for v in row: DAK = math.lcm(DAK, int(v.q))
        AKz = [[int(v * DAK) for v in row] for row in AKl]
        scale = fmpq(wgt) / (DB * Dh * DAK)
        for i in range(N):
            if pb.etaIIm[0][i] is None: continue
            nn = W + 3 - ix.wt[i]
            r1, r2 = [], []
            for i1, i2 in ix.bysum[i]:
                bt = Btl[i2]
                if not bt or not any(bt): continue
                r1.extend(bt[:nn] + [0] * (nn - min(nn, len(bt))))
                r2.extend(AKz[i1][:nn])
            if not r1: continue
            p = len(r1) // nn
            M1 = fmpz_mat(p, nn, r1)
            M2 = fmpz_mat(p, nn, r2)
            Z = fmpq_mat(M1.transpose() * M2) * scale
            GII[i] = Z if GII[i] is None else GII[i] + Z
    return Gb, GII


def chain_to_kap(pb, Gb, GII):
    """bundle/rect gradients -> wI[F] (dict alpha -> fmpq), wJ[F] (dict (b,gm) -> fmpq)."""
    ix = pb.ix
    N = len(ix)
    SA, LM, W, g, delta = pb.SA, pb.LM, pb.W, pb.g, pb.delta
    fl = [factorial(n) for n in range(2 * LM + 4)]
    C = [[fmpq(fl[b], fl[b - l]) for l in range(b + 1)] for b in range(LM + 1)]
    dpow = [delta ** n for n in range(LM + 2)]
    gpow = [g ** n for n in range(LM + 2)]
    wI, wJ = [], []
    for i in range(N):
        Ff = ix.fact[i]
        gb = Gb[i]
        wI.append({al: gb[al] * fl[al] * Ff for al in range(SA) if gb[al] != 0})
        G2 = GII[i]
        nn = W + 3 - ix.wt[i]
        Bmax = min(LM, LM - ix.wt[i] + 2)
        gd = gb[SA:2 * SA]; gg = gb[2 * SA:3 * SA]
        ED = [sum((gd[l] * C[B][l] * dpow[B - l] for l in range(B + 1) if gd[l] != 0), fmpq(0)) for B in range(Bmax + 1)]
        EG = [sum((gg[l] * C[B][l] * gpow[B - l] for l in range(B + 1) if gg[l] != 0), fmpq(0)) for B in range(Bmax + 1)]
        if G2 is not None:
            R2 = [sum((G2[l, B - l] * C[B][l] for l in range(B + 1) if l < nn and B - l < nn), fmpq(0)) for B in range(Bmax + 1)]
        d = {}
        for B in range(Bmax + 1):
            base = ED[B] - EG[B] - (R2[B] if G2 is not None else 0)
            for gm in range(B + 1):
                b = B - gm
                v = base + gpow[gm] * EG[b]
                if G2 is not None:
                    for l in range(b + 1):
                        e = b - l + gm
                        if l < nn and e < nn: v += G2[l, e] * C[b][l]
                if v != 0: d[(b, gm)] = v * Ff
        wJ.append(d)
    return wI, wJ


_PB = None


def _worker(tasks):
    t0 = time.time()
    k = _PB.k
    N = len(_PB.ix)
    wIc = lambda m, r: comb(k, m) * (-1) ** r * comb(k - m, r)
    wJc = lambda m, r: comb(k - 1, m) * (-1) ** r * comb(k - 1 - m, r)
    GbT = [[fmpq(0)] * (3 * _PB.SA) for _ in range(N)]
    GIIT = [None] * N
    for (r, nZ, todo) in tasks:
        t1 = time.time()
        Gb, GII = group_adjoint(_PB, r, nZ, todo, wIc, wJc)
        for i in range(N):
            row, acc = Gb[i], GbT[i]
            for p, v in enumerate(row):
                if v != 0: acc[p] += v
            if GII[i] is not None:
                GIIT[i] = GII[i] if GIIT[i] is None else GIIT[i] + GII[i]
        print("    group r=%d nZ=%d (%d jobs): %.1fs" % (r, nZ, len(todo), time.time() - t1), flush=True)
    wI, wJ = chain_to_kap(_PB, GbT, GIIT)
    s_I = [{a: (int(v.p), int(v.q)) for a, v in d.items()} for d in wI]
    s_J = [{bg: (int(v.p), int(v.q)) for bg, v in d.items()} for d in wJ]
    return s_I, s_J, time.time() - t0


def weights(data, procs=1, log=print):
    global _PB
    pb = cc.Problem(data)
    pb.prepare(log=log)
    cmb = pb.combos()
    pb.prepare_powers(cmb, log=log)
    groups = {}
    for kind, m, r, nZ in cmb:
        groups.setdefault((r, nZ), []).append((kind, m))
    tasks = sorted([(r, nZ, todo) for (r, nZ), todo in groups.items()], key=lambda t: -len(t[2]))
    _PB = pb
    N = len(pb.ix)
    WI = [dict() for _ in range(N)]
    WJ = [dict() for _ in range(N)]
    t0 = time.time()
    nb = max(1, procs)
    chunks = [[] for _ in range(nb)]
    load = [0] * nb
    for t in tasks:
        j = load.index(min(load)); chunks[j].append(t); load[j] += len(t[2])

    def absorb(sI, sJ):
        for i in range(N):
            for a, (p, q) in sI[i].items():
                WI[i][a] = WI[i].get(a, fmpq(0)) + fmpq(p, q)
            for bg, (p, q) in sJ[i].items():
                WJ[i][bg] = WJ[i].get(bg, fmpq(0)) + fmpq(p, q)
    if nb > 1:
        import multiprocessing as mp
        with mp.get_context("fork").Pool(nb) as pool:
            for sI, sJ, dt in pool.imap_unordered(_worker, chunks):
                absorb(sI, sJ)
                log("  adjoint chunk done: %.1fs (elapsed %.1fs)" % (dt, time.time() - t0))
    else:
        sI, sJ, dt = _worker(chunks[0]); absorb(sI, sJ)
    return pb, WI, WJ


def self_test(pb, WI, WJ):
    """exact <kap, w> for the input vector (kapI from pb.prepare; kapJ rebuilt the same way)."""
    ix = pb.ix
    # rebuild kapI, kapJ exactly as capped_check.prepare does
    pF = {}
    for a, F, c in pb.terms:
        i = ix.pos[F]
        pF[i] = pF.get(i, fmpq_poly()) + fmpq_poly([0] * a + [c])
    IT = fmpq(0)
    keys = sorted(pF)
    kapI = {}
    for i1 in keys:
        for i2 in keys:
            isum = ix.pos[tuple(x + y for x, y in zip(ix.idx[i1], ix.idx[i2]))]
            kapI[isum] = kapI.get(isum, fmpq_poly()) + pF[i1] * pF[i2]
    for i, p in kapI.items():
        for al, v in enumerate(p.coeffs()):
            if v != 0: IT += v * WI[i].get(al, fmpq(0))
    qF = build_q(pb, [c for a, F, c in pb.terms])
    JT = fmpq(0)
    keys = sorted(qF)
    for i1 in keys:
        for i2 in keys:
            isum = ix.pos[tuple(x + y for x, y in zip(ix.idx[i1], ix.idx[i2]))]
            for (b1, g1), v1 in qF[i1].items():
                for (b2, g2), v2 in qF[i2].items():
                    w = WJ[isum].get((b1 + b2, g1 + g2))
                    if w is not None: JT += v1 * v2 * w
    return IT, JT


def term_q(pb, a, F):
    """rows of Q for one basis term: dict (rest_index, b, gm) -> fmpq."""
    ix = pb.ix
    out = {}
    for e in itertools.product(*[range(x + 1) for x in F]):
        mult = 1
        for x, y in zip(F, e): mult *= comb(x, y)
        Wd = sum(j * x for j, x in zip(pb.parts, e))
        rest = ix.pos[tuple(x - y for x, y in zip(F, e))]
        for q in range(a + 1):
            key = (rest, a - q, Wd + q + 1)
            out[key] = out.get(key, fmpq(0)) + fmpq((-1) ** q * comb(a, q) * mult, Wd + q + 1)
    return out


def build_q(pb, coeffs):
    qF = {}
    for (a, F, _), c in zip(pb.terms, coeffs):
        for (i, b, gm), v in term_q(pb, a, F).items():
            d = qF.setdefault(i, {})
            d[(b, gm)] = d.get((b, gm), fmpq(0)) + v * c
    return qF


def gram(pb, WI, WJ, basis_terms, PREC, log=print):
    """GI exact (fmpq_mat), GJ in fixed point (python ints / 2^PREC, times 1/LQ^2) -> arb_mat."""
    ix = pb.ix
    n = len(basis_terms)
    t0 = time.time()
    GI = fmpq_mat(n, n)
    for x, (a1, F1) in enumerate(basis_terms):
        for y in range(x, n):
            a2, F2 = basis_terms[y]
            v = WI[ix.pos[tuple(p + q for p, q in zip(F1, F2))]].get(a1 + a2, fmpq(0))
            GI[x, y] = v; GI[y, x] = v
    log("GI built: %.1fs" % (time.time() - t0))
    # Q columns
    cols = [term_q(pb, a, F) for a, F in basis_terms]
    LQ = 1
    for col in cols:
        for v in col.values(): LQ = math.lcm(LQ, int(v.q))
    rows = sorted({key for col in cols for key in col})
    rpos = {key: t for t, key in enumerate(rows)}
    colsI = [[(rpos[key], int(v * LQ)) for key, v in col.items()] for col in cols]
    log("Q: %d rows, %d nonzeros, LQ=%d" % (len(rows), sum(len(c) for c in colsI), LQ))
    # fixed-point table of wJ: Hfix[s][(b,gm)]
    S = 2 ** PREC
    Hfix = [{bg: (v.p * S) // v.q for bg, v in d.items()} for d in WJ]
    rest_vec = [ix.idx[i] for i, _, _ in rows]
    sumpos = {}
    # HQ[r1][t2] = sum_{r2 in col t2} H[r1,r2] Q[r2,t2]
    HQ = [[0] * n for _ in rows]
    for r1, (i1, b1, g1) in enumerate(rows):
        f1 = ix.idx[i1]
        row = HQ[r1]
        for t2, col in enumerate(colsI):
            acc = 0
            for r2, qv in col:
                i2, b2, g2 = rows[r2]
                key = (i1, i2)
                s = sumpos.get(key)
                if s is None:
                    s = ix.pos[tuple(p + q for p, q in zip(f1, ix.idx[i2]))]
                    sumpos[key] = s
                h = Hfix[s].get((b1 + b2, g1 + g2))
                if h: acc += h * qv
            row[t2] = acc
        if r1 % 500 == 0: log("  HQ row %d/%d (%.0fs)" % (r1, len(rows), time.time() - t0))
    GJint = [[0] * n for _ in range(n)]
    for t1, col in enumerate(colsI):
        for t2 in range(n):
            acc = 0
            for r1, qv in col: acc += qv * HQ[r1][t2]
            GJint[t1][t2] = acc
    log("GJ built: %.1fs" % (time.time() - t0))
    colabs = [sum(abs(qv) for _, qv in col) for col in colsI]
    return GI, GJint, LQ, colabs


def is_pd(M):
    """rigorous: True only if the symmetric ball matrix M is certainly positive definite
    (recursive Schur complements in ball arithmetic: M > 0 iff M11 > 0 and M22 - M21 M11^{-1} M12 > 0)."""
    n = M.nrows()
    if n == 1:
        return M[0, 0] > 0
    h = n // 2
    M11 = arb_mat(h, h, [M[i, j] for i in range(h) for j in range(h)])
    if not is_pd(M11):
        return False
    M12 = arb_mat(h, n - h, [M[i, j] for i in range(h) for j in range(h, n)])
    M22 = arb_mat(n - h, n - h, [M[i, j] for i in range(h, n) for j in range(h, n)])
    X = M11.solve(M12)                       # rigorous enclosure (raises if M11 not certainly invertible)
    S = M22 - M12.transpose() * X
    # symmetrise the enclosure (S is symmetric in exact arithmetic): take the union of S and S^T
    S = arb_mat(n - h, n - h, [S[i, j].union(S[j, i]) for i in range(n - h) for j in range(n - h)])
    return is_pd(S)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pjson")
    ap.add_argument("--procs", type=int, default=1)
    ap.add_argument("--out")
    ap.add_argument("--prec", type=int, default=6000)
    ap.add_argument("--bits", type=int, default=0, help="round the found vector to this many bits (0: dyadic midpoints)")
    ap.add_argument("--sigma", type=float, default=4.3)
    ap.add_argument("--check", help="capped_check result json for the input vector (exact I_T, J_T)")
    ap.add_argument("--weights_only", action="store_true")
    ap.add_argument("--save", help="pickle the exact weights wI, wJ here")
    ap.add_argument("--load", help="load exact weights instead of running the adjoint")
    ap.add_argument("--ceiling", type=str, default="", help="comma-separated sigmas: certify sigma*GI - k*GJ > 0")
    a = ap.parse_args()
    log = lambda *x: print(*x, flush=True)
    data = json.load(open(a.pjson))
    t0 = time.time()
    import pickle
    if a.load:
        pb = cc.Problem(data); pb.prepare(log=log)
        WIr, WJr = pickle.load(open(a.load, "rb"))
        WI = [{al: fmpq(p, q) for al, (p, q) in d.items()} for d in WIr]
        WJ = [{bg: fmpq(p, q) for bg, (p, q) in d.items()} for d in WJr]
        log("weights loaded from %s" % a.load)
    else:
        pb, WI, WJ = weights(data, procs=a.procs, log=log)
        log("adjoint done: %.1fs" % (time.time() - t0))
        if a.save:
            pickle.dump(([{al: (int(v.p), int(v.q)) for al, v in d.items()} for d in WI],
                         [{bg: (int(v.p), int(v.q)) for bg, v in d.items()} for d in WJ]), open(a.save, "wb"))
            log("weights saved to %s" % a.save)
    IT, JT = self_test(pb, WI, WJ)
    log("self-test from weights: I_T=%.15e J_T=%.15e ratio=%.12f" % (cc.fq(IT), cc.fq(JT), cc.fq(pb.k * JT / IT)))
    if a.check:
        chk = json.load(open(a.check))
        okI = IT == toq(chk["I_T"]); okJ = JT == toq(chk["J_T"])
        log("EXACT agreement with %s: I_T %s, J_T %s" % (a.check, okI, okJ))
        if not (okI and okJ): sys.exit("self-test FAILED")
    if a.weights_only: return
    basis_terms = [(a_, F) for a_, F, c in pb.terms]
    # note: pb.terms drops zero coefficients; use the full basis of the input file instead
    full = []
    for (a_, b) in data["basis"]:
        bb = list(b) + [0] * max(0, pb.parts[-1] - 1 - len(b))
        full.append((int(a_), tuple(bb[j - 2] for j in pb.parts)))
    basis_terms = full
    GI, GJint, LQ, colabs = gram(pb, WI, WJ, basis_terms, a.prec, log=log)
    n = len(basis_terms)
    flint.ctx.prec = a.prec - 200
    scale = arb(fmpq(1, LQ * LQ)) * arb(2) ** (-a.prec)
    A = arb_mat(GI)
    B = arb_mat(n, n, [arb(GJint[i][j]) for i in range(n) for j in range(n)]) * scale * pb.k
    c0 = arb_mat(n, 1, [toq(x) for x in data["coeffs"]])
    r0 = ((c0.transpose() * B * c0)[0, 0] / (c0.transpose() * A * c0)[0, 0]).mid()
    log("Gram check: ratio of input vector from Gram = %s" % r0.str(15))
    if a.ceiling:
        # rigorous: B_true = k GJ_true, |GJint/(LQ^2 2^P) - GJ_true|[t1,t2] <= colabs[t1] colabs[t2] / (LQ^2 2^P)
        Brig = arb_mat(n, n, [arb(GJint[i][j], colabs[i] * colabs[j] + 1) for i in range(n) for j in range(n)]) * scale * pb.k
        for sg in a.ceiling.split(","):
            ok = is_pd(A * arb(fmpq(*map(int, sg.split("/")))) - Brig)
            log("CEILING sigma=%s: sigma*I_T - k*J_T positive definite on the whole test space: %s" % (sg, ok))
    C = (B - A * arb(a.sigma)).solve(A, algorithm="approx").mid()
    v = c0
    lam = None
    for it in range(600):
        x = (C * v).mid()
        nrm = max(abs(x[i, 0].mid()) for i in range(n))
        v = x * (1 / nrm)
        if it % 5 == 4:
            new = ((v.transpose() * B * v)[0, 0] / (v.transpose() * A * v)[0, 0]).mid()
            log("  iter %d: %s" % (it, new.str(15)))
            if lam is not None and abs(new - lam) < arb("1e-14"): break
            lam = new
    # round
    ent = []
    for i in range(n):
        man, ex = v[i, 0].mid().man_exp()
        man, ex = int(man), int(ex)
        if a.bits and man != 0:
            sh = max(0, man.bit_length() - a.bits)
            man = (man >> sh) if man > 0 else -((-man) >> sh); ex += sh
        ent.append(fmpq(man) * fmpq(2) ** ex if ex >= 0 else fmpq(man, fmpz(2) ** (-ex)))
    q = arb_mat(n, 1, ent)
    rq = ((q.transpose() * B * q)[0, 0] / (q.transpose() * A * q)[0, 0]).mid()
    log("rounded vector, ratio from Gram (not a certificate): %s" % rq.str(15))
    if a.out:
        out = dict(data)
        out["coeffs"] = [str(e) for e in ent]
        out["source"] = "capped_gram.py optimum on the capped support, from " + a.pjson
        out["gram_ratio"] = rq.str(15)
        json.dump(out, open(a.out, "w"))
        log("wrote", a.out)
    log("total %.1fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
