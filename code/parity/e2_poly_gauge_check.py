#!/usr/bin/env python3
"""Second program for the Session 36 parity attempt (route card 2026-11-19-e2-polynomial-gauge.md).

Independent exact check of the blocking certificates written by e2_poly_gauge.py (no sympy, no LP):
  1. every event identity  cx * prod(xv) + s d = cy * prod(yv)  holds identically (checked on a 5x5x5 integer grid,
     which is exact: every polynomial involved has degree <= 2 in each variable, so a nonzero difference cannot vanish
     on 5 points per variable), and the stored x-side expression equals cx * prod(xv);
  2. multipliers are 1 or prime, the required signs match the E2 shapes, and every vertex is odd at m0;
  3. the certificate S (a list of sign vectors on the vertices) is nonempty, no vector in S meets any event (meets =
     agrees with the required sign on every vertex of the event), and on S every vertex takes +1 and -1 equally often.
Then the uniform measure on S is a fair, target-free distribution: the system is blocked.
Usage: /usr/bin/python3 -I code/parity/e2_poly_gauge_check.py [cert.json]
"""
import sys, json, itertools

def isprime(n):
    return n > 1 and all(n % p for p in range(2, int(n ** 0.5) + 1))

def ev(expr, pt):
    m, u, w = pt
    return eval(expr, {'__builtins__': {}}, {'m': m, 'u': u, 'w': w})

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else 'code/parity/e2_poly_gauge_cert.json'
    certs = json.load(open(path))['certs']
    grid = list(itertools.product(range(-2, 3), repeat=3))
    nev = 0
    bydmod = {}
    for c in certs:
        d, V, S = c['d'], c['V'], c['S']
        assert d % 4 != 0
        idx = {v: i for i, v in enumerate(V)}
        for v in V:
            assert ev(v, c['m0']) % 2 != 0, ('vertex even at m0', v)
        reqs = []
        for e in c['events']:
            nev += 1
            for cm, side in ((e['cx'], e['xv']), (e['cy'], e['yv'])):
                assert cm == 1 or isprime(cm)
                sg = [t[1] for t in side]
                assert (cm == 1 and sg in ([1], [-1, -1])) or (cm > 1 and sg == [-1]), (cm, sg)
            for pt in grid:
                px = e['cx']
                for v, _ in e['xv']:
                    px *= ev(v, pt)
                py = e['cy']
                for v, _ in e['yv']:
                    py *= ev(v, pt)
                assert px + e['s'] * d == py, ('identity fails', e)
                assert ev(e['X'], pt) == px
            r = {}
            for v, sg in e['xv'] + e['yv']:
                if v in r and r[v] != sg:
                    r = None; break
                r[v] = sg
            if r is not None:
                reqs.append([(idx[v], sg) for v, sg in r.items()])
        assert S, 'empty certificate'
        for sv in S:
            assert len(sv) == len(V)
            assert not any(all(sv[i] == sg for i, sg in rq) for rq in reqs), 'certificate meets an event'
        for i in range(len(V)):
            assert 2 * sum(1 for sv in S if sv[i] == 1) == len(S), 'unbalanced coordinate'
        bydmod[d] = bydmod.get(d, 0) + 1
    print(f"verified {len(certs)} blocking certificates ({nev} events); systems per d: {bydmod}")
    print("ALL CHECKS PASSED")

if __name__ == '__main__':
    main()
