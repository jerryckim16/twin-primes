# Rung 182: source transcription for the tail term E_{H_C^c} (and E_{C^c})

Source [M]: GPT-6 Astra (OpenAI), prompted by R. Sharifi, "A fixed-profile proof for prime gaps of at most 182",
main paper = PDF pp. 1-52 of https://www.math.ucla.edu/~sharifi/AI/prime_gaps_182_expository_bundle.pdf.
Fetched 15 Nov 2026 with plain curl into a new empty scratch directory: HTTP 200, 17271479 bytes, SHA-256
5362e977880af92a73a79b411a9c66daf0b93af4ec0ed6bec320090386f4b881. This is the same hash as in notes/sources-182.md
(same file). It was read with `pdftotext -layout` and `-raw` (pp. 1-52 only). Nothing in it was executed.
The printed page numbers are the PDF page numbers.

Conventions here:
- "Q:" means verbatim text, apart from the math glyphs, which are rewritten in ASCII/LaTeX-ish form.
- "[transcribed]" means a displayed formula rebuilt from a layout where the sub/superscripts are split over several
  lines. I checked these against `-raw`.
- "[garbled]" means the extraction cannot be trusted at that point.
- "Mine:" means my own remark or calculation. It is not from the source.
- Status of everything here: **Claimed** (read from source). Nothing was checked except where it says CHECKED.

## 1. Where the tail enters

- **(7.4), p. 32, Sec. 7.6 "The cap form and its enclosure".**
  - Q: "Replace L0, L1, C in (6.7) by H0, H1, H_C, keeping the same F, K, ell. Write the resulting face forms as
    J_{0,H}, J_{+,H}, E_{H_C^c}. The cap quotient is"
        q_H = rho* (J_{0,H} + (1 - ell) J_{+,H} - d_h E_{H_C^c}) / I(F).                      (7.4)
  - The extraction renders the subscript as "E_{H^c}" with a stray "C" on the next line [garbled]. The `-raw` text
    and the sentence before the display give E_{H_C^c}.
  - Q (p. 32, after (7.6)): "For a positive lower quotient bound the positive numerator terms use their lower
    endpoints, the negative term uses its upper endpoint, and the denominator is I+."
  - So the certificate needs an **upper** bound for E_{H_C^c}(F)/𝒩.
- **(6.7), p. 28, Sec. 6.3.**
      𝒥(U) = J0(U) + (1 - ell) J+(U) - d_h E_{C^c}(U),                                         (6.7)
  - Q: "where the three quantities are the sums of J_{0,i}, J_{+,i}, E_i^tail."
  - The sum is over the detected coordinates i = 1..39.
- **Prop. 6.1 (Tail hybrid), p. 28.**
  - Q: "Put J_{0,i} = ||V0||^2, J_{+,i} = ||v||^2, E_i^tail = int_{C^c} K |V|^2 dnu^{k-1}."
  - Then, [transcribed]:
        liminf_{x->inf} M_x(1_P A^2) >= J_{0,i} + ( sqrt(J_{+,i}) - sqrt(kappa_true E_i^tail) )_+^2.   (6.5)
  - Proof, in substance: pointwise 1_P (A - B0 - B_H)^2 >= 0. Cauchy-Schwarz with weight b_x and then (5.8) bound
    the cross term below by -2 sqrt(kappa_true E_i^tail) ||H||. Then take H = alpha v with
    alpha = (1 - sqrt(kappa_true E_i^tail / J_{+,i}))_+.
- **(6.6), p. 28.**
      ( sqrt u - sqrt v )_+^2 >= (1 - ell) u - (1/ell - 1) v,   u, v >= 0,  0 < ell < 1.          (6.6)
  - Q: "Replace kappa_true by its upper bound kappa-bar in the negative term and set d_h = kappa-bar (1/ell - 1)."
  - In the extraction the bar is misplaced, as "𝜅(1/ℓ ̄ − 1)" [garbled]. The notation table, p. 46, confirms
    "K, ell, d_h: Exceptional step kernel, fixed hybrid parameter, and kappa-bar(1/ell - 1)".
