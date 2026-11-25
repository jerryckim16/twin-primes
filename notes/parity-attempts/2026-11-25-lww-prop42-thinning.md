# Route card: does LWW Prop. 4.2 survive thinning of the auxiliary prime sets? (2026-11-25)

**Classification: conditional.** Every use of P_i, V_i, |P_i| and the auxiliary-prime structure in pp. 26-47 and
53-61 (Sections 4.3-4.5, 4.7), and in pp. 47-53 (Section 4.6), re-read this session, goes through for arbitrary
P'_i ⊂ P_i with c_0 <= V'_i (c_0 > 0 fixed). The change is routine: replace P_i, V_i, nu_i, s_i, omega, G(P_1) and the
line-average weights prod (p+1)^{-1} by the same objects built on P'_i. Implied constants then also depend on c_0.
The choices of A_0 and K (p. 53, after (4.135)) do not. The success criterion below is met (Literature reading +
Proved here, elementary bookkeeping). The no-go criterion is not triggered.
- This is conditional on [LWW] Prop. 4.2 being correct as stated (Claimed, unrefereed). It is a statement about the
  robustness of their argument, not a check of it.
- **First unresolved implication** (for the Remark 1 route of the 2026-11-24 card, Finding 4): Type I for the target
  G_g with general bounded multiplicative f. That needs P3 (BV with zero main term) for f. It rests on the Session 40
  outline only. On the Prop. 4.2 side, Appendix Lemma A.1 (p. 72, statement only, not its proof) and [17] are
  unread.
- Twins (K = 0) are untouched. There is no parity-breaking content of our own.

