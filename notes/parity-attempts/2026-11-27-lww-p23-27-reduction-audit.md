# Audit: route card 2026-11-27-lww-p23-27-reduction.md (LWW Q_Y − Q_Y^maj → (4.52), pp. 16-18, 23-27)

Fresh-context adversarial audit, 2026-11-27. No repository file was edited; this file is new.

## Verdict
- **The mathematics stands.** I re-derived from the printed text, independently of the card:
  - Lemma 4.1, including (4.10) and (4.11);
  - the (4.12) equivalence and the ψ_{-2} insertion;
  - the p. 24 claims (G(P_1) = Db, \overline{f(P)}f(Q) = α_m\overline{α_r}β_n\overline{β_s}, ρ^0 = 1, t ≠ 0,
    primitivity);
  - the bijection behind (4.44), the weight (4.45), the d_0 sum and (4.46);
  - the gcd > 1 removal for Q_Y^maj, the 1 − w bound, (4.50), (4.51) and (4.52).

  I found no error in LWW and no wrong derivation in R1-R7.
- **(I1) and (I2) are the only unproved inputs.** Everything else is elementary or definitional, with one small
  exception: the properties of η (finding 1).
  - (I1) as stated is a correct consequence of Shiu. The bound is (X/φ(ℓ))L^{-1}exp(4Σ_{p≤X, p∤ℓ}1/p) ≪ (X/ℓ)L³,
    uniformly for odd ℓ, with residue −2 coprime to ℓ.
  - The card's claim that only (X/Y)exp(o(L^{1/10})) is needed is right for both of its uses, Lemma 4.1 and (4.50).
- **Every printed formula the card quotes matches the rendered pages.** I checked the bars in (4.7), (4.14),
  (4.21), (4.42), p. 24, B_{d_0} and (4.44); the binomial \binom{J}{2} on p. 26; and the absolute values in (4.52).
  The arXiv abs page lists v1 and v2 only.
- **The script is stronger than the Prop. 4.3 toy was.** The exact chain identity (D) breaks under every mutation I
  tried that changes the mathematics (table below).
- **The problems are in the description of the evidence and in the T-list.** One number is wrong (660 vs 142). T1 has
  no coprime solutions of (4.12), so the indicator half of the chain is exercised only by T2. Two checks are
  tautological. Two T-entries are not terse places, and one terse place is missing.
- Counts: **0 errors, 2 gaps, 3 overstatements, 4 slips** (9 findings).

## Source and reproduction
- PDF: curl into a new empty directory /tmp/claude-0/lww-audit-p23/. SHA-256
  `7ac341311b4a648c32c2b23b3029e1f4a3202258b55614a33ba7e8282423d000` (matches), 895,874 bytes. I ran
  pdftotext -layout and rendered pp. 16-19 and 23-27 (120-160 dpi). PDF page = printed page.
- `/usr/bin/python3 -I code/parity/lww_p23_27_check.py`: 36.0 s. Apart from the timings, the output is identical
  to `lww_p23_27_check.out`: 23 POS / 0 failing, 10 NEG / 10 failing, 0 unexpected.
- Mutations: the toy class (script lines 1-64 and 129-402) was copied to the scratchpad and edited there. Nothing in
  the repository was changed and nothing was committed. Results for the (D) chain identity:

  | Mutation | T1 | T2 |
  |---|---|---|
  | none (baseline) | holds (1.8e-15) | holds |
  | Ω P_1-range lower end 2d_0YM | holds | breaks |
  | Ω P_1-range upper end 8d_0YM | breaks | breaks |
  | bar on β instead of α in (4.42) | breaks | breaks |
  | w excludes only p′_i (not p_{i,J+1}) | breaks | breaks |
  | 1_{d_0≤D<2d_0} dropped | breaks | breaks |
  | ρ-exponent with 2KJ instead of 2K(J+1) | breaks | breaks |
  | kernel c_2(t, b, a) instead of c_2(t, a, b) | breaks | breaks |
  | primitivity filter on positions removed | holds | holds |

  The last row is expected. Under 16Y < Z there are no non-primitive terms, which is exactly the p. 24 claim. The
  NEG with |t| < 960Y shows that the filter matters once that claim fails.
