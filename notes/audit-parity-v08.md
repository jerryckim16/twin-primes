# Referee audit: parity paper v0.8, Subsection `subsec:window`

Scope: `papers/parity-barrier/main.tex`, from `\label{subsec:window}` to `\section{The asymptotic sieve`.
The working tree changed while this audit ran. Lines 1058-1189 now include the new
Corollary `cor:k3-linear`, the kappa paragraph, and Remark 1 with 0.43831. All of these are audited below.
Nothing in the paper was edited and nothing was committed.

**Verdict.** No ERROR in the proved or computed statements. Everything recomputed agrees.
- The proposition and its proof are correct.
- All six certificates re-verify.
- All quoted numbers match the outputs.

There are 2 GAPs and 6 WORDING items. One heuristic sentence is false on a short interval (W3).
The new corollary makes parts of Theorem `thm:k3-window`(2) redundant and slightly improves the 0.439 threshold.

## 1. Proposition `prop:unc-ceiling` and its proof (checked line by line)

- **Fibres and positivity.** D = (3/2)R_3, and u = (x, y) lies in Delta, so x + y <= a.
  - The fibre is t_i in [0, 3/2 - x - y]. It is non-empty because a < 3/2.
  - The index-i term of h is 1[x+y<=a] g(u) = g(u). The other two terms are >= 0 because phi >= 0.
  - So h >= g(u) > 0 on the fibre.
  - Cauchy-Schwarz with weights h^{-1/2}, h^{1/2} is valid: h is bounded because mu > 0 and phi is continuous on a compact set.
  - Fubini/Tonelli applies to F^2/h >= 0, and int F dt_i exists for a.e. u. No hidden measurability or integrability issue.
- **Active indicator terms.**
  - Take the coordinate equal to x, call its index j. Then t_{-j} = {t_i, y}, and the term is 1[t_i + y <= a] g(t_i, y).
  - Along the fibre this is active for t_i in [0, min(a - y, 3/2 - x - y)].
  - The claim a - y <= 3/2 - x - y is equivalent to x <= 3/2 - a. It holds because x <= a (from x + y <= a), and a <= 3/2 - a is equivalent to eps >= 1/4. Correct.
  - Symmetry of g is used correctly: g(t_i, y) is the same whatever the coordinate order.
  - Integrating in t_i gives Phi(y). The coordinate equal to y gives Phi(x).
- **Bound on the fibre integral.** int h dt_i = (3/2-x-y) g + Phi(x) + Phi(y) <= (3/2 - x - y + mu + x + y) g = C g. Correct.
- **Final chain.**
  - J_i <= C int_{t_{-i} in Delta} F^2 g(t_{-i}) / h dt.
  - Summing over i, the numerator becomes h itself on {h > 0}. This gives C int_{h>0} F^2 <= C I(F). Correct.
  - On {h = 0} no fibre over Delta passes through the point, so nothing is lost.
- **Edge cases.**
  - y = a: then x = 0, Phi(a) = 0 and the upper limit a - y = 0. Fine.
  - x + y = a: the active length is exactly x = a - y. Fine.
