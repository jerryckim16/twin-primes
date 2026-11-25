# Rung 186: second, independent check of Lemma 1.5 of [14]

Source [14]: OpenAI, "Numerical certificate for prime gaps at most 186", 30 Aug 2026,
`code/third_party/openai186/short_gaps_numerics.pdf` (read with `pdftotext -layout`; pages 4 and 10 also rendered
as images to confirm (1.13)-(1.16) and (1.38)). Page numbers are the printed ones.

Script: `code/oai186_lemma15_check2.py`, output `code/oai186_lemma15_check2.out`. Exact arithmetic only:
`fractions.Fraction`, `sympy` (exact symbolic identities) and python-flint 0.9.0 `arb` (rigorous balls, 200 bits).
No repository code or data was used; every number is recomputed from the PDF's formulas.
**510,802 checks, 0 failures, about 60 s, peak RSS about 64 MB.** Sections 1-5 were written after the script and
its output were final, and before I opened the first program's note.

**Verdict: verified as stated**, under the reading of L_{<=l} in section 2 (the PDF does not define it).

## 1. Statement and definitions used

- p. 10, **Lemma 1.5** (Full-radius factorization): "If u+ = h⌈u/h⌉, the residual radial factor is
  W_r = exp(θ{rh − U + (m − 1)u+ + dh}). (1.38) For an erased coordinate of index v, use W_{r+v} before summing
  over that coordinate." Proof: "The identity Π_i e^{θ(j_i h−U/d)} = e^{θ(rh−U)} together with the full-cell
  correction proves the formula. On an erased-coordinate term the full index is r + v, giving exactly (2.20)."
- p. 1: ν, fragment configurations X (multisets), |X|, Y ⊕_i X, E_i. p. 2, (1.3): N = 98304, h = S/N,
  n = N − 40, C_j = [jh,(j+1)h). (1.4): a d-coordinate cell with index sum r.
- p. 4, (1.13)-(1.16): constants, ladders ω, δ (stop at the first Ω), B, ξ, a, b. p. 5-6, (1.18) caps,
  (1.22)-(1.24) groups with (d, m, ξ, U, b, t, z, p). p. 9, §1.5.1: "write its parameters as (d, m, ξ, U, z, p_G)";
  the lists U_1..U_6, a_j = (6/5)^j/20, slopes ⌈7/u_j⌉, 120 at (G1, L3), ⌈9/u_j⌉ on G6.
- p. 9, §1.5.2, (1.36)-(1.37): for a witness in a low bin (ℓ, u], L_{≤ℓ} < s + (m−1)u − U, and the Palm sum
  Σ_{p∈X∩(ℓ,u]} exp(θ{s + (m−1)u − U − L_{≤ℓ}}).
- p. 12-13, (2.4) and Lemma 2.3: ℓ = h⌊ℓ0/h⌋, u = h⌈u0/h⌉ (= u+), D_θ carries the tilt e^{−θjh} on fragments
  ≤ ℓ; p. 13: "Apply (1.38) at the full index before erasure". p. 16, before (2.17): the same W(r) with d_G;
  (2.20): C(r) = Σ_a χ_G(r+a) W(r+a) K_a^(0); "their exponent is less than 700".

## 2. Formalization (where I had to choose)

- **L_{≤ℓ} is not defined in [14].** I read it as the total size of all fragments ≤ ℓ in the root (all d
  coordinates). This is the only reading under which (1.36) follows from a witness p ∈ (ℓ,u] (Σ_{q≥p} q ≤ s − L_{≤ℓ})
  and which matches the tilt e^{−θt} of Lemma 2.3.
- "Residual radial factor" means: on a d-cell of index sum r (t_i ∈ C_{j_i}, s = Σ t_i),
  exp(θ{s + (m−1)u − U − L_{≤ℓ}}) ≤ W_r · exp(−θ L_{≤ℓ}), i.e. W_r ≥ sup over the cell of exp(θ{s + (m−1)u − U}),
  with u the bin's upper endpoint u0 and u+ = h⌈u0/h⌉. The factor exp(−θL) is left to the kernel (Lemma 2.3).
- d is the dimension of the root the event lives on: 40 for O_2, O_5/2 and 39 for the four inner groups. For the
  erased coordinate (outer groups), r is the 39-coordinate face index, v the erased index and d = 40.

## 3. Method, and why it is independent

- **A (data).** Rebuilds S, T0, T1, ρ, ρ*, e from (1.13) (checked against (1.1)-(1.2)), both ladders (29/43 rows,
  order counts (12,12,5), (12,12,19)), the six groups, and the 61 low bins with slopes. Cross-checks the printed
  z_G/h (= ⌊cap(1.18)/h⌋) and p_G/h (= ⌊U/(2mh)⌋), and 2h < ξ < p ≤ z, z + mp ≤ U (Lemma 1.1).
