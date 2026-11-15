# Quantitative two-point logarithmic Chowla: rates and uniformity (shift, dilation, progression)

These are source notes for the open step of paper Prop. `prop:tao-weight` (papers/parity-barrier/main.tex) and the route card
notes/parity-attempts/2026-11-15-tao-twisted-typeI-weights.md. The question: how fast may the sieve level R(x) grow?
They were compiled 15 Nov 2026 (Session 17 helper) from arXiv PDFs. The PDFs were downloaded to the scratchpad directory, read with
`pdftotext -layout` and are not committed.

**Q:** marks a quote from the PDF. The words are verbatim; formulas are re-typed from the pdftotext rendering, so subscripts and
superscripts are linearised. Page numbers are the printed page numbers. **Mine:** marks the helper's reading.

**Status warning.** Of the seven sources, only Tao16 has a journal version (Forum Math. Pi 4 (2016) e8). The rest are arXiv preprints
with no journal reference on arXiv as of 15 Nov 2026. Three of them are 2026 preprints that are recent and, as far as we know,
unrefereed: Tao–Teräväinen (2512.01739), Guo (2608.23500) and Hughes (2609.28526). Guo's paper says that "OpenAI Codex was used as an
AI research assistant ... developing and checking arguments" (v2 p. 20). Treat everything from these three as **Claimed**.

| # | arXiv id | version read | SHA-256 of the PDF |
|---|---|---|---|
| T16 | 1509.05422 (Tao) | v4, 29 Jul 2016 | 467329ae414b669808555fddf131be3bc07025777ae3af8ccdea6e98db6722e9 |
| HR | 2103.06853 (Helfgott–Radziwiłł) | v2, 13 Apr 2021 (latest) | ab3809a4c5c7e9928cf8954c1a4651036d29f4abc2cc146ce574abdd7cd691cf |
| P | 2310.19357 (Pilatte) | v3, 25 Aug 2026 (latest) | f23e885ae2c4b28d5c3afe618865f7b961e2d67607d9f224f0ca5a39a9172f12 |
| TT | 2512.01739 (Tao–Teräväinen) | v2, 25 Apr 2026 (latest) | ce10e83b10c6544e1dbff037a5e4efa0e387892e0fc596ae09dce76025d7b41e |
| G2 | 2608.23500 (Guo) | v2, 25 Aug 2026 | e100958d0dff32780d63ccbe2f3c0a31112490e819e4efbc2cfe2a312f4fb3cd |
| G4 | 2608.23500 (Guo) | v4, 1 Sep 2026 (latest; retitled) | 95861fcc574a53c0cfc8985093b2fd62340eacdbbddd616e1bd53f0f6ed1c0a4 |
| Hu | 2609.28526 (Hughes) | v1, 22 Sep 2026 (latest) | a54f900da7c070d37ac67cae962b8f67c22ea993e2f8d0cfaf48b98011051467 |
| CR | 2412.17583 (Charamaras–Richter) | v3, 17 Aug 2026 (latest) | e5c861fd31615f8695aa5ec58deb8da22b7a0d2259b8fa0c9d532a35d64db248 |

Every download succeeded (HTTP 200). Found but not used: Tao–Teräväinen arXiv:1708.02610v2 (qualitative structure theorem;
SHA-256 232bdb1a…6aa276ad).

---

## 1. Tao16 (baseline): arXiv:1509.05422v4

- Thm 1.2 (p. 2). Q: "Let a1, a2 be natural numbers, and let b1, b2 be integers such that a1 b2 − a2 b1 ≠ 0. Let 1 ≤ ω(x) ≤ x be a
  quantity depending on x that goes to infinity as x → ∞. Then one has Σ_{x/ω(x)<n≤x} λ(a1 n + b1)λ(a2 n + b2)/n = o(log ω(x))".