- **Monotonicity in eps'.**
  - The support (3/2)R_3 of Theorem 3.14 at k = 3 is k/(k-1) R_k and does not depend on eps.
  - J_{i,1-eps'} <= J_{i,1-eps} because the domain is smaller and the integrand is non-negative.
  - The eps-dependent marginal condition is never used, so sigma_3(eps') <= sup without the condition <= C. Correct.
- **Is phi > 0 needed everywhere?** No. The proof needs phi >= 0 and g > 0 on Delta.
  - Every (x, y) in Delta has min(x, y) <= a/2. So phi > 0 on [0, a/2] together with phi >= 0 suffices.
  - That weaker hypothesis is exactly what `k3_unc_cert.py` accepts.
  - The verifier, and every certificate file, has strictly positive node values. So the stated hypothesis is met. See W5.
- **W1 (WORDING).** In "The term for the coordinate x", say "the term whose index j has t_j = x (so t_{-j} = {t_i, y})". This makes the indicator 1[t_i + y <= a] self-evident.

## 2. The sharpness and eigenfunction claim after the proof

**G1 (GAP / WORDING).** "With the exact Perron eigenfunction it is sharp ... the eigenfunction of that problem has the form ..." is stated as fact and carries no label. Only the numerical check after it is labelled Heuristic.

- *What is provable in two lines.* If a continuous phi > 0 satisfies Phi = phi with mu, then:
  - F = h satisfies int h dt_i = C g(t_{-i}) on Delta;
  - so h is an exact eigenfunction with eigenvalue C;
  - so the ratio of h is exactly C, and the Schur bound is attained.
- *What is assumed.* Two things:
  - That the supremum is attained by an eigenfunction. The form is not compact (each P_i^* P_i is an infinite-rank projection), so the top of the spectrum need not be an eigenvalue.
  - That a positive solution of the 1D equation exists at mu = mu*.
- *Is the form right?* Yes, if an eigenfunction exists.
  - From lambda F = sum_i 1[t_{-i} in Delta] (int F dt_i), we get F = sum_i 1[...] G(t_{-i}).
  - Integrating along a fibre gives (lambda - 3/2 + x + y) G = psi(x) + psi(y), with psi(y) = int_0^{a-y} G(tau, y) dtau.
  - This is exactly g with mu = lambda - 3/2, and psi = Phi.
- *Numerics.* The claim is plausible numerically.
  - 1D (N = 200, 400) and 2D kernel at eps = 3/8: 2.05637 and 2.056338 (n = 160, still rising). They agree to 1e-4.
  - The 1D computation also matches the Corollary's scaling: kappa = 0.89017 from eps = 0.4385, 0.439 and 0.44.
- *Fix.* Rewrite as follows. "If phi > 0 solves Phi = phi exactly, then h attains the bound, so the test is sharp. Heuristically the supremum is attained by such an h, and the 1D, 2D and 3D computations agree to 1e-4."
- Also record the outputs of `k3_unc_1d.py` and `k3_unc_kernel.py` in a `.out` file. No such file exists in `code/parity/`, and the "3D" computation behind the 1e-4 agreement is not named here. The route card cites `k3_thm314_dual.py` in 'none' mode; name it in the paper.

## 3. Certificates and the two programs

Runs, with at most 2 cores. All passed.

| file | output |
|---|---|
| `k3_unc_cert_439_1000.json` | eps=439/1000, C=19999/10000, N=600, verified on 5135 boxes (~5 min) |
| `k3_unc_cert_9_20.json` | eps=9/20, C=399/200 = 1.995, N=200, 848 boxes |
| `k3_unc_cert_1_4.json` | eps=1/4, C=217/100, N=300, 1667 boxes |
| `k3_unc_cert_3_8.json` | eps=3/8, C=2057/1000, N=300, 4150 boxes |
| `k3_arrangement_cert_2_9_n18.json` | I, J equal to the certificate; 0 violations; J/I - 2 = 342007/555935160 |
| `k3_arrangement_cert_7_24_n24.json` | I, J equal; 0 violations; J/I - 2 = 4238047/46648223968 |
| `k3_arrangement_cert.json` (n=8, eps=1/4; extra) | J/I - 2 = 711155/3866758832 |

In each file, the eps, C and mu = C - 3/2 values agree with the theorem. The verifier asserts mu, eps >= 1/4 and mu > 0.

Critical reading of `k3_unc_verify.py` (and `k3_unc_cert.py`):
- **Box majorant.** For y in [y0, y1] and every t:
  - The numerator satisfies phi(t) + phi(y) <= phi(t) + P with P = max_box phi, and it is >= 0.
  - The denominator satisfies mu + t + y >= mu + t + y0 > 0.
  - The integrand is positive, so the upper limit can be raised from a - y to a - y0.
  - Hence Phi(y) <= Phi+ on the whole box. This is rigorous.
- **Max and min of phi on a box.** Both programs take max and min over phi(y0), phi(y1) and every node strictly inside (y0, y1). For a piecewise-linear phi this is exact. Node evaluation uses exact Fractions.
- **Closed form.** Substitute v = s + t with s = mu + y0, so phi = alpha + beta (v - s). This gives int (alpha - beta s + P + beta v)/v dv = beta (v1 - v0) + (alpha - beta s + P) log(v1/v0). Correct.
  - `k3_unc_cert.py` splits the same expression differently (the P log((s+T)/s) term kept separate). That is algebraically equal.
  - The loop truncates the last piece at T = a - y0 correctly.
- **Interval rigour.**
  - All quantities are exact rationals before conversion.
  - The verifier converts each rational as `iv.mpf([n,n])/d`, which is outward rounded at 120 bits, then applies `iv.log`.
  - `k3_unc_cert.py` uses `arb(n)/d` at 128 bits.
- **Comparison.** The verifier tests `tot.b < X(pmin).a`; the generator tests `up.upper() < arb(pmin).lower()`. Both are strict, on the correct ends, and against the box minimum of phi(y). Correct.
- **Coverage.** The initial uniform grid covers [0, a], and failing boxes are bisected (depth <= 30, asserted). Every box is either verified or the program aborts. Correct.
- **Positivity.** The verifier asserts all node values > 0. The generator adds delta = 1e-3 to every node, so positivity holds with margin.
- **W5 (WORDING, code).**
  - The `k3_unc_cert.py` docstring states the hypothesis as "phi >= 0, phi > 0 on [0,a/2]", which is weaker than the Proposition's phi > 0. Either add a footnote to the Proposition (the weaker hypothesis suffices, see section 1) or change the docstring.
  - The same docstring says "the integrand is ... decreasing in y". That holds only after phi(y) is replaced by the box maximum. The paper's wording is fine.

## 4. Numbers in Theorem `thm:k3-window` and Remark `rem:k3-window`

- **Theorem (1).** All three ratios match the verifier exactly, and the cell counts n = 18, 8, 24 match the files.
- **Theorem (2).** Matches the certificates.
- **Remark (1).** `k3_unc_1d.py` gives:
  - eps = 0.4375, N = 200: lambda_unc = 2.000732
  - eps = 0.44, N = 200: 1.998507
  - (also eps = 0.439: 1.999397; eps = 0.4385, N = 400: 1.999832; eps = 0.2501: 2.16754; eps = 0.45: 1.98961; eps = 0.375: 2.05637)

  The crossing at 2 is about 0.4383. The current text, 0.43831, agrees with `kappa_closed_form.out` (eps* = 0.438308). The committed HEAD text said "about 0.4385", which was slightly off; the working tree has fixed this.
- **Remark (2) against `k3_arrangement_eps2.out`.**

  | eps | value in Remark | value in file | n |
  |---|---|---|---|
  | 1/6 | 1.9909 | 1.990937 | 24 |
  | 1/5 | 1.9982 | 1.998162 | 20 |
  | 3/10 | 1.9990 | 1.999029 | 20 |
  | 1/3 | 1.9952 | 1.995151 | 24 |

  All agree.

- **W2 (WORDING).** "At 1/5 and 3/10 they are still rising with n, so these cases are undecided" suggests that 1/6 and 1/3 are decided. They are not.
  - At 1/6 the values rise from 1.98996 (n = 12) to 1.99094 (n = 24).
  - At 1/3 they rise from 1.99405 (n = 12) to 1.99515 (n = 24).
  - All four are rigorously undecided. Fix: "All four are still rising with n, so none is decided. At 1/5 and 3/10 the gap to 2 is small enough that even the extrapolations do not settle them."

## 5. The new Corollary `cor:k3-linear`, and its effect on the theorem

- **Proof.** The scaling argument is correct.
  - With tau = s tau' and y = s y', both dtau and the denominator scale by s. So Phi_{sa,s mu}[phi(./s)](s y') = Phi_{a,mu}[phi](y').
  - Positivity and continuity are preserved, and the Proposition applies because eps is in [1/4, 1/2).
  - 0.4999/0.561 = 4999/5610 exactly. The corollary rests only on the 0.439 certificate, which re-verified.
- **G2 (GAP, presentation).** The corollary supersedes parts of Theorem (2).
  - It gives sigma_3(1/4) <= 2.16827, sigma_3(3/8) <= 2.05692 and sigma_3(0.45) <= 1.99009. These are all stronger than the stated 2.17, 2.057 and 1.995.
  - It also gives sigma_3 < 2 for all eps > 1 - 5610/9998 = 0.438888. That is slightly better than the theorem's 0.439.
  - Fix, either way:
    - (a) state the theorem's part (2) via the corollary: "sigma_3(eps) <= 3/2 + (4999/5610)(1-eps), which is < 2 for eps > 0.43889". Keep the other three certificates only as independent cross-checks.
    - (b) Or add a sentence after the corollary saying it improves part (2).
  - Then update in the same way: the threshold 0.439 in the abstract (line 42), the open question 6 interval ("sigma_3(1/4) in (2.0001, 2.17]"), and changelog 0.8.
  - In open question 6, the lower bound 2.0001 is also weaker than the exact 2.00255 (n = 24) quoted in Remark `rem:k3-eps`. Either value is a valid lower bound, but use the best one.

## 6. Overclaiming and heuristic labels

- **Window label.** The window (0.19, 0.31) and the maximum of about 2.003 are inside a remark labelled Heuristic, and are introduced by "the picture is ... roughly". Open question 6 says "Heuristically". This is adequately labelled.
- **W3 (WORDING; a false heuristic sentence).** Remark (3) says: "a rigorous upper bound below 2 ... anywhere in [0.31, 0.439) needs the marginal condition: without it the supremum exceeds 2 there."
  - By the paper's own kappa computation, the unconstrained supremum is below 2 for eps > 0.43831.
  - So on (0.43831, 0.439), a finer certificate without the marginal condition would suffice.
  - With the corollary, the rigorous threshold is already 0.43889.
  - Fix: replace [0.31, 0.439) with [0.31, 0.4383), or say "for eps < eps* ~ 0.43831". Make the same change in open question 6 (line 1702).
- **W4 (WORDING).** The theorem says "cannot prove it for any eps in [0.439, 1/2)". Make it precise as "the criterion of Theorem 3.14 with k = 3 cannot give DHL[3,2]", which is what the theorem means. This does not mean DHL[3,2] fails.
- **W6 (WORDING).** "(and eps = 1/4 is [Theorem 3.15]PM8b)" should say what is being identified: "the case eps = 1/4 is the computation behind [PM8b, Theorem 3.15] (H_1 <= 6 under GEH)". The page reference p. 63 and the quoted phrase were not checked against arXiv:1407.4897v4, because no local copy exists.
- **Twin primes and parity.** Nothing in the subsection suggests progress on twin primes or on the parity problem. The results concern only the GEH-conditional criterion for DHL[3,2] (H_1 <= 6) at k = 3. The abstract sentence (lines 41-42) is consistent with that.

## Summary of fixes

1. **G1:** reword the sharpness claim as conditional and provable, with existence or attainment labelled Heuristic. Name the 3D script and record the 1D and 2D outputs.
2. **G2:** fold Corollary `cor:k3-linear` into Theorem (2), or state that it supersedes it. The threshold becomes 0.43889, and the bounds become 2.1683 (eps = 1/4), 2.0569 (eps = 3/8) and 1.9901 (eps = 0.45). Propagate to the abstract, open question 6 and the changelog. Use 2.0025 as the lower bound for sigma_3(1/4).
3. **W3:** change [0.31, 0.439) to [0.31, 0.4383) in Remark (3) and in open question 6.
4. **W2:** all four of 1/6, 1/5, 3/10 and 1/3 are undecided.
5. **W1, W4, W5, W6:** minor wording, as above.
