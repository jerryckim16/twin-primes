# Rung 186: check of the finite contractions (2.16)-(2.21) of [14]

Source [14]: OpenAI, "Numerical certificate for prime gaps at most 186" (30 August 2026),
`code/third_party/openai186/short_gaps_numerics.pdf`, read with `pdftotext -layout`. The extract was kept in the
scratch directory only. Page numbers below are the printed ones.

Program: `code/oai186_contractions_check.py` (run with `/usr/bin/python3`; uses fractions, sympy 1.14; python-flint is
not needed). Output: `code/oai186_contractions_check.out`. Runtime is 172 s wall and peak RSS is 80 MB.
**127 checks (100 positive, 27 negative controls), 0 failures. All 27 negative controls fail as required.**

**Verdict (Computed with script + Proved here, by reading): verified as stated, in the scope of §4.** The forms
(2.17), (2.19) and (2.21) are exact finite rewritings of the physical source integrals they replace. The only
inequality steps are the face multiplier bound h_i <= 1, the bound w(r) >= h_i, and the sum of prefix squares over
P. These forms hold once the coordinate arrays majorise the event measure. That majorisation is Lemmas 2.3 and 2.4
and (2.8), which are checked elsewhere and not here.

## 1. What (2.16)-(2.21) are

They are not contractions in the sense of a contraction mapping, a spectral radius or an operator norm. Sec. 2.2 is
titled "Finite contractions" (pp. 14-16). The word means tensor contraction: the 40-variable squared trial is
contracted against moments of coordinate arrays. STATE.md's phrase "40-dimensional contractions" refers to this.
The objects are:

- p. 15, **(2.16)**: the marking rings and the extracted coefficients for each kind of source component:
  - low bin L_j: P + yD (mod y^2), coefficient [y];
  - rank-two P_j: P + xA + yB + xyC (mod x^2, y^2), coefficient [xy];
  - factorial H: F0 + yF1 + y^2F2 + y^3F3 (mod y^4), coefficient [y^3].

  Profile power 2 (K^(2)) applies on retained coordinates and power 0 (K^(0)) on an extra erased coordinate.
  Λ = log(q+/q-) for a rank-two bin and 1 otherwise.
- p. 16, **(2.17)**: R_G := 40Λ Σ_{r<n} χ_G(r) W(r) Σ_η Q_η(r) [X^r *] M_{40,η}. "The factor 40 bounds the sum of
  the absolute face multipliers, each at most one."
- p. 16, **(2.18)**: P(u,v) := {l ∈ {1,2,3} : max(u, c_{l+1}) < min(v, c_l)}, with c_4 := 0.
- p. 16, **(2.19)**: β_G := (40hΛ/Z) Σ_{l∈P} S(v^(l), ([X^r *]M_{39,η})_{η,r}; χ_G W). This is the inner form, where
  P = P(q-,q+) for an inner rank-two component and P(0,z_G) otherwise.
- p. 16, **(2.20)**: C(r) := Σ_{a=0}^{n-1-r} χ_G(r+a) W(r+a) K_a^(0) and H_η(r) := [*](C(r)[X^r]M_{39,η}).
- p. 16, **(2.21)**: V_G := (40h²Λ/Z) Σ_{l∈P(0,z_G)} S(v^(l), H; w), where w(r) = 1, max{|a_h+b_h|, |b_h|} or |b_h|
  according as (r+39)h <= T0, <= T1, or > T1.

They rely on these ingredients: (2.10) (p. 14, the set-partition moments M_{d,σ}[K]), (2.11) Q_η, (2.13) the
erased-marginal rows v_{s,τ} and prefixes v^(l) = Σ_{s<=l} v_s, and (2.14) the pairing S(v,M;A) (p. 15). Their
targets are the losses (1.30) (β_old, β_new) and (1.32) (E_O) on p. 8.

Remark 2.7 (p. 21) states the implicit claim: "The physical source integrals are the quantities majorized by the
computational forms (2.17), (2.19) and (2.21); these are not identified by definition". It also says the Lean
development "does not yet verify all the finite contractions". The implicit claim is the statement checked here.

## 2. The claims, in my words

For a component whose event indicator is majorised by Λ times a sum over role placements of products of
coordinate arrays κ^ρ_j (cell mass / h):

- (R) Σ_i ∫ 1_B h_i |F|² dν^40 / (hZ)^40 <= R_G. This holds because Σ_i h_i <= 40 and F² = Π g² Σ_η Q_η P_η. On the
  cells this is the identity Σ_cells χW F̃² Π K = Σ_r χW Σ_η Q_η [X^r *]M_{40,η}, with K^(2) = g²κ/Z.
