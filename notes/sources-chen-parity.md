# Sources: Chen's theorem, the parity problem, Selberg–Delange, Pintz's λ(p+d) result

Literature check. Date accessed for every source: **2026-11-16**.
Only sources I actually downloaded and read are marked `read`. PDFs were fetched with curl from
arxiv.org and converted with `pdftotext -layout`. Blog pages were fetched from terrytao.wordpress.com
and converted to text. Page numbers are the page numbers of the arXiv PDF (as printed by
`pdftotext -f N -l N`), not those of the journal versions. Quotes are verbatim from the extracted text.
Formulas are re-typed from the PDF text layer, so minor typographical differences are possible.

Normalisation key used below:
- C_2 := ∏_{p>2} (1 − 1/(p−1)^2) ≈ 0.6601... (the usual twin-prime constant; I did not verify the numerical value in any source).
- Wu's and Lichtman's Π(x) := 2 C_2 x/(log x)^2 (Wu writes C = 2∏_{p>2}(1 − 1/(p−1)^2); Lichtman writes
  Π(x) = (2x/(log x)^2) ∏_{p>2} (1−2/p)/(1−1/p)^2, which is the same thing).
- **Caution:** R. Li (arXiv:2405.05727) writes `C_2 = 2∏_{p>2}(1 − 1/(p−1)^2)`, i.e. his "C_2" already contains the factor 2.
  So Li's `c · C_2 x/(log x)^2` = `c · Π(x)` in Wu's normalisation.
- Tao (254A notes) writes `2Π_2 x/log^2 x` for the Hardy–Littlewood main term, i.e. Tao's Π_2 = C_2.

---

## Q1. Chen's theorem with explicit constants; twin-prime upper bound constant

### 1.1 J. Wu, "Chen's double sieve, Goldbach's conjecture and the twin prime problem"
- Identifier: arXiv:0705.1652v1 (submitted 11 May 2007), https://arxiv.org/abs/0705.1652. Header says
  "Acta Arithmetica 114 (2004), 215–273".
- Status: **read** (pp. 1–4 of the intro in full).
- Definitions (p. 3): "π2 (x) := |{p ⩽ x : Ω(p + 2) = 1}|"; "(1.6) π2 (x) ∼ Π(x)" with
  "Π(x) := Cx/(log x)^2 and C := 2 ∏_{p>2} (1 − 1/(p − 1)^2)".
- Upper bounds (p. 3): "upper bounds of this type (1.7) π2 (x) ⩽ {a + o(1)}Π(x)" ... "In particular Wu [26]
  obtained 3.418 ... Recently Cai & Lu [6] improved the constant 3.418 to 3.406."
- **Theorem 3 (p. 4):** "For sufficiently large x, we have π2 (x) ⩽ 3.3996 Π(x)."
- Chen's lower bound (p. 4): "As an analogue of Theorem 2, Chen [7] proved that (1.8) π1,2 (x) ⩾ 0.335 Π(x) (x ⩾ x0 ),
  where π1,2 (x) := |{p ⩽ x : Ω(p + 2) ⩽ 2}|." ... "In particular he [Cai] obtained 1.0974 in place of 0.335,
  which is an improvement of Wu's constant 1.05 [26]."
- **Theorem 4 (p. 4):** "For sufficiently large x, we have π1,2 (x) ⩾ 1.104 Π(x)."
- Also relevant to Q2/Q3 (p. 2): the linear sieve bounds "are the best possible in the sense that taking
  A = Bν := {n : 1 ⩽ n ⩽ x, Ω(n) ≡ ν (mod2)} (ν = 1, 2), the upper and lower bounds in (1.3) are respectively
  attained by ν = 1 and ν = 2 (see [14], page 239)."
- Goldbach analogues (pp. 2–3): Theorem 1 "D(N ) ⩽ 7.8209 Θ(N )"; Theorem 2 "D1,2 (N ) ⩾ 0.836 Θ(N )".

### 1.2 J. Wu, "Chen's double sieve, Goldbach's conjecture and the twin prime problem, 2"
- Identifier: arXiv:0709.3764v1 (24 Sep 2007). (Journal: Acta Arith. 131 (2008), 367–387, as cited by Li below.)
- Status: **read** (intro, pp. 1–3). This paper only treats the Goldbach version D_{1,2}(N).
- p. 2: "Theorem. For sufficiently large N , we have D1,2 (N ) ⩾ 0.899 Θ(N )." with Θ(N) = C_N N/(log N)^2.
- No new twin-prime constant in this paper.

