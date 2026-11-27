# Route card: LWW reduction Q_Y − Q_Y^maj → (4.52) (pp. 16-18, 23-27) (2026-11-27)

**Classification: conditional on listed inputs.** The chain is proved here relative to LWW's definitions, with two
inputs. The only non-elementary one is the divisor bound (4.9).
- The reduction, from Q_Y − Q_Y^maj ((4.7), (4.14)) to the two inner-product sums of (4.52), was re-derived step by
  step. The steps covered are:
  - Lemma 4.1;
  - the (4.12) equivalence and the ψ_{-2} insertion (pp. 17-18);
  - the p. 24 claims: G(P_1) = Db, \overline{f(P)}f(Q) = α_m\overline{α_r}β_n\overline{β_s}, ρ^{...} = 1, t ≠ 0, and
    primitivity;
  - the expansion (4.44)-(4.46);
  - the removal of the gcd(a, b) > 1 terms from Q_Y and Q_Y^maj (p. 26);
  - the w(a, b) step (4.48), the bound on 1 − w, and (4.49)-(4.51);
  - the triangle inequality (4.52).
- **Inputs not proved here:**
  - **(I1) the divisor bound (4.9)** (p. 17): Σ_{h≪X/Y, ℓh>2} τ(ℓh − 2)² ≪ XL³/Y, uniformly for odd ℓ ≍ Y = x^{o(1)}.
    This is a standard consequence of Shiu's theorem (Brun-Titchmarsh for multiplicative functions; Shiu 1980), which
    was **not read in source** here. LWW's own one-line derivation of it is terse (T1). Only (X/Y)·exp(o(L^{1/10}))
    is actually needed, not L³.
  - **(I2)** V_i = log 2 + o(1) (Mertens). LWW state this on p. 7; it was not re-derived here. Only ∏V_i^{-2} ≪_K 1
    is used.
- **No error in LWW found.** There are thirteen terse places (T1-T13) and two harmless typos (S1). None changes the
  conclusion. Remarks S2-S3 record suppressed dependencies of constants.
- An exact toy computation (script section (D)) checks the whole chain (4.38) → (4.44) → (4.46) → (4.48) as an
  identity to 1e-15. Q_Y, Q_Y^maj and Σ B_{d_0}/d_0 are each computed literally from their definitions. Four
  plausible misreadings break it (NEG). The toy has K = 1, so the K = 2 structure is only covered by the combinatorial
  checks (A) and (E).
- Role in the chain: (4.52) is now reached from Prop. 4.2's left side, conditional on (I1) and (I2). The first sum of
  (4.52) was handled by Prop. 4.3 (2026-11-27-lww-prop43.md) and the earlier cards. The second sum is the next item.
- **First unresolved implication:** the second sum of (4.52), Σ_{d_0}|⟨f, T_{-2}^C f⟩ − ⟨f, A_{-2}^C f⟩|/d_0. This is
  Section 4.8, (4.148)-(4.157), pp. 58-61, which uses Prop. 4.5(ii)/(4.96) (stated p. 37, proof pp. 45-46). It has not
  had a full correctness check; it was only examined for set-dependence (2026-11-25-lww-prop42-thinning.md, items 8,
  9 and 12).
- This is not a check of Prop. 4.2 or of the paper as a whole. Twins (K = 0) are untouched. There is no
  parity-breaking content, and nothing here bears on the twin prime conjecture.

## Criteria
These were written after a first read of pp. 16-18 and 23-27, before the script and the final write-up. Some
derivation was done while reading.
- **Success**:
  - Every nonzero term of Q_Y − Q_Y^maj with gcd(a, b) = 1 corresponds bijectively to a nonzero term of
    Σ_{d_0} B_{d_0}/d_0 (states, p′, Q), with weight w-type factors exactly as in (4.44)-(4.46). This includes
    primitivity, C-membership, Ω-membership, G(P_1) = Db, the conjugation pattern, ρ^0, the ψ_{-2} factor and d_0/D.
  - Lemma 4.1 and the Q_Y^maj analogue give the gcd(a, b) > 1 part as o(XYL^{-A}).
  - 1 − w ≪ J²exp(−cL^{0.1}) and (4.49) ≪ XYL^{O(1)} together give (4.48).
  - The script's exact toy identity holds, and its negative controls fail.