- (β) Σ_i ∫_{face, event} |V_i|² dν^39 / (hZ)^40 <= β_G. Here V_i(Y) = Σ_{s<=l(Y)} Σ_a χ_s(r+a) h d_s(a) F(Y ⊕_i a)
  is the true erased marginal. Its shell set is the prefix {1..l}, where l is fixed by the face's largest fragment
  M(Y) ∈ (c_{l+1}, c_l]. The bound |V|² <= Σ_{l∈P} |v^(l)|² holds because l(Y) ∈ P.
- (V) Σ_i ∫_{event on all 40 coords} h_i(Y) |V_i(Y)|² dν^40 / (hZ)^40 <= V_G. The erased coordinate carries K^(0)
  and the full-index weight χW(r+a), which gives C(r). The four, two or four placements across the erased and
  retained coordinates come out of [*] in the ring product, and h_i <= w(r).

## 3. What was checked, and how

All decisions are exact: `fractions.Fraction`, integers and sympy polynomials. No floats are used except for
printing.

**A. Reduced models, full enumeration (d = 3 and 4 in place of 40).** There are 8 cases covering the plain cap
ring and the L, P and H rings, with P-sets {3}, {2,3}, {1,3} and {1,2,3}. The models use random positive role
arrays, random trial coefficients on the true signatures (1.6) of degree <= 6, the true profile g (1.7) on a grid
with h = 1/10, three outer shells with their own cap arrays d_s(a), and random χW, w and Λ. The following are
computed directly by summing over every cell, every role placement (the semantic placement list, not the ring
algebra) and every erased position i:

- the normalised integrals of (R), (β) and (V);
- the true marginal V_i^(l)(Y) at each prefix l, built from the cell values of F.

The results are compared with the formulas (2.10)-(2.21) as written: set partitions with falling factorials, ring
products, Q_η, the rows (2.13), the pairing (2.14), C(r) and H_η. All agree exactly, including (2.13) pointwise for
every face, position and prefix.

**B. True dimension 40/39 on a short grid (n = 5).** There are 4 cases, one per ring: plain, L, P and H. They
check (2.13), R_G, β_G and V_G with the literal factors 40Λ, 40hΛ/Z and 40h²Λ/Z and the true (40)_{|π|} and
(39)_{|π|}. Cells are enumerated by orbits of index multisets, with exact orbit sizes. Placements run over all 40
coordinates: 1600 for the P ring and 11480 for the H ring. The sum over the 40 faces is taken as 40 times one face
by symmetry; Part A verified that symmetry explicitly by summing over i.

**C. (2.18) and the prefix claim.** 4000 random exact cases (c_1 > c_2 > c_3, c_4 = 0, interval (u,v], and sampled
M including the endpoints and the cap values) confirm three things:

- the allowed shells {s : c_s >= M} form the prefix {1..l};
- M lies in (c_{l+1}, c_l];
- l ∈ P(u,v).

A further 2000 random cases confirm that the actual prefix square is at most Σ_{l∈P} prefix squares.

**D. Ring closed forms at d = 40 (sympy).** The following were verified:

- [xy](P+xA+yB+xyC)^40 = 40P^39C + 1560P^38AB, which is (1.43);
- [y](P+yD)^40 = 40P^39D;
- [y^3](F0+yF1+y²F2+y³F3)^40 = 40F0^39F3 + 1560F0^38F1F2 + 9880F0^37F1³;
- [y^3] Π_i Σ_a C(N_i,a) y^a = C(ΣN_i, 3) >= 1[ΣN >= 3], on 300 random 40-vectors. This is the factorial
  marking behind (2.8) and (1.47).

**E. Full-scale exact data.**
- (1.13) is consistent with (1.1): ρ* = 2624989/10^7, and S, T0 and T1 agree.
- (1.27)-(1.28) give a_h, b_h, d_0 and 1 - b_h = d_0 + a_h, and 0 < |b_h| <= max{|a_h+b_h|, |b_h|} <= 1. This
  supports the factor 40 in (2.17).
- The caps of (1.18), floored to h, give exactly the (1.5) caps (68225, 49152, 46580 / 68225, 44781, 35265 /
  68225, 44976, 35419). These are the z_G/h of (1.24).
