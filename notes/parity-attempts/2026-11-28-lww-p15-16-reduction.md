# Route card: LWW pp. 15-16, (4.1)-(4.8): Type II sum → Q_Y (2026-11-28)

**Classification: proved here relative to LWW's definitions, conditional on one standard input (I2, Mertens).**
- Every step from (4.1) to (4.8) was re-derived. Each error term was bounded explicitly, with its dependencies tracked.
- **No error in LWW found.** There are five terse places (T1-T5) and five slips or typos (S1-S5). None changes the
  conclusion.
- **Input not proved here:** (I2) V_i = log 2 + o(1) (Mertens; stated by LWW on p. 7). Only V_i ≫ 1, that is
  ∏V_i^{-1} ≪_K 1, is used. This is the same (I2) as in the 2026-11-27 p23-27 card. Everything else is proved here
  from first principles, including the two things LWW import: the smooth ψ (from their [2, p. 242], **not read**) and
  the short-interval divisor bound.
- **What the steps give**, uniformly in v (|v| ≤ L^{2B}), in the dyadic boxes (M, N ≥ x^{1/5}, MN ≍ x) and in Y:
  |T_3(F)| ≪ Σ_{M,N} ∫_{|v|≤L^{2B}} |ψ̂(v)| Σ_Y ((MN/Y)Q_Y)^{1/2} dv + x L^{-A}.
  The constants depend only on K, ρ (through ‖W‖_∞) and B, and they need B ≥ A + 2 (T3). Each (α, β) that occurs
  satisfies Prop. 4.2's hypotheses (with any C ≥ 2) and Prop. 5.3's hypotheses.
- Role: this card closes the "pp. 15-16" gap listed in the Session 61 README entries. With it, Section 4 from (4.1) to
  (4.157) has a card. The Prop. 4.2 chain still rests on (I1) (the divisor bound (4.9), Shiu) and on the inputs of the
  downstream cards.
- This is not a check of Prop. 4.2, Section 5 or Theorem 1. Twins (K = 0) are untouched. Nothing here bears on the
  twin prime conjecture.

## Criteria
These were written after the first read of pp. 15-16 and before the script.
- **Success:**
  - each of (4.1)-(4.8) is re-derived from LWW's definitions;
  - every discarded quantity (the smoothing error, the Mellin tail, the (a, h) > 1 terms) is bounded, after the
    v-integral and the M, N, Y sums, by ≪ xL^{-A} for each A, given a choice of B;
  - the bounds are uniform in the parameters that (5.32) sums over;
  - the exact toy identities hold, and the negative controls fail.
- **No-go** (would count as an error in LWW): any of
  - a discarded term that cannot be made ≪ xL^{-A} (for example, if the (a, h) > 1 terms were of size ≍ X/L^{O(1)});
  - a wrong normalisation between T_Y (∏V_i^{-1}) and Q_Y (∏V_i^{-2}), or a missing factor X/Y in (4.6), so that
    (4.8) would not follow;
  - a conjugation error in the second line of (4.7);
  - coefficients α, β that violate Prop. 4.2's hypotheses.

Outcome: success criterion met, conditional on (I2). No-go not triggered.

## Source
- arXiv:2610.20242v2. Fetched 2026-11-28 with curl into the new empty directory /tmp/claude-0/lww (not committed).
- SHA-256 `7ac341311b4a648c32c2b23b3029e1f4a3202258b55614a33ba7e8282423d000` (matches notes/sources-lww26.md).
- Read with pdftotext -layout: pp. 1-18 (Section 2: (2.1), Prop. 2.1 with Vaughan (2.3), (2.12)-(2.15), Prop. 2.3;
  Section 3 end; Section 4.1 through Prop. 4.2 on p. 18). Also read: Prop. 5.3 (p. 63) and (5.31)-(5.33) (pp. 69-70),
  where (4.8) is used.
- pp. 15-16 were rendered to PNG (pdftoppm, 130 dpi) and read visually. This settled:
  - (4.4): [corrected after the audit] at 400 dpi the second line reads "T_3(F) ≤ Σ∫|ψ̂(v)| T(M,N) dv + …", with
    **no** bars on T(M,N) (the 130-dpi reading of bars was wrong);
  - (4.7): the second line has α_m\overline{α_r}β_n\overline{β_s} (pdftotext drops the bars);
  - (4.8): the right side is Σ_Y ((MN/Y)Q_Y)^{1/2}.

