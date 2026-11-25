# Rung 186: second, independent check of Lemma 2.4 of [14]

Source [14]: OpenAI, "Numerical certificate for prime gaps at most 186", 30 Aug 2026,
`code/third_party/openai186/short_gaps_numerics.pdf` (read with `pdftotext -layout`; printed pages 10, 12 and 14
rendered at 150 dpi to confirm (1.40)-(1.43), (2.1) and (2.9)). Page numbers are the printed ones.

Script: `code/oai186_lemma24_check2.py`, output `code/oai186_lemma24_check2.out`. Exact arithmetic (`Fraction`,
`sympy`) and python-flint 0.9.0 `arb` balls (256 bits); floats only in printed ratios. No repository code or
data was used. **1,940,407 checks, 0 failures, 63 s, peak RSS 135 MB.** Sections 1-5 were written after the
script and its output were final, and before I opened the first program's files.

**Verdict: verified as stated**, under the readings in section 2.

## 1. Statement and definitions used

- p. 14, set-up before (2.9): for a largest-fragment bin (a,b], U/(m+1) <= a < b <= z0 < U, m ∈ {2, 5/2},
  r(q) = (U−q)/m <= q, r− = (U−b)/m, r+ = (U−a)/m, s−_j = max(0, j − ⌈b/h⌉), s+_j = max(0, j + 1 − ⌊a/h⌋),
  t+_j = (j+1)h, β_j = 0 for jh < b and β_j = d_{s+_j}(r−) otherwise; upward caps in upper grids, downward caps in
  lower grids; (2.9): P_j = ŵ d̄_j(b+), A_j = 1[t+_j > a] ŵ d̄_{s−_j}(r+), B_j = ŵ[d̄_j(b+) − d_{j+1}(r−)]_+,
  C_j = 1[t+_j > a + r+] ŵ[d̄_{s−_j}(b+) − β_j]_+.
- p. 14, **Lemma 2.4**: the arrays bound the ordinary, largest-fragment, distinct-secondary and same-coordinate
  coordinates; Λ = log(b/a), λ(v) = min{1, max{0, log(v/a)/Λ}} (0 for v <= 0); the largest-fragment and coincident
  arrays are multiplied by upper bounds for λ(t+_j) and λ(min{t+_j, (mt+_j − U)/(m−1)}); Λ is charged once.
- p. 10, (1.39)-(1.43): the rank-two condition, d(q) = max{p_G, ξ, (U−q)/m}, max(p_G, ξ) <= U/(m+1), the Palm
  density Σ_j ∫ (A_j Π A_i − B_j Π B_i) dq/q with A = D_q, B = D_{d(q)} (shifted by q on the largest-fragment
  coordinate), the bound (1.41), Q = P + xA + yB + xyC and (1.43).
- p. 12, Lemma 2.2 (2.1): d_j <= D_c(jh) <= d̄_j for c = Mh, with the acceptance tests.
- p. 9, §1.5.1: q0 = U_G/(m_G + 1), bins (q0 + t_{j−1}(z_G − q0), q0 + t_j(z_G − q0)] for the lists T_1..T_6
  (6 + 12 + 1 + 2 + 4 + 5 = 30 bins). Group data from (1.13)-(1.24) (pp. 4-6).

## 2. Readings I had to fix

- The arrays are pointwise bounds of the role densities: for t ∈ C_j and q ∈ (a,b] in the feasible set, the role
  density at (t, q) is at most the array value. The fractions handle the q-measure of the feasible set.
- Role densities, from (1.41) with d(q) replaced by r(q) (the enlarged event): ordinary D_q(t); largest only
  D_{r(q)}(t−q) (t >= q); secondary only D_q(t) − D_{r(q)}(t); both in one coordinate D_q(t−q) − D_{r(q)}(t−q).
- Caps: b+ = h⌈b/h⌉, r+ rounded up, r− rounded down (M = ⌊r−/h⌋). d̄, d are the Lemma 2.2 enclosures, which I
  recompute myself (160-bit dyadics, one directed rounding per step).
- z0 = z_G. The weights ŵ_j^(e) are dropped: a common positive factor on both sides, with ŵ >= w by definition.
- β_j = 0 for jh < b is conservative: t − q <= t+_j − a holds for every j. Taken as written.

## 3. Method, and why it is independent

- **A (data).** Rebuilds the ladders and groups, checks printed z_G/h, p_G/h, max(p_G, ξ_G) <= U/(m+1),
  and for all 30 bins U/(m+1) <= a < b <= z0 < U, m ∈ {2, 5/2} and r(a) <= a.
- **B (symbolic, sympy).** (i) (1.41) − (1.40)-integrand is a polynomial with nonnegative coefficients in B_i and
  δ_i = A_i − B_i >= 0 (d = 2..6, every j), i.e. a positivity certificate; (ii) [xy] Π_i (P_i + xA_i + yB_i + xyC_i)
  equals the four placements, and the role substitution P → A, A → B^sh, B → A − B, C → A^sh − B^sh turns it into
  Σ_j (1.41) (d = 2..6); (iii) (1.43) for d = 1..40 in R[x,y]/(x², y²); (iv) ∫_(a,b] 1[q < v] dq/q = Λλ(v) in
  all three cases; same-coordinate feasibility t > q + r(q) ⟺ q < (mt − U)/(m−1), q + r(q) increasing, equality
  at t = a + r+.
