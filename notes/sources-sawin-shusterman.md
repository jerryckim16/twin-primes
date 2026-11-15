# Source transcription: Sawin-Shusterman, Chowla and twin primes over F_q[T]

Source [SS]: Will Sawin and Mark Shusterman, "On the Chowla and twin primes conjectures over F_q[T]",
arXiv:1808.04001 [math.NT], **version v2** (submitted 7 Sep 2019; v1 was 12 Aug 2018). Published in
Annals of Math. (2022). The page numbers below are for the arXiv v2 PDF and not for the Annals version.
- URL: https://arxiv.org/pdf/1808.04001. The abstract page https://arxiv.org/abs/1808.04001 (HTTP 200) lists v1 and v2. The PDF
  stamp reads "arXiv:1808.04001v2 [math.NT] 7 Sep 2019".
- Fetched on 15 Nov 2026 with plain curl into a new empty directory /tmp/claude-0/ss. Results: HTTP 200, 425032 bytes,
  SHA-256 5b762a0888363d2d1140bb9831a6d940586208f690b4dda3fa6e712337e0a687. It is a 41-page PDF (LaTeX/dvips).
- It was read with `pdftotext -layout`, and some displays were checked with `-raw`. Nothing from the download was run.
- The PDF page number equals the printed page number throughout (printed p. 1 = PDF p. 1).

Conventions:
- "Q:" marks verbatim text. Math glyphs are rewritten in ASCII/LaTeX. Pages are written "p. N" (PDF = printed).
- "[transcribed]" marks a display rebuilt from a split layout. "[garbled]" marks extraction that cannot be trusted.
- "Mine:" marks my own remark or calculation. It does not come from the source.
- Status of everything here: **Literature (read from source)**. I re-derived nothing except where it says "Mine: checked".

## 1. Main theorems

Notation (p. 1). Q: "Define the norm of a nonzero f in F_q[T] to be |f| = q^{deg(f)} = |F_q[T]/(f)|." (1.1)
Singular series (1.4), p. 1-2 [transcribed]:
  S_q(h) = prod_P (1 - |P|^{-1})^{-2} (1 - |P|^{-1} - |P|^{-1} 1_{P nmid h}), where P runs over the monic irreducibles.

**Theorem 1.1 (twin primes), p. 2.**
Q: "For an odd prime number p, and a power q of p satisfying q > 685090 p^2, the following holds. For any nonzero
h in F_q[T] we have
  #{f in F_q[T] : |f| = X, f and f + h are prime} ~ S_q(h) X / log_q^2(X)        (1.5)
as X -> infinity through powers of q. Moreover, we have a power saving (depending on q) in the asymptotic above."
- Q (p. 2): "For example, the 2-point Hardy-Littlewood conjecture holds over F_{3^15}, F_{5^11}, F_{7^9}, F_{11^8},
  F_{685093^3}." (1.6) [transcribed exponents]
- Body version: **Theorem 6.3, p. 30.** Q: "For every odd prime number p, and power q of p with q > 685090 p^2,
  there exists lambda > 0 such that the following holds. For nonnegative integers d > l, and a in M_l we have
  sum_{f in M_d} Lambda(f) Lambda(f + a) = S_q(a) q^d + O(q^{(1-lambda)d}) (6.18) as d -> infinity, with the implied
  constant depending only on q." Here M_d is the set of monic polynomials of degree d (1.22, p. 8), and (6.10, p. 28) gives
  S_q(a) = prod_{P|a}(1-|P|^{-1})^{-1} prod_{P nmid a}(1-(|P|-1)^{-2}).
- Mine: the range is **q fixed** with deg -> infinity. The condition is on q relative to the characteristic p
  (q > 685090 p^2). It is not a condition relating q to n, and it is not a large-q limit. Remark 1.6 (p. 5, quoted
  below) sets this apart from the "large finite field limit".
- Remark 1.2, p. 2. Q: "Our proof of Theorem 1.1 establishes also the analog of the Goldbach problem over function fields,
  and can be modified to treat more general linear forms in the primes."

