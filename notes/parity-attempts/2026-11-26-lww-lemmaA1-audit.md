# Referee audit: route card 2026-11-26-lww-lemmaA1.md (LWW Lemma A.1 and (4.86)-(4.88))

Auditor: fresh-context adversarial referee, 2026-11-26.

## What I did
- Source: /tmp/claude-0/lww-a1-t6bn/lww.pdf. SHA-256 is 7ac341311b4a648c32c2b23b3029e1f4a3202258b55614a33ba7e8282423d000,
  as expected. 75 pages. The abs page lists v1 and v2 only.
- I read pp. 33-35 and pp. 72-74 myself with pdftotext -layout. I also checked the context the card relies on:
  - p. 17 (4.5): Y = 2^ℓ, Y <= a <= 4Y;
  - p. 18 (4.17)-(4.18): d_0 = 2^{ℓ_0}, Ω;
  - Prop. 4.2: M, N >= x^δ;
  - p. 43: the moduli S = S_0 q_1...q_k used in Prop. 4.5;
  - L = log x (2.1).
- I re-derived the lemma's steps independently:
  - #R_u, including the primes of S_2 where c_0 may be 0 mod q;
  - the CRT/orthogonality identity;
  - G | S_1 gcd(h,k,u);
  - the exponents in (A.3) and (A.4);
  - the smoothing;
  - the per-u count and the u-sum;
  - the swap;
  - the line criterion, the g_0 count and the S^4 bookkeeping.
- I read code/parity/lww_lemmaA1_check.py and its .out line by line.
- I also re-ran an independent Kloosterman-ratio scan over m <= 160 and m ∈ {256, 512, 768, 1024, 108, 216, 180}.
  The worst ratio is at the prime m = 139 (0.9972). For the 2-power and mixed moduli tested it is <= 0.32.

I found no mathematical error in LWW in these pages and no error in the card that changes its conclusion. All the
findings below are slips, small gaps and overstatements, mostly in how the card and script describe what was checked.

## Findings

1. **slip (card L3; LWW p. 73).** The card says "Modulo uS1, every c ≡ c0 (S1) is a unit". This is false as stated.
   - At a prime p | u with p ∤ S, nothing in "c ≡ c0 (mod S1)" makes c a unit; for example, c ≡ 0 (mod p) is allowed.
   - What makes c a unit there is the congruence cv ≡ ud0' - 1 ≡ -1 (mod p).
   - The identity is still right, because K_{uS1} sums over units only and those are exactly the c that occur in R_u.
   - Fix: "every c occurring in R_u is a unit mod uS1 (at p | S1 by c ≡ c0, at p | u, p ∤ S by cv ≡ -1); conversely
     every unit y ≡ c0 (S1) gives one point of R_u".

2. **overstatement (card header, "relative to one standard input").** The proof also uses other standard facts:
   - the divisor bound τ(m) ≪_ε m^ε, with ε = 1/200 and an absolute constant;
   - a smooth compactly supported probability density with |φ̂(ξ)| ≪_j (1+|ξ|)^{-j};
   - Σ μ(ℓ)/ℓ^2 = 1/ζ(2).

   These are textbook facts, but the claim of a single input is not literally true. Fix: "proved here relative to the
   Weil/Estermann bound (A.2) (Literature, not re-opened) and textbook facts (divisor bound, Schwartz bump)".

3. **overstatement (card L5, L6, L10: the "✓ (J)" marks; script section (J)).**
   - Section (J) only checks rational exponent arithmetic: 0.515, 0.555, -0.07, 0.99, ... It does not check any
     bound, smoothing or summation.
   - The "swap" item, F(7,3)·F(5,2)·1/(F(7,3)·F(5,2)) == 1, is a tautology that tests nothing.
   - Citing (J) next to "✓" in L5, L6 and L10 suggests more than this.
   - Fix: label (J) "exponent arithmetic only", and drop or replace the swap item.

