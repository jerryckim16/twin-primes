# Audit: route card 2026-11-27-lww-s48-second-sum.md (LWW Section 4.8, (4.148)-(4.157), pp. 58-61; (4.31); Prop. 4.5(ii))

Fresh-context adversarial audit, 2026-11-27. No repository file was edited; this file is new. Nothing was committed.

## Verdict
- **The mathematics of Section 4.8 stands.** I re-derived the following from the printed text, independently of the
  card, and found no error in LWW:
  - p. 58: Sf = f, (4.149), and both S-removals;
  - the change of variables behind (4.150): TP = g′z_0, TQ = g′z′, t′ = −t/2, ψ_{-2}(t/Y) = ψ_1(t′/Y), and
    r_{g̃z_0} ≡ w_1 − 2r ≡ −2r for w = (w_1, 1);
  - the triangle inequality into Φ_W, with weights σ∏V_i^{-1} = ∏V_i^{-(J+2)} and d_0/D;
  - (4.152)-(4.153), the p. 60 prime sum, and (4.154) with sup over (p, p′) outside the triple integral;
  - (4.155) via (4.124) at z = z_0, w = (0, 1): h + rDt ∈ [1/16, 16];
  - the two z′-bounds, the measure step, and (4.156)-(4.157);
  - the Q-centred treatment of the second term (edge reversal, both W even, ψ_1(−·));
  - (4.28)-(4.31);
  - the new parts of the proof of (ii) on p. 46: the F_1 factorisation, the H_{1,p} average, log S, |h|, |k| ≪ d_0Y,
    the error count, and the B_1 boundary equations a(−2r) = n ± ϑ.
- Every formula the card quotes matches the rendered pages. This includes:
  - the |·| in (4.94);
  - |ηηψ_1| in Φ (p. 37), on p. 46 and in (4.152);
  - |ψ_1| in (4.154) and |ψ_{-2}| on p. 60;
  - the bar in |\overline{f(P)}f(Q)| ≤ L^{4C};
  - sup over p and p′_1, ..., p′_K in (4.154).

  Reading note N1 is correct. Without the bars, ∫_{M_1} e(θw)dθ < 0 for 49-61% of w in five toy (L^{A_0}, Y),
  including (10, 10^6).
- **The problems are in the card.** The most important: the card's explanation of *why* the second term must be
  re-centred is false as stated, and the script's (G) Möbius NEG, which the card lists as substantive evidence, has an
  arbitrary threshold (finding 1).
- Counts: **0 errors in LWW. In the card and script: 1 error (non-load-bearing), 2 gaps, 1 overstatement, 4 slips**
  (8 findings).

## Source and reproduction
- PDF: curl into a new empty directory /tmp/claude-0/lww-audit-s48/.
  - SHA-256 `7ac341311b4a648c32c2b23b3029e1f4a3202258b55614a33ba7e8282423d000` (matches).
  - I ran pdftotext -layout on pp. 7, 15-23, 32-46 and 58-61.
  - I rendered pp. 21, 22, 37, 46, 58, 59, 60 and 61 (110-130 dpi) and read the images.
- `/usr/bin/python3 -I code/parity/lww_s48_check.py`: the output is byte-identical to `lww_s48_check.out`, including
  the wall time of 3.5 s. All quoted counts match:
  - 23 POS / 10 NEG;
  - 2,304 lines, 360 triples, 90 with D | det;
  - 248/484, 240/240, 4000/4000, 514/2400, 30/30;
  - max seen 15 and 16, and meas 1.00000.
- Mutations were run on copies in the scratchpad (.../scratchpad/mut48/); none touched the repository:

  | # | Mutation | Result |
  |---|---|---|
  | M1 | (G) NEG threshold 2·meas F → 128·514·meas F (a valid bound, see finding 1) | NEG no longer fails: 0/1, UNEXPECTED |
  | M2 | (E) sign error in (4.155): h − rDt for h + rDt | caught, 19901/20000 |
  | M3a | (C) exponent J+2 → J+1 | passes (weaker bound; harmless, but (C) cannot see it) |
  | M3b | (C) exponent J+2 → J+3 | caught, 6/6 |
  | M4 | (B) ρ-exponent shifted by −1 (normalisation off by ρ^{-1}) | caught, 90/360 (the ρ = 2 NEG then stops failing) |
  | M5 | (B) K(J+1) → KJ in the ρ-exponent | passes (weaker direction; harmless) |

## Findings

**1. Error, in the card and not in LWW; non-load-bearing (card step 12, "Why the re-centring is needed"; (G) NEG;
"Weight of the evidence").**
- The card says r_{g̃z_1} = τ(w)/τ(z_1) "is a Möbius function of r. The bad set {r : r_{g̃z_1} ∈ F} depends on z_1 and
  is not of measure ≍ meas F", and that "the (4.154)-type sup_p ∫_E bound would fail".
