# Route card: LWW Section 4.8, the second sum of (4.52), (4.148)-(4.157), pp. 58-61 (2026-11-27)

## Criteria
These were written after a first read of pp. 58-61, p. 37 and pp. 45-46, before the derivation and the script.
- **Success**:
  - (4.149) and the two S-removals on p. 58 hold as operator identities on H.
  - (4.150) is a valid upper bound: the absolute value of each term of ⟨(1 − G_{-2})f, T_{-2}^C f⟩ is matched
    term by term to a summand of a restricted Φ_W, with the same weights.
  - The restricted (4.96) applies with the restriction set E(p) depending only on (r, p).
  - (4.152)-(4.155) and the p. 60 prime sum hold as stated.
  - The final bound (4.156)-(4.157) gives Σ_{d_0}|...|/d_0 ≪ XYL^{-A} uniformly.
  - The second term of (4.149) is covered by an argument that the text supports.
  - (4.31) follows from (4.26)-(4.30).
- **No-go** (would count as an error in LWW): any of
  - a step false as printed (with counterexample);
  - a weight or normalisation mismatch between ⟨·,·⟩ and Φ (∏V_i^{-(J+2)}, d_0/D, ρ-power, ψ_{-2} ↔ ψ_1);
  - a restriction set that depends on z′ (so that the measure bound (4.31) cannot be pulled out);
  - an L-power not beaten by exp(−cL^{0.1});
  - a use of Prop. 4.5(ii) outside what its proof covers.

Outcome: success criterion met, conditional on the inputs listed below. No-go not triggered.

**Classification: conditional on listed inputs.**
- **Section 4.8 itself, (4.148)-(4.157), is proved here, relative to the restricted form of (4.96).** Every step
  was re-derived.
- **(4.31) is proved here** from (4.26)-(4.30) and (2.12), including the ordering a_1 < ... < a_K that (4.29) needs.
- **Prop. 4.5(ii) / (4.96) (pp. 45-46) was checked, but only relative to the Prop. 4.5(i) machinery.**
  - Its new elements were re-derived:
    - the F_1 factorisation;
    - the H_{1,p} average bound;
    - the bound log S ≪ L^{0.96};
    - the z_1 coordinate bound;
    - the error count;
    - the form of the B_1 boundary equations;
    - r_{g̃z_0} ≡ −2r.
  - The steps marked "as in (i)" were not re-derived independently; they are inherited from the Prop. 4.5(i) card
    (2026-11-26-lww-p37-47-prop45.md, N4-N6). These are: the B_0/B_1 box count (4.110), the grouping, and the
    P-side truncation.
  - Hence (4.96) inherits that card's input U1: Lemma A.1, via (4.87)-(4.88). U1 was discharged by
    2026-11-26-lww-lemmaA1.md, relative to the Weil/Estermann Kloosterman bound (A.2) (Literature) and textbook
    facts. This was not re-checked here.
- **No error in LWW found.** There are eight terse places (T1-T8), one reading note (N1) and three harmless slips
  (S1-S3). None changes the conclusion.
- **One pdftotext artefact settled from the page image.** (4.94) prints W(w) = |∫_{M_1} e(θw)dθ| with absolute value
  bars, and Φ has |η η ψ_1|. pdftotext drops both. Without the bars, p. 46's "0 ≤ W ≤ 1" would be false:
  ∫_{M_1} e(θw)dθ is real but negative for about half of all w ((F)). With the bars it is correct, and (4.150) is a
  valid inequality.
- **Uniformity.** The bound (4.156) is uniform in d_0, Y, M, N (M, N ≥ x^δ) and v. The constants depend on K, ρ, C,
  A (through A_0) and the constant c of (4.31). The O_A(L^{-A}) of (4.151) is in fact O(exp(−cL^{3/4})), which is
  uniform in the same parameters.
- This is not a check of Prop. 4.2 or of the paper as a whole. Twins (K = 0) are untouched. There is no
  parity-breaking content, and nothing here bears on the twin prime conjecture.

## Source
- arXiv:2610.20242v2 PDF. Fetched 2026-11-27 ~18:10 UTC with curl into a new empty directory /tmp/claude-0/lww-s48/
  (not committed).
