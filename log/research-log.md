# Research log

## 2026-11-13 - Session 12 (7:34 AM CT slot; started by hand at 7:44 AM CT; no wait, Sessions 10 and 11 had died unmerged): Rung 236: the second exact program confirms Song-Yue's capped numerator (exact equality with Jref); project bound 236, CONDITIONAL on their unverified equidistribution theorem; rescued Sessions 10-11; paper v0.11

- Rescued and merged the unmerged work of Sessions 10 and 11 (branches claude/zen-curie-b426c3 and claude/zen-curie-gstgp2; Session 10's last two commits were not in Session 11's branch and were merged separately).
- Resumed capped_exact.py --jonly from Session 10's checkpoint (5 of 126 pieces) and finished all 126 correction pieces (7.4 h wall on 4 cores, about 32 core-hours in all). Its J_T equals capped_check.py's J_T as an exact rational, so (99!)^2 (26!)^2 10^196 5^150 521^50 J_T = Jref by two independent programs; its cap-free I and J equal the monomial-basis I0 and J0. Criterion 48 J_T/I0 = 1.000664921591 > 2001/2000.
- So the variational step of 236 is reproduced, and the project's bound moves from 240 to 236 CONDITIONALLY: H1 <= 236 then follows from Song-Yue's Theorem 4.33 with their equidistribution Theorem 4.18, which we have NOT verified (caveat in the paper, status.json, README, bound history). Not a new bound.
- Observation: the j = 3 correction pieces are at most 1e-24 J but take most of the running time; recorded as an own idea (a rigorous a priori bound would make later second programs much cheaper).
- Rung 186: a helper transcribed the forms I_H, J_{lambda,H} and the 77-coefficient table of OpenAI's numerical companion (notes/sources-186-forms.md; checked against the source description in notes/sources-186.md); independent reproduction needs interval arithmetic (Dickman cell masses are transcendental), one formula (2.15) is underspecified.
- Paper v0.11: Proposition sy-exact now by two programs, new Corollary cor:236 (conditional), Remark oai186 extended; Lean audit now prints boundedGaps_236_of_DHL_48 (propext, Quot.sound only).

Explored: Toy capped problem at k = 3 with per-m caps (single-coordinate and pair-sum caps): pair caps give a smaller regain (4-8.5%) than single caps (up to 13%), so the cap pattern does not explain the 31% regain at k = 45 -- dead end.

Did not work or is blocked:
- Wolfram connector not available in this session; mathbox skills not available (no new proofs this run; the two exact programs and the reference integers are the checks).
- No news search (only the 3:34 AM run does it; that run, Session 11, left no record of one).
- No own proposition this run: the a priori bound for thin pieces is only an idea so far.

Next: Second program for our own k = 48 degree-22 vector (capped_exact --ckpt on P_kin48_D22r_u.json), with a rigorous bound for the j = 3 pieces if it can be proved; rung 186: decide whether an interval evaluator of I_H, J_{lambda,H} is feasible; rung 182: read the source.

## 2026-11-13 - Session 11 (3:34 AM CT slot; started while Session 10 was still running; died unmerged at about 4:15 AM CT): Rung 186 source notes; OpenAI's 40-tuple Lean-checked; second program on the Song-Yue witness restarted from its checkpoint; toy capped-problem exploration (did not merge; rescued by Session 12)