- **No-go** (would count as an error in LWW): any of
  - a conjugation mismatch between ⟨f, Tf⟩ and the summand α_m\overline{α_r}β_n\overline{β_s} of (4.7);
  - a nonzero term of Q_Y − Q_Y^maj whose P or Q is non-primitive, or not in C or Ω (it would be missing from B);
  - a weight in (4.44) different from σ·∏V_i^{-1}·(d_0/D)/d_0;
  - a gcd(a, b) > 1 contribution, or a (1 − w)D contribution, not ≪ XYL^{-A};
  - an L-power in (4.49) that depends on something not fixed before A_0, or that is not absorbed by
    exp(−cL^{0.1}).

Outcome: success criterion met, conditional on (I1) and (I2). No-go not triggered.

## Source
- arXiv:2610.20242v2 PDF. Fetched 2026-11-27 ~17:35 UTC with curl into a new empty directory
  /tmp/claude-0/lww-p23-27/src.4N9x (not committed).
- SHA-256 `7ac341311b4a648c32c2b23b3029e1f4a3202258b55614a33ba7e8282423d000`, 895,874 bytes (matches).
- Extracted with pdftotext -layout. PDF page = printed page.
- pp. 15-18 and 23-27 were rendered to PNG (pdftoppm, 110 dpi) and read visually for the bars and indices. This
  settled:
  - (4.7) and (4.14) have α_m\overline{α_r}β_n\overline{β_s};
  - (4.42) is f(P) = \overline{α_{P_1/G(P_1)}}β_{P_2};
  - p. 24 prints \overline{f(P)}f(Q) = α_m\overline{α_r}β_n\overline{β_s};
  - B_{d_0} = Σ\overline{f(P, p)}(T_{-2}^C f)(P, p)σ;
  - (4.44)'s summand and the binomial \binom{J}{2} in the 1 − w bound (p. 26);
  - (4.52) has absolute values on both sums.
- The abs page was not re-fetched this run. The Prop. 4.3 card (same day, 09:36 UTC) recorded v1 and v2 and no v3.

## Inputs (equation numbers as printed)
- **Definitions** (Literature, read in source; they define objects, so there is nothing to check):
  - (2.1) R_Z, Z = exp(L^{0.24});
  - (2.12)-(2.13) P_i (pairwise disjoint, 1/10 < a_i < 1/5), V_i, ω_i;
  - (4.3) α, β;
  - η (p. 16, supported on [1, 4]), Y = 2^ℓ;
  - (4.7) Q_Y, (4.13) ψ_1, M_1, M_{-2}, ψ_{-2}, H_{-2}, (4.14) Q_Y^maj;
  - Prop. 4.2's hypotheses |α_m| ≤ L^C R_Z(m)1_{(M,2M]}, |β_n| ≤ L^C R_Z(n)1_{(N,2N]};
  - (4.17)-(4.22) d_0, Ω, S, σ, ⟨·,·⟩, D, a, b;
  - (4.35)-(4.38) P, Q, t, C, T_{-2}^C;
  - (4.41) A_{-2}^C, (4.42) f, G(P_1).
- **(I1)** (4.9), outside input (see the header). **(I2)** V_i = log 2 + o(1) (p. 7).
- Elementary facts used (Proved here):
  - τ(n)² ≤ τ_4(n), checked prime power by prime power: (k+1)² ≤ \binom{k+3}{3}, since 6(k+1) ≤ (k+2)(k+3).
    Hence Σ_{n≤x}τ(n)² ≤ x(1 + log x)³.
  - On T, θ ↦ −2θ preserves Lebesgue measure.

## Step-by-step re-derivation
Labels: Proved here / Literature (read in source) / Computed ((X) = script section).