- The size claim is false on the region that matters. Because (z_1, p′) ∈ S_ℓ requires g̃z_1 ∈ Ω′, only r with
  τ(z_1) ∈ [1/16, 16] occur.
  - There φ(r) := τ(w)/τ(z_1) is monotone, with |φ′| = 2/τ(z_1)² ∈ [1/128, 512].
  - So meas{r : τ(z_1) ∈ [1/16, 16], φ(r) ∈ F + Z} ≤ 128·(512 + 2)·meas F for every measurable F ⊂ T.
  - The pull-back is therefore ≪ meas F, with an absolute constant.
- The script's example is consistent with this. For z_1 = (16, 1), τ ∈ (14, 16], and the ratio 1/0.00893 ≈ 112 is
  below 128. The NEG "fails" only because its threshold, 2·meas F, is arbitrary. With the valid constant (M1) the NEG
  no longer fails.
- The real obstruction is that the bad set depends on z_1 (equivalently on h, for fixed t). For fixed (p, p′, t), the
  admissible h move with r. Each h is admissible only on an r-interval of length ≤ 16/(D|t|), and there are ≍ D|t| + 16
  of them. Bounding each h separately loses a factor up to ≍ d_0Y = exp(O(L^{0.2})), which exp(−cL^{0.1}) cannot pay
  for. LWW's re-centring makes the restriction depend on r alone, so sup_{p′} meas E(p′) can be pulled out.
- **Fix:** replace the step-12 paragraph by the z_1-dependence explanation. Relabel the (G) NEG as an illustration
  that the pull-back is not *the same* set as F, not as evidence that it is large. Remove "(G)'s Möbius NEG" from the
  substantive list. Note also that LWW state, and the card leaves unchecked, the (g̃z_1, p′) variant of (4.96). The
  card cannot claim that the other route is impossible, only that the (4.154) argument does not carry over verbatim.

**2. Gap (card "Inputs"; the classification bullets).** The inputs are incompletely listed. The derivation uses, but
the card does not list:
- (4.76) (p. 32), in steps 4 and 9. (F) checks it numerically, but it is not re-derived.
- The bijection Q ↦ TQ from Ω ∩ C onto the primitive vectors of Ω′ with odd first coordinate (proof of Prop. 4.4,
  p. 32), together with (4.81). Step 4's Q ↔ z′ bijection needs both.
- 0 ≤ η ≤ 1 and supp η ⊂ [1, 4] (pp. 16-17). (4.154) silently drops (d_0/D)|η(a/Y)η(b/Y)| ≤ 1, and step 13 uses
  Y ≥ a/4.
- log d_0 ≤ 2KJL^{0.2} and log Y ≤ 2KL^{0.2} (p. 40, from (4.17) and supp η). Step 11's error count
  "(O(d_0Y))² ... = exp(O_K(L^{0.21}))" needs these.
- (2.12): the P_i are pairwise disjoint (step 7), |P_i| ≤ exp(2L^{a_i}), and a_1 < ... < a_K (p. 7). These are cited
  in the classification only. J = ⌊L^{0.01}⌋ is also used.

**Fix:** add these as definitional inputs (pages as above).

**3. Gap (card header "Prop. 4.5(ii) ... inherits that card's input U1"; (J2); "Uniformity").**
- The Prop. 4.5(i) card (2026-11-26-lww-p37-47-prop45.md) is conditional on U1-U7, not on U1 alone.
  - U2-U7 are definitional or elementary.
  - U7 (the c_δ of (4.88) is a fixed positive constant depending on δ) is a real dependence.
  - The Prop. 4.5(i) card also carries a Session-59 correction note on U2.
- The card's uniformity bullet lists the constants as depending on K, ρ, C, A (through A_0) and c of (4.31). It omits
  δ, which enters through (4.88) and the threshold "x large".
- **Fix:** write "(4.96) inherits U1-U7 of that card (U1 = Lemma A.1 the substantive one)", and add δ to the
  dependence list.

**4. Overstatement (card "Computation / Weight of the evidence"; step 12 "Computed (F), (G)"; (H)).**
- Beyond finding 1:
  - Step 12's "Computed (F), (G)" tests only |W(−w)| = |W(w)| and the (flawed) Möbius illustration. Nothing in the
    script tests the re-centring identity itself (that the Q-centred expansion of ⟨Gf, T(1−G)f⟩ is a Φ-type sum with
    W(−·), ψ_1(−·) and a ↔ b).
  - The (H) NEG "avg H_{1,p} ≤ 1/(p+1)" fails (514/2400) only at ρ = 0.05: the exact average 2(1−√ρ)/(p+1) exceeds
    1/(p+1) iff ρ < 1/4. So it is a ρ-dependent sensitivity check, not a misreading control.
  - (C) cannot distinguish V^{J+1} from V^{J+2} (M3a). This is harmless, but "exact" overstates what it pins down.
