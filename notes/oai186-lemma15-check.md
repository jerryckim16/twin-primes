# Rung 186: check of Lemma 1.5 of [14] (full-radius factorization of the low-bin weight)

Source [14]: OpenAI, "Numerical certificate for prime gaps at most 186", dated 30 August 2026. The PDF is at
`code/third_party/openai186/short_gaps_numerics.pdf`. I read it with `pdftotext -layout`. Page numbers below are
the printed page numbers.

Script: `code/oai186_lemma15_check.py`, output `code/oai186_lemma15_check.out`. It uses exact `fractions.Fraction`
and integer arithmetic only: python-flint, mpmath and gmpy2 are not installed, and none is needed. It runs 44
checks with 0 failures in about 23 s (peak RSS about 33 MB).

**Verdict: verified as stated.** The lemma is a short bookkeeping step, and the printed two-line proof is correct.
It leaves several steps implicit: monotonicity in θ > 0 and m > 1, the bin enlargement to (Lh, Hh], which is
where u^+ comes from, the reading of L_{<=l}, the ν-null endpoint, and why d must be the full dimension 40 for the
erased coordinate. I supply each of these below. None needs a repair. The "+dh" term cannot be reduced to
"+(d-1)h": an explicit failing root shows that the cover would then fail (section [4] of the script). The
implementations agree with (1.38) on every retained index of every low bin: our four evaluators and the authors'
script. I found no discrepancy between the PDF and the code for this factor.

## 1. Definitions (with page references)

- p. 1. ν = ν_ζ is e^γ ζ times the law of the Poisson process on (0, ζ] with intensity dv/v. A fragment
  configuration X is a multiset, with |X| = Σ_{p∈X} p. The erased-coordinate operator is
  E_i F(Y) := ∫ F(Y ⊕_i X) dν(X), where Y ⊕_i X inserts X in coordinate i.
- p. 2, (1.3)-(1.4). N = 98304, h = S/N, n = N - 40 and C_j = [jh, (j+1)h). "A d-coordinate cell with index sum
  r" is the cell (j_1, ..., j_d) with r = Σ j_i. Its coordinate totals satisfy t_i ∈ C_{j_i}, so
  rh <= s < (r + d)h.
- p. 2, (1.5). These are the face masks. The largest retained index is 98263 (outer), 89524 (base) and 89914
  (enlarged).
- p. 5-6, (1.22)-(1.24). These give the six groups G1..G6 = O_2, O_{5/2}, I_2^old, I_{5/2}^old, I_2^new,
  I_{5/2}^new, with dimensions d_G = 40, 40, 39, 39, 39, 39 and parameters (m_G, ξ_G, U_G, b_G, t_G, z_G, p_G).
- p. 6, (1.25)-(1.26). These give the retained full-cell interval floor(b_G/h) - d_G + 1 <= j <= floor(t_G/h),
  intersected with (1.5), and for a low bin ending at u the clipped lower boundary c_G(u).
- p. 9, Sec. 1.5.1. "For a group G write its parameters as (d, m, ξ, U, z, p_G)." These are the d, m, U of
  (1.38). The endpoint lists U_1..U_6 define 61 low bins (l, u]. The slope is θ = ceil(7/u), except θ = 120 at
  (G1, L3) and θ = ceil(9/u) throughout G6.
- p. 9, Sec. 1.5.2, (1.36)-(1.37). If a witness lies in a low bin (l, u], then L_{<=l} < s + (m-1)u - U, and the
  event is covered by Σ_{p∈X∩(l,u]} exp(θ{s + (m-1)u - U - L_{<=l}}). **L_{<=l} is not defined in [14].** I read it,
  as notes/sources-186-loss.md does, as the total size of the fragments <= l in the root. This is the only reading
  consistent with Lemma 2.3, where those fragments carry the tilt e^{-θt}. s is the root total: 40 coordinates for
  the outer groups and the 39-coordinate face for the inner groups.