**R1. Lemma 4.1 (pp. 16-17).** Proved here, given (I1) and (I2); Computed (A).
- In Q_Y (second line of (4.7)), a and b run over ordered tuples (p_i), (q_i). Since the P_i are disjoint, the map
  tuple ↦ a is injective, so pairs of tuples can be counted as pairs of integers (T3).
- Fix a and b. Both are odd (all primes in ∪P_i are > 2) and lie in [Y, 4Y] (η-support). Then
  Σ_h Σ_{mn+2=ah, rs+2=bh} |α_m α_r β_n β_s| ≤ L^{4C} Σ_h τ(ah − 2)τ(bh − 2). By Cauchy-Schwarz and (I1) with ℓ = a and
  ℓ = b, this is ≪ XL^{4C+3}/Y. Here h ≤ (4X + 2)/Y because ah = mn + 2. ✓ (T2)
- (4.11): if gcd(a, b) > 1, then some p ∈ ∪P_i divides both. The number of pairs (a, b) ∈ [Y, 4Y]² with p | a, p | b
  is ≤ ⌊4Y/p⌋². Summing over p > exp(L^{1/10}) gives ≤ 16Y² Σ_{p>e^{L^{0.1}}} p^{-2} ≪ Y² exp(−L^{1/10}). ✓
- Total, using 0 ≤ η ≤ 1 and ∏V_i^{-2} ≪_K 1 (I2): ≪ (X/Y)L^{4C+3}·Y²e^{−L^{0.1}} ≪ XY e^{−L^{1/20}}. This is stronger
  than the stated O(XYL^{-A}) (S2). ✓
- (A): over 5 toy families (K = 1, 2, 3), #pairs with gcd > 1 ≤ Σ⌊4Y/p⌋². NEG: a linear bound Σ#{a : p | a} fails
  4/5.

**R2. (4.12) equivalence and the ψ_{-2} insertion (pp. 17-18).** Proved here; Computed (B).
- If (mn+2)/a = (rs+2)/b = h ∈ N*, then b(mn+2) = abh = a(rs+2), that is, bmn − ars = 2(a − b). This direction holds
  for every (a, b).
- Conversely, suppose gcd(a, b) = 1 and b(mn+2) = a(rs+2). Then a | mn + 2, and h := (mn+2)/a = (rs+2)/b is a
  positive integer (mn + 2 > 0). For fixed (a, b, m, n, r, s), h is determined, so the sum over h in (4.7) collapses
  to the condition (4.12). ✓
- ψ_{-2}(t/Y) = ψ_1(−t/(2Y)). On t = 2(a − b) this is ψ_1((b − a)/Y), and |b − a|/Y ≤ 3 ≤ 4, so it equals 1. ✓ The
  insertion therefore holds for every term of Q_Y, coprime or not.
- 1_{t=2(a−b)} = ∫_T e(θ(t − 2(a − b)))dθ. So H_{-2}(t; a, b) = ψ_{-2}(t/Y)∫_{M_{-2}} e(θ(t + 2b − 2a))dθ is the
  major-arc piece of the same integral. The signs in (4.13) and (4.38) agree. ✓
- (B):
  - 39,127 random coprime cases, including 660 solutions of the equation: 0 failures. NEG: the equivalence for
    gcd > 1 fails in 459 cases.
  - ψ-insertion on all (a, b) ∈ [Y, 4Y]² for six values of Y: 0 failures out of 9.4M. NEG: ψ_1 = 1 only on
    |u| ≤ 2 fails.

**R3. The p. 24 step.** Proved here; Computed (C), (C′).
- Take a term with α_m\overline{α_r}β_n\overline{β_s} ≠ 0. Then R_Z(m) = R_Z(n) = R_Z(r) = R_Z(s) = 1, so
  P^-(mnrs) > Z.