## Question
The previous card (2026-11-24-lww-prop53-twist.md) left this open: does [LWW] Prop. 4.2 (Q_Y - Q_Y^maj << XY L^{-A},
p. 18) hold when every P_i is replaced by a subset P'_i (e.g. P_i ∩ {p ≡ a mod q_0}) with V'_i = sum_{P'_i} 1/p >= c_0?
The earlier answer rested on a text scan of pp. 26-47 and 53-61. This card replaces the scan with a line-by-line
reading.

## Criteria (written 2026-11-25 ~01:36 UTC, before reading pp. 26-47, 53-61)
- Success criterion: every step in pp. 26-47 and 53-61 (Sections 4.3-4.5, 4.7) that uses P_i, V_i, |P_i|, the
  density of the auxiliary primes, or exact values (V_i = log 2 + o(1), sizes of P_i, completeness of residue
  classes) goes through for arbitrary P'_i ⊂ P_i with V'_i >= c_0 > 0 (c_0 fixed), each change stated with
  page/equation.
- No-go criterion: a step that genuinely needs the full P_i (exact value of V_i, a PNT/prime-count lower bound on
  |P_i| used to absorb a loss, orthogonality over all residues, an identity over all primes in the interval), with
  page/equation, that cannot be repaired by a stated routine change.

Outcome: success criterion met (conditional on LWW). No-go not triggered.

## Sources read (this session)
- arXiv:2610.20242v2, fetched 2026-11-25 01:35:39 UTC from https://arxiv.org/pdf/2610.20242v2 into a new empty
  scratch directory (not committed). SHA-256 `7ac341311b4a648c32c2b23b3029e1f4a3202258b55614a33ba7e8282423d000`
  (matches). Converted with pdftotext -layout and split at form feeds; PDF page n = printed page n.
- Abs page https://arxiv.org/abs/2610.20242, fetched 2026-11-25 01:35:44 UTC: v1 (14 Oct 2026, 53 KB) and v2
  (19 Nov 2026, 78 KB). **No v3.**
- Read line by line: pp. 15-17 (context: (4.1)-(4.13), Lemma 4.1), 18-26 (context), **26-47**, 47-53 (Section 4.6,
  re-read), **53-61** (to the start of Section 5).
- Statement only: Lemma A.1 (p. 72). Not opened: [17] (OpenAI), [4], [19], or the proof of Lemma A.1.

## Notation
As in the previous card. Primes in P_i lie in (exp(L^{a_i}), exp(2L^{a_i})] ((2.12), p. 7), with 1/10 < a_i < 1/5.
V_i = sum_{P_i} 1/p. Thinned: P'_i ⊂ P_i, V'_i = sum_{P'_i} 1/p in [c_0, V_i]. J = floor(L^{0.01}), R = ceil(L^{1/2}/2),
B = ceil(L^{3/4}).

## Findings (each: page/equation; what is used; survives thinning?; change)
Kinds of use: [N] means normalised by the set's own V_i, so it holds by the definition of V'_i. [U] is an upper bound
on |P_i| or on sum 1/p, which subsets keep. [L] is p >= exp(L^{a_i}) for p in P_i, which subsets keep. [C] is a
constant through V_i^{-1}, which becomes c_0^{-1}.

1. **p. 26, 1 - w(a,b).** The bound w(a,b) <= 1 is [N]. The bound
   0 <= 1 - w << J^2 exp(-cL^{0.1}) uses (J^2/2) sum 1/(pV_i)^2 + J/(p'V_i) + J/(p_{i,J+1}V_i). This is [L]+[C]: the
   right side picks up a factor c_0^{-2}. **Survives.**
2. **(4.49)-(4.51), pp. 26-27.** prod V_i^{-2} << 1 becomes c_0^{-2K}. (4.50) uses (4.9) (divisor sums, p. 17), and
   (4.51) counts O(Y^2) pairs (a, b) trivially. Neither depends on the set. **Survives** [C].
3. **Prop. 4.3, (4.53)-(4.66), pp. 27-30.** P_i enters only through ||f|| << (d_0 Y M N)^{1/2} L^{2C} ((4.43), p. 25,
   via sum_{P_i} 1/p = V_i, [N]) and through log(d_0 Y) = O_K(L^{0.21}) (product of K(J+1) primes <= exp(2L^{0.2}),
   [U]). The other ingredients are set-free: the position counts (#{P : P_2/P_1 in I_j} << d_0 Y, at most 16
   solutions per h, p. 29), the spectral/Hölder step (4.64), and (4.66). (I re-derived (4.66) from (4.63)-(4.65);
   the exponent bookkeeping checks.) **Survives.**
4. **Prop. 4.4, (4.67)-(4.78), pp. 31-33.** U_T is unitary because sigma = prod V_i^{-(J+1)} is constant and T fixes the
   prime tuples. This is set-free. **Survives.**
5. **(4.79)-(4.88), pp. 33-35: counting with line conditions.**
   - Lemma A.1 (p. 72) is stated for any squarefree S.
   - The count 2 prod_{p|S} p(p-1) of g_0 is over p | S, p > 2. The main term 1/(3ζ(2) prod_{p|S}(p+1)) is
     prime-by-prime.
   - S <= exp(O(L^{0.98})) is [U].
   - There is no completeness over the set: only the primes dividing S appear.
   **Survives.**
6. **(4.89)-(4.94), pp. 35-37.** ℓ ranges over choices of lines at every p in ∪P_i. M_R ((4.93)) averages over ℓ with
   the probability weight prod_{p in ∪P_i} (p+1)^{-1}. Built on ∪P'_i, this is again a probability measure. The inner
   product <.,.>_ℓ has prod V_i^{-(J+1)}, which is [N]. **Survives**, with the change: products over ∪P'_i.
7. **Prop. 4.5(i), pp. 37-45.**
   - (4.97)-(4.102) are a set-free change of variables. (4.103)-(4.110) are set-free except for "every selected prime
     is at most exp(2L^{0.2})" and #{(a, ϑ)} <= exp(O_K(L^{0.21})) (p. 40-41, via (4.29)). Both are [U].
   - **(4.111)-(4.112), p. 43.** The inclusion-exclusion over q_1 < ... < q_k in ∪P_i is a finite identity for any
     finite set. log S << L^{0.96} is [U].
   - **(4.115), p. 44.** sum_{p in ∪P_i} (p+1)^{-1} <= sum_i V_i <<_K 1 is [U]. It gives (C_K R)^B/B! <<
     exp(-cL^{3/4}). A smaller set only helps.
   - **p. 45.** exp(O_K(L^{0.71})) configurations, using |P_i| <= exp(2L^{0.2}), [U]. The "remaining coefficients
     exp(O_{K,ρ}(R(J+1)))" include factors prod_i V_i^{-(J+1)-2R} (total exponent K(J+1+2R); audit finding 1). These become exp(O_{K,ρ,c_0}(R(J+1))), still
     << exp(o(L^{3/4})) [C]. **Survives.**
8. **Prop. 4.5(ii), pp. 45-46.** As in 7. The bound sum 2/(p+1) for H_{1,p} is prime-by-prime, and |P_i| <=
   exp(2L^{0.2}) is [U]. **Survives.**
9. **Good-state conditions and measure, (4.26)-(4.31), pp. 21-22**, used again at p. 52 and in (4.154)-(4.156).
   - (4.27) weights tuples by prod 1/(q_i V_i). The total weight is 1 ([N], p. 21).
   - (4.29) #{D̃ Z_I} <= (J+1)^K prod |P_i| = exp(o(L^{a_{i*}})) is [U].
   - The Markov step (4.30) uses only the total weight 1 and the pair count. So (4.31) holds for the thinned sets with
     the same exponent.
   **Survives.** This is the "probability over the auxiliary set" step, and it does not use density.
10. **Section 4.6, pp. 47-53 (re-read).**
    - (4.121): pV_i nu_i(p) = 1 + O(R/p) [N]; Delta << c_0^{-1} e^{-L^{0.1}} [L]+[C]; s_i = 1 + O(R/p_min) [N]+[L].
    - p. 49 Schur test: needs only V'_i < 1, with V_i in numerators.
    - (4.125): 1/V_i for groups in I is [C].
    - p. 50: m(a) <<_K Y^{-1} is [C]. Uniqueness of a = q_1...q_K needs disjoint P_i, and subsets of disjoint sets are
      disjoint.
    - **p. 52 (key step).** At most one product D Z_I fits, because 32/p_* <= 32 e^{-L^{a_{i*}}} < 100 e^{-L^{a_{i*}}}
      (separation from (4.27)). Here p_* in P_{i*}, so p_* > exp(L^{a_{i*}}) [L]. ε_K in (4.132) depends on the set
      only through C_{K,ρ} (now also on c_0), and its L-power L^{2}(J+1)^{-K} is set-free.
    - (4.133)-(4.134): p_min >= e^{L^{0.1}} [L].
    - (4.135): A_0 > A + 3 and K > 200(A + 3) are set-free.
    **Survives**, with the same A_0, K.
11. **Section 4.7, pp. 53-58.**
    - (4.137) and the per-prime expansion (pp. 53-54) are exact identities for each p. They use only
      V_i nu_i(p) = 1/((p+1)b'_p) (a definition) and the V_i^{-κ_p} bookkeeping.
    - ||b||^2 = prod s_i^{J+1} = 1 + o(1) [N]+[L].
    - (4.138): prod (1 + C_ρ R/p) <= exp(C_ρ R sum_{∪P_i} 1/p) <= exp(C_{K,ρ} R) [U].
    - (4.140)-(4.141): combinatorial. (4.142)-(4.143): Delta [L]+[C], V_i in numerators.
    - (4.144)-(4.145) need C|B|^2 Delta <= e^{-L^{0.1}/2}. This holds with c_0^{-1} absorbed.
    - (4.146): orthogonality on T^s is used to impose equalities of integers p_a = p_{a'}. It is not orthogonality over
      residues or over the set.
    - (4.147) is set-free.
    **Survives.**
12. **Section 4.8, pp. 58-61.**
    - (4.149)-(4.151) are as in 8.
    - (4.152): ω_ℓ >= K(J+1) and ρ < 1.
    - (4.153): the average over ℓ_q at q not dividing Dab is (q+1)^{-1} sum 1 = 1, prime-by-prime, for any set.
    - p. 60: sum_{q in P_i} 1/(q+1) <= V_i, raised to the power J+2, cancels the prod V_i^{-(J+2)} of (4.152) [N].
    - (4.155) is set-free. (4.156)-(4.157) use (4.31) (item 9).
    **Survives.**
13. **Searched for and not found** in the pages read:
    - any lower bound on |P_i| or on the number of primes of P_i in a subinterval;
    - any use of V_i = log 2 + o(1) beyond V_i < 1 (p. 49);
    - any sum over all residue classes, or over all primes of an interval, that is not normalised by V_i or by
      (p+1)^{-1} per prime;
    - PNT, Siegel or Mertens for the auxiliary primes.
    The size condition |P'_i| >= J+2 ((4.19), (4.22)) follows from V'_i >= c_0, since |P'_i| >= c_0 exp(L^{a_i}).
14. **Order of constants (Proved here, elementary).** A_0 and K are fixed at p. 53 from A alone. c_0 enters only the
    implied constants and the x-threshold, through c_0^{-O(K)}, c_0^{-(J+1+2R)K} = exp(O(R)) (item 7), and Delta.
    So for fixed c_0 the statement of Prop. 4.2 holds verbatim, with <<_{A,K,ρ,c_0}, **uniformly over all subsets**
    P'_i ⊂ P_i with V'_i >= c_0 (P'_i may depend on x and, downstream, on a residue class (a, q_0)); implied constants
    and the x-threshold depend only on A, K, ρ, δ, C, c_0 (and the a_i). c_0 -> 0 with x is NOT covered (audit finding 4).
15. **Lemma 4.1, p. 17 (used at p. 26 to drop gcd(a,b) > 1 from Q_Y; added after audit finding 3).** It uses
    prod V_i^{-2} <<_K 1 (a lower bound on V_i) and sum_{∪P_i} 1/p^2 << e^{-L^{0.1}}. Under thinning: c_0^{-2K} [C] and
    [L]. **Survives.** (So item 13's "not found" list refers to lower bounds used to absorb losses beyond such [C] constants.)

## Possible issues in LWW (presumed our misreading until checked)
- None that bear on thinning or on correctness.
- p. 30, after (4.66): "there are O_K(L) intervals [d_0, 2d_0)". The true count is O_K(L^{0.21}), since
  log d_0 <= 2KJL^{0.2}. This is a harmless overcount, not an error.
- p. 54: "Multiplication over p proves the identity below" (the expression of M_R through G_j, O_j). This is the
  least explicit step in Section 4.7. I checked only that it uses the set through per-prime normalisations. I did not
  re-derive the identity, so its correctness is not checked here.

## Outcome
The first unresolved implication of the 2026-11-24 card is closed conditionally. Prop. 4.2 holds for thinned sets
P'_i with V'_i >= c_0 if it holds as stated. Combined with the previous card (Prop. 5.3, Section 3 and Prop. 2.3 survive
thinning), route (b) of that card is complete in outline, conditional on LWW. The remaining gap for Remark 1 is on
the Type I side (Session 40 outline), not in Prop. 4.2.

## What this does NOT show
- Nothing about whether LWW is right or wrong. Every statement is conditional on Prop. 4.2 (and 5.3, Section 3,
  Prop. 2.3) being correct. They are Claimed, not verified, and this card checked robustness, not correctness.
- Nothing about twins: K = 0 is untouched. Lambda(n+2) has no P2 (sources-lww26.md).
- No parity-breaking content of our own.
- Not read: the proof of Lemma A.1 (pp. 72-), [17], [4], [19]; the identity on p. 54 not re-derived.
- No numerics. Nothing here is visible at toy scale.

## Scripts
None. No Lean.

## Fresh-context audit (2026-11-25)
Adversarial re-read against the v2 text (pdftotext pages p15-p61), about 45 minutes. I re-read pp. 17-30, 32, 34-61
directly, spot-checked items 1, 7, 9, 10, 12 and 14, and looked for the specific break points: lower bounds on |P_i|
or V_i used to absorb a loss, quantitative uses of V_i = log 2 + o(1), counts over all primes of an interval, and
c_0 entering A_0, K, J, R, B, C_*, kappa_0. No step was found where thinning breaks.

Checks that came back clean:
- Item 1 (p. 26). 1 - w <= sum_i [(J^2/2) sum 1/(pV_i)^2 + J/(p'_i V_i) + J/(p_{i,J+1} V_i)] uses that the full
  sum is (sum_{P_i} 1/(pV_i))^J = 1. That is [N]. The loss is at most c_0^{-2}. Confirmed.
- Item 7 (pp. 43-45). (4.112)-(4.115) use only finite inclusion-exclusion and sum (p+1)^{-1} <= sum V_i. The
  constant c in exp(-cL^{3/4}) comes from (C_K R)^B/B! and does not depend on the set. The coefficients of
  (4.100)-(4.102) carry prod_i V_i^{-(J+1)-2R}. So c_0 costs c_0^{-K(J+1+2R)} = exp(K log(1/c_0) (L^{0.01} + L^{1/2}
  + 1)) = exp(O_{K,c_0}(R)), which is o(L^{3/4}). Confirmed. In (ii) (p. 46) the same holds with
  prod V_i^{-(J+2)} rho^{-K(J+1)} = exp(O(L^{0.01})).
- Item 9 (pp. 21-22). (4.29) uses only |P_i| <= exp(2L^{a_i}). (4.30) uses only total weight 1 ([N]). (4.31) is
  therefore unchanged. Confirmed.
- Item 10 (pp. 47-53).
  - Delta << c_0^{-1} e^{-L^{0.1}}.
  - s_i = 1 + O(R/p_min) follows from normalisation ([N]).
  - In the Schur test (p. 49) the column factor needs eta' V_i/(theta v_0) <= 1/(theta v_0). V'_i <= V_i < 1 is
    enough.
  - The factors 1/V_i at transfers from m_i, and m(a) << c_0^{-K} Y^{-1}, are per-step constants c_0^{-O(K)}. They
    are absorbed into L^{C_*} in (4.125) for large x, so C_*, kappa_0 and C_0 do not change.
  - (4.132): the per-step saving L^2 (J+1)^{-K} comes from the symmetrisation weight and does not depend on the set.
    The constant C_{K,rho} becomes C_{K,rho,c_0}, and in (4.147) C^{2R+1} = L^{o(R)}.
  - The p. 52 separation step uses p_* > e^{L^{a_{i*}}} ([L]) and the weights prod nu_i ~ prod (p V_i)^{-1}, which
    hold with set-free constants.
  Confirmed.
- Item 12 (pp. 58-61). In (4.152)-(4.154), prod V_i^{-(J+2)} cancels exactly against (sum_{P_i} 1/(q+1))^{J+2} <=
  V_i^{J+2} ([N]). (4.153) is prime-by-prime. (4.155) does not depend on the set. (4.156) uses (4.31). Confirmed.
- Item 14. J, R and B are fixed powers of L. A_0 > A+3, K > 200(A+3), E_0 > A+4C+2 and A = E_0+5 do not depend on
  the set. C_* = C_*(K, A_0, rho) is unchanged because c_0^{-K} is absorbed by one power of L. c_0 enters only the
  implied constants and the x-threshold. Confirmed.
- Item 13. |P'_i| > c_0 exp(L^{a_i}) is correct, since V'_i < |P'_i| e^{-L^{a_i}}.
- The occurrences of V_i = log 2 + o(1) at text lines 354, 474, 502 and 739 are all in Sections 2-3. Prop. 4.2's proof
  does not invoke them. At 474 and 739 only V_i < 1 is used.

Findings:
1. **slip** (item 7; p. 38 (4.100)-(4.102), p. 45). "V_i^{-(J+1)-2RK} factors" should read prod_i V_i^{-(J+1)-2R},
   which is a total exponent K(J+1+2R). Item 14 has it right. The conclusion is unaffected.
2. **slip** (item 10; (4.121), p. 47). The identity p V_i nu_i(p) = p/((p+1)b'_p) = 1 + O(R/p) does not depend on the
   set. Labelling it [N] is harmless.
3. **gap**, an omission that survives (Lemma 4.1, p. 17, used at p. 26 to drop gcd(a,b) > 1 from Q_Y). It uses
   prod V_i^{-2} <<_K 1, a lower bound on V_i, and sum_{∪P_i} 1/p^2 << e^{-L^{0.1}}. The card does not list it, and
   item 13's "not found" list could be read as excluding it. With thinning it becomes c_0^{-2K} ([C]) and [L], so it
   survives.
4. **gap/overstatement** (item 14, "holds verbatim"). Item 14 does not state that the bound holds uniformly over all
   admissible subsets. P'_i = P'_i(x) changes with x, and downstream it would change with a residue class (a, q_0).
   So the statement should read: uniformly over all P'_i ⊂ P_i with V'_i >= c_0, with implied constants and
   x-threshold depending only on A, K, rho, delta, C, c_0 (and a_i for the threshold). The proof supports this,
   because every use is of type [N]/[U]/[L]/[C], but the card should say it. It also needs c_0 fixed: c_0 -> 0 with
   x is not covered.
5. **gap** (disclosed by the card). The p. 54 identity (M_R through G_j, O_j) was not re-derived, here either. Its
   dependence on the set is per-prime (V_i nu_i(p) = 1/((p+1)b'_p), V_i^{-kappa_p}), so thinning does not affect it.
   Its correctness is part of the "conditional on LWW" hypothesis.
6. **No errors found.** The "Possible issues" remark is correct: the O_K(L) count of intervals [d_0, 2d_0) on p. 30
   is really O_K(L^{0.21}) (log d_0 <= 2KJL^{0.2}, p. 40), and the overcount is harmless.

Classification "conditional" is honest. The card checks robustness only and says so. The Outcome's "route (b) is
complete in outline" also rests on the previous card, which this audit did not re-check.

**Verdict:** no step in pp. 17-61 breaks under thinning to P'_i with V'_i >= c_0 (c_0 fixed). The conclusion stands,
conditional on LWW. Fix the item-7 exponent, add Lemma 4.1, and state uniformity in P'_i.


### Fixes applied (coordinator, Session 53)
Findings 1 (exponent in item 7), 3 (Lemma 4.1, new item 15) and 4 (uniformity in P'_i, c_0 fixed; item 14) applied.
Finding 2 (label of (4.121)) is harmless and left as recorded. Finding 5 is already disclosed (p. 54 identity not
re-derived; part of the 'conditional on LWW' hypothesis). The coordinator also spot-checked (4.115) and the p. 49
'V_i < 1' step in the text.
