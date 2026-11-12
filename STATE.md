# Handoff (rewrite this file at the end of every session)

Home: GitHub repo jerryckim16/twin-primes (branch main). Website (GitHub Pages, from docs/): https://jerryckim16.github.io/twin-primes/
Each session works on the claude/... branch its system instructions name (create it from the latest origin/main), opens a pull request and merges it (squash).

## Position (after session 4, 2026-11-12, 8 AM run started by hand)
- Established in the literature: H1 <= 246 (Polymath8b 2014; Lean-formalised by Axiom given Bombieri-Vinogradov).
- Claimed in 2026 preprints: 240 (Stadlmann), 236 (Kintali; Song-Yue), 212 (Charton et al.), 186 (OpenAI, Lean conditional on 3 axioms; Nervous-Machine re-run 7 Nov: "conditionally supported ... not yet settled"), 182 (GPT-6 Astra prompted by R. Sharifi, DHL[39,2]). No news search this session (only the 3:34 AM run does it). The 182 PDF still has not been re-opened.
- Reproduced end to end by this project: 246 = the established bound (M_{50,1/25} >= 4.0012466, even power sums degree 25, 1780 coeffs, eps-enlarged simplex; + Lean tuple (50,246) + BV + Polymath8b Thm 3.12(i)). Matches Polymath8b's 4.00124 at d=25. Reproduction, not new.
- Own results so far: Theorem 15 (was 13): eps-enlarged simplex floor k <= 29. Session 4: Proposition 19 (numerical): dual weights depending only on (t_m, S) stall near 4.14 at (50, 1/25); Remark 20 (heuristic): degree extrapolation suggests sup_eps M_{49,eps} ~ 3.993 < 4, i.e. the eps-simplex stops at k = 50. Remark 16: Polymath8b Prop. 6.5 as printed (arXiv text, re-read this session) proves only (k/(k-1)+eps) log(2k-1).
- The twin prime conjecture itself is OPEN. Sieve methods of this kind stop at 6 even under GEH (parity).

## Paper numbering (v0.4)
Thm 1 Lean; Thm 2, 4 certificates; Lemma 3 EGF; Cor 5 (270); Thm 6 M_{50,1/25}; Cor 7 (246); Table 2 eps-data; Props 8, 10 rigidity; Lemma 13 dual lemma; Prop 14 first order; Thm 15 floor k<=29; Remarks 16-18; Prop 19 (t_m,S)-family; Remark 20 k=49 extrapolation.

## What exists
- code/mk_general.py: `python3 code/mk_general.py k D --even [--eps p/q] [--prec bits] [--cert out.json]`. Precision 300-500 bits is enough (was ~6000): D=25 at k=50 took 16 min build + 4 min solve, ~3.5 GB, on 4 cores/15 GB (build is single-threaded Python; it dominates).
- code/verify_cert.py re-checks any mk_general certificate (reads the "eps" key; old certificates have none = 0). Not for cert_M5/102/105 (other format, make_cert.py).
- code/scan_eps.py (grid of certified M_{k,eps}), code/extrapolate_eps.py (heuristic Aitken/power fits), runs/scan_k49.jsonl, runs/scan_k50.jsonl.
- code/dual_lp.py: convex optimisation over weights rho(S,u)*(L-sigma+(k-1)u) (cvxpy + Clarabel; pip install cvxpy). `python3 code/dual_lp.py k eps Nc N` (use Nc = N). Logs in runs/dual_lp_*.log.
- Certificates: cert_M50e25_D25e.json (new), cert_M54_D23e.json, cert_M55_D20e.json, ... , cert_floor_k29.json.
- Lean: Basic.lean now also has isPrime_two, not_boundedGaps_one, admissible_pair_iff.
%D27%

## Bound history
- log/bound-history.json: 578 -> 330 -> 288 -> 278 -> 272 -> 270 -> 246. Append whenever status.json bounds.project decreases; never edit past entries. Next rung would be 240 (k = 49), which needs Stadlmann's support.

## Next steps (in order)
1. Track A, reproduce 240: Stadlmann's support T_k (notes/sources-enlarged-supports.md §2): eps = 0.0075, A1 = 0.253, delta = 0.028, caps B_{1,1}=B_{1,2}=0.15, B_{1,m}=0.17 (m>=3), k = 49, basis p^2 (1 - sum t)^b, D = 19. Needs integrals over the simplex with rough-mass caps (sum of coordinates > delta at most B_{|I|}): think about inclusion-exclusion over which coordinates exceed delta, or Monte-Carlo-free exact formulas; first re-read arXiv:2608.31126 Def. 1, Def. 5, Prop. 1 and §5.1.
2. Own, main direction: Collatz-Wielandt weights psi_m = (int F dt_m)/F from a positive approximate extremal F (Prop. 19 says (t_m,S)-weights cannot reach the truth). Try F = h(S) prod g(t_i) or the Galerkin eigenfunction; the hard part is a rigorous sup over t. Also: converge Prop. 19 at (30, 1/4) (bigger N, or a better discretisation) to locate the exact floor of the (t_m,S) family.
3. Track B: Bombieri's asymptotic sieve and Heath-Brown (Siegel zeros => twin primes) as precise statements; the bilinear-hypothesis problem as Lean Props.
4. Optional: M_{49,eps} at degree 24-25 for eps 1/30, 1/25 to test Remark 20 (D=22 took about 9 min build each).

## Rotation of areas to explore (one per session, about half the effort)
variational/spectral methods; convex duality and LP/SDP bounds; exponential sums and l-adic methods (Type III); automorphic methods and large moduli (Maynard, Lichtman); zero-density and large values (Guth-Maynard); function fields (Sawin-Shusterman); Siegel zeros; multiplicative functions and entropy (Tao, Matomaki-Radziwill); additive combinatorics; probabilistic models of primes.
Done so far: session 1 combinatorics/polyhedral; session 2 enlarged supports + generating functions; session 3 convex duality (Theorem 15); session 4 variational/spectral (convex program over dual-weight families, Collatz-Wielandt view, degree extrapolation). Next: exponential sums / Type III, or Siegel zeros for Track B.

## Workspace constraints
- Lean: curl -sSL -o lean.zip https://github.com/leanprover/lean4/releases/download/v4.35.0/lean-4.35.0-linux.zip, unzip in /root/tools, add bin/ to PATH. `lake build` in lean/ (about 25 s), then `lake env lean Audit.lean`.
- python3 is 3.11 at /usr/local/bin: install with `python3 -m pip install ...` (plain `pip` installed into python3.13 this session). Packages: mpmath sympy numpy scipy python-flint cvxpy.
- apt needs `apt-get update` first for texlive. pdftotext is available (used to read the Polymath8b PDF fetched through WebFetch).
- Mathlib cache host, releases.lean-lang.org and direct arxiv.org downloads are blocked (403). Core Lean only. WebFetch of arxiv.org/pdf/... saves the PDF; read it with pdftotext. Do not work around blocked hosts.
- pandoc 3.1.3 cannot parse \Bigl / \Bigr: use \left / \right in main.tex.
- Helper agents may be used for reading and for testing ideas; check their proofs line by line before anything enters the paper.