## Definitions used (Literature, read in source; nothing to check)
- (2.1): L = log x, Z = exp(L^{0.24}), U = V = x^{1/5}, R_Z(n) = 1_{P^-(n)>Z}, and c_V(r) = Σ_{ℓ|r, ℓ>V} Λ(ℓ), with
  0 ≤ c_V(r) ≤ log r.
- (2.12)-(2.13):
  - P_i = {p : exp(L^{a_i}) < p ≤ exp(2L^{a_i})}, with 1/10 < a_1 < … < a_K < 1/5. The P_i are pairwise disjoint, and all
    their primes are odd and < Z.
  - ω_i(n) = #{p ∈ P_i : p | n} and V_i = Σ_{P_i} 1/p.
  - W(n) = ∏_i ω_i(n)ρ^{ω_i(n)−1}/V_i, with 0 < ρ < 1 and 0 ≤ W ≪_{K,ρ} 1 (p. 7).
- Prop. 3.1 (p. 10): F(n) = µ(n+2)W(n+2).
- (4.3): α_m = µ(m)R_Z(m)m^{iv} and β_n = c_V(n)R_Z(n)n^{iv}, each restricted to its box.
- η (p. 16), and Q_Y of (4.7).
- Prop. 4.2 (p. 18): X = MN, together with its hypotheses on α and β.

## Steps checked

**R0. (4.1) is Prop. 2.1's T_3 with F(k) = µ(k+2)W(k+2).** Proved here.
- Substitute F(dr) = µ(dr+2)W(dr+2) into T_3(F) (p. 5) and rename d → m, r → n.
- Re-derived in passing: Vaughan's identity (2.3), sign included. Λ_{>V} = Λ_{>V}*µ_{≤U}*1 + Λ_{>V}*µ_{>U}*1, and
  Λ_{>V}*µ_{≤U}*1 = µ_{≤U}*log − µ_{≤U}*Λ_{≤V}*1. So the last term enters with a +, and its inner sum over ℓk = r is
  c_V(r).
- The Z-error of Prop. 2.1 is outside this card.

**R1. Smoothing 1_{x<mn≤2x} → ψ(mn/x).** Proved here; the import is replaced by a construction (T4).
- ψ exists. Let ψ = 1_{[1,2]} * φ_ε, where ε = L^{-B}, φ_ε(t) = ε^{-1}φ(t/ε) and φ ≥ 0 is a fixed C^∞ bump with
  support in [−1, 1] and integral 1. Then:
  - 0 ≤ ψ ≤ 1;
  - ψ = 1 on [1+ε, 2−ε], and ψ = 0 outside (1−ε, 2+ε);
  - |ψ^{(j)}| ≤ ‖φ_ε^{(j)}‖_1 = ε^{-j}‖φ^{(j)}‖_1 ≪_j L^{Bj}.
  LWW's reference [2, p. 242] was not read; it is not needed.
- Error. |1_{(x,2x]}(mn) − ψ(mn/x)| ≤ 1, and it is supported where mn lies in I_1 = (x(1−ε), x(1+ε)) or in
  I_2 = (x(2−ε), x(2+ε)). Both intervals lie in [x/2, 3x] and have length ≤ 2xε. The summand of (4.1) has absolute
  value ≤ c_V(n)‖W‖_∞ ≤ (L+2)‖W‖_∞. So the error is ≤ (L+2)‖W‖_∞ Σ_{k∈I_1∪I_2} τ(k).
- The divisor bound. Σ_{k∈I}τ(k) ≤ 2Σ_{d≤√(3x)}(|I|/d + 1) ≪ |I|L + x^{1/2}. This uses τ(k) ≤ 2#{d | k : d ≤ √k}.
  It is elementary, so it is proved here.
- Total error: ≪_{K,ρ} L(xL^{1−B} + x^{1/2}) ≪ xL^{2−B}. ✓ This matches LWW.