4. **slip (card "Arithmetic" list; script (J)).** The card lists (J) under "exact integers and Fractions". But (J)'s
   last item, the (4.88) threshold check, uses math.log and math.exp in floating point. Fix: move it to the "floats"
   list, or redo it in exact form (for example with integer comparisons on L^{0.02}).

5. **slip (card L1, Computed (B)).** "(B): 3,357,742 (u, v, c, g0) cases, with S up to 15 and all u ≡ u0" is not
   what the script does.
   - It takes only the first three u >= 2 with u ≡ u0 (mod S), and u < 40.
   - It takes v <= 2uS.
   - For S = 15 it samples 60 g0 out of 2,880.

   Similarly, (A) samples 150 g0 for S ∈ {15, 30}, and the card's "all g0 for |SL2| <= 800" leaves that sampling
   unsaid. Fix: say "first three u in each class, v <= 2uS, g0 sampled when |SL2(Z/SZ)| > 300 (B) / > 800 (A)".

6. **gap (card L6, Computed (E)).** The (A.4) illustration never has S1 > 1.
   - The u used are 1009, 2003, 3001, 4097 = 17·241 and 4199 = 13·17·19, with S ∈ {1, 3, 15}.
   - So no u shares a prime with S, and the CRT/j-average part of (A.3) is never exercised in (E).
   - The card does not claim otherwise for (E). But the criteria emphasise "including u sharing primes with S", and
     the reader may assume (E) covers it.
   - Fix: add u ≡ 0 (mod 3) and u ≡ 0 (mod 15), for example u = 3003 and 4095, or state the limitation.

7. **slip (card L6).** "|f^±^(n)| <= |1̂_J(n)| |φ̂_Δ(n)|" should use the enlarged or contracted interval J^± (length
   |J| ± 4Δ), not J. Also, the construction is mollification of an indicator, not a "Beurling–Selberg-type"
   extremal minorant/majorant. Fix the formula and the name. The bound is unaffected.

8. **slip (card L7).** "(in fact N|I2|/(uS) + 1 pieces)". Splitting an interval of length ℓ at multiples of uS gives
   at most ℓ/(uS) + 2 pieces, and the count need not be an integer of the stated form. LWW's O(N/u + 1) is correct.
   Fix: "<= N|I2|/(uS) + 2 pieces".

9. **slip (card T4, L8).** "This is where I2 ⊆ [1,16] (rather than [0,16]) is used" is too narrow. Lower endpoints >= 1
   are also used in the following places:
   - I1 ⊆ [1,16] gives u >= U >= 2, which is needed for a Kloosterman modulus >= 2, for Δ <= 1/100, and for the
     error sum Σ_u u^{-0.01} ≪ U^{0.99};
   - in the swapped case, v >= N plays the same role.

   Fix: "one of the places where".

10. **gap (card L10, "U >= M >= x^δ (d0, Y >= 1)").** No source is given for Y >= 1. LWW define Y = 2^ℓ with ℓ ∈ Z
    (p. 17) and have Y <= a <= 4Y with a a product of K large primes. So Y >= a/4 is huge whenever the sum is non-empty,
    and in any case Y >= 1/4. Likewise d_0 = 2^{ℓ_0} >= 1 by (4.17). The conclusion holds even with U >= M/4. Fix: cite
    p. 17 (4.5) and (4.17), or write U ≫ M.

11. **slip (card L10, "previous card: log S ≪_K L^{0.95}").** LWW p. 43 prints log S ≪_K R(J+1)L^{0.2} + BL^{0.2} ≪_K
    L^{0.96}. The card quotes the previous card's L^{0.95} rather than the source. This is harmless, since both are
    <= L^{0.98}, but the citation should be to LWW p. 43, with the printed exponent 0.96.

