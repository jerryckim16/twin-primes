# Tao–Teräväinen Thm 3.1 ⇒ Prop. prop:tao-weight at level R = (log x)^{c0} (conditional on a preprint)

- **Date:** 2026-11-15 (helper run, next step 1(a) of STATE.md). Kind: attempt (a quantitative version of a proved weak-regime
  statement; it locates the barrier, it does not cross it).
- **Target.** Paper Prop. `prop:tao-weight` (papers/parity-barrier/main.tex, around l. 162) proves the following from Tao16 Thm 1.2.
  For w_R(n) = (Σ_{d | n(n+2), d ≤ R} λ_d)^2 with R fixed, or with R(x) → ∞ at an unspecified slow rate (a diagonal argument),
  Σ_{n≤x} w_R(n)λ(n)λ(n+2)/n = o(Σ_{n≤x} w_R(n)/n). Question: does the quantitative estimate of Tao–Teräväinen [TT25] give this at
  the explicit level R = (log x)^{c0}, uniformly in the weights?
- **Labels.** Proved here / Literature / Claimed (preprint) / Open, as in the repo. [TT25] is an arXiv preprint (v2, no journal
  reference on arXiv as of 15 Nov 2026), so everything that uses it is **Claimed (preprint)** as input. The deduction below is
  **Proved here, conditional on [TT25] Thm 3.1**. The proof of [TT25] Thm 3.1 itself was not audited.

## 1. Sources read (exact locations, versions)

| key | source | version read | SHA-256 of PDF | where read |
|---|---|---|---|---|
| TT25 | T. Tao, J. Teräväinen, *Quantitative correlations and some problems on prime factors of consecutive integers*, arXiv:2512.01739 | v2, 25 Apr 2026 ("minor edits"; v1 1 Dec 2025); abs page lists no journal ref | ce10e83b10c6544e1dbff037a5e4efa0e387892e0fc596ae09dce76025d7b41e (same file as notes/sources-chowla-quantitative.md) | §1.6 Notation pp. 9–10; Thm 3.1 p. 24; Remarks 3.2 pp. 24–25; §3.2 opening p. 27 |
| MRT | K. Matomäki, M. Radziwiłł, T. Tao, *An averaged form of Chowla's conjecture*, Algebra Number Theory 9 (2015) 2167–2196, arXiv:1503.05121 | v3, 1 Mar 2022 | 8a2633b1594615fe0c340bbca01ad059be5bd66d3495bd028e7e9d2264f1e688 | eq. (1.12) and the sentences around it (p. 6 of the arXiv PDF) |

Both were fetched with WebFetch (abs page, then the PDF) and read with `pdftotext -layout`. The PDFs are in the scratchpad and are
not committed. **Q:** marks a quote. The words are verbatim; formulas are re-typed from pdftotext and linearised.

### 1.1 TT25 Theorem 3.1 (p. 24), verbatim

Q: "Theorem 3.1 (A quantitative correlation estimate). Let X ≥ 2. Suppose that g1, g2 : N → C are 1-bounded multiplicative
functions. Let 1 ≤ L ≤ log X and δN be real numbers for all X^{0.4} ≤ N ≤ X, obeying one of the following two axioms:
(i) (Equidistributed case) g1 is real-valued and for all X^{0.4} ≤ N ≤ X and a, q ∈ N one has the equidistribution bound
Σ_{N<n≤2N, n≡a (mod q)} g1(n) = δN N/q + O(N L^{−1}). (3.1)
Furthermore, we assume the technical condition g1(p) = 1 (3.2) whenever exp(log^{1/11} X) ≤ p ≤ exp(log^{1/10} X).
(ii) (Non-pretentious case) One has δN = 0 for all X^{0.4} ≤ N ≤ X, as well as the non-pretentious inequality
exp(M(g1; X^2, log^{1/125} X)) ≫ L. (3.3)
Let c > 0 be a sufficiently small absolute constant. Then, there exists a set E ⊂ [√X, X] satisfying the logarithmic density bound
(1/log X) ∫_E dt/t ≪ L^{−c}
such that for any W ∈ [L^c] and integers b, h1, h2 = O(L^c) with h1 ≠ h2, we have
(W/N) Σ_{N<n≤2N} (g1(n + h1) − δN) g2(n + h2) 1_{n≡b (mod W)} ≪ L^{−c} (3.4)
for all N ∈ [√X, X] \ E."

