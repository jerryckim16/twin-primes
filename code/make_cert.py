#!/usr/bin/env python3
"""Write and re-verify an exact certificate that M_k > T.

usage: make_cert.py k degree [T]   (T defaults to 4, the Bombieri-Vinogradov threshold; use 2 for EH)
"""
import sys, json
sys.path.insert(0, "code")
from fractions import Fraction as Fr
from mk_bound import run, gram
k, D = int(sys.argv[1]), int(sys.argv[2])
T = int(sys.argv[3]) if len(sys.argv) > 3 else 4
info, exact, basis, q = run(k, D)
den = q[0].denominator
for x in q: assert (x*10**40).denominator == 1
cert = dict(k=k, D=D, basis=basis, scale="1e40", coeffs=[str(int(x*10**40)) for x in q],
            rayleigh_num=str(exact.numerator), rayleigh_den=str(exact.denominator))
json.dump(cert, open(f"code/cert_M{k}.json", "w"))
# independent re-verification from the file
c = json.load(open(f"code/cert_M{k}.json"))
b2, I, J = gram(c["k"], c["D"])
assert [list(x) for x in b2] == c["basis"]
v = [Fr(int(s), 10**40) for s in c["coeffs"]]
n = len(v)
num = c["k"]*sum(v[i]*J[i][j]*v[j] for i in range(n) for j in range(n))
dn = sum(v[i]*I[i][j]*v[j] for i in range(n) for j in range(n))
assert dn > 0 and num > T*dn
print("VERIFIED exactly: M_%d >= %s > %d   (margin %.6f)" % (k, info["certified"], T, float(num/dn - T)))
