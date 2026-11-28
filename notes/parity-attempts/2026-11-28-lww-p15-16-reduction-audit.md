# Audit: route card LWW pp. 15-16, (4.1)-(4.8) (2026-11-28)

Audited file: notes/parity-attempts/2026-11-28-lww-p15-16-reduction.md (the card was not edited).
Auditor: fresh-context adversarial agent. Sources I used:
- arXiv:2610.20242v2 at /tmp/claude-0/lww/lww.pdf. I checked SHA-256 `7ac34131…2d423000` myself.
- I re-extracted pp. 5-8, 14-18 and 62-63, 69-70 with pdftotext.
- I rendered pp. 15-16 with pdftoppm at 150 dpi. I also rendered the (4.4) display at 400 dpi and read it visually.
- I re-ran the script code/parity/lww_p15_16_check.py with /usr/bin/python3 -I. Its output matches the committed
  .out apart from wall time: 32 POS ok, 12 NEG failing as they must, 0 unexpected, 16.8 s.
- I ran four one-line mutations of the script on scratch copies (see Script below).

## Verdict
The mathematics of R0-R9 holds. I re-derived each step:
- the smoothing error;
- the Mellin bounds with Stirling numbers;
- the ordering of the Mellin truncation against the dyadic split;
- the W-expansion;
- the (a, h) > 1 residue count;
- η and (4.5);
- the Cauchy-Schwarz constant;
- the conjugates in (4.7);
- the assembly of (4.8).

I found no error in LWW's mathematics. The card's main defect is a **misreading of the source at (4.4)**. Because of
it, the card describes a slip LWW did not make (S1) and misses the slip LWW did make. There is also one understated
use of (I2). The rest are small slips in how the script's evidence is described.

## Findings