Notation (pp. 9–10). Q: "We write X ≪ Y, X ≫ Y, or X = O(Y) to denote the estimate |X| ≤ CY for some constant C". Q: "D(f, g; X) :=
(Σ_{p≤X} (1 − Re(f(p)ḡ(p)))/p)^{1/2}" and Q: "M(g; X, Q) := inf_{|t|≤X; q≤Q; χ (mod q)} D(g, n ↦ χ(n)n^{it}; X)^2 (1.18) where χ
ranges over Dirichlet characters of modulus q ≤ Q". [N] is [1, N] ∩ N (source notes, p. 9).

### 1.2 TT25 Remarks 3.2 (pp. 24–25), verbatim

- First bullet. Q: "A qualitative version of this theorem (with o(1) type error terms), using logarithmic averaging instead of
  natural averaging outside of an exceptional set, was established in [50, Theorem 1.3] (in the non-pretentious case) and [54,
  Theorem 1.4] (in the equidistributed case). The ability to replace logarithmic averaging with natural averaging outside of an
  exceptional set was first observed (in the non-pretentious case) in [51]. The L^{−c} type error terms were first obtained by
  Pilatte [42] (with L = log X and W = 1) in the model case of the Liouville function λ (which is both equidistributed and
  non-pretentious), which improved on [1] and [50]; the arguments here will rely heavily upon those of Pilatte. The technical
  condition (3.2) at small primes can most likely be weakened or even dropped with some additional work, but in any event this
  condition is satisfied in our applications, so we retain it for this paper."
- Second bullet. Q: "Note that in the equidistributed case (i) we permit a to share a common factor with q; thus it asserts that g1
  is quantitatively equidistributed in both primitive and non-primitive residue classes of moduli of size O(L). As noted in [54,
  Remark 1.3], this type of definition includes all sufficiently non-pretentious 1-bounded multiplicative functions. Note also that
  by setting q = 1 in (3.1) we have δN = (1/N) Σ_{N<n≤2N} g1(n) + O(L^{−1}) = O(1). (3.5)"
- Third bullet. Q: "It is also worth noting that Theorem 3.1 contains as a special case the following uniform bound for
  Chowla-type averages: For some constant c > 0, for any a1, a2, b1, b2 ∈ [1, (log N)^c] ∩ N with a1 b2 ≠ a2 b1 we have
  (1/N) Σ_{n≤N} λ(a1 n + b1)λ(a2 n + b2) ≪ (log N)^{−c} for all N ∈ [2, ∞) \ E with E satisfying (1/log X) ∫_{[1,X]∩E} dt/t ≪
  (log X)^{−c} for all X ≥ 2. This follows from Theorem 3.1(ii) with W = a1 a2 since the Liouville function λ satisfies (3.3) by
  [39, equation (1.12)] and since we can write λ(a1 n + b1)λ(a2 n + b2) = λ(a1)λ(a2)λ(a1 a2 n + a2 b1)λ(a1 a2 n + a1 b2)."
  ([39] is MRT.)

### 1.3 TT25 §3.2, opening (p. 27): how E becomes uniform in (W, b, h)

Q: "By shifting n, h2, b by h1 (and adjusting c slightly), we may normalize h1 = 0, thus h2 = σh for some h ∈ [L^c] and σ = ±1. If
we can prove the claim for any single quadruple (W, b, σ, h), then we can obtain it for all (W, b, σ, h) (after replacing c by,
say, c/4), since there are only O(L^{3c}) possible choices of (W, b, σ, h) and one can concatenate all the exceptional sets by the
union bound."

**Mine:** this confirms two readings. (a) E is chosen once, for all W, b, h1, h2 together. (b) Only b mod W matters. The phrase
"integers b, h1, h2 = O(L^c)" is ambiguous about whether b must be O(L^c). That is harmless here: 1_{n≡b (W)} depends only on b mod
W, so we always take 0 ≤ b < W ≤ L^c.

### 1.4 MRT eq. (1.12) (arXiv v3, p. 6), verbatim

