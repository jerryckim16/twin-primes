# Audit: route card "E_mem and (4.138)-(4.147), LWW pp. 55-58" (2026-11-25)

Audited: `notes/parity-attempts/2026-11-25-lww-p55-58-emem.md` (the card is not edited here), with
`code/parity/lww_p55_58_check.py` and `.out`.

## Source and re-run (by this referee)
- I downloaded arXiv:2610.20242v2 into a new empty scratch directory. SHA-256
  `7ac341311b4a648c32c2b23b3029e1f4a3202258b55614a33ba7e8282423d000` matches. I ran pdftotext -layout and re-read
  pp. 44-58, plus pp. 7, 18, 27, 32-33, 35-40 for definitions.
- I rendered pp. 47, 49 and 55-57 to PNG and read them. They confirm the following:
  - ϑ^2 > √ρ (p. 47);
  - √ρ/ϑ^2 + 1/(ϑv_0) < 1 (p. 49);
  - κ_0 = ⌈C_0 · 2R log L / L^{0.1}⌉ (p. 56);
  - C_0 > 2(C_* + E_0 + 7) (p. 56);
  - the C_0 / 𝒞_0 font distinction (S4).
- The abs page lists v1 (14 Oct 2026, 53 KB) and v2 (19 Nov 2026 16:45:02 UTC, 78 KB). There is no v3. This
  matches the card.
- `/usr/bin/python3 -I code/parity/lww_p55_58_check.py` (Python 3.13, sympy 1.14.0) ran in 6.4 s. Its output is
  identical to the committed `.out`, line for line, including the runtime.

## Verdict in one line
I found no error in LWW pp. 55-58, and none in the card's mathematics. I agree with the card's reading of every
displayed step. The problems are in how the card classifies and documents its result:
- the headline classification is stronger than what was shown;
- R2 has an inconsistent status;
- some inputs are used but not listed;
- one statement about factors of 2 is wrong (harmless);
- several "checks" and "negative controls" are weaker than they are presented.

Counts: **0 errors, 4 gaps, 2 overstatements, 2 slips**. Findings 9-15 record what was confirmed OK.

## Findings (most serious first)

1. **Overstatement: the classification line (card header; pp. 49-53, 35-45, 54).**
   - The card says "**proved under a stated reading**" and "Every step from the p. 54 identity to |M_R| << L^{-2R(E_0+4)} ... was either derived here or checked".
   - The real content of the conclusion is in inputs the card did not check:
     - (4.135), ||O_j|| <= L^{-A}. This is the whole low-rank saving in (4.147).
     - (4.124)-(4.125) and the p. 49 "choice multipliers" remark. (4.142), (4.143) and the modified-operator bounds of D6 are built from these.
     - (4.95), which needs all of Prop. 4.5(i), pp. 38-45.
     - (4.73).
     - The p. 54 identity, which the previous card proved only under R1.
   - The repo's index already uses "conditional" for this kind of result (Session 53). Session 54's "proved under R1" fitted there because that identity was self-contained. This one is not.
   - **Fix:** change the classification to **"conditional: the implication [inputs] ⟹ |M_R| << L^{-2R(E_0+4)} ⟹ (4.78) ⟹ (4.136) is proved here under R1"**. Name the inputs in the same line. Change "Every step ... was derived" to "every step, relative to the listed inputs, ...".

