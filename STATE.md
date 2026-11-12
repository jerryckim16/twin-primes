# Handoff (rewrite this file at the end of every session)

Home: GitHub repo jerryckim16/twin-primes (branch main). Website (GitHub Pages, from docs/): https://jerryckim16.github.io/twin-primes/
Each session works on a branch session/YYYY-MM-DD-HHMM, opens a pull request and merges it.

## Position (after session 3, 2026-11-12, 7 AM recovery run)
- Established in the literature: H1 <= 246 (Polymath8b 2014; Lean-formalised by Axiom given Bombieri-Vinogradov).
- Claimed in 2026 preprints: 240 (Stadlmann; MathWorld also lists H. Zhang 240), 236 (Kintali; Song-Yue), 212 (Charton et al., DHL[45,2]), 186 (OpenAI, DHL[40,2], Lean conditional on 3 axioms; MathWorld attributes the proof to GPT-6 Astra), 182 (GPT-6 Astra prompted by R. Sharifi, DHL[39,2], dated 18 Sep 2026). The Nervous-Machine re-run of PrimeGaps186 (status 7 Nov 2026): "conditionally supported ... not yet settled". The 182 PDF could not be re-opened on 12 Nov (too large for WebFetch, curl refused): re-check it.
- Reproduced end to end by this project: 272 (M_55 >= 4.00516 with even power sums of degree 20 + Lean tuple (55, 272) + BV + Maynard Prop 4.2). 270 (k = 54, degree 23) was still computing when session 3 merged: rerun `python3 code/mk_general.py 54 23 --even --cert code/cert_M54_D23e.json` (about 15-25 min, 9 GB RAM: too big for a 7 GB box; try degree 22 there). This is a reproduction, not new.
- Own result: Theorem 13 (floor of the eps-enlarged simplex): M_{k,eps} < 3.99 for every k <= 29 and every eps < 1. Certificate code/cert_floor_k29.json, checked by two interval libraries.
- The twin prime conjecture itself is OPEN. Sieve methods of this kind stop at 6 even under GEH (parity).

## What happened to the 3:34 AM and 6:34 AM runs
- 3:34 AM: nothing reached GitHub (lost).
- 6:34 AM: produced paper v0.3 and sent the PDF, then errored before pushing. Session 3 (this one, run by hand from Jerry's chat at about 7 AM) rebuilt everything in the v0.3 PDF from scratch: certificates rerun, scripts rewritten, text re-entered. Remark 16 came out differently on exact re-evaluation (4.178, not 4.146) and the paper says so.

## What exists
- paper/main.tex (v0.3): status table (now with 182); Theorem 1 (Lean, incl. DHL.mono); Theorems 2 and 4 (certificates); Lemma 3 (exponential-moment formula, own); Corollary 5 (H1 <= 270); Propositions 6 and 8 (pigeonhole rigidity); Section 4: Lemma 11 (dual lemma), Proposition 12 (eps-enlargement is exactly (1+eps) to first order), Theorem 13 (floor k <= 29), Remarks 14-17 (incl. a caution on Polymath8b Prop. 6.5); programme.
- lean/: Basic.lean (definitions, twin_iff, admissible_of_check, Admissible.sublist, DHL.mono, NarrowTuple.boundedGaps), Tuples.lean (generated), Audit.lean.
- code/mk_general.py: exact Gram matrices via Lemma 3; `--even` = even power sums. `python3 code/mk_general.py k D --even --cert code/cert_Mk_DDe.json`. code/verify_cert.py re-evaluates any stored certificate exactly from scratch.
  Timings on a 4-core / 15 GB box: even D=20 (707 coeffs) at k=55: 9 minutes, 3 GB; D=23 (1236 coeffs) at k=54: over 15 minutes and 9 GB. On a 2-core / 7 GB box run one at a time.
- code/dual_eps_cert.py (writes cert_floor_k29.json), code/check_floor_cert.py (re-check with mpmath.iv), code/dual_eps.py (floating-point Remarks 15 and 16).
- Certificates: cert_M5/102/105.json (P1,P2), cert_M64_D12.json, cert_M58_D16e.json, cert_M56_D18e.json, cert_M55_D18e.json (3.99153, a failure kept for the record), cert_M55_D20e.json (4.00516), cert_floor_k29.json.
- notes/sources-enlarged-supports.md, notes/enlarged-rigidity.md.

## Bound history
- log/bound-history.json records every time the project's end-to-end bound goes down. Append whenever status.json bounds.project decreases; never edit past entries. The website draws it as a log-scale step chart.

## Next steps (in order)
0. Track A, finish 270: M_54 > 4 (command above).
1. Track A, reproduce 246: add the eps-enlarged simplex to mk_general.py. Support (1+eps)R_k, basis (1+eps-P1)^a P^b; J outer region (1-eps)R_{k-1}: expand (1+eps-P1')^A = (2eps + (1-eps-P1'))^A binomially and integrate over (1-eps)R_{k-1} by scaling. Target M_{50,1/25} > 4 (Polymath8b: 4.0043 at degree 27). Proposition 12 says the gain over M_50 is about eps*M_50 for small eps, which is a sanity check for the code.
2. Own, main direction: sharpen Theorem 13 toward the true threshold near k = 50. Remark 16 says what a better weight must do (treat small coordinates near sparse points t' differently). Then the same dual approach for Stadlmann's hybrid support (Problem 18).
3. Check Polymath8b Prop. 6.5 against the published text (Remark 14 caution).
4. Track B: Bombieri's asymptotic sieve and Heath-Brown (Siegel zeros => twin primes) as precise statements; the bilinear-hypothesis problem as Lean Props.
5. Narrower tuples for k = 56..64 (not needed for the bound any more).

## Rotation of areas to explore (one per session, about half the effort)
variational/spectral methods; convex duality and LP/SDP bounds; exponential sums and l-adic methods (Type III); automorphic methods and large moduli (Maynard, Lichtman); zero-density and large values (Guth-Maynard); function fields (Sawin-Shusterman); Siegel zeros; multiplicative functions and entropy (Tao, Matomaki-Radziwill); additive combinatorics; probabilistic models of primes.
Done so far: session 1 combinatorics/polyhedral (perfect graphs, Prop 5); session 2 same idea on enlarged supports (Prop 8) and generating functions (Lemma 3); session 3 convex duality (Lemma 11 weights, Theorem 13).

## Workspace constraints
- Lean: curl -L https://github.com/leanprover/lean4/releases/download/v4.35.0/lean-4.35.0-linux.zip (about 900 MB), unzip, add bin/ to PATH. `lake build` in lean/ (about 15 s), then `lake env lean Audit.lean`.
- Mathlib cache host, releases.lean-lang.org and direct arxiv.org downloads are blocked (403). Core Lean only. Read arXiv through WebFetch. Do not work around blocked hosts.
- pip install --break-system-packages mpmath sympy numpy scipy python-flint. Scheduled runs: 2 cores, about 7 GB RAM. If pdflatex/latexmk are missing: apt-get install -y texlive-latex-base texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended latexmk.
- pandoc 3.1.3 cannot parse \Bigl / \Bigr: use \left / \right in main.tex.
- Helper agents may be used for reading and for testing ideas; check their proofs line by line before anything enters the paper.