**R2. (4.2), Mellin inversion and its two bounds.** Proved here; LWW state it without proof (T4).
- Put g(s) = ψ(e^s) ∈ C_c^∞(ℝ). Then ψ̂(v) = (2π)^{-1}∫g(s)e^{-ivs}ds. Fourier inversion for C_c^∞ functions gives
  ψ(y) = ∫ψ̂(v)y^{iv}dv pointwise, and the sign conventions agree with LWW.
- For j ≥ 1, g^{(j)}(s) = Σ_{i=1}^{j} S(j,i)e^{is}ψ^{(i)}(e^s), where S(j,i) are Stirling numbers of the second kind.
  This is supported on two s-intervals of length ≪ ε, so ‖g^{(j)}‖_1 ≪_j L^{B(j−1)}. Integration by parts j times
  gives |ψ̂(v)| ≪_j L^{B(j−1)}|v|^{-j}.
- With j = 2: ∫_{|v|>L^{2B}} |ψ̂| ≪ L^{B}·L^{-2B} = L^{-B}, uniformly in y. ✓
- With j = 0 on |v| ≤ 1 (‖g‖_1 ≪ 1) and j = 1 on 1 < |v| ≤ L^{2B}: ∫_{|v|≤L^{2B}}|ψ̂| ≪ 1 + 2B log L. ✓
- The implied constants depend only on φ.

**R3. Dyadic split, (4.3)-(4.4).** Proved here; the order of steps is terse (T1).
- Write m ∈ (U2^j, U2^{j+1}] and n ∈ (V2^k, V2^{k+1}]. Keep the boxes that meet supp ψ(mn/x). Since MN < mn ≤ 4MN,
  every such box has MN ∈ [(1−ε)x/4, (2+ε)x), so MN ≍ x. There are ≪ L such boxes, since for each j at most 4 values
  of k occur. This is within the "≤ L³ dyadic segments" of (5.32).
- The ordering matters. The truncated Mellin integral does not vanish off supp ψ, so its O(L^{-B}) error must be
  applied only to pairs inside the kept boxes. Those pairs satisfy mn < 4(2+ε)x. Their total weight is
  Σ|α_mβ_n| ≤ (L+2)Σ_{k≤9x}τ(k) ≪ xL². This gives the stated O_{K,ρ}(xL^{2−B}).
- LWW write (4.2) before the split and do not spell this out. The bound is correct once the split comes first.
- Coefficients: |α_m| ≤ 1, and |β_n| ≤ log(2N) ≤ L + 1. So with C ≥ 2 and x large, |α_m| ≤ L^C R_Z(m)1_{(M,2M]} and
  |β_n| ≤ L^C R_Z(n)1_{(N,2N]}. Also M, N ≥ x^{1/5} ≥ x^δ for every δ < 1/5. These are Prop. 4.2's hypotheses. α is
  exactly µR_Z·m^{iv}, as Prop. 5.3 requires.
- (4.4), first line ✓. The second line is printed with T(M,N), not |T(M,N)|, on the right (S1). T(M,N) is complex
  (it carries m^{iv}), so the line is meaningless as printed; the intended bound, with |T(M,N)|, follows from the
  triangle inequality, which is the form R9 and (4.8) use.

**R4. The W-expansion (p. 15).** Proved here; Computed (A), (B).
- ω_i(k) = Σ_{p∈P_i, p|k} 1. So W(k) = ∏V_i^{-1}Σ_{(p_1,…,p_K), p_i∈P_i, p_i|k}ρ^{ω(k)−K}, with ω := Σω_i.
- The P_i are disjoint, so p_i | k for all i ⟺ a = p_1⋯p_K | k. Also the tuple ↦ a map is injective.
- With k = ah:
  - if (a, h) = 1, then µ(ah) = (−1)^Kµ(h) and ω(ah) = K + ω(h);
  - otherwise µ(ah) = 0.
- So LWW's display is exact. ✓

**R5. Removal of (a, h) = 1.** Proved here, with (I2); LWW say only "by trivial estimate" (T2).
- The dropped quantity is
  D = (−1)^K∏V_i^{-1}Σ_{tuples}Σ_{mn+2=ah, (a,h)>1} α_mβ_nµ(h)ρ^{ω(h)}.
  Its terms are **not** zero individually: µ(ah) = 0, but µ(h) need not be. The toy shows D ≠ 0 (NEG (B)). So an
  estimate is needed, and the full expansion equals T(M,N) + D.
