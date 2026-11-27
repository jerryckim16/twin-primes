#!/usr/bin/python3
"""Exact toy checks for LWW (arXiv:2610.20242v2), the reduction Q_Y - Q_Y^maj -> (4.52), pp. 16-18, 23-27.

Run: /usr/bin/python3 -I code/parity/lww_p23_27_check.py
Route card: notes/parity-attempts/2026-11-27-lww-p23-27-reduction.md

What is checked (toy parameters; finite identities only, nothing analytic):
 (A) Lemma 4.1 counting step (4.11): #{(a,b): Y<=a,b<=4Y, (a,b)>1} <= sum_p floor(4Y/p)^2, a, b products
     of one prime from each of K disjoint toy sets.                                   exact integers
 (B) (4.12) equivalence: for gcd(a,b)=1, (mn+2)/a = (rs+2)/b in N*  <=>  bmn - ars = 2(a-b);
     and the p. 17 psi_{-2} insertion: a,b in [Y,4Y] => |(b-a)/Y| <= 3 <= 4.            exact integers
 (C) the p. 24 claims on an exhaustive toy: for every term with nonzero summand (coprime a,b,
     |t| < 16Y < Z), t != 0, gcd(Dbm,s) = gcd(Dar,n) = 1, G(P1) = Db, G(Q1) = Da,
     conj f(P) f(Q) = alpha_m conj(alpha_r) beta_n conj(beta_s), rho-exponent = 0.  exact ints + complex
 (D) the full chain (4.38) -> (4.44) -> (4.46) -> (4.48) as an EXACT identity in a toy:
       Q_Y - Q_Y^maj - sum_{d0} B_{d0}/d0
         = prod V^{-2} [ sum_{gcd(a,b)=1} (1 - w(a,b)) D(a,b) + sum_{gcd(a,b)>1} D_full(a,b) ],
     with B_{d0} = <f, T^C_{-2} f> computed literally from states (P,p) in S(d0), the operator (4.38)
     (with a generic complex toy kernel c2 in place of the M_{-2} integral) and the inner product (4.21);
     Q_Y from the first line of (4.7); Q^maj from (4.14); w(a,b) by brute force.     complex floats
 (E) w(a,b) <= 1 and the p. 26 bound on 1 - w(a,b) (K = 2 toy); the (4.51) count
     #{l : |bk - al| < 16Y} <= 33 (and symmetrically in k).                    exact Fractions / ints
 (F) meas M_{-2} = meas M_1 <= 4 L^{3A0}/Y (used for |H_{-2}| << L^{O(1)} Y^{-1}).      exact Fractions
Negative controls are marked NEG and must FAIL.
"""
import math, random, time, itertools, cmath
from fractions import Fraction as Fr

T0 = time.time()
random.seed(20261127)
RESULTS = []


def report(name, kind, failures, total, detail=""):
    ok = (failures == 0) if kind == 'POS' else (failures > 0)
    RESULTS.append((name, kind, ok))
    tag = "ok" if ok else "UNEXPECTED"
    print(f"[{kind}] {name}: {failures}/{total} failures -> {tag} {detail}")


def primes_upto(n):
    s = bytearray([1]) * (n + 1); s[0:2] = b'\x00\x00'
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(n + 1) if s[i]]


def lpf(n):  # least prime factor (n >= 2)
    if n % 2 == 0:
        return 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return d
        d += 2
    return n


def RZ(n, Z):  # (2.1): 1_{P^-(n) > Z}
    return 1 if n > 1 and lpf(n) > Z else 0


