# Rung 182: exact re-check of the printed arithmetic of [M] (report)

Status: **finished**. The program re-does in exact rational arithmetic every rational or arithmetical step that the
182 paper [M] prints in (8.3), in the Section 10 tables and (10.1)-(10.3), in Sec. 13.3 and in Sec. 3.7. It recomputes
from the printed inputs only. All 86 substantive checks pass. One item is cosmetic and is printed as a NOTE, not counted
as a check: a decimal printed with "..." on p. 15 is rounded to nearest at its last digit, not truncated.

**What this does not verify.** None of this checks the 182 claim. Every input taken from the Section 10 tables is an
upper bound for a source integral and is **Claimed**: A_j, M_j and b, and also mu- of (7.6). The PDF does not print the
individual A_j, M_j (197 components). So the 197-term square-root sum can only be bracketed from the 6 printed group
totals; it cannot be recomputed.

- Program: `code/sharifi182_arith.py`. Run it with `/usr/bin/python3 -I code/sharifi182_arith.py`. It exits with
  status 0 (86 PASS, 0 FAIL); the cosmetic item described below is printed as a NOTE (changed by the coordinator,
  Session 21, after re-running the script). Each input carries a comment giving its page and
  equation number.
- Source PDF: the bundle `prime_gaps_182_expository_bundle.pdf`, 17271479 bytes.
  - Its SHA-256 is 5362e977880af92a73a79b411a9c66daf0b93af4ec0ed6bec320090386f4b881. This is **identical** to the hash
    recorded in notes/sources-182.md (14 Nov download).
  - The copy read here was a fresh download kept in the session scratchpad. Its text was extracted with
    `pdftotext -layout`, and with `-raw` for pp. 12, 16-18 and 33-41.
  - Nothing from the authors' programs was run.
- Page numbers are printed pages of [M]. For [M] these equal the PDF pages.
- Rounding conventions used here:
  - Section 10 entries are "rounded upward ... in units of 10^-6" (p. 39), with 9 decimals. So a printed p stands for a
    true value v with p - 1e-9 < v <= p, in units of 1e-6.
  - "Consistent" means that some choice of true values inside all these rounding intervals reproduces every printed
    number.
  - Square roots are enclosed rigorously by integer square roots (`math.isqrt`, scale 1e40). They are cross-checked
    with python-flint arb balls at 200 bits.

## (a) (8.3), p. 33

- Quoted: "eps_h = kappa-bar(1/.0108 - 1) 2.194, delta_op = 4 rho* eps_h, gamma_op = 1 - delta_op,
  Gamma = 4 rho*(1 + eps_h)".
  - The `-raw` extraction puts the bar on kappa: it is kappa-bar = 46653544162031/5e17 of (4.3), p. 21.
  - 2.194 is the step-kernel bound 0 <= K <= 2.194 of (5.7), p. 26.
  - rho* = 2624989/10^7 comes from (7.1), p. 29.
- Exact values:
  - eps_h = 126565513539834821311/6750000000000000000000 = 0.018750446450...
  - delta_op = 0.019687886270...
  - gamma_op = 0.980312113729...
  - Gamma = 1.069683486270...
  - t - gamma_op = 0.119687886270..., with t = 11/10 (p. 34).
- The printed "for orientation" values are eps_h ~ .01875045, delta_op ~ .01968789 and gamma_op ~ .98031211. **PASS**:
  each is the nearest 8-decimal rounding of the exact value.
- **PASS**:
  - gamma_op > 0.
  - t = 11/10 > gamma_op.
  - Gamma = 4 rho* + delta_op, an identity.
  - eps_h <= 1.
- **PASS**, from (6.8), p. 28: .0108 <= ell <= .0112, with ell ~ 0.0109438385.
  - So the 1/.0108 in eps_h is a valid upper replacement for 1/ell.
  - eps_h >= d_h * 2.194, where d_h = kappa-bar(1/ell - 1) ~ 0.0084327. The slack is 2.49e-4.
  - Hence -eps_h <= a_H, a, as used in (8.4).
  - ell <= .0112 also matches the "old-inner coefficient at most .0112" of p. 35.