- Thm 1.3 (p. 5). Q: "Let ε > 0, and suppose that A is sufficiently large depending on ε, a1, a2, b1, b2. Let x ≥ ω ≥ A, and let
  g1, g2 : N → C be multiplicative functions with |g1(n)|, |g2(n)| ≤ 1 for all n, with g1 "non-pretentious" in the sense that
  Σ_{p≤x} (1 − Re g1(p)χ(p)p^{−it})/p ≥ A (1.6) for all Dirichlet characters χ of period at most A, and all real numbers t with
  |t| ≤ Ax. Then |Σ_{x/ω<n≤x} g1(a1 n + b1)g2(a2 n + b2)/n| ≤ ε log ω."
  - Remark 1.4 (p. 5). Q: "Our arguments are in principle effective, and would yield an explicit value of A as a function of
    ε, a1, a2, b1, b2 if one went through all the arguments carefully, however we did not do so here".
  - Footnote 2 (p. 5). Q: "the decay rate ... is something like O(log x/(log log log x)^c) ... the dependence of A on 1/ε ... appears to
    be roughly triple-exponential".
- Cor 1.5 (pp. 5–6) is the asymptotic version under (1.8). **Mine:** twists by Dirichlet characters are allowed: g1 = λχ is
  1-bounded and multiplicative, and it is non-pretentious in the sense of (1.6) for χ of bounded modulus. There is no uniformity in
  the modulus.

## 2. Helfgott–Radziwiłł: arXiv:2103.06853v2, "Expansion, divisibility and parity"

- Main Theorem (p. 4) is the spectral statement for the divisibility graph. For the Liouville function the key statement is:
- **Cor 1.5 (p. 6).** Q: "For any e < w ≤ x such that w → ∞ as x → ∞, (1/log w) Σ_{x/w≤n≤x} λ(n)λ(n+1)/n = O(1/√(log log w))."
  - Rate: O(log w / (log log w)^{1/2}).
- Cor 1.6 (p. 6) is the same statement "at almost all scales".
- **Uniformity in h: none stated.** Every theorem is for the shift (n, n+1).
- **Dilations / APs.** The only statement is the Note at the end of §8.3 (p. 84). Q: "Both the main result and Corollary 1.1 are fully
  general – they do not even require multiplicativity – and, as we have just shown, deriving results such as Corollary 1.5 and 1.6
  from them is straightforward. In particular, we can replace λ(n)λ(n + 1) in Cor. 1.5 and 1.6 by λ(m1 n + a1)λ(m2 n + a2) with
  (mi, ai) = 1 and (m1, a1) ≠ ±(m2, a2); it is essentially enough to consider λ(n)χ(n), with n [sic: χ] a Dirichlet character,
  instead of λ(n)."
  - **Mine:** this covers fixed dilated forms, including our case a1 = a2 = q, after removing gcd's. It is a remark, not a theorem,
    and it gives no dependence on m_i, a_i. Hughes (p. 3) reads it the same way: "that note does not state an explicit bound for the
    dependence on the coefficients."
  - It also confirms that the character twist is the intended mechanism.
  - The proof of Cor 1.4 (p. 80) already uses residue classes mod 3 to remove the sign σ ("a congruence trick").

## 3. Pilatte: arXiv:2310.19357v3, "Improved bounds for the two-point logarithmic Chowla conjecture"

- **Thm 1.1 (p. 3).** Q: "(Logarithmic two-point Chowla correlations). For some absolute constant c > 0,
  Σ_{n⩽x} (1/n) λ(n)λ(n + 1) ≪ (log x)^{1−c}."
  - Rate: a power saving in log x, which Q: "appears to be best possible with current methods" (abstract).
- Thm 2.4 (p. 8). Q: "Let N be an integer such that log N ⩾ (log H)^{2.001}. Then
  Σ_{(p1,...,pJ)∈P1×···×PJ} Σ_{n∈(N,2N], p1···pJ | n} λ(n)λ(n + p1···pJ) ⩽ e^{O(J)} (V1···VJ)^{1/2} N."
  - Remark 2.6 (p. 8) gives the version with absolute values / arbitrary signs.