- D and b consist of distinct primes (the entries of the state are distinct), so Db is squarefree; similarly Da. All
  their primes lie in ∪P_i ⊂ (2, Z), since exp(2L^{a_i}) < exp(L^{0.24}) = Z. Since gcd(m, Db) = 1 and m has no prime
  factor < Z, G(Dbm) = Db and ω_i(Dbm) = J + 1 for every i. The same holds for Dar. Hence
  - f(P) = \overline{α_m}β_s and f(Q) = \overline{α_r}β_n,
  - \overline{f(P)}f(Q) = α_m β̄_s\overline{α_r}β_n, which is the summand of (4.7)/(4.14), and
  - the ρ-exponent (ω(P_1) + ω(Q_1) − 2K(J+1))/2 is 0. ✓
- Parity: D, a and b are odd, and m, n, r, s > 1 have no prime factor ≤ Z, so they are odd. Hence P, Q have odd
  coordinates. ✓
- Ω-membership: D ∈ [d_0, 2d_0), b ∈ [Y, 4Y] and m ∈ (M, 2M] give Dbm ∈ (d_0YM, 16d_0YM), and s ∈ (N, 2N]. ✓ (This
  is implicit in LWW; see T6.)
- t ≠ 0. gcd(a, b) = 1 and P^-(rs) > Z > max ∪P_i give gcd(b, ars) = 1. If t = 0, then b | ars with b ≥ Y > 1, a
  contradiction. ✓
- Primitivity. Let p | Dbm and p | s. Since P^-(s) > Z, p > Z, so p ∤ Db and p | m. Then p | bmn − ars = t. Now
  |t| < 16Y wherever the summand is nonzero: on the indicator, |t| = 2|a − b| ≤ 6Y; on H_{-2}, the factor ψ_{-2}(t/Y)
  vanishes for |t| ≥ 16Y. Also 16Y ≤ 16a ≤ 16exp(2KL^{0.2}) < Z for large x. So 0 < |t| < p and p | t, a
  contradiction. Hence gcd(Dbm, s) = 1, and symmetrically gcd(Dar, n) = 1 (p | Dar, p | n ⟹ p | r ⟹ p | t). ✓ (T4)
- (C), exhaustive on toys T1 (K = 1, J = 1, 46 terms) and T2 (K = 1, J = 2, 2,196 terms), each with 16Y < Z: t ≠ 0,
  primitivity, G, the f-identity and ρ^0 all hold, with 0 failures.
  - NEG: f = αβ without the bar fails 2,196/2,196.
  - NEG: kernel support |t| < 960Y ≫ Z gives 18,144 non-primitive terms out of 147,504. So the claim depends on
    |t| = o(Z).
- (C′): over the whole P_1-range of Ω for T1 (10,081 values), {P_1 : f(P_1, ·) ≠ 0} is exactly {g·m}. Here f is
  evaluated from (4.42) by factorisation.

**R4. The expansion (4.44)-(4.46) (p. 25).** Proved here; Computed (D).
- Bijection (T6). Take a state (P, p) ∈ S(d_0) with P ∈ C and f(P) ≠ 0. ω_i(P_1) = J + 1 and the J + 1 listed primes
  divide P_1, so they are all the P_i-primes of P_1. With μ²(G) = 1 this gives G(P_1) = Db (D from the first J
  entries, b from the (J+1)-st), and m := P_1/(Db), s := P_2.
- Similarly a choice p′ and a Q with f(Q) ≠ 0 give Q = (Dar, n).
- Conversely, (p_{i,j}), p′ and (m, n, r, s) with nonzero coefficients and nonzero kernel give primitive P, Q ∈ C ∩ Ω
  (R3), and (P, p), (Q, p′) ∈ S(d_0).
- det(P, Q) = D(bmn − ars), so t = bmn − ars. ✓
- Weight: σ·(∏V_i^{-1})·(d_0/D)/d_0 = D^{-1}∏V_i^{-(J+2)} = ∏_{i,j≤J}(p_{i,j}V_i)^{-1}·∏V_i^{-2}. This is (4.45). ✓
- In (4.38), the factor ψ_{-2}(t/Y) multiplies {1_{t=2(a−b)} − ∫_{M_{-2}}}. On the indicator it equals 1 (R2), and
  on the integral it makes H_{-2}. This gives (4.44)'s brace (T7). ✓