Q: "For g(n) = λ(n) and X, Q, M as in the above theorem, one obtains, for every ε > 0, the bound
M ≥ inf_{|t|≤X; q≤Q; χ (q)} Σ_{exp((log X)^{2/3+ε}) ≤ p ≤ X} (1 + Re χ(p)p^{it})/p ≥ (1/3 − ε) log log X + O(1) (1.12)
where the last inequality is established via standard methods from the Vinogradov-Korobov type zero-free region ... for L(s, χ)
and some absolute constant c > 0, which applies since χ has conductor q ≤ (log X)^{1/125} (so that there are no exceptional
zeros), see [20, §9.5]. ... We remark that as our arguments make no use of exceptional zeroes, all the implied constants in our
theorems are effective."

Here MRT's M is M(λ; X, Q) with Q ≤ log^{1/125} X (MRT Thm 1.6 setting). **Mine:** MRT says the last inequality in (1.12) is
"established via standard methods" and does not write it out. I take it as Literature (published, MRT).

## 2. Criteria (fixed before the work)

- **Success.** A complete deduction, with every step checked against the verbatim statement in §1.1, of the following. There is an
  absolute c0 > 0 such that for all large x, all 1 ≤ R ≤ (log x)^{c0} and all real (λ_d)_{d≤R} with λ_1 = 1 and |λ_d| ≤ 1:
  |Σ_{n≤x} w_R(n)λ(n)λ(n+2)/n| ≤ (log x)^{−c0} Σ_{n≤x} w_R(n)/n.
  The deduction must keep track of the number of residue classes (Σ ρ([d1,d2])) and of the low range and the exceptional scales.
- **No-go.** Any of the following.
  (a) Thm 3.1 does not cover a progression n ≡ b (mod W) with shift pair (0, 2) uniformly in W ≤ R^2 and b with one exceptional
  set.
  (b) λ is not shown, in a source, to satisfy (3.3) with L a power of log X.
  (c) The summed error over the ≍ Σ_{d1,d2≤R} ρ([d1,d2]) classes, or the trivial bounds on the exceptional scales and the low range,
  is not o(main term) for any R → ∞ that is a power of log x. Then record the exact obstruction.
- **Cheapest decisive check.** The error budget: per class the error is ≪ (log x)^{1−η}/e + O(1). The sum over classes is then
  ≪ (log R)^6 (log x)^{1−η} + R^{2+o(1)}, against a main term ≫ (log R)^{−2} log x.

## 3. The argument

Notation: x is large; λ is the Liouville function; e = [d1, d2]; C_e := {c ∈ [0, e) : e | c(c+2)}; ρ(e) := |C_e|; c_TT is the
absolute constant c of Thm 3.1, taken small enough (we may assume c_TT < 1).

### Step 0. Choice of L for λ (from Literature + Claimed)

Apply MRT (1.12) at scale X^2 with Q = log^{1/125} X ≤ log^{1/125}(X^2) and ε = 1/12. M(g; X, Q) increases as Q decreases, and the
t-range |t| ≤ X^2 and the prime range p ≤ X^2 are MRT's at scale X^2. This gives
M(λ; X^2, log^{1/125} X) ≥ (1/4) log log(X^2) − O(1).
So exp(M) ≫ (log X)^{1/4}, and (3.3) holds with **L = L(X) := (log X)^{1/4}**. Also 1 ≤ L ≤ log X for X ≥ e, and δN = 0. This is
the case of Thm 3.1(ii) with g1 = g2 = λ. TT Remarks 3.2 (third bullet) assert that λ satisfies (3.3) via the same reference; the
exponent 1/4 is my reading of MRT (1.12).

Put κ := c_TT/4. Then Thm 3.1 gives the following **(Claimed, preprint)**. For each X ≥ X_* (absolute) there is
E(X) ⊂ [√X, X] with ∫_{E(X)} dt/t ≪ (log X)^{1−κ}. For every integer 1 ≤ W ≤ (log X)^κ, every b ∈ [0, W) and every
N ∈ [√X, X] \ E(X),

  |Σ_{N<n≤2N, n≡b (W)} λ(n)λ(n+2)| ≤ C_1 (log X)^{−κ} N/W.   (T)