2. **Gap: R2 has an inconsistent status (card D3 "Reading R2", S3, inputs list, "Next in line"; pp. 45, 55).**
   - The card calls R2 a *reading*. But D3 goes on to supply its own count of the operator-expansion skeleton, which does not use the p. 45 bound. The count covers:
     - the z_j in Z_0;
     - the tuple primes;
     - the permutations;
     - the per-O_j factor bounds;
     - the ϑ cancellation.
   - Yet the card also lists "the p. 45 configuration count" as an unchecked input, and as "next in line" (header, and "What this does NOT show").
   - These cannot all be true:
     - If D3's count stands, then R2 is not a reading but a supplied proof (a gap-fill for S3). The p. 45 count is then not used. Only the size bounds are used: log(Rd_0Y) << L^{0.21} and |P_i| <= exp(2L^{0.2}).
     - If D3's count does not stand, then E_mem depends on an assumption the card never states.
   - D3's list is also slightly incomplete. It names 2^K choices of S per O_j, but not the 2^K choices of I. Nor does it say that the permutation weights from (4.32) and the indicators for D and (4.26)/(4.27) are <= 1. All of these are harmless, at exp(O(KR)) or bounded by 1.
   - **Fix:** remove R2 from the "Readings used" list. Restate it as "S3 gap, filled in D3 (proved here)", and add the I-choices to the count. Delete "the p. 45 count" from the inputs, from "first unresolved / next in line" and from "What this does NOT show". Replace it with "log(Rd_0Y) << L^{0.21} (p. 40)". The alternative is to keep R2 as an assumption and drop "Proved here" from D3. Do one or the other, not both.

3. **Gap: some inputs are used but not listed as "taken as given".**
   - **V_i = log 2 + o(1)** (§2.3, p. 7). The card uses a *lower* bound on V_i in three places. "V_i < 1", which it cites, gives only the upper bound. The places are:
     - the factors prod_{i∈I} V_i^{-1} per O_j (R2);
     - V_i^{-(κ_p-1)} per tuple prime (D3), absorbed into exp(O(J+R));
     - Σ_{p∈∪P_i} 1/p = Σ V_i << 1 (D2). This last one needs only the upper bound, which is fine.
   - **log(Rd_0Y) << L^{0.21}**: proved on p. 40, and only quoted on p. 45 (see 8).
   - **(2.12)**: |P_i| <= exp(2L^{0.2}) and p_min > exp(L^{a_1}) with a_1 > 1/10. The card uses these for b'_p >= 1/2 and for the tuple-prime count.
   - **The p. 54 identity itself** (previous card, under R1). It is the starting point, but it is not in the inputs list.
   - **The p. 49 remark** that the absolute bounds (4.125) survive multipliers of modulus <= 1 that preserve symmetry. D6 uses it ("modified O_j: L^{C_*}"; G_j: C). It is a separate claim from (4.125) and should be named.
   - **(4.142)** is labelled "Proved here", but it is a modification of the unchecked (4.124)/(4.125) row count, with a prescribed prime contributing ν_i(p) <= Δ instead of s_i.
   - **Fix:** add these items to the "taken as given" bullet and to "Not checked (inputs)". Label (4.142) "proved relative to the (4.124) count".