## (b) Section 10 tables, pp. 39-40

Printed inputs, verbatim (units 1e-6):

| Outer source | Count | sum A_j | sum M_j | Loss |
|---|---|---|---|---|
| G1 low | 8 | 0.749574898 | 14.579171091 | 6.699042427 |
| G1 rank two | 14 | 0.224037660 | 1.558976746 | 1.177680761 |
| G1 high | 1 | 0.000019087 | 0.000031473 | 0.000051304 |
| G2 low | 22 | 3.755008125 | 40.782076795 | 25.186856792 |
| G2 rank two | 14 | 23.449034139 | 151.904930860 | 121.397753113 |
| G2 high | 1 | 0.779494639 | 5.803481072 | 4.347133100 |

- Inner contributions to b: G3 low (8) 0.007585797; G4 low (21) 0.017382180; G5 low (8) 0.413045470; G6 low (20)
  2.684023505; C low (7) 9.828292827; all rank-two and high (73) 13.752470897.
- The four-term table gives b = 26.702800674, Gamma b/t = 25.966859017, 2 sum sqrt(A_j M_j) = 155.342695198 and
  (t - gamma_op) sum A_j = 3.465822296.
- (10.1) states b < .000026702801.
- (10.2) states L-bar = 105739089/500000000000 = .000211478178.

Results (all **PASS**):

- **Counts.**
  - Outer: 8+14+1+22+14+1 = 60. Inner: 8+21+8+20+7+73 = 137. Total 197.
  - These agree with the Sec. 9.1 family table (p. 36): G1 (8,14,1), G2 (22,14,1), G3 (8,14,1), G4 (21,12,1),
    G5 (8,14,1), G6 (20,13,1), C (7,15,1).
  - The inner split is 64 low + 68 rank two + 5 high, and 73 = 68 + 5, as stated on p. 36.
- **b.**
  - The six inner rows sum to 26.702800676 (rounded-up rows). Printed b = 26.702800674.
  - The rounding intervals (26.702800670, 26.702800676] and (26.702800673, 26.702800674] intersect, so the values are
    consistent: summing rounded-up entries can exceed the rounded-up exact sum.
  - (10.1) follows from printed b.
- **Gamma b/t.**
  - Gamma * 26.702800674 / (11/10) = 25.966859016510..., which rounds up to **25.966859017**, exactly the printed value.
  - Over the whole b-interval the value lies in (25.966859015537, 25.966859016510]. So the printed entry is consistent
    with the printed b and with Gamma of (8.3), and is a valid upper bound for it.
- **(t - gamma_op) sum A_j.**
  - The printed group sums give sum A = 28.957168548.
  - Times t - gamma_op this is 3.4658222959..., which rounds up to **3.465822296**, exactly the printed value.
- **Outer Loss column**, defined on p. 39 as Loss = 2 sum sqrt(A_j M_j) + (t - gamma_op) A_g.
  - *Single-component groups (high).* Here Loss is an exact function of the printed A and M.
    - G1 high: f(A, M) = 0.000051303872..., which rounds up to 0.000051304. Matches.
    - G2 high: f = 4.347133102148... Over the rounding box of A, M the value rounds up to [4.347133099, 4.347133103],
      which contains the printed 4.347133100. Consistent.
    - The printed Loss is below f evaluated at the printed (upper) A, M. That is possible only because the true A, M
      are slightly below their rounded-up displays.
    - arb and isqrt enclosures of sqrt(AM) agree to 15 decimals.
  - *Multi-component groups.* Each Loss lies strictly between (t - g) A_g and the Cauchy-Schwarz ceiling
    2 sqrt(A_g M_g) + (t - g) A_g, as Sec. 8.3 says it must.
    - The ratios of the cross part to the CS ceiling are 0.9997, 0.9737, 0.9995 and 0.9935.
    - Mine: these ratios are close to 1. Within groups, A_j and M_j are thus nearly proportional, so keeping the
      components separate gains little inside a group.
  - *Totals.*
    - The Loss column sums to 158.808517497, against printed 155.342695198 + 3.465822296 = 158.808517494. Consistent.
    - Row-wise, Loss minus (t-g)A brackets 2 sum sqrt(A_j M_j) in (155.342695195, 155.342695201). This contains the
      printed 155.342695198.
    - The printed 155.342695198 is at most the group-CS ceiling 156.162522956.