- (a, h) > 1 ⟹ p := p_i | h for some i ⟹ p² | mn + 2.
  - Given p, the number of tuples with p_i = p and a | mn + 2 is ≤ ∏_{j≠i}ω_j(mn+2) ≤ (2L^{0.9})^{K−1}. This holds
    because ω_j(k) ≤ log k / L^{a_j}.
  - For fixed m: if p | m, then p ∤ mn + 2 (p is odd). Otherwise n lies in one class mod p², so there are
    ≤ N/p² + 1 values of n.
  - Hence |D| ≤ ∏V_i^{-1}(L+2)(2L^{0.9})^{K−1}Σ_{p∈∪P_i}(2X/p² + 2M) (using M < m ≤ 2M).
  - Bound the sums. Σ_{p>exp(L^{0.1})}p^{-2} ≤ 2exp(−L^{0.1}). Also Σ_p M ≤ exp(2L^{0.2})·X/N ≤ X x^{-1/5+o(1)}.
- Result: |D| ≪_K XL^{0.9K+1}e^{−L^{0.1}} ≪ XL·exp(−L^{1/20}). The x-threshold depends on K. ✓ This matches LWW's
  O_{K,ρ}(XL exp(−L^{1/20})). In fact the constant does not depend on ρ.
- This uses: a_i > 1/10 (lower end of P_i), a_i < 1/5 (count of P_i), p odd, ∏V_i^{-1} ≪_K 1 (I2), and N ≥ x^{1/5}.

**R6. η and (4.5).** Proved here; Computed (C).
- Construction. Let χ ∈ C^∞ be nondecreasing, with χ = 0 on (−∞, 1] and χ = 1 on [2, ∞). Put η(t) = χ(t) − χ(t/2).
  Then supp η ⊂ [1, 4], 0 ≤ η ≤ 1, η is real, and η^{(j)} ≪_j 1. The sum Σ_ℓ η(t/2^ℓ) telescopes to 1 for t > 0.
  LWW assert only existence; realness and 0 ≤ η ≤ 1 are used in (4.7) and in Lemma 4.1.
- All sums are finite (a ≤ exp(2ΣL^{a_i})), so the interchange is trivial. This gives Σ_ℓ T_{2^ℓ} = T(M,N) + D,
  which is (4.5) with error −D. ✓
- On the support: Y ≤ a ≤ 4Y and h = (mn+2)/a ≤ (4X+2)/Y. ✓
- Range of Y. a ∈ [exp(ΣL^{a_i}), exp(2ΣL^{a_i})], so the Y with T_Y ≠ 0 number ≪ K L^{1/5}, and Y = x^{o(1)}.

**R7. Cauchy-Schwarz, (4.6).** Proved here; Computed (E).
- T_Y = (−1)^K∏V_i^{-1}Σ_h c_h S_h, where c_h = µ(h)ρ^{ω(h)} with |c_h| ≤ 1 (since 0 < ρ < 1) and
  S_h = Σ_{tuples}η(a/Y)Σ_{mn+2=ah}α_mβ_n.
- S_h = 0 unless 1 ≤ h ≤ (4X+2)/Y. So |T_Y|² ≤ ⌊(4X+2)/Y⌋·∏V_i^{-2}Σ_h|S_h|² = ⌊(4X+2)/Y⌋Q_Y ≤ 6(X/Y)Q_Y.
- The normalisations agree: ∏V_i^{-1} squared is the ∏V_i^{-2} of (4.7). The constant 6 is absolute. ✓

**R8. (4.7), second line.** Proved here; Computed (D).
- Expand |Σ_a η(a/Y)Σ_{mn+2=ah}α_mβ_n|². Use η real and sum over h ≥ 1. The pair of conditions (mn+2 = ah, rs+2 = bh,
  h ∈ N*) becomes (mn+2)/a = (rs+2)/b ∈ N*, and the summand is α_m\overline{α_r}β_n\overline{β_s}. ✓