- **Operator form, (8.1)-(8.2), p. 33.**
      a_H = ell 1_{H0} + (1 - ell) 1_{H1} + d_h K 1_{H_C} - d_h K,                            (8.1)
      a   = ell 1_{L0} + (1 - ell) 1_{L1} + d_h K 1_{C}   - d_h K.                            (8.2)
  - Q: "Thus a_H is 1 on H0, 1 - ell on H1 \ H0, zero on H_C \ H1, and -d_h K outside H_C."
  - So the tail is the region where a_H = -d_h K. Each E_i^tail is K-weighted and integrates |E_i F|^2 over the
    complement of H_C.
  - (8.3): eps_h = kappa-bar(1/.0108 - 1) 2.194 uses the bound (5.7) on K.

## 2. Objects used by the tail

### 2.1 V, the complement, C and H_C

- **Sec. 6.1, p. 27.**
  - Q: "Fix a detected coordinate i, an arithmetically allowed profile U supported on O, and write
    V = E_i U, V0 = 1_{L0} V, v = 1_{L1 \ L0} V, V_C = 1_C V, g = 1_{C^c} V."
  - Q: "**Complements are taken in the retained-root ambient space. They are not new independently capped
    domains.**"
  - Sec. 6.2, p. 28: T_i = A^0_i - B_C, where A^0_i is the exact erased sum. Q: "Its limiting profile is g."
    Q: "No square B_C^2 is evaluated by a distribution theorem. Its contribution inside T_i is instead included in
    the positive exceptional bound (5.8)."
  - Mine: this explains why the tail is the full face profile |E_i U|^2 on C^c, weighted by K, with no
    distribution input.
- **Erasure, (2.6), p. 8.** (E_i F)(X̂_i) = int F(X_1, ..., X_{i-1}, X, X_{i+1}, ..., X_k) dnu(X).
  - Q: "Erasure is an integral, not a conditional expectation."
  - (2.7): J_i(F) = int |E_i F|^2 dnu^{k-1}.
  - (2.8) writes out the square: the two erased coordinates X, X' are independent and Y is shared.
- **Measure, (2.1), p. 7.** nu_zeta = e^{gamma_E} zeta Law(Pi_zeta). Pi_zeta is the Poisson process of intensity
  du/u on (0, zeta]. The total mass is e^{gamma_E} zeta, so it is not a probability measure.
  - (2.3), p. 7: the image of nu under X -> |X| is rho_D(t/zeta) dt.
  - (2.4), p. 8: nu_zeta restricted to {max X <= c} is nu_c.
  - Q: "integration on a cap c uses rho_D(t/c) dt."
  - zeta = .17277/rho (p. 29). Lean: trialPrimeCap = 172770/262499.
- **Subtraction domain C, (3.12), p. 15:** C = H_C ∩ C^raw_14.
  - (3.18), p. 17: C^raw_14 = {s <= S_C, M0 <= zeta} ∩ Q(a_C, xi_C, a_C + xi_C).
  - (3.17), p. 17: S_C = B0 - b14 - eps_r/rho* and sigma0 = .100001, with omega_C, delta_C and xi_C = delta_C/rho as
    displayed there. Q: ".2607860319243 < rho* S_C < .2607860319244".
  - Inclusions L0 ⊂ L1 ⊂ C (p. 15) and H0 ⊂ H1 ⊂ H_C (p. 30).
  - Mine: C ⊂ H_C gives C^c ⊃ H_C^c, so E_{C^c}(U) >= E_{H_C^c}(U). The arithmetic tail is the larger one. Its
    excess is absorbed by the restoration step through a_H - a >= 0, D >= 0 (p. 33) and the inner "C: low" source
    family (Sec. 10 table, p. 40: 7 components, contribution 9.828292827 to b).