**Theorem 1.3 (Chowla, k-point), p. 3.**
Q: "For an odd prime number p, an integer k >= 1, and a power q of p satisfying q > p^2 k^2 e^2, the following holds.
For distinct h_1, ..., h_k in F_q[T] we have sum_{f in F_q[T]^+, |f| <= X} mu(f + h_1) mu(f + h_2) ... mu(f + h_k)
= o(X), X -> infinity." (1.9)
- Q (p. 3): "For instance, the 2-point Chowla conjecture holds over F_{3^6}, F_{5^5}, F_{7^4}, F_{3^13}." (1.10)
- Q (p. 3): "In fact, in Theorem 1.3 we obtain a power saving inversely proportional to p, and the shifts h_1, ..., h_k
  can be as large as any fixed power of X (the corresponding assumption on q becomes stronger as this power grows
  larger). In Corollary 6.1 we also get cancellation in case the sum is restricted to prime polynomials f."
- In the body this is Corollary 4.7, p. 23: q > p^2 n^2 e^2 and distinct coprime pairs (a_i, M_i), giving
  sum_{g in M_d} prod_i mu(a_i + g M_i) = o(|M_d|) "as d -> infinity for fixed q, n, a_i, M_i".
  Uniform version: **Theorem 4.5, p. 22** [transcribed]. Fix eps, delta > 0, 0 < beta < 1/2 and n >= 1. Let q be a power
  of an odd p with q > ( p n e / min{eps/(eps+2), eps delta/(eps+delta)} )^{2/(1-2beta)} (4.33). Then for
  d >= max{eps m_i, delta k_i} with k_i != d + m_i, and (a_i, M_i) in M_{k_i} x M_{m_i} with the a_i/M_i distinct:
  sum_{g in M_d} prod_{i=1}^n mu(a_i + g M_i) << |M_d|^{1 - beta/p} (4.35).
- Corollary 4.6 (p. 23) gives the simpler condition q > p^2 n^2 e^2 max{1 + 2/eps, 1/eps + 1/delta}^2 (4.39), with o(|M_d|).
- Mine: there is an inconsistency in the source. (4.8) and (4.35) state the saving as exponent 1 - beta/p (checked with
  `-raw`). The proof of Thm 4.5 on p. 22 says Q: "we obtain a savings in each term of q^{(d-t')beta/2p} ... To obtain
  our desired savings of q^{d beta/2p}". So the constant in the saving exponent is beta/p in one place and beta/(2p) in
  the other. Either way the saving is proportional to 1/p.

**Theorem 1.4 (beyond Burgess), p. 4.** Q: "Fix eta > 0. Then for a prime power q > e^2/eta^2 the following holds. For a
squarefree M in F_q[T], a real number X >= |M|^eta, and a nonprincipal Dirichlet character chi mod M, we have
sup_{s} |sum_{|a| <= X} chi(s + a)| = o(X), |M| -> infinity." (1.12). There is no parity-of-p hypothesis here.

**Theorem 1.7 (Mobius, level ~ 1), p. 5.** Q: "Fix eta > 0. For an odd prime number p, and a power q of p with
q > p^2 e^2 (2/eta - 1)^2, the following holds. For coprime M, a in F_q[T], and a real number X with X^{1-eta} >= |M| we
have sum_{f monic, |f| <= X, f = a mod M} mu(f) = o(X/|M|), |M| -> infinity." (1.14)
- [transcribed] The q-condition is split across lines in both -layout and -raw ("p2e2 / 2 / eta - 1 / 2"). Mine: I read
  it as (2/eta - 1)^2. This agrees with Cor. 4.6 for n = 1, eps = eta/(1-eta), delta large: 1 + 2/eps = 2/eta - 1.
- Q (p. 5): "As in the previous theorems, we obtain a power savings estimate."

