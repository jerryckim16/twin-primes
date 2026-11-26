# Audit: route card 2026-11-26-lww-p48-53-norms.md (LWW pp. 48-53, (4.124)-(4.135))

Adversarial audit, fresh context, 2026-11-26.

**Source.** /tmp/claude-0/lww/v2-rZ9L/lww.pdf. SHA-256 7ac34131...d000 (matches). I extracted pp. 44-54 and the
full text myself with pdftotext -layout. I rendered pp. 49 and 52 at 150 dpi (pdftoppm) to read the displays
pdftotext garbles. I also read pp. 7, 17-23 and 36 ((2.12), (4.13), (4.17)-(4.34), (4.91)).

**Script.** I read code/parity/lww_p48_53_norms_check.py in full and compared it with its committed .out. The
numbers in the card match the .out, except for item 7.

**Verdict.** I found no error in LWW. The card's main conclusion holds: (4.125) and (4.135) follow from the listed
inputs, plus the two inputs added in items 2-3. Specific findings:
- The constant bookkeeping is correct: LWW's choices give exponents -A-2.8 and < -A-2, and the minimal thresholds
  are K > 200(A+1) and A_0 > A+0.2.
- The weighted Schur test (4.123) is used correctly, with C(T) = R(T*) and the w(s)m(s) weight.
- The uniformity claim is correct.
- The G_j factors on p. 49 are as printed. I checked the render: the q_j belongs to q_j/ϑ^2, not to the exponential.
- The lattice, Gram and Dirichlet steps are correct.

There are 11 findings: **1 error, 3 gaps, 3 overstatements, 4 slips**. All of them are in the card or script, not
in LWW.

## Findings

1. **Error. S1 is not a slip in LWW.**
   - The p. 52 display before (4.132) is printed with **double bars** ‖·‖, i.e. distance to the nearest integer. This
     is the same notation as in (4.26) and (4.27). The 150 dpi render of p. 52 shows this clearly.
   - pdftotext dropped the bars, and the card read the display as |·|.
   - The printed statement is exactly what script check (E) confirms as its positive case.
   - The (E) negative control does not test the printed text. It tests a misreading.

   **Fix (card):**
   - Delete S1.
   - In N6, replace "**read in R/Z** (S1)" with "(the printed ‖·‖ is the distance to the nearest integer)".
   - In N6, Computed (E): replace "The literal |X| <= 16/p_* fails in 345/2340" with "the absolute-value reading
     |X| <= 16/p_* (not LWW's) fails in 345/2340, so the ‖·‖ is needed".
   - In the header, replace "Two terse places and one notational slip (S1-S3)" with "one terse place (S4, item 2
     below) and remarks S2-S3; no slip".

   **Fix (script):**
   - In the docstring, change "(E) ... NEG: the literal absolute value |.| (as printed) fails" to "NEG: the
     absolute-value reading |.| (LWW prints ‖.‖) fails".
   - Change the report label "(E) NEG literal |X| <= 16/p* (as printed)" to "(E) NEG |X| <= 16/p* (absolute
     value, not LWW's ‖·‖)".

2. **Gap. The column entries ε_K in the p. 52 table need the permutation average at the z' end. The card does not
   say this or list it as an input.**
   - The card's N6 says: "The column is the row of O_j^*, which swaps S and I and uses (4.27) at (g̃z', p')". Its
     input list is "U2, U4-U6, U8", without U3.
   - In the adjoint row at a fixed t = (z', p', m'), the (J+1)^{-K} gain needs a sum over *which* entry of each list
     at z' is the unshared one. Only then does the uniqueness of D·Z_S from (4.27) at (g̃z', p') fix that choice.
   - That sum exists only if O_j carries the (4.32) average on its right as well as its left. Equivalently, O_j must
     act on functions symmetric in each prime list.
   - This holds in LWW: A_{1,ℓ} = G_{1,ℓ} S T_{1,ℓ} S G_{1,ℓ}, (4.91), p. 36. In (A A^*)^R every T and T^* therefore
     sits between two copies of S.
   - Without the right-hand S, D is fixed by the ordering of t. The adjoint row then only avoids ⌈L^2⌉^{|S|-1} and
     gives C = O(⌈L^2⌉). For S ≠ ∅, I = ∅, Schur would then give only ‖·‖ ≪ L, not o(1).
   - So the C column of the table, and with it (4.135), uses this structure essentially.
   - LWW's p. 48 phrase "We also keep the permutations in (4.32)" leaves the endpoints unstated. This is terse, not
     wrong.

   **Fix:**
   - In N6, after "The column is the row of O_j^*", insert: "This needs the (4.32) average at the z' end too (S on
     both sides of T_{1,ℓ}, (4.91) p. 36). It makes the unshared entry at z' range over the J+1 entries with weight
     (J+1)^{-1} each, so (4.27) at (g̃z', p') yields (J+1)^{-K}. With the average only at z, the adjoint row is
     O(⌈L^2⌉) and the S ≠ ∅, I = ∅ entry fails."
   - Change "relative to U2, U4-U6, U8" to "relative to U2-U6, U8, U10".
   - Add **U10**: "O_j carries the (4.32) permutation average at both endpoints (A_{1,ℓ} = G S T S G, (4.91), p. 36;
     S^2 = S = S^*, G S = S G, (4.33), p. 22)."
   - Add **S4 (p. 48, terse)**: "'keep the permutations in (4.32)' must be read as at both endpoints. The column
     entries of the p. 52 table depend on it."

