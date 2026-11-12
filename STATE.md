# Handoff (rewrite this file at the end of every session)

Home: GitHub repo jerryckim16/twin-primes (branch main). Website (GitHub Pages, from docs/): https://jerryckim16.github.io/twin-primes/
Each session works on the claude/... branch its system instructions name (create it from the latest origin/main), opens a pull request and merges it (squash).

## Position (after session 5, 2026-11-12, 10:30 AM run started by hand in place of the 11:34 AM slot)
- Established in the literature: H1 <= 246 (Polymath8b 2014; Lean-formalised by Axiom given Bombieri-Vinogradov).
- Claimed in 2026 preprints: 240 (Stadlmann), 236 (Kintali; Song-Yue), 212 (Charton et al.), 186 (OpenAI, Lean conditional on 3 axioms), 182 (GPT-6 Astra prompted by R. Sharifi). No news search this session (only the 3:34 AM run does it).
- Reproduced end to end by this project: 246 (unchanged). The 240 rung is NOT reproduced: best certified capped ratio 3.95972 < 4 (k = 49, degree 20).
- Session 5 results (paper v0.5, new Section 5 "Stadlmann's support"):
  - Prop. 22 (Computed): cap-free = dilation of the eps-simplex: M_k(L,tau) = 4 A1 M_{k,eps/A1}. M_{49,15/506} >= 3.9685535 (D=20) -> Stadlmann cap-free 4.016176; M_{45,8/257} >= 3.9029887 (D=21, dim 846 = Charton's dim) -> 4.012272 vs their claimed capped 4.00438.
  - Prop. 23 (Proved here): I_T <= I(P), J_T >= J - 2 sqrt(J L E), E = union bound over R_m(g, c_m) (m coords > g, sum >= cap; m <= 6 caps, m = 7 with c = 7g). code/caps_exact.py integrates R_m pieces exactly (self-tests: Lemma 3 identity, sympy k=3).
  - Prop. 24 (Computed): penalised eigenproblem (code/stadlmann_caps_opt.py) gives capped ratio >= 3.95972 at D=20 (eta = 1/800), 3.93625 at D=16. Loss: penalty forces P small on V (4.0162 -> 3.9710), Cauchy-Schwarz costs 0.011.
  - Theorem 25 (own; Proved + Computed): one-band hybrid supports, any delta/caps/minorant: no k <= 29 (omega=0), <= 28 (omega = 3/1000, 1/300), <= 26 (7/1000), <= 22 (omega <= 1/68). code/floor_hybrid.py (certify; --check re-verifies with mpmath.iv). Two-zone weight fails at the next k in each case.
  - Lean: TwinPrimes/Caps.lean (length_mul_le_sum, stadlmann_large_count, stadlmann_seven_large).
- Source re-check (helper, notes/stadlmann-recheck-s5.md): Stadlmann's parameters confirmed; his text says degree 19 in one place and <= 21 elsewhere; omega(j,j') = (A_j+A_j')/2 - 1/4; helper's reconstruction gives omega <= ~0.0032 (binding Type II). Charton et al.: P_lambda are products of power sums; their Lemma 9.1 caps (31/50, 17/25) contradict Table 3 (/5000 values).
- The twin prime conjecture itself is OPEN. Sieve methods of this kind stop at 6 even under GEH (parity).

## Paper numbering (v0.5)
Thm 1 Lean; Thm 2, 4 certificates; Lemma 3 EGF; Cor 5 (270); Thm 6 M_{50,1/25}; Cor 7 (246); Props 8, 10 rigidity; Lemma 13 dual lemma; Prop 14 first order; Thm 15 floor k<=29; Remarks 16-18; Prop 19 (t_m,S)-family; Remarks 20 (k=49 extrapolation), 21 (scope). Section 5: Prop 22 cap-free, Prop 23 cap bound, Prop 24 capped 3.9597, Thm 25 hybrid floor, Remark 26. Section 6 Programme (label sec:prog).

## What exists
- code/mk_general.py: `python3 code/mk_general.py k D --even [--eps p/q] [--prec bits] [--cert out.json]`. D=20 at k=49: 2.5 min build; D=21 at k=45: 3 min; D=25 at k=50: 16 min.
- code/verify_cert.py re-checks any mk_general certificate.
- code/caps_exact.py (CapPieces: exact integrals over R_m(g,c); `python3 code/caps_exact.py` runs the self-tests).
- code/stadlmann_caps_opt.py k D --etas ... --out: penalty Gram (D=16: 4 min; D=20: 32 min, single-threaded) + eigen + exact bounds. code/stadlmann_caps.py: first attempt (cap-free vector, union bound without the g condition; failed, kept for the record).
- code/floor_hybrid.py k omega --out / --check files: Theorem 25 certificates code/cert_floor_hybrid_k*_w*.json.
- code/dual_eps_cert.py, check_floor_cert.py (Theorem 15), dual_lp.py (Prop 19), scan_eps.py / extrapolate_eps.py (Remark 20).
- Certificates: cert_M50e25_D25e/D27e (246), cert_stad49_capfree_D20e, cert_ax45_capfree_D21e, cert_stad49_caps_D20e (capped, 3.9597, not > 4), cert_floor_k29, cert_floor_hybrid_*.

## Bound history
- log/bound-history.json: 578 -> 330 -> 288 -> 278 -> 272 -> 270 -> 246. Unchanged this session. 240 would also rest on Stadlmann's equidistribution estimates (Claimed); if the variational part is ever certified, record it as conditional and discuss before lowering bounds.project.

## Next steps (in order)
1. Track A, 240: compute J_T(P 1_T) EXACTLY. Write J_T = J - 2 int a b + int b^2 with b the marginal over the violation part of the fibre; on the fibre over u' the set {u_k : (u',u_k) not in T} is an interval [U(u'), L-|u'|] determined by the large set of u' (u_k <= g never violates if u' is admissible; u_k > g violates iff s_I(u') + u_k > C_{|I|+1}). Decompose u' by its large set (inclusion-exclusion with shifted power sums as in caps_exact.py) and get exact quadratic forms; then optimise P directly on T (no penalty). Degree 20-22 should then reach > 4 if Stadlmann is right (cap-free 4.016). Check against Charton et al.'s 4.00438 at k=45 (their Table 3 caps) as a test of the formulas.
2. A degree-22 capped run (code/stadlmann_caps_opt.py 49 22) was started this session; if runs/stad49_capsopt_D22.log is incomplete it was killed at the end of the session: resume with `nohup python3 code/stadlmann_caps_opt.py 49 22 --etas 1/400,1/800,1/1600 --out code/cert_stad49_caps_D22e.json > runs/stad49_capsopt_D22.log 2>&1 &` (about 2 h single-threaded). Low priority: the method's ceiling is far below 4.
3. Own: a floor that sees the caps (Theorem 25 ignores them), e.g. a dual weight that is large on large coordinates; or the Collatz-Wielandt weight (STATE of session 4). Multi-band supports: J has cross terms between bands.
4. Track B: Bombieri's asymptotic sieve and Heath-Brown (Siegel zeros => twin primes) as precise statements; the bilinear-hypothesis problem as Lean Props.

## Rotation of areas to explore (one per session, about half the effort)
variational/spectral methods; convex duality and LP/SDP bounds; exponential sums and l-adic methods (Type III); automorphic methods and large moduli (Maynard, Lichtman); zero-density and large values (Guth-Maynard); function fields (Sawin-Shusterman); Siegel zeros; multiplicative functions and entropy (Tao, Matomaki-Radziwill); additive combinatorics; probabilistic models of primes.
Done so far: session 1 combinatorics/polyhedral; session 2 enlarged supports + generating functions; session 3 convex duality (Theorem 15); session 4 variational/spectral (convex program over dual-weight families, Collatz-Wielandt view, degree extrapolation); session 5 convex duality again, applied to the 2026 hybrid supports (Theorem 25) plus exact integration over cap regions. Next: exponential sums / Type III (which constraint on omega is binding, cf. the helper's omega <= 0.0032), or Siegel zeros for Track B.

## Workspace constraints
- Lean: curl -sSL -o lean.zip https://github.com/leanprover/lean4/releases/download/v4.35.0/lean-4.35.0-linux.zip, unzip in /root/tools, add bin/ to PATH. `lake build` in lean/ (about 25 s), then `lake env lean Audit.lean`.
- python3 is 3.11 at /usr/local/bin: install with `python3 -m pip install ...` (plain `pip` installed into python3.13 this session). Packages: mpmath sympy numpy scipy python-flint cvxpy.
- apt needs `apt-get update` first for texlive. pdftotext is available (used to read the Polymath8b PDF fetched through WebFetch).
- Mathlib cache host, releases.lean-lang.org and direct arxiv.org downloads are blocked (403). Core Lean only. WebFetch of arxiv.org/pdf/... saves the PDF; read it with pdftotext. Do not work around blocked hosts.
- Website math: the paper is typeset with KaTeX (build_site.py runs pandoc --katex). Text in status.json and log/*.json is shown through code/texify_text.py, which typesets plain notation (M_{k,eps}, H1, DHL[k,2], eps, <=, ...) at build time; you may also write TeX inside $...$ there. Never put a literal $ in that text for anything but math.
- pandoc 3.1.3 cannot parse \Bigl / \Bigr: use \left / \right in main.tex.
- Helper agents may be used for reading and for testing ideas; check their proofs line by line before anything enters the paper.