**Theorem 1.8 (Fouvry-Michel analogue), p. 6.** Q: "Let q be a prime power, and let eps > 0. Then for a squarefree
M in F_q[T], and an additive character psi mod M, we have sum_{f monic, |f| <= X, (f,M)=1} mu(f) psi(fbar)
<< |M|^{3/16+eps} X^{25/32}, X, |M| -> infinity where fbar denotes the inverse of f mod M". In the body this is
Theorem 5.1, p. 24, stated for "an odd prime power q" with d <= m: << q^{(3/16+theta)m + (25/32)d} (5.1).

**Theorem 1.9 (von Mangoldt, level beyond 1/2), p. 6.** Q: "Fix delta < 1/126. For an odd prime p and a power q of p
with q > p^2 e^2 ((51 - 26 delta)/(1 - 126 delta))^2 (1.19), the following holds. For a squarefree M in F_q[T], a
polynomial a in F_q[T] coprime to M, and X a power of q with X^{1/2+delta} >= |M| we have
sum_{f monic, |f| <= X, f = a mod M} Lambda(f) = X/phi(M) + o(X/|M|), |M| -> infinity." (1.20)
- In the body this is **Corollary 5.3, p. 25**: 0 < omega < 1/32, q > p^2 e^2 (1 + 50/(1-32 omega))^2, d >= (1-omega)m,
  squarefree M in M_m, deg a < d + m, and sum_{g in M_d} Lambda(a + gM) = q^{d+m}/phi(M) + E_q "with a power saving error
  term E_q".
- Mine: checked. Put m/(d+m) = 1/(2-omega) = 1/2 + delta. Then omega = 4delta/(1+2delta), so omega < 1/32 <=> delta < 1/126,
  and 1 + 50/(1-32omega) = (51-26delta)/(1-126delta). The two statements agree.
- Note: this is a **pointwise** estimate, for every single squarefree modulus. It is not an average over moduli.

Small-q results (p. 7): Theorem 1.11 (q a power of 3, sign changes of mu in intervals |g| <= |f|^eta, 3/7 < eta < 1) and
Theorem 1.12 (q a power of 3, cancellation of mu in the progression 1 mod P^n). Both use Burgess [Hsu99], not Section 2.

## 2. Architecture of the proof

### (a) The distribution estimates

- Level of distribution for **Mobius**: modulus degree up to (1 - eta) n, for any fixed eta, once q > p^2 e^2 (2/eta-1)^2
  (Thm 1.7). The saving is a power q^{-(beta/p) d} (Thm 4.5). Mine: this is far beyond the square-root barrier. It is
  for individual moduli and allows multi-point correlations (sums of prod_i mu(a_i + g M_i)).
- Level of distribution for **von Mangoldt**: modulus degree up to (1/2 + delta) n with delta < 1/126, with a power
  saving (Thm 1.9 / Cor 5.3). So it goes beyond 1/2, but only slightly.
- Abstract, p. 1. Q: "we obtain a level of distribution close to 1 for the Mobius function in arithmetic progressions, and
  resolve Chowla's k-point correlation conjecture with large uniformity in the shifts. Using a function field variant
  of a result by Fouvry-Michel on exponential sums involving the Mobius function, we obtain a level of distribution
  beyond 1/2 for irreducible polynomials, and establish the twin prime conjecture in a quantitative form."
- On the limit of 1/2 + 1/6. Q (p. 6-7): "We have not ventured too much into improving the constant 1/126, as our method
  cannot give anything above 1/6, even if Theorem 1.8 would give square root cancellation. Since our proof of
  Theorem 1.9 is based on the 'convolutional' connection of von Mangoldt and Mobius, it is not surprising that a level of
  distribution of 2/3 = 1/2 + 1/6, which is a longstanding barrier for the divisor function over Z (perhaps the most
  basic convolution), is a natural limit of our techniques. A large finite field variant of Theorem 1.7 and Theorem 1.9
  was earlier proved in [BBSR15, Theorem 2.5]."
- Over Z, for comparison. Q (p. 5): "Over the integers, assuming the Generalized Riemann Hypothesis (GRH), this level of
  distribution is (at least) 1/2, which means that sum_{n<=X, n=a mod M} mu(n) = o(X/|M|), sum Lambda(n) = X/phi(M)
  + o(X/|M|) (1.13) where M, a are coprime integers, and |M| <= X^{1/2-eps} (for any fixed eps > 0 and A in R).
  For Mobius over F_q[T], we obtain a level of distribution close to 1." [garbled: the "A in R" refers to something
  missing from the extracted display, probably a log^{-A} error term. I am not inferring it.]