12. **gap (card L10, uniformity statement).** "The implied constant is absolute. The threshold x_0 depends on δ and C"
    holds only for x >= x_0(δ, C), with x_0 = exp((800C/δ)^{50}).
    - For x < x_0 one needs the trivial bound: the LHS of (4.88) is O(1). So, read over all x, the O-constant
      depends on (δ, C).
    - In the application C = O_K(1), with K fixed by A, so this is fine.
    - The task also asked about summation against exp(O(L^{0.71})) configurations and x^{o(1)} moduli. The card
      asserts uniformity but does not spell out that the absolute constant, together with the fixed exponent
      cδ = δ/200, is what makes that summation legitimate. This was done in the previous card.
    - Fix: one sentence stating "O-constant absolute for x >= x_0(δ, C); hence summable against x^{o(1)} terms".

13. **slip (card L5).** "(A.2) ... the standard Weil (prime m) / Estermann (general m) form". Estermann treats prime
    powers; general m follows by twisted multiplicativity. More importantly, the claim is checked only numerically for
    m <= 160, where the 2-power moduli reach only 128. The card's Limits section says this, so this is only a wording
    issue. Fix: "Weil (p), Estermann (p^k), multiplicativity".

14. **slip (card intro / T1 framing).** "The argument closes as printed." This is accurate with T1 and T3 noted. One
    more terse place deserves a mention: LWW p. 35 asserts "≪ S^4 min^{-1/100} ≪ x^{-cδ} since M, N ≫ x^δ" without
    noting that S^4 = x^{O(L^{-0.02})} = x^{o(1)} is needed. The card supplies this in L10 but does not list it as a
    terse place. Suggested T5.

## Checked and found correct (no finding)
- **Lemma A.1, pp. 72-74.** I re-derived each step and found it correct:
  - #R_u;
  - the R_u ↔ matrix-congruence equivalence, including c = u being impossible for u >= 2;
  - the CRT phase 1/(uS) ≡ γ/(uS1) + γ''/S2;
  - the j-detection giving K_{uS1}(γh + ju, γk(ud0' - 1));
  - G | S1 gcd(h,k,u) and gcd(h,k,u) <= max(|h|,|k|), which covers h = 0 or k = 0;
  - (A.3) exponents 0.515 / 1.005;
  - the tail Δ^{-11}H^{-9} = O(u^{-0.07});
  - the per-u count, with error (NU^{0.99} + U^{1.99})S^2 and U <= N;
  - the u-sum, with (ℓ,S) = 1 giving one class mod ℓS for any u0, including u0 not coprime to S;
  - |SL2(Z/SZ)| = S^3 ∏(1 - p^{-2});
  - the swap: canonical complement, involution, the 1/(uv) <= 1/(UN) sandwich, and an O(1) main-term shift.
- **The Kloosterman bound.** It is applied at modulus uS1 >= 2, with gcd over all three entries and τ(uS1). The script
  computes K as Σ_y e((hy + k y^{-1})/m), the same normalisation as LWW.
- **(4.85)-(4.88), pp. 34-35.** These are also correct:
  - the line criterion;
  - 2S squarefree for odd squarefree S;
  - #g0 = 2∏p(p-1);
  - |SL2(Z/2S)| = 6∏p(p^2 - 1);
  - the constant 1/(3ζ(2)∏(p+1));
  - the error #g0 · (2S)^2 min^{-1/100} ≪ S^4 min^{-1/100} <= x^{-δ/200} for x >= x_0(δ, C).
- **Match with U1.** This matches U1 of the previous card: O(x^{-cδ}), uniform in odd squarefree S <= exp(O(L^{0.98})),
  in the lines and in the intervals, using M, N >= x^δ.
- **Script.** The (I) enumeration really runs over every line choice (42 combinations). The NEG controls do fail as
  reported.
- **Classification.** The "What this does NOT show" section is honest. It does not imply that LWW's theorem is verified.

## Counts
Error 0, gap 3 (6, 10, 12), overstatement 2 (2, 3), slip 9 (1, 4, 5, 7, 8, 9, 11, 13, 14).

**Verdict: the card stands. Lemma A.1 and (4.86)-(4.88) are proved relative to the Weil/Estermann bound (A.2) and
textbook facts, and U1 is discharged in that relative sense. No error was found in LWW on these pages. The fixes above
are wording and test-description corrections; none changes the conclusion.**