- Remark 2.8 (p. 10) gives Q: "(1/log w) ∫_{X/w}^{X} |(1/x) Σ_{n⩽x} λ(n)λ(n + 1)| dx/x ≪ 1/(log w)^c" (almost all scales).
- Scope (p. 3). Q: "The methods of this paper should generalise to a wider class of multiplicative functions through appropriate
  modifications. The complete multiplicativity of λ is only used in Proposition 3.1 and in the proof that Theorem 2.4 implies
  Theorem 1.1. The only other property of λ we use is that it is 1-bounded".
- **Uniformity in h, dilations, APs, characters: none stated.** Every statement is for the shift 1. The word "progression" occurs only
  in the internal sieve (prohibited progressions, §§7, 9, 13).

## 4. Tao–Teräväinen: arXiv:2512.01739v2, "Quantitative correlations and some problems on prime factors of consecutive integers"

**This is the statement that covers progressions, shifts and character twists uniformly.**

- **Thm 3.1 (p. 24).** Q: "(A quantitative correlation estimate). Let X ≥ 2. Suppose that g1, g2 : N → C are 1-bounded
  multiplicative functions. Let 1 ≤ L ≤ log X and δN be real numbers for all X^{0.4} ≤ N ≤ X, obeying one of the following two axioms:
  (i) (Equidistributed case) g1 is real-valued and for all X^{0.4} ≤ N ≤ X and a, q ∈ N one has the equidistribution bound
  Σ_{N<n≤2N, n≡a (mod q)} g1(n) = δN N/q + O(N L^{−1}). (3.1) Furthermore, we assume the technical condition g1(p) = 1 (3.2) whenever
  exp(log^{1/11} X) ≤ p ≤ exp(log^{1/10} X). (ii) (Non-pretentious case) One has δN = 0 for all X^{0.4} ≤ N ≤ X, as well as the
  non-pretentious inequality exp(M(g1; X^2, log^{1/125} X)) ≫ L. (3.3) Let c > 0 be a sufficiently small absolute constant. Then, there
  exists a set E ⊂ [√X, X] satisfying the logarithmic density bound (1/log X) ∫_E dt/t ≪ L^{−c} such that for any W ∈ [L^c] and
  integers b, h1, h2 = O(L^c) with h1 ≠ h2, we have (W/N) Σ_{N<n≤2N} (g1(n + h1) − δN) g2(n + h2) 1_{n≡b (mod W)} ≪ L^{−c} (3.4)
  for all N ∈ [√X, X] \ E."
  - Notation (pp. 9–10): M(g; X, Q) := inf_{|t|≤X; q≤Q; χ (mod q)} D(g, n ↦ χ(n)n^{it}; X)^2, and "[N] for [1, N]∩N".
- **Remarks 3.2, third bullet (p. 25).** Q: "Theorem 3.1 contains as a special case the following uniform bound for Chowla-type
  averages: For some constant c > 0, for any a1, a2, b1, b2 ∈ [1, (log N)^c] ∩ N with a1 b2 ≠ a2 b1 we have
  (1/N) Σ_{n≤N} λ(a1 n + b1)λ(a2 n + b2) ≪ (log N)^{−c} for all N ∈ [2, ∞) \ E with E satisfying (1/log X) ∫_{[1,X]∩E} dt/t ≪
  (log X)^{−c} for all X ≥ 2. This follows from Theorem 3.1(ii) with W = a1 a2 since the Liouville function λ satisfies (3.3) by
  [39, equation (1.12)] and since we can write λ(a1 n + b1)λ(a2 n + b2) = λ(a1)λ(a2)λ(a1 a2 n + a2 b1)λ(a1 a2 n + a1 b2)."
- First bullet (p. 24). Q: "The L^{−c} type error terms were first obtained by Pilatte [42] (with L = log X and W = 1) in the model
  case of the Liouville function λ ... the arguments here will rely heavily upon those of Pilatte."
