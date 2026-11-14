#!/usr/bin/env python3
"""Parse the 182 trial data (code/data182/TrialData182_part*.lean, verbatim copies of formal/TrialData182.lean of
romyar1/prime-gaps-lean, supplied by Jerry Kim on 14 Nov 2026) into exact rationals, and run integrity checks:
shapes, cell-aligned caps (cap/h integers equal to the table of notes/sources-182.md), knots as in the bundle,
band chain lowerBand_{t+1} = upperBand_t, upperBand = (1/2 + 2 omega)/rho, activation = delta/rho on the rows where it
holds (reported, not asserted), order counts. usage: python3 code/sharifi182_data.py [--json out.json]"""
import re, sys, json
from fractions import Fraction as F

def rat(s):
    s = s.strip().strip("()")
    if "/" in s:
        a, b = s.split("/")
        return F(int(a), int(b))
    return F(int(s))

def load():
    p1 = open("code/data182/TrialData182_part1.lean").read()
    p2 = open("code/data182/TrialData182_part2_coefficients.lean").read()
    p3 = open("code/data182/TrialData182_part3_sources.lean").read()
    D = {}
    for name in ["trialRadius", "trialRho", "trialRhoStar", "trialLambda", "trialKappa", "trialLargestCap", "trialPrimeCap",
                 "trialBaseRadius", "trialEnlargedRadius", "trialSubtractionRadius", "trialSubtractionActivation",
                 "trialDenominatorLower", "trialDenominatorUpper", "trialJ0Lower", "trialJPlusLower", "trialTailUpper"]:
        m = re.search(r"def %s : ℚ := (\([^)]*\)|\d+)" % name, p1)
        D[name] = rat(m.group(1))
    D["dim"] = int(re.search(r"def trialDimension : ℕ := (\d+)", p1).group(1))
    D["N"] = int(re.search(r"def trialIntervals : ℕ := (\d+)", p1).group(1))
    kn = p1.split("def trialKnots")[1].split("def trialAngular")[0]
    D["knots"] = [rat(x) for x in re.findall(r"\(-?\d+ / \d+\)", kn)]
    sg = p1.split("def trialAngularSignature")[1].split("def trialComponentCap")[0]
    D["signatures"] = [tuple(int(y) for y in re.findall(r"\d+", x)) for x in re.findall(r"\[([\d, ]*)\]", sg.split(":=")[1])]
    cc = p1.split("def trialComponentCap")[1].split("structure TrialShell")[0]
    D["component_caps"] = [rat(x) for x in re.findall(r"\(-?\d+ / \d+\)", cc)]
    sh = p1.split("def trialShells")[1].split("def trialBaseRadius")[0].split(":=", 1)[1]
    shells = []
    for blk in sh.split("],")[0:5]:
        rows = re.findall(r"lower := ([^,]+), upper := ([^,]+), cap := ([^}]+) \}", blk)
        shells.append([tuple(rat(v) for v in r) for r in rows])
    D["shells"] = dict(zip(["outer", "base", "enlarged", "subtractionC", "full"], shells))
    co = [rat(x) for x in re.findall(r"\(-?\d+ / \d+\)", p2)]
    assert len(co) == 3 * 11 * 22, len(co)
    D["coeff"] = [[[co[(c * 11 + s) * 22 + d] for d in range(22)] for s in range(11)] for c in range(3)]
    def rows(txt):
        out = []
        for r in re.findall(r"\{ order := (\d+), (.*?) \}", txt):
            d = {"order": int(r[0])}
            for k, v in re.findall(r"(\w+) := (\([^)]*\)|\d+)", r[1]):
                d[k] = rat(v)
            out.append(d)
        return out
    D["old_rows"] = rows(p3.split("def trialOldSourceRows")[1].split("def trialNewSourceRows")[0])
    D["new_rows"] = rows(p3.split("def trialNewSourceRows")[1])
    return D

def checks(D):
    out = {}
    S, N, rho = D["trialRadius"], D["N"], D["trialRho"]
    h = S / N
    out["h"] = str(h)
    out["S_ok"] = S == F(1379373467, 1312494500)
    out["h_ok"] = h == F(1379373467, 516093837312000)
    ccap = [c / h for c in D["component_caps"]]
    out["component_caps_over_h"] = [str(x) for x in ccap]
    out["component_caps_ok"] = ccap == [141720, 177528, 246256]
    sh = {k: [(str(l / h), str(u / h), str(c / h)) for (l, u, c) in v] for k, v in D["shells"].items()}
    out["shell_caps_over_h"] = {k: [c for (_, _, c) in v] for k, v in sh.items()}
    out["shell_caps_ok"] = out["shell_caps_over_h"] == {"outer": ["246256", "196608", "186253"], "base": ["246256", "177542", "140306"],
                                                        "enlarged": ["246256", "179967", "141724"], "subtractionC": ["246256", "186491"], "full": ["246256"]}
    kn = D["knots"]
    out["knots_ok"] = (len(kn) == 26 and kn[:4] == [F(3, 20)] * 4 and kn[13:17] == [F(324809441462533, 344528493755500)] * 4
                       and kn[-4:] == [S] * 4 and all(kn[i] <= kn[i + 1] for i in range(25)))
    out["signatures"] = [list(s) for s in D["signatures"]]
    out["signatures_ok"] = D["signatures"] == [(), (2,), (3,), (4,), (2, 2), (5,), (2, 3), (6,), (2, 4), (3, 3), (2, 2, 2)]
    out["radii_ok"] = (D["trialEnlargedRadius"] == F(1262625033, 1312494500) and D["trialLargestCap"] == D["component_caps"][2])
    for lab in ("old_rows", "new_rows"):
        R = D[lab]
        cnt = [sum(1 for r in R if r["order"] == o) for o in (1, 2, 3)]
        chain = all(R[i + 1]["lowerBand"] == R[i]["upperBand"] for i in range(len(R) - 1))
        ub = sum(1 for r in R if r["upperBand"] == (F(1, 2) + 2 * r["omega"]) / rho)
        act = sum(1 for r in R if r["activation"] == r["delta"] / rho)
        out[lab] = dict(rows=len(R), order_counts=cnt, band_chain=chain, upperBand_formula_rows=ub, activation_eq_delta_over_rho_rows=act,
                        first_lowerBand=str(R[0]["lowerBand"]), last_upperBand=str(R[-1]["upperBand"]))
    out["I_target"] = [float(D["trialDenominatorLower"]), float(D["trialDenominatorUpper"])]
    return out

if __name__ == "__main__":
    D = load()
    r = checks(D)
    print(json.dumps(r, indent=1))
    if "--json" in sys.argv:
        json.dump(r, open(sys.argv[sys.argv.index("--json") + 1], "w"), indent=1)