4. **Gap: D6, why Φ^sym, and whether the modified operators meet the p. 49 proviso (p. 57; p. 49 last paragraph).**
   - D6 proves that replacing Φ_l by Φ^sym leaves I(𝒞_0) unchanged. It does not say what the replacement is *for*, and it does not check the condition that makes the bounds still apply.
   - On p. 49, the absolute bounds (4.125) survive inserted multipliers only "provided they preserve symmetry in the coordinates of m_i present before the operation".
     - For the column bound of G_j, computed through G_j^*, the appended tuple plays the role of the pre-existing coordinates. That is where the symmetry of Φ^sym is needed.
     - For the modified O_j, the multipliers must also be checked: the phase e(θ_h p'_i) on the ν-selected entry, and the indicator 1[a ∈ B_act] (the ν option versus taking from m). Both are trivially symmetric in m, but the card does not say so.
   - **Fix:** add two sentences to D6. Say that Φ^sym is what makes the p. 49 proviso hold for the modified G_j, in the adjoint/column direction. Say that the O_j multipliers depend only on p'_i and on the I/ν choice, so they are symmetric in the pre-existing coordinates of m_i. List the proviso as an input (see 3).

5. **Overstatement (minor): what the computations test (card "Computation", D2, D5, D6).**
   - **(D) series check.** It compares truncated sums that satisfy the inequality term by term (1/l! <= 1/(l-s)!). It cannot fail.
   - **(D) retention check.** The script chooses v_0 so that √ρ/ϑ^2 + 1/(ϑv_0) < 1, then tests q ∈ {ρ, √ρ}. Since q/ϑ^2 + (1-q)/(ϑv_0) increases in q, the result is implied by the construction.
   - **(E).** It checks the abstract substitution identity Σ Φ^sym F ν = Σ Φ F ν for symmetric F. It does not test the substantive claim, which is that the rest of the expansion *is* symmetric in the appended tuple. That claim is argued in prose only.
   - **(G).** It checks the card's own transcription of the exponents, with symbolic constants.
   - **Negative controls.** Four of the nine do not run the checking code at all. They only show that a hypothesis is needed:
     - η' = 3/2;
     - ϑ^2 > ρ only;
     - C_0 = 2(C_* + E_0 + 3);
     - R ≍ L.

     The controls that do show the checker can detect an error are the (4.140) sign and weight, n^κ, dropping h_t, and the non-symmetric F.
   - **(C) tuple part.** This is the check most exposed to a modelling error, and it has **no negative control**. It also counts histories without weighing them, so the D3 weight claim (<= 4V_i^{-(κ_p-1)}) is not computed anywhere.
   - **(C) non-tuple part.** The DP builds R1 in, and builds in V_iν_i = 1/((p+1)b'_p) through the parameters (nu is computed from b'_p). So it tests the ϑ bookkeeping and the summation structure, not R1 and not (4.120).
   - **Fix:**
     - Relabel (D) and (E) as "sanity checks of elementary lemmas".
     - Split the "nine negative controls" into "detection controls (5)" and "hypothesis-necessity illustrations (4)".
     - Add a detection control to the tuple-history DP. For example, allow a second ν-selection after discarding, or allow G-removal in a gap; the count must then differ from (a+1)(2R-c+1).
     - Add a weighted version of the tuple-history DP. It should give at most 2·V_i^{-(κ_p-1)}·(max first-selection weight); see 6.
     - In "Limits", state that (C) has R1 and (4.120) built in.

6. **Slip: S2 and D3, the factor 2 for tuple primes (p. 55).**
   - The card says each tuple-prime history has "at most two factors 2", and S2 says the factor 2 "also applies to tuple primes (prefix/suffix), giving at most 4".
   - This is wrong about the suffix. In the suffix, the pair is appended by O_c (the S option), not by a G_j, so it gets no inserted factor 2. Under distinctness a tuple prime is selected once, so it has at most one G-append, in the prefix. The paper's own wording on p. 55 agrees: "appended or removed by the operators G_j" means a G-append in the prefix and a G-removal in the suffix.
   - Also, "ν_i or 2η'ν_i <= 2" already contains that single factor 2, so "4" counts it twice. The expression is loosely written as well: the G-first weight is 2η'_hV_iν_i/ϑ, times ϑ, times one extra 1/V_i at the transfer in. Relative to V_i^{-(κ_p-1)} this is 2η'_hν_i.
   - The bound 4 is still a valid overestimate, so nothing downstream changes.
   - **Fix:** S2 should read "the factor 2 applies only to a prefix G-append; at most one per tuple prime (<= 2), absorbed in exp(O(J+R))". In D3, replace "at most two factors 2" by "at most one factor 2".

7. **Gap (minor): the uniformity clauses of Prop. 4.6 are not tracked (p. 53 statement and last paragraph; p. 57-58).**
   - The card says it reaches (4.136). But Prop. 4.6 asserts (4.136) "uniformly for the values of d_0 in (4.52)". It also asserts that A_0 and K are chosen "independently of the fixed exponents a_i". And the M_R bound must be uniform in (u, v, r) over the region before (4.95) is integrated.
   - The card says nothing about any of these. They hold because every bound used is uniform, with the dependence on a_i only in the threshold for x (p. 53). But that is inherited from the inputs, not checked.
   - **Fix:** add one bullet: "Uniformity in d_0 and (u, v, r), and independence of a_i, inherited from (4.121), (4.125), (4.135) and (4.95) (p. 53, last paragraph); not checked here."

8. **Slip: a page citation (card D3/R2, "What was read").**
   - "log(Rd_0Y) << L^{0.21} (p. 45)". This bound is *derived* on p. 40, from log d_0 <= 2KJL^{0.2} and log Y <= 2KL^{0.2}. Page 45 only quotes it.
   - **Fix:** cite p. 40, and add the bound to the inputs list (see 3).

9. **OK: quotes of pp. 54-58.**
   - All of the following match the PDF and the rendered images:
     - the E_mem definition, including max over 0 <= t <= 4R+1, Σ_i k_i^{(t)} > ⌈L^2⌉ and the inserted factor 2;
     - the non-tuple display and the bound 2(2R+1)/((p+1)b'_p);
     - (4.138) and (4.139);
     - B_act;
     - (4.140)-(4.147);
     - κ_0 with the ceiling;
     - C_0 > 2(C_* + E_0 + 7);
     - A = E_0 + 5;
     - the p. 58 closing sentence.
   - The parameter citations are correct: L = log x (p. 4, (2.1)); J = ⌊L^{0.01}⌋ (p. 18); R = ⌈L^{1/2}/2⌉ (pp. 27, 40); (4.73) on p. 32; (4.78) on p. 33; (4.93) and (4.95) on pp. 36-37.

10. **OK: D1, E_mem set-up and S1.**
    - Each kernel is restricted at both ends, so the truncated expansion is exactly {γ : max_t Σk^{(t)} <= ⌈L^2⌉}.
    - The O_j append at most 2KR coordinates, so a counted γ has at least ⌈L^2⌉ + 1 - 2KR G-appends.
    - The printed 2^{-⌈L^2⌉+2KR} is weaker by a factor of 2, and valid.

11. **OK: D2, the non-tuple prime factor.**
    - I re-derived the ϑ pairing for append, retained-matching (q_j), unmatched and remove.
    - I re-derived the telescoping Σ_{c>a} y_c Π(1-y_j) = 1 - Π(1-y_j) ∈ [0,1].
    - I re-derived the bound 1 + 2·2R/((p+1)b'_p) and b'_p >= 1/2.
    - I also checked the ϑ cancellation for a tuple prime's gap and suffix pair, which the card asserts without displaying. The exponent is 0.
    - Check (C) is a faithful single-prime model. Its h_t detection control is meaningful.

12. **OK: D3, the tuple-history count.**
    - (a+1)(2R-c+1) is right. The prefix options are fresh or G_h with h < a. In the gaps, the S option is forced and no removal is allowed. The suffix options are discard, or an O_c-append followed by a G_h-removal with h > c.
    - I read through the DP code, including the closure over `new`, and found no bug. All 676 occupancy sets for R <= 4 match.

13. **OK: D4, (4.139)-(4.141).**
    - (4.140) is exactly the partition-lattice Möbius identity. Check (A) tests exactly that statement, over all 19531 = (5^7 - 1)/4 cases, and its two sign and weight controls are meaningful.
    - (4.141) holds: the sum equals c(n, n-κ) <= C(n,2)^κ <= n^{2κ}, and at most 2κ indices are involved. Check (B) is exact.

14. **OK: D5 and D6, the arithmetic.**
    - The direction of the row-bound iteration is right: the innermost (rightmost) sum is taken with the values to its left fixed, so later indices are the prescribed ones.
    - s <= K in (4.142).
    - b <= w, and ||b||^2 = Π s_i^{J+1} = 1 + o(1).
    - Σ_{κ>=κ_0} y^κ <= 2y^{κ_0} <= 2L^{-C_0R}.
    - The margin (6+δ)R - C_* is right.
    - "At most 2κ operators are modified" holds, by monotonicity in the number m <= 2κ of modified O_j.
    - The exponent -2AR + κ(2β + 2A + 2C_*) + o(R) is right, with -2AR + 2R(E_0+4) = -2R.
    - At p. 58: the integration volume is 15, and cL^{3/4} >> RE_0 log L.

15. **OK: scope disclaimers.**
    - The card says it is not a check of Prop. 4.6 or 4.2, that LWW remains Claimed and unrefereed, that twins (K = 0) are untouched, and that there is no parity-breaking content. It nowhere implies more.
    - "No error in LWW found" agrees with my reading of pp. 54-58.
