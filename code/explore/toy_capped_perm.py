#!/usr/bin/env python3
"""Exploration (heuristic, floating point; Session 12): toy capped problem at k = 3 with PER-m caps.
Region T = {t >= 0, t1+t2+t3 <= 1, t_i <= c1, t_i + t_j <= c2}.  Same quantities as toy_capped.py
(opt_free, trunc, opt_T, regain = (opt_T - trunc)/(opt_free - trunc)), symmetric polynomials of degree <= d.
Question (from Session 11's toy, notes/explorations.md): is a large regain caused by caps on SUMS of several
coordinates (m >= 2) rather than by caps on single coordinates?"""
import sys, itertools, numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from toy_capped import poly_quad, monos, symmetrise, best

def grams3(d, c1, c2, order):
    k = 3; ms = monos(k, d); E = np.array(ms)
    pairs = [(0, 1), (0, 2), (1, 2)]
    A = [-np.eye(3), np.ones((1, 3)), np.eye(3)]; b = [np.zeros(3), [1.0], c1 * np.ones(3)]
    for (i, j) in pairs:
        r = np.zeros((1, 3)); r[0, i] = r[0, j] = 1; A.append(r); b.append([c2])
    P, W = poly_quad(np.vstack(A), np.concatenate(b), order)
    Phi = np.prod(P[:, None, :] ** E[None, :, :], axis=2)
    GI = Phi.T @ (W[:, None] * Phi)
    # fibre in t1 over y = (t2, t3): U(y) = min(c1, 1 - y2 - y3, c2 - y2, c2 - y3), need U >= 0, y in T's projection
    lin = [(np.zeros(2), c1), (-np.ones(2), 1.0), (np.array([-1.0, 0]), c2), (np.array([0, -1.0]), c2)]
    GJ = np.zeros_like(GI)
    for a, (ga, ca) in enumerate(lin):           # region where U = ga.y + ca is the minimum (ties: lowest index)
        A2 = [-np.eye(2), np.eye(2), np.ones((1, 2)), np.ones((1, 2)), -ga[None, :]]
        b2 = [np.zeros(2), c1 * np.ones(2), [1.0], [c2], [ca]]         # y_i <= c1, sum y <= 1, y2+y3 <= c2, U >= 0
        for bb, (gb, cbv) in enumerate(lin):
            if bb == a: continue
            A2.append((ga - gb)[None, :]); b2.append([cbv - ca])      # ga.y + ca <= gb.y + cb
        Y, Wy = poly_quad(np.vstack(A2), np.concatenate(b2), order)
        if len(Wy) == 0: continue
        U = Y @ ga + ca
        a1 = E[:, 0]; rest = E[:, 1:]
        Psi = (U[:, None] ** (a1[None, :] + 1) / (a1[None, :] + 1)) * np.prod(Y[:, None, :] ** rest[None, :, :], axis=2)
        GJ += Psi.T @ (Wy[:, None] * Psi)
    return ms, *symmetrise(ms, GI, GJ)

def run(d, caps, order=None):
    order = order or (d + 3)
    ms, GI1, GJ1 = grams3(d, 1.0, 1.0, order)
    r_free, v = best(GI1, GJ1)
    for (c1, c2) in caps:
        _, GI, GJ = grams3(d, c1, c2, order)
        trunc = (v @ GJ @ v) / (v @ GI @ v); r_T, _ = best(GI, GJ)
        reg = (r_T - trunc) / (r_free - trunc)
        print("k=3 d=%d c1=%.3f c2=%.3f  free %.6f  trunc %.6f  opt_T %.6f  loss %.2e  regain %.3f"
              % (d, c1, c2, 3 * r_free, 3 * trunc, 3 * r_T, 3 * (r_free - trunc), reg), flush=True)

if __name__ == "__main__":
    d = int(sys.argv[1])
    caps = [tuple(float(x) for x in s.split("/")) for s in sys.argv[2].split(",")]
    run(d, caps)