- **C (Lemma 2.2 enclosures).** All 90 caps (b+, r+, r− for each bin, M = 20689..49152) computed to j = N; all
  pass acceptance; d_j <= ρ(j/M) <= d̄_j at 18,269 grid points against my own rigorous ρ (power series about
  k + 1/2 with an inductive tail bound, about 1e−50).
- **D (per cell).** For each bin, every 53rd cell plus all cells within 3 of each index threshold (⌊a/h⌋,
  ⌈b/h⌉, ⌊(a+r+)/h⌋, ⌈(b+r−)/h⌉, ⌊r∓/h⌋, U/h, n − 1): 57,118 cells, and at 7 exact points (t,q) each (four
  corners of C_j × (a,b], including the extremal corner t = jh, q = b, plus 3 random): the four true role
  densities are rigorously <= the arrays; indicator ⟺ fraction > 0; λ' <= λ; a positive same-coordinate density
  occurs only where same-coordinate placement is feasible. 399,826 points. Negative controls are violated as
  expected: A with the cap r− instead of r+ (28,786 points), B with d_j instead of d_{j+1} (5,821 points).
- **E (end-to-end).** 1,022 random configurations of coordinate totals (d = 2, 3, 4 and the group dimension
  39/40) in random cells. A rigorous upper bound of the TRUE one-largest Palm integral (1.40) over q ∈ (a,b] (with
  r(q), the enlarged event) is computed by splitting (a,b] at the totals and into 100 (16 for d = 39/40) pieces,
  using monotonicity in q of each factor. It is compared with Λ·[xy]Π_i(P + xλA + yB + xyλ'C) built from the
  arrays. All pass; 1,021 have provably positive true mass; largest ratio true-upper/bound 0.9705 (O5/2 bin 8,
  d = 4).

Independence: truth-side densities use the exact ρ at the actual (t, q), not the monotone reductions of the
proof; the Palm integral is integrated directly rather than bounded by sup × fraction.

## 4. Findings

- All checks pass; the reductions (monotonicity in cap and total, the s±_j index shifts, the j + 1 index in B,
  the β_j lower endpoint, the two empty-cell indicators and the two fractions) are correct as written.
- The bound can be close to tight (ratio 0.97 in low dimension on narrow O5/2 bins), so its components are not
  wastefully loose. The negative controls show that the index and cap directions matter.
- Lemma 2.2's acceptance passes for every cap used here (all M >= 20689), unlike the small-M low kernels of
  Lemma 2.3.

## 5. Coverage limits

- Cells are sampled (about 1,900 per bin, dense around every threshold), not all j < n. The array formulas are
  uniform in j between thresholds, and every threshold neighbourhood is covered.
- The Palm-calculus steps (Mecke formula, densities D_q of coordinates with all fragments <= q) are taken from the
  paper; I check the algebra and the inequalities, not the probability theory.
- The weights ŵ and the later contraction (§2.2) are not checked.

## 6. Comparison with the first program (notes/oai186-lemma24-check.md, read after the above was final)

- **Verdict: agree** (verified as stated). Same readings: the arrays are sup-densities with the Lemma 2.2 grid
  enclosures (not cell averages); b+ and r+ are rounded up and r− down; β_j = 0 for jh < b is an optional
  weakening; the weights are a common positive factor. The first program also points out that (2.9)'s A is the
  proof's B on the owner coordinate (its R1). This matches my role table in §2, though I did not flag the
  letter clash.
- Same data: 30 bins, the hypotheses hold, caps M from 20689 to 49152. The first program counts 89 distinct caps.
  My "90 caps" in the output counts per-bin computations: one cap value occurs in two bins, and 89 are distinct.
  This is a counting difference, not a disagreement. Both find that the acceptance tests pass for all of them (to
  j <= n there, to j = N here).
- Per-cell: the first program evaluates whole-bin suprema with exact caps on 36,325 cells and 326,925 points. I
  evaluate 57,118 cells and 399,826 points. Both have negative controls, with A capped at r− in both. Its second
  control drops the C shift; mine uses the B index j. The first program also checks the index facts exhaustively
  over all 30 × 98264 pairs. I checked them once per bin as ceil/floor facts.
- End-to-end: the first program integrates d = 2 on 155 instances (max ratio 0.949). I do d = 2, 3, 4 and the
  group dimension 39/40 on 1,022 instances (max ratio 0.9705, at d = 4). These are consistent. Both indicate the
  bound is fairly tight, and the 40-dimensional case it lists as not integrated is covered here, if coarsely
  (16 q-pieces).
- The first program also runs the authors' kernels (agreement to 3·10^−44). I did not.
- No disagreement found. I made no change to my script after reading the first program.
