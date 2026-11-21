# Route card: the main term of the Session 39 transfer, by a model target (Session 40, 21 Nov 2026)

**Classification: located (conditional implication, now complete in outline; audit below).**
Not in the parity paper (v1.0.1 frozen). No parity-breaking content of our own. Flag update for Jerry
(the conditional consequence is far stronger than the published literature; it is a pointer at [LWW] Prop. 4.2
and Prop. 5.3, NOT an error found, and NOT a result of ours).

## Question
Session 39 (`2026-11-20-lww-orbit-test.md`, Finding 3) showed that, if the Type II estimate of Lü–Wang–Wu
(arXiv:2610.20242v2, CLAIMED; Prop. 4.2 with Prop. 5.3) holds, the same argument applied to the target
G(N) = prod_i V_i^{-1} sum_{a in A, a | N} Lambda(N/a) gives
sum_{x<n<=2x} Lambda(n) G(n+2) = (Type I main term) + O(x L^{-A}),
but the Type I main term was asserted, not computed (the gap). Can the gap be closed without computing
Type I main terms by hand?

- Success criterion: a complete (conditional) derivation of sum Lambda(n) G(n+2) = c x (1 + o(1)) with an
  explicit c > 0, using only [LWW] Props. 2.1, 4.2, 5.3 (as stated), the classical Bombieri–Vinogradov theorem
  and the fundamental lemma of sieve theory.
- No-go criterion: a place where the Type I sums of [LWW] Section 3 use more of the target than its
  distribution in residue classes to moduli <= x^{2/5+o(1)} (then the model argument below fails).
- Cheapest decisive check: read [LWW] Section 3 (pp. 10-14) line by line for every use of the target.

## Source read (this session)
arXiv:2610.20242v2 (same file as Sessions 38-39, SHA-256 7ac34131...2d423000; still v2 on 21 Nov 2026, no
public comments found by a web search): pp. 4-5 (Prop. 2.1), pp. 7-10 (Prop. 2.3 and proof), pp. 10-14
(Section 3, Prop. 3.1 and proof, (3.1)-(3.10)), pp. 15-18 (Section 4.1, Lemma 4.1, Prop. 4.2), p. 61 ((5.1)),
p. 63 (Prop. 5.3 statement), pp. 69-70 (Section 5.3, proof of Theorem 1).

## Notation
L = log x, Z = exp(L^{0.24}), U = V = x^{1/5}; P_i = (exp(L^{a_i}), exp(2 L^{a_i})], 1/10 < a_1 < ... < a_K < 1/5;
A = {p_1...p_K : p_i in P_i}; V_i = sum_{p in P_i} 1/p; by [LWW] (5.1), prod V_i^{-1} sum_{a in A} 1/a = 1.
For a function g on the positive integers with |g| <= L^C put
  F_g(n) = G_g(n + 2),  G_g(N) = prod_i V_i^{-1} sum_{a in A, a | N} g(N/a),
  T(g) = sum_{x<n<=2x} Lambda(n) F_g(n).
G = G_Lambda is the target of Session 39; the LWW target mu(N)W(N) is G_g for
g(h) = (-1)^K mu(h) rho^{omega(h)} 1_{(a,h)=1} (the coprimality depends on a; harmless, as in [LWW] p. 15).

