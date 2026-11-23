# Route card: Merikoski's large-sieve route to Green–Sawhney-type Type I estimates, and the twin family n(n+2)

- **Date:** 2026-11-23 (Session 48). Kind: bounded parity attempt (mechanism 1 of review 2026-11-23 §4; deferred since
  Session 34). Literature reading, elementary arguments, and one small computation.
- **Classification: located (this route does not help; Merikoski's multiplicative-large-sieve argument itself is
  unpublished and unread; elementary; possibly folklore).** The success criterion below is NOT met. The no-go criterion
  holds for every placement examined here, but the argument that names the route has not been read, so the card does
  not claim a no-go for it.
- **Where the large sieve enters.** In Merikoski's published Type I argument (arXiv:2112.03617v3, §3.3) it is a large
  sieve over the roots ν/d of ν² + 1 ≡ 0 (mod d). That argument uses (i) an ANISOTROPIC norm form, whose roots are well
  spaced (Lemma 6, quoted from FI98b), and (ii) a second, free coordinate of length about X^{1/2}, which Poisson
  summation turns into a long dual variable n = hb.
- **How the twin polynomial n(n+2) = (n+1)² − 1 compares:**
  - It is the y = 1 slice of the ISOTROPIC split form x² − y² = (x − y)(x + y), so there is no second free coordinate.
  - For odd d = d₁d₂, each root mod d lies within 1/d of a rational whose denominator divides min(d₁, d₂) ≤ √d.
  - The Lemma 6 shape (D + N) fails for its root set: Δ ≥ (4/17)·N·(D + N) for N ≤ D/16, so the loss is ≫ D in the
    regime N ≍ D that Merikoski uses. Classical spacing gives Δ ≤ N + D², so the loss is bounded for N ≥ D² (Finding 3:
    proved, and computed).
  - This failure sits on the unbalanced ("trivial") roots. For n(n+2) itself, Type I sums over d | n(n+2) are
    elementary up to a level close to the length, so the failure is irrelevant there rather than an obstruction. On the
    balanced roots the sieve behaves well (table).
  - Its "multiplicative family" is the split algebra Z × Z. There the twin pairs form a codimension-one line,
    twin-prime elements (p, p+2) have λ(N(a)) = +1, and the algebra's own primes are trivial (Finding 2).
  - "Type I information on λ" is trivial in a multiplicatively closed family (Finding 1). On the twin line it is exactly
    the twisted Type I input of PM8b's obstruction, i.e. the paper's own class.
  - The coordinate placement through the Green–Sawhney remark is circular at frequency 0 (Finding 5), as in Session 34.
- **No parity-breaking content.** Nothing here bears on a lower bound for twin primes, and the twin prime conjecture
  stays OPEN. Not in the paper (v1.0 frozen).

## Mechanism (new for this programme)

Green–Sawhney (GS) prove Type I estimates for weights in product form, w(x + y√−n) = f(x) f′(y), from Gowers U³-norm
lower bounds (their Prop. 4.2). In the remark after Prop. 4.2 they record that Merikoski indicated "a rather different
argument using the multiplicative large sieve". That argument gives a stronger conclusion: f and f′ correlate with
major-arc phases. Merikoski's published Type I estimates for a² + (b² + 1)² and a² + (c³ + d³)² are the nearest
published instance of a large-sieve Type I argument in a thin norm-form family. The bounded question (review §4,
mechanism 1): does n(n+2), or a twin-adjacent norm-form family, carry a multiplicative family large enough for the
multiplicative large sieve to give Type I information on λ in that family?

## Question and criteria (fixed before reading the sources and before the check)

What is already implied by the paper's weight class (sec:bip, "The class of weights"): under the Möbius-randomness
heuristic, twisted Type I sums Σ ν(n) λ(n)λ(n+2) (with f = 1 or Λ at one position) are negligible. So a fair pattern
weight, e.g. 1 − λ(n)λ(n+2), reproduces every Type I input and kills the twin target. A PROOF of Type I information on
λ(n)λ(n+2), at any level, therefore only confirms the obstruction's input (cf. Prop. prop:tao-weight-logc). It is not
success.