# ---------------------------------------------------------------------------------------------
print("== (A) Lemma 4.1, counting step (4.11)")
fails = tot = 0; negf = 0
for (sets, Y) in [([[3, 5, 7], [11, 13, 17]], 32), ([[3, 5, 7, 11], [13, 17, 19, 23]], 64),
                  ([[3, 5], [7, 11], [13, 17, 19]], 256), ([[5, 7, 11, 13, 17]], 4),
                  ([[3, 5, 7], [11, 13], [17, 19, 23, 29]], 1024)]:
    A = sorted({math.prod(t) for t in itertools.product(*sets)})
    A = [a for a in A if Y <= a <= 4 * Y]
    cnt = sum(1 for a in A for b in A if math.gcd(a, b) > 1)
    allp = [p for s in sets for p in s]
    bnd = sum((4 * Y // p) ** 2 for p in allp)
    tot += 1; fails += (cnt > bnd)
    # NEG: the count of pairs sharing p is ~ (#multiples)^2, a bound linear in #multiples is too small
    negb = sum(len([a for a in A if a % p == 0]) for p in allp)
    negf += (cnt > negb)
    print(f"   K={len(sets)} Y={Y}: #A={len(A)}, #pairs gcd>1 = {cnt} <= sum floor(4Y/p)^2 = {bnd}; linear {negb}")
report("A (4.11) #{(a,b) in [Y,4Y]^2: gcd>1} <= sum_p floor(4Y/p)^2", 'POS', fails, tot)
report("NEG A pair count <= sum_p #{a: p|a} (linear, not squared)", 'NEG', negf, tot)

# ---------------------------------------------------------------------------------------------
print("== (B) (4.12) equivalence and psi_{-2} insertion (p. 17)")
fails = tot = 0; neg_conv = 0; negtot = 0
for _ in range(60000):
    a = random.choice([3, 5, 7, 9, 15, 21, 35, 11, 33, 13]); b = random.choice([3, 5, 7, 11, 13, 25, 39, 55])
    m, n, r, s = (random.randint(1, 60) for _ in range(4))
    lhs = ((m * n + 2) % a == 0 and (r * s + 2) % b == 0 and (m * n + 2) // a == (r * s + 2) // b)
    rhs = (b * m * n - a * r * s == 2 * (a - b))
    if math.gcd(a, b) == 1:
        tot += 1; fails += (lhs != rhs)
    else:
        negtot += 1; neg_conv += (lhs != rhs)
# make sure the equation side is hit often: solve for s given (a,b,m,n,r)
hits = 0
for _ in range(20000):
    a = random.choice([3, 5, 7, 11, 13]); b = random.choice([3, 5, 7, 11, 13])
    m, n, r = (random.randint(1, 80) for _ in range(3))
    num = b * m * n - 2 * (a - b)
    if num % (a * r) == 0 and num // (a * r) >= 1:
        s = num // (a * r); hits += 1
        lhs = ((m * n + 2) % a == 0 and (r * s + 2) % b == 0 and (m * n + 2) // a == (r * s + 2) // b)
        if math.gcd(a, b) == 1:
            tot += 1; fails += (not lhs)
        else:
            negtot += 1; neg_conv += (not lhs)
report(f"B (4.12) <=> for gcd(a,b)=1 ({hits} equation solutions included)", 'POS', fails, tot)
report("NEG B (4.12) <=> also for gcd(a,b)>1", 'NEG', neg_conv, negtot)
fails = tot = 0; negf = 0
for Y in [1, 2, 4, 8, 16, 1024]:
    for a in range(Y, 4 * Y + 1):
        for b in range(Y, 4 * Y + 1):
            tot += 1
            fails += not (abs(Fr(b - a, Y)) <= 4)          # psi_1 = 1 on |u| <= 4
            negf += not (abs(Fr(b - a, Y)) <= 2)           # NEG: psi_1 = 1 only on |u| <= 2
report("B psi_{-2}((bmn-ars)/Y) = psi_1((b-a)/Y) = 1 on Y<=a,b<=4Y", 'POS', fails, tot)
report("NEG B same with psi_1 = 1 only on |u| <= 2", 'NEG', negf, tot)
# and the algebra -(bmn-ars)/(2Y) = (b-a)/Y on the relation
fails = 0
for _ in range(2000):
    a, b, Y = random.randint(1, 99), random.randint(1, 99), random.randint(1, 50)
    t = 2 * (a - b)
    fails += (Fr(-t, 2 * Y) != Fr(b - a, Y))
report("B psi_{-2}(t/Y) = psi_1(-t/(2Y)) = psi_1((b-a)/Y) when t = 2(a-b)", 'POS', fails, 2000)


# ---------------------------------------------------------------------------------------------
# Toy model for (C), (D)
def psi1(u, inner=4, outer=8):
    u = abs(u)
    if u <= inner:
        return 1.0
    if u >= outer:
        return 0.0
    return (outer - u) / (outer - inner)


def eta(x):  # supported in [1,4], positive inside
    return math.sin(math.pi * (x - 1) / 3) ** 2 if 1 < x < 4 else 0.0


def c2(t, a, b):  # generic complex stand-in for the M_{-2} integral (deterministic)
    h = (t * 1000003 + a * 9176 + b * 7919) % 100003
    return complex(math.cos(h), 0.7 * math.sin(3 * h)) * 0.3


class Toy:
    def __init__(self, sets, J, Y, Z, M, N, rho=0.6, conj_alpha=True, psi_outer=8, psi_inner=4,
                 dD_factor=True, seed=1):
        self.sets, self.K, self.J, self.Y, self.Z, self.M, self.N = sets, len(sets), J, Y, Z, M, N
        self.rho, self.conj_alpha, self.dD = rho, conj_alpha, dD_factor
        self.pin, self.pout = psi_inner, psi_outer
        self.allp = [p for s in sets for p in s]
        self.which = {p: i for i, s in enumerate(sets) for p in s}
        self.V = [sum(Fr(1, p) for p in s) for s in sets]
        self.Vf = [float(v) for v in self.V]
        rnd = random.Random(seed)
        self.alpha = {m: complex(rnd.uniform(-1, 1), rnd.uniform(-1, 1)) * 0.7
                      for m in range(M + 1, 2 * M + 1) if RZ(m, Z)}
        self.beta = {n: complex(rnd.uniform(-1, 1), rnd.uniform(-1, 1)) * 0.7
                     for n in range(N + 1, 2 * N + 1) if RZ(n, Z)}

    def psim2(self, u):  # psi_{-2}(u) = psi_1(-u/2)
        return psi1(-u / 2, self.pin, self.pout)

    def G_and_omega(self, P1):  # G(P1) = prod_{p^nu || P1, p in U P_i} p^nu ; omega_i(P1)
        G, om = 1, [0] * self.K
        for p in self.allp:
            if P1 % p == 0:
                om[self.which[p]] += 1
                q = P1
                while q % p == 0:
                    q //= p; G *= p
        return G, om

    def mu2(self, n):
        for p in self.allp:
            if n % (p * p) == 0:
                return 0
        return 1

    def f(self, P):  # (4.42), read literally
        G, om = self.G_and_omega(P[0])
        if self.mu2(G) == 1 and all(o == self.J + 1 for o in om):
            al = self.alpha.get(P[0] // G, 0)
            al = al.conjugate() if self.conj_alpha else al
            return al * self.beta.get(P[1], 0)
        return 0

    def coeff_sum(self, a, b, mode):
        """sum_{m,n,r,s} alpha_m conj(alpha_r) beta_n conj(beta_s) * kernel, as in (4.7), (4.14), (4.44)."""
        Y = self.Y
        F = {}
        for m, am in self.alpha.items():
            for n, bn in self.beta.items():
                F[m * n] = F.get(m * n, 0) + am * bn
        tot = 0
        for k, Fk in F.items():
            for l, Fl in F.items():
                t = b * k - a * l
                if mode == 'QY':        # (mn+2)/a = (rs+2)/b in N*
                    ind = ((k + 2) % a == 0 and (l + 2) % b == 0 and (k + 2) // a == (l + 2) // b)
                    v = 1.0 if ind else 0.0
                elif mode == 'H':       # H_{-2}(t; a, b) with toy integral
                    v = self.psim2(t / Y) * c2(t, a, b)
                elif mode == 'eq':      # 1_{bmn - ars = 2(a-b)}
                    v = 1.0 if t == 2 * (a - b) else 0.0
                if v:
                    tot += Fk * Fl.conjugate() * v
        return tot

    def products(self):
        return sorted({math.prod(t) for t in itertools.product(*self.sets)})

    def QY_direct(self):  # first line of (4.7)
        Y = self.Y
        inner = {}
        for a in self.products():
            ea = eta(a / Y)
            if ea == 0:
                continue
            for m, am in self.alpha.items():
                for n, bn in self.beta.items():
                    if (m * n + 2) % a == 0:
                        h = (m * n + 2) // a
                        inner[h] = inner.get(h, 0) + ea * am * bn
        pv = math.prod(1 / v ** 2 for v in self.Vf)
        return pv * sum(abs(x) ** 2 for x in inner.values())

    def Dab(self, a, b):
        e = eta(a / self.Y) * eta(b / self.Y)
        if e == 0:
            return 0
        if math.gcd(a, b) == 1:
            return e * (self.coeff_sum(a, b, 'eq') - self.coeff_sum(a, b, 'H'))
        return e * (self.coeff_sum(a, b, 'QY') - self.coeff_sum(a, b, 'H'))

    def w(self, a, b):  # w(a,b) by brute force over ordered distinct J-tuples avoiding {p'_i, p_{i,J+1}}
        fa, fb = self.factor_ab(a), self.factor_ab(b)
        tot = Fr(1)
        for i, s in enumerate(self.sets):
            avail = [p for p in s if p not in (fa[i], fb[i])]
            tot *= sum(Fr(1, math.prod(tup)) / self.V[i] ** self.J
                       for tup in itertools.permutations(avail, self.J))
        return tot

    def factor_ab(self, a):
        out = [None] * self.K
        for p in self.allp:
            if a % p == 0:
                out[self.which[p]] = p
        return out

    # ---- operator side, read literally from (4.18), (4.19), (4.21), (4.36), (4.38)
    def supp_positions(self):
        """All P1 with f(P1, .) possibly nonzero: P1 = g*m, g = squarefree product of exactly J+1 primes of
        each P_i, alpha_m != 0. Verified against brute force in check_support()."""
        per = [list(itertools.combinations(s, self.J + 1)) for s in self.sets]
        P1s = set()
        for choice in itertools.product(*per):
            g = math.prod(math.prod(c) for c in choice)
            for m in self.alpha:
                P1s.add(g * m)
        return sorted(P1s)

    def check_support(self, lo, hi):
        sp = set(self.supp_positions())
        bad = 0
        n0 = next(iter(self.beta))
        for P1 in range(lo, hi + 1):
            nz = self.f((P1, n0)) != 0
            bad += (nz != (P1 in sp))
        return bad, hi - lo + 1

    def B_sum(self, record_terms=None):
        """sum over dyadic d0 of B_{d0}/d0, B_{d0} = <f, T^C_{-2} f> (4.21), (4.38)."""
        K, J, Y, M, N = self.K, self.J, self.Y, self.M, self.N
        P1s = self.supp_positions()
        Ds = set()
        for tup in itertools.product(*[list(itertools.permutations(s, J)) for s in self.sets]):
            Ds.add(math.prod(math.prod(c) for c in tup))
        d0s = sorted({2 ** (D.bit_length() - 1) for D in Ds})
        sigma = math.prod(v ** -(J + 1) for v in self.Vf)
        total = 0
        nterms = 0
        prim_viol = 0
        for d0 in d0s:
            lo1, hi1 = d0 * Y * M, 16 * d0 * Y * M
            # positions of S(d0) in supp f, in C, primitive
            pos = []
            for P1 in P1s:
                if not (lo1 <= P1 <= hi1):
                    continue
                for P2 in self.beta:
                    if not (N <= P2 <= 2 * N):
                        continue
                    P = (P1, P2)
                    if math.gcd(P1, P2) != 1 or P1 % 2 == 0 or P2 % 2 == 0:
                        continue
                    fv = self.f(P)
                    if fv != 0:
                        pos.append((P, fv))
            # index Q by the set of P_i-primes dividing Q1
            byset = {}
            for (Q, fq) in pos:
                ps = frozenset(p for p in self.allp if Q[0] % p == 0)
                byset.setdefault(ps, []).append((Q, fq))
            Bd = 0
            for (P, fp) in pos:
                divs = [[p for p in s if P[0] % p == 0] for s in self.sets]
                omP = sum(len(d) for d in divs)
                # states: ordered tuples of J+1 distinct primes of P_i dividing P1 (4.19)
                for tup in itertools.product(*[list(itertools.permutations(d, J + 1)) for d in divs]):
                    D = math.prod(math.prod(c[:J]) for c in tup)
                    if not (d0 <= D < 2 * d0):
                        continue
                    b = math.prod(c[J] for c in tup)
                    Tf = 0
                    for pp in itertools.product(*[[p for p in s if p not in c] for s, c in zip(self.sets, tup)]):
                        a = math.prod(pp)
                        need = frozenset(x for c, q in zip(tup, pp) for x in (list(c[:J]) + [q]))
                        for ps, lst in byset.items():
                            if not need <= ps:
                                continue
                            for (Q, fq) in lst:
                                detPQ = P[0] * Q[1] - P[1] * Q[0]
                                assert detPQ % D == 0
                                t = detPQ // D
                                omQ = len(ps)
                                kern = eta(a / Y) * eta(b / Y) * self.psim2(t / Y)
                                if kern == 0:
                                    continue
                                kern *= (d0 / D if self.dD else 1.0)
                                kern *= self.rho ** ((omP + omQ - 2 * K * (J + 1)) / 2)
                                kern *= ((1.0 if t == 2 * (a - b) else 0.0) - c2(t, a, b))
                                Tf += kern * fq
                    Tf *= math.prod(1 / v for v in self.Vf)
                    Bd += fp.conjugate() * Tf * sigma
            total += Bd / d0
        return total

    def p24_checks(self):
        """For every (tuples, p', m, n, r, s) with nonzero summand: t != 0, primitivity, G, f-identity, rho."""
        K, J, Y = self.K, self.J, self.Y
        cnt = bad_prim = bad_t = bad_G = bad_f = bad_rho = 0
        for tup in itertools.product(*[list(itertools.permutations(s, J + 1)) for s in self.sets]):
            D = math.prod(math.prod(c[:J]) for c in tup); b = math.prod(c[J] for c in tup)
            if eta(b / Y) == 0:
                continue
            for pp in itertools.product(*[[p for p in s if p not in c] for s, c in zip(self.sets, tup)]):
                a = math.prod(pp)
                if eta(a / Y) == 0:
                    continue
                for m in self.alpha:
                    for n in self.beta:
                        for r in self.alpha:
                            for s in self.beta:
                                t = b * m * n - a * r * s
                                if not (t == 2 * (a - b) or self.psim2(t / Y) != 0):
                                    continue
                                cnt += 1
                                P, Q = (D * b * m, s), (D * a * r, n)
                                bad_t += (t == 0)
                                bad_prim += (math.gcd(*P) != 1 or math.gcd(*Q) != 1)
                                GP, omP = self.G_and_omega(P[0]); GQ, omQ = self.G_and_omega(Q[0])
                                bad_G += (GP != D * b or GQ != D * a)
                                lhs = self.f(P).conjugate() * self.f(Q)
                                rhs = self.alpha[m] * self.alpha[r].conjugate() * self.beta[n] * self.beta[s].conjugate()
                                bad_f += abs(lhs - rhs) > 1e-12
                                bad_rho += (sum(omP) + sum(omQ) != 2 * K * (J + 1))
        return cnt, bad_t, bad_prim, bad_G, bad_f, bad_rho

    def chain(self):
        pv = math.prod(1 / v ** 2 for v in self.Vf)
        QY = self.QY_direct()
        A = self.products()
        QY2 = pv * sum(eta(a / self.Y) * eta(b / self.Y) * self.coeff_sum(a, b, 'QY') for a in A for b in A)
        Qmaj = pv * sum(eta(a / self.Y) * eta(b / self.Y) * self.coeff_sum(a, b, 'H') for a in A for b in A)
        Bs = self.B_sum()
        cop = [(a, b) for a in A for b in A if math.gcd(a, b) == 1]
        ncp = [(a, b) for a in A for b in A if math.gcd(a, b) > 1]
        D = {ab: self.Dab(*ab) for ab in cop + ncp}
        W = {ab: self.w(*ab) for ab in cop}
        rhs446 = pv * sum(float(W[ab]) * D[ab] for ab in cop)
        rhs = pv * (sum((1 - float(W[ab])) * D[ab] for ab in cop) + sum(D[ab] for ab in ncp))
        return dict(QY=QY, QY2=QY2, Qmaj=Qmaj, B=Bs, rhs446=rhs446, lhs=QY - Qmaj - Bs, rhs=rhs,
                    nnz_cop=sum(1 for ab in cop if abs(D[ab]) > 0), ncop=len(cop),
                    gcd1=pv * sum(D[ab] for ab in ncp), wmin=min(W.values()), wmax=max(W.values()))


def close(x, y, tol=1e-9):
    return abs(x - y) <= tol * max(1.0, abs(x), abs(y))


TOYS = {
    # K=1, J=1: small enough to brute-force the support of f over all P1 in Omega's range
    'T1 K=1 J=1': dict(sets=[[3, 5, 7]], J=1, Y=2, Z=37, M=40, N=40),
    # K=1, J=2: w(a,b) has nontrivial exclusions
    'T2 K=1 J=2': dict(sets=[[3, 5, 7, 11, 13]], J=2, Y=4, Z=67, M=70, N=70),
}

print("== (C) p. 24: t != 0, primitivity, G(P1)=Db, conj f(P) f(Q) identity, rho exponent")
for name, kw in TOYS.items():
    toy = Toy(**kw)
    cnt, bt, bp, bG, bf, br = toy.p24_checks()
    print(f"   {name}: {cnt} terms with nonzero kernel (|t|<16Y or t=2(a-b)), 16Y={16*kw['Y']} < Z={kw['Z']}")
    report(f"C {name} t != 0 and gcd(Dbm,s)=gcd(Dar,n)=1", 'POS', bt + bp, cnt)
    report(f"C {name} G(Dbm)=Db, G(Dar)=Da", 'POS', bG, cnt)
    report(f"C {name} conj f(P) f(Q) = a_m conj(a_r) b_n conj(b_s)", 'POS', bf, cnt)
    report(f"C {name} omega(P1)+omega(Q1) = 2K(J+1) (rho^... = 1)", 'POS', br, cnt)
# NEG: drop the conjugation on alpha in (4.42)
toy = Toy(**TOYS['T2 K=1 J=2'], conj_alpha=False)
cnt, bt, bp, bG, bf, br = toy.p24_checks()
report("NEG C f = alpha*beta (no bar on alpha): identity fails", 'NEG', bf, cnt)
# NEG: widen the kernel support far beyond Z (|t| < 16*60*Y): primitivity must fail somewhere
toy = Toy(**TOYS['T2 K=1 J=2'], psi_inner=4 * 60, psi_outer=8 * 60)
cnt, bt, bp, bG, bf, br = toy.p24_checks()
report("NEG C kernel support |t| < 960Y >> Z: primitivity fails", 'NEG', bt + bp, cnt)

print("== (C') support of f (4.42), brute force over the full P1-range of Omega (T1)")
toy = Toy(**TOYS['T1 K=1 J=1'])
bad, n = toy.check_support(2 * 2 * 40, 16 * 4 * 2 * 80)
report("C' T1 {P1: f(P1,.) != 0} = {g m: g = (J+1)-subset product, alpha_m != 0}", 'POS', bad, n)

print("== (D) exact chain (4.38) -> (4.44) -> (4.46) -> (4.48)")
for name, kw in TOYS.items():
    t1 = time.time()
    toy = Toy(**kw)
    R = toy.chain()
    print(f"   {name}: Q_Y={R['QY']:.6g} (alt {R['QY2'].real:.6g}{R['QY2'].imag:+.1e}i), Q^maj={R['Qmaj']:.4g},"
          f" sum B/d0={R['B']:.4g}")
    print(f"      lhs={R['lhs']:.6g}  rhs={R['rhs']:.6g}  nonzero D(a,b): {R['nnz_cop']}/{R['ncop']} coprime pairs;"
          f" gcd>1 part {R['gcd1']:.3g}; w in [{float(R['wmin']):.4f}, {float(R['wmax']):.4f}]  ({time.time()-t1:.1f}s)")
    report(f"D {name} (4.7) two forms of Q_Y agree", 'POS', 0 if close(R['QY'], R['QY2']) else 1, 1)
    report(f"D {name} (4.46) sum_d0 B_d0/d0 = prod V^-2 sum_coprime w D", 'POS',
           0 if close(R['B'], R['rhs446']) else 1, 1, f"diff {abs(R['B']-R['rhs446']):.1e}")
    report(f"D {name} Q_Y - Q^maj - sum B/d0 = prod V^-2[sum (1-w)D + sum_gcd>1 D]", 'POS',
           0 if close(R['lhs'], R['rhs']) else 1, 1, f"diff {abs(R['lhs']-R['rhs']):.1e}")

kw = TOYS['T2 K=1 J=2']
for label, extra in [("no bar on alpha in (4.42)", dict(conj_alpha=False)),
                     ("kernel support |t| < 960Y >> Z (primitivity lost)", dict(psi_inner=240, psi_outer=480)),
                     ("d0/D factor dropped from (4.38)", dict(dD_factor=False)),
                     ("psi_1 = 1 only on |u| <= 1 (insertion invalid)", dict(psi_inner=1, psi_outer=2))]:
    toy = Toy(**kw, **extra)
    R = toy.chain()
    report(f"NEG D T2 chain identity with {label}", 'NEG', 0 if close(R['lhs'], R['rhs']) else 1, 1,
           f"lhs {R['lhs']:.4g} vs rhs {R['rhs']:.4g}")

# ---------------------------------------------------------------------------------------------
print("== (E) w(a,b) and the p. 26 bound; (4.51) count")
# (E1) small sets, J = 1, 2, 3, all pairs, exact Fractions (positive check only: the toy bound is loose here)
sets = [[3, 5, 7, 11, 13], [17, 19, 23, 29, 31, 37]]
V = [sum(Fr(1, p) for p in s) for s in sets]
fails = tot = 0
for J in [1, 2, 3]:
    for pa in itertools.product(*sets):
        for pb in itertools.product(*sets):
            if any(x == y for x, y in zip(pa, pb)):
                continue
            w = Fr(1)
            for i, s in enumerate(sets):
                avail = [p for p in s if p not in (pa[i], pb[i])]
                w *= sum(Fr(1, math.prod(t)) / V[i] ** J for t in itertools.permutations(avail, J))
            bnd = sum(Fr(J * (J - 1), 2) * sum(Fr(1, (p * p)) / V[i] ** 2 for p in s)
                      + Fr(J, pa[i]) / V[i] + Fr(J, pb[i]) / V[i] for i, s in enumerate(sets))
            tot += 1
            fails += not (0 <= w <= 1 and 0 <= 1 - w <= bnd)
report("E1 w(a,b) <= 1 and 0 <= 1-w <= sum_i [C(J,2) sum 1/(pV_i)^2 + J/(p'_iV_i) + J/(p_{i,J+1}V_i)] (K=2, small sets)",
       'POS', fails, tot)
# (E2) larger primes (p in (1000, 6000], 1/(pV) small), J = 2, K = 2, brute force over ordered pairs (floats):
# here 1 - w is first order, so the NEG (factor J dropped) can bite.
PR = [p for p in primes_upto(12000) if p > 1000]
sets = [[p for p in PR if p <= 6000], [p for p in PR if 6000 < p <= 12000]]
Vf = [math.fsum(1 / p for p in s) for s in sets]
fails = tot = 0; negf = 0; J = 2
for _ in range(4):
    pa = [random.choice(s) for s in sets]; pb = [random.choice([q for q in s if q != x]) for s, x in zip(sets, pa)]
    w = 1.0
    for i, s in enumerate(sets):
        inv = [1 / (p * Vf[i]) for p in s if p not in (pa[i], pb[i])]
        S1 = math.fsum(inv); S2 = math.fsum(x * x for x in inv)
        # brute force over ordered distinct pairs = S1^2 - S2 (identity), cross-checked on a slice below
        w *= S1 * S1 - S2
    # brute-force cross-check of the pair sum for i = 0 on the first 400 primes
    sl = [1 / (p * Vf[0]) for p in sets[0][:400] if p not in (pa[0], pb[0])]
    bf = math.fsum(x * y for ix, x in enumerate(sl) for iy, y in enumerate(sl) if ix != iy)
    s1 = math.fsum(sl)
    assert abs(bf - (s1 * s1 - math.fsum(x * x for x in sl))) < 1e-12
    bnd = sum(math.comb(J, 2) * math.fsum(1 / (p * Vf[i]) ** 2 for p in s) + J / (pa[i] * Vf[i]) + J / (pb[i] * Vf[i])
              for i, s in enumerate(sets))
    bneg = sum(math.comb(J, 2) * math.fsum(1 / (p * Vf[i]) ** 2 for p in s) + 1 / (pa[i] * Vf[i]) + 1 / (pb[i] * Vf[i])
               for i, s in enumerate(sets))
    tot += 1; fails += not (0 <= 1 - w <= bnd + 1e-12); negf += not (1 - w <= bneg)
    print(f"   E2: 1-w = {1-w:.5f}, bound = {bnd:.5f}, NEG bound = {bneg:.5f}")
report("E2 0 <= 1-w <= p. 26 bound (K=2, J=2, primes in (1000,12000])", 'POS', fails, tot)
report("NEG E2 same bound with J/(p'V), J/(p_{J+1}V) replaced by 1/(p'V), 1/(p_{J+1}V)", 'NEG', negf, tot)
fails = tot = 0; mx = 0
for _ in range(3000):
    Y = random.choice([4, 16, 64, 1024]); a = random.randint(Y, 4 * Y); b = random.randint(Y, 4 * Y)
    k = random.randint(1, 10 ** 6)
    lo = math.floor((b * k - 16 * Y) / a); cntl = sum(1 for l in range(lo - 2, lo + 40) if abs(b * k - a * l) < 16 * Y)
    lo = math.floor((a * k - 16 * Y) / b); cntk = sum(1 for kk in range(lo - 2, lo + 40) if abs(b * kk - a * k) < 16 * Y)
    tot += 1; fails += (cntl > 33 or cntk > 33); mx = max(mx, cntl, cntk)
report(f"E (4.51) #{{l: |bk-al|<16Y}} <= 33 and #{{k: ...}} <= 33 (max seen {mx})", 'POS', fails, tot)

# ---------------------------------------------------------------------------------------------
print("== (F) meas M_{-2} = meas M_1 <= 4 L^{3A0} / Y (exact interval arithmetic)")


def union_measure(ivs):  # intervals on R (already reduced to [0,1) pieces)
    ivs = sorted(ivs); tot = Fr(0); cur = None
    for lo, hi in ivs:
        if cur is None or lo > cur[1]:
            if cur:
                tot += cur[1] - cur[0]
            cur = [lo, hi]
        else:
            cur[1] = max(cur[1], hi)
    if cur:
        tot += cur[1] - cur[0]
    return tot


def mod1_pieces(lo, hi):
    out = []
    k = math.floor(lo)
    while k < hi:
        a, b = max(lo, Fr(k)), min(hi, Fr(k + 1))
        if a < b:
            out.append((a - k, b - k))
        k += 1
    return out


fails = tot = 0
for (LA, Y) in [(3, 200), (5, 1000), (4, 97), (6, 5000)]:
    rad = Fr(2 * LA, Y)
    M1 = []
    for k in range(1, LA + 1):
        for j in range(k):
            if math.gcd(j, k) == 1:
                M1 += mod1_pieces(Fr(j, k) - rad, Fr(j, k) + rad)
    m1 = union_measure(M1)
    # M_{-2} = {theta : -2 theta in M_1}: preimage of [u,v) under theta -> -2 theta is
    # {theta in (-v/2,-u/2]} + {1/2 + same}
    Mm2 = []
    for (u, v) in M1:
        for sh in (Fr(0), Fr(1, 2)):
            Mm2 += mod1_pieces(-v / 2 + sh, -u / 2 + sh)
    m2 = union_measure(Mm2)
    tot += 1; fails += not (m1 == m2 and m1 <= 4 * Fr(LA) ** 3 / Y)
    print(f"   L^A0={LA}, Y={Y}: meas M_1 = {float(m1):.5f}, meas M_-2 = {float(m2):.5f}, 4L^(3A0)/Y = {4*LA**3/Y:.5f}")
report("F meas M_-2 = meas M_1 <= 4 L^{3A0}/Y", 'POS', fails, tot)

# ---------------------------------------------------------------------------------------------
print("== SUMMARY")
pos = [r for r in RESULTS if r[1] == 'POS']; neg = [r for r in RESULTS if r[1] == 'NEG']
print(f"positive checks: {len(pos)}, failing: {sum(1 for r in pos if not r[2])}")
print(f"negative controls: {len(neg)}, failing as they must: {sum(1 for r in neg if r[2])}")
unexp = [r[0] for r in RESULTS if not r[2]]
print(f"unexpected outcomes: {len(unexp)} {unexp}")
print(f"wall time {time.time() - T0:.1f} s")