## Findings
1. **Type I sums see only residue classes (Literature reading + Proved here, elementary).** By [LWW] Prop. 2.1,
   T(g) = T_1(F_g) - T_2(F_g) + T_3(F_g) + O(||F_g||_inf Z), and ||F_g||_inf <= L^{C+1} (K + 1)^K... = x^{o(1)} is
   harmless since Z = x^{o(1)}. In the proof of Prop. 3.1 the only uses of the target in T_2 (and T_1, by partial
   summation) are: (i) the truncation of R_Z(k) to divisors r | k with omega(r) <= R_0, whose error needs an
   UPPER bound for sum_{k: r | k} |F(qk+2)|, and (ii) the remaining sums
   sum_{x<qk<=y, 2 ∤ k, r | k} F(qk + 2).
   (The truncation of W in (3.5)-(3.6) is part of the LWW target, not needed for G_g, whose a-sum is exact.)
   For F = F_g, writing qk + 2 = a h, sum (ii) equals
   prod V_i^{-1} sum_{a in A, (a, r) = 1} sum_{h in I_a(y), h ≡ b(a,q,r) mod 2qr} g(h),
   I_a(y) = ((x+2)/a, (y+2)/a], b = 2 a^{-1} mod qr, h odd; here (a, q) = 1 because q is Z-sifted and the
   primes of a are <= exp(2 L^{0.2}) < Z, a prime p | (a, r) makes the class empty (ah ≡ 0, not 2, mod p), and b is a
   reduced class mod 2qr. So T_1 - T_2 is a LINEAR functional of g that depends on g only through its sums over
   reduced classes mod m = 2qr <= x^{2/5+o(1)} on intervals of length >= x^{1-o(1)}.
