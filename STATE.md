# Handoff (rewrite this file at the end of every session)

Home: GitHub repo jerryckim16/twin-primes (branch main). Website (GitHub Pages, from docs/): https://jerryckim16.github.io/twin-primes/
Each session works on the claude/... branch its system instructions name (create it from the latest origin/main), opens a pull request and merges it (squash).

## POSITION (after Session 48, 11:34 AM CT slot of 23 Nov, run 17:35 UTC 23 Nov): PHASE B
- Bounds: established 246; claimed 182; project 236 CONDITIONAL (caveat everywhere), 240 conditional, 246 unconditional. Unchanged.
- PHASE B. Time split: ~35% parity programme, ~25% other small results (3g), ~20% bound work, ~15-20% exploration.
- Papers: verification-note v1.0.1 FROZEN; parity-barrier v1.0.1 FROZEN (v1.1 revision in preparation: material staged in
  papers/parity-barrier/v11/, NOT yet in main.tex; see v11/README.md); main paper v0.48 (33 pp.).
  Active lines (review of 23 Nov): main paper as an index; a short Lean note for programme (4) (after the k-dimensional
  identity, or after 6 runs); the single parity v1.1 revision. Paused: toolkit note (5), H_m, rung 182.
- Weekly review: notes/reviews/2026-11-23.md (read section 8, the coordinator's decisions). Next review: the first run
  starting on Monday 30 Nov, Central time (normally the 3:34 AM CT run).
- LWW flag (arXiv:2610.20242, still v2 on 23 Nov) open; see notes/flags-for-jerry.md.

## Next steps (in order; from the review of 23 Nov, updated in Session 48)
1. Bound share: the 186 majorisation lemmas, ONE per run, in order 1.6, 1.7, 2.3, 2.4 (1.4 done S47, 1.5 done S48:
   notes/oai186-lemma15-check.md, code/oai186_lemma15_check.py, 44 exact checks, verified as stated; the PDF is
   code/third_party/openai186/short_gaps_numerics.pdf, transcription notes/sources-186-loss.md). Then settle which threshold
   the restoration step (Prop. 4.6 of the main 186 paper) needs (prop:oai186-budget). NO per-run regressions:
   code/cap6/regress_all.py at most monthly; add the 186 main terms and outer parts when it is next run.
2. Parity v1.1 (see papers/parity-barrier/v11/README.md): (a) literature check DONE (S47 + S48, notes/sources-lww26.md);
   (b) subsection DRAFTED (v11/lww-transfer.tex; needs bib entries Wan26, HLWW26, BH98, Din25 taken from their pages);
   (c) ONE remark merging the E2 cards (S32, S33, S36); (d) one "Further tests" paragraph (S37, S38, S42, S46, S47,
   S43-S45 together, S34+S35, S48 Merikoski; S41 only after Tao-Teraeväinen 2019 is opened); (e) integrate into main.tex
   (placement in v11/README.md), one referee lane, cosmetic items (item 7 below), refreeze as v1.1. Folklore checks first.
3. Parity attempts: one per run (Jerry's rule), each with a pre-stated success outcome NOT implied by the paper's class.
   Mechanisms of the review of 23 Nov now all touched: Green / Granville-Shao (S47, located), Merikoski (S48, located:
   the root large sieve does not help; Merikoski's multiplicative-large-sieve argument is unpublished, GS ref [16]
   forthcoming), LWW mu-versus-lambda (Remark 1 re-read S48: "very likely applicable to ... the Liouville function", not
   pursued by them; a card on what their Sections 2-3 need from mu would still be new). Next: that LWW card, or new
   mechanisms for the review of 30 Nov to choose.
4. Lean: k-dimensional Maynard identity, one lemma per run: MaynardInv.lean (S48) has tuple Moebius inversion (all R, k)
   and the lambda <-> y round trips, conditional on MuSign c (mu(a)mu(x) = mu(x/a), a | x | c squarefree), checked by
   decide for c <= 30. Next: prove MuSign for all squarefree c (multiplicativity of the recursive mu), then
   mu(prod r_i) = prod mu(r_i) for coprime entries, then the diagonalisation of S1 in y.
5. Main paper: bump the version only when content changes; keep sec:related as an index.
6. Paused: rung 182 (restoration data unpublished); k = 3 GEH thread (stopped); H_m; toolkit note.
7. Deferred minor items of the parity referee (cosmetic): label keys prop:/cor: on remarks, bib key Cit26, journal pages for
   MR16, GT10, GT12 (do them inside v1.1).
8. Exploration follow-up (optional, cheap): derive the Montgomery-Soundararajan-type prediction for the twin short-interval
   variance (S48 measured slope 0.51 at 1e8 and 1e9, against a rough 1/log x-decaying guess); see notes/explorations.md.

## Session 48 (11:34 AM CT slot of 23 Nov, started on time 17:35 UTC; no wait) -- additions
- Bound share: 186 Lemma 1.5 (full-radius factor W_r) verified as stated: code/oai186_lemma15_check.py (/usr/bin/python3;
  ~20 s, ~35 MB; .out), 44 exact checks, 0 failures; our four loss programs and the authors' script use the same factor;
  notes/oai186-lemma15-check.md. Helper-written; re-run here, identical output. One program.
- Lean: TwinPrimes/MaynardInv.lean (box, tdvd, tmuq, upSum, mobInv, tuple_mobius_lower/upper, mobInv_upSum, upSum_mobInv,
  maynardY, maynardLam, maynard_lam_of_y(_sqfree), maynard_y_of_lam(_sqfree), signOK_of_entries, muSignCheck_31,
  maynard_inversion_R30('), examples incl. a failing non-squarefree case; helper agent, statements checked here; in
  Audit.lean, 18 lines); lake build and Audit.lean pass (propext / Quot.sound / Classical.choice only).
- Parity attempt: route card notes/parity-attempts/2026-11-23-merikoski-large-sieve.md (located: this route does not help).
  Sources (PDFs not committed): Merikoski arXiv:2112.03617v3 (SHA-256 d7555c65...ae819), Green-Sawhney arXiv:2410.04189v3
  (741b8ebc...4e5a4e), Grimmelt-Merikoski-Pandey-Pascadi arXiv:2610.41356v1 (Sect. 1 only). Script
  code/parity/merikoski_root_large_sieve.py (/usr/bin/python3 -I; ~3 s; .out). Fresh-context adversarial audit: 5 errors
  (incl. a wrong quantification of the root-sieve defect and a misidentification of FI98's (B)) and several overstatements,
  all fixed in the card.
- Parity v1.1: literature check (a) done (notes/sources-lww26.md, Session 48 section: SHA-256 of LWW v2 corrected to
  ...2423d000 (our earlier records had a transcription slip); HAL v1 hal-05793028; three citing works opened; 12 web
  searches + arXiv API + OpenAlex; Semantic Scholar 429 and Google Scholar 403, not needed). Subsection (b) staged in
  papers/parity-barrier/v11/lww-transfer.tex.
- Exploration: code/explore/twin_short_variance.py [X] (/usr/bin/python3 -I; ~30 s, ~1.5 GB at 1e9; .out): inconclusive.
- Main paper v0.48 (Theorem 1 item 17; rem:186-status Lemma 1.5). Wolfram and mathbox NOT available. No news search
  (not the 3:34 AM run).

## Session 47 (3:34 AM CT slot of 23 Nov, started on time 09:35 UTC; no wait) -- additions
- Weekly review notes/reviews/2026-11-23.md (fresh-context helper; facts checked; coordinator decisions in section 8).
- News search: nothing changes the numbers. LWW still v2. Secondhand mention (163.com, 4 Sep 2026, Machine Heart) of a
  "188" formal proof by an Anthropic team: no primary source, not recorded as a claim. Sharifi's page unchanged (182 bundle).
  Yang arXiv:2609.24347, 2608.13299 (densities of P^+(p-1) >= p^c) do not affect the 0.677 comparison.
- Parity attempt: notes/parity-attempts/2026-11-23-granville-shao-level-half.md (located; audited: 3 errors incl. a
  sieve-size miscount, fixed). Sources: Green arXiv:1604.04481v4, Granville-Shao arXiv:1703.06865v2 (SHA-256 in the card;
  PDFs not committed). Script code/parity/green_example_check.py (.out). Minor flag: Green p. 2 example misprinted.
- Exploration: code/explore/shifted_prime_fourier.py [X] [log2M] (/usr/bin/python3 -I; 50 s at 1e8, 2^27; ~5 GB; .out): dead end.
- Bound share: 186 Lemma 1.4 verified as stated (code/oai186_lemma14_check.py, 18 s, exact; notes/oai186-lemma14-check.md;
  re-run by the coordinator, identical output). Last regression batch: code/cap6/compare_loss_inner_regen_s47.json
  (one Arb radius differs, explained there). code/cap6/regress_all.py written (240 / 236 / 17 inner jobs; untested end to end).
- Lean: TwinPrimes/MaynardS1.lean (tupleDvd, mSieveSum, maynard_S1_expand(_W), tupleDvd_lcm, crt_tuple_residue,
  crt_tuple_count_bounds, maynard_S1_error, example; helper agent, checked here); in Audit.lean; build and audit pass.
- Main paper v0.47. Log: the 14 Nov entries merged into one daily summary (log/archive-2026-11-14.json).
- Wolfram and mathbox NOT available.

## Session 46 (7:34 PM CT slot of 22 Nov, started on time 01:35 UTC 23 Nov; no wait) -- additions
- Parity attempt: route card notes/parity-attempts/2026-11-23-katai-bsz-dilation.md (refuted as a route in the classical
  form; located in the growing-range form). Source read: Bourgain-Sarnak-Ziegler arXiv:1110.0992v1, Thm 2, Sect. 2 and
  p. 13 (SHA-256 dee51b51...c44a; PDF not committed). Script code/parity/katai_dilation.py [X] (/usr/bin/python3 -I;
  ~40 s at 1e8, ~4 GB; .out). One web search (literature scope recorded in the card). Fresh-context adversarial audit:
  2 errors (no-go argued from a fixed pair; cross-term equivalence wrong for p > w), 2 gaps, 4 slips; all fixed.
- Exploration: code/explore/dilation_second_moment.py [X] (/usr/bin/python3 -I; ~2 min at 1e8, ~3 GB; .out): inconclusive.
- Lean: TwinPrimes/SelbergEq.lean (selbergEqY/T/Lam, selbergEqT_sum, selbergEq_Y, selbergG_pos, selbergEq_lam_one,
  selbergEq_LHS, selberg_lower_eq, selberg_lower_attained, selbergEq_D6; helper agent, statements checked here; in
  Audit.lean); lake build and Audit.lean pass. Selberg.lean docstring updated.
- Bound share: from-scratch regression of 3 more of the 17 inner-loss parts of 186 (I2new L1,L2,L3; I2new L4,L5,L6;
  I5/2old L4,L5,L6): /usr/bin/python3 code/oai186_loss_inner.py --group G --comp C --part code/cap6/loss_inner_regen_s46/<part>.json
  (one core each, ~20 min, ~1.4-1.6 GB, python-flint); identical to the committed code/cap6/loss_inner/ parts
  (code/cap6/compare_loss_inner_regen_s46.py -> .json). One program only. 6 of the 17 inner parts now re-run (S45 + S46).
- Main paper v0.46. Wolfram and mathbox NOT available. No news search (not the 3:34 AM run).

## Session 45 (11:34 AM CT slot of 22 Nov, started on time 17:34 UTC; no wait) -- additions
- Parity attempt: route card notes/parity-attempts/2026-11-22-switching-rung3.md (refuted at level 1/2; located for a common
  level, theta* = 0.5692 for kappa = 2/3). Script code/parity/switch_ladder.py [X] (/usr/bin/python3 -I; ~3 min at 1e8,
  ~1.5 GB, scipy; .out). No new source opened. Fresh-context adversarial audit: 2 errors (one-sided level comparison;
  "parity-blocked whatever the level"), 1 slip (V(z) excludes l = 2), 4 gaps; fixed / recorded in the card.
- Exploration: code/explore/twin_dispersion.py [X] (/usr/bin/python3 -I; 10 s at 1e8, ~1 GB; .out): inconclusive (curiosity).
- Lean: TwinPrimes/Cosets.lean (cnt, A/B recursion, cnt_eq_AB, AB_closed, coset_count_zero, coset_count_nonzero,
  coset_prob_two, coset_count_three, small decide checks; helper agent, statements checked here; in Audit.lean);
  lake build and Audit.lean pass.
- Bound share: from-scratch regression of 3 of the 17 inner-loss parts of 186 (I2old L2,L3; I5/2old L1,L2,L3;
  I5/2new L7,L8,L9): python3 code/oai186_loss_inner.py --group G --comp C --part code/cap6/loss_inner_regen_s45/<part>.json
  (one core each, ~16 min, ~1.5 GB, python-flint); identical to the committed code/cap6/loss_inner/ parts
  (code/cap6/compare_loss_inner_regen_s45.py -> .json). One program only. The other 14 inner parts and the outer ones
  were not re-run.
- Main paper v0.45. Wolfram and mathbox NOT available. No news search (not the 3:34 AM run).

## Session 44 (3:34 AM CT slot of 22 Nov, started on time 09:34 UTC; no wait) -- additions
- News search (3:34 AM run): nothing new; LWW still v2 (19 Nov); no report on 240/236/186/182 verification found.
- Parity attempt: route card notes/parity-attempts/2026-11-22-level-ladder.md (located). Script code/parity/level_ladder.py [X]
  (/usr/bin/python3 -I; ~85 s at 1e8, ~1.2 GB; .out). Sources read with pdftotext (PDFs not committed): Lichtman
  arXiv:2309.08522v1 (SHA-256 665693af...98c55b5), Maynard arXiv:2006.07088v1 (04516b14...4bb4), Gaudet arXiv:2408.01610v1
  (d5bfce37...0d04e1). Fresh-context adversarial audit: 5 errors, 4 gaps, all fixed (recorded in the card); the
  conclusion is narrowed to the pure beta-sieve at z = x^{1/2}; switching at z = x^{1/3} is the first unresolved step.
- Exploration: code/explore/kappa_universality.py [X] (/usr/bin/python3 -I; ~40 s at 1e8, ~2 GB; .out): inconclusive (curiosity).
- Lean: TwinPrimes/SelbergOpt.lean (mu, mu_divisor_sum, mu_upto_12, weighted_cauchy_schwarz, mu_y_sum, selberg_lower,
  selberg_lower_D6_consts; helper agent, statements checked here; in Audit.lean); lake build and Audit.lean pass.
- Bound share: from-scratch regression of the 186 main terms: code/oai186_IH.py and code/oai186_J.py re-run (one core each,
  355 s and 1141 s; need gmpy2: python3 -m pip install --break-system-packages gmpy2): identical to the committed
  code/oai186_IH.json and code/oai186_J.json in every field (code/cap6/compare_oai186_regen_s44.json; outputs
  code/cap6/oai186_*_regen_s44.json). One program only (program 1 of the two); the loss bound L+ was not re-run.
- Log: the four 13 Nov entries merged into one daily summary (log/archive-2026-11-13.json).
- Main paper v0.44. Wolfram and mathbox NOT available.

## Session 43 (7:34 PM CT slot of 21 Nov, started on time 01:35 UTC 22 Nov; no wait) -- additions
- Parity attempt: route card notes/parity-attempts/2026-11-22-dimension-ladder.md (located; conditional on EH and the
  beta-sieve theorem as quoted). Script code/parity/dim_ladder.py [X] (/usr/bin/python3 -I; ~80 s at 1e8, ~1 GB; .out).
  Sources (helper, PDFs not committed): Gaudet arXiv:2408.01610v1, Blight thesis (Rutgers 2010), Ford sieve notes 2023,
  Teräväinen arXiv:1611.08585v2, Shute arXiv:2209.08949v2, Campbell arXiv:2603.10356v2 (SHA-256 in the card).
  Fresh-context adversarial audit: 3 errors, 5 gaps, fixed (recorded in the card).
- Exploration: code/explore/shifted_prime_sign_entropy.py [X] (/usr/bin/python3 -I; 7 s at 1e8, ~1.5 GB; .out): dead end.
- Lean: TwinPrimes/Gauss.lean (gauss_totient for all n >= 1; selberg_diag for all D; helper agent, statements checked
  here; in Audit.lean); lake build and Audit.lean pass. Selberg.lean docstring updated.
- Bound share: regression of the 236 evaluation: capped_check.py re-run from scratch on code/cap6/P_sy236_u.json (3464 s,
  3 procs, ~2 GB/worker, /usr/bin/python3 with python-flint) equals the committed check_sy236.json exactly (I_T, J_T;
  48 J_T/I_T = 4.0030988048); code/cap6/compare_sy236_regen_s43.json, check_sy236_regen_s43.json. One program only.
- Main paper v0.43. Wolfram and mathbox NOT available. No news search (not the 3:34 AM run).

## Session 42 (11:34 AM CT slot of 21 Nov, started on time 17:34 UTC; no wait) -- additions
- Parity attempt: route card notes/parity-attempts/2026-11-21-linnik-ladder.md (located; no-go inside the paper's class).
  Script code/parity/linnik_ladder.py (/usr/bin/python3 -I; 46 s, ~1 GB; .out). Sources read: MRT arXiv:1707.01315v3
  pp. 2-7 (SHA-256 e93924c5...9a493a1), Ford-Maynard arXiv:2407.14368v1 pp. 1-4, 19-22 (SHA-256 3ca80785...76d2301).
  Fresh-context adversarial audit (recorded in the card). Helper-written; findings checked here.
- Exploration: code/explore/twin_error_spectrum.py [X] (/usr/bin/python3 -I; 6 s at 2e8, ~0.6 GB; .out): dead end.
- Lean: TwinPrimes/Linnik.lean (stirling2, linnik_stirling for ALL r by telescoping, orderedFact_squarefree_check;
  helper agent, statements checked here and values checked in Python); in Audit.lean; lake build and Audit.lean pass.
- Bound share: regression of the 240 certificate: capped_check.py re-run from scratch on code/cap6/P_capfree_D20_u.json
  (250 s, 3 procs; needs python-flint: /usr/bin/python3 -m pip install --break-system-packages python-flint) equals the
  committed check_capfree_D20.json and res_capfree_D20.json exactly (code/cap6/compare_capfree_D20_regen_s42.json).
  Note: code/stadlmann_caps.py (the superseded union-bound method) gives a negative lower bound by design; not a regression.
- Main paper v0.42. Wolfram and mathbox NOT available. No news search (not the 3:34 AM run).

## Session 41 (3:34 AM CT slot of 21 Nov, started on time 09:34 UTC; no wait) -- additions
- News search: nothing new; LWW arXiv:2610.20242 still v2, no public comment found.
- Parity attempt: route card notes/parity-attempts/2026-11-21-large-q-pellet.md (located). Sources read (PDFs not
  committed): Carmon-Rudnick arXiv:1205.1599v3 (SHA-256 8148dcfa...4b86), Bary-Soroker arXiv:1206.3930v3 (aed115a8...b1c0),
  Rudnick arXiv:1501.01769v1 (cc59f8c9...c994). Script code/parity/large_q_pellet.py [X] (/usr/bin/python3 -I; 3 s; .out).
  Fresh-context adversarial audit (3 errors, gaps; fixed; recorded in the card).
- Exploration: code/explore/digit_pellet.py [p k] (/usr/bin/python3 -I; 5-10 s; .out): dead end.
- Lean: Selberg.lean + selberg_sos_D6, selberg_opt_D6, selberg_opt_D6_eq, selberg_opt_D6_eq_iff (helper agent; numbers
  checked here in Python; in Audit.lean); lake build and Audit.lean pass.
- Main paper v0.41 (thm:lean item 13 extended; Related results sentence; 186 account condensed). Wolfram and mathbox NOT available.

## Session 40 (7:34 PM CT slot of 20 Nov, started on time 01:35 UTC 21 Nov; no wait) -- additions
- Parity attempt: route card notes/parity-attempts/2026-11-21-lww-main-term.md (located; conditional implication
  complete in outline). Source read: LWW arXiv:2610.20242v2 pp. 4-5, 7-18, 61, 63, 69-70 (same SHA-256). Fresh-context
  adversarial audit (recorded in the card; Findings 1-3 hold, count and wording corrected, side remark rewritten).
- Exploration: code/explore/fake_target_density.py [H AMAX] (/usr/bin/python3 -I; 4 s; .out): dead end.
- Lean: TwinPrimes/Selberg.lean (gauss_totient_upto, selberg_diag_D6, selberg_diag_example; helper agent, statements
  checked here; in Audit.lean); lake build and Audit.lean pass.
- Main paper v0.40. Wolfram and mathbox NOT available. No news search (not the 3:34 AM run).

## Session 39 (11:34 AM CT slot of 20 Nov, started on time 17:34 UTC; no wait) -- additions
- Parity attempt: route card notes/parity-attempts/2026-11-20-lww-orbit-test.md (located; conditional implication, one gap).
  Sources read: LWW arXiv:2610.20242v2 pp. 4-11, 14-19 (audit helper: also pp. 61-71); R. Li arXiv:2508.18285v3
  (SHA-256 8e892c00...7003), Ding arXiv:2510.04026v2 (SHA-256 192e0b23...0af9), introductions only. Fresh-context audit
  (recorded in the card). Baker-Harman 1998 not opened (notes/sources-needed.md).
- Exploration: code/explore/dilation_variance.py [HMAX seed] (/usr/bin/python3 -I; 2 s; .out): dead end.
- Lean: TwinPrimes/Orbit.lean (orbit_sign, orbit_two_step, orbit_example_*; helper agent, statements checked here; in
  Audit.lean); lake build and Audit.lean pass.
- Main paper v0.39. Wolfram and mathbox NOT available. No news search (not the 3:34 AM run).

## Session 38 (3:34 AM CT slot of 20 Nov, started on time 09:34 UTC; no wait) -- additions
- News: LWW26 (above). Script code/parity/lww_numerics.py [X] (/usr/bin/python3 -I; ~3 min at 1e9, < 1 GB; .out).
  Source read: arXiv:2610.20242v2 (SHA-256 7ac34131...2d423000), Sections 1, 2.2-2.3, 4.1, Prop. 4.2 statement.
- Parity attempt: route card notes/parity-attempts/2026-11-20-odd-order-chowla.md (located). Script
  code/parity/odd_chowla_class.py (/usr/bin/python3 -I; 7 s; .out). Sources: TT arXiv:1708.02610v2, 1710.02112v1.
  Fresh-context adversarial audit (recorded in the card).
- Exploration: code/explore/ap3_targets_classes.py [NMAX] (8 s; .out): inconclusive (curiosity).
- Lean: TwinPrimes/Fano.lean (4 theorems, decide, maxRecDepth 20000), in Audit.lean; lake build and Audit.lean pass.
- Parity paper v1.0.1 (status note only); main paper v0.38. Wolfram and mathbox NOT available.

## Session 37 (7:34 PM CT slot of 19 Nov, started on time 01:34 UTC 20 Nov; no wait) -- additions
- Parity attempt: route card notes/parity-attempts/2026-11-20-almost-prime-tuples.md (located; consistency test).
  Script code/parity/almost_prime_tuples.py (/usr/bin/python3 -I; 2 s; .out). Sources (arXiv PDFs, not committed):
  Lewulis 2203.09432v1, 1806.09034v3; Maynard 1205.4610, 1205.5021; Franze 1111.2003. Fresh-context audit (in the card).
- Exploration: code/explore/weighted_omega_targets.py [KMAX AMAX] (3.5 s; .out): dead end.
- Lean: Counting.lean s2Count, s2_expand, s2_error, s2_expand_example (helper agent; statements checked here);
  Parity.lean omega4_no_weakly_fair_weight, omega3_weight. All in Audit.lean; lake build and Audit.lean pass.
- Main paper v0.37 (thm:lean item 10). Log: 12 Nov entries merged into one daily summary (log/archive-2026-11-12.json).
  Wolfram and mathbox NOT available. No news search (not the 3:34 AM run).

## Session 36 (11:34 AM CT slot of 19 Nov, started on time 17:34 UTC; no wait) -- additions
- Parity attempt: route card notes/parity-attempts/2026-11-19-e2-polynomial-gauge.md (proved (located), model-restricted).
  Scripts: code/parity/e2_poly_gauge.py [cert.json] (/usr/bin/python3 -I; ~10 min, sympy + scipy; .out; writes
  code/parity/e2_poly_gauge_cert.json), code/parity/e2_poly_gauge_check.py [cert.json] (independent exact check, 0.5 s; .out).
  Fresh-context adversarial audit (recorded in the card).
- Exploration: code/explore/ramanujan_twin_blind.py [X QMAX] (15 s at 1e7; .out): dead end (Ramanujan coefficients of
  prime-supported weights only see the mean).
- Lean: TwinPrimes/Counting.lean crt_* (11 theorems, in Audit.lean; written by a helper agent, statements checked here);
  lake build and Audit.lean pass.
- Main paper v0.36 (thm:lean item 9; Kintali account condensed). Wolfram and mathbox NOT available. No news search
  (not the 3:34 AM run).

## Session 35 (3:34 AM CT slot of 19 Nov, started on time 09:34 UTC; no wait) -- additions
- Parity attempt: route card notes/parity-attempts/2026-11-19-smooth-middle-bilinear.md (located). Script
  code/parity/middle_bilinear.py [X A seed] (/usr/bin/python3 -I; ~5 min and ~2 GB at X = 1e8, A = 3000; .out).
  Source read: Kontorovich math/0507569v3 pp. 1-6. Fresh-context audit (recorded in the card).
- Exploration: code/explore/liouville_twin_centres.py [K] (76 s at 1e8; .out): dead end.
- Lean: TwinPrimes/Counting.lean (countDvd_bounds, countDvd_eq, countRes_bounds, selberg_expand, selberg_error + list-sum
  helpers; in Audit.lean); lake build and Audit.lean pass. Written by a helper agent, statements checked here.
- Main paper v0.35 (thm:lean item 8; Song-Yue recomputation account shortened). News search: nothing new.
  Wolfram and mathbox NOT available.

## Session 34 (7:34 PM CT slot of 18 Nov, started on time 01:35 UTC 19 Nov; no wait) -- additions
- Parity attempt: route card notes/parity-attempts/2026-11-19-green-sawhney-gowers-type-ii.md (located). Script
  code/parity/gs_norm_form_check.py [X] [PKAPPA] (/usr/bin/python3 -I; < 1 min at 1e9, ~0.7 GB; .out). Fresh-context audit:
  3 errors in the draft, fixed (recorded in the card).
- Exploration: code/explore/gs_twin_carry.py [X] [Q...] (~1 min at 1e9; .out): dead end.
- Lean: Reduction.lean + lt_of_two_sided, good_m, eventually_lt_of_asymptotics, sieveInequality_of_asymptotics,
  boundedGaps_246_of_asymptotics_50 (in Audit.lean; `grind` used for two polynomial identities). lake build and Audit pass.
- Main paper v0.34. Wolfram and mathbox NOT available. No news search (not the 3:34 AM run).
- Setup note: /usr/bin/python3 is 3.13 here and needed `/usr/bin/python3 -m pip install --break-system-packages scipy ...`.

## Session 33 (11:34 AM CT slot of 18 Nov, started on time 17:35 UTC; no wait) -- additions
- Parity attempt: route card notes/parity-attempts/2026-11-18-e2-odd-cycles.md (proved (located), model-restricted).
  Scripts: code/parity/e2_odd_cycles.py [d maxlen A0 mults] (seconds; .out), code/parity/e2_cycle_cert.py (exact, 0.3 s; .out).
  Fresh-context audit: no errors, gaps fixed.
- Exploration: code/explore/e2_quadratic_hyperedges.py [AMAX BMAX] (< 1 s; .out): dead end.
- Lean: TwinPrimes/Reduction.lean (6 theorems, in Audit.lean); lake build and Audit.lean pass.
- Main paper v0.33. Wolfram and mathbox NOT available. No news search (not the 3:34 AM run).

## Session 32 (3:34 AM CT slot of 18 Nov, started on time 09:34 UTC; no wait) -- additions
- Parity paper v1.0 (frozen): restructured from 33 to 24 pages (see notes/parity-programme.md, Session 32), five-lane referee
  pass referee/2026-11-18-parity-barrier-v1/ (report.md + lane files) applied, plus a sixth helper checking the fixes.
- Parity attempt: route card notes/parity-attempts/2026-11-18-e2-consistency-test.md (consistent); script
  code/parity/e2_consistency.py (/usr/bin/python3, ~2 min), output .out.
- Exploration: code/explore/parity_margin_lp.py (1.5 s), output .out: parity-margin LP is a tautology (dead end).
- Main paper v0.32 (Related results: parity paper frozen, entry shortened). News search (3:34 AM run): nothing new.
- Lean: lake build and Audit.lean pass (no Lean changes). Wolfram and mathbox NOT available.

## Session 31 (7:34 PM CT slot of 17 Nov, started on time 01:35 UTC 18 Nov; no wait) -- additions
- Parity paper v0.16: Remark rem:gm (Fejér averages, pair correlation, scale log X), open question oq:mrtcond relabelled and
  partly answered, bib Mer16, Gol04, MS04, KS19; changelog order fixed. Fresh-context audit (3 errors, 4 gaps; all fixed).
  Route card notes/parity-attempts/2026-11-18-pair-correlation-variance.md.
- Scripts: code/parity/variance_fejer.py [X KMAX] (/usr/bin/python3 -I; 2 min at 1e8, < 2 GB), output .out;
  exploration code/explore/ff_ball_variance.py q n (python-flint; seconds for q^n <= 2e4; q = 13, n = 5 is too slow), output .out.
- Sources: hashes in notes/parity-programme.md (Session 31 section).
- Main paper v0.31: rem:oai186 condensed; Related results item for rem:gm; history item.
- Lean: lake build and Audit.lean pass (no Lean changes). Wolfram and mathbox NOT available. No news search (not the 3:34 AM run).

## Session 30 (11:34 AM CT slot of 17 Nov, started on time 17:35 UTC; no wait) -- additions
- Parity paper v0.15: Remark rem:lt22 (LT22 arXiv:2111.08912v3 read in full, SHA-256 87410676...68464014; bib LT22),
  rem:ford-twin updated; referee items 2.6, 2.7, three labelling items. Audit notes/audit-parity-v015.md (5 errors, 3 gaps in
  the first draft, all fixed). Route card notes/parity-attempts/2026-11-17-hybrid-averages-mean-gap.md.
- Script: code/parity/hybrid_shifted_primes.py [X HMAX] (/usr/bin/python3 -I; ~2 min at 2e7, < 2 GB); output .out
  (also the exploration: Polya-type bias across shifts, inconclusive).
- H_m scoping: code/hm/mpz_region_check.py (exact, seconds; .out); notes/hm-programme.md section 6. Sources read: Stadlmann
  2309.00425v3 pp. 8-9, PM8a 1402.0811 Def. 2.6 / Lemma 2.7 / Thm 2.8 / Remark 3.2, Stadlmann 2608.31126v1 Lemmas 3-7.
- Main paper v0.30 (Related results, history item). Lean: lake build and Audit.lean pass (no Lean changes).
- Wolfram and mathbox NOT available. No news search (not the 3:34 AM run).

## Session 29 (3:34 AM CT slot of 17 Nov, started on time 09:34 UTC; no wait) -- additions
- Parity paper v0.14: subsec:mrt17 (Literature: MRT17 Thm 1.3(i), footnote 4, p. 5; MRT15 and MRT17b abstracts), Remark
  rem:mrt17 (window identity, second difference, location), open question on conditional ranges; bib MRT17, MRT17b; FI98b and HB01
  digests halved. Audit notes/audit-parity-v014.md (3 errors, 5 gaps, fixed). Route card
  notes/parity-attempts/2026-11-17-mrt-averaged-hardy-littlewood.md.
- Script: code/parity/mrt_averaged_hl.py [X H] (/usr/bin/python3 -I; 39 s at 1e8, < 1 GB); outputs .out and _1e7.out.
  Exploration (same script, part 4): residual structure across shifts -- dead end; sub-Poisson spread noted.
- Source read: MRT17 arXiv:1707.01315v3 (SHA-256 e93924c5...9a493a1), pp. 1-11.
- Main paper v0.29 (cleanup, see Next steps 3); verification note v1.0.1 (erratum).
- News search (3:34 AM run): nothing new (three searches). Lean: lake build and Audit.lean pass (no Lean changes).
- Wolfram and mathbox NOT available.

## Session 28 (7:34 PM CT slot of 16 Nov, started on time 01:35 UTC 17 Nov; no wait) -- additions
- Parity paper v0.13: subsec:gowers (Prop. prop:gowers-blind, Remark rem:gowers), bib GT10, GT12, Tao16b; rem:mr16-transfer
  corrected (MRT15 builds on MR16); rem:pm65 and rem:debouzy shortened; abstract one clause longer (\enlargethispage{4pt} after
  the TOC keeps page 1 clean). Audit notes/audit-parity-v013.md (3 errors, 5 gaps in the first draft of the remark, all fixed).
  Route card notes/parity-attempts/2026-11-17-gowers-infinite-complexity.md.
- Scripts: code/parity/gowers_twin_blocks.py [N L seed] (/usr/bin/python3 -I; 19 s; output .out); exploration
  code/explore/local_u2_liouville.py [X M seed] (2 s; .out; dead end).
- Sources read: GT10 arXiv:math/0606088v2, GT12 arXiv:0807.1736v4, Tao arXiv:1509.05422v4, arXiv:1605.04628v1 (hashes in
  notes/parity-programme.md). GTZ inverse theorem not opened.
- Main paper v0.28. Lean: lake build and Audit.lean pass (no Lean changes). Wolfram and mathbox NOT available.
- No news search (not the 3:34 AM run).

## Session 27 (11:34 AM CT slot of 16 Nov, started on time 17:34 UTC; no wait) -- additions
- Verification note v1.0 (frozen): Section sec:basis (per-number basis), Appendix app:facts, abstract 204 words; internal referee
  pass referee/2026-11-16-verification-note-v1/report.md (8 errors, 8 gaps, all fixed; minor items partly deferred, see above).
- Parity paper v0.12: Remark rem:chen; cuts (see Next steps 2); bib Tao07, Tao15c. Audit of the rewrites by a fresh-context helper
  (see the log entry). Route card notes/parity-attempts/2026-11-16-chen-consistency-test.md.
- Lean: chen_no_weakly_fair_weight, chen_twin_half_weight, chen_semiprime_half_weight (Parity.lean; in Audit.lean).
- Literature: notes/sources-chen-parity.md (Chen constants: Wu 1.104, R. Li 1.2759 (preprint); twin upper bound Lichtman 3.29956;
  Tao 2007 / 2015 / 2016 blog posts; Pintz 2010; Selberg-Delange only via Klazar's notes (Tenenbaum's book not opened)).
- Exploration: code/explore/omega_mod_q_weights.py [x] (/usr/bin/python3 -I; 14 s at 1e7), output .out: dead end (mod-q analogue).
- Main paper v0.27. Wolfram and mathbox NOT available.

## Session 26 (3:34 AM CT slot of 16 Nov, started on time; no wait) -- additions
- Weekly review notes/reviews/2026-11-16.md (fresh-context helper review, checked against the files).
- Parity paper v0.11: Section subsec:pintz (Thm thm:pintz-maynard, Cor cor:pintz12, Rem rem:pintz-parity), bib Pi10
  (arXiv:1004.1065v1, SHA-256 45d7a850...69d693) and May15 (arXiv:1311.4600v3, SHA-256 dce1a7a0...63cda9); first review
  cuts; abstract 174 words; audit notes/audit-parity-v011.md (no errors, 11 fixes applied). Route card
  notes/parity-attempts/2026-11-16-pintz-dichotomy-maynard.md. Flag (minor) in notes/flags-for-jerry.md.
- Scripts: code/parity/pintz_maynard.py [maynard5 | opt K DEG] (seconds; /usr/bin/python3 has scipy), vectors in
  code/parity/pintz_maynard_vectors.json; second program code/parity/pintz_maynard_check2.py (~3.5 min), output .out.
- Verification note v0.12 (wording of the Lemma 9.1 ceiling); main paper v0.26 (version tags out of headings, Related results).
- Exploration: 4-tuple version of the dichotomy needs level 0.5423 (dead end with current inputs).
- News search (3:34 AM run): nothing new found on the 2026 claims or on parity (three searches); status table unchanged.
- Lean: lake build and Audit.lean pass (no Lean changes). Wolfram and mathbox NOT available.
- Note: /usr/local/bin/python3 lacks scipy/flint; use /usr/bin/python3 for the scripts.

## Session 25 (7:34 PM CT slot of 15 Nov, started on time 01:34 UTC 16 Nov; no wait) -- additions
- Parity paper v0.10: new Section sec:siegel (Prop. prop:siegel-bias, Cor. cor:siegel-typeI, Remarks rem:siegel-locates,
  rem:siegel-num, eq. eq:tt-exc), open question 8, bib TT22 (arXiv:2109.06291v2, SHA-256 d0b968ce...08956) and HB83
  (quoted only). Route card notes/parity-attempts/2026-11-16-siegel-world-typeI.md. Audit notes/audit-parity-v010.md
  (3 errors, 3 gaps, all fixed). Full referee pass referee/2026-11-16-parity-barrier/report.md (+ checks/), framing fixes
  applied, cuts deferred to the review. Abstract 197 words (TeX source count).
- Scripts: code/parity/siegel_class_bias.py [x q w seed] (/usr/bin/python3 -I; ~1 min at 5e7, < 2 GB), output .out.
  Exploration code/explore/l1_small_split.py [QMAX] (.out; 11 s).
- Sources: Matomaki-Merikoski arXiv:2112.11412 downloaded (SHA-256 2e664b17...521ff), not read. Heath-Brown 1983 needed
  (Cloudflare 403).
- Main paper v0.25 (Related results, history item). Lean: lake build and Audit.lean pass (no Lean changes).
- Wolfram and mathbox NOT available.

## Session 24 (11:34 AM CT slot, started on time 17:35 UTC 15 Nov; no wait) -- additions
- Parity paper v0.9: new Section sec:bomb (Prop. prop:bomb-twin, Remarks rem:ford-twin, rem:debouzy), second table in sec:num,
  open question 7; abstract rewritten (173 words). Route card notes/parity-attempts/2026-11-15-bombieri-level-alone.md.
  Audits: notes/audit-parity-v09.md (two fresh-context agents; 5 errors fixed, incl. p+2 vs p-2).
- Sources read (hashes in notes/parity-programme.md): Ford arXiv:math/0401215v1; Debouzy arXiv:1907.06393v1; Lichtman 2009.08969v2.
- FLAG (minor): Debouzy's constant 2 S_2 should apparently be 4 S_2 (notes/flags-for-jerry.md, README).
- Scripts: code/parity/bombieri_twin_split.py [x] (numpy, ~4 GB at 3e7; 1e8 is OOM-killed at 13 GB: do not run it), output .out;
  code/explore/hooley_twin_parity.py [x] [alpha...] (.out).
- k = 45 Schwartz-Zippel (capped_exact on code/cap6/P_rand45_lemma91_u.json) resumed from 74/273 pieces with 3 procs, /usr/bin/python3
  (python-flint is installed for /usr/bin/python3, not for /usr/local/bin/python3). DONE (~72 min): I_T, J_T equal check_rand45_lemma91.json
  exactly (code/cap6/res_rand45_lemma91.json, compare_rand45_lemma91.out). Verification note v0.11, main paper v0.24 Prop. prop:cha-ceiling.
- Wolfram and mathbox NOT available.

## Session 23 (back-to-back run 2 of 3, continued in the same conversation as Session 22 at Jerry's request; no wait) -- additions
- Parity paper v0.8: subsec:window (Prop. prop:unc-ceiling, Thm. thm:k3-window, Cor. cor:k3-linear, Remark rem:k3-window);
  open question 6 partly answered. Route card notes/parity-attempts/2026-11-15-k3-window.md. Audit notes/audit-parity-v08.md.
- Scripts (code/parity/, /usr/bin/python3 -I): k3_unc_1d.py eps [N] and k3_unc_kernel.py eps n... (Heuristic 1D/2D values);
  k3_unc_cert.py eps_p eps_q C_p C_q [N] [delta] (arb certificate -> k3_unc_cert_<p>_<q>.json) and k3_unc_verify.py <json>
  (independent mpmath iv check; ~5 min for the 439/1000 file); arrangement certificates k3_arrangement_cert_2_9_n18.json,
  k3_arrangement_cert_7_24_n24.json (verified by k3_arrangement_verify.py; output k3_arrangement_verify_eps.out);
  eps sweep output k3_arrangement_eps2.out (runs/k3_eps2_jobs.sh).
- Exploration: code/explore/kappa_closed_form.py (kappa = 0.8901675, no closed form; dead end).
- Wolfram and mathbox NOT available.

## Session 22 (back-to-back bonus run 1 of 3 at Jerry's request, 15:51 UTC 15 Nov; no wait) -- additions
- Parity paper v0.7: subsec:dual (Lemma lem:dual, Prop. prop:overlap, Prop. prop:orth-relax, Prop. prop:k3-step, Remark rem:k3-eps),
  Remark rem:tao14b (credit to Tao's 2014 blog post for the core of prop:bipartite; bib Tao14b, Ake25), open question 6 sharpened.
  Audit notes/audit-parity-v07.md (fixes applied). Route card notes/parity-attempts/2026-11-15-k3-dual-orthogonal.md.
- Scripts (all in code/parity/, run with /usr/bin/python3 -I): k3_thm314_dual.py eps mode n... (cube grids; modes full/disj/none;
  output .out), k3_extrapolate.py, k3_orth_relax_cert.py p q n (+ data/orth_relax_*.json) and k3_orth_relax_verify.py,
  k3_arrangement_exact.py [--eps p/q] [--cert-each] n... (helper-written; exact arrangement class; cert k3_arrangement_cert.json,
  eps runs in k3_arrangement_eps.out) and k3_arrangement_verify.py (independent fibre-wise exact check).
- Exploration: code/explore/k3_extremal_marginal.py (dead end).
- Sources: notes/sources-tao14b.md (Tao blog 2014, Akeno arXiv:2508.02769v3). New 'needed': 182 restoration data.
- Wolfram and mathbox NOT available.

## Session 21 (bonus run at Jerry's request, 14:54 UTC 15 Nov; no wait) -- additions
- Parity paper v0.6: Section sec:ceil (Prop. prop:ceil, Cor. cor:ceil, Remark rem:ceil-locates, Thm thm:k2, Remark rem:k2,
  Cor. cor:consistent, Remark rem:pm65), subsec:mr16 + Remark rem:mr16-transfer; open question 2 partly answered, new open
  question 6. Scripts: code/parity/geh_ceiling.py (/usr/bin/python3 -I; arb), code/parity/k2_thm314_numeric.py (/usr/bin/python3,
  floating point; output .out). Audit notes/audit-parity-v06.md (no errors; gaps fixed). Route card
  notes/parity-attempts/2026-11-15-geh-ceilings-k2.md. Sources: notes/sources-mr16.md.
- Rung 182: code/sharifi182_arith.py (86 PASS), code/sharifi182_rows.py (30 PASS), notes/arith-182-report.md, notes/sources-182.md
  section 11 (T0 exact from the rows). Verification note v0.10, main paper v0.21.
- Exploration: code/explore/k3_thm314_grid.py (+ .out): k = 3 grid lower bounds, extrapolating to ~2.003 (inconclusive).
- Minor flag: PM8b Prop 6.5 proof step (notes/flags-for-jerry.md).
- Wolfram and mathbox NOT available. numpy/scipy/flint are installed for /usr/bin/python3 only (pip install went elsewhere).

## Session 20 (bonus run at Jerry's request, 11:37 UTC 15 Nov; no wait) -- additions
- Parity paper v0.5: Section sec:ss (Sawin-Shusterman read in arXiv:1808.04001v2, notes/sources-sawin-shusterman.md),
  Prop. prop:ss-split (over Z, unconditionally: twin asymptotic iff T_D(x) = o(x); compare Murty-Vatwani, known to us only via
  Cantarini arXiv:2607.09110v1), Remark rem:ss-transfer; Cor. cor:maynard-logc (two-variable weights, conditional on TT25);
  open question 3 answered from the literature (notes/sources-oq3-level.md). Audit notes/audit-parity-v05.md (all fixed).
- Rung 182: code/sharifi182_kappa.py (run with /usr/bin/python3 -I; python-flint is installed only there), result
  code/data182/kappa_result.json, notes/kappa-182-report.md, notes/sources-182-kappa.md. Verification note v0.9, main paper v0.20.
- Exploration: code/explore/bdh_twin_liouville.py (dead end, notes/explorations.md).
- Minor flag: Sawin-Shusterman Thm 4.5 saving exponent beta/p vs beta/(2p) (notes/flags-for-jerry.md).
- Sources needed: Murty-Vatwani (JNT 2017), BFI (Acta 1986).
- Wolfram and mathbox NOT available.

## Session 19 follow-up (15 Nov, after the merge of PR #39)
- Jerry uploaded Heath-Brown's x^3+2y^3 (journal scan, SHA-256 in notes/sources-hb-x3-2y3.md; not committed). Parity paper v0.4:
  Section subsec:hb-x3, Remark rem:hb-transfer. Source request marked received.

## Session 19 (3:34 AM CT slot, started on time 09:34 UTC 15 Nov; no wait) -- additions
- News search (WebSearch, standard, 3 queries; Science News article of 11 Sep opened): nothing new.
- RUNG 182 TAIL second program DONE: code/sharifi182_tail2.py (--selftest; --cap b,...; --combine), results code/data182/tail2_result.json
  and tail2_cap_<b>.json (+ precision check tail2_cap_196608_P192B160.json), report notes/tail2-182-report.md. T ball radius 1.4e-45
  inside program 1's ball; nominal r_max gives T above trialTailUpper (5e-7 rel), so r_max = n0 - 1 is forced. 2 workers x 1.5 GB,
  14 min. Spot-checked here: selftest re-run PASSED; nesting of the two balls and T_upper <= trialTailUpper checked exactly.
- PARITY ATTEMPT: notes/parity-attempts/2026-11-15-tt25-level-logc.md + audit 2026-11-15-tt25-audit.md (sound; fixes applied);
  paper v0.3 Prop. prop:tao-weight-logc, Remark rem:tao-weight-logc, open questions 1 and 5, bib MRT15.
- Exploration: code/explore/aux_forms_lp.py (dead end, notes/explorations.md).
- Heath-Brown x^3+2y^3: blocked; notes/sources-hb-x3-2y3.md (secondary only).
- Verification note v0.8 (Remark rem:182, TOC, abstract); main paper v0.19 (rem:sha182 paragraph, Related results, history list).
- Wolfram and mathbox NOT available.

## Session 18 (3:34 AM CT slot started early at Jerry's request, 04:23 UTC 15 Nov; no wait, Session 17 merged as PR #36) -- additions
- News search (WebSearch, standard): nothing new since the last entry.
- PARITY ATTEMPT: notes/parity-attempts/2026-11-15-bipartite-criterion.md, paper v0.2 Section sec:bip (Prop. prop:bipartite,
  Cor. cor:six, Remark rem:marg, subsec:rem81). Code code/parity/bipartite_obstruction.py; Lean lean/TwinPrimes/Parity.lean
  (triangle_no_fair_weight, pm8b_path_weight_*, narrow5/7_admissible). Audit notes/audit-parity-v02.md (2 errors, all fixed).
- FLAG (minor): Polymath8b Remark 8.1 printed weight identically zero (notes/flags-for-jerry.md); journal version blocked by a
  bot challenge (notes/sources-needed.md, 'needed', low priority).
- Parity paper thread 2: FI a^2+b^4 (notes/sources-fi-x2y4.md; subsec:fi-x2y4, Remark rem:fi-transfer).
- Literature for open question 1: notes/sources-chowla-quantitative.md (HR, Pilatte, Tao-Teravainen, Guo, Hughes).
- 3g: notes/hm-programme.md, code/hm/pm8b_mk_lower.py (PM8b Thm 6.7 reproduced: k = 35410 MPZ, 41588 BV-only).
- Exploration: code/explore/residue_parity_lp.py (dead end; global fairness is the wrong notion).
- RUNG 182 J second program DONE: code/sharifi182_check2_J.py (--cap b, --combine, --selftest), results code/data182/check2_J_result.json and check2_J_cap_<b>.json; J0, J+ balls above the published lower bounds; vs program 1 rel 2e-23 (J0), 2e-32 (J+). Report notes/check2-J-182-report.md. 2 workers x 3.7 GB, ~107 min.
- RUNG 182 TAIL (one program): code/sharifi182_tail.py (imports check2_J and check2), results code/data182/tail_result.json and tail_cap_<b>.json, report notes/tail-182-report.md; source notes notes/sources-182-tail.md. T = 5.286348805928e-13 +- 1e-40 <= published trialTailUpper (rel gap 8e-12); q_H - 1 = 2.767059e-4 >= mu- = 2.766919e-4. Kernel K exact in fmpq; (5.7) needs r_max = n0-1 (nominal block end violates it). 2 workers x 3.6 GB, 66 min. NEXT for 182: an independent second program for the tail (different contraction), then the restoration losses (2.115e-4 claimed).
- Wolfram and mathbox NOT available.

## Session 17 (7:34 PM CT slot, 14 Nov; started 01:34 UTC 15 Nov; no wait) -- additions
- 186 program 1: the 19 remaining outer components. NOTE: at --prec 128 the 15 smallest bins (O2 L1, L2; O5/2 L1-L13) abort with
  "renewal: nonpositive lower endpoint" (the paper's own rejection rule): use runs/oai186_outer_job256.sh (256 bits, ~14 min each,
  2 in parallel). Combined: code/cap6/oai186_loss_outer.json, summary code/cap6/oai186_loss_summary.json (97/97, all <= table).
- 186 program 2: code/oai186_loss_outer2.py (--comp X --out f; --selftest; --ihcheck), results code/cap6/loss_outer2/part_*.json
  (P1-P12, H, L19-L22 of O5/2), ~12 min per P, 18 min H, 6 min L, 1.3 GB. No renewal branch: L18 and below abort (assertion in the
  delay recurrence). runs/loss_outer2_cache/ is a regenerable 31 MB pickle (gitignored).
- Parity paper v0.1 + route card 2026-11-15; exploration code/explore/parity_weighted_liouville.py.
- Wolfram and mathbox NOT available.

## RELAYED DECISION (Jerry Kim via the coordinator session, 14 Nov 15:26 UTC; received by Session 16 after its merge)
- SWITCH TO PHASE B AS SOON AS RUNG 186 IS FINISHED: its variational step INCLUDING the loss bound L^+ reproduced by two independent programs, or shown to fail as stated, or blocked. Do not wait for rung 182 (it continues inside Phase B's ~20% bound share). When the switch happens, record it in STATE.md, status.json (phase "B") and the log; Phase B top priority is the parity-barrier programme (papers/parity-barrier/, notes/parity-programme.md, one bounded attempt per run in notes/parity-attempts/), ~35%.
- Status after Session 16: NOT yet finished. L^+ has been re-evaluated by ONE program for 78 of 97 components (all but 1.2e-6 of L^+). Still needed: the 19 small outer components, and a second, independent program (at least for the decisive group O_{5/2}). Until then, prioritise 186's loss bound.

## Session 16 (started early at Jerry's request, 9:23 AM CT, 14 Nov; no wait, no other run active) -- additions
- POSITION unchanged: bounds.project = 236 CONDITIONAL (caveat everywhere), 240 conditional, 246 unconditional. Phase A. No news search (not the 3:34 AM run).
- The 186 companion PDF and the authors' script are now committed (code/third_party/openai186/, Apache-2.0, PR #30). The script was NOT used (not read) this session.
- RUNG 186 LOSS: two new evaluators written from the PDF:
  - code/oai186_loss_inner.py (45 inner components, (2.19)); ALL 45 DONE (code/cap6/loss_inner/part_*.json, combined code/cap6/oai186_loss_inner.json): every value <= table, within 5e-10 for most; ceil + (2.31) reproduces the four inner group totals of Table 2.7 EXACTLY.
  - code/oai186_loss_outer.py (52 outer components, R (2.17) and V (2.20)-(2.21)); run in decreasing order of table E, 128 bits, one component per job (~60 min wall each with 4 in parallel, ~1.6 GB each). Done: see code/cap6/oai186_loss_outer.json (33 of 52 done, all but 1.2e-6 of L^+ together with the inner ones; every value <= table).
  - Group data now read in the PDF: radial intervals (1.23)-(1.24); delay recurrence only if M >= 64 and the acceptance tests after (2.1) pass (implemented as stated; it confirms Session 15's inferred renewal choice); clipping (1.26) with core/threshold b_t, C_t (inner rows) and a_t, A_t (outer rows); the schedule reproduces Lemma 1.6's counts.
  - Small bins use the closed form T_e = (exp Q - X^{e+1} exp(XQ))/(1-X) (arb series exp), essential for L = 3 cells.
  - Fresh-context audit of both programs vs the PDF: notes/audit-186-loss/report.md, no discrepancy.
  - RESUME the outer queue (skips finished parts):  cat runs/oai186_outer_queue.txt | xargs -P 4 -L 1 sh runs/oai186_outer_job.sh   then   python3 code/oai186_loss_outer.py --combine code/cap6/loss_outer/part_*.json
- OWN IDEA: margin budget (code/oai186_margin_budget.py, paper Prop. prop:oai186-budget): O_{5/2} = 89.5% of L^+, may be at most 2.06% too small (margin > 1/50000) or 14.3% (margin > 0); the inner groups barely matter.
- Exploration: pretentious twin statistic for class-number-one discriminants (code/explore/siegel_pretentious_twin.py) -- dead end.
- Wolfram and mathbox NOT available.

## Session 15 (3:34 AM CT slot, 14 Nov; waited 62 min for Session 14 follow-up 3's branch to go quiet, work 4:37 AM CT on) -- additions
- POSITION unchanged: bounds.project = 236 CONDITIONAL (caveat everywhere), 240 conditional, 246 unconditional. Phase A. News search: nothing new.
- RUNG 182: second program for I(F) DONE: code/sharifi182_check2.py (arb; own Lean parser, own Dickman form, Cox-de Boor in fmpq, A(y)^39 moments). Result code/data182/check2_I_result.json: ball [1.48963410081137215290e-11 +/- 5.2e-40], inside the published enclosure; vs program 1 rel 1.7e-22 (program 1's 2^-224 rounding; at 400 bits the gap is 3e-34 on a test grid). Per-cap files code/data182/check2_I_cap_<b>.json. 2 workers x 2.9 GB, 67 min. Shared with program 1: reading of F and the layered cap decomposition.
- RUNG 186: code/oai186_loss_I2old.py -> code/cap6/oai186_loss_I2old.json: all 7 I2old raw bounds at or just below Table 2.3 (readings: radial interval = old-ladder rows 12-23 (chi_A); renewal majorant for L2, L3 and delay recurrence for the rest, INFERRED from the numbers; clipping (1.26) inactive for this group). Each bin ~8 min, P1/H ~17 min, < 1.6 GB. NOTE: gmpy2 is not installed for python3.11 by default (pip install --break-system-packages gmpy2 if oai186_IH.py / oai186_J.py are needed).
- OWN IDEA (FC3) SETTLED: paper Prop. prop:psi-weight (Proved here; equalisation lemma) + certificates code/psi_weight_cert.py 10373 10000 41463 10000 (arb) and code/explore/psi_scratch_certify.py 10373 10000 4.14631 (mpmath.iv): M_{50,1/25} < 4.1463. Two-zone weight certifies 4.1459 (code/twozone_50_cert.py), so psi does NOT improve the best upper bound. Helper notes notes/psi-weight/ (attempt-helper.md, audit.md).
- Exploration: F_2[T] Moebius autocorrelation / twin irreducibles (code/explore/ff_chowla.py), inconclusive.
- Wolfram and mathbox NOT available.

## Session 14 (7:34 PM CT slot, 13 Nov; no wait, Session 13 had merged at 7:18 PM CT) -- additions
- POSITION unchanged: bounds.project = 236 CONDITIONAL (caveat everywhere), 240 conditional, 246 unconditional.
- Audit of SY Thm 4.18 (PR #19) integrated: paper Remark rem:sy-audit (label "Literature, audited", not peer review), status-table footnote, status.json project_note, verification note Remark lemma5. Kl3 check re-run (1.03 vs 29.97).
- capped_exact.py: new --split (Corr2 = Q(R)^2 part - Q(U)^2 part; exact, same totals, tested k = 12) and --bonf (one-sided: Icorr j<=1, Corr1 j<=2, R parts j<=2, U parts j<=1). New assert L - g <= tau (true for all our inputs). Paper Prop prop:bonf2 (Proved here). 240 vector: 4.012038868083 > 4 from 98 pieces, 3.5e-8 below exact (code/cap6/compare_capfree_D20_bonf.json).
- RUNG 186, big step: code/oai186_IH.py and code/oai186_J.py (GMP Kronecker products, directed rounding; rho_D closed forms at 110 digits) give I_H = 2.36853178533e-14 (inside Lemma 2.5 enclosure) and J_lambda = 9.0248755655e-14 (5.9e-9 above its lower bound), rho* J/I_H = 1.000206087 > 500103/500000. Own reading of layered (2.15): layers over all 7 cap values {35265, 35419, 44781, 44976, 46580, 49152, 68225}, erased coordinate in outer shells with cap >= b_a, face masks cap >= b_a. Paper Prop prop:oai186-main. 7 + 23 min on one core. Fresh-context audit: no defect.
  Second program code/oai186_check2.py (arb balls, y-series A(y)^d instead of set partitions): I-mode run plus J workers `--jcap b` (one per layer cap; linearity: each worker returns S(v^{l(a)}, M^b; chi_a) - S(v^{l(a+1)}, M^b; chi_{a+1}) into code/cap6/oai186_check2_J_b<b>.json). MEMORY: each worker ~3 GB, at most 3 at a time (one OOM kill at 4). Queue: runs/oai186_check2_queue.sh. Combined with code/oai186_check2_combine.py "$(cat code/cap6/oai186_check2_IH.txt)" --out code/oai186_check2.json: agrees with program 1 to 7e-17 (DONE).
  Remaining for 186: the loss bound L^+ (97 components, their Sec. 2.4, Tables 2.1-2.7) -- the PDF is in the GitHub repo openai/PrimeGaps186, outside this session's GitHub scope; requested from Jerry (notes/sources-needed.md).
- RUNG 182: notes/sources-182.md (helper transcription of the bundle; k = 39; 726 coefficients NOT in the bundle, only in GitHub repo romyar1/prime-gaps-lean -> requested from Jerry). Lean: sharifi39 / boundedGaps_182_of_DHL_39'. Paper Remark rem:sha182.
- k = 45 Schwartz-Zippel run was STOPPED at 74/273 pieces to free cores (checkpoint code/cap6/pieces_rand45_lemma91.jsonl). Resume (alone, 3-4 procs, several hours):
      nohup python3 code/capped_exact.py code/cap6/P_rand45_lemma91_u.json --procs 4 --ckpt code/cap6/pieces_rand45_lemma91.jsonl --out code/cap6/res_rand45_lemma91.json > runs/exact_rand45.log 2>&1 &
  NOTE: it was started without --split; resume it the same way (same piece keys). Low priority.
- Exploration: code/explore/level_slack.py (level slack in SY's exponent margins vs the omega needed for k = 47) -- dead end.
- Wolfram and mathbox NOT available.

## Session 13 (11:34 AM CT slot, 13 Nov; waited 3 h 30 min for Session 12, stood down, resumed at Jerry's request 3:10 PM CT after PR #18 merged; finished ~7:30 PM CT) -- additions
- POSITION unchanged: bounds.project = 236 CONDITIONAL (caveat everywhere), 240 conditional, 246 unconditional.
- DONE: second program for our own k = 48 D22 vector: capped_exact.py --ckpt, all 176 pieces (code/cap6/pieces_kin48_D22r.jsonl, result code/cap6/res_kin48_D22r.json, 15.5 core-hours). I_T and J_T equal check_kin48_D22r.json exactly (code/compare_two_programs.py -> code/cap6/compare_kin48_D22r.json). 4.0060814208 > 4 by two programs. Paper Prop kin-capped and verification note Prop kin-own now say two programs.
- NEW Prop bonf (paper v0.12, Proved here): Bonferroni -> one-sided certificate J_T >= J - (S0 - S1 + S2) - Corr2, I_T <= I - S'0 + S'1; drops Corr1 j = 3 and Icorr j >= 2. k = 48: one-sided 4.006081420807 (loss 3.5e-12), saves 28% of time. compare_two_programs.py prints the one-sided value from a pieces file.
- code/thin_bound.py: crude a priori bound (|P| <= sum |c| L^deg times region volume): Corr1 j = 3 <= 1.4e-14 J (SY witness), useless for Corr2 (6e32 J). Volume formulas cross-checked against capped_exact.T1/T2 (--volcheck, 30 pieces, 0 failures; slow, ~1 h). Output code/cap6/thin_bound_sy236.json.
- Rung 186: code/oai186_dickman_cells.py (closed-form Dickman cell masses; all 7 caps inside the transcribed enclosures (2.1)-(2.2)); notes/sources-186-forms.md has a Session 13 section.
- Exploration: code/explore/tuple_counts_hl.py (HL vs prime pairs in narrow48 translates) -- dead end.
- Wolfram and mathbox NOT available.
- NOTE: a worker restart killed the background job once (77/176); restarting with the same command resumed from the checkpoint. Commit checkpoint files often.

## Session 12 (7:34 AM CT slot, 13 Nov; started by hand 7:44 AM CT; Sessions 10 and 11 had died unmerged at ~4:15 AM CT) -- additions
- POSITION NOW: bounds.project = 236 CONDITIONAL (Song-Yue's equidistribution Thm 4.18, via Thm 4.33; NOT verified). Caveat is in the paper (Cor. cor:236), status.json, README, bound-history "how". Keep it everywhere 236 appears. 240 remains conditional on Stadlmann; 246 unconditional.
- Rescued: Session 11's branch (claude/zen-curie-gstgp2) and Session 10's last two commits (claude/zen-curie-b426c3; not ancestors of each other). Both died while running concurrently (Session 11 thought Session 10 was dead).
- DONE: capped_exact.py --jonly --ckpt on code/cap6/P_sy236_u.json, all 126 pieces (code/cap6/pieces_sy236_jonly.jsonl, result code/cap6/res_sy236_jonly.json; 26542 s wall this session + 5 pieces from Session 10). J_T == capped_check J_T exactly (code/songyue_compare2.py -> code/cap6/compare2_sy236.json); songyue_compare.py on it -> Jref equality (code/cap6/compare_sy236_exact.json); its cap-free I, J == monomial I0, J0.
- Timing per piece (4 procs): Corr1 j=3 50-55 min each (10 pieces), Corr2b/Corr2c j=3 7-38 min, j=2 6-45 min, j<=1 2-30 min. The j=3 pieces are <= 1.0e-24 J in absolute value (own idea in the ledger: rigorous a priori bound for them).
- Rung 186: notes/sources-186.md (Session 11) and notes/sources-186-forms.md (Session 12 helper transcription of [14]: nu_c, trial F, forms (2.10)-(2.15), the 77 coefficients as JSON, Lemma 2.5, L^+). Reproduction needs interval arithmetic (Dickman masses transcendental); (2.15) layered cap convolution underspecified; avoid FLINT for independence.
- Exploration: per-m caps toy (code/explore/toy_capped_perm.py) -- dead end.
- Wolfram and mathbox NOT available again.
- Paper v0.11 (Prop sy-exact two programs; Cor cor:236; Remark oai186 extended).

## Session 10 (scheduled 11:34 PM CT, 12 Nov; work started about 1:25 AM CT, 13 Nov, after waiting ~1 h 50 min for Session 9 to merge) -- additions
- Heartbeat protocol in use: runs/heartbeat.json (section 0 of the task). Session 9 had no heartbeat (older prompt); it was treated as active while it kept pushing.
- RUNG 236 via Song-Yue's witness: DONE with one program, second running.
  - code/songyue_convert.py: witness -> u-format (z = (520/521) u; augmented monomials -> even power sums), integer coefficients with "scale" (code/cap6/P_sy236_u.json, 1311 terms, degree 25). code/songyue_pointcheck.py: exact at random rational points.
  - code/songyue_I0.py (monomial basis, partial-matching DP, 25 s): (98!)^2 10^192 5^150 521^50 I0 == Iref EXACTLY. code/songyue_J0.py: cap-free J0, 48 J0/I0 = 4.0036348167 (= Kintali's claimed uncapped value).
  - capped_check.py on P_sy236_u.json (56 min, 4 procs, ~1.9 GB/worker): code/cap6/check_sy236.json. code/songyue_compare.py: (99!)^2 (26!)^2 10^196 5^150 521^50 J_T == Jref EXACTLY; 48 J_T/I0 = 1.000664921591 > 2001/2000 (4.0026596864 Polymath); 48 J_T/I_T = 4.0030988047 (= Kintali's claimed capped value). Fresh-context audit of the four scripts found no errors (sympy toy checks at k = 2-4).
  - Second program: capped_exact.py --jonly (new option: skip I corrections) with --ckpt (new: exact value of each finished piece in a JSONL; restart skips them). 126 pieces; the j = 3 pieces take 28-47 min each on 4 procs. Cap-free part agrees (4.0036348167). RESUME (alone on the machine):
      nohup python3 code/capped_exact.py code/cap6/P_sy236_u.json --procs 4 --jonly --ckpt code/cap6/pieces_sy236_jonly.jsonl --out code/cap6/res_sy236_jonly.json > runs/exact_sy236_jonly.log 2>&1 &
    then compare J_T in res_sy236_jonly.json with check_sy236.json (exact string equality of the rationals). If equal: the variational step of 236 is reproduced by two programs; the project bound may move to 236 CONDITIONALLY (analytic input: [SY26] Thm 4.18 / Stadlmann's estimates as amended by [Kin26], Claimed; caveat everywhere; Lean tuple boundedGaps_236_of_DHL_48 exists).
- Exploration: [SY26, Remark 4.23] on [Sta26, Lemma 5] read against arXiv v1 (notes/explorations.md): the step does use a Siegel-Walfisz hypothesis on alpha that Lemma 5 / Def. 9 (I) do not provide. Repair not checked. Paper Remark rem:sta-lemma5 and the status-table footnote.
- Paper v0.10: Prop sy-exact, Remark rem:sta-lemma5 (inserted after Prop kin-capped, before the hybrid floor).
- Wolfram connector and mathbox skills NOT available in this session.

## Session 9 (11:34 PM CT slot, 2026-11-12/13) -- additions
- NOTE: the sandbox clock (date) ran about 50 minutes behind real time in sessions 8-9; budget the merge by elapsed time, not by `date`.
- k = 45 Lemma 9.1 (from the saved weights, `--load`): ceiling re-certified for sigma = 4 at 6500 bits with block split 1/3, and sigma = 3.99 also certified (paper Prop 33 now says < 3.99). Optimum in the 846-dim space 3.98555 (Gram float; vector code/cap6/P_opt45_lemma91_D21r_u.json, not re-certified exactly). The registered prediction 3.977-3.981 FAILED (Remark 34): regain is 31% of the truncation loss at k = 45 vs 9% at k = 49.
- Schwartz-Zippel check: random integer vector code/cap6/P_rand45_lemma91_u.json (seed 20261113, entries in [-2^31, 2^31]); capped_check gives code/cap6/check_rand45_lemma91.json; weights reproduce both exactly (runs/gram45_rand_selftest.log), and the ball Gram forms contain them (--gramcheck). capped_exact on the same vector was stopped after 138 pieces (~4 h needed on 2 procs). Resume: `python3 code/capped_exact.py code/cap6/P_rand45_lemma91_u.json --procs 4 --out code/cap6/res_rand45_lemma91.json` and compare I_T, J_T with check_rand45_lemma91.json.
- capped_gram.py: new options --split p/q (PD block split), --gramcheck, --maxit.
- Rung 236 (Kintali): k = 48 cap-free degree 22 (1041 coeffs, cert_kin48_capfree_D22e.json): M = 3.9589046383, ratio x 253/250 = 4.0064115 > 4 (build 7 min, solve 33 min, ~7.5 GB: run it alone). On Kintali's support (P_kin48_D22r_u.json, 400-bit rounding): capped_check gives 48 J_T/I_T = 4.0060814208 > 4 (check_kin48_D22r.json, 22 min on 4 procs); caps cost 0.00033. Second program capped_exact.py was started and stopped (several hours: first correction piece 9 min on 4 procs). Resume: `python3 code/capped_exact.py code/cap6/P_kin48_D22r_u.json --procs 4 --out code/cap6/res_kin48_D22r.json` and compare I_T, J_T with check_kin48_D22r.json. Project bound NOT lowered (analytic input Claimed).
- Memory: mk_general at D22 needs ~7.5 GB; capped_gram main at 6500 bits ~10 GB during the PD test. Never run two of these together (four OOM kills in sessions 8-9).
## NEW 13 Nov, 11:30 PM CT (coordination session): Song-Yue's 236 paper obtained -- top priority for rung 236
- Read `notes/sources-236-song-yue.md` first. Its support is the same D182 support as Kintali's. The full 1295-row witness (degree 25) is in `code/cap6/songyue236_witness.json` and their reference integers are in `code/cap6/songyue236_appC.json`.
- Their criterion uses the CAP-FREE denominator: 48 J_T / I0 > 2001/2000, with reference ratio 1.00066492. So only the cap-free I0 and the capped numerator J are needed.
- The authors say fresh regeneration of the capped numerator is still PENDING. Recomputing J exactly and matching Jref is the next concrete step on 236 (see §6 of the note).
- Their Remark 4.23 claims a missing hypothesis in the proof of [Sta26, Lemma 5]. We have not checked it; add it to the status table as an unverified possible gap in the analytic input for 240.

## Session 8 (bonus run, 5:51 PM CT, 2026-11-12; the trigger called it Session 7) -- additions
- code/capped_gram.py: exact reverse-mode weights of capped_check.py -> Gram matrices G_I (exact), G_J (fixed point, explicit error bound); options --check (exact self-test vs a capped_check result), --save/--load (pickle of weights), --out (top eigenvector on T, written in u-format), --ceiling s1,s2 (rigorous: sigma G_I - k G_J positive definite by recursive Schur complements in arb), env GRAM_CHUNKS=n (n chunks per worker; bounds worker memory).
  Self-test passed exactly at k = 12 and k = 49 (D20). Memory: workers grow to ~5 GB at k = 45 (rational denominators accumulate); with other jobs running this OOM-killed two runs. Fix next: put each group's gradients over a common denominator / reduce before accumulating.
- k = 49 Stadlmann, optimised on T (D20, 707 coeffs): 4.0124198475 > 4; capped_check (check_opt49_D20r.json) and capped_exact (res_opt49_D20r.json) agree exactly. Vector code/cap6/P_opt49_D20r_u.json (400 significant bits per coefficient; the unrounded P_opt49_D20_u.json gives the same 12 digits but makes the evaluators 8x slower: always round). Paper v0.8 Props 31 (adjoint), 32 (4.0124).
- Rung 236: notes/sources-236.md (Kintali read and checked against the PDF; Song-Yue PDF blocked, 403). Kintali: k = 48, L = 521/500, tau = 491/500, g = 91/1250, all caps 1899/2500; `to_ucoords.py --params kintali` (and --support-scale --k 48 to transport a k = 50 eps = 1/25 certificate the way he does: code/cap6/P_kin48_M50D25_u.json from our cert_M50e25_D25e, not evaluated, degree 25 is heavy). Our k = 48 cap-free D20: 3.952004 x 253/250 = 3.9994 < 4 (cert_kin48_capfree_D20e.json). Lean: kintali_large_count, kintali_extra_le_three.
- Registered prediction (notes/session8-prediction.md): Lemma 9.1 caps at k = 45, D21 optimum about 3.977-3.981 < 4.
- DONE in session 8 (04:36 UTC): k = 45 Lemma 9.1 self-test exact; CEILING sigma = 4 certified PD (no P in the 846-dim space reaches 4); sigma = 3.985 NOT certified; the optimiser was still running at merge time (no optimum recorded). Paper Prop 33.
- To redo / get the optimum (run ALONE on the machine, ~100 min adjoint on 2 procs + gram + ceilings):
  GRAM_CHUNKS=4 python3 code/capped_gram.py code/cap6/P_ax45_D21_u_lemma91caps.json --procs 2 --check code/cap6/check_ax45_D21_lemma91caps.json --prec 5000 --sigma 4.3 --save /tmp/w45.pkl --ceiling 4/1,3985/1000 --out code/cap6/P_opt45_lemma91_D21_u.json > runs/gram45_lemma91_D21.log
  then round the vector (400 bits, as in session 8) and certify with capped_check.py.

## Session 7 (bonus run, 4:39 PM CT, 2026-11-12) -- additions
- Both evaluators now take per-m caps (JSON caps {"1":..,"2":..,...,"11+":..}); code/to_ucoords.py --params charton.
- Charton et al. (k = 45, Table 3 caps): our cap-free D21 vector truncated to T gives 4.0027351 > 4; capped_check.py and capped_exact.py agree exactly (code/cap6/check_ax45_D21.json, res_ax45_D21.json). Lemma 9.1 caps (31/50, 31/50, 17/25...): 3.9736870 < 4 (code/cap6/check_ax45_D21_lemma91caps.json). bounds.project NOT lowered to 212 (cap discrepancy in the draft; analytic input Claimed). Paper v0.7: Prop. 29 (k = 45), Remark 30 (ceiling <= 4.126); Thm 31 is now the hybrid floor.
- Lean: charton_caps_valid, charton_large_count, charton_extra_le_six.
- Next steps 1-2 below are updated: (1) optimise P on a capped support: build the correction Gram matrices (capped_check's contraction structure is fastest; capped_exact took 108 min for one vector at k = 45) and settle whether Lemma 9.1's caps can reach 4; (2) rung 236.

## Position (after session 6, 2026-11-12, 12:39 PM CT run started by hand in place of the 3:34 PM slot)
- Established in the literature: H1 <= 246 (Polymath8b 2014; Lean-formalised by Axiom given Bombieri-Vinogradov).
- Claimed in 2026 preprints: 240 (Stadlmann), 236 (Kintali; Song-Yue), 212 (Charton et al.), 186 (OpenAI, Lean conditional on 3 axioms), 182 (GPT-6 Astra prompted by R. Sharifi). No news search this session (arXiv:2608.31126 still v1, no erratum, checked 12 Nov).
- (superseded in Session 12: project bound now 236 conditional) Reproduced by this project: 240 CONDITIONAL (variational step of [Sta26] reproduced exactly; rests on his equidistribution estimates, NOT verified by us); 246 unconditional (given BV). bounds.project = 240 with project_note; bound-history entry for 240 carries the caveat. Keep the caveat everywhere 240 appears.
- Session 6 results (paper v0.6, Section 5):
  - Prop. 25 (Proved here): fibre of T over u' is [0, min(R, max(g, C_{m+1}-s))] (needs C_{m+1} <= C_m + g); I_T = I - int_V P^2, J_T = J - Corr1 - Corr2 (non-admissible base; U = g; U = C_{m+1}-s), each an inclusion-exclusion sum (m <= 9, j <= 3) of polygon integrals in (r_A, rho).
  - Thm 26 (Computed, exact, two independent programs): F = P 1_T, P = cap-free D20 optimiser: k J_T/I_T = 4.0120389035 > 4 (cap-free 4.0161761). code/capped_exact.py (mine, 46 min on 3 cores) and code/capped_check.py (helper, independent, 6 min on 4 cores) agree on I_T, J_T exactly. Files: code/cap6/P_capfree_D20_u.json, res_capfree_D20.json, check_capfree_D20.json.
  - Degree trend (capped vs cap-free): D8 3.789068/3.789069, D12 3.923849/3.923943, D16 3.985976/3.987180, D20 4.012039/4.016176.
  - Cor. 27: variational step reproduced; H1 <= 240 follows from [Sta26] Prop. 1 + his equidistribution theorem (unverified). Lean tuple narrow49 / boundedGaps_240_of_DHL_49 already existed.
  - Remark 28 (own): ceiling 4.14 (two-zone weight, certify_box, 337 pieces); cap-aware cut at 0.6 moves the float sup only 4.13785 -> 4.13753.
  - Prop. 24 (3.9597) is superseded (Cauchy-Schwarz artefact).
  - Lean: stadlmann_coord_le (coordinates <= 600/1000), stadlmann_extra_le_three.
- The twin prime conjecture itself is OPEN. Sieve methods of this kind stop at 6 even under GEH (parity).

## Paper numbering (v0.9: Prop 33 Lemma 9.1 ceiling < 3.99, Remark 34 failed prediction; hybrid floor Thm 35)
## Paper numbering (v0.8: Section 5 adds Prop 31 adjoint Gram, Prop 32 optimised 4.0124; Prop 33 Lemma 9.1 ceiling; hybrid floor is now Thm 34)
## Paper numbering (v0.6)
Thm 1 Lean; Thm 2, 4 certificates; Lemma 3 EGF; Cor 5 (270); Thm 6; Cor 7 (246); Props 8, 10; Lemma 13; Prop 14; Thm 15 floor k<=29; Remarks 16-18; Prop 19; Remarks 20, 21. Section 5: Prop 22 cap-free, Prop 23 cap bound, Prop 24 capped 3.9597 (superseded), Prop 25 exact reduction, Thm 26 capped 4.0120, Cor 27 (240 conditional), Remark 28 ceiling, Thm 29 hybrid floor, Remark 30. Section 6 Programme (label sec:prog).

## What exists
- code/capped_exact.py P_u.json [--procs N] [--out f] [--direct]: exact I_T, J_T (cap-free minus corrections). code/capped_check.py P_u.json [--procs N] [--out f]: independent exact evaluator (direct sum over large sets); tests code/capped_check_tests.py [--slow]; code/cap6/mc_test.py (Monte Carlo, k=12). Input format: code/to_ucoords.py (converts mk_general eps-certificates; caps given as "1","2","3+" only -- extend for per-m caps before Charton et al.).
- code/mk_general.py: `python3 code/mk_general.py k D --even [--eps p/q] [--cert out.json]`. code/verify_cert.py re-checks certificates.
- code/caps_exact.py (shape densities over shifted groups; used by capped_exact.py), code/stadlmann_caps_opt.py (session-5 penalty method, superseded).
- code/floor_hybrid.py, dual_eps_cert.py (certify_box), check_floor_cert.py, dual_lp.py, scan_eps.py / extrapolate_eps.py.
- Certificates: cert_M50e25_D25e/D27e (246), cert_stad49_capfree_D20e (+ cap6/P_capfree_D20_u.json: the 240 variational certificate), cert_ax45_capfree_D21e, cert_floor_*.

## Bound history
- log/bound-history.json: 578 -> 330 -> 288 -> 278 -> 272 -> 270 -> 246 -> 240 (session 6, conditional on [Sta26]'s equidistribution input; stated in the "how" field).

## Older next-step notes (Phase A; superseded by the list at the top)
- Resume commands for old jobs are in the session sections above.

## Rotation of areas to explore (one per session, about half the effort)
variational/spectral methods; convex duality and LP/SDP bounds; exponential sums and l-adic methods (Type III); automorphic methods and large moduli (Maynard, Lichtman); zero-density and large values (Guth-Maynard); function fields (Sawin-Shusterman); Siegel zeros; multiplicative functions and entropy (Tao, Matomaki-Radziwill); additive combinatorics; probabilistic models of primes.
Done so far: session 1 combinatorics/polyhedral; session 2 enlarged supports + generating functions; session 3 convex duality (Theorem 15); session 4 variational/spectral (convex program over dual-weight families, Collatz-Wielandt view, degree extrapolation); session 5 convex duality again, applied to the 2026 hybrid supports (Theorem 25) plus exact integration over cap regions. Session 6: exact integration / inclusion-exclusion over capped regions (verification focus). Next: exponential sums / Type III (which constraint on omega is binding, cf. the helper's omega <= 0.0032), or Siegel zeros for Track B.

## Workspace constraints
- Lean: curl -sSL -o lean.zip https://github.com/leanprover/lean4/releases/download/v4.35.0/lean-4.35.0-linux.zip, unzip in /root/tools, add bin/ to PATH. `lake build` in lean/ (about 25 s), then `lake env lean Audit.lean`.
- python3 is 3.11 at /usr/local/bin: install with `python3 -m pip install ...` (plain `pip` installed into python3.13 this session). Packages: mpmath sympy numpy scipy python-flint cvxpy.
- apt needs `apt-get update` first for texlive. pdftotext is available (used to read the Polymath8b PDF fetched through WebFetch).
- Mathlib cache host, releases.lean-lang.org and direct arxiv.org downloads are blocked (403). Core Lean only. WebFetch of arxiv.org/pdf/... saves the PDF; read it with pdftotext. Do not work around blocked hosts.
- Website math: the paper is typeset with KaTeX (build_site.py runs pandoc --katex). Text in status.json and log/*.json is shown through code/texify_text.py, which typesets plain notation (M_{k,eps}, H1, DHL[k,2], eps, <=, ...) at build time; you may also write TeX inside $...$ there. Never put a literal $ in that text for anything but math.
- pandoc 3.1.3 cannot parse \Bigl / \Bigr: use \left / \right in main.tex.
- Helper agents may be used for reading and for testing ideas; check their proofs line by line before anything enters the paper.