- Σ_{ℓ_0} 1_{2^{ℓ_0} ≤ D < 2^{ℓ_0+1}} = 1. Ω and S depend on d_0, but every term sits in the S(d_0) of its own D.
  Dyadic d_0 with no D contribute nothing. ✓
- gcd(a, b) = 1 is automatic: p′_i ≠ p_{i,J+1} and the P_i are disjoint. The map (p′, (p_{i,J+1})) ↦ (a, b) is a
  bijection onto coprime pairs of products. D(a, b) depends only on (a, b, m, n, r, s), and D(a, b) includes ηη (T8).
  Summing the first J entries gives w(a, b). This is (4.46). ✓ (T9)
- (D): T1 and T2 are computed literally:
  - B_{d_0} = ⟨f, T_{-2}^C f⟩, over all states of S(d_0), all p′ and all Q, with a generic complex kernel c_2(t, a, b)
    in place of the M_{-2} integral;
  - Q_Y from the first line of (4.7), and again from the a, b expansion (they agree);
  - Q_Y^maj from (4.14);
  - w(a, b) by brute force over ordered tuples.
  - Result: Σ_{d_0}B_{d_0}/d_0 = ∏V^{-2}Σ_{coprime} wD agrees to 1 ulp (6.9e-18). Q_Y − Q_Y^maj − ΣB/d_0 =
    ∏V^{-2}[Σ_{coprime}(1 − w)D + Σ_{gcd>1}D_full] agrees to 1.8e-15. 12/20 coprime pairs have D ≠ 0 in T2.
  - NEG (each breaks the identity): no bar on α in (4.42); support |t| < 960Y (primitivity lost); d_0/D dropped;
    ψ_1 = 1 only on |u| ≤ 1.

**R5. gcd(a, b) > 1 and (4.47) (p. 26).** Proved here, given (I1) and (I2).
- Q_Y: by R1.
- Q_Y^maj: |H_{-2}| ≤ meas M_{-2} = meas M_1 ≤ Σ_{k≤L^{A_0}} k·4L^{A_0}/Y ≤ 4L^{3A_0}/Y, supported on |t| < 16Y.
  The per-pair bound of R6(b), Σ_{m,n,r,s}|...H_{-2}| ≪ XL^{2·2C+3+3A_0}/Y, does not use coprimality. Multiplying by
  the pair count (4.11) gives ≪ XY L^{O(1)}e^{−L^{0.1}}. LWW's "factor 1/p²" is this argument (T10). ✓
- The coprime parts of Q_Y and Q_Y^maj combine via (4.12) into ∏V^{-2}Σ_{coprime}D(a, b). Subtracting (4.46) leaves
  (4.48). ✓
- (F): meas M_{-2} = meas M_1 ≤ 4L^{3A_0}/Y, by exact interval arithmetic in 4 cases.

**R6. (4.48)-(4.51) (pp. 26-27).** Proved here, given (I1) and (I2); Computed (E).
- w(a, b) ≤ ∏_i(Σ_{p∈P_i}1/(pV_i))^J = 1 (dropping the restrictions only adds nonnegative terms).
- 1 − ∏_i w_i ≤ Σ_i(1 − w_i), since 0 ≤ w_i ≤ 1 (T13). The excluded tuples have a coincidence p_{i,j} = p_{i,k}
  (\binom{J}{2} pairs, each of weight Σ_p(pV_i)^{-2}) or an entry in {p′_i, p_{i,J+1}} (J positions each). So
  1 − w_i ≤ \binom{J}{2}Σ(pV_i)^{-2} + J/(p′_iV_i) + J/(p_{i,J+1}V_i) ≪ J²e^{−L^{0.1}}/V_i², using p > e^{L^{a_i}}
  ≥ e^{L^{0.1}}. ✓ (c = 1 works.)