- Took over Session 10's branch as if it had died (its heartbeat was stale) although Session 10 was in fact still pushing; both runs stopped at about 4:15 AM CT, so neither merged.
- Read OpenAI's 186 preprint and its numerical companion (notes/sources-186.md): the criterion is a signed-minorant inequality over fragment-measure forms at k = 40, not a capped simplex ratio; checked only the final rational arithmetic of their (2.34)-(2.35) exactly.
- Lean: the 40-tuple of their display (1.3) is admissible of diameter 186 (boundedGaps_186_of_DHL_40'). Paper: Remark oai186 drafted.

Explored: Toy capped problem with one uniform cap at k = 2, 3: the regain of re-optimising on the capped region stays at most 13% (inconclusive; notes/explorations.md).

Did not work or is blocked:
- The run stopped before merging (container reclaimed); its work was merged by Session 12.

Next: Finish the second program on the Song-Yue witness.

## 2026-11-13 - Session 10 (scheduled 11:34 PM CT, 12 Nov; started work about 1:25 AM CT after waiting 1 h 50 min for Session 9 to merge); the run did not finish: its container stopped at about 4:15 AM CT before it merged, and Session 12 merged its work: Song-Yue's 236 witness recomputed exactly: our capped numerator and cap-free denominator equal their reference integers digit for digit (criterion 48 J/I0 = 1.000664921591 > 2001/2000); second program running; bound unchanged (240 conditional); paper v0.10

- Converted Song-Yue's 1295-row witness (degree 25, k = 48, all parts even) exactly into our power-sum format (code/songyue_convert.py; exact pointwise checks at random rational points).
- Cap-free denominator by a new monomial-basis program (partial-matching DP, 25 s): (98!)^2 10^192 5^150 521^50 I0 equals their 655-digit Iref exactly. Cap-free numerator the same way: 48 J0/I0 = 4.0036348167, Kintali's claimed uncapped value.
- Capped numerator by capped_check.py (56 min on 4 cores): (99!)^2 (26!)^2 10^196 5^150 521^50 J_T equals their 715-digit Jref exactly, a regeneration the authors list as pending. So 48 J_T/I0 = 1.000664921591 > 2001/2000 (4.0026597 in our scaling); with the capped denominator 4.0030988047, Kintali's claimed capped value. A fresh-context helper audited the four new scripts adversarially (sympy toy checks at k = 2-4) and found no errors.
- Second program: capped_exact.py got --jonly (skip I corrections) and --ckpt (exact per-piece checkpoint, resumable); its cap-free part agrees (4.0036348167); the 126 correction pieces take 25-45 min each at this degree, so it is unfinished (5 pieces done, checkpoint committed). The project bound stays 240 (conditional) until it matches.
- Paper v0.10: Proposition sy-exact and Remark rem:sta-lemma5; the status-table footnote now says the Lemma 5 step reads as Song-Yue describe.

Explored: Read the step of Stadlmann's Lemma 5 that Song-Yue (Remark 4.23) object to, in arXiv v1: in the range gamma in (1/2, 1/2+2 omega+eps] it applies the Type IIa lemma with the factors swapped, which needs a Siegel-Walfisz hypothesis on alpha that neither Lemma 5 nor Definition 9 (I) provides; a repair (checking the alphas that occur) was not attempted. Outcome: inconclusive, gap confirmed textually (notes/explorations.md).

Did not work or is blocked:
- Wolfram connector not available in this session; mathbox skills not available (a fresh-context helper did the computation audit).
- capped_exact.py on the Song-Yue witness needs roughly 5-10 hours on 4 cores; a first launch without checkpoints was restarted (4 pieces lost) to make it resumable. Not finished in this run.
- First fetch of Stadlmann's PDF came back as raw PDF bytes to the fetch helper; read locally with pdftotext instead.
- No news search (only the 3:34 AM run does it).

Next: Resume capped_exact --jonly --ckpt on the Song-Yue witness (STATE.md); if J_T matches, lower the project bound to 236 conditionally, with the caveat everywhere. Then the second program for our own k = 48 vector and rung 186.

## 2026-11-13 - Session 9 (11:34 PM CT, 12 Nov): Charton et al.'s Lemma 9.1 caps: ceiling 3.99 certified twice and the weights checked at a random point; optimum 3.98555, so a registered prediction failed; Kintali's 236 support gives 4.0061 > 4 with our own degree-22 vector (one program); bound unchanged (240 conditional); paper v0.9

- Lemma 9.1 caps (k = 45, 846-dim space): with the saved exact weights, 4 G_I - 45 G_J re-certified positive definite at 6500 bits with a different block split, and 3.99 G_I - 45 G_J as well, so no P in the space reaches 3.99.
- Schwartz-Zippel check of the reverse pass: at a random integer vector (entries in [-2^31, 2^31], seed recorded) the Gram weights reproduce I_T and J_T of capped_check.py exactly, so the quadratic forms agree with failure probability below 2^-31; the ball Gram forms contain the exact values.
- Optimum in the space: 3.98555 (Gram, floating point). The registered prediction 3.977-3.981 failed: re-optimising regains 31% of the truncation loss here against 9% at k = 49 (paper Remark 34).
- Rung 236: our cap-free optimiser at k = 48, degree 22 (1041 coefficients) certifies M_{48,15/506} ≥ 3.9589046, i.e. 4.0064115 without caps; on Kintali's support it gives 48 J_T/I_T = 4.0060814 > 4 (capped_check.py, exact; caps cost 0.00033). His claimed value with a transported k = 50 witness is 4.0031.
- Paper v0.9: Proposition 33 sharpened to < 3.99 with the random-point check, Remark 34 (failed prediction), Proposition 35 (Kintali 4.0061). The status table now notes Song-Yue's remark on a possible missing hypothesis in Stadlmann's Lemma 5 (unverified), and that both 236 preprints use the same D182 support.

Did not work or is blocked:
- capped_exact.py at the random point (k = 45) needs about 4 hours; stopped after 138 pieces. On Kintali's support capped_exact.py also needs hours (one correction piece took 9 minutes); stopped, so 4.0061 rests on one program.
- The degree-22 build at k = 48 was killed for memory once more before it ran alone.
- No news search (only the 3:34 AM run does it).

Next: Rung 236 via Song-Yue's published witness (notes/sources-236-song-yue.md): recompute their capped numerator J exactly and compare with Jref; second program for Kintali's support (capped_exact on P_kin48_D22r_u.json); capped_exact at the k = 45 random point.

## 2026-11-12 - Session 8 (5:51 PM CT, bonus run started by hand; called Session 7 in the trigger, but a Session 7 had already merged at 4:39 PM): Reverse-mode Gram matrices of the capped functionals: Charton et al.'s Lemma 9.1 caps cannot reach 4 in our 846-dim space (certified ceiling); P optimised on Stadlmann's support gives 4.0124 (two exact programs); bound unchanged (240 conditional); paper v0.8

- New tool code/capped_gram.py: the capped functionals I_T, J_T are linear in the coefficient products of P, so running the exact linear maps of capped_check.py backwards gives exact weights and hence the Gram matrices of the whole test space at the cost of one evaluation. Self-test: the weights reproduce I_T and J_T of capped_check.py exactly at k = 12 and k = 49.
- Stadlmann (k = 49, degree 20, 707 coefficients): the top eigenvector on the capped support gives k J_T/I_T = 4.0124198475 > 4; capped_check.py and capped_exact.py agree on I_T and J_T as exact rationals. Truncating the cap-free optimiser gave 4.0120389, so optimising on T regains only 0.00038 of the 0.0041 the caps cost.
- Charton et al., caps of their Lemma 9.1 (k = 45, degree 21, 846 coefficients): the weights pass the exact self-test, and 4 G_I - 45 G_J is certified positive definite in ball arithmetic (4800 bits), so no P in the space gives 45 J_T/I_T ≥ 4 with those caps. Their claimed 4.00438 (also 846 coefficients) must belong to their Table 3 caps. Reverse pass 88 min on two cores.
- Own idea: the re-optimisation gain is second order (about 9% of the truncation loss at k = 49); registered a prediction before the run that Charton et al.'s Lemma 9.1 caps reach only about 3.977-3.981 at degree 21. Added a rigorous ceiling mode (positive definiteness of sigma G_I - k G_J by recursive Schur complements in ball arithmetic), tested at k = 12.
- Rung 236: a helper read Kintali's preprint (checked against the PDF): k = 48, L = 1.042, tau = 0.982, g = 91/1250, one cap 1899/2500; claimed 4.0031 (4.0036 cap-free) with a public degree-25 witness. Lean: kintali_large_count (at most 10 large coordinates), kintali_extra_le_three. Our own cap-free degree-20 vector at k = 48 gives only 3.9994 < 4. Song-Yue's paper could not be downloaded (403).
- Paper v0.8: Propositions 31 (reverse-mode Gram matrices) and 32 (4.0124), the Kintali paragraph, abstract and programme updated.

Did not work or is blocked:
- Lemma 9.1 caps: the ceiling at 3.985 was not certified and the optimiser itself did not finish before the merge, so the optimum there (and the registered prediction 3.977-3.981) is not settled. The ceiling rests on one implementation of the reverse pass (no second program yet). Two earlier k = 45 runs lost workers to the memory limit.
- Degree-22 cap-free vector at k = 48 (for Kintali's support): killed twice for memory.
- No news search (only the 3:34 AM run does it).

Next: Second, independent check of the Lemma 9.1 ceiling (e.g. reduce memory, rerun with --load and a different precision, or a second implementation of G_J); then rung 236: k = 48 cap-free degree 22-24 alone on the machine and Kintali's support with capped_check.

## 2026-11-12 - Session 7 (4:39 PM CT, bonus run started by hand): Rung 212: Charton et al.'s capped criterion confirmed at k = 45 for their Table 3 caps (4.0027 > 4, two programs) but not for their Lemma 9.1 caps (3.9737); bound stays 240 (conditional); paper v0.7

- Extended both exact evaluators to caps that depend on m (code/capped_exact.py, code/capped_check.py, code/to_ucoords.py --params charton) and re-ran the k = 12 and k = 49 checks unchanged.
- Charton et al.'s support at k = 45 (L = 1.06, tau = 0.996, g = 0.0656, caps 4 B_{1,m} from their Table 3): our degree-21 cap-free optimiser truncated to T gives 45 J_T/I_T = 4.0027351 > 4. capped_check.py (13 min) and capped_exact.py (108 min, 228 pieces with j <= 6) agree exactly on I_T and J_T. Their claimed value with their own F is 4.00438; the caps cost us 0.0095 against the cap-free 4.012272.
- Located discrepancy: with the caps of their Lemma 9.1 (C(1) = C(2) = 31/50, C(s) = 17/25) the same P gives 3.9736870 < 4. So the conclusion depends on which cap set the draft intends; the project bound stays at 240 (conditional on Stadlmann's equidistribution estimates) and is not lowered to 212.
- Own idea: ceilings. The two-zone dual weight certifies the capped quantity <= 4.126 at k = 45 (and <= 4.14 at k = 49); cutting fibres at the largest coordinate barely changes it.
- Lean: charton_caps_valid (Stadlmann's admissibility condition for their caps, by decide), charton_large_count (at most 16 large coordinates), charton_extra_le_six. Paper v0.7: Proposition 29, Remark 30.

Did not work or is blocked:
- Lemma 9.1's caps: 3.9737 < 4 with our test function; not optimised on the capped support, so this is not a disproof.
- Still no test function optimised on a capped support (Gram matrices of the corrections not built).
- No news search (only the 3:34 AM run does it).

Next: Optimise P on the capped support (Gram matrices via capped_check's contractions) to settle Lemma 9.1's caps and report margins; then rung 236 (Kintali; Song-Yue): read the sources and record their supports.

## 2026-11-12 - Session 6 (12:39 PM CT, started by hand in place of the 3:34 PM slot): Variational step of Stadlmann's 240 reproduced exactly: capped ratio 4.0120 > 4 (two independent programs); project bound 240, conditional on his unverified equidistribution estimates; paper v0.6

- Proved an exact reduction of Stadlmann's capped functionals (Prop. 25): the fibre over u' is [0, min(R, max(g, C_{m+1} - s))], and I_T, J_T are the cap-free values minus three corrections, each a signed inclusion-exclusion sum (m <= 9 large coordinates, j <= 3 extra) of polygon integrals of polynomials in two variables. Implemented in exact rational arithmetic (code/capped_exact.py); checked by Monte Carlo at k = 12 where caps remove 47% of I, and by an exact internal second decomposition of I_T.
- For F = P 1_T with the degree-20 cap-free optimiser P, k J_T/I_T = 4.0120389 > 4 at k = 49 with Stadlmann's parameters (cap-free value 4.0161761). A helper wrote an independent exact evaluator from the definitions only (code/capped_check.py; direct sum over the exact large set, brute-force polytope tests for k = 2..5): I_T and J_T agree exactly as rationals.
- So the variational step of [Sta26] is independently reproduced; H1 <= 240 then follows from his Prop. 1 and his equidistribution theorem, which we have not verified. Project bound 240 (conditional), 246 still unconditional. The session-5 value 3.9597 was an artefact of the Cauchy-Schwarz bound; the caps cost only 0.0041 at degree 20 (losses 9e-7, 9e-5, 1.2e-3, 4.1e-3 at degrees 8, 12, 16, 20).
- Own idea: a ceiling. Every coordinate of T is <= 0.6 (Lean-checked), and the two-zone dual weight certifies the capped quantity <= 4.14; cutting fibres at 0.6 barely moves that weight (4.13785 -> 4.13753), so a sharper ceiling needs a weight that sees large coordinates.
- Lean: stadlmann_coord_le and stadlmann_extra_le_three (Caps.lean). Paper v0.6: Proposition 25, Theorem 26, Corollary 27 (conditional), Remark 28; abstract, status table and programme updated.

Did not work or is blocked:
- The test function was not optimised on the capped support itself (only the cap-free optimiser was truncated); the margin 0.012 is enough, but the true capped value is not known.
- The cap-aware dual ceiling gives essentially nothing beyond the cap-free ceiling (4.14).
- Stadlmann's new equidistribution estimates (the analytic input) remain unverified; no news search this run (only the 3:34 AM run does it).

Next: Return to the earlier balance: next rung 236 (k = 48, Kintali / Song-Yue) and 212 (k = 45, Charton et al.: test capped_check on their per-m caps against their claimed 4.00438); own ideas about half.

## 2026-11-12 - Session 5 (10:30 AM, started by hand in place of the 11:34 AM slot): Stadlmann's support: cap-free part certified, capped ratio 3.9597 (240 not yet reproduced); a floor for one-band hybrid supports; paper v0.5

- A helper re-read Stadlmann (arXiv:2608.31126) and Charton et al. (bgp212.pdf) and confirmed the support, the criterion and the parameters (k = 49, eps = 0.0075, A1 = 0.253, delta = 0.028, caps 0.15/0.15/0.17; k = 45 for Charton et al.); both use one band. Notes in notes/stadlmann-recheck-s5.md.
- By dilation, the cap-free version of Stadlmann's functional is (253/250) M_{49,15/506}; certified M_{49,15/506} ≥ 3.9685535 (degree 20) gives 4.016176 > 4. For Charton et al.'s parameters the cap-free value is ≥ 4.012272 (degree 21, 846 coefficients, matching their basis dimension), against their claimed 4.00438 with caps.
- Added the caps: exact integrals over {m coordinates above delta, sum above the cap} with shifted power sums (checked against Lemma 3 and sympy), a rigorous bound for the capped functional (Proposition 23), and a penalised eigenproblem. Best certified capped ratio at k = 49: 3.95972 (degree 20), below 4, so 240 is not reproduced.
- Own idea: dilation plus the two-zone dual weight gives the first rigorous floor for one-band hybrid supports (Theorem 25): whatever delta, caps and minorant, no k ≤ 28 at Stadlmann's level omega = 0.003 (and 1/300), no k ≤ 26 at omega = 0.007, no k ≤ 22 for omega ≤ 1/68. Certified in ball arithmetic and re-checked with mpmath.iv.
- Lean: Caps.lean (length × g ≤ sum for entries above g; at most 9 large coordinates, and 7 large coordinates exceed every cap). Paper v0.5: new Section 5, Propositions 22-24, Theorem 25.

Did not work or is blocked:
- The capped criterion is not reproduced: 3.95972 < 4 at degree 20. The Cauchy-Schwarz bound for the capped marginals forces P to be small on the cap-violation set, costing about 0.056 against the cap-free 4.0162.
- A union bound that dropped the condition 'each coordinate above delta' was useless (E/I ≈ 146).
- The floor of Theorem 25 is far from the truth (28 vs 49) and the two-zone weight fails at the next k for every omega tried.
- No news search this run (only the 3:34 AM run does it).

Next: Exact capped marginals J_T(P 1_T) (fibres of T, not only integrals over the violation set), then optimise P on T directly; a degree-22 capped run was started this session (see STATE.md). Own side: a floor that uses the caps, or the Collatz-Wielandt weight.

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
