"""Rung 182: check the 43 + 55 source rows of the trial data against the row definitions printed in the
expository bundle (Sec. 3.5, p. 14; Sec. 3.6, pp. 15-16; (3.13)).  Exact rational arithmetic.

Data: code/data182/TrialData182_part3_sources.lean (verbatim copy of formal/TrialData182.lean, part 3, as pasted by
Jerry Kim on 14 Nov 2026).  Printed inputs: rho = 262499/10^6 ((7.1), p. 29); S = 1379373467/1312494500,
N = 393216 (Sec. 7); T1 = 1262625033/1312494500, B0 = 1/(2 rho) (p. 16); rho* = 2624989/10^7;
rho* T0 = .2491228441011 (p. 29, decimal only).

Row definition (p. 14): B = (1/2 + 2 omega_prev)/rho, xi = delta/rho, a_r = B - T, b_r = B - S,
eta = xi (r = 1, 2), (xi + S + T - B)/2 (r = 3), A_r = a_r + eta, C_r = b_r + eta; budget A_r + C_r <= B + xi;
order-three plateaux (p. 15): Lambda_old = clip((3A - C)/4; 3 max(A,C)/7, 3 min(A,C)/5), Lambda_new = 23 C/40.
Ladder (p. 16): 43 old and 55 new rows, B_first = 1/(2 rho), B_next = B_r^+ = (1/2 + 2 omega_r)/rho;
(3.13): B_last^+ >= h[(N - 1) + min(floor(T/h), N - 2)], T = T0 (old), T1 (new), h = S/N.
Field reading (ours): lowerBand = B, upperBand = B^+, activation = xi, outerCore = a_r, innerCore = b_r,
outerThreshold = A_r, innerThreshold = C_r, plateau = L.  The radius bounds S, T of each row are recovered as
B - innerCore and B - outerCore.
Run: /usr/bin/python3 -I code/sharifi182_rows.py   (exit 1 on any failure)
"""
import re, sys, math
from fractions import Fraction as Fr
src = open('code/data182/TrialData182_part3_sources.lean').read()
def parse(name):
    i = src.index('def ' + name); j = src.index(']', i)
    rows = []
    for m in re.finditer(r'\{([^}]*)\}', src[i:j]):
        rows.append({k: Fr(v.replace(' ', '')) for k, v in re.findall(r'(\w+)\s*:=\s*\(?([-0-9/ ]+)\)?', m.group(1))})
    return rows
FAILS = []; NP = 0
def check(name, ok, detail=''):
    global NP
    if ok: NP += 1; print('PASS ', name, detail)
    else: FAILS.append(name); print('FAIL ', name, detail)
rho = Fr(262499, 10**6); rhos = Fr(2624989, 10**7)
S_pr = Fr(1379373467, 1312494500); N = 393216; h = S_pr / N; T1 = Fr(1262625033, 1312494500)
old, new = parse('trialOldSourceRows'), parse('trialNewSourceRows')
check('row counts 43 old, 55 new (p. 16)', (len(old), len(new)) == (43, 55), f'{len(old)}, {len(new)}')
out = {}
for nm, R in (('old', old), ('new', new)):
    check(f'{nm}: B_first = 1/(2 rho)', R[0]['lowerBand'] == 1 / (2 * rho))
    check(f'{nm}: contiguity B_next = B_r^+', all(R[i+1]['lowerBand'] == R[i]['upperBand'] for i in range(len(R) - 1)))
    check(f'{nm}: B^+ = (1/2 + 2 omega)/rho', all(r['upperBand'] == (Fr(1, 2) + 2 * r['omega']) / rho for r in R))
    check(f'{nm}: omega increasing', all(R[i+1]['omega'] > R[i]['omega'] for i in range(len(R) - 1)))
    check(f'{nm}: xi = delta/rho', all(r['activation'] == r['delta'] / rho for r in R))
    Ts = {r['lowerBand'] - r['outerCore'] for r in R}; Ss = {r['lowerBand'] - r['innerCore'] for r in R}
    check(f'{nm}: one radius T for all rows', len(Ts) == 1); check(f'{nm}: one radius S for all rows', len(Ss) == 1)
    T, S = Ts.pop(), Ss.pop(); out[nm] = (S, T)
    check(f'{nm}: S = printed S', S == S_pr, f'S = {S}')
    ok_eta = ok_A = ok_C = ok_bud = ok_pl = True; nplat = 0; viol12 = []
    for r in R:
        B, xi, ordr = r['lowerBand'], r['activation'], int(r['order'])
        a, b = B - T, B - S
        eta = xi if ordr in (1, 2) else (xi + S + T - B) / 2
        ok_A &= r['outerThreshold'] == a + eta; ok_C &= r['innerThreshold'] == b + eta
        if ordr == 3: ok_bud &= r['outerThreshold'] + r['innerThreshold'] <= B + xi
        else: viol12.append(r['outerThreshold'] + r['innerThreshold'] <= B + xi)
        A, C = r['outerThreshold'], r['innerThreshold']
        if ordr == 3:
            nplat += 1
            if nm == 'old':
                z = (3 * A - C) / 4; lo, hi = 3 * max(A, C) / 7, 3 * min(A, C) / 5; L = min(hi, max(lo, z))
            else:
                L = Fr(23, 40) * C
            ok_pl &= r['plateau'] == L
        else:
            ok_pl &= r['plateau'] == 0
    check(f'{nm}: A_r = a_r + eta (eta by order)', ok_A); check(f'{nm}: C_r = b_r + eta', ok_C)
    check(f'{nm}: order-3 budget A_r + C_r <= B + xi (p. 14, stated in the order-three paragraph)', ok_bud)
    print(f'INFO  {nm}: orders 1-2 rows satisfying A_r + C_r <= B + xi: {sum(viol12)} of {len(viol12)} (no such budget is printed for orders 1-2)')
    check(f'{nm}: plateau = Lambda_{nm} at order 3 ({nplat} rows), 0 otherwise', ok_pl)
    Tl = T if nm == 'old' else T1
    if nm == 'new': check('new: T = T1 (p. 16)', T == T1, f'T = {T}')
    rhs = h * ((N - 1) + min(math.floor(Tl / h), N - 2))
    check(f'{nm}: (3.13) B_last^+ >= h[(N-1) + min(floor(T/h), N-2)]', R[-1]['upperBand'] >= rhs,
          f'margin {float(R[-1]["upperBand"] - rhs):.3e}')
S, T0 = out['old']
v = rhos * T0
check('old: rho* T0 matches printed .2491228441011 (13 places, rounding)', abs(v - Fr('0.2491228441011')) <= Fr(5, 10**14),
      f'T0 = {T0} = {float(T0):.15f}, rho* T0 = {float(v):.15f}')
check('rho* S = .2758746934 (10 places)', abs(rhos * S - Fr('0.2758746934')) <= Fr(5, 10**11))
print(f'T0 (old-ladder radius, recovered from the rows; not printed in the PDF) = {T0}')
print(f'{NP} PASS, {len(FAILS)} FAIL'); sys.exit(1 if FAILS else 0)