- The mask ends satisfy floor(T0/h) - 39 = 89524 and floor(T1/h) - 39 = 89914.
- **w(r) >= h_i(Y) holds for all 98264 radial indices of a 39-face.** w switches below 1 exactly at r = 89525 and
  to |b_h| exactly at r = 89915, right after the H0 and H1 mask ends, so w is the tight radial envelope of h_i.
- P(0,z_G) = {2,3} for O_2 (z_G = c_2) and {3} for the other five groups.
- All 30 rank-two bins of Sec. 1.5.1 satisfy 0 < q- < q+ <= z_G <= c_1 and have nonempty P(q-,q+) contained in
  P(0,z_G). Every inner bin has P(q-,q+) = {3}.

**Negative controls (27, all fail as required):**

| Control | Count |
|---|---|
| d^{\|π\|} in place of (d)_{\|π\|} | 3 |
| single-shell rows v_l in place of prefixes v^(l) | 3 |
| 40/Z in place of 40h/Z | 7 |
| 40h/Z in place of 40h²/Z | 4 |
| K^(2) on the erased coordinate | 3 |
| χW(r) in place of χW(r+a) in C(r) | 3 |
| P ring without the coincident role C | 2 |
| T0 - 50h in place of T0 in w(r) | 1 |
| ≤ in place of < in (2.18): the set changes on some case | 1 |

## 4. Readings and differences from [14]'s formulation

1. The reduced models change only the dimension, the grid length and the data. The data are random positive
   arrays, random coefficients, h = 1/10, and x_r = (r + d/2)h - 9/10 in place of (r+20)h - 9/10. Since the claims
   are algebraic identities in these data, the true numbers are not needed. The checks are exact identities for
   all r < n; truncation mod X^n is the same as in [14].
2. The event measure is modelled as Λ × Σ_placements Π_k (h κ^{ρ_k}_{j_k}), with K^(2) = g²κ/Z and K^(0) = κ. That
   κ majorises the true event (Lemmas 2.3 and 2.4, (2.8), Lemma 1.7) is assumed here.
3. h_i is treated as a function of the cell's radial index through the masks (1.5). Fragment caps only shrink H0 and
   H1, so this is an upper envelope.
4. W and χ_G are arbitrary positive or 0/1 functions of the index. The exponent < 700 claim and Lemma 1.5 are not
   rechecked here.

## 5. Not covered

- The numerical values of R_G, β_G and V_G for the 97 components. They were re-evaluated earlier by
  `code/oai186_loss_outer.py`, `code/oai186_loss_inner.py` and `code/oai186_loss_outer2.py` (two programs for
  O_{5/2}), which agree with Tables 2.1-2.6 to about 1e-9.
- The directed arithmetic of Sec. 2.3: the 192/224-bit fixed point, the binary64 reductions and (2.26).
- The majorisation lemmas themselves, apart from the ring and factorial combinatorics in D.
- The cap forms (2.12) and (2.15).
- The restoration step (Prop. 1.3), the renewal majorant (2.3), Lemma 1.1, and rank cover beyond the P-set and bin
  facts in E.
- No input was taken from the authors' build_inputs. All full-scale constants were derived from the PDF text.

## 6. Comparison with the authors' script (opened only after the program and its output were final)

In `prime_gap_186_certificate.py`, `SourceContractions`, `affine_prefixes`, `_source_root_square`, `_source_fiber`,
`_source_face_square` and `source_component_raw` (about lines 1821-2125) were read. They agree with the reading
above on every point checked:

- R uses the factor k × max face weight = 40 × 1.
- The face weights switch at floor(T/h) - k + 1 = 89524 and 89914, as in our w(r).
- `affine_prefixes` builds the running prefix sums v^(l) and keeps l iff max(lo, c_{l+1}) < min(hi, c_l). The last
  shell uses c_4 = 0, read as `current >= 0` when there is no range, which is the same set.
- The largest range (q-,q+) is used only for inner rank-two components; outer uses P(0,z_G).
- The normalisation is k·h·(h if outer)/Z.
- The erased fibre is a correlation of χ_G·W at the full index with the power-0 kernel, i.e. C(r) indexed at r + a.
- The mixed placements are: same·ordinary + plain·both + owner·second + difference·first for P (this is (1.44)),
  Σ_deg fibre_deg × rows(order 3 - deg) for H, and witness·plain + plain·witness for L.
- Rank-two R and V are multiplied by Λ. Inner low components carry W as a radial factor, and outer low components
  use the upper endpoint of W.

No discrepancy was found.