- **Ranges.**
  - Rate: L^{−c}. For λ this is (log N)^{−c} in natural averages outside E.
  - Shifts: h1, h2 = O(L^c).
  - Progressions: n ≡ b (mod W) for every W ≤ L^c and every b, coprime or not.
  - Dilations: a_i, b_i ≤ (log N)^c, by the displayed reduction to a progression mod a1 a2.
  - E does not depend on W, b, h1 or h2.
- **Character twists.** g1, g2 are arbitrary 1-bounded multiplicative functions, so g1 = λχ is allowed, subject to (3.3) for λχ.
- **Effectivity: not discussed** in the quoted text. Whether (3.3) for λ is effective in this range of character moduli is not
  stated.

## 5. Guo: arXiv:2608.23500 (v2 "...uniformly over fixed polylogarithmic shift ranges"; v4 "...across all shift scales")

- **G2 Thm 1.1 (p. 2).** Q: "There exists an absolute constant c > 0 such that the following holds. For every fixed A > 0, there are
  constants C_A > 0 and x_A ≥ 3 for which sup_{1≤h≤(log x)^A} |Σ_{n≤x} λ(n)λ(n + h)/n| ≤ C_A (log x)^{1−c} for every real x ≥ x_A."
  - Q (p. 2): "The theorem does not give uniformity for a prescribed exponent A = A(x) tending to infinity".
  - Cor 8.1 (p. 19) gives the same for 0 ≤ h1 < h2 ≤ (log x)^A.
  - Cor 8.2 (p. 20) gives a non-explicit range (log x)^{ω(x)}. Q: "The function ω is non-explicit because the character estimate in
    Input 2.3 inherits Siegel–Walfisz ineffectivity."
- **G4 Thm 1.1 (p. 2).** Q: "There is an absolute constant c > 0 such that every sufficiently large x admits a set E_x ⊆ [1, x] ∩ N
  chosen independently of the exponent below, with the following properties. For every fixed A > 0, uniformly for 1 ≤ H ≤ x,
  |E_x ∩ [1, H]| ≪_A H(log x)^{−A}, (2) and max_{1≤h≤x, h∉E_x} sup_{1≤y≤x} |Σ_{n≤y} λ(n)λ(n + h)/n| ≪ (log x)^{1−c}. (3)"
  - The constants are ineffective (Siegel).
- G4 Thm 1.3 (p. 3), under GRH. Q: "uniformly for h ∈ N and 1 ≤ y ≤ x, |Σ_{n≤y} λ(n)λ(n + h)/n| ≤ log(2 min{h, y}) +
  O((log x)^{1−cG})".
- **Dilations / APs / characters: none.** All statements are for λ(n)λ(n+h) with no congruence condition. Characters appear only
  inside the proof (major arcs).

## 6. Hughes: arXiv:2609.28526v1, "Effective logarithmic two-point Chowla bounds in every window"

- Definition 1.1 (p. 1). Q: "The augmented height of an admissible pair is h := max(a1, a2, |b1|, |b2|, |∆|, 2)". B := K(a1 + a2),
  where K := ⌈4R0⌉ and R0 := max(1, |b1|/a1, |b2|/a2).
- **Thm 1.2 (p. 2).** Q: "There is an effective absolute constant C1 such that for every admissible pair, every g1, g2 ∈ {λ, µ}, every
  0 < ε ≤ 1/10, and all x ≥ ω ≥ exp4(C1 B ε^{−2}), |Σ_{x/ω<n≤x} g1(L1(n))g2(L2(n))/n| ≤ ε log ω. Since B ≤ 15h (Lemma 2.1), this holds
  in particular for ω ≥ exp4(15 C1 h ε^{−2}); and there is an effective absolute C such that for x ≥ ω ≥ exp4(Ch), uniformly over
  admissible pairs of height at most h, |Σ_{x/ω<n≤x} g1(L1(n))g2(L2(n))/n| ≤ C (h/log4 ω)^{1/2} log ω."