**1. Error (card's reading of the source; no mathematical consequence).**
- The card says, under Source: "(4.4): the second line is "T_3(F) ≤ Σ∫|ψ̂(v)||T(M,N)|dv + …", with bars on T(M,N) and
  none on T_3(F);".
- R3 says: "The second line is printed "T_3(F) ≤ …" (S1). It is valid as printed, since T_3(F) is real".
- S1 says: "the left side of the second line is T_3(F), not |T_3(F)|. It is harmless, since T_3 is real".
- What the PDF actually shows (p. 15, rendered at 400 dpi): `⩽ Σ_{M,N} ∫_{|v|⩽L^{2B}} |ψ̂(v)| T(M, N) dv + O_{K,ρ}(xL^{2−B})`.
  There are **no** bars on T(M, N). The only bars are those around ψ̂(v).
- T(M, N) is complex, because α_m and β_n carry m^{iv} and n^{iv}. So the printed second line is not a meaningful
  inequality. "Valid as printed" is false.
- LWW's real slip is the missing |·| on T(M, N). |T_3(F)| on the left is needed only for (4.8). (4.8) does print
  |T_3(F)|, and its right side does have |T_Y|.
- This does not change the conclusion. The correct statement |T_3(F)| ≤ Σ∫|ψ̂||T(M,N)| + O(xL^{2−B}) follows from the
  first line by the triangle inequality, which is what R9 actually uses.
- **Fix:**
  - Source bullet: "(4.4): the second line is printed "T_3(F) ≤ Σ∫|ψ̂(v)| T(M,N) dv + …". There are bars only on ψ̂(v),
    none on T(M,N) and none on T_3(F)."
  - Rewrite S1: "(4.4), second line: T(M, N) lacks absolute-value bars. T(M, N) is complex (m^{iv}, n^{iv}), so the
    line is meaningless as printed. Intended: |T_3(F)| ≤ Σ∫|ψ̂(v)||T(M,N)|dv + O(xL^{2−B}), which follows from the
    first line by the triangle inequality. Harmless."
  - In R3, delete "It is valid as printed, since T_3(F) is real".
  - The claim "pp. 15-16 were rendered … This settled: (4.4) …" should be corrected, not just reworded. The visual
    check was claimed and was wrong.

**2. Overstatement (scope of (I2)).**
- Card text: "Only V_i ≫ 1, that is ∏V_i^{-1} ≪_K 1, is used" (header), and "Only V_i ≫ 1 is used, in R5" (Inputs).
- The card also uses ‖W‖_∞ ≪_{K,ρ} 1, in R1, R3 and R9. It lists this under "Definitions used (… nothing to check)",
  citing p. 7.
- LWW's p. 7 bound 0 ≤ W ≤ ((2/log 2) sup_j jρ^{j−1})^K uses V_i ≥ (log 2)/2. That is (I2) again.
- So (I2) enters the smoothing and Mellin errors too, not only R5. The logical status does not change: the card is
  still conditional on (I2) alone. But the claim about where (I2) is used is wrong.
- **Fix:**
  - Header: "Only V_i ≫ 1 is used: in R5 (∏V_i^{-1}), and in R1/R3 through ‖W‖_∞ ≪_{K,ρ} 1 (p. 7)."
  - Move "0 ≤ W ≪_{K,ρ} 1" out of "nothing to check" and mark it "(uses I2)".
- Optional: V_i ≫ 1 needs only Chebyshev-strength bounds (π(2y) − π(y) ≫ y/log y), not Mertens.

**3. Slip (description of NEG (E)).**
- Card: "(E) (4.6) … NEG: the same inequality without the factor X/Y fails."
- The script's NEG is not "the same inequality" with a factor removed. It switches to α = β = 1 and c_h = 1
  (lines building `Spos`, `tp`, `qp`), which is a different instance. The script's docstring and label say this
  correctly. The card's summary does not.
- **Fix:** "NEG: with α = β = 1 and c_h = 1, the inequality without the factor X/Y fails."

**4. Slip (description of the |D| check).**
- Card: "|D| is ≤ the R5 bound. This is a loose sanity check."
- The script does not evaluate R5's bound ∏V_i^{-1}(L+2)(2L^{0.9})^{K−1}Σ_p(2X/p² + 2M). Instead it uses:
  - the actual counts #{(m,n): p² | mn+2};
  - the maximum of ω_j over the box;
  - max|α| · max|β|.
- So it is the intermediate union bound before the residue-count step, and it has 18× to 2700× slack. Like the
  "every (a,h) > 1 term has p_i² | mn+2" check, it holds by construction and cannot fail informatively.
- **Fix:** "|D| ≤ the R5 union bound with actual residue counts (before the N/p² + 1 step), and with slack 18-2700×.
  This is not a test of R5's size estimate." Also mark the p_i² check as true by construction.

## Points checked and found correct (no finding)
- **R1.** The convolution ψ = 1_{[1,2]} * φ_ε satisfies all of LWW's requirements. The error is ≪ L(xL^{1−B} + x^{1/2}),
  and the divisor bound is correct.
- **R2.** The Fourier normalisation matches ψ̂(v) = (2π)^{-1}∫ψ(u)u^{-iv}du/u and gives x^{-iv} in (4.4). The formula
  g^{(j)} = ΣS(j,i)e^{is}ψ^{(i)}(e^s) holds, with ‖g^{(j)}‖_1 ≪ L^{B(j−1)}. The tail ∫_{|v|>L^{2B}} ≪ L^{-B}
  (using j = 2). The bulk is ≪ 1 + 2B log L, since ‖g'‖_1 = 2.
- **R3.**
  - The box range MN ∈ [(1−ε)x/4, (2+ε)x) holds, with ≤ 4 values of k per j and ≪ L boxes.
  - The ordering point (T1) is real and correctly resolved, with total weight ≪ xL².
  - Prop. 4.2's hypotheses (p. 18: 0 < δ < 1/5, M, N ≥ x^δ, X = MN ≍ x, |α_m| ≤ L^C R_Z(m)1, |β_n| ≤ L^C R_Z(n)1) hold
    for every |v| ≤ L^{2B}.
  - Prop. 5.3's hypotheses (p. 63: α_m = µ(m)R_Z(m) times m^{iv}, |v| ≤ x^{C_0}) hold.
  - Uniformity of the conclusions in v follows because both statements depend only on the size bounds. The card
    defers this to the p23-27 card, which states it. The Y-range that Prop. 4.2's proof needs (16Y < Z) follows from
    R6's a ≤ exp(2ΣL^{a_i}) and is recorded in the p23-27 card.
- **R4.** The expansion is exact, and the injectivity of tuple ↦ a holds.
- **R5.**
  - (a, h) > 1 ⟹ p_i² | mn+2.
  - The tuple count is ≤ (2L^{0.9})^{K−1}.
  - p ∤ m is forced, since p is odd. For p ∤ m, n lies in one class mod p², giving ≤ N/p² + 1 values.
  - Σ_{p>e^{L^{0.1}}} p^{-2} ≤ 2e^{−L^{0.1}}.
  - #primes · M ≤ X x^{−1/5+o(1)} (needs N ≥ x^{1/5}).
  - Result: |D| ≪_K XL^{0.9K+1}e^{−L^{0.1}} ≪ XL e^{−L^{1/20}}.
  - LWW's O_{K,ρ}(XL exp(−L^{1/20})) is correct, and the "dropped terms are nonzero" remark is right (µ(h) ≠ 0 is
    possible; the toy has 19·43 + 2 = 273·3).