- **(10.2).**
  - The four printed terms sum to 211.478177185e-6.
  - L-bar = 105739089/5e11 = .000211478178 exactly, which is that sum rounded up at 1e-12. The slack is 8.15e-13.

**Not checkable from the PDF:** the 2 sum sqrt(A_j M_j) over the 197 individual components (only 6 group totals of A
and M are printed), and every individual A_j, M_j and inner b-component. Q (p. 39): "The full rational values,
including individual source bins, are in the digital supplement."

## (c) (7.6), (10.3), Sec. 13.3

All **PASS**.

- **(7.6).**
  - mu- = 9968877639291/36028797018963968, and 36028797018963968 = 2^55.
  - mu- = 0.000276691937120293... > .0002766919371.
- **(7.5).** 0 < I- < I+, with I- = 1.48963408e-11 and I+ = 1.48963412e-11. Both are "about 1.4896341e-11".
- **(10.3).**
  - mu- - L-bar equals the printed 573626291549967919851/8796093022208000000000000 **exactly**. The denominator is
    2^43 * 10^12.
  - mu- - L-bar = 0.000065213759120293... > .000065213759 > 0.
  - The abstract (p. 1) and p. 5 repeat the same three decimals.
  - Mine: L-bar / mu- = 0.7643.
- **Sec. 13.3 (p. 45), Lean margin.**
  - kappa_cvx = 11696/125000000 = .000093568 exactly, and kappa_cvx > kappa-bar.
  - The two printed forms of xi_add in (13.1), (1-ell)^2 (kappa_cvx - kappa-bar)/d_h and
    ell(1-ell)(kappa_cvx - kappa-bar)/kappa-bar, agree exactly.
  - 4 rho* xi_add = 3.17802e-5, which satisfies the printed "0 < 4 rho* xi_add < 32/10^6".
  - With J+(PF) <= 4 I(F) (quoted from p. 45, not checked), (mu- - L-bar) - 4 rho* xi_add = 3.34335e-5 > 33/10^6.
  - Via the coarse bound 32e-6 it is 3.32138e-5 > 33e-6.
  - So the printed "> 33/10^6" follows from (10.3) by arithmetic.

## (d) Section 3.7, pp. 16-18

Inputs are quoted from the `-raw` extraction:

- T1 = 1262625033/1312494500, B0 = 1/(2 rho), eps_r = 10^-7 and U_n = T1 + eps_r/rho.
- b13 and b14 as in (3.15)-(3.16), with xi_j = U_n - b_j.
- omega_s = 21/5000, delta_s = 2279/100000, xi_s = delta_s/rho = 22790/262499 and c_s = B0 - T1.
- From (3.17): S_C = B0 - b14 - eps_r/rho*, omega_C = (rho(S_C+T1) - 1/2 + eps_r)/2, sigma0 = .100001,
  delta_C = (1 - 4 sigma0)/16 - (7/2) omega_C - eps_r and xi_C = delta_C/rho.
- a_C = B0 - T1 and b_C = B0 - S_C.
- From (3.5), p. 12: a = .41361, I0 = .34941, c = .41364, tau = 10^-10.

**PASS** (each strict bracket or identity holds exactly):

- xi_s = 22790/262499.
- The p. 17 table:
  - c_s - b13 = .0359890960831929...
  - xi_s - xi13 = .0315909495519855...
  - c_s + xi_s - U_n = .0675800456351784...
  - Each lies inside its printed (lower, upper) pair. All three are > 0, which is what (3.14) needs.
