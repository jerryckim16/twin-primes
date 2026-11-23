# Rung 186: check of Lemma 1.6 of [14] (containment of the low-witness intervals)

Source [14]: OpenAI, "Numerical certificate for prime gaps at most 186", dated 30 August 2026,
`code/third_party/openai186/short_gaps_numerics.pdf`, read with `pdftotext -layout`. Page numbers are the printed
page numbers.

Script: `code/oai186_lemma16_check.py`, output `code/oai186_lemma16_check.out`. All decisions use exact
`fractions.Fraction` and integers. **42 checks, 0 failures**, about 6.5 s and 42 MB peak RSS.

**Verdict: verified as stated, under the natural readings fixed below.** No repair is needed. Every numerical
assertion in the proof checks exactly: the counts 10/22/5/7/6/11, the direct check (11, 2, 5 / 11, 5, 6) and
nonemptiness. The two-line argument is correct once "a source failure assigned to an interval" means **assigned by
a witness of the failing source row**. That is what the proof uses ("for an eligible originating row ... a witness
below u"). Section [5](d) gives an explicit root showing that a looser reading, "any group-level H_{m_G} witness in
the bin", would make the sentence false. The overall cover is unaffected, because that root is retained by the bin
that contains its row witness. One structural fact is not stated in the PDF: on all 61 bins the threshold term
V_t − (μ_t − 1)u never decides the minimum in (1.26). So c_G(u) = max(b_G, min of the eligible cores), and the
"own order" clause changes nothing on this schedule.

## 1. Definitions (with page references)

- p. 1. Inclusive obstruction H_{φ,ξ}(X) := max({Σ_{q∈X, q≥p} q + φ(p) : p ∈ X, p > ξ} ∪ {0}).
  **p. 4, (1.12)** defines H_{m,ξ}(X) := max_{p∈X, p>ξ} (Σ_{q≥p} q + (m−1)p) for m ∈ {2, 5/2}. So the reading
  φ(p) = (m−1)p that notes/sources-186-loss.md §0 flags as open is in fact printed in (1.12). The empty maximum is 0
  (p. 1, "throughout").
- p. 4, (1.15)-(1.16). The rows t = (ν, t) carry the **activation** ξ_t := δ_t/ρ, the cores a_t = B_t − T_ν
  (outer) and b_t = B_t − S (inner), and the thresholds A_t, C_t. The word "activation" is defined on p. 1 (for
  M_ξ, "for an activation ξ") and used for ξ_G in (1.23) on p. 6.
- p. 5, (1.20)-(1.21). Retained rows are (o, 0..27) and (n, 0..38). The predicates are
  O_t = {s ≤ a_t} ∪ {H ≤ A_t} (orders 1-2) and I_t = {s ≤ b_t} ∪ {H_2 ≤ C_t} (order 2). I_t is the whole space in
  order 1. Order 3 reduces, by Lemma 1.4 (p. 9), to a nonlargest H_{5/2,ξ_t} failure at the same threshold.
  **Reading: "radial core and threshold" (c_t, V_t) of (1.26) = (a_t, A_t) for outer groups and (b_t, C_t) for
  inner groups.** A row fails iff s > c_t and H_{μ_t,ξ_t} > V_t.
- p. 5, (1.22). These are the originating rows of G1..G6 = O_2, O_{5/2}, I_2^old, I_{5/2}^old, I_2^new, I_{5/2}^new.
- p. 6, (1.23)-(1.24). These give (ξ_G, U_G, b_G, t_G, z_G, p_G). **"The group's original lower radial boundary" =
  b_G**: the lower end of the radial interval (b_G, t_G] in (1.23), before any clipping.
- p. 6, (1.25)-(1.26). "For a low bin ending at u, include every originating row, also those of the preceding
  order-two group when m_G = 5/2 ... c_G(u) := max{b_G, min_{t: ξ_t<u} max{c_t, V_t − (μ_t−1)u}}. An empty eligible
  set gives an empty event; otherwise retain j ≥ ⌊c_G(u)/h⌋ − d_G + 1. In particular, an absorbed row keeps its own
  order." **Eligible** = an originating or absorbed row with ξ_t < u. **Absorbed (order-two) rows** = the rows of
  the preceding order-two group, used in a 5/2 group. **Absorbed order-two activation** = ξ_t of such a row; their
  minimum is ξ of that order-two group.
- p. 9, Sec. 1.5.1. The endpoint lists U_1..U_6, a_j = (6/5)^j/20, and the bins (u_{j−1}, u_j].
- p. 10, Lemma 1.6 and its proof (quoted in the script docstring).

## 2. Statement in my notation

Fix G and a low bin (ℓ, u] of G. Let X be a root (d_G coordinates; the face for inner groups) with total
s ∈ (b_G, t_G]. Suppose some originating or absorbed row t fails at X with a witness p ∈ (ℓ, u]: that is,
p ∈ X, p > ξ_t, Σ_{q≥p} q + (μ_t−1)p > V_t, and s > c_t. Then s > c_G(u). If the coordinate totals lie in the
cells j_i, then r = Σ j_i ≥ ⌊c_G(u)/h⌋ − d_G + 1.

## 3. The argument

1. ξ_t < p ≤ u, so t is eligible.
2. The prefix Σ_{q≥p} q is at most s. So s > V_t − (μ_t−1)p ≥ V_t − (μ_t−1)u, using μ_t > 1. Also s > c_t. Hence
   s > max{c_t, V_t − (μ_t−1)u} ≥ the minimum over eligible rows.
3. s > b_G because the failure lies in G's radial interval. Hence s > c_G(u).
4. The outward full-cell test is exact. A cell with index sum j has s ∈ [jh, (j+d)h), so it meets {s > c} iff
   (j+d)h > c iff j ≥ ⌊c/h⌋ − d + 1. In particular r ≥ ⌊c_G(u)/h⌋ − d + 1. The script ([5](a)) exhibits a point
   with s > c_G in the boundary cell, and shows that one index lower has none, on all 61 bins.
5. Absorbed rows. An absorbed order-two row t fails by H_2 at V_t ≥ U_G (V_t = S+e, T+e). With its own μ_t = 2, step 2
   gives s > V_t − u, which is sharper than V_t − 3u/2 and still valid. That every such failure is an
   H_{5/2,ξ_G} failure at U_G, so that it belongs to the 5/2 group at all, was checked in the Lemma 1.4 note.

Without the failing row's own witness the sentence is false. Section [5](d) gives an O_2 root:
s = 1.0087, fragments 0.0371, 0.1, 0.45 and 0.4216, all ≤ z_G. Row (o,0) fails with witness 0.1 ∈ L3. The fragment
0.0371 ∈ L1 = (ξ_G, 3ξ_G/2] is an H_{2,ξ_G} witness at U_G = S+e, but it is not a witness of any failing row.
Since s ≤ c_G(L1) = 1.00939, bin L1 drops the root. Bin L3 keeps it (c_G = b_G). So the cover holds, and the lemma
holds in the "row witness" sense that its proof uses.

## 4. Results

| # | Item | Result |
|---|------|--------|
| 0 | Rows, retained set, (1.17), group table re-derived: ξ_G = min own ξ_t, U_G = min own V_t, b_G = min own core; t_{G,2} = b_{G,5/2}; z_G and p_G; absorbed rows = rows of the preceding order-two group, μ = 2, V_t ≥ U_G; `oai186_support_data.py` all_ok | 11 PASS |
| 1 | 61 bins, counts 10, 22, 5, 7, 6, 11; strictly increasing from ξ_G to p_G; 40 order-5/2 bins | 3 PASS |
| 2 | c_G(u) on all 61 bins (table in the .out). The eligible set is nonempty on every bin. c_G ≥ b_G, nonincreasing in u. **c_G(u) = max(b_G, min eligible core) on every bin**, so μ_t is immaterial. No tie ξ_t = u | 4 PASS |
| 3 | Direct check, exact: O_{5/2} first 11 bins (u_11 = 0.0225 < ξ_{o,23} = 0.024787 < u_12 = 0.03375); I_{5/2}^old first 2 (0.01 < 0.024787 < 0.03375); I_{5/2}^new first 5 (0.0225 < ξ_{n,23} = 0.028353 < 0.06). On the remaining 11/5/6 bins the order-three minimum **equals** b_G exactly. It is never below b_G, because every own core is ≥ b_G. On the first 11/2/5 bins it is > b_G, so the split is sharp. Consequence: c_G with absorbed rows = c_G without them on all 40 bins. The same counts hold with "≤" | 12 PASS |
| 3' | Authors' script (comparison only): same 61 (ℓ, u, θ); `source_clipped_group` gives the same c_G(u) and the same first index on all 61. Its 5/2 groups omit the absorbed rows, which is harmless by row 3 | 3 PASS |
| 4 | Nonempty: (A) (1.25) ∩ whole (1.5) domain ∩ (1.26); (B) only the mask row with cap z_G; (C) c_G(u) < t_G; and each bin contains a grid point. Smallest count is 5 indices (O_{5/2} L1) | 4 PASS |
| 5 | (a) full-cell test exact; (b) 7050 exact failing roots (2229 from absorbed rows, 654 boundary roots with p = u and margin 10^-30), 16510 low witnesses, 0 lost (radially or by cell index); (c) negative controls: u→ℓ in (1.26) loses 1458 and eligibility ξ_t < ℓ loses 2449, while μ→2 loses 0 as row 2 predicts; (c') dropping absorbed rows loses 0; (d) the explicit root of §3 | 5 PASS |

## 5. Ambiguities and the readings taken

1. **c_t, V_t** ("radial core and threshold", p. 6) are not named elsewhere. I read them as (a_t, A_t) for outer
   groups and (b_t, C_t) for inner groups, from (1.21). The authors' script uses the same (`core`/`ceiling` keys).
2. **"Assigned"** (Lemma 1.6) is not defined. It must mean "via a witness of the failing source row" (see §3). The
   looser group-witness reading is false, as [5](d) shows. This does not harm the cover.
3. **"End below every absorbed order-two activation"**: I read u < ξ_t for every absorbed row, which is equivalent
   to "no absorbed row is eligible". There are no ties, so "≤" gives the same counts.
4. **"The order-three minimum is the group's original lower radial boundary"**: I read it as min over eligible own
   (order-3) rows of max{c_t, V_t − 3u/2} = b_G of (1.23). Since each term is ≥ b_G, "≤ b_G" and "= b_G" coincide.
5. **"Nonempty on this grid"**: it does not say which object is nonempty. I checked all three readings (§4 row 4).
   (1.25)'s "appropriate rows of (1.5)" can mean the whole domain mask or only the cap-z_G row. Both are nonempty.
   The upper bound ⌊t_G/h⌋ in (1.25) is outward (not ⌊t_G/h⌋ − d), which is harmless.
6. **H_2, H_{5/2}**: these are fixed by (1.12) on p. 4. This closes the item in sources-186-loss.md §7.
7. The PDF never says that the threshold term in (1.26) is inactive on this schedule. It is: c_G(u) is always the
   least eligible core, floored at b_G. So the "own order" clause for absorbed rows is a correctness statement that
   makes no numerical difference here.

## 6. Not covered

Lemma 1.4 (taken from notes/oai186-lemma14-check.md); that every failure has a witness in some low,
rank-two or factorial component (Sec. 1.5.3-1.5.4); the upper radial side ((1.25) and the masks (1.5)); and
the loss values. The random test is a sanity check; the proof is §3.