- **R6.** η = χ(t) − χ(t/2) is real, lies in [0, 1], has support in [1, 4], and telescopes. The number of Y is
  ≪ KL^{1/5}.
- **R7.** |T_Y|² ≤ ⌊(4X+2)/Y⌋Q_Y ≤ 6(X/Y)Q_Y, and the normalisations ∏V^{-1} and ∏V^{-2} agree.
- **R8.** The conjugates in (4.7) are confirmed in the render: α_m\overline{α_r}β_n\overline{β_s}.
- **R9 and the claim "every discarded term is ≪ xL^{-A} once B ≥ A+2".** This is correct.
  - The smoothing and Mellin errors are O_{K,ρ}(xL^{2−B}).
  - The D-part is ≪ L · B log L · xL e^{−L^{1/20}}.
  - B = B(A) then feeds into the ∫|ψ̂| ≪ B log L of (5.32). This is harmless and is noted in T3.
- **Terse places T1-T5** are all genuine.
- **Slips.**
  - S2 is real: X is first defined in Prop. 4.2, p. 18.
  - S3 is real.
  - S4 is real but incomplete: the top-of-p. 16 display and (4.5) both have no subscript at all, while the sentence
    before them has O_{K,ρ}.
  - S5 is real.
  - S1 is wrong (Finding 1).
- **Vaughan sign (R0).** T_1 − T_2 + T_3, as in (2.4), and c_V(r) = Σ_{ℓ|r, ℓ>V}Λ(ℓ). Both are correct.

## Script
- The script reproduces the card's numbers exactly: 247/65/11 for (A) NEG, and |D|² = 70.2, 80.1, 181.
- **Mutation tests (mine).** Each was one line, run on a scratch copy.
  - ρ^{ω(h)} → ρ^{ω(h)+1} in the expansion: caught by (B) and (C) in all 3 toys.
  - H_Y = ⌊(4X+2)/Y⌋ → ⌊X/(4Y)⌋: caught by (E) in 2 toys. So (E) is not vacuous.
  - Sign (−1)^K → 1: caught for K = 1 and K = 3 (K = 2 is blind, as expected).
  - Coprimality test weakened to "(a,h) = 1 or 2 | h": caught by (B) and (C) for K = 1 only. The K = 2 and K = 3
    toys have just 3 bad terms each.
- The core checks (A), (B), (C), (D) and (E) are discriminating.
- Some checks are tautological or nearly so: "(a,h) > 1 ⟹ p_i² | mn+2", "unique box per pair" in (F), and the
  |D| bound (Finding 4).
- The NEGs are meaningful:
  - (A) and (D) test the actual identity against its mutilated form.
  - (B) NEG is exactly "D ≠ 0".
  - (E) NEG is a different instance (Finding 3).
- As the card says, nothing analytic is tested: not (4.2), not the size estimate in R5, not (I2).

## Tally
- Error: 1 (Finding 1). It is in the card's reading of (4.4), not in LWW, and has no mathematical consequence.
- Gap: 0.
- Overstatement: 1 (Finding 2).
- Slip: 2 (Findings 3 and 4).

Errors found in LWW: 0. LWW's (4.4) second line has a real typographical slip (the missing |T(M,N)|). The card
misreports it.