Here h1 = 0 and h2 = 2. The condition h2 = 2 ≤ L^c holds once X ≥ X_*. C_1 is absolute: TT's c is "absolute", the hypothesis
constant in (3.3) is absolute, and ≪ is the paper's |·| ≤ C·. **Adversarial note:** TT do not say in words that the implied
constants in (3.4) and in the density bound are independent of X, g1, g2. That is the standard reading of "Let X ≥ 2 ... ≪" with an
absolute c, and TT's own Remarks 3.2 (third bullet) use it in exactly this way, uniformly in X. I flag it as a reading, not a quote.

### Step 1. From dyadic sums to the log sum for one class (Proved here, given (T))

Fix e ≥ 1 and c ∈ [0, e). Put f(n) := λ(n)λ(n+2) 1_{n≡c (e)} 1_{n≤x} and F(N) := Σ_{N<n≤2N} f(n). For n ≥ 1 we have
∫_{n/2}^{n} N^{−2} dN = 1/n, and N < n ≤ 2N ⇔ n/2 ≤ N < n. Hence, exactly,

  S(e,c;x) := Σ_{n≤x, n≡c(e)} λ(n)λ(n+2)/n = ∫_0^x F(N) N^{−2} dN.

Scales: X_0 := x and X_{j+1} := X_j^{1/2}. Let J := max{j : log X_j ≥ (log x)^{1/2}}. Then log X_J < 2(log x)^{1/2} and
J ≤ log_2 log x. Split (0, x] into

- (A) (x/2, x];
- (B_0) [X_1, x/2], and (B_j) [X_{j+1}, X_j] for 1 ≤ j ≤ J;
- (C) (0, X_{J+1}).

For all N, |F(N)| ≤ #{n ∈ (N, 2N] : n ≡ c (e)} ≤ N/e + 1.

- (A) ∫_{x/2}^{x} (N/e + 1) N^{−2} dN ≤ (log 2)/e + 2/x.
- (B_j) Here 2N ≤ x (for j ≥ 1 because 2X_j ≤ 2√x ≤ x), so F(N) is a full dyadic sum. Apply (T) at X = X_j, W = e, b = c. This needs

    e ≤ (log X_j)^κ, which holds for all j ≤ J if e ≤ (log x)^{κ/2}.   (U)

  For N ∉ E(X_j): ∫ C_1(log X_j)^{−κ} (N/e) N^{−2} dN ≤ C_1 (log X_j)^{1−κ}/(2e) ≤ C_1 (log x)^{−κ/2} (log X_j)/e.
  For N ∈ E(X_j): ∫_{E(X_j)} (N/e + 1)N^{−2} dN ≤ (1/e)·O((log X_j)^{1−κ}) + 1/X_{j+1}.
  Σ_j log X_j ≤ 2 log x, and Σ_{j≤J} 1/X_{j+1} ≤ (J+1)/X_{J+1} = o(1). Total over the (B_j):
  ≪ (log x)^{1−κ/2}/e + o(1).
- (C) ∫_0^{X_{J+1}} |F(N)| N^{−2} dN ≤ Σ_{1≤n<2X_{J+1}, n≡c(e)} 1/n. This is ≤ 1 + (1 + log(2X_{J+1}))/e ≤ 1 + (2 + (log x)^{1/2})/e:
  the term n = c (if c ≥ 1) is ≤ 1, and the rest is ≤ (1/e)Σ_{k≤Y/e} 1/k.

**Lemma A (Proved here, conditional on TT25 Thm 3.1).** There are absolute C_2, x_0 such that for x ≥ x_0, every e ≤ (log x)^{κ/2}
and every c ∈ [0, e):
  |S(e,c;x)| ≤ C_2 (log x)^{1−κ/2}/e + 2.
(The (log x)^{1/2}/e term from (C) is absorbed because κ < 1.)

**Mine (adversarial).** The "+2" is real. It comes from the first term n = c of each class (and O(1) boundary terms). It must be
paid once per class, ρ(e) times per pair (d1, d2). This is where a large number of classes could hurt (see Step 3).

### Step 2. Expanding the square (Proved here)

Since 1_{d1|m}1_{d2|m} = 1_{[d1,d2]|m},
w_R(n) = Σ_{d1,d2≤R} λ_{d1}λ_{d2} 1_{[d1,d2] | n(n+2)} = Σ_{d1,d2≤R} λ_{d1}λ_{d2} Σ_{c∈C_e} 1_{n≡c (e)}, with e = [d1,d2] ≤ R^2.
Hence, exactly,
  Σ_{n≤x} w_R(n)λ(n)λ(n+2)/n = Σ_{d1,d2≤R} λ_{d1}λ_{d2} Σ_{c∈C_{[d1,d2]}} S([d1,d2], c; x).   (E)

