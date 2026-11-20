# Route card: what the Lü–Wang–Wu Type II argument uses, and what else it would prove (Session 39, 20 Nov 2026)

**Classification: located (conditional implication; outline with one open gap, the main term; audited, see below).**
Not in the parity paper (v1.0.1 frozen). No parity-breaking content of our own. Flag update for Jerry (the
consequence below is much stronger than the published literature, so either the preprint's Type II
estimate is a larger breakthrough than claimed, or it fails; this is a pointer for an expert, not an error found).

## Question
Lü–Wang–Wu (arXiv:2610.20242v2, 75 pp., CLAIMED; notes in `notes/sources-lww26.md`) claim
sum_{p<=x} mu(p+2) = o(pi(x)). Which properties of mu at the shifted point does their argument actually use,
and does the mechanism transfer to other targets, in particular Lambda(n+2)?

- Success criterion (for a new mechanism): a transfer of the argument to a target with Lambda at n+2 that
  reaches a statement the Liouville-pattern class blocks and that is not already in the preprint.
- No-go / red-flag criterion: a "fake function" satisfying every property of mu that the argument uses,
  but correlating with Lambda(n) at n+2; or a consequence of the argument that contradicts or far exceeds
  the literature.
- Cheapest decisive check: read Section 4.1 (pp. 15-18) for the exact use of mu(n+2) in the Type II sum.

## Source read (this session)
arXiv:2610.20242v2 (SHA-256 7ac34131...2d423000, the same file as Session 38): pp. 4-11 (Prop. 2.1 Vaughan,
Prop. 2.2 character–Mellin estimate for mu, Section 2.3 auxiliary weights W, Prop. 2.3, start of Section 3),
pp. 14-19 (end of Section 3; Section 4.1, eqs. (4.1)-(4.14), Lemma 4.1, Prop. 4.2; start of Section 4.2).

## Findings
1. **What the Type II step uses (Literature reading, pp. 15-16).** With mn + 2 = ah, a = p_1...p_K (p_i in P_i),
   they use mu(ah) = (-1)^K mu(h) and then, in (4.6), Cauchy–Schwarz over h with only |mu(h) rho^{omega(h)}| <= 1:
   |T_Y|^2 << (X/Y) Q_Y. The quantity Q_Y (4.7) does not contain the target at all. Its smallness must come from
   alpha_m = mu(m) R_Z(m) m^{iv}, the Möbius coefficient of Vaughan's identity for Lambda(n) (the prime variable),
   through Prop. 4.2 (Q_Y = Q_Y^maj + O(XY L^{-A}) for arbitrary coefficients |alpha_m| <= L^C R_Z(m),
   |beta_n| <= L^C R_Z(n)) and a major-arc bound for the actual alpha (Section 5, Prop. 2.2).
   So in the Type II part the target is used only through boundedness and multiplicativity at the auxiliary
   primes; the Type I part (Section 3) uses Bombieri–Vinogradov for mu along n = qk + 2.