- **Thm 1.3 (p. 2).** Common translation is moved out of the tower. hs := max(a1, a2, |∆|, 2), and m is the integer nearest
  (β1+β2)/2 with βi = bi/ai. Q: "|Σ ...| ≤ C[(hs/log4 ω)^{1/2} log ω + log(2 + |m|)]". Q: "For λ(n + b)λ(n + b + h), h ≠ 0, ...
  cancellation is uniform as soon as |h| = o(log4 ω) and |b| = ω^{o(1)}".
- Q (p. 2): "C1 depends on the implied constant in the Matomäki–Radziwill–Tao estimate ... and on ... the Green–Tao restriction
  estimate ...; these are effective but have not been computed".
- **Ranges.**
  - Rate: (h/log_4 ω)^{1/2}.
  - Uniform in all coefficients a1, a2 (dilations allowed, a1 = a2 = q allowed), b1, b2 and the determinant up to height
    h = o(log_4 ω).
  - No characters: Remark 8(4), p. 16. Q: "We make no claim for general multiplicative functions."
  - An AP n ≡ c (mod q) is the special case a1 = a2 = q, b1 = c, b2 = c+2, with ∆ = 2q.
- Remark 8(5) (p. 16). Q: "A sieve for prime tuples needs cancellation against sieve weights relative to the sifted mass. An
  intermediate target with content is sup_{h≤(log ω)^β} |·| ≪ (log ω)^{1−γ} for all windows".
- p. 3. Q: "subtracting prefix bounds leaves an error of size (log x)^{1−c}, which gives no cancellation when log ω ≤ (log x)^{1−c}."
  **Mine:** this is irrelevant for us, because our prefix is n ≤ x, i.e. ω = x.

## 7. Charamaras–Richter: arXiv:2412.17583v3

- Theorem A (p. 3). Q: "For any bounded functions a, b : N → C, we have E^{log}_{n∈[N]} a(Ω(n))b(Ω(n + 1)) = (E_{n∈[N]} a(Ω(n)))
  (E_{n∈[N]} b(Ω(n))) + O((log log log N)^2/√(log log N))."
- Shift 1 only, with no dilations, APs or characters. It is not useful for uniformity.

---

## Helper's analysis (not from the sources)

**A. A direct AP statement exists, so no reduction is needed.** TT Thm 3.1(ii) contains 1_{n≡b (mod W)} explicitly. We take g1 = g2 = λ,
δN = 0, h1 = 0, h2 = 2 and W = e. Then for every e ≤ L^c and every b,
|Σ_{N<n≤2N, n≡b (e)} λ(n)λ(n+2)| ≪ L^{−c} N/e for N ∈ [√X, X] \ E, with E independent of e and b.

The log-averaged sum follows from the exact identity 1/n = ∫_{n/2}^{n} dN/N^2:
Σ_{n≤x} f(n)/n = ∫ (1/N) Σ_{N≤n<2N, n≤x} f(n) dN/N.

Over [√X, X], the good N contribute ≪ L^{−c} log X / e, and the N in E contribute ≪ (1/e) ∫_E dN/N ≪ L^{−c} log X / e. Apply this with
X = x, x^{1/2}, x^{1/4}, ... down to X0 = exp((log x)^{1/2}), and bound n ≤ X0 trivially. With L ≍ (log X)^{c1} for λ (TT Remarks 3.2),
this gives, uniformly for e ≤ (log x)^{c2} and all b,

  Σ_{n≤x, n≡b (e)} λ(n)λ(n+2)/n ≪ (log x)^{1−c3}/e + (contribution of n ≤ X0),

for small absolute c2, c3 > 0. This is the "uniformity in q" the route card asks for, but only for q up to a small power of log x.

**B. Consequence for Selberg-type weights.** Let w(n) = Σ_{d1,d2≤R} λ_{d1}λ_{d2} 1_{[d1,d2] | n(n+2)} with |λ_d| ≤ 1 and squarefree
support.