- B0 + xi_s - T1 = 1.029584... > 1.02958.
- 1/2 + 2 omega_s - 2 rho T1 = .003349794... > .00334979.
- 1/2 + 2 omega_s - 2 rho* T1 = 8374967/2500000000 = .0033499868 **exactly**.
- rho* S_C = .2607860319243636988... lies in (.2607860319243, .2607860319244).
- omega_C = .0066556670361227... and delta_C = .0142048153735704... lie in their brackets.
- b_C - b14 = 1/2624989 exactly.
- xi_C - xi14 = .0034033703034562... and b_C + xi_C - U_n = .0034037512574335... lie in their brackets.
- (3.19): B0 + xi_C - max(2S_C - T1, 2T1 - S_C) = .933937484 > .93393748.
- (3.20):
  - 1/2 + 2 omega_C - rho(S_C+T1) = 10^-7 exactly.
  - 1/2 + 2 omega_C - rho*(S_C+T1) = 2.955479e-7 > 2.9554e-7.
  - delta_C - rho* xi_C = 5.411379e-9 > 5.411e-9.
  - 1/2 - rho* B0 = 1/5249980 exactly.
- T1 < S_C < S, and a_C = c_s > b_C.
- Order-two source inequalities (p. 18), with sigma0 = .100001 used at both sources:
  - First genuine-prime inequality (56w + 16d + 4 sigma0 < 1): the margin is **exactly 39/250000** at the self source
    and **exactly 1/625000** at the subtraction source, as printed.
  - Every other displayed inequality has margin > .0096 at both sources: GP 68w+14d<1; GP sigma0 > 1/18 + 28w/9 + 2d/9;
    SM 56w+16d+4 sigma_m<1; SM 68w+14d<1; SM a+1/2+2w<1; SM I0-tau > 1/4+7w+2d;
    SM sigma3 > 1/30 + 56 wbar/15 + 4d/15; SM 108 wbar+2d > 1.
  - The tightest is sigma3 at the self source, with margin .009616.
  - Observation (not counted as a failure): the inline condition "sigma0 > 1/10" holds with margin only 10^-6. I read
    "every other listed inequality" as the displayed list, which is how the claim holds.

**FAIL (cosmetic), p. 15 after (3.12).**
- Printed: "its physical radius is .2607860319243637 ...". The exact value is rho* S_C = .26078603192436369884...
- So ".2607860319243637" is the nearest 16-digit rounding (PASS under that reading), not the leading digits that the
  "..." suggests.
- The strict bracket on p. 17 is correct. This has no effect on any inequality.

**Cross-check against the repository copy of the trial data** (code/data182/TrialData182_part3_sources.lean; this is
not a PDF claim): b13 and b14 are exactly the `innerCore` of new-ladder rows 13 and 14 (0-based). U_n = T1 + eps_r/rho
is exactly their `innerThreshold` 331437939786917/344528493755500. Both **PASS**.

## (e) What Sections 9-10 (and the rest of the bundle) do NOT print

I confirm the note's statement, with page references:

- **Source-row tables (omega_prev, omega, delta, order, S, T).**
  - Only the definition of a row is printed (p. 14, before (3.8)), together with the counts "43 retained old rows and
    55 retained new rows" (p. 15).
  - Only rows 13 and 14 of the new ladder appear, and only partially, as b13, b14 and U_n (p. 16, (3.15)-(3.16)).
  - Q (p. 6): "The digital supplement supplies the lengthy rational coefficient and source tables."
  - No table appears in Secs. 9-10 or in the companions (searched: "ladder", "prev", "source row").
  - The rows are available in the repo copy of TrialData182.lean (above), not in the PDF.
- **Low-witness and Chernoff parameters.**
  - Only the form of the bound (9.2), p. 37, is printed, with beta generic.
  - p. 41 refers to "fixed Chernoff parameters" without values.
  - Not printed: bin windows, beta values, count prefixes R and the dyadic scale Q = 2^b of Sec. 9.5 (p. 39).
  - Printed are the split points p_G/h (p. 37) and the family counts (p. 36).
  - The beta on p. 50 is an unrelated Kloosterman/Fu parameter.
- **T0.** It is printed only as "rho* T0 = .2491228441011" (p. 29, table of physical radii). There is no exact rational
  anywhere in the bundle. In Sec. 9.5, p. 39, "(T0)_0" is the power series T_r at r = 0, not the radius.
- **Per-component A_j, M_j, and the 197 inner/outer source values.** These are not printed: only the 6 outer group
  totals and the 6 inner group contributions (p. 40).