### (b) How the twin prime count is deduced (Sections 5-6)

- Q (p. 2): "Once Theorem 1.7 and Theorem 1.9 below are established, Theorem 1.1 will follow from a quick argument
  involving a convolution identity relating the von Mangoldt function, which can be used to count primes, to the
  Mobius function."
- The identity used. Q (p. 25): "We shall use the convolution identity Lambda = -1 * (mu . deg) which for f monic of
  degree d >= 0 says that Lambda(f) = -sum_{k=1}^d k sum_{A in M_k, B in M_{d-k}, AB = f} mu(A)." (5.7)
- **Cor 5.3 (Lambda in APs, p. 25-26).** (5.7) is applied to Lambda(a + gM) and the range of k = deg A is split.
  (i) For k <= d, the sum over B is complete mod M, and Prop. 5.2 gives the main term q^{d+m}/phi(M).
  (ii) For k > d with (3/16 + 2theta) m + (25/32) k < d (5.12), the sum is expanded in additive characters
  mod M and Theorem 5.1 (Mobius against psi(abar)) gives a power saving.
  (iii) For the remaining k, the sum is sum_B sum_{g in M_{k-m}} mu(b + gM) (5.13). This is Mobius in an AP mod M of
  length degree k - m >= eps m, with eps = delta = (32/25)(1/32 - omega - 2theta) (5.14), and it is handled by Theorem 4.5.
- **Thm 6.3 (twins, p. 30-31).** Q: "Using Eq. (5.7) our sum becomes -sum_{k=0}^d k sum_{M in M_k} mu(M)
  sum_{N in M_{d-k}} Lambda(a + NM)." (6.19) For **k <= d/(2-omega)** the modulus M has degree up to 1/(2-omega) > 1/2 of
  the total, and Cor 5.3 together with Prop 6.2 (the singular series) gives the main term. For the
  **other range k > d/(2-omega)**, Q: "we need to prove a power savings bound for sum_{k > d/(2-omega)} k sum_{N in
  M_{d-k}} sum_{M in M_k} Lambda(a + MN) mu(M) (6.22) and this is done by applying Corollary 6.1 to the innermost sum
  with n = 1, eps~ = delta~ = infinity, alpha = 1 - omega > (d-k)/k". The constraints are q > 2pe(4/omega - 1)^2 (6.24) [sic,
  as extracted: "2pe" with the square outside] and (6.25). Q (p. 30-31): "the optimal bound is obtained by solving
  2(4/omega - 1) = 1 + 50/(1 - 32 omega) whose solution is omega = (103 - sqrt(30803/3))/64 = .0261... which satisfies
  2e(4/omega - 1)^2 < 685090." [transcribed]
- **Cor 6.1 ("Chowla sums over primes", p. 27)** bounds sum_{g in M_d} Lambda(a + gM) prod_i mu(a_i + g M_i)
  << |M_d|^{1 - beta(1-alpha)/(2p)} for m <= alpha d (6.2). Proof (p. 27-28): Lambda(a + gM) is split again by (5.7) at
  z = floor((d+m)/2) into a divisor B with deg B <= z and a cofactor C. After g = N + hB, each piece is a
  **multi-point Mobius correlation in progressions**, and Theorem 4.5 is applied "to the innermost sum".
- Type I / Type II. Mine: the paper does not use the words "Type I/II", "sieve", "Vaughan" or "Heath-Brown" in the
  deduction of Thm 1.1. The decomposition there is only the one-step identity Lambda = -1*(mu.deg). **Vaughan's
  identity and Type I / Type II sums appear only in Appendix A**, in the proof of Theorem 5.1 (mu twisted by
  psi(fbar)). Q (p. 32-33): "Following [FM98], we use Vaughan's identity ... By applying Vaughan's identity as in [FM98,
  Section 6], we reduce our task to bounding sums of type I ... and sums of type II". Type I is handled by the bilinear
  shifting trick + Hoelder ([FM98, §4]) and Kloosterman sheaves (Prop A.1). Type II is handled by Cauchy + Polya-Vinogradov completion
  as in [FKM14, Thm 1.17] and a Weil bound (Prop A.4). Prop A.1 has a separate case for p = 3 (pp. 35-38).
