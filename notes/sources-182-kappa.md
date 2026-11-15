# Rung 182: source transcription for the mass deficit kappa_true (Sec. 4.4-4.5, Sec. 13.3)

Source [M]: GPT-6 Astra (OpenAI), prompted by R. Sharifi, "A fixed-profile proof for prime gaps of at most 182",
main paper = PDF pp. 1-52 of https://www.math.ucla.edu/~sharifi/AI/prime_gaps_182_expository_bundle.pdf.
Fetched 15 Nov 2026 with plain curl into a new empty directory /tmp/claude-0/k182: 17271479 bytes, SHA-256
5362e977880af92a73a79b411a9c66daf0b93af4ec0ed6bec320090386f4b881. This matches notes/sources-182.md (same file).
It was read with `pdftotext -layout` and `-raw` (pp. 1-52). Nothing in it was executed.
The page numbers are the printed page numbers, which equal the PDF page numbers.

Conventions:
- "Q:" means verbatim text. The math glyphs are rewritten in ASCII/LaTeX-ish form.
- "[transcribed]" means a display rebuilt from split sub/superscripts. I cross-checked these against `-raw`.
- "[garbled]" means the extraction is unreliable at that point.
- "Mine:" means my own remark.
- Status: everything here is **Claimed** (read only). The checks are in notes/kappa-182-report.md (**Computed**).

## 1. The support and the coefficient 24 (Sec. 4.1-4.2, pp. 19-20)

- Q (p. 19): "Set lambda = 1 - 2a = .17278. On x <= n <= 2x, let S5(a; x) consist of products of five distinct
  primes such that every pair product is less than x^a. Equivalently, order the primes decreasingly and require
  only p1 p2 < x^a."
- (4.1), p. 19 [transcribed; the extraction prints "241𝒮5(𝑎;𝑥)", which is 24 * 1_{S5(a;x)}]:
      rho_x(n) = 1_P(n) - b_x(n),   b_x(n) = 24 * 1_{S5(a;x)}(n).                                     (4.1)
- Q (p. 20): "For a fixed set of five distinct primes, B1 has four labelings: p4 is the smallest, p5 can be any of
  the other four, and the other labels are then ordered. The count B2 has twenty labelings [...] Therefore
  (B1 + B2) 1_squarefree = 24 1_{S5(a;x)}."
  - Mine: a brute force over permutations in the selftest gives 4 and 20 (**Computed**).
- a = .41361 is from (3.5), p. 12 (see notes/sources-182.md).

## 2. Definition (4.2), p. 20-21 [transcribed]

- Q (p. 20): "Its exact limiting deficit has a simple integral description. Let
      P_a = {(alpha_1, ..., alpha_4) : alpha_1 > ... > alpha_5 > 0,  alpha_5 = 1 - sum_{j=1}^4 alpha_j,
             alpha_1 + alpha_2 < a}."
- Q (p. 21): "Then
      kappa_true = 24 int_{P_a} d alpha_1 d alpha_2 d alpha_3 d alpha_4 / (alpha_1 alpha_2 alpha_3 alpha_4 alpha_5)."   (4.2)
- Q (p. 21): "The inequalities force alpha_i >= lambda on the closure of the region, so there is no singularity at a
  zero prime exponent. [...] This gives sum_{x<=n<=2x} rho_x(n) = (1 - kappa_true + o(1)) x / log x. The ordering in
  P_a counts a distinct factorization once. The factor 24 is the multiplicity just proved."
- Q (p. 21): "Exact polytope integration with outward rational bounds gives
      .000093307088324061 < kappa_true < .000093307088324062."
- (4.3), p. 21: Q: "The proof uses the convenient upper bound
      kappa-bar = 46653544162031 / 500000000000000000."                                              (4.3)
  - Mine: this is exactly .000093307088324062, the printed upper end.
- Constants: Q: "a = .41361" ((3.5)); u = a - 2/5 = 1361/100000 (p. 21, below).
- Mine: the integrand and the measure are the standard ones for counting products of five ordered primes
  (x/log x) * int d alpha_1..d alpha_4 / (alpha_1...alpha_5). The domain has no individual caps; Q (p. 20): "the original
  individual caps and triple conditions are automatic on the residual set."

## 3. The paper's route, Sec. 4.5, pp. 21-23

- (4.4), p. 21. Q: "Let kappa_{5,1} denote the limiting mass of the first labeled error E1. On the hyperplane
  sum_i alpha_i = 1, its two pair constraints are alpha_1 + alpha_2 < a and alpha_1 + alpha_5 < a [...]. Thus this
  limiting region is exactly four labeled copies of the ordered region in (4.2). [...] Hence
      kappa_true = 6 kappa_{5,1}."                                                                   (4.4)
  - The extraction prints "𝜅𝑚𝑡𝑟𝑢𝑒" here and in (4.6) and (4.11) [garbled]. From context and from (4.2) it is
    kappa_true. The stray "m" is an artefact of the math-italic subscript.