- **Success:** a placement of the fixed-shift twin condition (n, n+2) into a family F with multiplicative structure,
  together with an estimate provable by the (multiplicative or root) large sieve in F, such that the transported fair
  weight ν·(1 − λ(n)λ(n+2)) FAILS that estimate. Such an estimate would separate the twin weight from a member of the
  class, which no input of the class can do. A weaker success: a reduction of such an estimate to a hypothesis strictly
  weaker than the twin asymptotic and not itself a twisted Type I input of the class.
- **No-go:** in every placement, one of the following holds, and no other placement is visible.
  - (i) The large-sieve inequality for the family fails, or gives only the trivial level.
  - (ii) Type I on λ is either trivial (the family is multiplicatively closed) or exactly the PM8b twisted Type I input
    (the class's own input).
  - (iii) The needed input contains the twin asymptotic (circular).
- **Outcome:** success not met. Every placement examined falls under (i), (ii) or (iii) (Findings 1–5). (i) is meant in
  the sense "gives nothing beyond the trivial level", not as an obstruction (Finding 3, last paragraph). The
  multiplicative-large-sieve argument itself is unread, so the verdict is "located; this route does not help", not a
  no-go for that argument.

## Sources (Literature; downloaded with curl into a new directory /tmp/claude-0/merikoski/, read with `pdftotext -layout`; PDFs not committed)

- J. Merikoski, *The polynomials X² + (Y² + 1)² and X² + (Y³ + Z³)² also capture their primes*, arXiv:2112.03617v3
  (21 Jul 2023), 68 pp. Published as Proc. Lond. Math. Soc. (3) 127 (2023), 1057–1133 (GS ref. [39]).
  - SHA-256 d7555c6539fdf9f1ba967d7fb8e28181835deb5d2fb61daa16e10a9bcd5ae819.
  - Read: §1 including the sketch §1.1 (pp. 1–6), §3 (Props. 4, 5, Lemma 6, the proof §3.3 to p. 13). Not read: §§4–11.
  - The identifier 2112.03617 was confirmed by web search and arXiv abs page.
- B. Green, M. Sawhney, *Primes of the form p² + nq²*, arXiv:2410.04189v3 (6 Jun 2026), 59 pp.
  - SHA-256 741b8ebc72b401e912f99a14b74572de4047921194f6c176715a5d6f14635e4f. This is the same file as the Session 34
    card.
  - Read this run: p. 3 (the Merikoski citations [38, 39]), Props. 4.2 and 4.3 and the Remark between them (pp. 20–21),
    and reference [16].
- L. Grimmelt, J. Merikoski, M. Pandey, A. Pascadi, *Primes and the Möbius function over quadratic polynomials*,
  arXiv:2610.41356v1 (30 Oct 2026), 59 pp.
  - SHA-256 a5bbd01a8fa3e6a867b257dc50d9d4cc13768feb5a4e892522ad8f921fddf54c. It was found during the search, kept in a
    separate new directory, and used only for literature scope.
  - Read: abstract and §1 (pp. 1–4).
- **Could not be opened / does not exist yet:**
  - The "multiplicative large sieve" argument itself. GS attribute it to Merikoski as a personal communication, say
    "as we will discuss in [16]", and give [16] as "Ben Green and Mehtaab Sawhney, Corners in the Gaussian primes,
    Forthcoming." A web search (23 Nov 2026) found no arXiv posting. The exact inequality used, and the family it is
    applied to, are therefore UNREAD. Only the conclusion GS state is used below.
  - FI98b Lemma 3.2 (Friedlander–Iwaniec, "The polynomial X² + Y⁴ captures its primes", Ann. of Math. 148 (1998)
    945–1040; Merikoski's ref. [6]), the root large sieve, is quoted from Merikoski's Lemma 6, not opened. "FI98" alone
    means the asymptotic-sieve paper (same volume, 1041–1065), as on the 2026-11-14 card.
  - Merikoski arXiv:2302.11331 ([38] in GS) was not opened.

## What the sources say (Literature, as stated there)

- **Merikoski, Prop. 4 (Type I):** for bounded α(d) and D₁ ≤ X^{3/4−η′},
  Σ_{d∼D₁} α(d) Σ_{n∼X/d} (a_{dn} − b_{dn}) ≪ X^{1−η}.
  - Here a_n = κ₁ Σ 2b over the representations n = a² + (b² + 1)² with b > 0 and (a, b² + 1) = 1. The comparison
    sequence b_n counts the representations n = a² + b² with b > 0 and (a, b) = 1.
  - The coprimality conditions are needed (Remark 2: at d = 5 the two sides differ by a factor 8/9).
- **Where the arithmetic enters Type I (§3.3, p. 11):**
  - d | a² + b² with (a, b) = 1 is rewritten as a ≡ νb (mod d), where ν runs over the roots of ν² + 1 ≡ 0 (mod d).
  - Poisson summation in the FREE coordinate a (length A ≍ X^{1/2}) leaves frequencies 0 < |h| ≤ H = X^{ε′} c D₁/A.
  - Cauchy–Schwarz and Lemma 6 are then applied: Σ_{d≤D} Σ_{ν² + 1 ≡ 0 (d)} |Σ_{n≤N} γ_n e_d(νn)|² ≪ (D + N) Σ|γ_n|².
    The dual variable is n = hb, of length N = HB/c. The discrepancy is Δ(b) = 1 − κ₁ Σ_{b = b₀²+1} 2|b₀|, split as
    Δ₁ − Δ₂. In the case k = 2 that is written out, γ_n carries the THIN weight Δ₂(bc) = κ₁ Σ_{bc = b₀²+1} 2|b₀|.
  - The resulting bound D₁^{3/2} X^{1/8} ≪ D₁ X^{1/2} gives the level X^{3/4} (p. 13).
  - The factorisation wz = b² + 1 + ia (m = |w|², n = |z|²) is used only in Type II (§1.1, §4). Type I uses the
    Gaussian structure only through the roots ν. Type II is handled by the Weil bound in the range X^{1/4+η} ≪ N ≪ X^{1/3−η}, which is too narrow for an asymptotic, so
    Harman's sieve gives the order of magnitude only.
  - The large sieve in this paper is therefore an ADDITIVE large sieve over special points (roots of a quadratic
    congruence), not the multiplicative (character) large sieve.
- **GS, Remark after Prop. 4.2 (p. 21), verbatim in substance:** Merikoski's argument "using the multiplicative large
  sieve ... allows one to show that in fact f, f′ correlate with linear phases e(θx) with θ close to a rational with
  denominator ≪ (log X/δ)^{O(1)}". Prop. 4.2 itself gives only ‖f‖_{U³[X^{1/2}]}, ‖f′‖_{U³[X^{1/2}]} ≫
  (δ/((|ℓ|+1) log X))^{O(1)}.
  - In GS the parity barrier is broken by the Type II statement Prop. 4.3 (any 1-bounded α, β over ideals), not by
    Type I.
- **GMPP (2610.41356), §1:** they compare μ(n² + h) and Λ(n² + h), on average over h ≤ H, with the "twin prime
  analogues" n(n + h). The latter are known for H ≥ X^{8/33+ε} (Λ) and for H → ∞ (μ) by Matomäki–Radziwiłł–Tao, and
  they call the irreducible case "significantly harder". Their Type I sums are "very easy" because d is shorter than
  the smooth variable r. Parity is broken by their Type II sums, through averaging over h.

## Findings

### Finding 1 (Proved here, elementary): Type I on λ is trivial in a multiplicatively closed family

Let K be a number field, F the set of all integral ideals a of O_K with N(a) ≤ X, and g = λ∘N. Since N is
multiplicative and λ is completely multiplicative, g is completely multiplicative on ideals, and for every ideal d
  Σ_{a ∈ F, d | a} g(a) = g(d) Σ_{N(b) ≤ X/N(d)} g(b).
The inner sum is o(X/N(d)), uniformly, with a de la Vallée-Poussin error. Its Dirichlet series is
ζ_K(2s)/ζ_K(s) times a function holomorphic and non-zero in Re s > 1/2 + ε. For quadratic K this was checked prime by
prime: split p gives (1 + p^{−s})^{−2}, inert p gives (1 − p^{−2s})^{−1} against 1/(1 + p^{−2s}), and ramified p
(one ideal of norm p, g = −1) gives (1 + p^{−s})^{−1} against (1 − p^{−s})/(1 − p^{−2s}) = 1/(1 + p^{−s}), so it
holds there too. Hence
Type I on λ holds at every level D ≤ X^{1−ε} with no large sieve at all.

"Type I information on λ" is informative only in a family that is NOT closed under d | a ↦ a/d. The GS product weights
f(x) f′(y) are such a family, and so is the twin line of Finding 2. Thus the bounded question is really about the
non-closed case.

### Finding 2 (Proved here, elementary): the multiplicative family carried by n(n+2) is the split algebra, and twins sit on a line in it

n(n+2) = (n+1)² − 1 = N_A(u, v) with A = Q × Q, N_A(u, v) = uv, (u, v) = (n, n+2). Equivalently, n(n+2) is
x² − y² = (x − y)(x + y) at y = 1. The multiplicative family is Z × Z: about X log X elements with uv ≤ X. The twin
condition is the additive, codimension-one condition v − u = 2, with about X^{1/2} elements. This is the
"family large enough" question, answered by size and by the following structure.
- **(a) No prime detector of GS/Merikoski type.** The primes of A are (p, 1) and (1, p), so "N_A(a) prime" forces one
  coordinate to be 1. A twin element (p, p+2) is the product (p, 1)(1, p+2) of two primes of A from different
  components, with λ(N_A a) = λ(p)λ(p+2) = +1 for every twin-prime element. That is an E2-type, parity-EVEN target: the fair weight
  1 − λ(N_A(a)) = 1 − λ(n)λ(n+2) kills it.
- **(b) Type I on λ along the line is the class's input.** For d = d₁d₂ with d₁ | u, d₂ | v, the sum
  Σ_{d₁ | n, d₂ | n+2} λ(n)λ(n+2) is exactly the twisted Type I sum of PM8b, and it is assumed in the class.
  - What is known: a log-averaged statement for Selberg-square weights at level (log x)^{c₀}, conditional on the
    TT25 preprint (paper Prop. prop:tao-weight-logc). That is not a per-modulus statement.
  - The line is not multiplicatively closed: if (u, u+2) lies on it, then (u/d₁, (u+2)/d₂) is in general not on it.
    It can be: u = 6, d₁ = 3, d₂ = 2 gives (2, 4). So Finding 1 does not apply.
- **(c) A-bilinear sums.**
  - For the cross factorisation (u, 1)·(1, v), Σ α_u β_v 1[v = u + 2] is the binary correlation itself (α = β = Λ is
    the twin count): circular.
  - For factorisations inside one component, with Λ at the other component, the sums are Σ α_m β_k Λ(mk + 2). Taking
    β_k = γ(k, C) μ(mk) (outer absolute value over m) gives (B-twin) of the 2026-11-14 card, FI98's (B) for
    Λ(· + 2), documented out of reach. The general α × β form is stronger than (B-twin).

### Finding 3 (Proved here, plus computed): the Lemma 6 shape fails for the roots of the isotropic twin polynomial, on their unbalanced part

Let P(F, D) = {ν/d mod 1 : d ≤ D, F(ν) ≡ 0 (mod d)}, and let Δ(P, N) be the best constant in
Σ_{x∈P} |Σ_{n≤N} γ_n e(nx)|² ≤ Δ Σ|γ_n|².

- **(a) Anisotropic forms repel small-denominator rationals.** Take F = x² + 1, ν/d ≠ a/q and m = qν − ad ≠ 0. Then
  m² + q² ≡ q²(ν² + 1) ≡ 0 (mod d), so m² + q² ≥ d and |ν/d − a/q| = |m|/(qd) ≥ √(d − q²)/(qd), which is ≍ 1/(q√d)
  for q ≤ c√d.
  - This is far larger than 1/d. (Heuristic, since the proof of FI98b Lemma 3.2 was not opened: this repulsion,
    together with the well-spacing that Lemma 6 encodes, is what makes Δ ≪ D + N.)
  - The same holds for any anisotropic form; for indefinite ones, for q ≪ √d. For example, for x² − 2 (indefinite):
    m² − 2q² ≡ 0 (mod d) and m² − 2q² ≠ 0 (√2 is irrational), so for q < √(d/2), m² ≥ d + 2q² and |m| ≥ √d. The computed
    constant behaves the same way (see below).
- **(b) The split form has isotropic vectors, and the roots sit on them.** Take F = x² − 1, which gives the roots of
  n(n+2) ≡ 0 (mod d) via n = ν − 1. Let d be odd. (For even d the coprime decomposition below can fail: d = 8, ν = 3
  gives gcd(ν − 1, 8) = 2 and gcd(ν + 1, 8) = 4.) Write d = d₁d₂ with (d₁, d₂) = 1, ν ≡ 1 (mod d₁), ν ≡ −1 (mod d₂). Then
  ν = 1 + d₁t with t ≡ −2·d̄₁ (mod d₂), so
    ν/d = t/d₂ + 1/d, and symmetrically ν/d = s/d₁ − 1/d.
  Every root therefore lies within 1/d of a rational whose denominator divides min(d₁, d₂) ≤ √d. Here m = ±q is allowed:
  m² − q² = 0, which is an isotropic vector. This is distinctive only when min(d₁, d₂) is small, i.e. on the unbalanced
  and trivial part. For balanced d₁ ≍ d₂ ≍ √d, being within 1/d of a rational with denominator ≤ √d is no constraint
  (Dirichlet).
  - The trivial roots ν = ±1 (d₁ or d₂ = 1, i.e. d | n or d | n+2) give the points ±1/d.
  - With γ_n = 1 (n ≤ N) and N ≤ D/16, every d ∈ (8N, D] has Re Σ_{n≤N} e(n/d) ≥ N cos(π/4).
  - Hence Δ ≥ (D − 8N)N/2 ≥ (4/17)·N·(D + N) for N ≤ D/16 (using both points ±1/d would double this). The Lemma 6
    shape (D + N) thus fails by a factor ≥ (4/17)N for N ≤ D/16, which is ≫ D in the regime N ≍ D that Merikoski uses.
  - Upper bound: the roots are distinct reduced fractions (ν² ≡ 1 forces (ν, d) = 1) with denominators ≤ D, so they
    are 1/D²-spaced. The classical large sieve then gives Δ ≤ N + D². So the loss factor is about min(N, D²/N), and it is
    bounded for N ≥ D². The failure is not "≫ min(N, D)" for all N (corrected in the audit).
- **(c) Computed** (code/parity/merikoski_root_large_sieve.py, output .out, D = 1000; top eigenvalue of the N × N Gram
  matrix, computed numerically in double precision with eigvalsh):

  | Point set | Δ/(D+N) at N = 30 | N = 1000 | Share within 5/D of a/q, q ≤ 5 (uniform ≈ 0.1) |
  |---|---|---|---|
  | x² + 1 | 0.61 | 1.87 | 0.008 |
  | x² − 2 | 0.59 | 1.17 | 0.011 |
  | x² − 1 (all roots) | 52.9 | 217 | 0.59 |
  | x² − 1, "trivial": odd part of d divides ν − 1 or ν + 1 | 52.8 | 217 | 0.75 |
  | x² − 1, mixed, min odd factor ≥ D^{1/4} | 1.59 | 4.47 | 0.000 |

  The bad part of the twin root set is exactly the part where one linear factor carries (almost) all of d. The balanced
  mixed part looks like the anisotropic case at this size (it grows mildly, from 1.6 to 4.5; no claim is made about
  its true order). These are illustrations at one small D, not proofs. The proved statements are those in (b).

What (b) means, and what it does not mean:
- Merikoski's Type I argument uses the spacing of roots that an anisotropic norm form supplies. The split twin
  polynomial does not supply it on its unbalanced part. Its roots mod d are governed by the factorisations d = d₁d₂,
  i.e. by the two linear forms n, n+2 separately, which is the structure the class already sees.
- This is NOT an obstruction for n(n+2) itself. Type I sums over d | n(n+2) are elementary up to a level close to the
  length of n, so the root large sieve is not needed. On the balanced roots it behaves well at this size (table). The
  failure only shows that the 2D family x² − y² carries no Lemma-6-type input as a whole.

### Finding 4 (Proved here, elementary, for the Poisson + root-large-sieve scheme): even with good spacing, a one-point thin coordinate gives only the trivial level

Put the twin condition in Merikoski's scheme as the thin coordinate, b ∈ S = {1} (the slice y = 1), with the free
coordinate a ∼ A.
- After Poisson summation in a, the dual variable is n = h·1 with h ≤ H = X^ε D/A, and Cauchy–Schwarz with Lemma 6 bounds
  the error by
    (A/D) · D^{1/2} · ((D + H)H)^{1/2} ≪ X^{ε} (AD)^{1/2}.
- Against the main term ≍ A this is non-trivial only for D < A X^{−2ε}. That is no better than the trivial level of a
  one-variable quadratic polynomial (error Σ_{d≤D} ρ(d) ≪ D log D).
- This is in the anisotropic analogue x² + 1, i.e. even granting the spacing of Finding 3(a).
- In Merikoski's theorems the thin set has size |S ∩ [B]| ≍ B^{1/2} (b² + 1) or B^{2/3} (c³ + d³) inside B ≍ X^{1/2}, and
  in [38] (as described by GS, not opened) ≫ B^{1−δ}. A one-point S is below every threshold.
- So, within the Poisson + root-large-sieve scheme with a one-point thin set, n(n+2) does not carry a family large
  enough. (This says nothing about the unread multiplicative-large-sieve argument.) Twin-adjacent norm families that do have a long thin coordinate,
  x² − y² with y ∈ S growing, encode prime pairs at the differences 2y, y ∈ S. That is averaged Hardy–Littlewood over
  the shifts, the MRT setting compared in GMPP §1 (and the 2026-11-17 MRT card). It is excluded from the new mechanisms
  by the review.

### Finding 5 (Proved here, elementary, conditional on the GS remark as stated): the coordinate placement stays circular

Take the GS Type I sum with f(x) = (Λ′(x)Λ′(x+2) − F(x))/(log X)², with F a model. This f is O(1)-bounded, not
1-bounded; a constant rescaling fixes that.
- By the Merikoski variant (as GS state it), a large Type I sum forces f to correlate with e(θx), θ near a/q,
  q ≪ (log X/δ)^{O(1)}.
- The contrapositive needs non-correlation at all such phases. At θ = 0 (q = 1) that is Σ_{x≤N} Λ′(x)Λ′(x+2) =
  Σ F(x) + O(δ^{c} N (log N)²): the twin asymptotic at precision δ (GS use δ = (log X)^{−12}).
- The Session 34 circularity therefore persists. The weaker hypothesis (major-arc Fourier instead of U³) does not
  remove the frequency-0 term.
- With f(x) = λ(x)λ(x+2) the needed input is two-point Chowla twisted by major-arc phases at power-of-log precision.
  That is open. Tao 2016 has the logarithmic average only, and TT25 Thm 3.1(ii) gives natural-density bounds outside
  exceptional scales (as recorded on the 2026-11-15 cards; not reopened). It is again a twisted Type I input of the class, so it
  is not success.
- Independently: even a full Type I theory does not break parity in GS. Their Type II Prop. 4.3 does, through the
  multiplicativity of the norm, i.e. for prime-norm (λ = −1) targets, which twins are not (Finding 2a).

## Answers

- **Does n(n+2) carry a multiplicative family large enough?** Not for the Poisson + root-large-sieve scheme with a
  one-point thin set (the multiplicative-large-sieve argument itself is unread).
  - Its multiplicative family is the split algebra Z × Z (Finding 2). The twin pairs form a codimension-one line there,
    and the thin coordinate is a single point (Finding 4).
  - The Lemma 6 shape fails for the split form's roots by a factor ≥ (4/17)N for N ≤ D/16, i.e. ≫ D at N ≍ D. The
    failure is on the unbalanced part, and it is irrelevant for n(n+2) itself, whose Type I sums are elementary
    (Finding 3b).
  - Type I on λ is trivial in closed families (Finding 1) and equals the class's twisted input on the twin line
    (Finding 2b).
- **Does a twin-adjacent norm-form family?**
  - Anisotropic families (x² + h, h not minus a square; norm forms of fields) carry the sieve, but a prime norm there is
    ONE prime, not a fixed-shift pair.
  - Isotropic families encode pairs only through their split factorisation, at λ_A = +1 (Finding 2a), or as averaged
    shifts (Finding 4).
  - No placement examined satisfies the success criterion. Each falls under (i), (ii) or (iii). Classification:
    located; this route does not help.

## Checks

- code/parity/merikoski_root_large_sieve.py (`/usr/bin/python3 -I`, about 3 s, well under 1 GB; numpy 2.5.3),
  output code/parity/merikoski_root_large_sieve.out.
- The lower bound in Finding 3(b) was checked against the computed Δ. At D = 1000, N = 30 the bound is
  (1000 − 240)·30/2 = 11400 ≤ 54475. Finding 3(b) itself is the elementary bound and needs no computation.

## First unresolved implication

On this route there is no placement examined in which the large sieve gives information beyond the trivial level or
the class's input. The first unresolved step is the one already recorded on the 2026-11-14 card: (B-twin), FI's
μ-twisted bilinear condition for Λ(· + 2),
  Σ_m |Σ_{N<n≤2N, mn≤x} γ(n, C) μ(mn) Λ(mn + 2)| ≤ x (log x)^{−2^{22}},
in the component-respecting factorisations of the split algebra. The large sieve over roots does not address it.

For the Type I side alone, the first open hypothesis is two-point Chowla with major-arc twists at power-of-log precision
(Finding 5). It would give GS-type Type I for product weights λ(x)λ(x+2)·f′(y), but that only confirms the obstruction's
input.

## Literature scope (what was and was not checked)

- Checked: Merikoski 2112.03617v3 §§1, 3; GS 2410.04189v3 pp. 3, 20–21 and ref. [16]; GMPP 2610.41356v1 §1. A web
  search found no posting of GS [16] (Corners in the Gaussian primes).
- Not checked:
  - the actual multiplicative-large-sieve argument (unpublished);
  - FI98b Lemma 3.2 and its proof;
  - Merikoski 2302.11331;
  - the GS proof of Prop. 4.2 (§5);
  - the GMPP Type II argument;
  - whether Finding 3(b) (root clustering for split quadratics, i.e. isotropy) is stated in the literature. It is
    surely folklore: equidistribution of roots of quadratic congruences is classically stated for irreducible
    polynomials.

## No parity-breaking content

Nothing in this card separates the twin weight from a fair Liouville-pattern weight. Every estimate found is either
trivial, or a twisted Type I input of the paper's class, or circular. Twin primes remain OPEN.

## Audit (fresh context, adversarial)

Every item was applied to this card. Script changes were to the docstring and labels only, and the rerun reproduced
the same numbers.

- **Errors**
  - (1) "Fails by a factor ≫ min(N, D)" was false for general N. Fixed: the factor is ≥ (4/17)N for N ≤ D/16, which is
    ≫ D at N ≍ D. Added the upper bound Δ ≤ N + D² from 1/D² spacing, so the loss is about min(N, D²/N).
  - (2) "Within 1/d of rationals whose denominator divides d" was vacuous. Fixed: for odd d, the denominator divides
    min(d₁, d₂) ≤ √d.
  - (3) "(u/d₁, (u+2)/d₂) not on the line unless d₁ = d₂ = 1" was false. Fixed: "in general not on it", with the
    counterexample u = 6 → (2, 4).
  - (4) The general Σ α_m β_k Λ(mk+2) is not FI98's (B). Fixed: β_k = γ(k, C)μ(mk) gives (B-twin), and the general form
    is stronger. The first unresolved implication is restated as (B-twin) in FI's μ-twisted form.
  - (5) Lemma 3.2 is in FI98b (X² + Y⁴), not FI98. Fixed in the sources and literature scope here, and in the script
    docstring.
- **Gaps and overstatements**
  - Classification softened to "located (this route does not help; Merikoski's multiplicative-large-sieve argument
    itself is unpublished and unread)"; "no-go met" was removed (header, Outcome, Answers).
  - "Needs (i) ... (ii)" was changed to "Merikoski's argument uses".
  - Added that Type I for d | n(n+2) is elementary, so the root-sieve failure on the unbalanced part is irrelevant
    rather than an obstruction, and that on the balanced part the sieve behaves well (header, after Finding 3, Answers).
  - The first unresolved implication now reads "no placement examined in which it gives information beyond the
    trivial level or the class's input".
  - Finding 4 and the Answers were restricted to the Poisson + root-sieve scheme with a one-point thin set.
  - Clustering is now marked as distinctive only on the unbalanced/trivial part, with odd d required (d = 8, ν = 3
    noted).
  - "≍ 1/(q√d)" is now stated only for q ≤ c√d, and the spacing sentence is labelled heuristic.
  - The (log x)^{c₀} statement is now described as log-averaged, for Selberg-square weights, conditional on TT25, and
    not per-modulus.
  - TT25 Thm 3.1(ii) natural-density bounds outside exceptional scales are now mentioned in Finding 5.
- **Slips**
  - x² − 2 is now called indefinite: "any anisotropic form (for indefinite ones, for q ≪ √d)".
  - The "trivial" row and the script label were relabelled "odd part of d divides ν − 1 or ν + 1".
  - "Exact top eigenvalue" was changed to "computed numerically in double precision (eigvalsh)".
  - γ_n now carries Δ₂(bc), not "the discrepancy".
  - κ₁ and b > 0 were added to the definition of a_n.
  - Type I is now said to use the Gaussian structure only through the roots ν; the factorisation wz = b² + 1 + ia is
    used only in Type II.
  - "Twin elements" was changed to "twin-prime elements (p, p+2)".
  - The ramified case was added to Finding 1 (it holds).
  - f in Finding 5 is now called O(1)-bounded.
  - The Proc. LMS (3) 127 (2023) 1057–1133 citation was taken from GS ref. [39].