- Here "a = p_1⋯p_K" means a sum over tuples, which by R4 is the same as a sum over the integers a. The α_m and β_n
  are understood as restricted to their boxes.

**R9. (4.8).** Proved here.
- From (4.4) and (4.5), |T_3(F)| ≤ Σ_{M,N}∫|ψ̂|(Σ_Y|T_Y| + |D|)dv + O(xL^{2−B}).
- The |D| part is ≪ L·(1 + 2B log L)·xL e^{−L^{1/20}} ≪ xL^{-A}.
- The smoothing error is ≤ xL^{-A} once B ≥ A + 2 (T3).
- Then |T_Y| ≤ (6(MN/Y)Q_Y)^{1/2}, which gives (4.8). ✓
- Hand-off (read p. 70, not re-derived beyond the bookkeeping). (5.32) inserts Q_Y = Q_Y^maj + O(MNYL^{-A'}) (Prop. 4.2)
  and Q_Y^maj ≪ MNYL^{-A'} (Prop. 5.3), then sums over ≤ L³ (M, N, Y) and ∫|ψ̂| ≪ log L. This needs Props. 4.2 and 5.3
  uniformly in v, M, N and Y. R3 shows their hypotheses hold uniformly. Uniformity of the reduction inside Prop. 4.2
  was recorded in the 2026-11-27 p23-27 card. Prop. 5.3 states uniformity in |v| ≤ x^{C_0}.

## Inputs not proved here
- **(I2)** V_i = log 2 + o(1) (Mertens; LWW p. 7). Only V_i ≫ 1 is used: in R5, and through ‖W‖_∞ ≪_{K,ρ} 1 (LWW p. 7) in R1, R3 and R9 [corrected after the audit]. It was not re-derived or read in a
  source. It is standard.
- Fourier inversion for C_c^∞ functions on ℝ (textbook analysis). It is used, not re-proved.
- LWW's [2, p. 242] (the construction of ψ) was **not read**; R1 replaces it.
- Upstream (not this card): (I1), the divisor bound (4.9), for Prop. 4.2 itself.

## Terse places (gap fillable; how)
- **T1** (p. 15): Mellin truncation versus the dyadic split. The O(L^{-B}) error must be applied only inside the kept
  boxes (R3). This is a standard reordering.
- **T2** (pp. 15-16): "By trivial estimate" for the (a, h) > 1 terms. Filled by the residue-class count in R5 (no
  divisor-function bound is needed). One should also note that the dropped terms are nonzero.
- **T3** (pp. 15-16): B is "a sufficiently large constant", but (4.8) and (5.32) claim xL^{-A} for every A. So B must
  be chosen after A (B ≥ A + 2). This is harmless, since B enters elsewhere only through ∫|ψ̂| ≪ B log L.
- **T4** (p. 15): (4.2) and its two bounds are stated without proof, and ψ is imported from [2]. Both are filled in
  R1-R2.
- **T5** (p. 16): the existence of η and its realness/positivity (R6).

## Slips and typos (none affects the argument)
- **S1** (4.4) [corrected after the audit]: the right side of the second line has T(M,N) where |T(M,N)| is meant
  (T(M,N) is complex). Harmless: the triangle-inequality form is what is used later.
- **S2** (p. 16): X is used in "O(XL exp(−L^{1/20}))", (4.5) and (4.6) before it is defined. It is defined as X = MN
  only in Prop. 4.2 (p. 18).
- **S3** (p. 16): "we may see that The contribution": stray capital.
- **S4** (4.5): the error term is printed without the subscript K. The constant depends on K (R5).
- **S5** (p. 15): ω(h) := Σ_iω_i(h) reuses the symbol ω, which means "number of prime factors" on p. 8 ((2.19)). It is
  local and harmless.

## Uniformity
- **Constants.** R1 and R3: K, ρ (‖W‖_∞). R2: φ only, with ∫|ψ̂| ≪ 1 + 2B log L. R5: K (with (I2)). R7: absolute.
- **x-threshold.** It depends on K (absorbing L^{0.9K} into e^{−L^{0.1}+L^{0.05}}) and on B.
- **Uniform in.** v, the box (M, N), and Y. None of the bounds uses anything about α, β beyond |α| ≤ 1 and |β| ≤ L + 2.

## Computation (Computed)
Script: code/parity/lww_p15_16_check.py, run with /usr/bin/python3 -I. Output: code/parity/lww_p15_16_check.out.
Exact arithmetic (Fractions, Gaussian rationals). Toys: K = 1 ({3,5,7}), K = 2 ({3,5},{7,11}), K = 3 ({3},{5,13},{7}).
Small boxes, random Gaussian-rational α, β, ρ ∈ {1/2, 2/3, 1/3}.
- **(A)** µ(n)W(n) equals the (a, h) = 1 expansion for all n ≤ 3000. NEG: the same expansion with the condition dropped
  fails 247, 65 and 11 times.
- **(B)** T(M,N) of (4.3) equals the (a, h) = 1 expansion exactly. NEG: dropping the condition without an error term
  fails in all three toys (|D|² = 70.2, 80.1, 181). Also:
  - every (a, h) > 1 term has p_i² | mn+2;
  - the per-m count is ≤ N/p² + 1 (0 if p | m);
  - |D| is ≤ the R5 bound, a union bound with actual counts (18-2700× slack), so it cannot fail informatively.
- **(C)** η partition of unity on A; Σ_Y T_Y = T(M,N) + D exactly; the support facts Y ≤ a ≤ 4Y and
  h ≤ (4X+2)/Y.
- **(D)** (4.7): the first line equals the literal second line exactly. NEG: the second line without conjugates fails.
- **(E)** (4.6) with the explicit factor ⌊(4X+2)/Y⌋, for the true c_h and for c_h = 1. NEG: the inequality without the
  factor X/Y, at α = β = 1 and c_h = 1, fails.
- **(F)** Sanity checks: the dyadic-box facts of R3 (1.1M pairs) and the short-interval divisor bound (300 intervals).
- **Results:** 32 positive checks, 0 failing; 12 negative controls, all failing as they must; 0 unexpected. Wall time
  about 16 s.
- **Not tested:** the Mellin bounds (4.2), any asymptotic size (only the R5 bound's arithmetic shape), (I2), and
  Prop. 4.2. The η used is piecewise linear (rational), not smooth; the identities do not use smoothness.
- **Honesty note.** The first draft had two bugs, both in the test code and neither in LWW:
  - the (C) check compared Σ_Y T_Y with T − D instead of T + D;
  - the K = 3 toy had D = 0, because every bad h was non-squarefree, so its NEG passed.
  Both were fixed (the sign corrected; the K = 3 box changed from (11, 13) to (18, 25), which gives the bad term
  19·43 + 2 = 273·3) before the recorded run.

## First unresolved
(I1): the divisor bound (4.9) (p. 17), needed by Lemma 4.1 and hence by Prop. 4.2. It is a consequence of Shiu 1980,
which is unread. Alternatively one could give an elementary proof of the weaker (X/Y)e^{o(L^{0.1})} bound that
suffices. (I2) (Mertens) is the other open standard input.

## Audit
Fresh-context adversarial audit (spawned by the main session, Session 62): 2026-11-28-lww-p15-16-reduction-audit.md.
Tally: 1 error (the card misread (4.4); see S1, corrected), 0 gaps, 1 overstatement ((I2) is used beyond R5;
corrected), 2 slips (descriptions of two script checks; corrected). 0 errors in LWW's mathematics; every step R0-R9
re-derived by the auditor; the script re-run gives the committed output, and four mutated copies were each caught.

Earlier note (before the audit):
(Superseded.) No independent audit had been run at writing time. The task called for a fresh-context adversarial audit agent. The session
that wrote this card had no tool for spawning agents, so no audit file
(2026-11-28-lww-p15-16-reduction-audit.md) exists. Until one is run, treat the classification as unaudited.
- A self re-check against the PDF was done instead. It is **not** independent. It re-read pp. 15-16 (PNG) and
  re-verified the R3, R5 and R6 counts. One slip was fixed: S5 had cited "(4.11)'s context", where ω does not occur.
- Script re-run after the edit: 32 positive checks, 0 failing; 12 negative controls, all failing; 0 unexpected; ~16 s.
