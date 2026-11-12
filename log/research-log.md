# Research log

## 2026-11-12 - Session 4 (8 AM, first test run of the schedule): H1 ≤ 246 reproduced (M_{50,1/25} ≥ 4.0043063); dual weights that see only t_m and S stall near 4.14; paper v0.4

- Added Polymath8b's epsilon-enlarged simplex to the exact pipeline (scaling plus the binomial rewrite 1+eps-P1 = 2eps + (1-eps-P1)); checked every Gram entry against direct sympy integration for k = 3, 4. Lowering the search precision from about 6000 to 300-500 bits made high degrees cheap.
- Certified M_{50,1/25} ≥ 4.0012466 (degree 25, 1780 coefficients) and ≥ 4.0043063 (degree 27, 2526 coefficients), matching Polymath8b's 4.00124 and 4.0043. With the Lean tuple (50, 246) the project's end-to-end bound moved from 270 to 246, the established bound: a reproduction, not new.
- Own idea (variational/spectral): optimised Lemma 13 over every dual weight of the form Psi(S - t_m, t_m) as a convex program. It returns exactly k/(k-1) log k at eps = 0 and settles near 4.14 at (50, 1/25), far above the truth (≥ 4.0043): sharper floors need weights that see more of t (Proposition 19). A Collatz-Wielandt weight from the Galerkin eigenfunction is within 1e-4 of M_3 at k = 3 (sampled), but for eps > 0 the eigenfunction vanishes where no index is active.
- Certified M_{k,eps} for k = 49, 50 at degrees 10-24 and six values of eps. A geometric extrapolation in the degree, tested against the known k = 50 values and against a prediction registered before the degree-24 run (3.98230 predicted, 3.98218 certified), suggests sup_eps M_{49,eps} ≈ 3.991-3.994 < 4: heuristic evidence that the enlarged simplex stops at k = 50 (Remark 20).
- Lean: not_boundedGaps_one (gaps of size 1 happen only once) and admissible_pair_iff ({0,d} is admissible iff d is even). Re-read Polymath8b Prop. 6.5 in the arXiv text: as printed, the argument gives (k/(k-1)+eps) log(2k-1) (Remark 16).

Did not work or is blocked:
- The first discretisations of the dual-weight program were wrong or unstable (Kelley cutting planes drifted; piecewise-constant weights in (sigma,u) could not represent the two-zone weight). The final version uses cells in (S,u) and an exact convex solver per step.
- At (k, eps) = (30, 1/4) the discretised optimum has not converged (4.050, 4.035, 4.024 for N = 80, 120, 160, above the 4.0021 already certified), so the exact floor of the (t_m,S) family is not determined.
- A product-form Collatz-Wielandt weight (F = prod 1/(1+A t_i)) gave useless bounds (above 5 at k = 50).
- No news search this run (only the 3:34 AM run does it); the 182 preprint is still not re-opened.

Next: Stadlmann's support for 240 (rough-mass caps in the integration formulas). Own side: a Collatz-Wielandt weight that stays positive where an index is active, aiming at a rigorous floor near k = 50.

## 2026-11-12 - Session 3 (7 AM, recovery of the 6:34 AM run): H1 ≤ 270 reproduced; the epsilon-enlarged simplex cannot reach k ≤ 29 (Theorem 13); paper v0.3

- Certified M_55 ≥ 4.00516 (even power sums, degree 20) and M_54 ≥ 4.0023860 (degree 23, 1236 coefficients; 49 minutes, 10 GB). With the Lean tuple (54, 270) the project's end-to-end bound moved from 278 to 272 to 270, matching Polymath8b to every printed digit.
- Own idea (convex duality): a two-zone weight in Polymath8b's dual lemma, keeping the region of the marginals, proves M_{k,eps} < 3.99 for every k ≤ 29 and every eps < 1 (Theorem 13). 857 rational intervals, checked in flint ball arithmetic and again with mpmath intervals.
- Proposition 12: the enlargement gains exactly a factor 1+eps to first order, so any saving needs eps of size about 1/k. Noted a step in Polymath8b Prop. 6.5 we could not complete (Remark 14, Open).
- Lean: added Admissible.sublist and DHL.mono; the development builds with only propext and Quot.sound.
- Status table: added the 182 claim (GPT-6 Astra prompted by R. Sharifi) and the Nervous-Machine re-run of PrimeGaps186 (conditionally supported, not yet settled).