- SHA-256 `7ac341311b4a648c32c2b23b3029e1f4a3202258b55614a33ba7e8282423d000`, 895,874 bytes (matches).
- Extracted with pdftotext -layout. PDF page = printed page. The abs page was not re-fetched.
- pp. 37, 46 and 58-61 were rendered (pdftoppm, 120 dpi) and read visually. This settled:
  - the |·| in (4.94) and the |η η ψ_1| in Φ, p. 37; the same |·| appears on p. 46 and in (4.152) and (4.154);
  - the bar in "|\overline{f(P)}f(Q)| ≤ L^{4C}", p. 58;
  - that (4.152)'s second line multiplies inside Σ^†;
  - "sup_p" outside the triple integral in (4.154);
  - |ψ_{-2}| in the two z′-bounds, p. 60.
- Text read for context: pp. 17-23 ((4.9)-(4.41)), pp. 31-46 ((4.67)-(4.117), and the statement and proof of
  Prop. 4.5), p. 49 ((4.124)), pp. 57-61.

## Inputs (equation numbers as printed)
- **Definitions** (Literature, read in source):
  - (4.13) M_1, M_{-2}, ψ_1 (0 ≤ ψ_1 ≤ 1, support |u| < 8), ψ_{-2};
  - (4.17)-(4.22) d_0, Ω, S, σ, ⟨·,·⟩, D, a, b;
  - (4.25)-(4.27) r_P and the good-state conditions;
  - (4.32) S, (4.36) C, (4.38) T_{-2}^C, (4.39) G_{-2}, (4.41) A_{-2}^C, (4.42) f;
  - (4.68), (4.80) g′, (4.83) ℓ_p(g′), (4.89) g̃, (4.90) S_ℓ, (4.94) W, Φ (p. 37).