- Count of coprime solutions of bmn − ars = 2(a − b) with η(a/Y)η(b/Y) ≠ 0:
  - T1: **0** (570 solutions with a = b);
  - T2: **16** (8 with |b − a|/Y > 1; 1,740 with a = b).

## Findings

**1. Gap (card, Inputs/"Definitions"; used in R1 and implicitly in (4.7)).** The card lists η as "supported on [1, 4]".
Two further properties are used:
- R1 uses 0 ≤ η ≤ 1.
- The second line of (4.7), as printed with η(a/Y)η(b/Y) and no bar, requires η to be real-valued.

LWW's definition on p. 16 says only "smooth dyadic partition of unity, supported on [1, 4], η^{(j)} ≪_j 1,
Σ_ℓ η(t/2^ℓ) = 1". Realness and 0 ≤ η ≤ 1 are first asserted in passing in the proof of Lemma 4.1 (p. 17). Both are
standard for a partition of unity, so this is harmless, but it is an unlisted assumption. Fix: add "η real,
0 ≤ η ≤ 1 (implicit in 'partition of unity'; asserted p. 17)" to the definitional inputs.

**2. Gap (card, header and "Role in the chain").** The card does not say that (4.47)/(4.52) hold uniformly. Prop. 4.2
feeds (4.8), which sums over v, (M, N) and Y, so it needs uniformity in v, M, N, Y and d_0. This is true: every
implied constant in R1-R7 depends only on K, C, A (through A_0) and the absolute constant of (I1). The "x large"
thresholds (16Y < Z, exp(2L^{a_i}) < Z) depend only on K. Fix: add one line stating the uniformity and what the
constants depend on.

**3. Overstatement (card, header bullet "An exact toy computation (script section (D)) checks the whole chain";
R4 "(D): T1 and T2 ...").** In T1 there are **no** coprime solutions of (4.12) with nonzero η-weight. T1's (D)
identity therefore exercises only:
- the H_{-2}/c_2 half and the gcd > 1 part;
- not the indicator half: the (4.12) converse on actual solutions, and ψ_{-2} = 1 on indicator terms.

T2 has 16 such solutions, and 8 of them have |b − a|/Y > 1. Those 8 are what make the NEG "ψ_1 = 1 only on |u| ≤ 1"
fail, at a margin of about 2e-3 in an identity of size about 8. Fix: say that the indicator half is exercised only
in T2 (16 coprime solutions), and that T1 tests the major-arc half alone.

**4. Overstatement (card, R2 "(B)" bullets and R1 "(A)" bullet; Computation section).**
- The ψ-insertion check over 9.4M pairs tests |b − a| ≤ 4Y for a, b ∈ [Y, 4Y]. That holds by construction
  (|b − a| ≤ 3Y), so it cannot fail. Its NEG (|u| ≤ 2) only shows that 3 > 2.
- (A) compares a toy count with Σ⌊4Y/p⌋², which has 10²-10⁴ slack (45 vs 2,964, ..., 204 vs 3,269,210). Its NEG
  (a linear bound) is a strawman that is not a plausible misreading of LWW.

Neither is wrong, but listing them as "Computed" evidence next to "Proved here" overstates their weight. Fix: call
these arithmetic sanity checks. The substantive computations are (B)'s equivalence test, (C), (C′), (D) and E2.

**5. Overstatement (card, R4 "(D)": "B_{d_0} = ⟨f, T_{-2}^C f⟩, over all states of S(d_0)").** `B_sum` enumerates only
positions P_1 ∈ {g·m} (`supp_positions`), restricted to Ω. That set is brute-force verified to equal supp f only for
T1, in (C′). For T2 the restriction is a proved reduction (f(P) = 0 off that set), not a literal enumeration of
S(d_0). The same holds for Q. This does not weaken the identity, because f(P) = 0 elsewhere. But "computed literally
... over all states" is not what the code does. Fix: "over all states of S(d_0) whose position lies in supp f
(supp f brute-forced for T1 in (C′))". Alternatively, extend (C′) to T2.