Did not work or is blocked:
- The 3:34 AM and 6:34 AM runs did not reach GitHub; the 6:34 run had produced v0.3 and sent the PDF, then errored. This session rebuilt all of it from the PDF.
- Jerry uploaded a git bundle of the lost 3:34 AM run: its M_54 certificate re-verifies exactly and gives the same value, an independent confirmation. Its other files were not merged; this session's rebuild is used.
- Remark 16 did not reproduce as drafted: exact fiber evaluation gives 4.178 (the weight is worse than scaling), not 4.146. The paper now gives the reproducible number.
- The 182 preprint could not be re-opened (too large for WebFetch, direct download refused); its details are as read by the earlier run.
- Theorem 13 is far from sharp: the expected threshold is near k = 50.

Next: Add the eps-enlarged simplex to mk_general.py and certify M_{50,1/25} > 4 (246). Own side: a sharper dual weight for small eps (Remark 16 says what it must do).

## 2026-11-12 - Session 2 (12:40 AM): All symmetric test functions: certified down to k = 56 (H1 ≤ 278 reproduced); rigidity on the enlarged simplex

- Proved an exponential-moment formula for simplex integrals of power-sum products (Lemma 3) and used it to build exact Gram matrices for every symmetric test function.
- Certified M_64 > 4 (all symmetric, degree 12), M_58 > 4 and M_56 ≥ 4.00519 (even power sums, degrees 16 and 18). The end-to-end bound inside the project moved from 578 to 278.
- Searched admissible tuples for k = 56..64 (diameters 278 to 330) and added them to the Lean development; it still builds with no sorry and only propext and Quot.sound.
- Own idea, with a helper agent: does Proposition 5 survive on Polymath8b's epsilon-enlarged simplex? Yes. A single rescaling closes the gap that naive slicing leaves (Proposition 8), and k = 3 numerics agree.
- A second helper read Polymath8b, Stadlmann and the 212 draft and wrote exact definitions of the enlarged supports to notes/sources-enlarged-supports.md. Key fact: with Bombieri-Vinogradov any epsilon < 1 is allowed.

Did not work or is blocked:
- M_55 reaches only 3.99153 at degree 18, so 270 (k = 54) is not yet reproduced.
- The first inverse-iteration version converged to a non-top eigenvalue; fixed by keeping the shift above the Polymath8b upper bound. Certified values were never affected (they are exact Rayleigh quotients).
- arxiv.org is blocked for direct downloads in this workspace; sources are read through WebFetch.

Next: Even power sums at degree 20 to 22 for k = 54 and 55 (estimate 6 to 15 minutes each), then add the epsilon-enlarged simplex to mk_general.py for k = 50.

## 2026-11-12 - Session 1 (setup): Survey, first certificates, first Lean build, one no-go result

- Surveyed the field. The 2014 record of 246 was passed in the week of 31 August 2026 by a run of preprints: 240 (Stadlmann), 236, 212 (DHL[45,2]) and 186 (DHL[40,2]). None was found fully verified independently; no claim below 186 was found.
- Built an exact-arithmetic pipeline for Maynard's sieve constant and reproduced M_105 > 4. Pushed the same family of test functions to k = 102, where it stalls.
- Searched for narrow admissible tuples for k = 2..55, 102 and 105. Every k up to 55 matches the published optimum. For k = 102 the search found diameter 578; a 576 search did not succeed.
- Wrote the Lean development (core Lean 4.35.0, no Mathlib, no sorry). It builds in about 15 seconds. Axioms used: propext, Quot.sound.
- Tested an idea of our own, the weighted pigeonhole. It cannot work; the proof became Proposition 5.

Did not work or is blocked:
- Mathlib cannot be built here (its cache host is blocked), so the analytic statements stay outside Lean for now.
- No 102-tuple of diameter 576 found.

Next: Generalise the test functions beyond P1, P2 to reproduce M_54 > 4 (270). In parallel, read Stadlmann's paper closely enough to write down her support region exactly.