- How parity is avoided. Q (p. 2): "The main ingredient in the proof of Theorem 1.1 is the removal of the 'parity
  barrier'. More precisely, we confirm Chowla's k-point correlation conjecture over F_q[T] for some prime powers q."
  Mine: the "Mobius side" of every convolution (ranges (iii) of Cor 5.3 and the large-k range of Thm 6.3 via Cor 6.1) is
  bounded directly by Thm 4.5. No sieve is used. Thm 4.5 is a parity-sensitive statement (mu in APs at level close to 1,
  and correlations of mu). It holds because of the identity in (c) below.

### (c) The algebraic and geometric inputs

- **The derivative trick (Sec. 3, char p, p odd).** Q (p. 3): "our result relies on special properties of the Mobius
  function (in positive characteristic). Specifically, we observe that for any fixed polynomial r, the function
  mu(r + s^p) essentially equals chi_{D_r}(s + c_r) where chi_{D_r} is a quadratic Dirichlet character and c_r is a
  shift, both depending only on r (and not on s)." Q (p. 3-4): "In odd characteristic, this sign is determined by the
  value of the quadratic character of F_q^x on the discriminant of f, i.e. the resultant of f and its derivative f'.
  In characteristic p, the derivative of f = r + s^p is equal to the derivative of r, so the aforementioned sign of
  Frobenius is determined by the quadratic character of the resultant of f with the fixed polynomial r'."
  - Formal version, Lemma 3.2 (p. 15): mu(a + gM) = S . chi(w + g), where w, chi and S depend only on (a, M, g') and chi
    is a real character mod E with E built from D = M^2 (g + a/M)' (3.4). The proof uses Pellet's formula
    mu(f) = (-1)^{deg f} psi(Disc f) (3.7) [Con05] and quadratic reciprocity.
  - Proposition 4.1 (p. 17) counts how many g in M_d share a derivative class (a saving of q^{-min(m, floor((d-1)/p))}).
    Q (p. 5, Remark 1.5): "The relation between Mobius and multiplicative characters is less powerful the larger p is,
    as then fewer polynomials share a given derivative. On the other hand, our geometric character sum bounds become
    stronger as q grows. Thus, to make this method of proving Chowla work, we need q to be sufficiently large with
    respect to p."
- **Short character sums (Sec. 2): Theorem 2.1, p. 8.** For t <= m, g in M_m squarefree, chi nontrivial mod g:
  |sum_{deg h < t, gcd(f+h,g)=1} chi(f + h)| <= (q^{1/2} + 1) binom(m-1, t) q^{t/2} (2.1) [transcribed].
  - Method. Q (p. 4): "we express the problem geometrically, viewing the short interval {s + a : |a| <= X} as an affine
    space over F_q, and the character chi as arising from a sheaf on that space. Following a strategy from [Hoo91,
    appendix by Katz], we use vanishing cycles theory to compare the cohomology of this sheaf for the s = 0 short
    interval and its cohomology for a general short interval. ... we split the modulus M of chi into a product of
    distinct linear terms over F_q [sic; geometrically], which makes our vanishing locus a union of the hyperplanes
    ... a simple normal crossings divisor away from some isolated points. This implies that the cohomology groups
    vanish until almost the middle degree."
  - The ingredients, with pages: character sheaf L_chi via the Lang isogeny (p. 8). The stalk at (0,1) is computed through
    S_t-invariants/Kuenneth, giving rank binom(m-1, t) in degree t (Lemma 2.3, p. 9). SNC away from deg gcd > t (Lemma 2.4,
    p. 10). [SGA7-II XIII 2.1.11] and perversity of vanishing cycles [Ill94, Cor 4.6] (Lemma 2.6, p. 11). Q (p. 13):
    "By Deligne's theorem, the absolute values of the eigenvalues of Frobenius on the i-th cohomology group are at
    most q^{i/2}", followed by Lefschetz.
  - **Corollary 2.7, p. 13**: fix eta > 0 and 0 < beta < 1/2. If q >= (e eta^{-1})^{2/(1-2beta)} and t >= eta deg(g), then
    sum_{deg h < t} chi(f + h) << q^{(1-beta)t}. Mine: the binomial (Betti-number) bound costs about (e m/t)^t, and
    q must be large enough to absorb it. This is where "q large" comes in. The relevant ratio is length/conductor-degree,
    which is bounded below by eta/(pn) (4.24, p. 20). Hence the p^2 n^2 e^2 thresholds.
  - Q (p. 4): "By further enlarging q, we get arbitrarily close to square root cancellation."
- Large-finite-field contrast. Q (p. 5, Remark 1.6): "The study of the statistics of polynomial factorizations by
  examining Frobenius as an element of the symmetric group has been very fruitful in the 'large finite field limit',
  where (in the notation of Theorem 1.3) X is kept fixed and q is allowed to grow. ... Our methods likely give an
  improved savings in the large finite field limit when the characteristic is fixed, as long as the degrees of the
  polynomials are sufficiently large with respect to the characteristic".
- Characteristic 2 is open. Q (p. 7, Remark 1.10): "It would be interesting to see whether our results can be extended
  to characteristic 2".

### (d) The authors' remarks on the integers and on parity

- Q (p. 1): "Our main results are the resolutions of two open problems in number theory, except with the ring of
  integers Z replaced by the ring of polynomials F_q[T], under suitable assumptions on q."
- Q (p. 2): "The strongest result known over the integers is [PM14, Theorem 16(i)], which says that for any 'admissible
  tuple' of 50 integers, there exists at least one difference h between two elements in the tuple such that there are
  infinitely many pairs of primes separated by h."
- Q (p. 2): "The only completely resolved case is k = 1 which is essentially equivalent to the prime number theorem."
  (This is about Chowla over Z.)
- Q (p. 3): "In contrast to these works [Tao, Tao-Teravainen, MR], which deal with any sufficiently general (i.e.
  non-pretentious) multiplicative function, our result relies on special properties of the Mobius function (in
  positive characteristic)." [the bracket is mine and summarizes the preceding sentences]