**6. Slip (card, R2 "(B)": "39,127 random coprime cases, including 660 solutions of the equation"; the same number
appears in the script's report label).** 660 is the total number of targeted hits. 520 of them have gcd(a, b) > 1
(mostly a = b) and go to the NEG pool. The positive (coprime) test contains **142** equation solutions: 140 from the
targeted loop and 2 from the random loop. I checked this by replaying the script's RNG (seed 20261127). Fix: "...
including 142 coprime solutions of the equation". In the script, count `hits` only when gcd(a, b) = 1, or print
both numbers.

**7. Slip (card, R6, 1 − w bound: "... + J/(p′_iV_i) + J/(p_{i,J+1}V_i) ≪ J²e^{−L^{0.1}}/V_i²").** The last two terms
are ≪ Je^{−L^{0.1}}/V_i, not /V_i². With V_i ≍ 1 (I2) this does not matter. Fix: write ≪_K J²e^{−L^{0.1}} (using
V_i ≫ 1), as LWW do.

**8. Slip (card, T-list: T2, T8 and T13 are inaccurate).**
- **T2.** "a, b ... in [Y, 4Y] ... both are implicit". The range is stated explicitly on p. 16 ("Y ⩽ a ⩽ 4Y since η is
  supported on [1, 4]"). Only oddness is implicit.
- **T8.** This is not a terse place. In the printed (4.44), η(a/Y)η(b/Y) stands inside the Σ_{m,n,r,s} display, after
  the brace. So "the sum over m, n, r, s in (4.44)" includes it as printed.
- **T13.** This misdescribes LWW. They do not use 1 − ∏w_i ≤ Σ(1 − w_i). They take a union bound directly on the
  product space: "the prime tuples excluded from w(a, b) satisfy, for some i, j, either ...". Each event has weight
  equal to the corresponding term, because the other factors sum to 1. That argument is complete as printed.

Fix: reword T2 to "oddness implicit"; turn T8 into a reading note; drop T13 (or turn it into a remark that the
card's route differs). This gives 11 terse places.

**9. Slip (card, T-list is missing one terse place).** (4.50) is stated in the form bmn − ars = 2(a − b) and is
proved "by applying the Cauchy–Schwarz inequality and (4.9)" (p. 26). To apply (4.9), one first has to go back
through the converse of (4.12) to the h-form mn + 2 = ah, rs + 2 = bh. This is valid because gcd(a, b) = 1. Only then
does (4.10) apply per pair. The card does this correctly in R6(a) but does not list it as a terse place. Fix: add
"T14 (p. 26, (4.50)): uses the (4.12) converse (coprime pairs) to return to the h-parametrisation before (4.9)/(4.10)".

## What I checked and found correct (no finding)
- **R1.** Injectivity of tuple ↦ a uses the disjointness of the P_i. The count is ≤ ⌊4Y/p⌋², and
  Σ_{p>e^{L^{0.1}}}p^{-2} ≪ e^{−L^{0.1}}. The per-pair bound is XL^{4C+3}/Y with h ≤ (4X + 2)/Y. The final bound
  XYe^{−L^{1/20}} is correct (S2 is a fair remark).
- **R2.** Both directions of (4.12) and the role of gcd(a, b) = 1 are right; the NEG 459/21,533 is genuine. The
  insertion ψ_{-2}(t/Y) = ψ_1((b − a)/Y) = 1 holds for every term, coprime or not. The signs of (4.13) and (4.38)
  agree.
- **R3 (p. 24).**
  - f(P) = \overline{α_m}β_s, f(Q) = \overline{α_r}β_n, and \overline{f(P)}f(Q) equals the summand of (4.7) and
    (4.14).
  - The convention of (4.21), with the bar on the first slot, matches B_{d_0} as printed on p. 25.
  - ρ-exponent 0; oddness; Ω-membership (open bounds).
  - t ≠ 0, via gcd(b, ars) = 1 and b > 1.
  - Primitivity, via p > Z > 16Y > |t|. This uses 16Y ≤ 16exp(2KL^{0.2}) < Z = exp(L^{0.24}). The card's
    |t| ≤ 6Y / < 16Y split is right (T4).
- **R4.**
  - det(P, Q) = D(bmn − ars).
  - The weight σ·∏V_i^{-1}·(d_0/D)/d_0 = D^{-1}∏V_i^{-(J+2)}, which is (4.45).
  - Σ_{ℓ_0}1_{2^{ℓ_0}≤D<2^{ℓ_0+1}} = 1.
  - gcd(a, b) = 1 is automatic, and (p′, p_{·,J+1}) ↔ (a, b) is a bijection (T9).
  - ψ_{-2} disappears on the indicator (T7).
- **R5.** meas M_{-2} = meas M_1 ≤ Σ_{k≤L^{A_0}}φ(k)·4L^{A_0}/Y ≤ 4L^{3A_0}/Y, and the support is |t| < 16Y. The
  per-pair bound of (4.51) does not use coprimality, so it times (4.11) disposes of the gcd > 1 part of Q_Y^maj (T10).
- **R6.**
  - The 1 − w bound term by term (\binom{J}{2} coincidence pairs; J positions for each of p′_i, p_{i,J+1}).
  - τ² ≤ τ_4, via (k + 1)² ≤ \binom{k+3}{3}.
  - Σ_{n≤x}τ_4(n) ≤ x(1 + log x)³.
  - ≤ 32 (the card says ≤ 33) values of l per k and of k per l. T11 is right that LWW state only one direction.
  - The total power 4C + 3 + 3A_0 is absorbed by e^{−L^{0.1}} (S3).
- **R7.** (4.52) as printed has |Q_Y − Q_Y^maj| on the left and absolute values on both sums.
- **Other T-entries.** T1, T3-T7, T9-T12 and S1-S3 are accurate. On T1, I also could not reconstruct the middle "≤"
  of (4.9) as an exact inequality with the printed ranges. Since the ranges carry implicit constants, I record no
  finding.
- **(I1)** via Shiu, as above. **(I2)** is used only as V_i ≫ 1, i.e. ∏V_i^{-2} ≪_K 1 and V_i^{-1} ≪ 1 in the 1 − w
  bound.
- **Script.**
  - (C) evaluates f from (4.42) by factorisation (G, μ², ω_i). Its NEGs (no bar; support 960Y) are meaningful: the
    second exhibits 18,144 non-primitive terms.
  - (D)'s identities hold to 6.9e-18 and 1.8e-15. They break under all seven substantive mutations above, including
    two the card did not try: narrowing Ω, and the bar on β.
  - E2's near-tight bound and its J → 1 NEG are as described.
  - (F) is exact.
  - The card's reported numbers (46; 2,196; 10,081; 12/20; 0.01269/0.01274; max 32; 36 s) all match.
- **Chain pointers.** Section 4.8 is (4.148)-(4.157), pp. 58-61. (4.96) is stated on p. 37 and proved on pp. 45-46.
  (4.31) is on p. 22, and p. 60 cites it.

## Fixes needed for the card (summary)
1. Inputs: add "η real, 0 ≤ η ≤ 1".
2. Header/Role: state uniformity in v, M, N, Y, d_0, and that the constants depend only on K, C, A, (I1).
3. R4 (D): say that T1 has 0 coprime solutions of (4.12), so the indicator half is exercised only in T2 (16
   solutions, 8 with |b − a| > Y).
4. R1 (A), R2 (B): relabel the ψ-insertion check and (A) as arithmetic sanity checks.
5. R4 (D): "over all states of S(d_0) with position in supp f" (or brute-force supp f for T2).
6. R2 (B): 660 → 142 coprime solutions, and fix the script label to count coprime hits.
7. R6: J/(p′V_i) is ≪ Je^{−L^{0.1}}/V_i; write ≪_K J²e^{−L^{0.1}}.
8. T-list: T2 → "oddness implicit"; T8 → reading note; T13 → drop (LWW's union bound on the product space is
   complete).
9. T-list: add T14 for (4.50), which returns to the h-form via the (4.12) converse before applying (4.9).