- p. 10. **Lemma 1.5.** "If u^+ = h⌈u/h⌉, the residual radial factor is
  W_r = exp(θ{rh - U + (m-1)u^+ + dh}) (1.38). For an erased coordinate of index v, use W_{r+v} before summing
  over that coordinate." Proof: "The identity Π_i e^{θ(j_i h - U/d)} = e^{θ(rh-U)} together with the full-cell
  correction proves the formula. On an erased-coordinate term the full index is r + v, giving exactly (2.20)."
- p. 12-13, (2.4)-(2.7) and Lemma 2.3. For a low bin (l_0, u_0], (l, u, z) := (Lh, Hh, Kh) with L = floor(l_0/h),
  H = ceil(u_0/h) and K = ceil(z_0/h). So the bin is enlarged to (Lh, Hh], and Hh = u^+. D_θ = h Σ_j d*_j(l)
  e^{-θjh} X^j tilts the fragments <= l. The mark polynomial M = Σ_{a=L}^{H-1} X^a/a covers [Lh, Hh). B_θ and M_θ
  majorize the physical-cell masses of (e^{-θt} D_l(t) dt) * exp_*(1_{(l,z]} dv/v), and of the same with a
  designated fragment in (l, u]. "Apply (1.38) at the full index before erasure" (p. 13).
- p. 15, (2.16). The marking rings. Profile power 2 applies on retained coordinates and power 0 on the erased
  coordinate.
- p. 16, (2.17)-(2.21). "Its radial weight is W(r) := exp(θ{rh - U_G + (m_G - 1)u^+ + d_G h}) ... Only indices
  with χ_G = 1 are evaluated, and their exponent is less than 700." The outer erased-coordinate form (2.20) is
  C(r) = Σ_{a=0}^{n-1-r} χ_G(r+a) W(r+a) K_a^{(0)} and H_η(r) = [*] C(r)[X^r]M_{39,η}: "The event and radial weight
  remain at the full index r + a; the erased coordinate carries no extra profile factor."

## 2. Statement in my notation

Fix a group G with (d, m, U), d ∈ {39, 40} and m ∈ {2, 5/2}, and a low bin (l_0, u_0] with slope θ > 0. Put
L = floor(l_0/h), H = ceil(u_0/h) and u^+ = Hh. Let X = (X_1, ..., X_d) be a root, with coordinate totals t_i in
cells j_i, r = Σ j_i and s = Σ t_i. Let L_i be the total of the fragments <= Lh in coordinate i. Then

    exp(θ{s + (m-1)u_0 - U - L_{<=l_0}})  <  W_r · Π_i e^{-θ L_i},   W_r = exp(θ{rh - U + (m-1)u^+ + dh}).   (*)

Consequently, on the event "some p ∈ (l_0, u_0] has Σ_{q>=p} q + (m-1)p > U", the bound below holds:

    1  <=  #(X ∩ [Lh, Hh)) · W_r · Π_i e^{-θ L_i}   (ν-a.e.).

The product Π_i (count-marked, e^{-θ L_i}-tilted coordinate measure) is what Lemma 2.3 majorizes cellwise.
W_r depends on the cell only through r, so it multiplies [X^r] of the product moment.

Erased coordinate (outer groups, d = 40). For a 39-coordinate face Y of index sum r and an erased coordinate X_i
of index v, the root Y ⊕_i X_i has index r + v. Its weight is W_{r+v}, with d = 40, and its mask is χ_G(r+v).
|V_i(Y)|^2 does not depend on X_i. So integrating the majorant over X_i against ν (profile power 0) gives
Σ_v χ_G(r+v) W_{r+v} K_v^{(0)} = C(r), which is (2.20).

## 3. Proof, step by step