2. **Orbit picture (Proved here, elementary; Lean-checked finite core: `lean/TwinPrimes/Orbit.lean`).** If
   f(ah) = s f(h) (s = +-1) for all K-products a coprime to h, then f(ah) = f(bh), and N = ah = bh' forces
   f(h) = f(h'): f is determined up to the known sign on "orbits" that link n + 2 to many far-away integers
   (a/b)(n + 2). A function constant on orbits can correlate with primes only through orbit-level fluctuations of
   prime counts, which is exactly what Q_Y measures. This is why the mechanism lies outside the
   Liouville-pattern class of the parity paper (that class sees sign patterns in a bounded window only).
3. **The argument proves more than claimed (Proved here in outline, conditional on [LWW] Prop. 4.2 and their
   Section 5 bound).** Replace mu(n+2) W(n+2) by G(n+2), G(N) = prod V_i^{-1} sum_{a in A, a | N} Lambda(N/a).
   The Type II sum has the same shape with mu(h) rho^{omega(h)} replaced by Lambda(h), and Cauchy–Schwarz gives
   |T_Y|^2 << (X/Y) L Q_Y, a loss of only L^{1/2}; the Type I sums are evaluated by the classical
   Bombieri–Vinogradov theorem for primes (moduli q r <= x^{2/5+o(1)}, primes l <= 2x/a, a = x^{o(1)}).
   (G <= L^{K+1}; the errors O(||G|| Z) of (2.2) and O(x L^{2-B}) of (4.2)-(4.4) are absorbed by taking B large
   after K is fixed; K itself must be large in terms of A, as in [LWW] Prop. 4.2, whose operator bound is
   << L^{1-0.005K} + L^{-A}.) Hence sum_{x<p<=2x} log p G(p+2) = (Type I main term) + O(x L^{-A}).
   GAP (found by the audit): the main term >> x is asserted, not written out. [LWW] never compute a Type I main
   term (theirs vanish by (3.1)); for G one must compute T_1 - T_2 and show that the Type II part of a smooth
   local-density model is negligible. That model depends on mn modulo a, a about exp(L^{0.2}), far beyond the
   Siegel–Walfisz range (our first draft wrongly said "by Siegel–Walfisz"); the audit suggests Bombieri–Vinogradov
   for mu averaged over a with weight 1/a. Until this is written, the consequence is: if the main term is >> x, then
   infinitely many primes p with
   p + 2 = a l, l prime, a a product of exactly K primes each <= exp(2 (log x)^{1/5}) = x^{o(1)}. Consequences:
   P^+(p+2) > p^{1-o(1)} infinitely often, and (K even) Omega(p+2) = K + 1 odd, so lambda(p+2) = -1 infinitely
   often (the open problem noted by Pintz 2010). The last statement is of the same kind as LWW's own Theorem 2
   (which already prescribes mu(p+2)), so it adds nothing parity-wise; the new point is the EH-strength first one.
4. **Comparison with the literature (Literature, opened this session).** The best unconditional exponent for
   P^+(p+a) > p^c is c = 0.677 (Baker–Harman 1998; cited as the record in Y. Ding, arXiv:2510.04026v2, p. 1);
   R. Li, arXiv:2508.18285v3, claims 0.679 and writes that "even 0.678 seems impossible without any new things";
   every c < 1 is known under Elliott–Halberstam (Ding, loc. cit., citing Pomerance, Granville, Wang, Wu).
   So, if correct (and once the main-term gap is closed), the LWW Type II estimate gives unconditionally an
   EH-strength statement for this problem. Not a contradiction with anything proved, but a strong consistency
   red flag: the place to check is Prop. 4.2 (with Section 5).
5. **Twin primes.** The twin case is K = 0 (a = 1); in fact Prop. 4.2 needs K large in terms of A, so every
   fixed small K is out as well. With K = 0, Y = 1, there is no average over a, Cauchy–Schwarz over h
   gains nothing, and Q_Y is the full twin-type square. First unresolved implication: K = 0. Equivalently, by
   Lambda = Lambda_I + Lambda_II, the off-diagonal of Q_Y is (up to Type I terms computable by
   Bombieri–Vinogradov) an average over a != b in A of binary Hardy–Littlewood correlations of the Type II
   pieces along the forms (ah - 2, bh - 2); the twin problem is the single unaveraged form.

## Audit
Fresh-context adversarial audit (helper agent; read LWW pp. 1-20 and Section 5, pp. 61-71, which contains the
proof of Theorem 1; Section 4.2 onward by text search). Verdicts: Finding 1 holds (minor corrections: omega(h) in
[LWW] counts only primes in the union of the P_i; the rho-powers in the operator kernels of Section 4.2 come from
the construction and equal 1 on the support; no further use of mu at the shifted point was found, including
Prop. 2.3, the average over the weights W_j and the final Cauchy–Schwarz on p. 70; omission: K must be large in
terms of A). Finding 3 holds as conditional logic with one gap (the main term, above) and one error (the
Siegel–Walfisz remark, corrected above); (a, qr) = 1 in the Type I step checked. Finding 5 holds.
The auditor also called the parity remark of Finding 3 false, arguing that Bombieri's asymptotic sieve under EH
already counts integers with exactly k >= 2 prime factors. We do not accept this as stated: Selberg's example
a_n = 1 + lambda(n) has the same level of distribution as a_n = 1 and no integers with odd Omega, so Type I
information cannot fix the parity of Omega (Bombieri's Lambda_k sums mix different Omega, e.g. sum lambda Lambda_2
has no main term). The point is moot for this card: LWW's Theorem 2 already prescribes mu(p+2), so the parity part
of Finding 3 adds nothing new, and the card rests on the EH-strength consequence. Recorded as a disagreement.

## Scripts
None new for the mathematics (reading and argument). Related exploration: `code/explore/dilation_variance.py`
(see `notes/explorations.md`, Session 39). Lean: `lean/TwinPrimes/Orbit.lean` (orbit_sign, orbit_two_step and a
concrete instance; written by a helper agent, statements checked here; in Audit.lean).