- Change of variables. Q: "Put u = a - 2/5 = 1361/100000, alpha_i = 1/5 + u z_i, z5 = -z1 - z2 - z3 - z4. The
  closure of the first labeled region becomes the fixed polytope P_E in R^4 defined by
      z_i >= -2 (1 <= i <= 5),  z1 >= z2 >= z3 >= z4,
      z1 + z2 + z3 + 2 z4 <= 0,  z1 + z2 <= 1,  z2 + z3 + z4 >= -1."                                     (4.5)
- (4.6), p. 21 [transcribed]:
      kappa_true = 6 u^4 int_{P_E} dz1 dz2 dz3 dz4 / prod_{i=1}^5 (1/5 + u z_i).                       (4.6)
  - Q (p. 22): "The factor u^4 is the coordinate Jacobian. There is no additional factor 5!, or Euclidean
    hyperplane-area factor."
- Vertex table, p. 22 (identical in -layout and -raw):

      j   v_j
      0   (-1/3, -1/3, -1/3, -1/3)
      1   (0, 0, 0, 0)
      2   (1/2, 1/2, -3/4, -3/4)
      3   (1/2, 1/2, -1/3, -1/3)
      4   (1/2, 1/2, 1/2, -2)
      5   (1/2, 1/2, 1/2, -3/4)
      6   (4/3, -1/3, -1/3, -1/3)

- Q: "and a triangulation is Sigma1 = (0, 1, 3, 5, 6), Sigma2 = (0, 2, 3, 5, 6), Sigma3 = (0, 2, 4, 5, 6). One way to
  check the partition is to cut P_E by z3 + 2z4 = -1 and z2 + 2z4 = -1. [...] z3 + 2z4 >= -1,
  z3 + 2z4 <= -1 <= z2 + 2z4, z2 + 2z4 <= -1."
- (4.7), p. 22 [transcribed]:
      V1 = 125/5184,  V2 = 625/20736,  V3 = 625/6912,  sum_j V_j = 125/864.                           (4.7)
- (4.8), p. 22 [transcribed; the extraction prints "55", which is 5^5]:
      prod_{i=1}^5 (1/5 + u z_i)^{-1} = 5^5 prod_i (1 - v B_i)^{-1} = 5^5 sum_{n>=0} v^n h_n(B_1, ..., B_5),   (4.8)
  - Here B_i(t) = -12 z_i(t) (integer coefficients in the barycentric coordinates t0..t4) and v = 5u/12.
  - The recurrence is H_{i,n} = H_{i-1,n} + B_i H_{i,n-1}, H_{i,0} = 1, H_{0,n} = 0 (n > 0), h_n = H_{5,n}.
- (4.9) [transcribed]:
      E_Sigma[t0^{b0} ... t4^{b4}] = 4! prod_j b_j! / (n + 4)!,   sum_j b_j = n.                       (4.9)
- r_Sigma = 5u max over vertices of max_i |z_i|. Q (p. 23): "r_Sigma1 = r_Sigma2 = 1361/15000, r_Sigma3 = 1361/10000."
- (4.10) [transcribed]:
      T_D(r) = 1/(1 - r)^5 - sum_{n=0}^D binom(n+4, 4) r^n.                                           (4.10)
- A_Sigma = sum_{n=0}^{22} v^n E_Sigma[h_n(B_1, ..., B_5)].
- (4.11) [transcribed; again "55" is 5^5]:
      kappa_true in 6 * 5^5 u^4 sum_{j=1}^3 V_j [A_Sigma_j - T_22(r_Sigma_j), A_Sigma_j + T_22(r_Sigma_j)].   (4.11)
  - Q: "Its width is less than 3 * 10^-20, and outward comparison with terminating rationals yields
    .000093307088324061 < kappa_true < .000093307088324062 = kappa-bar."
- Mine: (4.5) carries "z_i >= -2 (1 <= i <= 5)". This gives alpha_i >= 1/5 - 2u = lambda, which is redundant. I
  include it anyway; it changes nothing.

## 4. kappa_cvx, Sec. 13.3, p. 45

- Q: "The rational moment argument of Section 4.5 gives kappa_true < kappa-bar, with kappa-bar as in (4.3). An
  alternative convexity argument gives
      kappa_true < kappa_cvx := 11696/125000000 = .000093568.
  The convexity bound is proved in Lean without numerical-integral, distribution or finite-field premises. For the
  positive convex density on each simplex in Section 4.5, the integral is at most the simplex volume times the
  average of its five vertex values. The three rational vertex averages give the displayed upper bound."
- (13.1): xi_add = ((1 - ell)^2 / d_h)(kappa_cvx - kappa-bar) = ell(1 - ell)(kappa_cvx - kappa-bar)/kappa-bar.
  The extraction splits the fraction [transcribed].
- Mine: the "three rational vertex averages" are not printed. Only their rounded-up total 11696/125000000 is. I
  recomputed them from the vertex table (see the report).