- Of the ten NEGs, two are tightness or sensitivity checks ((E) "≤ 15", (H)). The (G) NEG is finding 1.
- **Fix:** say that steps 4, 6-7 and 9 rest on (B), (D), (E) and (F), and that step 12 is argument only. Describe the
  (H) NEG as ρ-sensitivity.

**5. Slip (card Inputs, (J6)).** "(4.124) ... used only in the special case z = z_0, where it is elementary (step
8)". The use is in step 9. **Fix:** "(step 9)".

**6. Slip (card Source, "settled ... that (4.152)'s second line multiplies inside Σ^†").** The image of p. 59 shows the
second line beginning with "×" on a new line, with no bracket. The image does not settle the scope. Inside Σ^† is
forced because the factor depends on the summation variables z′, p, p′. **Fix:** "read as inside Σ^† (the factor
depends on z′, p, p′; no bracket is printed)".

**7. Slip (card "Terse places / slips", T8 and S2).** T8 ("O_K(L) values of d_0", in fact ≪_K L^{0.21}) and S2 (O_A(L^{-A})
where O(exp(−cL^{3/4})) is available) are true, weaker statements. They are neither terse places nor slips. The Prop.
4.3 audit (finding 11) made the same point. **Fix:** relabel both as remarks. That leaves T1-T7, N1, S1, S3 and two
remarks.

**8. Slip (card "Role in the chain").**
- "each part of Section 4 from (4.7) to (4.157) appears to have been the subject of a card" overlaps the "First
  unresolved implication: pp. 15-16, (4.1)-(4.8)": (4.7)-(4.8) are in both. The p23-27 card explicitly excludes
  (4.1)-(4.8); it starts from the definition (4.7) of Q_Y.
- The card does not cite 2026-11-25-lww-prop42-thinning.md items 9 and 12, which had already examined (4.26)-(4.31)
  and (4.149)-(4.157) for set-dependence. The Prop. 4.3 audit (finding 4) flagged the same pattern.
- **Fix:** "from (4.9) to (4.157), with Q_Y as defined in (4.7)". Add "partially examined (set-dependence only) in
  2026-11-25-lww-prop42-thinning.md, items 9, 12".

## What I checked and found correct (no finding)
- Steps 1-11 and 13 of the card are correct as written. In particular:
  - the ∏V^{-(J+2)} bookkeeping;
  - ω_ℓ ≥ K(J+1) under the restrictions;
  - the prime-by-prime factorisation of (4.153), using the pairwise coprimality of D, a, b;
  - z′ = (h, −Dt/2) with first coordinate u(h + rDt);
  - the count of at most 16 integers in an interval of length 15 + 15/16;
  - ≤ 16Y even t with |t| < 16Y, and meas M_{-2} = meas M_1 ≤ 4L^{3A_0}/Y;
  - meas{r : −2r ∈ F} = meas F;
  - the (4.31) chain: (J+1)^K Y^{0.2} values each of measure 2Y^{-0.7}; (4.29) via a_1 < ... < a_K; Markov;
    log Y ≥ KL^{0.1} − log 4; c < 1/2;
  - (4.157) and the ≪_K L^{0.21} count of d_0;
  - in (ii): the exact average 2(1−√ρ)/(p+1) or (1−ρ)/(p+1); Bonferroni plus independence over p giving
    e_B(h) ≤ (Σh)^B/B!; log S ≪ L^{0.95}; |k| < 16d_0Y and |h| ≤ 16 + 2|k|; the error count;
    r_{g̃z_0} ≡ −2r, so the B_1 boundary equations have τ(z_0) = 1.
- Step 12 is correct apart from its "why" paragraph (finding 1):
  - the edge reversal (D, a, b) ↦ (D, b, a), as on p. 20, with σ and 1_{d_0≤D<2d_0} symmetric;
  - t′ ↦ −t′ and W(t′−b+a) ↦ W(−(t′−b+a));
  - ψ_{-2}(t_{PQ}/Y) = ψ_1(−t′_Q/Y);
  - the restriction now at (g̃_Q z_0, p′).
- T1-T7, N1, S1 and S3 are accurate. Two details:
  - T1: p. 58 asserts S(1−G_{-2})f = (1−G_{-2})f without proof. The p. 22 argument for G_1 transfers.
  - T5: p. 17 never says ψ_1 is even. Only 0 ≤ ψ_1 ≤ 1 and supp ψ_1 ⊂ [−8, 8] are used in (ii) and (4.154).
- (J4) is fine as a consequence. Prop. 4.2 assumes |α_m| ≤ L^C R_Z(m)1_{M<m≤2M}, and f is built from the twisted
  α, β of (4.3), whose moduli are no larger. Citing (4.3) would be more exact.
- The script's descriptions match its code. The NEGs in (A), (B) (both), (D), (F) and (C) are genuine misreading
  controls. (B) is a true brute force against (4.153), and the (B), (C) and (E) checks catch the M2, M3b and M4
  mutations.