- Q (p. 4): "Refining the method of Burgess is the focus of several works, but the exponent 1/4 has not yet been
  improved (even conditionally). However, in the function field setting, we can do better by a geometric method, as
  long as q is sufficiently large."
- The 2/3 divisor-function barrier over Z (p. 7) is quoted in (a).
- Mine: the paper never says that an integer analogue of its estimates would prove twin primes over Z, and it makes no
  conditional claim over Z. The word "parity" appears only in "removal of the 'parity barrier'" (p. 2) and in the
  description of the parity of the number of prime factors (p. 3).

## 3. Which step has no integer analogue

From the paper:
1. **The characteristic-p identity (Lemma 3.2).** mu restricted to the "lines" r + s^p (or a + (r + s^p)M) becomes a
   Dirichlet character in s. Q (p. 6): "we view F_q[T] as a rank p lattice over its subring F_q[T^p]. Restricting the
   Mobius function to any line in this lattice gives a Dirichlet character whose modulus varies with the line." It
   uses f' = r' when f = r + s^p, and Pellet's formula. The paper ties this explicitly to "positive characteristic" (p. 3).
2. **Short character sums beyond Burgess (Thm 1.4/2.1/Cor 2.7).** These are needed at length/conductor ratio about
   eta/(pn), which is far below 1/4. Over Z, Q (p. 4): "the exponent 1/4 has not yet been improved (even
   conditionally)."