- **(J1) Prop. 4.5(ii)/(4.96), restricted form** ("Σ^* restricted to terms for which at least one of (4.26), (4.27)
  fails at (g̃z_0, p)"). This is checked here relative to (J2).
- **(J2) the Prop. 4.5(i) machinery, as checked in 2026-11-26-lww-p37-47-prop45.md.**
  - N4-N6 of that card: the box count, (4.110) and the truncated inclusion-exclusion.
  - Its input U1: Lemma A.1 ⇒ (4.88). This is discharged in 2026-11-26-lww-lemmaA1.md, relative to (A.2)
    (Weil/Estermann). That card was not re-checked here.
- **(J3) V_i = log 2 + o(1)** (p. 7, Mertens). Only V_i ≍ 1 is used, so that ∏V_i^{-(J+2)} = exp(O(L^{0.01})) in
  the error count of (ii).
- **(J4) |α_m|, |β_n| ≤ L^C** (hypotheses of Prop. 4.2), so |f(P)| ≤ L^{2C} by (4.42).
- **(J5) meas M_{-2} = meas M_1 ≪ L^{3A_0}/Y.** This was proved in the p23-27 card (R5, script (F)). It is
  re-computed in (F) here.
- **(J6) (4.124)** (p. 49), used only in the special case z = z_0, where it is elementary (step 8).

## Step-by-step re-derivation
Labels: Proved here / Literature (read in source) / Computed ((X) = script section).

**1. Reduction to ⟨f, T f⟩ (p. 58).** Proved here; Computed (A).
- f(P, p) = f(P) by (4.42), so f is invariant under permutations within the tuples, and Sf = f.
- With S* = S (4.33): ⟨f, Kf⟩ = ⟨Sf, T Sf⟩ = ⟨f, T f⟩. ✓
- (A): 30/30 random toys. NEG: f depending on the order of the tuple breaks it 30/30.

**2. (4.149).** Proved here; Computed (A).
- G_{-2} is multiplication by a 0/1 function, so G_{-2}* = G_{-2}, and A = G K G.
- ⟨f, Kf⟩ − ⟨f, GKGf⟩ = ⟨(1−G)f, Kf⟩ + ⟨Gf, Kf⟩ − ⟨Gf, KGf⟩ = ⟨(1−G)f, Kf⟩ + ⟨Gf, K(1−G)f⟩. ✓
- The support statements after (4.149) are immediate.

**3. Removing S (p. 58).** Proved here; Computed (A).
- ⟨(1−G)f, STSf⟩ = ⟨S(1−G)f, T f⟩, and S(1−G)f = (1−G)f. This holds because (1−G)f is permutation-invariant: f is,
  and the G_{-2} conditions are.
- LWW prove the permutation-invariance on p. 22 for G_1 only. For G_{-2} it is the same argument, since r_P is
  replaced by −2r_P, which depends only on P (T1).
- Likewise ⟨Gf, K(1−G)f⟩ = ⟨Gf, T(1−G)f⟩. ✓
- (A). NEG: a G that depends on the order of the tuple breaks the S-removal 30/30.

**4. (4.150).** Proved here; Computed (D).
- Expand ⟨(1−G)f, T f⟩ = Σ_{(P,p)} \overline{(1−G)f(P,p)} σ (T f)(P, p). With σ·∏V_i^{-1} = ∏V_i^{-(J+2)}, each term is
  ∏V^{-(J+2)} 1_{d_0≤D<2d_0} \overline{f(P)} f(Q) (d_0/D) η(a/Y)η(b/Y) ψ_{-2}(t/Y) ρ^{(ω(P_1)+ω(Q_1)−2K(J+1))/2}
  {1_{t=2(a−b)} − ∫_{M_{-2}}}, restricted to "bad at (P, p)".
- Change of variables: TP = g′z_0, TQ = g′z′, with g′ from (4.80) and r = c/u. Then:
  - Q ↦ z′ is a bijection from {Q ∈ Ω ∩ C : (Q, p′) ∈ S} onto {z′ : (z′, p′) ∈ S_ℓ(g′)} ((4.81), (4.83), p. 38);
  - ω(Q_1) = ω_ℓ(z′);
  - t′ := det(z_0, z′)/D = det(TP, TQ)/D = −t/2;
  - ψ_{-2}(t/Y) = ψ_1(t′/Y);
  - 1_{t=2(a−b)} = 1_{t′−b+a=0}, and ∫_{M_{-2}} e(θ(t − 2(a−b))) = ∫_{M_1} e(φ(t′−b+a)) by (4.76);
  - the restriction "bad at (P, p) with r_P → −2r_P" equals "bad at (g̃z_0, p)", since
    r_{g̃z_0} ≡ τ(w)/τ(z_0) = w_1 − 2r ≡ −2r for w = (w_1, 1).
- The triangle inequality on the brace, |f(P)f(Q)| ≤ L^{4C}, and η, ψ_1 ≥ 0 then give (4.150), with Φ_W ≥ 0 as
  printed (absolute values in (4.94); see the header). ✓
- (D) checks the identities exactly, for 4,000 random P, Q ∈ C:
  - det g′ = 1;
  - z′ is primitive with an odd first coordinate;
  - q_1 = uz′_1 − 2cz′_2;
  - det(z_0, z′) = det(TP, TQ) = −det(P, Q)/2;
  - r_{TP} ≡ −2r_P;
  - g̃(u, v, c/u) = g′.
- NEG: r_{TP} ≡ +2r_P fails 4000/4000.

**5. (4.151): applying the restricted (4.96).** Literature (J1), checked as in step 11.
- The O_A(L^{-A}) is the O(exp(−cL^{3/4})) of (4.96), weakened (S2).

**6. (4.152) (p. 59).** Proved here; Computed (B).
- The ℓ-dependent restrictions in Σ^* are exactly ℓ_p = [z_0]_p (p | Db) and ℓ_p = [z′]_p (p | Da).
- Under these restrictions ω_ℓ(z_0), ω_ℓ(z′) ≥ K(J+1). With 0 < ρ < 1 the ρ-power is ≤ 1.
- The remaining factors do not depend on ℓ, so Σ_ℓ and Σ^† can be interchanged. ✓
- (B), brute force over all 2,304 line tuples for primes {3, 5, 7, 11}, K = J = 1, 360 triples (z′, p, p′):
  - the inequality holds;
  - ω ≥ K(J+1) holds;
  - NEG: ρ = 2 breaks the inequality in 90/360 cases (exactly the triples with D | det).

**7. (4.153).** Proved here; Computed (B).
- D, a and b are squarefree and pairwise coprime (the entries are distinct, and the P_i are disjoint). So the
  ℓ-average factorises prime by prime:
  - q ∤ Dab contributes (q+1)^{-1}(q+1) = 1;
  - q | a or q | b contributes (q+1)^{-1};
  - q | D contributes (q+1)^{-1}1_{[z]_q=[z′]_q}.
- For z and z′ nonzero mod q, [z]_q = [z′]_q ⟺ q | det(z, z′). With D squarefree, the product over q | D is
  1_{D|det(z,z′)}. ✓
- (B): exact equality at ρ = 1 (Fractions) for 360/360 triples; 90 of them have D | det.
- NEG: dropping the constraint at p | D breaks it 270/360.

**8. p. 60 prime sum, and (4.154).** Proved here; Computed (C).
- The weight ∏_{q|Dab}(q+1)^{-1} factorises over i. The sum over ordered distinct (p_{i,1}, ..., p_{i,J+1}, p′_i) is
  ≤ (Σ_{q∈P_i}(q+1)^{-1})^{J+2} ≤ V_i^{J+2}, which cancels ∏V_i^{-(J+2)}. ✓
- E(p) depends only on (r, p), and the z′-sum depends on (D, a, b, u, r). The finite sums interchange with ∫, and
  pulling out Σ_{p,p′}(weights) ≤ ∏V^{J+2} leaves sup_{p,p′} of the triple integral over [1,16]×[1,2]×E(p). This is
  (4.154). Its conditions g̃z′ ∈ Ω′ and D | det are kept, and the other ℓ-independent conditions are dropped, since
  everything is nonnegative. ✓
- (C): exact, K = 2, J = 1, 2, three toy set pairs. NEG: an extra 1/(J+2)! per i (an unordered-tuple misreading)
  fails 6/6.

**9. (4.155) and the two z′-bounds (p. 60).** Proved here; Computed (E), (F).
- t′ = det(z_0, z′)/D = z′_2/D, so z′ = (h, −Dt/2). Write u = d_0YMs with s ∈ [1, 16]. The first coordinate of
  g̃z′ is uτ(z′) = u(h − 2rz′_2) = u(h + rDt). So g̃z′ ∈ Ω′ forces d_0YM ≤ u(h + rDt) ≤ 16d_0YM, hence
  1/16 ≤ h + rDt ≤ 16.
- This is (4.124) with z = z_0 and w_z = (0, 1). The interval has length 15 + 15/16 < 16, so it contains at most 16
  integers. ✓
- Indicator: t = 2(a−b) is fixed, so at most 16 vectors z′, and |ψ_{-2}| ≤ 1.
- Major arcs: ψ_{-2}(t/Y) ≠ 0 ⟹ |t| < 16Y. t ∈ 2Z because D | z′_2 (T6). At most 16Y values of t, 16 vectors z′ each,
  and |∫| ≤ meas M_{-2} ≤ 4L^{3A_0}/Y (J5). Total ≤ 16·16Y·4L^{3A_0}/Y ≪ L^{3A_0}. ✓
- (E): in 20,000 random cases {h : g̃z′ ∈ Ω′ (first coordinate)} ⊂ {h : 1/16 ≤ h + rDt ≤ 16}. The counts are ≤ 16
  (max seen 15 and 16 respectively). The "≤ 15" control is a tightness check, not a misreading.
- (F), exact arcs, four (L^{A_0}, Y):
  - (4.76) holds for even t;
  - ∫_{M_1} e(φw) is real, |·| ≤ meas M_1, and |W(−w)| = |W(w)|;
  - NEG: (4.76) with t odd fails 240/240 (the left side vanishes), so t ∈ 2Z is genuinely used.

**10. Measure bound and (4.156)-(4.157) (pp. 60-61).** Proved here; Computed (G).
- r ↦ −2r on T is measure-preserving in the sense meas{r : −2r ∈ F} = meas F, since the map is 2-to-1 with
  Jacobian 2. So meas E(p) = meas{r : (4.26) or (4.27) fails with r_P = r} ≪_K exp(−cL^{0.1}) by (4.31), uniformly
  in p. ✓
- Inserting this into (4.154): |⟨(1−G)f, Kf⟩|/(d_0YMN) ≪ L^{4C}(16 + L^{3A_0})·15·e^{−cL^{0.1}} + L^{-A}. This is
  (4.156). ✓
- The second term of (4.149): see step 12. Dividing by d_0 and using MN = X gives XY(L^{4C+3A_0}e^{−cL^{0.1}}
  + L^{-A}) ≪ XYL^{-A-2}, after renaming A in (4.151). This is (4.157). ✓
- d_0 = 2^{ℓ_0} ≤ D ≤ exp(2KJL^{0.2}), so there are ≪_K L^{0.21} ≪ L values of d_0. This gives (4.148). ✓
- (G): exact Fractions, 300 cases each:
  - meas{r : ‖mr‖ ≤ ε} = 2ε, which is (4.28)'s step;
  - meas{r : −2r ∈ F} = meas F for random finite unions F.

**11. Prop. 4.5(ii) / (4.96) (pp. 45-46).** Proved here relative to (J2) and (J3); Computed (H).
- F_1 factorisation. ρ^{(ω_ℓ(z_0)+ω_ℓ(z_1))/2} = ∏_p(1 − H_{1,p}(ℓ_p)) with H_{1,p}(ℓ) = 1 − ρ^{(1_{ℓ=[z_0]_p}
  + 1_{ℓ=[z_1]_p})/2} ∈ [0, 1). ✓
- Its average is ≤ 2/(p+1): it is nonzero for at most 2 lines and ≤ 1. ✓ (The exact value is 2(1−√ρ)/(p+1) or
  (1−ρ)/(p+1).)
- Truncation. Bonferroni gives |∏(1−H) − Σ_{k<B}(−1)^k e_k(H)| ≤ e_B(H). Its ℓ-average is ≤ (Σ_p 2/(p+1))^B/B!
  ≤ (2ΣV_i)^B/B! ≪ exp(−cL^{3/4}) for B = ⌈L^{3/4}⌉. ✓ (H checks the identity, the average and Bonferroni.)
  The P-side truncation (E_B(ℓ(P)) via (4.110)) is "as in (i)" (J2).
- Moduli. S = abDq_1⋯q_k is odd and squarefree, and log S ≤ (K(J+2) + B)·2L^{0.2} ≪ L^{0.95} ≤ L^{0.98}, as
  (4.84) requires. ✓
- Coordinates of z_1 = (h, k). ψ_1(t′/Y) ≠ 0 ⟹ |k| = D|t′| < 8YD < 16d_0Y. g̃z_1 ∈ Ω′ ⟹ 1/16 ≤ h − 2rk ≤ 16, so
  |h| ≤ 16 + 2|k|. Hence |h|, |k| ≪ d_0Y. ✓
- Error count. The number of (z_1, p, p′) is ≤ (O(d_0Y))²∏|P_i|^{J+2} = exp(O_K(L^{0.21})). The remaining factor
  has size ≤ ∏V^{-(J+2)}ρ^{-K(J+1)} = exp(O_{K,ρ}(L^{0.01})) by (J3). Against exp(−cL^{3/4}) this closes. ✓
- B_0: g̃z_0 ∈ Ω′ is automatic, since g̃z_0 = TP. g̃z_1 ∈ Ω′ is the (4.105)-(4.106) situation with |k| ≪ d_0Y. The
  box count is (J2).
- B_1 (restriction at (g̃z_0, p)). r_{g̃z_0} ≡ −2r, so the boundary equations are a(−2r) = n ± ϑ. These are of the
  (4.108) type with τ(z_0) = 1, so #R and the box count are as in (i). ✓ (relative to J2)
- Normalisation. Summing F_1 over ℓ with weight ∏(p+1)^{-1} matches the density 1/(3ζ(2)∏_{p|S}(p+1)) of (4.88)
  for any function of (ℓ_p)_{p|S}. ✓
- Not re-derived: the grouping of configurations and the application of (4.110) term by term. Both are "as in (i)",
  covered by (J2).
- The variant "fails at (g̃z_1, p′)" is not used by Section 4.8 (step 12) and was not checked.

**12. The second term ⟨Gf, K(1−G)f⟩ (p. 61).** Proved here; Computed (F), (G).
- LWW "take (Q, p′) as the initial pair in (4.96)". This is the edge reversal of p. 20: (P, p) → (Q, p′) is an edge
  iff (Q, p′) → (P, p) is one, with (D, a, b) ↦ (D, b, a). The conditions d_0 ≤ D < 2d_0 and the weights σ, ∏V^{-1}
  are symmetric.
- In Q-centred coordinates (TQ = g′_Q z_0, TP = g′_Q z_1), t′ ↦ −t′ and a ↔ b, so W(t′−b+a) ↦ W(−(t′−b+a)).
  - Both choices of W in (4.94) are even: the indicator trivially, and |∫_{M_1} e(−θw)| = |∫_{M_1} e(θw)|.
  - η(a/Y)η(b/Y) and the ρ-power are symmetric.
  - ψ_1(t′/Y) becomes ψ_1(−t′/Y). See T5.
- The "bad" restriction is now at the initial pair (Q, p′), where r_{g̃z_0} ≡ −2r_Q. So E(p′) is a set of r
  depending only on p′, (4.31) applies, and steps 6-10 go through verbatim. ✓
- Why the re-centring is needed. Keeping P as the base point would put the restriction at (g̃z_1, p′).
  r_{g̃z_1} = τ(w)/τ(z_1) is a Möbius function of r. The bad set {r : r_{g̃z_1} ∈ F} depends on z_1 and is not of
  measure ≍ meas F.
- (G) NEG, z_1 = (16, 1): for an interval F of measure 0.0089, meas{r : r_{g̃z_1}(r) ∈ F} = 1.0. So the (4.154)-type
  "sup_p ∫_{E}" bound would fail. LWW's choice avoids this.

**13. (4.31) (pp. 21-22).** Proved here; Computed (G) for (4.28)'s step.
- (4.28): there are ≤ (J+1)^K values of D̃ and ≤ Y^{0.2} values of ℓ, each with measure 2Y^{-0.7}. Total
  ≤ 2(J+1)^K Y^{-1/2}. ✓
- (4.29): #{D̃Z_I} ≤ (J+1)^K∏_{i∈I∖{i*}}|P_i| ≤ exp(O(log L) + 2Σ_{i<i*}L^{a_i}) = exp(o(L^{a_{i*}})). This uses
  the increasing order a_1 < ... < a_K (p. 7), since i* is the largest index of I. ✓
- ∫F_I ≤ 200e^{−L^{a_{i*}}}·#{D̃Z_I}². The weights Σ∏_{i∉I}(q_iV_i)^{-1} = 1, and each pair has a nonzero integer
  multiplier m with meas{‖mr‖ < δ} = 2δ. ✓
- (4.30), Markov: meas{F_I > e^{−L^a/4}} ≤ e^{L^a/4}·e^{−L^a+o(L^a)} ≤ e^{−L^a/2}. ✓
- (4.31): Y ≥ a/4 ≥ e^{KL^{0.1}}/4, so the total is ≤ 2(J+1)^K Y^{-1/2} + (2^K−1)e^{−L^{0.1}/2} ≪_K e^{−cL^{0.1}}
  with any c < 1/2. The bound is uniform in p and d_0. ✓

## Terse places / slips / reading notes in LWW (none affects the result)
- **T1 (p. 58).** S(1−G_{-2})f = (1−G_{-2})f needs G_{-2} to be permutation-invariant. This is proved on p. 22 for
  G_1 only; the same argument works for G_{-2}.
- **T2 (p. 58, (4.150)).** The change of variables Q ↔ z′ and the identification "r_P → −2r" = "bad at (g̃z_0, p)"
  (r_{g̃z_0} ≡ −2r) are left as "by calculation". Filled in at step 4.
- **T3 (p. 59, (4.152)).** Interchanging Σ_ℓ with Σ^* uses that every non-ℓ restriction and coefficient is
  independent of ℓ. This is implicit.
- **T4 (p. 60, (4.154)).** Pulling the prime weights out as sup_{p,p′} of an integral over E(p) requires that E(p)
  depends on p only (not on z′). This is true for the first term, and it is the reason the second term is
  re-centred (T5).
- **T5 (p. 61).** "Take (Q, p′) as the initial pair" silently uses three things:
  - the edge reversal of p. 20;
  - the evenness of both W;
  - ψ_1(−·) in place of ψ_1(·). The paper never says ψ_1 is even, but the proof of (ii) does not use its shape,
    only 0 ≤ ψ_1 ≤ 1_{|u|<8}.
  
  Filled in at step 12.
- **T6 (p. 60).** "Since t ∈ 2Z" comes from D | z′_2 (or from Q ∈ C). The (4.76) substitution genuinely needs it
  (NEG (F)).
- **T7 (p. 46).** Prop. 4.5(ii)'s proof leaves the B_0/B_1 box count, the grouping and the P-side truncation to
  "as in (i)". The analogy holds for the pieces checked in step 11.
- **T8 (p. 61).** "O_K(L) values of d_0": in fact ≪_K L^{0.21}.
- **N1 (pp. 37, 46, reading note).** (4.94) has W(w) = |∫_{M_1} e(θw)dθ| and Φ has |η η ψ_1|. pdftotext drops the
  bars. Read without them, p. 46's "0 ≤ W ≤ 1" would be false ((F): negative for 248/484 values of w), and (4.150)
  would not be an inequality.
- **S1 (p. 58).** "to the these two terms". **(p. 60)** "r_P placed by −2r". Both are typos.
- **S2 (p. 58, (4.151)).** It states O_A(L^{-A}) where (4.96) gives O(exp(−cL^{3/4})). The L^{4C} of (4.150) and the
  L^{-A} of (4.154) are absorbed by renaming A. Harmless.
- **S3 (p. 59).** p′ denotes both a prime and the tuple (p′_1, ..., p′_K). Harmless.

## Computation (Computed)
- `code/parity/lww_s48_check.py`; output in `code/parity/lww_s48_check.out`.
- Run: `/usr/bin/python3 -I code/parity/lww_s48_check.py`. Pure Python. Wall time 3.5 s.
- Results: 23 positive checks, 0 failing. 10 negative controls, all failing as they must. 0 unexpected outcomes.
- Weight of the evidence:
  - The substantive computations are (B) (a brute-force line average against (4.153), with an exact equality at
    ρ = 1), (D), (F)'s (4.76) and (G)'s Möbius NEG.
  - (A), (C) and (H) are algebraic sanity checks.
  - (E)'s "≤ 15" is a tightness control, not a misreading.
- Limits:
  - The toys are tiny (K = 1 in (B), and primes ≤ 200).
  - Nothing analytic is tested: not (4.88), not (4.96) as an asymptotic, not the sizes in (4.31).
  - There is no end-to-end toy of ⟨(1−G)f, Kf⟩ against (4.156).

## What this does NOT show
- It does not re-check (J2): the Prop. 4.5(i) machinery and the Lemma A.1 card are used as they stand. Prop. 4.5(ii)
  is only as good as they are, and the steps of (ii) marked "as in (i)" were not re-derived independently.
- It does not check the "(g̃z_1, p′)" variant of (4.96), which Section 4.8 does not use.
- It does not check Prop. 4.2 as a whole, pp. 15-16, Section 5 or Theorem 1. LWW remains Claimed and unrefereed.
- Twin primes (K = 0) are untouched. Nothing here bears on the twin prime conjecture.

## Role in the chain
- Discharged, conditional on (J1) ⇐ (J2) and on (J3)-(J5): the second sum of (4.52), Σ_{d_0}|⟨f, T_{-2}^C f⟩ −
  ⟨f, A_{-2}^C f⟩|/d_0 ≪ XYL^{-A} ((4.148)).
- Combined with the earlier cards, each part of Section 4 from (4.7) to (4.157) appears to have been the subject of a card (judged from the card list, not re-audited). These are: the
  p23-27 card ((4.52), given (I1) and (I2)); the Prop. 4.3, 4.4 and 4.5(i) cards; the Lemma A.1 card; and the
  pp. 47-53, p. 54 and pp. 55-58 cards (the first sum, Prop. 4.6). Their conditions are as stated in each card and were not re-audited
  here. Remaining inputs named in those cards: (I1) = (4.9) via Shiu (not read in source); (A.2) Weil/Estermann
  (Literature).
- **First unresolved implication:** pp. 15-16, (4.1)-(4.8). This is the passage from the sum in Prop. 4.2 to Q_Y,
  including the removal of (a, h) = 1 and the Cauchy-Schwarz step (4.6). It has had no line-by-line correctness card (the
  prop53-twist and mu-vs-lambda cards read it for other questions); the p23-27 card lists it as open. After it come (I1) via Shiu 1980, then Section 5 (Q_Y^maj, Prop. 3.1, Theorem 1).