2. **Type II sums do not see g (Session 39, Finding 1).** By (4.3)-(4.8), T_3(F_g) << L^C x L^{-A'/2} for every
   |g| <= L^C (Cauchy–Schwarz over h uses only sum_h |g(h)|^2 << L^{2C} X/Y; the terms with (a, h) > 1 are
   O(x L^{C} exp(-L^{1/20})) by the trivial estimate of p. 15), PROVIDED Prop. 4.2 and Prop. 5.3 hold (Q_Y does
   not contain g; Prop. 5.3 needs alpha_m = mu(m) R_Z(m) m^{iv}, beta_n arbitrary, which is the case).
3. **Model target (Proved here, conditional only through Finding 2).** Let D = L^{B_1} and
   f(h) = kappa_D 1_{(h, P(D)) = 1}, kappa_D = prod_{p <= D} (1 - 1/p)^{-1} << log D.
   (a) Lambda and f have the same distribution in reduced classes on average: for m <= y^{1/2} L^{-B} and (b, m) = 1,
   sum_{h <= y, h ≡ b (m)} f(h) = (y/phi(m)) prod_{p | m, p > D}(1 - 1/p) (1 + O(e^{-s})) + O(D^{s})
   by the fundamental lemma (dimension 1, level D^s, s = A log L, so D^s = x^{o(1)}); the factor
   prod_{p|m, p>D}(1 - 1/p) is 1 + O(omega(m)/D) = 1 + O(L/D). With Bombieri–Vinogradov for Lambda (with the
   weight tau(m), by Cauchy–Schwarz and the trivial bound) this gives
   sum_{m <= x^{2/5+o(1)}} tau(m) max_{(b,m)=1} max_{y' <= y} |sum_{h <= y', h ≡ b (m)} (Lambda - f)(h)|
   << y L^{-A} once B_1 is large in terms of A. Classes with (b, m) > 1 do not occur (Finding 1).
   (b) Hence, summing over a with prod V_i^{-1} sum_a 1/a = 1 ((5.1)) and using |varpi_q| <= L and the count of
   representations m = 2qr <= tau(m), (T_1 - T_2)(F_Lambda - F_f) << x L^{-A}. The truncation errors (i) are
   << x L^{-A} for both targets: for f trivially (|f| << log D, as in [LWW] p. 11), for Lambda by Brun–Titchmarsh for
   the primes l <= 2x/a, l ≡ 2 a^{-1} mod qr (qr <= x^{2/5+o(1)}), which gives the same bound as [LWW] with an
   extra O(1).
   (c) T(f) is computed directly: the primes of a exceed exp(L^{0.1}) > D, so ((n+2)/a, P(D)) = 1 iff
   (n+2, P(D)) = 1, and
   T(f) = kappa_D prod V_i^{-1} sum_{a in A} sum_{x<p<=2x, p ≡ -2 (a), (p+2, P(D)) = 1} log p + O(x^{1/2+o(1)})
        = (1 + O(e^{-s})) kappa_D prod_{3 <= l <= D}(1 - 1/(l-1)) x prod V_i^{-1} sum_a 1/phi(a) + O(x L^{-A})
        = 2 C_2 x (1 + o(1)),   C_2 = prod_{l > 2} (1 - 1/(l-1)^2),
   by the fundamental lemma on p + 2 (sifting primes 3 <= l <= D, density 1/(l - 1) for l ∤ a; p + 2 is odd) and
   Bombieri–Vinogradov for the moduli a d <= x^{o(1)}; kappa_D prod_{3<=l<=D}(1 - 1/(l-1)) = 2 prod_{3<=l<=D}
   (1 - 1/(l-1)^2), and prod V_i^{-1} sum_a 1/phi(a) = prod_i (sum_{p in P_i} 1/(p-1))/V_i = 1 + o(1).
   (d) T_3(F_f) << x L^{-A} by Finding 2 (|f| << log D).
4. **Conclusion (conditional on [LWW] Prop. 4.2 and Prop. 5.3; outline).** Combining,
   T(Lambda) = T(f) + (T_1 - T_2)(F_Lambda - F_f) + T_3(F_Lambda) - T_3(F_f) + O(x^{o(1)}) = 2 C_2 x (1 + o(1)),
   which is also the Hardy–Littlewood prediction for this weighted count (for fixed a the expected count of
   p + 2 = a l is (x/a) 2 C_2 prod_{p | a}(p-1)/(p-2), and prod V_i^{-1} sum_a (1/a) prod_{p|a}(p-1)/(p-2) = 1 + o(1)).
   Since G(p + 2) != 0 forces p + 2 = a l^j with a <= exp(2K L^{0.2}), and prime powers j >= 2 contribute O(x^{1/2+o(1)}),
   **if Prop. 4.2 and Prop. 5.3 of [LWW] are correct, then there are >> x/L^{K+2}... (indeed >> x/L after weights)
   primes p in (x, 2x] with p + 2 = a l, a a product of K primes each in (exp(L^{1/10}), exp(2 L^{1/5})], l prime;
   in particular P^+(p + 2) >= p exp(-2K (log p)^{1/5}) for infinitely many p.** Unconditionally the record is
   P^+(p + 2) > p^{0.677} (Baker–Harman 1998, as cited by Ding arXiv:2510.04026v2, p. 1); every exponent c < 1 is
   known under Elliott–Halberstam (loc. cit.). The conditional statement is of at least EH strength. The Session 39
   gap is closed in outline: the implication now rests only on [LWW]'s own Prop. 4.2 and Prop. 5.3.
5. **Why the model trick works, and what it says about [LWW] (Proved here, elementary).** Findings 1-2 give a
   transference principle: if [LWW]'s Type II estimate holds, then for EVERY |g| <= L^C, T(g) equals the value
   predicted by the distribution of g in reduced classes to moduli x^{2/5+o(1)}, up to O(x L^{-A}). Taking
   g = 1_S with S = {h : a h - 2 is composite for every a in A} gives T(1_S) = 0 identically, so the estimate forces
   the Type I prediction of 1_S, roughly 2 C_2 x times the density of S in the relevant ranges, to be O(x L^{-A}):
   almost every h must have a prime among {a h - 2 : a in A, a h in (x, 2x]}. Under the Cramér model this needs
   #{a in A : a ~ Y} >> L log L, which [LWW]'s sets satisfy by a huge margin (exp(L^{1/10}) and more), so there is
   no contradiction; but it shows that the estimate is an "almost all h" statement for primes along the dilation
   sets {a h - 2}, and that it must FAIL for small sets A (consistent with [LWW] needing K large in terms of A).
   Exploration of this session (`code/explore/fake_target_density.py`) measures the density of S for toy A.

## First unresolved implication
Prop. 4.2 (Q_Y - Q_Y^maj << X Y L^{-A}) together with Prop. 5.3. Everything else in the chain above is classical
(BV, fundamental lemma, Brun–Titchmarsh) or elementary. Twins remain the case K = 0, where nothing is gained
(Session 39, Finding 5).

## Audit
See the section "Audit (fresh context)" below (added after the audit).

## Scripts
`code/explore/fake_target_density.py` (exploration, see notes/explorations.md, Session 40). No Lean.