- **B (symbolic proof, sympy).** For d = 39 and 40, with symbols j_i, f_i ∈ [0,1), t_i = (j_i+f_i)h, θ, h, U, m,
  u, u+: (a) the product identity of the proof; (b) the exact decomposition
  log W_r − θ(s + (m−1)u − U) = θh Σ_i (1 − f_i) + θ(m−1)(u+ − u),
  which is > 0 once θ > 0, m > 1, u+ ≥ u; (c) the Palm-term split exp(θ{…−L}) = exp(θ{…})·exp(−θL); (d) erased
  coordinate: W at r39 + v with d = 40 equals the full-cell bound; (e) negative control: a retained-only correction
  (39h + vh) is below the residual (retained f_i → 1, erased f = 1/2), so the erased cell must be counted.
- **C (exact grid, all 61 bins).** θ > 0, m > 1, u+ is the least grid point ≥ u0 (u0 ≤ u+ < u0 + h). For every r
  in 0..n−1 with stride 211 plus endpoints (469 values), three index vectors (balanced, concentrated, random),
  coordinate-by-coordinate: the product identity, tightness (log W_r − cell sup of the residual = θ(m−1)(u+−u0)
  exactly, so the dh correction is the least one that works), strict domination at interior points f = 0, 1/2,
  1 − 2^−40, and log W affine in r with step θh (monotone). Outer bins: 60 random (r39, v) splits with random
  dyadic positions, checking domination by W_{r+v} and W_{r+v} = W_r e^{θvh}.
- **D (end to end).** 400 random exact roots per bin (24,400 events) built to contain a witness p ∈ (ℓ0,u0] with
  inclusive prefix + (m−1)p > U, fragments placed in random coordinates; checks log W_r − θL_{≤ℓ} > 0 with the
  kernel cutoff ℓ = h⌊ℓ0/h⌋ (so 1 ≤ the Palm sum majorant), and (1.36) itself.
- **E (rigorous).** arb enclosures of W_r; side claim "exponent < 700" on a *superset* of the retained cells
  (r ≤ min(⌊t_G/h⌋, n−1), no c_G(u) clipping; the exponent increases with r). Largest: 69.26 (I5/2new, L1).

Independence: different decomposition (fractional positions f_i, symbolic for full d rather than random
vectors), a direct check that the dh + (m−1)u+ correction is exactly the cell supremum, end-to-end witness events
in place of a code audit, and arb balls. I did not recompute c_G(u) (Lemma 1.6), so χ_G is replaced by a
superset; this only matters for the side claim in E.

## 4. Findings

- The lemma is a correct bookkeeping step. Implicit hypotheses, all verified on the data: θ > 0 (integer on all
  61 bins), m − 1 > 0, u+ ≥ u0; and d must be the full root dimension (40) for the erased coordinate.
- The bound is sharp per cell: equality with the cell supremum exactly when u0 is on the grid (bins ending at p_G).
- The PDF's "full-cell correction" covers both θdh and θ(m−1)(u+ − u); the second is not spelled out.
- Unclear in the PDF: L_{≤ℓ} (undefined, see section 2) and whether u in (1.38) is u0 or the rounded Hh of (2.4)
  (it makes no difference: ⌈Hh/h⌉h = Hh).

## 5. Differences from the PDF's formulation

- I prove the inequality form W_r ≥ sup_cell exp(θ{s + (m−1)u − U}); the PDF says "is" (it is the supremum only
  when u0 is on the grid).
- The 700 bound is checked on a coarser superset (top index ⌊t_G/h⌋, e.g. 89953 for I5/2new, not the mask
  maximum 89914) and without the c_G(u) lower clip. It still holds with a large margin.

## 6. Comparison with the first program (notes/oai186-lemma15-check.md, read after the above was final)

- **Verdict: agree** (verified as stated). Both read L_{≤ℓ} as the total of fragments ≤ ℓ in the root, and both
  list the same implicit steps: θ > 0, m > 1, u0 ≤ u+, d = 40 for the erased coordinate. The first program also
  makes explicit the ℓ-rounding (L_{≤Lh} ≤ L_{≤ℓ0}), the count over [Lh, Hh) and a ν-null endpoint at u0 = Hh;
  these belong to the set-up of Lemma 2.3 (my Part D uses ℓ = h⌊ℓ0/h⌋ and never hits u0 exactly).
- Sharpness of dh: the first program shows it with one explicit failing root; my Part B(e) and the tightness
  identity in C show it symbolically and on every sampled cell. Consistent.
- Exponent < 700: first program 13.768 (I5/2new L11, r = 89914) on the exact clipped χ_G; mine 69.26 (I5/2new
  L1, r = 89953) on an unclipped superset. Not a disagreement: my top index exceeds the mask maximum, and since the
  clip only raises the lower index, bin L1 must have an empty retained set in the first program (otherwise its
  top index would give a larger exponent there). I did not verify that emptiness myself. Both are < 700.
- The first program also audits the repository loss scripts and the authors' script; I did not (not required).
- No disagreement found.