### 1.3 J. D. Lichtman, "A modification of the linear sieve, and the count of twin primes"
- Identifier: arXiv:2109.02851v2 (14 Feb 2024); journal Algebra & Number Theory 19 (2025) 1–38 (as cited in Li's v4 bibliography).
- Status: **read** (pp. 1–3, and the end of §6.3).
- p. 3: "(1.5) π2 (x) ∼ (2x/(log x)^2) ∏_{p>2} (1 − 2/p)/(1 − 1/p)^2 =: Π(x)."
- **Theorem 1.2 (p. 3):** "As x tends to infinity, we have π2 (x) . 3.29956 Π(x)." (". " = "≲")
- p. 3: "Theorem 1.2 gives a 2.94% refinement from the previous record bound of Wu [21]."
- Chronology table (p. 3), column "π2 (x)/Π(x) ≲": "1966 Bombieri–Davenport 4", "1978 Chen 3.9171",
  "1986 Bombieri–Friedlander–Iwaniec 3.5", "1990 Wu 3.418", "2003 Cai–Lu 3.406", "2004 Wu [21] 3.39951".
- §6.3: "in [21, Theorem 3] Wu obtained π2 (x)/Π(x) . (7/2)(1 − H4/7 (2.1)) ⩽3.39951." So Wu's stated
  3.3996 is the rounding of 3.39951.
- Abstract: level of distribution "x^{10/17}" for the modified linear sieve weights.

### 1.4 R. Li, "On Chen's theorem, Goldbach's conjecture and almost prime twins II"
- Identifier: arXiv:2405.05727v4 (31 May 2025). The arXiv listing has v1 (9 May 2024), v2 (13 May 2024),
  v3 (22 May 2024), v4 (31 May 2025). v4 carries the title "... II"; its bibliography cites v3 as
  "[13] R. Li. On Chen's theorem, Goldbach's conjecture and almost prime twins. arXiv e-prints, page arXiv:2405.05727v3, 2024."
  **Preprint; I found no indication of refereed publication.**
- Status: **read** (pp. 1–2; checked Theorem 1.3's statement in §5). I did not check the numerics.
- p. 2: "(5) π1,2 (x) = |{p : p ⩽ x, p + 2 = P2 }|", "In 1973 Chen [5] showed simultaneously that
  π1,2 (x) ⩾ 0.335 C2 x/(log x)^2, (6) where C2 = 2 ∏_{p>2} (1 − 1/(p − 1)^2)".
  (P_r is defined on p. 1: "Pr denote an integer with at most r prime factors counted with multiplicity".)
- History (p. 2): "improved successively to 0.3445, 0.3772, 0.405, 0.71, 1.015, 1.05, 1.0974, 1.104, 1.123, 1.13
  by Halberstam [10], Chen [7] [6], Fouvry and Grupp [9], Liu [17], Wu [20], Cai [1], Wu [21], Cai [2] and Cai [3]
  respectively. In [13] we increase this constant to 1.238 by similar methods."
- **Theorem 1.3 (p. 2):** "π1,2 (x) ⩾ 1.2759 C2 x/(log x)^2." Uses Pascadi's distribution level ("Recently,
  Pascadi [18] got a powerful new distribution level for primes").
- Goldbach analogue, Theorem 1.1 (p. 1): "D1,2 (N ) ⩾ 1.9728 C(N )N/(log N )^2".
- Since Li's C2 is 2C_2, this is π_{1,2}(x) ≥ 1.2759 Π(x) in Wu's/Lichtman's normalisation.

**Summary for Q1 (all in the normalisation Π(x) = 2C_2 x/(log x)^2):**
- Lower bound for #{p ≤ x : Ω(p+2) ≤ 2}: Chen 0.335 → Wu 2004 1.104 (refereed) → Cai 1.123, 1.13 (only quoted by Li, not read)
  → Li 1.238 (v3 preprint, not read separately) → **Li 1.2759** (arXiv v4 preprint, read).
- Upper bound for π_2(x): Wu 2004 3.3996 (precisely 3.39951) → **Lichtman 3.29956** (ANT 2025, read).
- I did not look for, and so did not find, anything newer than Lichtman for the upper bound.

---

## Q2. Is "p+2 a semiprime (exactly two prime factors) infinitely often" known? Why does Chen escape parity?

**Finding:** None of the sources I read claims a proof that p+2 = (exactly two primes) for infinitely many
primes p. Several state the sieve limitation as "one cannot tell whether it has one or two prime factors".
Tao (2007) says plain sieve theory cannot "just count semiprimes". Pintz says that even the odd-Ω
version is not known. I found no source saying in so many words "it is open whether p+2 is a semiprime infinitely often".

### 2.1 T. Tao, "Open question: The parity problem in sieve theory" (blog, 5 June 2007)
- URL: https://terrytao.wordpress.com/2007/06/05/open-question-the-parity-problem-in-sieve-theory/
- Status: **read** (main text; comments not read in full).
- Statement: "Parity problem. If A is a set whose elements are all products of an odd number of primes (or are
  all products of an even number of primes), then (without injecting additional ingredients), sieve theory is
  unable to provide non-trivial lower bounds on the size of A. Also, any upper bounds must be off from the
  truth by a factor of 2 or more."
- **The key sentence for both parts of Q2:** "Thus we can hope to count P_2 almost primes (because they can have either an odd or an
  even number of factors), or to count numbers which are the product of 6 or 7 primes (which can for instance
  be done by a sieve of Bombieri), but we cannot hope to use plain sieve theory to just count primes, or just
  count semiprimes (the product of exactly two primes)."