- The key step is to expand w in the moduli e = [d1, d2] ≤ R^2, not in the period ∏_{p≤R} p ≈ e^R. Each 1_{e | n(n+2)} is a union of
  ρ(e) ≤ 2^{ω(e)} classes mod e.
- Then |Σ_{n≤x} w(n)λ(n)λ(n+2)/n| ≪ (log x)^{1−c3} Σ_{e≤R^2} μ^2(e) 3^{ω(e)} ρ(e)/e + O(log X0) ≪ (log x)^{1−c3} (log R)^6 +
  (log x)^{1/2}.
- The main term (paper's own argument) is Σ_{n≤x} w(n)/n ≥ (c_w + o(1)) log x with c_w ≥ (1/2)∏_{3≤p≤R}(1 − 2/p) ≫ (log R)^{−2}.
- So the relative error is ≪ (log x)^{−c3} (log R)^8 + (log x)^{−1/2}(log R)^2 → 0.
- **Explicit level (if TT Thm 3.1 is correct):** the prop's relative statement holds with R(x) = (log x)^{c0} for a small absolute
  c0 > 0 (we need R^2 ≤ (log x)^{c2}), with relative error (log x)^{−c'}.
- c0 is not numerical: it inherits TT's unspecified c, and effectivity is not stated in TT. This replaces the non-explicit diagonal
  R(x) → ∞ of the present proof. It needs a careful write-up: the trivial bound on the low range uses the periodicity of w with period
  ≤ e^{(1+o(1))R} ≤ X0, and the O_w(1) term in Σ w(n)/n needs care.

**C. Via Hughes instead (effective in principle, much slower).** Apply Thm 1.3 to each class: a1 = a2 = e, b1 = b, b2 = b+2, hs = 2e,
|m| ≤ 1, ω = x/e. Per class the bound is ≪ (1/e)(e/log_4 x)^{1/2} log x. Summing as in B gives a relative error
≪ R(log R)^{7}(log_4 x)^{−1/2}, so R(x) = (log_4 x)^{1/2−ε} works, with effective but uncomputed constants. Expanding in the full
period q ≈ e^R instead would give only R ≈ log_5 x.

**D. Characters, and why shift-only results do not help.**
- Expanding 1_{n≡c (q)} = (1/φ(q)) Σ_χ χ̄(c)χ(n) (for (c, q) = 1) turns the AP sum into Σ λχ(n)λ(n+2)/n. This is a *twisted*
  correlation with g1 = λχ, not a shift-only correlation of λ.
- T16 Thm 1.3/Cor 1.5 (fixed modulus) and TT Thm 3.1 (modulus ≤ L^c, through (3.3) for λχ) allow such twists. HR's Note (p. 84) names
  this route. Hughes (g ∈ {λ, µ} only), Pilatte (λ only) and Guo (λ only) do not.
- Additive characters give λ(n)λ(n+2)e(an/q). These are also not shift-only.
- **Answer:** I know of no reduction of Σ_{n≡c (q)} λ(n)λ(n+2)/n to shift-only correlations λ(n)λ(n+h). So Guo's much larger shift
  ranges ((log x)^A, or almost all h ≤ x) give nothing for progressions or levels. The character route gives the same range as TT's
  direct AP statement, so it brings no gain.
- Non-coprime classes reduce to dilated forms λ(a1 m + b1)λ(a2 m + b2) with a1 ≠ a2 by complete multiplicativity. TT's identity
  (Remarks 3.2) maps these back to a progression mod a1 a2.

**E. What remains Open.**
- Nothing found reaches q (or R) a power of x, or even exp((log x)^ε). The route card's continuation (a), uniformity on average over
  q ≤ x^θ, is still not available.
- Even R = (log x)^{c0} only confirms the input of the parity obstruction in the log-averaged regime (paper Remark `rem:tao-missing`).
  It says nothing for f = Λ and gives no twin-prime lower bound.