Note that this expands in the moduli e ≤ R^2, not in the period ∏_{p≤R} p ≈ e^R of w_R. Expanding in the period, as the paper's proof
does, would need W ≈ e^R in (T), which is far outside TT's range.

Arithmetic facts (Proved here; checked numerically for e < 400 by a throwaway script):
- ρ is multiplicative (CRT).
- For odd p, p cannot divide both n and n+2, so ρ(p^k) = 2.
- ρ(2) = 1, ρ(4) = 2, and ρ(2^k) = 4 for k ≥ 3 (n = 2m, need 2^{k−2} | m(m+1)).
- Hence ρ(e) ≤ 2^{ω(e)+1}.
- #{(d1, d2) : [d1, d2] = e} = τ(e^2) (multiplicative, 2k+1 at p^k).

### Step 3. The error budget (Proved here, conditional)

Assume |λ_d| ≤ 1 and R^2 ≤ (log x)^{κ/2}, i.e. **R ≤ (log x)^{κ/4}**, which gives (U) for every e = [d1, d2]. By (E) and Lemma A:

|Σ_{n≤x} w_R λλ/n| ≤ C_2 (log x)^{1−κ/2} Σ_{d1,d2≤R} ρ([d1,d2])/[d1,d2] + 2 Σ_{d1,d2≤R} ρ([d1,d2]).

- First sum ≤ Σ_{e≤R^2} ρ(e)τ(e^2)/e ≤ ∏_{p≤R^2}(1 + Σ_{k≥1} ρ(p^k)(2k+1)/p^k). The factor at p = 2 is ≤ 1 + 4·5 = 21. The factor at
  odd p is 1 + 6/p + O(p^{−2}). Mertens then gives ≪ (log R)^6 (for R ≥ 2; ≪ 1 for R < 2).
- Second sum ≤ R^2 · max_{e≤R^2} 2^{ω(e)+1} = R^{2+o(1)}.

So the **error is ≪ (log R)^6 (log x)^{1−κ/2} + R^{2+o(1)}**.

### Step 4. The main term (Proved here, unconditional)

Let S_R := {n odd : p ∤ n(n+2) for all 3 ≤ p ≤ R}. For n ∈ S_R, n(n+2) is odd with no prime factor ≤ R. So the only d ≤ R dividing
it is d = 1, and w_R(n) = λ_1^2 = 1. Everywhere w_R ≥ 0. S_R is periodic mod P := ∏_{p≤R} p with density
δ_R = (1/2)∏_{3≤p≤R}(1 − 2/p) (CRT). By Mertens δ_R ≫ (log R)^{−2} for R ≥ 3, and δ_R = 1/2 for R < 3.

A(t) := |S_R ∩ [1,t]| ≥ δ_R t − P. Partial summation gives
Σ_{n≤x} w_R(n)/n ≥ Σ_{n≤x} 1_{S_R}(n)/n ≥ ∫_P^x (δ_R/t − P/t^2) dt ≥ δ_R log(x/P) − 1.
log P = θ(R) ≤ 2R = o(log x) (Chebyshev). Hence **Σ_{n≤x} w_R(n)/n ≥ (1 − o(1)) δ_R log x ≫ (log R)^{−2} log x**, uniformly in
1 ≤ R ≤ (log x)^{1/2} and in the real λ_d with λ_1 = 1.

On the size: for the optimal 2-dimensional Selberg weights the mean of w_R is ≍ (log R)^{−2} (the dimension is 2, because ρ(p) = 2),
not (log R)^{−1}. This lower bound has that order. That is standard Selberg-sieve theory, not re-read in a source here, and it is
not used: only the lower bound is used.

### Step 5. Conclusion

Ratio ≪ (log R)^8 (log x)^{−κ/2} + R^{2+o(1)}(log R)^2/log x ≤ (log x)^{−κ/2+o(1)} + (log x)^{κ/2−1+o(1)}.
Since κ < 1, this is ≤ (log x)^{−κ/4} for x ≥ x_0 (absolute). So the success criterion holds with **c0 := κ/4 = c_TT/16**.
Then 1_{λ(n)λ(n+2)=±1} = (1 ± λ(n)λ(n+2))/2 gives the parity-class statement.