- **Cap domain H_C, Sec. 7.2 table, p. 30** (d = 38 retained coordinates). r is the sum of the 38 retained cell
  indices j = floor(|Y_l|/h), and M0 is the largest fragment among all coordinates:

  | rows r       | cap c on M0 (units h) |
  |--------------|-----------------------|
  | 0 : 352698   | 246256                |
  | 352699 : 371671 | 186491             |

  - Q: "Outside the listed ranges the domain is empty."
  - Hence, on the support of E_i F, H_C^c = {r' >= 371672} ∪ {352699 <= r' <= 371671 and M0(Y) > 186491h}.
    (On r' <= 352698 the support of E_i F already forces M0(Y) <= 246256h.)
  - Lean: trialShells index 3 ("subtraction C"):
    - [0, u1) with cap 21229937030597/32255864832000 = 246256h;
    - [u1, trialSubtractionRadius) with cap 257240737234297/516093837312000 = 186491h;
    - trialSubtractionRadius = 284210047725358090299910326697/286076767019837125756522770000 (= S_C).
  - CHECKED HERE: with the shell rule lower <= (r + 38)h < upper (the whole-cell upper total s+ of p. 29), these
    give the last rows 352698 and 371671 exactly. rho* x trialSubtractionRadius = 0.26078603192436, which matches
    (3.17).

### 2.2 The kernel K (Sec. 5, pp. 23-27)

- **Hinge, Sec. 5.1, p. 23.** w_t(s) = (12/5)(s - t)_+ / (2/5 - t), with t = .38.
  - Lean: trialHingeThreshold = 19/50.
  - (5.1), p. 24: b_x(n) <= sum over p < q with pq | n, p, q > x^lambda and pq < x^a of w_t(log_x(pq)).
- **Root radius, Sec. 5.2, p. 24.**
  - Q: "For a retained configuration Y, let q(Y) = rho* sum_{j != i} |Y_j|."
  - The largest value is r_c = rho* S = .2758746934.
  - (5.2): z_j(q) = min{lambda - eps0, (1 - s_j)/2 - q - eps0}, eps0 = 10^-4.
  - Q: "(1 - a)/2 - r_c - eps0 = .0172203066 > 0".
  - lambda = 1 - 2a = .17278 (Sec. 4, (4.1) area, p. 19) and a = .41361.
  - Lean: trialRoughness = 8639/50000 = lambda, trialMinorantA = 41361/100000, trialAuxiliaryRetreat = 1/10000.
  - **NB:** Lean `trialLambda` = 6308693370963335/576460752303423488 is **ell**, not the paper's lambda.
- **Continuous kernel, (5.4), p. 26** [transcribed]:
      K_t(q) = 12/(5(2/5 - t)) int_t^a (s - t) log((s - lambda)/lambda) / (s min{lambda, (1 - s)/2 - q}) ds.   (5.4)
  - Q: "There is no additional factor of two: the density already counts unordered pairs."
  - It is not used numerically. Q: "The finite calculation below instead retains the fixed retreat eps0 = 10^-4;
    its kernel is correspondingly larger."
- **Step kernel, Sec. 5.4, p. 26, verbatim apart from glyphs:**
  - Q: "Partition the whole interval [2 lambda, a] into 1024 equal bins, with upper endpoints s_j. Set
    L21(v) = sum_{m=1}^{21} (-1)^{m+1} v^m / m, v_j = (s_j - 2 lambda)/lambda.
    Here 0 <= v_j < 1, so the odd alternating sum bounds log(1 + v_j) above. Round the following nonnegative
    quantity upward to a multiple of 10^-25:
        W_j^+ >= (s_j - s_{j-1}) (w_t(s_j)/s_j) L21(v_j).                                    (5.5)
    The weight is zero below the hinge except possibly on the bin straddling it, where an upper-endpoint bound is
    used."
  - Q: "For the fine grid in Section 7, put n0 = N - k. Divide retained sum indices into blocks of length
    ceil(n0/512) = 768. If the last index in a block is r_max, use the physical upper total
    q+ = rho*(r_max + k - 1)h. The value of K on that entire block is
        K = sum_{j=1}^{1024} W_j^+ / z_j(q+).                                                (5.6)
    The numerator rounding, auxiliary retreat and upper total all act in the direction of an upper bound. They give
        0 <= K <= 2.194                                                                      (5.7)
    on the whole retained domain. The same K is used in the cap form and in all restoration terms."
  - Lean: trialPairBins = 1024 and trialRadialBlocks = 512 (code/data182/TrialData182_part1.lean, lines 29-30).
    The W_j^+ and the per-block K values are **not** in our data files. Per Appendix B they are in
    formal/SourceKernels182.lean, which we do not have.
- **(5.8), p. 27.**
      limsup (1/𝔓_x) sum_{x<=n<=2x, n ≡ b0 (W)} b_x(n + h_i) B_H(n)^2 <= int K(q(Y)) |H(Y)|^2 dnu^{k-1}(Y).   (5.8)
  - Q: "All cross terms of the finite combination are included in its square."

### 2.3 Parameters

- **kappa-bar, (4.3), p. 21:** 46653544162031/500000000000000000 (Lean trialKappa).
  - kappa_true lies in (.000093307088324061, .000093307088324062) (4.2).
  - Lean Sec. 13.3, p. 45, uses instead kappa_cvx = 11696/125000000 via 𝒥cvx = 𝒥 - xi_add J+.
  - Q: "𝒥cvx uses the coefficient d_h and tail kernel of 𝒥". So the tail term is the same in both.
- **ell, (6.8), p. 28:** 6308693370963335/576460752303423488, with .0108 <= ell <= .0112. Lean: trialLambda.
- **d_h** = kappa-bar(1/ell - 1). Mine: = 0.0084326857231...
- **Normalization, Sec. 7.5, pp. 31-32.**
  - g_j = g((j + 1/2)h), Z = sum_{j<n0} g_j^2, 𝒩 = (hZ)^39.
  - Q: "Every quadratic form reported by the certificate, including a form with 38 retained coordinates, is divided
    by the same positive number 𝒩."
  - Cell mass: w_c(j) = int_{jh}^{(j+1)h} rho_D(t/c) dt. The root law has weights g_j^2 w_c(j)/(Z h).
  - Q: "In a face square there are 38 retained integrations and two erased integrations. After division by 𝒩, the
    sum over symmetric detected coordinates has the prefactor 39h/Z."
  - The grid (7.1), p. 29: k = 39, N = 393216, n0 = 393177, S = 1379373467/1312494500, h = S/N, and
    rho* = 2624989/10^7. Cell convention p. 29: t°_i = (j_i + 1/2)h, s° = (r + d/2)h, s+ = (r + d)h.
  - Q: "its support tests use the actual fragments and the whole-cell upper total."
  - The profile F is (7.3), p. 31; see notes/sources-182.md Sec. 4.

## 3. The published bound for the tail

- **[M] prints no number for E_{H_C^c}.** It prints only I- and I+ (7.5) and mu- (7.6).
- The value is in the Lean trial data, code/data182/TrialData182_part1.lean, line 110:
      def trialTailUpper : ℚ := (456062981993534172355663419289051290598102957656988886599 /
                                 862718293348820473429344482784628181556388621521298319395315527974912)
  - Mine: this is 5.286348805972699e-13.
  - It is presumably E_{H_C^c}(F)/𝒩 with the sum over i included. The consistency check below supports this
    reading.
  - The companions, in the same file:
    - trialJ0Lower = 5.636459089698676e-11
    - trialJPlusLower = 4.0824074296431434e-13
    - trialDenominatorLower/Upper are I-/I+ of (7.5).
- CHECKED HERE (exact Fractions): rho*(J0lo + (1 - ell)J+lo - d_h TailUp)/I+ - 1 = 2.766919373335e-4. This is
  >= mu- = 9968877639291/2^55 = 2.766919371203e-4, i.e. consistent with (7.6). The same check is already in
  code/data182/qH_check.json.
- The five "cap inequalities" of Appendix B.1 (p. 47) are presumably I-, I+, J0 lower, J+ lower and tail upper.
  This is a guess.
- **Size of the tail.**
  - d_h TailUp = 4.458e-15.
  - rho* d_h TailUp / I+ = **7.855e-5** of q_H. Compare mu- = 2.767e-4 and the final margin (10.3) mu- - L-bar =
    6.521e-5.
  - Mine: the theorem survives a tail up to about 1.83x the published upper bound (6.521e-5/7.855e-5 = 0.83 extra),
    if nothing else changes.
  - The tail is about 1.29 x J+ and about 0.94% of J0.

## 4. How [M] says the tail is computed or bounded

- Only generic statements are made. There is no tail-specific algorithm in the PDF.
  - Sec. 10.3, p. 41. Q: "The coordinate-kernel and directed-contraction methods are developed in [18, Sections
    2.1-2.3]." [18] is the OpenAI 186 companion.
  - Q: "The real-ball arithmetic uses Arb's enclosure operations [12, Sections 2-3]".
  - Q: "The cap integrals use interval arithmetic, exact rational spline pieces, and exact Dickman logarithm and
    dilogarithm primitives on 0 <= u <= 3. The largest Dickman argument in this trial is 393177/140306 < 3."
  - Q: "There are two independent scalar implementations. ... The fast scalar checks do not repeat those long
    integrations." The integration records are "supplied by the digital supplement" (romyar1/prime-gaps-lean,
    release external-numerics-20260909). We do not have it.