- Chen: "which can be used for instance to derive Chen's theorem that there are infinitely many primes p such
  that p+2 is a P_2 almost prime".
- Liouville: "Thus the parity problem applies whenever λ is identically +1 or identically -1 on the set A of interest."

### 2.2 J. Pintz, "An approximation to the twin prime conjecture and the parity phenomenon"
- arXiv:1004.1065v1 (7 Apr 2010). Journal: Indag. Math. (N.S.) 26(5) (2015) 883–896 (per OpenAlex record,
  DOI 10.1016/j.indag.2015.09.008, and per the citing papers below).
  **Note: the title differs from the one in the task ("Primes in short intervals ... and parity").**
- Status: **read** (pp. 1–5).
- p. 1: "The celebrated theorem of Chen [Che1], [Che2] proved nearly 50 years ago asserts that there are
  infinitely many primes p for which p+2 is either a prime or has exactly two prime factors. In view of this
  strong approximation of the twin prime conjecture seems to be a surprise that it is not known whether there
  are infinitely many primes p such that p + 2 has an odd number of prime factors."
- p. 1, quoting Hildebrand: "the so-called parity barrier, a heuristic principle according to which sieve methods
  cannot differentiate between integers with an even and odd number of prime factors."
- p. 1, quoting Iwaniec (**secondary**: I did not open Iwaniec's text): "Never mind producing primes; we cannot even
  produce numbers having either one, three, five or seven prime divisors. However, under the best circumstances we
  can obtain numbers having either 2006 or 2007 prime divisors. Similarly we can obtain numbers having either one
  or two prime divisors, but we are not able to determine which of these numbers are there, probably both."
- p. 2, Remark after Theorem 1': "Theorem 1' remains true if λ(p+d) = −1 is replaced by λ(p+d) = 1." (This is
  the even-Ω, i.e. semiprime-parity, side. It holds only inside the dichotomy of Theorem 1', not for a fixed d.)
- p. 3: "However, even assuming the Elliott–Halberstam conjecture we cannot prove the existence of infinitely
  many primes p with λ(p + d) = −1 for even a single a priori given d."

### 2.3 J.-J. Huang, H. Li, "On the connection between the Goldbach conjecture and the Elliott-Halberstam conjecture"
- arXiv:2005.03811v2 (28 Aug 2022). Status: **read** (pp. 1–2).
- pp. 1–2: "The barrier from Chen's theorem to the Goldbach conjecture has been well known as the parity problem
  in sieve theory: one can not tell whether q = N − p has exactly one or two prime divisors."

### 2.4 T. Tao, "254A, Notes 4: Some sieve theory" (blog, 21 Jan 2015), §5 "The parity problem"
- URL: https://terrytao.wordpress.com/2015/01/21/254a-notes-4-some-sieve-theory/ . Status: **read** (§5).
- Proposition 47 (Abstract parity barrier, informal) and then: "in which case the parity problem asserts (roughly
  speaking) that the sifting problem must allow both numbers with an even number of prime factors and numbers
  with an odd number of prime factors to survive if one is to have any hope of good lower bounds."