Mine (analysis, not in the paper):
- Step 1 is the decisive one. Z has no Frobenius-twisted subring Z[T^p] and no derivative with (r + s^p)' = r'. The
  Pellet/Stickelberger link between mu and a quadratic character of a discriminant has no analogue for integers.
  With step 1 in place, step 2 is the analytic bottleneck. Its integer counterpart (Burgess below 1/4) is open even
  under GRH, as the authors note.
- The integer statements that would replace the output of these steps (Theorem 4.5 / 1.7) are these. (i) mu in arithmetic progressions to
  **each individual modulus** M <= x^{1 - eta} with a power saving. Mine: this is beyond what GRH gives, since (1.13)
  stops at x^{1/2}. (ii) The correlations sum_{n<=x} prod_i mu(a_i + n M_i) with power saving and polynomial
  uniformity in a_i, M_i (two-point Chowla in progressions). For the twin-prime deduction (Thm 6.3), the needed
  integer inputs are: (iii) Lambda in APs to every individual modulus up to x^{1/2+delta} with a power saving (an
  EH-type statement for single moduli; the paper's Cor 5.3 analogue), and (iv) the "Chowla over primes" bound
  sum_{m ~ x/n} mu(m) Lambda(a + m n) = o(x/n), with n up to about x^{1-1/(2-omega)} (the paper's Cor 6.1 with n = 1).
  Statement (iv) is parity-sensitive: it is a mu-Lambda binary correlation, of the same depth as twin primes over Z.
- Whether this would suffice over Z: the paper does not say. Mine: the deduction in Sec. 5-6 is formal (identity (5.7),
  splitting of ranges, singular series in Prop 6.2 [the integer analogue is cited as GY03, Lemma 2.1, p. 28]). So the
  integer versions of Thm 4.5 (for (ii)/(iv)) and Thm 5.1 (Fouvry-Michel, which exists over Z for prime moduli [FM98];
  Q (p. 6): "While Fouvry-Michel work with characters to prime moduli, in order to establish Theorem 1.1 we need
  arbitrary squarefree moduli") would plausibly give twin primes by the same bookkeeping. This is my inference only.
- Type II. Mine: the parity-breaking input is **not** a Type II estimate. Type I/II sums appear only in Appendix A, for
  the (Fouvry-Michel) twisted-Mobius bound, which is not parity-sensitive. Parity is broken by Thm 4.5, which has no
  combinatorial decomposition at all: it comes from the algebraic identity plus character sums.

## 4. Quantitative relationships (for citing)

- Twins (Thm 1.1/6.3): p odd and q > 685090 p^2. Power saving q^{-lambda d} with lambda = lambda(q) > 0 not made explicit.
  The asymptotic is "X -> infinity through powers of q", that is, deg -> infinity with q fixed.
  685090 > 2e(4/omega - 1)^2 at omega = (103 - sqrt(30803/3))/64 = 0.0261... (p. 31).
- Lambda level (Thm 1.9): |M| <= X^{1/2 + delta}, delta < 1/126, q > p^2 e^2 ((51 - 26delta)/(1 - 126delta))^2. Methodological
  ceiling 1/2 + 1/6 (p. 6). Equivalent form (Cor 5.3): deg M <= deg g/(1-omega), omega < 1/32.
- Mobius level (Thm 1.7): |M| <= X^{1-eta}, q > p^2 e^2 (2/eta - 1)^2 [transcribed]. The saving exponent is about beta/p
  (Thm 4.5; see the beta/p vs beta/(2p) inconsistency in Sec. 1).
- Chowla (Thm 1.3): q > p^2 k^2 e^2. The saving is "inversely proportional to p". Shifts may be as large as a fixed power of X.
- Short character sums (Cor 2.7): length t >= eta deg g and q >= (e/eta)^{2/(1-2beta)} give a saving q^{-beta t}. Theorem 1.4 needs
  q > e^2/eta^2.
- Fouvry-Michel analogue (Thm 1.8/5.1): << |M|^{3/16+eps} X^{25/32}.
- Mine: "the level depends on p" is wrong as a description. The level for Lambda is a fixed 1/2 + delta, with delta < 1/126 for
  every admissible q. What depends on p is the **threshold on q** (q >~ p^2) and the **size of the saving** (~1/p).