| # | Step | Status | Exact check (script section) |
|---|------|--------|------------------------------|
| 1 | (1.36): a witness p ∈ (l_0, u_0] gives L_{<=l_0} < s + (m-1)u_0 - U | **verified** (not part of 1.5; needed for its use) | Every q >= p exceeds l_0, so Σ_{q>=p} q <= s - L_{<=l_0}, and (m-1)p <= (m-1)u_0. So the exponent in (1.37) is > 0 on the event, and the Palm sum (count >= 1) is > 1. Section [4]: all 3443 failing random roots. |
| 2 | The (1.37) exponent does not depend on the witness p, so the Palm sum is N_{(l,u]} · exp(·) | **verified** (implicit) | By inspection of (1.37). This is what lets the radial factor be pulled out of the Mecke marking. |
| 3 | "The identity Π_i e^{θ(j_i h - U/d)} = e^{θ(rh - U)}" | **verified** | Σ_i (j_i h - U/d) = rh - U. Section [2](a): exact, 2000 random index vectors, d ∈ {39, 40}. |
| 4 | "Full-cell correction", radial part: t_i < (j_i + 1)h, so θs < θ(r + d)h | **verified** (needs θ > 0) | [1]: θ is a positive integer on all 61 bins. The slack is θ Σ_i ((j_i+1)h - t_i) > 0. |
| 5 | Endpoint part: (m-1)u_0 <= (m-1)u^+ | **verified** (implicit; needs m > 1, u_0 <= u^+) | [1]: u_0 <= u^+ < u_0 + h on all 61 bins. u^+ = u_0 exactly on the 6 bins ending at p_G, which are grid-aligned. u^+ = Hh is the upper end of the enlarged bin of (2.4). The proof's words "full-cell correction" cover this step only implicitly. |
| 6 | e^{-θ L_{<=l_0}} <= Π_i e^{-θ L_i} (cutoff rounded down to Lh) | **verified** (implicit; belongs to Lemma 2.3's set-up) | L_{<=Lh} <= L_{<=l_0} [4]. The kernel's further rounding e^{-θ L_i} <= e^{-θ h floor(L_i/h)} only enlarges [4]. |
| 7 | Count: N_{(l_0,u_0]} <= N_{[Lh, Hh)} | **verified** up to a ν-null set | On the 6 grid-aligned bins, a witness exactly at u_0 = Hh lies in C_H, outside the mark range. The intensity dv/v has no atoms, so this does not affect the cover. [4] checks the count off that null set. |
| 8 | (*), and the cover 1 <= N · W_r · Π e^{-θ L_i} | **verified** | [4]: 7320 random exact roots on all 61 bins (120 per bin, d = 40 / 39, real U, m, θ, u, z_G, totals in the retained radial range). (*) holds strictly on all of them, and the cover holds on all 3443 failing ones. |
| 9 | Erased coordinate: use W_{r+v} with the full dimension d = 40 | **verified** | [3]: W_{r+v} = exp(θ{Σ over all 40 coordinates of (j_i+1)h - U + (m-1)u^+}) = W_r e^{θvh}. [4], sharpness: an explicit failing root of O_{5/2}, bin L22 (u = p_G, so u^+ = u), with r = 96008 retained. Its 40 coordinate totals sit h/2000 below a grid point and its failure margin is about h/8. With dh the majorant exponent exceeds the Palm exponent by exactly 40θh/2000 > 0. With (d-1)h it is < 0, so the cover fails. So the face dimension 39 would be wrong here; d_G = 40 is needed. |
| 10 | "Their exponent is less than 700" (p. 16) | **verified** | [3]: exact, on all 143,512 retained (bin, r) pairs, with r from lo(u) = max(R0, floor(c_G(u)/h) - d + 1) to R1. The exponent increases by θh per index. The maximum is 13.768 (I_{5/2}^new, L11, r = 89914). The smallest exponent on any retained index is 0.070 (O_2, L2), so W > 1 there. |

Negative controls ([4]). Replacing u^+ by the lower endpoint l leaves 2231 of the 3443 failing random roots
uncovered. Random roots almost never come close enough to the cell edges to break the variants d -> d-1 or
u^+ -> u - h (0 each). That is why the sharpness of dh is shown by the explicit construction in row 9.

Remark, not used and not checked by the script beyond row 6. Take a coordinate with no fragment > Lh. Its cell
slack (j_i+1)h - t_i, together with Lemma 2.3's tilt slack L_i - h floor(L_i/h), adds up to exactly h. So in the
composite bound (kernel × W) the term dh is generous by h for every such coordinate. That is only conservatism,
and (1.38) as stated is what the forms use.

## 4. Code consistency

All of the following was checked exactly by evaluating the code's own weight expressions. They were pulled out
with `ast` and evaluated with a stand-in for arb/mpmath that records exp(x) as its exact argument x. The resulting
exponent was compared with θ(rh - U + (m-1)u^+ + dh) at every index.

- **`code/oai186_loss_outer.py`** (O_2, O_{5/2}). `expo0 = θ(-U + (m-1)·ceil(u/h)·h + 40h)`, and `f_full[r]` is
  W on the full 40-coordinate index, zero off lo(u)..R1. This holds on all 32 outer bins (88,421 retained
  (bin, r) pairs). The low-bin schedule (l, u, θ, c_G(u)) equals Sec. 1.5.1 / (1.26). The R form (2.17) uses
  `f_full[R0+i]`. The V form uses `correl(f_full, K^(0))`, which I executed on small exact data with a
  pure-Python polynomial. It equals Σ_{a} f(r+a)K(a), so W sits at the full index r + a, as in (2.20). The
  erased arrays `arrays0 = {(0,): bc, (1,): mc}` carry no profile factor.
- **`code/oai186_loss_inner.py`** (four inner groups). It uses the same expression with `KD = d = 39`, with
  `Wr[i]` at r = R0 + i and `pair()` skipping i < lo_index - R0. This holds on all 29 inner bins (55,091 pairs).
  The inner forms have no erased coordinate, so d = 39 is the full root dimension there, which is correct.
- **`code/oai186_loss_I2old.py`** (Session 15, superseded). It uses the same weight with θ = ceil(7/u) and
  KD = 39 on all 5 I_2^old bins.
- **`code/oai186_loss_outer2.py`** (independent O_{5/2} evaluator, bins L19..L22). It has
  `W0 + θ r h = θ(rh - U + (m-1)u^+ + 40h)` on every retained index. Its `Wcoef`, run with a multiplicative
  stand-in, equals Σ_a χ(r+a) W(r+a) K0(a).
- **Authors' `prime_gap_186_certificate.py`.** The 61 low tasks have exactly our (l, u, θ). The weight is built
  from `last = ceil(high/step)`, `high = last*step` (= u^+) and
  `offset = (order - 1)·high + dimension·hq`. The resulting `radial[j] = exp(θ(jh - U + (m-1)u^+ + d h))` holds on
  every active index (143,512 pairs) and is zero elsewhere. The active set of the clipped group equals our
  lo(u)..R1 on all 61 bins. `_source_fiber` multiplies the window by this factor at the full index before the
  erased correlation, as its docstring says ("W is a function of the full radius BEFORE erasing").

**Discrepancies: none.** The PDF's (1.38) and its restatement after (2.16) on p. 16 agree, and every
implementation agrees with both. The 1.4 note found that upstream's 5/2 groups omit the absorbed order-two rows
when clipping. That difference has no effect here either: the clipped active index sets coincide on all 61 bins.

## 5. Not covered here

- Lemma 2.3 itself: that B_θ and M_θ majorize the tilted, marked physical-cell masses (Eulerian carries, the
  Dickman/renewal majorants d*_j). I use only its statement.
- Lemma 1.6 (containment of the clipped radial intervals). I only recompute c_G(u) and compare it with the code.
- Whether the 61 bins and the rank-two and factorial components together cover every witness rank.
- The numerical values of the loss components.

The random test in [4] is a sanity check. The proof is the algebra in rows 1-9.