- (a) (4.50). For coprime (a, b), the solutions of (4.12) correspond to h (R2). R1's per-pair bound then gives
  ≪ XL^{4C+3}/Y per pair, and O(Y²) pairs give XYL^{4C+3}. ✓
- (b) (4.51). Σ_{mn=k}|α_mβ_n| ≤ L^{2C}τ(k) with k, l ≤ 4X, and τ(k)τ(l) ≤ (τ(k)² + τ(l)²)/2. For fixed k, the l
  with |bk − al| < 16Y lie in an interval of length 32Y/a ≤ 32, so there are ≤ 33. For fixed l the same holds with
  b ≥ Y (LWW state only the first; T11). Then Σ_{k≤4X}τ(k)² ≤ 4X(1 + log 4X)³ (via τ² ≤ τ_4). This gives
  ≪ XL^{4C+3+3A_0}/Y per pair and XYL^{O(1)} in total. ✓
- (4.49) follows. The total L-power is 4C + 3 + 3A_0, with A_0 fixed from A before this point. Since
  J²e^{−L^{0.1}}·L^{O(1)} ≪ L^{-A}, (4.48) holds (S3). ✓
- (E1): exact Fractions, K = 2, J = 1, 2, 3, small sets, 1,800 cases: w ≤ 1 and the 1 − w bound hold.
- (E2): primes in (1000, 12000], J = 2, 4 cases. The bound is nearly tight here: for example 1 − w = 0.01269 against
  a bound of 0.01274. NEG: replacing J by 1 on the p′ and p_{J+1} terms fails 4/4. The E2 pair sum uses
  S_1² − S_2, cross-checked by brute force on a 400-prime slice.
- (4.51) count: #{l} ≤ 33 and #{k} ≤ 33 in 3,000 random cases (largest seen: 32).

**R7. (4.52) (p. 27).** Proved here.
- B_{d_0} = ⟨f, A f⟩ + (⟨f, T f⟩ − ⟨f, A f⟩), followed by the triangle inequality on (4.47). ✓

## Terse places / slips in LWW (none affects the result)
- **T1 (p. 17, (4.9), terse).** The middle inequality "≤ (X/Y)Σ_{d≪X^{3/4}}τ_3(d)/d" is not explained, and I could
  not reconstruct it as printed. Σ_{d|n}τ(d²) = τ(n)² and τ(d²) ≤ τ_3(d) give τ(n)² ≤ Σ_{d|n}τ_3(d). The restriction
  to d ≪ X^{3/4} and the exact "≤" are unexplained. The final bound is standard (Shiu), and it needs ℓ odd. This is
  input (I1).
- **T2 (p. 17, (4.10)).** It applies (4.9) with ℓ = a and ℓ = b. This needs a, b odd and in [Y, 4Y] (from the
  η-support); both are implicit.
- **T3 (p. 17, (4.11)).** It counts integer pairs (a, b), while Q_Y sums over prime tuples. These match because the
  P_i are disjoint (tuple ↦ a is injective). Not stated.
- **T4 (p. 24).** "0 < |t| ≪ Y = o(Z)" uses the support of each summand (indicator: |t| ≤ 6Y; H_{-2}: |t| < 16Y) and
  16Y < Z for large x. Filled in at R3.
- **T5 (p. 24).** "t ≠ 0" also needs b > 1. Trivial.
- **T6 (pp. 24-25).** The bijection between nonzero terms of B_{d_0} and (tuples, p′, m, n, r, s) is not spelled out.
  It needs ω_i(P_1) = J + 1 to force G(P_1) = Db and Ω-membership of P and Q. Filled in at R4.
- **T7 (p. 25, (4.44)).** The factor ψ_{-2}(t/Y) of (4.38) disappears without comment. It is 1 on the indicator
  (p. 17) and is part of H_{-2}.
- **T8 (p. 25).** D(a, b) "the sum over m, n, r, s in (4.44)" has to include ηη and the brace for (4.46)-(4.47) to read
  correctly. (4.50)-(4.51) then show |ηη| separately; this is consistent.
