# Handoff (rewrite this file at the end of every session)

Home: GitHub repo jerryckim16/twin-primes (branch main). Website (GitHub Pages, from docs/): https://jerryckim16.github.io/twin-primes/
Each session works on the claude/... branch its system instructions name (create it from the latest origin/main), opens a pull request and merges it (squash).

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
- Reproduced by this project: 240 CONDITIONAL (variational step of [Sta26] reproduced exactly; rests on his equidistribution estimates, NOT verified by us); 246 unconditional (given BV). bounds.project = 240 with project_note; bound-history entry for 240 carries the caveat. Keep the caveat everywhere 240 appears.
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

## Next steps (in order) -- the 240 focus is done; back to the earlier balance (reproduction ladder, own ideas about half)
0a. FIRST: finish the second program on the Song-Yue witness (resume command in the Session 10 block; it skips finished pieces). If J_T matches, lower bounds.project to 236 with the caveat (bound-history entry, README, status, paper Cor.), exactly like 240.
0b. Then the second program for our own k = 48 vector (capped_exact on P_kin48_D22r_u.json; add --ckpt), and the k = 45 random point (with --ckpt).
0c. Rung 186 (OpenAI, k = 40): read the source, record the support and parameters.
0. (Session 9) k = 45 Lemma 9.1: ceiling 3.99 certified twice, weights checked at a random point against capped_check; remaining: capped_exact at the same random point (resume command above), which also cross-checks capped_check at these caps. Then rung 236 per the Session 9 notes (capped_exact on P_kin48_D22r_u.json if not finished; then optionally optimise on T with capped_gram at k = 48 D22 -- memory: run alone; then 186 (OpenAI, k = 40)). Then rung 236: mk_general 48 22/24 --even --eps 15/506 (alone; ~5 GB), to_ucoords --params kintali, capped_check; optionally optimise on T with capped_gram.
1. (done in sessions 7-8 except the Lemma 9.1 optimisation) Rung 212 (Charton et al., k = 45): extend the input format for per-m caps (their Table 3, /5000 values) in capped_check.py and capped_exact.py; evaluate our cap-free degree-21 vector (code/cert_ax45_capfree_D21e.json, cap-free 4.012272) on their capped support and compare with their claimed 4.00438. Note their level/parameters need checking against their own equidistribution claims (Claimed).
2. Rung 236 (k = 48, Kintali; Song-Yue): read the sources (WebFetch arXiv, pdftotext), record the support and parameters in notes/, then the same pipeline.
3. Optional for 240: optimise P on T itself (Gram matrices of the corrections; capped_check's contraction structure is the faster base) to report the margin; and Stadlmann's own basis B19/B21.
4. Own: a ceiling that sees the caps (weight depending on large coordinates); floor for multi-band supports; Track B (Bombieri's asymptotic sieve, Heath-Brown's Siegel-zero theorem as Lean Props).

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