3. **Gap (minor). Within-list distinctness is used but not listed.**
   - N6 concludes "the omitted entry is fixed in all K tuples" from "D·Z_I unique". This needs the entries of each
     list p_i to be pairwise distinct. Otherwise two omitted positions holding the same prime give the same D.
   - The adjoint version needs p_* = p_{i*,J+1} to differ from the shared entries at z', which is the same fact.
   - "D is squarefree" (p. 48) also rests on it.
   - LWW does impose it: p_{i,j} ≠ p_{i,h} is built into the set of states (4.19), p. 19, and p. 51 lists "the
     indicators of distinctness within each prime tuple" among the factors of O_j. Section 4.6 itself "allow[s]
     repetitions in the underlying space" (p. 47), so the indicator has to come from the operator.
   - The card cites only (4.23), i.e. p'_i ∉ p_i.

   **Fix:** add to U2 or as **U11**: "O_j contains the within-list distinctness indicators ((4.19), p. 19; p. 51)".
   Cite it in N6 at "the omitted entry is fixed" and at the adjoint step.

4. **Overstatement. S2 is not a terse place in LWW, and its "Computed" illustration is a hand formula.**
   - LWW states that functions are invariant under permutations of the coordinates of each m_i (p. 47). The p. 49
     factorial identities are exactly the multiset/symmetric computation. The ordered "append at the end" kernel is
     the card's own model, not LWW's.
   - In the script, the "ILLUSTRATION" in (C) does not enumerate the ordered kernel. It evaluates the hand-derived
     closed form `col_ord = q/th^2 + kp*eta*V/(th*v0)`. This exceeds the printed q/ϑ^2 + η'V/(ϑv_0) for every k' >= 2
     and every parameter set, by inspection. So "12/12" carries no information. The closed form itself is correct
     (I re-derived it: m(s)/m(t) = k'/λ).

   **Fix:**
   - Reclassify S2 as a remark: "LWW works on symmetric functions (p. 47), and the p. 49 identities are the
     multiset computation. In an ordered-tuple model the column would carry an extra factor k'. Not a slip."
   - In N2, replace "Computed (C), illustration: for k' = 6 it exceeds the printed factor in 12/12 parameter sets"
     with "hand computation: the ordered column is q/ϑ^2 + k'η'V_i/(ϑv_0) > printed for k' >= 2".
   - In the script, relabel the print line as "hand formula, not enumerated".

5. **Overstatement. S3 is listed as a "slip / terse place" but is neither, and the "room to spare" claim needs a
   scope.**
   - S3 (A_0 > A+3 and K > 200(A+3) are more than needed) is a remark about generous constants.
   - The header claim "K > 200(A+1) and A_0 > A+0.2 would already suffice" is correct for (4.135) within pp. 48-53.
     I re-derived the exact thresholds: 1 - 0.005K < -A, and 0.2 - A_0 < -A.
   - It says nothing about whether Section 4.7 or Prop. 4.2 rely on the larger margins. The audit did not check this.

   **Fix:**
   - Move S3 into N8 as a remark.
   - In the header, add "(for (4.135) itself; later uses of A_0, K not checked)".

6. **Slip. The card says the gain beats the loss "once K > 200(A+1)", which mixes up two thresholds.**
   - Header: "It beats the ceil(L^2) loss once K > 200(A+1)". In fact ⌈L^2⌉(J+1)^{-K} → 0 already for K > 200.
   - K > 200(A+1) is the threshold for √ε_K = o(L^{-A}).

   **Fix:** replace with "it beats the ⌈L^2⌉ loss for K > 200, and gives √ε_K = o(L^{-A}) once K > 200(A+1)".

7. **Slip. A count in N5 is wrong.**
   - N5 says "Computed (H): 5534 θ ∉ M_1, 0 failures".
   - In the script, n also counts the four |M_1| measure checks (one per (Q0, Y)), so the θ count is 5530.

   **Fix:** "Computed (H): 5530 θ ∉ M_1 plus 4 |M_1| checks (5534 cases), 0 failures".

8. **Overstatement. The card overstates what the script covers.**
   - The script checks generic ingredients: identities, the Schur test on random matrices, lattice counts, the Gram
     bound, Dirichlet, and exponent arithmetic. Nothing computed touches the core of N6 (the stated focus):
     - the uniqueness of D·Z_I from the (4.27) separation;
     - the (J+1)^{-K} weight;
     - the column entries of the table;
     - the N3 counts behind (4.125);
     - E_coll;
     - (4.129).
     N6 rests on (D) and (E) plus argument.
   - Several negative controls fail by construction, so they detect nothing beyond what is evident:
     - (A) "drop a!" fails for any a >= 2;
     - (J) "K = 200A" and "A_0 = A" are the inequalities 1 - A < -A and 0.2 - A < -A, which are false for all A;
     - (E)'s negative control tests a misreading (item 1).
   - The meaningful controls are:
     - (D), j_1 ≡ 0;
     - (F), without max(A', B');
     - (G), without d log 2d;
     - (H), radius L^{A_0}/(4Y);
     - (B), mildly.
   - (I) has no negative control and asserts no box constants.

   **Fix:** under "Computation, Limits", add: "No computed check of the N6 mechanism, i.e. the (4.27) uniqueness,
   the (J+1)^{-K} weight and the table columns, nor of the N3 counts. These are argument only. The (A) and (J)
   controls are by construction. (E)'s control tests a misreading."

9. **Slip. U8 lists something that is derived directly.**
   - U8 lists "τ ≍ 1 on Z_0" as an unchecked transfer input.
   - It follows directly from (4.118) and the p. 47 range u/(d_0YM) ∈ [1, 16]: τ(z) ∈ [1/16, 16].

   **Fix:** remove it from U8 and state it in N5 as "(4.118) with u/(d_0YM) ∈ [1,16]".

10. **Gap (minor). N5 leaves out two steps that LWW states.**
    - LWW p. 51 handles the Fourier-inversion tail |v| > L^{A_0}/2 by the rapid decay of ψ̂_1 and the trivial matrix
      bound O(Y). N5 handles only |v| <= L^{A_0}/2.
    - The reduction ‖E_0‖ <= sup_{θ∉M_1} ‖·‖ (diagonalising the a - b convolution, over a set of measure <= 1) is
      asserted without saying why.

    **Fix:** add to N5: "Tail |v| > L^{A_0}/2: ∫|ψ̂_1(v)| dv over it is ≪_N L^{-NA_0}, times the trivial bound
    Y^{-1}·#R ≪ 1. The a - b dependence is a convolution on Z, which Fourier diagonalises, so ‖E_0‖ <=
    ess sup_{θ∉M_1} ‖K_θ‖."

11. **Slip (notation). N5 uses S for two different things.**
    - N5 writes "||S|| = 1" for the (4.32) permutation operator. In the same card, S is the subset of groups that
      append pairs.

    **Fix:** write "‖S_{(4.32)}‖ = 1 (the permutation average, (4.33))".

## Checked and found correct (no action)
- N1: the weighted Schur test, with C as on p. 52 (w(s)m(s)).
- N2: the row and column factors and "parentheses < 1". η' = 1 - q makes q/ϑ^2 + η'/(ϑv_0) increasing in q, so the
  maximum is at √ρ.
- N3: the counts, |M_1| <= 4L^{3A_0}/Y and 1/V_i <= 2.
- N4: the reading of the multiplier remark.
- N5: (4.126)-(4.130). This covers λ >= Y^{-0.8}, the box, Dirichlet with d <= ⌈Y/L^{A_0}⌉, the source of L^{0.2},
  the tensor structure and E_coll.
- N6 row argument: p_* ∤ Db, h_* independent of D and Z_I, the window, 32/p_* < 100e^{-L^{a_{i*}}}, the exceptional
  weight <= 2^K e^{-L^{0.1}/4}, hϑ^{h-1}, and the (J+1)^{-K} weight.
- N7: (4.133) and (4.134), including Y >= a/4 >= e^{KL^{0.1}}/4.
- N8: exponents, minimal thresholds, no circularity through C_*, and uniformity in (u, v, r), d_0, j and a_i.
- The L > 1.65·10^63 illustration.
- J = ⌊L^{0.01}⌋ (p. 18), so J + 1 > L^{0.01}.