- K is a step function, constant on 768-index blocks of the retained sum r' (5.6). So the tail is a cap face form
  of the same contraction type as J0 and J+, with a block-constant weight. This is what makes it computable by the
  same pipeline (Mine).
- Sec. 11, p. 41, lists "upper step kernel" among the finitely many boundary types (cell totals, spline knots,
  activation levels, tail bounds, largest-fragment caps).
  - Q: "The fixed K is bounded, so the exceptional energies converge as well."

## Helper's plan (not from the source)

Goal: a rigorous arb ball for T := E_{H_C^c}(F)/𝒩 = sum_i int_{H_C^c} K |E_i F|^2 dnu^38 / (hZ)^39, to be compared with
trialTailUpper. The ball's upper end should be <= trialTailUpper; with a correct reading it should be slightly below
it, as J0 and J+ are just above their published lower bounds.

**1. Kernel table (exact, seconds).**
- Compute W_j^+ = ceil(10^25 x (5.5))/10^25 in fmpq, for j = 1..1024:
  - s_j = 2 lambda + j(a - 2 lambda)/1024, with lambda = 8639/50000, a = 41361/100000 and t = 19/50;
  - w_t is evaluated at the upper endpoint s_j.
- For block b = floor(r'/768): K_b = sum_j W_j^+ / z_j(q+_b), with q+_b = rho*(min(768b + 767, n0 - 1) + 38)h and
  z_j(q) = min(lambda - 1e-4, (1 - s_j)/2 - q - 1e-4).
- Prototype: a 30-line Fractions script, kept in my scratchpad as kernel.py, not in the repo. Results:
  - 506 of the 1024 W_j are nonzero (the bins above the hinge .38), sum W = 0.0478156;
  - K = 0.27690 on the low blocks, 0.9542 at block 459 (where the tail starts, r' = 352699), 1.2892 at block 483
    and 2.19354 on the last block;
  - **(5.7) holds only if r_max on the last block is n0 - 1 = 393176.** With the nominal r_max = 768 x 512 - 1 =
    393215, the last block gives K = 2.19637 > 2.194. That resolves ambiguity (a) below.

**2. Masks and layers.**
- Only the H_C caps, the component caps and the outer caps matter. The tail layer set is
  B_T = {141720, 177528, 186253, 186491, 196608, 246256} (6 values, against 9 for J). The base and enlarged face
  caps do not enter the tail mask, so they need not be layer boundaries.
- On layer a (M0(Y) in (b_{a-1}, b_a]): chi_{T,a}(r') = 1 - [capC(r') >= b_a], where capC = 246256 on 0..352698,
  186491 on 352699..371671 and 0 above.
  - Get capC with `rows_of(X["shells"][3], 38, ...)` from code/sharifi182_check2_J.py and assert it equals the
    table.
- chi_T vanishes for r' <= 352698. The contraction therefore runs only over r' in [352699, 393176], about 40k rows.

**3. Reuse code/sharifi182_check2_J.py (imports check2).**
- Make a copy, sharifi182_check2_tail.py, rather than editing it.
- Setup: use BV = B_T and add the mask capC.
- marginal(la): unchanged. It already gives v^a_tau(r') for all r'. A' <= 393176 - r' <= 40477 could be exploited,
  but it is not needed.
- moments(b): unchanged. This is the same 38-fold y-series moment polynomial of length n, i.e. the expensive part.
- contract: one mask, with row weight K_{floor(r'/768)} (an exact fmpq turned into an arb) multiplying q*ml[r].
  Then layers a and a+1 with signs +/-, and the same factor 39h/Z.
- run_cap(b) per b in B_T. Then combine and compare ball_upper against trialTailUpper.
- Extend the selftest with brute force:
  - k = 3, 48-cell grid; give 186491 an artificial test cap, e.g. 24, between 186253 -> 23 and 196608 -> 25 in the
    existing tcaps map;
  - use an artificial block-constant K (e.g. block length 4, distinct rational values);
  - add the term K(r') [not in H_C] to the brute-force loop of selftest().
- Optional: a cheap consistency check is the unweighted tail mass M_T (K = 1). It must satisfy
  K_459 M_T <= T <= K_511 M_T.

**4. Cost (4 cores, 15 GB; another helper currently uses about 7 GB).**
- The existing check2_J caps took 1250-1450 s and about 3.5 GB each at prec 128. That time is dominated by moments.
- The tail has 6 caps, roughly 6 x 1400 s = 2.3 h serial, or about 1.2 h with 2 parallel workers (7 GB).
  - Running 4 workers (14 GB) is not safe while the other job runs.
  - The kernel table is negligible, and the contraction over 40k rows is cheaper than in J.
- Cheaper alternative: add the tail mask as a third output in check2_J's contract, with 186491 added to its BV, so
  that J and the tail come from one pass. But that means 10 caps (about 3.9 h serial) and re-running J. It is only
  worth it if J is re-run anyway.
- Program 1 (sharifi182_J.py, GMP fixed point) could get the same one-mask extension, as a non-rigorous second
  value.

**5. Ambiguities in the source (each to be tested or recorded).**
- (a) The last block's r_max: 393176 (= n0 - 1) or 393215. This is resolved by (5.7), see step 1; use n0 - 1.
  Blocks are assumed to start at r' = 0, i.e. [768b, 768b + 767]. The text says only "Divide retained sum indices
  into blocks of length 768".
- (b) "Round ... upward to a multiple of 10^-25" with "W_j^+ >=". I assume ceil of the exact rational (5.5). Any
  larger W is still valid, but it would shift T by at most about 1024 x 1e-25/0.017 relative to K ~ 1, i.e. it is
  negligible.
- (c) "Retained sum index" is read as r' = sum of the 38 retained cell indices. This is consistent with
  q+ = rho*(r_max + k - 1)h = rho* s+ for d = 38. K uses the block of r', not the actual q(Y), which is the upper
  direction.
- (d) The complement is "in the retained-root ambient space" (p. 27). I read this as all 38-coordinate Y outside
  H_C. Since E_i F = 0 off the projection of H_O, only the rows above matter.
- (e) That trialTailUpper is E_{H_C^c}/𝒩 summed over i (prefactor 39h/Z), in the same normalization as
  trialJ0Lower. This is supported by the (7.6) consistency check, but it is not stated in the PDF.
- (f) The hinge bin straddling t = .38 uses w_t(s_j) at the upper endpoint, as stated in (5.5).
- (g) The cap form uses the same F (7.3), including the three cap components summed before squaring. The outer
  support is H_O; the E_i F marginal is the same as for J.
- (h) Lean `trialLambda` is ell, and `trialRoughness` is the paper's lambda. Do not confuse them.
- (i) The actual (non-cap) tail E_{C^c}(PF) is never computed by itself. It enters only through the restoration
  bound b (Sec. 8). So a cap-only recomputation checks the trialTailUpper premise and nothing about C^raw_14.