- "Corollary 48 (Parity barrier for twin primes) (Very informal) One cannot use traditional sieve methods to
  resolve the twin prime conjecture."
- Exercise 49: "argue that any sieve-theoretic bound must in fact be off from the truth by a factor of at least four."

### 2.5 T. Tao, "254A, Supplement 5: The linear sieve and Chen's theorem (optional)" (blog, 29 Jan 2015)
- URL: https://terrytao.wordpress.com/2015/01/29/254a-supplement-5-the-linear-sieve-and-chens-theorem-optional/
  Status: **read** (statement and parity part only).
- "Theorem 5 (Chen's theorem) There are infinitely many primes p such that p+2 is the product of at most two primes."
- "The optimality of F, f is closely related to the parity problem obstruction discussed in Section 5 of Notes 4".
- The proof sketch states the goal as producing p with "p+2 ... the product of at most two primes, each of which is at least p^{1/8}".

### 2.6 T. Tao, "Notes on the Bombieri asymptotic sieve" (blog, 17 July 2016)
- URL: https://terrytao.wordpress.com/2016/07/17/notes-on-the-bombieri-asymptotic-sieve/ . Status: **read** (intro).
- This is the most precise statement I found about the "semiprime + 2 = prime" count. Conditional on EH, for
  n = p_1⋯p_r, the sum Σ g_r(log p_1/log n, …) Λ(n+2) "was equal to (δ_x+o(1)) ∫ g_r x/log x (7) when r was odd
  and (2−δ_x+o(1)) ∫ g_r x/log x (8) when r was even", for one unknown scalar δ_x ∈ [0,2]. Also: "the twin prime
  conjecture would be proved if one could show that δ_x is bounded away from zero"; "no additional bound beyond
  the inequalities 0 ≤ δ_x ≤ 2 provided by the Bombieri asymptotic sieve is known, even if one assumes all other
  major conjectures in number theory than the prime tuples conjecture and its variants".
- Parity condition: "Σ_{r odd} ∫ g_r = Σ_{r even} ∫ g_r is obeyed (informally: f gives the same weight to
  products of an odd number of primes as to products of an even number of primes ...)".
- **My inference, not stated by Tao:** take r = 2. On EH, the weighted count of primes q = n+2 with n = p_1 p_2
  (both factors ≥ x^ε) is (2 − δ_x) × (main term). It would be 0 if δ_x = 2. So a positive lower bound for
  "prime − 2 = semiprime" is exactly as hard as showing δ_x ≤ 2 − c. That is the mirror image of the
  twin-prime problem (δ_x ≥ c). The P_2 count (r=1 plus r=2) gets δ_x + (2 − δ_x) = 2, so δ_x cancels. This is
  the mechanism by which Chen-type statements are parity-insensitive. Tao's post concerns shift n+2 with n
  almost prime. The question p prime, p+2 semiprime has the opposite sign of shift; I assume it is analogous.

### 2.7 Polymath, "Variants of the Selberg sieve, and bounded intervals containing many primes", §8 "The parity problem"
- arXiv:1407.4897v4 (22 Dec 2014). Status: **read** (§8, pp. 68–69).
- p. 68: "In this section we argue why the "parity barrier" of Selberg [57] prohibits sieve-theoretic methods,
  such as the ones in this paper, from obtaining any bound on H1 that is stronger than H1 ≤ 6".
- Uses the weight ω(n) = (1 − λ(n)λ(n+2))(1 − λ(n+2)λ(n+6)) (p. 69).

### 2.8 K. Soundararajan, "The work of James Maynard" — arXiv:2207.03463v1 (7 Jul 2022). Status: **read** (p. 4).
- "Chen's theorem and Iwaniec's theorem exhibit a limitation of traditional sieve methods, known as the parity
  problem, which often prevents us from knowing the parity of elements left unsieved, and thus from producing
  prime numbers."

