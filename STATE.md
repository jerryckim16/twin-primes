# Handoff (rewrite this file at the end of every session)

Home: GitHub repo jerryckim16/twin-primes (branch main). Website (GitHub Pages, from docs/): https://jerryckim16.github.io/twin-primes/
Each session works on the claude/... branch its system instructions name (create it from the latest origin/main), opens a pull request and merges it (squash).

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
1. Rung 212 (Charton et al., k = 45): extend the input format for per-m caps (their Table 3, /5000 values) in capped_check.py and capped_exact.py; evaluate our cap-free degree-21 vector (code/cert_ax45_capfree_D21e.json, cap-free 4.012272) on their capped support and compare with their claimed 4.00438. Note their level/parameters need checking against their own equidistribution claims (Claimed).
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