- **T9 (p. 25, (4.46)).** gcd(a, b) = 1 is automatic, and (p′, p_{·,J+1}) ↔ (a, b) is a bijection. Not stated.
- **T10 (p. 26).** The removal of the gcd > 1 terms from Q_Y^maj ("a factor 1/p²") is a paraphrase of (4.11) times the
  per-pair bound of (4.51). Filled in at R5.
- **T11 (p. 27, (4.51)).** τ(k)τ(l) ≤ τ(k)² + τ(l)² also needs O(1) values of k per l (true, since b ≥ Y). LWW state
  only the "per k" half.
- **T12 (pp. 26-27).** "|H_{-2}| ≪ L^{O(1)}Y^{-1}": the O(1) is 3A_0, from meas M_{-2} = meas M_1 ≤ 4L^{3A_0}/Y.
  This is harmless.
- **T13 (p. 26).** The step 1 − ∏w_i ≤ Σ(1 − w_i) is implicit.
- **S1 (p. 17, typos).** "adimissible" and "may replaced". Harmless.
- **S2 (remark).** Lemma 4.1 proves O(XYe^{−L^{1/20}}), which is stronger than the stated O(XYL^{-A}).
- **S3 (remark).** In (4.49)-(4.51), "≪_{K,ρ} XYL^{O(1)}" suppresses the dependence of O(1) on C and A_0 (hence on
  A). This is harmless because the bound is absorbed by e^{−cL^{0.1}}.

## Computation (Computed)
- `code/parity/lww_p23_27_check.py`; output in `code/parity/lww_p23_27_check.out`.
- Run: `/usr/bin/python3 -I code/parity/lww_p23_27_check.py`. Pure Python (no numpy). Wall time 36.1 s.
- Results: 23 positive checks, 0 failing. 10 negative controls, all failing as they must. 0 unexpected outcomes.
- A first draft's NEG for the 1 − w bound (the coincidence term dropped, small primes) passed, because the toy bound
  is very loose for tiny primes. It was replaced by E2 (large primes, nearly tight bound) with a "J → 1" NEG. No
  positive check was changed. Recorded for honesty.
- Limits:
  - The chain toy (D) has K = 1. K ≥ 2 is covered only by (A) and (E).
  - c_2 is a generic stand-in for the M_{-2} integral. The identity is linear in the kernel, so this tests the
    bookkeeping, not anything about M_{-2}.
  - In T1 and T2 the gcd > 1 part (a = b) dominates the left side. The coprime part is the small B-side and the
    (1 − w)D-side, and it is matched to 1e-15.
  - Nothing tests (I1), and no analytic size is tested.

## What this does NOT show
- It does not show (I1): the AP divisor bound (4.9) was not proved or re-read here.
- It does not show that either sum in (4.52) is small. The first sum is handled conditionally by the Prop. 4.3/4.4/4.5/4.6
  cards. The second sum (Section 4.8) is unchecked.
- It does not check pp. 15-16 ((4.1)-(4.8), the removal of (a, h) = 1, and the Cauchy-Schwarz (4.6)), Section 5, or
  Prop. 4.2 as a whole. LWW remains Claimed and unrefereed.
- Twin primes (K = 0) are untouched. Nothing here bears on the twin prime conjecture.

## Role in the chain
- Discharged, conditional on (I1) and (I2): Q_Y − Q_Y^maj = Σ_{d_0}B_{d_0}/d_0 + O(XYL^{-A}) ((4.47)), and hence
  (4.52).
- **First unresolved implication:** the second sum of (4.52), Section 4.8, (4.148)-(4.157), pp. 58-61. It uses
  Prop. 4.5(ii)/(4.96) (stated p. 37, proof pp. 45-46) and the good-state measure bound (4.31) (pp. 21-22).
- Also open:
  - (I1), which could be closed by reading Shiu 1980 or by giving an elementary proof of the weaker
    (X/Y)e^{o(L^{0.1})} bound;
  - pp. 15-16, (4.1)-(4.8).