### 2.9 Not openable / not found
- M. R. Murty, A. Vatwani, "Twin primes and the parity problem", J. Number Theory 180 (2017) 643–659.
  URL tried: https://mast.queensu.ca/~murty/TwinPrimes-Parity.pdf. Result: HTTP 200, but the body is the
  HTML homepage of Ram Murty, not a PDF. **blocked (redirect to homepage, no PDF content)**. Contents not known to me.
- MathOverflow: my searches returned no MO thread on "p+2 exactly semiprime". No MO page opened.
- Wikipedia "Chen's theorem" talk page: not opened.

---

## Q3. Selberg–Delange for Σ z^{Ω(n)}; 1/Γ(z) and the parity problem

### 3.1 Tenenbaum, *Introduction to Analytic and Probabilistic Number Theory* (3rd ed., AMS 2015)
- **Not opened.** I did not try a publisher page. Everything below about the book is **secondary only**.

### 3.2 M. Klazar, "Lecture 7. The prime number theorem and the Riemann hypothesis. The Selberg–Delange method. Two arithmetic applications" (lecture notes, 12 April 2024)
- URL: https://kam.mff.cuni.cz/~klazar/ACNT24lec7.pdf . Status: **read** (secondary source for Tenenbaum).
- p. 1: "we cover Chapter II.4 ..., Chapter II.5. The Selberg–Delange method and Chapter II.6. Two arithmetic
  applications in G. Tenenbaum's book [7], up to page 317." ([7] = 3rd ed., AMS 2015.)
- p. 3: "The following are Theorems 6.1–6.6 in [7]." So Klazar's Theorem 15 corresponds to **Tenenbaum Thm II.6.2**
  (by order; my reading).
- **Theorem 15 (p. 4):** "For δ ∈ (0, 1) there exist c1 = c1 (δ), c2 = c2 (δ) > 0 such that it holds uniformly for
  x ≥ 3, |z| ≤ 2 − δ and N ∈ N0 that Σ_{n≤x} z^{Ω(n)} = x(log x)^{z−1} ( Σ_{k=0}^N νk (z)/(log x)^k + Oδ (RN (x)) )
  where RN (x) is defined in the previous theorem and where νk (z) := (1/Γ(z − k)) Σ_{h+j=k} (1/(h!j!)) G2^{(h)} (1, z)γj (z)."
  Here R_N(x) = exp(−c1 √log x) + ((c2 N + 1)/log x)^{N+1} (Theorem 14), and γ_j are the Taylor coefficients of
  Z(s,z) := ((s−1)ζ(s))^z, with Z(1,z) = 1 (Theorem 10, p. 3).
- Klazar does not write out G_2 explicitly. In his general setup (p. 3) G(s,z) = F(s)ζ(s)^{−z}. For
  F(s) = Σ z^{Ω(n)} n^{−s} = ∏_p (1 − z/p^s)^{−1} this gives G_2(1,z) = ∏_p (1 − z/p)^{−1}(1 − 1/p)^z
  (**my computation**). With N = 0 this gives the formula in the question:
  Σ_{n≤x} z^{Ω(n)} = x(log x)^{z−1}(G(z)/Γ(z) + O(1/log x)), uniformly for |z| ≤ 2 − δ.
- p. 4 also has ν(z) = (1/Γ(z+1)) ∏_p (1 − z/p)^{−1}(1 − 1/p)^z (the "/" in the PDF text layer is missing a "p").

### 3.3 A. Granville, D. Koukoulopoulos, "Beyond the LSD method for the partial sums of multiplicative functions"
- arXiv:1710.01389v3 (19 Feb 2018); Ramanujan J. (2019). Status: **read** (pp. 1–3).
- p. 2: "Tenenbaum's book [8] contains a detailed description of the LSD method along with a general theorem ...
  Theorem II.5.2 in [8, pp. 281] implies that (1.1) Σ_{n≤x} f (n) = x Σ_{j=0}^{J−1} c̃j (log x)^{α−j−1}/Γ(α − j)
  + O_{J,f}(x(log x)^{Re(α)−J−1})". Also: "c0 = c̃0 = ∏_p (1 + f(p)/p + f(p^2)/p^2 + ⋯)(1 − 1/p)^α."
- p. 2, footnote 1: "The method is often called the Selberg-Delange method, or even Selberg's method, but a key
  idea appears in Landau's work long before Selberg's and Delange's papers."
- No discussion of the parity problem or of sieves in the part I read (grep for "parity" found nothing).