**Bounded coefficients only.** If instead |λ_d| ≤ B, the error is multiplied by B^2. The conclusion survives for
B ≤ (log x)^{κ/16}, for example. Whether a given sieve's λ_d satisfy |λ_d| ≤ 1 is a separate matter. For Selberg's optimal weights
this is classical, but it was not re-read in a source in this run, so the proposition below simply assumes |λ_d| ≤ 1. GPY/Maynard-type
weights with λ_d of size (log R)^k are covered whenever (log R)^{2k} is ≤ (log x)^{κ/16}, which is automatic for R = (log x)^{c0}
and fixed k.

## 4. Adversarial checklist (each point checked)

1. **Averaging.** TT gives natural dyadic sums (N, 2N] outside E, not log sums. Converted exactly by ∫_{n/2}^{n} dN/N^2 = 1/n.
   Truncation at x is handled by (A). ✓
2. **Progressions.** 1_{n≡b (mod W)} is explicit in (3.4), for "any W ∈ [L^c]". Classes with gcd(b, W) > 1 are allowed (b is
   arbitrary). C_e contains non-coprime classes (e.g. c = 0), so this matters. ✓ No dilation (a_1 = a_2 = W) and no Remark 3.2
   identity is needed.
3. **Uniformity in W, b.** E is independent of W, b, h1, h2 (order of quantifiers in Thm 3.1, confirmed by §3.2's union bound). ✓
   The number of classes enters only through the summation in Step 3, not through E. ✓
4. **Shift.** h1 = 0, h2 = 2 = O(L^c) for X ≥ X_*. ✓
5. **Non-pretentiousness of λ.** (3.3) with L = (log X)^{1/4}, from MRT (1.12) at scale X^2 (Literature, published; the last
   inequality there is "standard methods", not written out in MRT). TT assert the same use. ✓ (reading)
6. **Several X.** Thm 3.1 is applied at J+1 ≪ log log x scales X_j ≥ exp((log x)^{1/2}). Constants are absolute (reading, see
   Step 0). The low range n ≲ exp((log x)^{1/2}) is bounded trivially and costs (log x)^{1/2}/e + 1 per class. ✓
7. **Number of classes.** Σ_{d1,d2≤R} ρ([d1,d2]) = R^{2+o(1)} classes, each with an O(1) penalty. This is fine only because R is a
   small power of log x. It would already fail at R = (log x)^{1/2}, where R^2 ≍ log x. The binding constraint, though, is TT's
   W ≤ L^c, not this. ✓
8. **Effectivity.** MRT's constants are effective (quoted). TT do not discuss effectivity in Thm 3.1 or Remarks 3.2, so c0 and x_0
   are not claimed effective or numerical.
9. **Not audited.** The proof of TT Thm 3.1 (pp. 25–40+, built on Pilatte's decoupling inequality, Thm 3.3) was not checked. This is
   the single external dependency. TT25 is unrefereed as far as we know.

## 5. Classification

**Proved here, conditional on [TT25] Thm 3.1 (preprint).** It also uses MRT (1.12) (Literature) for (3.3). Prop. prop:tao-weight
then holds at the explicit level R ≤ (log x)^{c0}, c0 = c_TT/16. The bound is uniform over all real λ_d with λ_1 = 1 and
|λ_d| ≤ 1, with relative error (log x)^{−c0}. This removes the diagonal choice of R(x) in the present proof.

**First unresolved implication (Open).** TT's range is W ≤ L^c ≤ (log X)^{c}. Any level R ≥ (log x)^{A} for large A, let alone
R = exp((log x)^ε) or R = x^θ, needs (3.4)-type cancellation for moduli W far beyond a power of log. At least it needs it on average
over W ≤ x^{2θ}, weighted by ρ(W)τ(W^2)/W. No source read in this project gives that (see notes/sources-chowla-quantitative.md
§E). The second bottleneck is the R^{2+o(1)} trivial term. It is not binding at this level and would be removed by any
averaged-over-W statement that controls the first terms.

## 6. What this would and would NOT mean

- **Would mean** (if TT25 Thm 3.1 is correct): the twisted Type I input of the parity obstruction (paper Remark rem:tao-missing)
  holds in the log-averaged regime up to a polylogarithmic sieve level, with a power-of-log saving. Selberg-type weights of level
  (log x)^{c0} cannot tell λ(n)λ(n+2) = +1 from −1. It is a quantitative **confirmation of the obstruction's input**.
- **Would NOT mean:**
  - Any statement about f = Λ or Type I/II sums with primes, about dyadic or natural averages over all x, or about level x^θ.
  - Any lower bound for twin primes, or any progress on breaking parity. On the contrary, it says that this class of weights is
    parity-blind, which is why it cannot see twin primes.
  - The level (log x)^{c0} is useless for sieve upper or lower bounds, which need R = x^θ.

## 7. LaTeX-ready draft (Proved here, conditional on [TT25] (preprint))

```latex
\begin{proposition}[\lbl{Proved here, conditional on \cite[Theorem~3.1]{TT25} (preprint)}]
\label{prop:tao-weight-logc}
There are absolute constants $c_0>0$ and $x_0$ such that the following holds
for $x\ge x_0$. Let $1\le R\le(\log x)^{c_0}$, let $(\lambda_d)_{d\le R}$ be
real with $\lambda_1=1$ and $|\lambda_d|\le1$, and let
$w_R(n)=\bigl(\sum_{d\mid n(n+2),\,d\le R}\lambda_d\bigr)^2$. Then
\[
\Bigl|\sum_{n\le x}\frac{w_R(n)\lambda(n)\lambda(n+2)}{n}\Bigr|
\le(\log x)^{-c_0}\sum_{n\le x}\frac{w_R(n)}{n},
\]
and consequently
$\sum_{n\le x,\ \lambda(n)\lambda(n+2)=\pm1}w_R(n)/n
=\bigl(\tfrac12+O((\log x)^{-c_0})\bigr)\sum_{n\le x}w_R(n)/n$
for both signs. One may take $c_0=c/16$, where $c$ is the constant of
\cite[Theorem~3.1]{TT25}; $c_0$ and $x_0$ are not claimed to be effective.
\end{proposition}

\begin{proof}
\emph{Input.} By \cite[(1.12)]{MRT15} at scale $X^2$ (with $\varepsilon=1/12$;
there $q\le(\log X)^{1/125}$), $M(\lambda;X^2,\log^{1/125}X)\ge\frac14\log\log X-O(1)$,
so (3.3) of \cite{TT25} holds for $g_1=\lambda$ with $L=(\log X)^{1/4}$
(as asserted in \cite[Remarks~3.2]{TT25}). Put $\kappa=c/4$.
\cite[Theorem~3.1(ii)]{TT25} with $g_1=g_2=\lambda$, $\delta_N=0$, $h_1=0$,
$h_2=2$ then gives, for $X\ge X_*$, a set $E(X)\subset[\sqrt X,X]$ with
$\int_{E(X)}dt/t\ll(\log X)^{1-\kappa}$ such that
\begin{equation}\label{eq:TT-input}
\Bigl|\sum_{\substack{N<n\le2N\\ n\equiv b\ (W)}}\lambda(n)\lambda(n+2)\Bigr|
\ll(\log X)^{-\kappa}\frac NW
\end{equation}
for all integers $1\le W\le(\log X)^{\kappa}$, all $b$, and all
$N\in[\sqrt X,X]\setminus E(X)$; $E(X)$ does not depend on $W,b$, and the
implied constants are absolute.

\emph{One residue class.} Let $e\le(\log x)^{\kappa/2}$, $0\le c<e$, and
$F(N)=\sum_{N<n\le\min(2N,x),\,n\equiv c\,(e)}\lambda(n)\lambda(n+2)$. Since
$\int_{n/2}^{n}N^{-2}\,dN=1/n$,
$S(e,c;x):=\sum_{n\le x,\,n\equiv c(e)}\lambda(n)\lambda(n+2)/n=\int_0^xF(N)N^{-2}\,dN$.
Let $X_0=x$, $X_{j+1}=X_j^{1/2}$ and $J=\max\{j:\log X_j\ge(\log x)^{1/2}\}$.
We use $|F(N)|\le N/e+1$ on $(x/2,x]$, on $E(X_j)$, and on $(0,X_{J+1})$, and
\eqref{eq:TT-input} with $X=X_j$, $W=e$ (admissible, since
$e\le(\log X_j)^{\kappa}$) on $[X_{j+1},X_j]\setminus E(X_j)$ (on
$[X_1,x/2]$ for $j=0$), where $F(N)$ is a full dyadic sum. Since
$\sum_j\log X_j\le2\log x$, we get
\[
|S(e,c;x)|\ll\frac{(\log x)^{1-\kappa/2}}{e}+\frac{(\log x)^{1/2}}{e}+1
\ll\frac{(\log x)^{1-\kappa/2}}{e}+1,
\]
where the term $1$ comes from the term $n=c$ in the range $n\le2X_{J+1}$.

\emph{Summation.} Expanding the square,
$w_R(n)=\sum_{d_1,d_2\le R}\lambda_{d_1}\lambda_{d_2}
\sum_{c\in\mathcal C_{[d_1,d_2]}}1_{n\equiv c\,([d_1,d_2])}$,
where $\mathcal C_e=\{0\le c<e:e\mid c(c+2)\}$ has $\rho(e)\le2^{\omega(e)+1}$
elements. Since $[d_1,d_2]\le R^2\le(\log x)^{\kappa/2}$ for $c_0\le\kappa/4$,
and $\#\{(d_1,d_2):[d_1,d_2]=e\}=\tau(e^2)$,
\[
\Bigl|\sum_{n\le x}\frac{w_R(n)\lambda(n)\lambda(n+2)}{n}\Bigr|
\ll(\log x)^{1-\kappa/2}\sum_{e\le R^2}\frac{\rho(e)\tau(e^2)}{e}
+\sum_{d_1,d_2\le R}\rho([d_1,d_2])
\ll(\log R+1)^6(\log x)^{1-\kappa/2}+R^{2+o(1)}.
\]

\emph{Main term.} If $n$ is odd and $p\nmid n(n+2)$ for $3\le p\le R$, then
$w_R(n)=\lambda_1^2=1$; these $n$ form a union of classes modulo
$P=\prod_{p\le R}p$ of density
$\delta_R=\frac12\prod_{3\le p\le R}(1-2/p)\gg(\log R+1)^{-2}$. Since $w_R\ge0$ and
$\log P\le2R=o(\log x)$, partial summation gives
$\sum_{n\le x}w_R(n)/n\ge\delta_R\log(x/P)-1\gg(\log R+1)^{-2}\log x$.

\emph{Conclusion.} The ratio is
$\ll(\log x)^{-\kappa/2+o(1)}+(\log x)^{\kappa/2-1+o(1)}\le(\log x)^{-\kappa/4}$
for $x\ge x_0$, as $\kappa<1$. Take $c_0=\kappa/4$. The second display follows
from $1_{\lambda(n)\lambda(n+2)=\pm1}=\frac12(1\pm\lambda(n)\lambda(n+2))$.
\end{proof}

\begin{remark}
This replaces the non-explicit $R(x)\to\infty$ of
Proposition~\ref{prop:tao-weight} by $R=(\log x)^{c_0}$, uniformly in the
weights, but only conditionally on the preprint \cite{TT25}, whose proof we
have not checked. Note that one must expand in the moduli $[d_1,d_2]\le R^2$
and not in the period $\prod_{p\le R}p$ of $w_R$. The range of moduli
$W\le L^c$ in \cite[Theorem~3.1]{TT25} is the binding constraint; level
$x^{\theta}$ remains \lbl{Open}, and even at that level the statement would
only confirm the input of the parity obstruction, not give a lower bound
for twin primes.
\end{remark}
```

(The draft cites `MRT15`, which is not in the paper's bibliography yet. Entry: K. Matomäki, M. Radziwiłł, T. Tao, *An averaged form
of Chowla's conjecture*, Algebra Number Theory 9 (2015), no. 9, 2167–2196; arXiv:1503.05121.)

- **Disposition:** closed (conditional proof written; adversarial self-audit above; an independent fresh-context audit is still to
  be done before anything goes into the paper). Continuation: an averaged-over-W version of TT (3.4) for W up to x^{θ} (Open; no
  source known).