### 3.4 D. Koukoulopoulos, "On multiplicative functions which are small on average"
- arXiv:1111.2659v5 (17 Jun 2013) (GAFA 2013; I did not verify the journal). Status: **read** (pp. 1–3).
- **p. 3 (closest statement to the "1/Γ vanishes at −1" point):** "if f (p) is equal to v ∈ U on average, then by
  the Selberg-Delange method [Ten, Chap. II.5] we expect that (1.3) Σ_{n≤x} f (n) = (cf,v /Γ(v) + of (1)) x(log x)^{v−1}
  (x → ∞), where cf,v is some non-zero constant and Γ denotes Euler's Gamma function. Therefore, unless v is a
  pole of Γ, relation (1.2) cannot hold for any A > 2 ≥ 1 − ℜ(v). The only poles of Γ in the unit circle are
  located at −1 and at 0. If now v = −1, then f looks like the Möbius function µ which satisfies (1.2) by a
  quantitative form of the prime number theorem." Here (1.2) means Σ_{n≤x} f(n) ≪_A x/(log x)^A, and U is the closed unit disc.
- Also p. 3: "this is obviously false, as the completely multiplicative function (−1)^{Ω(n)} n^{it} also satisfies (1.2)".
- **Not a sieve/parity statement.** The paper links the zero of 1/Γ at −1 to Möbius/Liouville-type cancellation.
  It does not link it to the sieve's parity problem or to sieve dimension.

### 3.5 Search result on the "sieve dimension z" / parity interpretation
- **Found nothing.** I found no openable source that explains the parity problem through 1/Γ(z) vanishing at z = −1,
  or that says the sieve sees z^{Ω} as a sieve of dimension z.
  Queries (WebSearch, standard): `"z^{\Omega(n)}" Selberg-Delange "|z| < 2" asymptotic Gamma(z) Tenenbaum Theorem II.6.2 arXiv`;
  `parity problem "1/\Gamma" Selberg-Delange Liouville "z^{\Omega(n)}" sieve dimension z mean value vanishes z=-1`;
  `"sieve of dimension" "-1" Liouville function "Gamma" parity Selberg-Delange "z = -1" ...`;
  `"Opera de Cribro" parity "sieve dimension" kappa Gamma(kappa) "1/\Gamma" ...`;
  `terrytao.wordpress.com 254A notes sieve theory parity problem Selberg-Delange Gamma function`.
  Friedlander–Iwaniec *Opera de Cribro* and Koukoulopoulos's book were **not opened**: no openable copy came up in the searches.
- Tao's 254A Notes 4 (read, §2) uses the term "sieve dimension" κ for densities g(p) ≈ κ/p. In the parts I read
  it does not connect κ to z^{Ω} or to Γ.
- **Caveat about the premise:** by the formula in 3.2, for |z| = 1, z ≠ 1, the main term already has size
  x(log x)^{Re z − 1} = o(x). So every z ≠ 1 on the unit circle has mean value 0 in the o(x) sense, and z = +1 has
  mean 1. What is special about z = −1 is that every coefficient ν_k(−1) carries 1/Γ(−1−k) = 0, so the sum is
  smaller than any power of log (cf. Koukoulopoulos's "unless v is a pole of Γ"). The phrase "only z = ±1 have
  negligible mean" in the task is therefore not right as stated (my analysis, not from a source).

---

## Q4. Improvements of Pintz's "|d| ≤ 16" via Maynard–Tao weights?

### 4.1 Pintz arXiv:1004.1065v1: what is proved (read, pp. 2–4)
- "Theorem 1. There exists an even number d such that 0 < |d| ≤ 16 and λ(p + d) = −1 for infinitely many primes p."
- "Theorem 1'. At least one of the following two assertions is true: (i) There exists an even d with |d| = 2, 4 or 8,
  such that λ(p + d) = −1 for infinitely many primes p; (ii) lim inf (pn+1 − pn ) ≤ 16."
- "Theorem 1". There exists a positive even d ≤ 18 such that λ(p + d) = −1 for infinitely many primes p."
- Theorem 2: "an odd b ≤ C and a d with 0 < |d| ≤ 30 such that P − (p + d) > p^c , Ω(p + d) = b for infinitely many primes p."
- Theorem 3 (p. 3): it rests on GPY with an admissible 6-tuple ("H0 = {0, 4, 6, 10, 12, 16} ... Choosing r = 8 we obtain Theorems 1 and 1'").
- Conditional (p. 5, Remark A): "If ϑ > 0.729, then we have a d with 0 < |d| ≤ 2 such that λ(p+d) = −1 for infinitely many primes p."

### 4.2 Search for later improvements: **nothing found**
- WebSearch (standard) queries used:
  `Liouville function shifted primes λ(p+d) = -1 infinitely many primes Maynard sieve improvement Pintz parity`;
  `"An approximation to the twin prime conjecture and the parity phenomenon" Pintz cited`;
  `"Liouville function" "shifted primes" Maynard-Tao bounded "odd number of prime factors" p+h infinitely many primes`;
  `Pintz parity phenomenon 2016 2018 survey "λ(p+d)" improvement Maynard weights almost primes odd number prime factors bounded gaps`;
  `"Pintz" "λ(p + d) = −1" OR "λ(p+d)=-1" OR "lambda(p+h)=-1" improved Maynard sieve parity theorem`.
- Citation list: Semantic Scholar API, `paper/DOI:10.1016/j.indag.2015.09.008/citations` (same result for `arXiv:1004.1065`),
  gave 10 citing items: Cantarini 2026 (arXiv:2607.09110); Lichtman–Teräväinen 2021 (arXiv:2111.08912);
  Tao–Teräväinen 2021 (arXiv:2109.06291); Huang–Li 2020 (arXiv:2005.03811, plus a variant paper);
  Murty–Vatwani 2017; Pintz 2010/2012 (AP in twin primes II); Kim–Kim–Kim 2026; Carella 2022.
  OpenAlex reports cited_by_count = 12, but its citing-works query failed: "Rate limit exceeded ... Insufficient budget"
  (not retried, no key used).
- I read the Pintz citations in the three arXiv citing papers I opened:
  - Lichtman–Teräväinen, arXiv:2111.08912v3, p. 3: "It is a folklore conjecture and a well-known model case for
    the parity problem in sieve theory that Σ_{p≤X} µ(p + h) = o(π(X)) for any fixed shift h ≠ 0. This has appeared
    in print (for h = 1) at least since Hildebrand [9]; see also Pintz [21] and Murty–Vatwani [19, (1.2)]." (They prove
    an averaged-over-h version, not a bounded-d result.)
  - Tao–Teräväinen, arXiv:2109.06291v2: "Corollary 1.8(iii) relates to the conjecture (considered in e.g. [23], [25],
    [15], [16]) that Σ_{|h|<p≤x} λ(p + h) = o(π(x)), proving it for infinitely many x under the existence of infinitely
    many Siegel zeros". [23] = Pintz.
  - Huang–Li, arXiv:2005.03811v2: cites Pintz [12] only in a list, "the parity barrier in different settings [2, 3, 4, 12, 14]".
  None of them improves 16.
- Pintz, "Polignac numbers, conjectures of Erdős on gaps between primes, arithmetic progressions in primes, and the
  bounded gap conjecture", arXiv:1305.6289v1 (27 May 2013). **read** (grep of the full text): no occurrence of
  "parity", "Liouville" or "λ(" in this sense. It does not revisit the 2010 result.
- Pintz's homepage publication list (https://users.renyi.hu/~pintz/List_of_publ-Janos_Pintz.pdf) opened, but it
  is old (ends at roughly the 2005–2006 AIM preprints), so it is useless for post-2013 work.
- Polymath8b (arXiv:1407.4897v4), Maynard's Annals paper and Magyar–Pintz arXiv:2505.07630v1: Polymath8b §8
  discusses parity for H_1 but not λ(p+d). 2505.07630 has no Liouville content (grep).
- **Not checked:** Google Scholar "cited by" (not used), MathSciNet/zbMATH reviews, and Pintz's later surveys other than 1305.6289.
- **Conclusion:** I found no published improvement of |d| ≤ 16 (or of d ≤ 18) via Maynard–Tao weights. This only means
  my search found nothing; it does not show that none exists.
- Observation (mine): alternative (ii) of Theorem 1' is lim inf gaps ≤ 16. The unconditional Maynard–Polymath
  bound is far larger (Tao's Notes 4, read: "the current record being H=246"), so it does not settle the dichotomy.
