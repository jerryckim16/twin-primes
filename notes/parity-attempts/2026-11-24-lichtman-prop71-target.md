# Route card: what Lichtman's Type II (Prop. 7.1) needs from the target, and whether "one rough variable" moves the parity step (2026-11-24 (Session 52))

**Classification: located (literature reading + exact toy check; audited, see the end).**
- Lichtman's Type II estimate (arXiv:2611.28392v1, Prop. 7.1, pp. 19-20, proved in §§6-11) uses the target
  mu(mn+1)phi(mn+1) only through the same three properties that the Session 50 card found in LWW:
  P1 (boundedness: |c(q)| <= 1, then discarded by Cauchy-Schwarz, (6.10) p. 17), P2 (sign-multiplicativity at the
  active primes: mu(v/a) = (-1)^k mu(v), phi_-(pv) = phi_-(v), inside the Ramare identity (6.5), p. 16), and P3
  (Bombieri-Vinogradov with zero main term, used only for the Type I sums, Prop. 5.5 via Lemma 5.4).
- All Type II cancellation comes from the SOURCE coefficient alpha_m = mu(m)R_z(m)m^{iv}w(m): on the major arcs
  through Prop. 8.1 (Mobius-character cancellation, = LWW Prop. 2.2 with zeta in place of 0.24, p. 22); the minor arcs
  "do not exploit any Mobius cancellation" (p. 15, line 963 of the extract; also p. 6). "Only one rough variable" is a
  relaxation on the source side (beta_n unrestricted, so the smooth-part weight U(s_n) can sit in beta). It does not
  touch the target side. **Our location of the parity-sensitive step, "P2 => T_3 small" (S50), is unchanged; in
  Lichtman's notation it is "(6.5) + Props. 8.2, 9.1 => (7.1)".**
- **New, and a correction to our S51 news note:** Lichtman v1 writes out the proof of Theorem 1.1 only (binary Chowla,
  mu(n)mu(n+1)). Theorem 1.2 (sum_{p<=X} mu(p+2) << pi(X)/(log X)^{1/2-eps}, the refinement of LWW) and Theorem 1.3 are
  supported in v1 only by the sentence "the same proof method also establishes a companion result for Mobius on shifted
  primes" (p. 2); there is no further occurrence of "p + 2" or of Theorem 1.2 in the 36 pages. Prop. 7.1 requires the
  rough coefficient to be alpha_m = mu(m)R_z(m)m^{iv}w(m), and its major-arc step (Prop. 8.2) needs that Mobius factor.
  For a prime source the decomposition, and which coefficient carries mu, are not written. So v1 is independent
  evidence for the Type II machinery (Props. 8.2, 9.1 adapt LWW's Prop. 5.3 and Sect. 4 "for completeness", p. 6) and
  for Theorem 1.1, but it is NOT a written re-proof of LWW's shifted-prime theorem. Our S51 wording ("an independent
  expert re-derives and sharpens LWW's theorem; the first strong outside evidence that LWW's main claim holds") was too
  strong and is downgraded (flag update of 24 Nov, S52).
- **First unresolved implication:** unchanged, LWW Prop. 4.2 (now also: the prime-source Type II in Lichtman's
  framework, unwritten in v1). The Sessions 39-40 consistency implication (P^+(p+2) > p^{1-o(1)}) needs a prime source,
  so Lichtman v1 gives no second written route to it.
- Twins: untouched. For a prime N = p+2 > z the typical part Lambda(N)phi_+(N) is 0 (a prime has no divisor in the
  active intervals), so the method sees twin pairs only through the exceptional set (cf. the S51 exploration).
- Not in the parity paper. No parity-breaking content of our own. No error in Lichtman or LWW found.

## Question
Session 51's news note queued: read Lichtman's Prop. 7.1 against the S50 analysis (target properties P1-P3 of LWW).
(i) Which properties of the target does his Type II use? (ii) Does "only one rough variable" change where the
parity-sensitive step sits? (iii) Does his paper give a second written route to the S39-S40 consistency implication?

## Criteria (written before reading §§6-8)
- Success: a list of every place in the proof of Prop. 7.1 where mu(mn+1)phi(mn+1) is used, with page/equation, and a
  verdict on whether a target failing P2 (Lambda) could pass; plus a verdict on (iii).
- No-go: Prop. 7.1 uses a target property outside P1-P3 (e.g. cancellation of the target sign on major arcs). Then
  the S50 location would be incomplete and would have to be revised.
- Cheapest decisive check: read §6 (pp. 15-18), Prop. 7.1's proof (pp. 19-20), the opening of §8 (p. 22) and the
  head of §9 (p. 23); check the Ramare identity exactly on toy intervals.

## Source
J. D. Lichtman, "Improved bounds for the binary Chowla conjecture", arXiv:2611.28392v1 (20 Nov 2026), 36 pp.
PDF SHA-256 4337830d0ff830ee3952513cdc5cb77c70201ff3f54224531764bc3492b3f838 (matches notes/news-2026-11-24.md). Read
with pdftotext -layout (extract in the scratch directory only; PDF not committed). Read: pp. 1-6 (intro, outline,
Fig. 1), §3 (pp. 9-10), §6 (pp. 15-18, to Lemma 6.2), §7 (pp. 19-21, Prop. 7.1 and its proof, Cor. 7.2, Prop. 7.3
statement), §8 (pp. 22-23). Not read: §§4-5 beyond statements, §§9-11 (minor arcs) beyond their first lines.
All page numbers are printed page numbers (approximate where the extract loses headers).

## Findings
1. **Target in the Type II sum (6.6), p. 16:** T = sum_{m~M, n~N} alpha_m beta_n mu(mn+1)phi(mn+1), alpha supported
   on z-rough m.
   - (6.7): the pairs with p^2 | mn+1 for some p in P0 cost O_A(XL^{-A}) (roughness of m fixes n mod p^2). Uses only
     |target| <= 1.
   - (6.5) (Lemma 6.1): for P0-squarefree v, mu(v)phi(v) = (-1)^k sum_{a in A, a|v} mu(v/a)phi_-(v/a)/prod_i(omega_i(v/a)+1).
     Its proof uses exactly mu(v/a) = mu(v)/mu(a) = (-1)^k mu(v) (multiplicativity with (a, v/a) = 1) and
     phi_-(pv) = phi_-(v) (6.3). This is P2 with sigma = -1 per active prime.
   - (6.8)-(6.10): with c(q) := mu(q)phi_-(q)/prod(omega_i(q)+1), |c| <= 1, Cauchy-Schwarz over q gives
     |T_Y|^2 << (X/Y) S_Y, and S_Y (6.11) involves only alpha, beta and a, b in A. The target is gone (P1).
   - Consequence (Proved here, elementary): steps (6.8)-(6.10) hold verbatim for any target of the form
     G_c(v) = sum_{a in A, a|v} c(v/a) with |c| <= 1 (for such a target (6.5) is the definition, and (6.7) is not
     needed). This is the "G_g" class of the S49 audit (Type II bound for targets of that form, not for every bounded
     target). The target Lambda(N) itself is not of this form on N > z: Lambda(N)phi_+(N) = 0 while
     sum_a Lambda(N/a)/prod(...) > 0 whenever N = a*prime (computed below).
2. **Where the saving comes from (pp. 6, 15, 22):** "On the minor arcs, we do not exploit any Mobius cancellation, and
   only use the variable size and support on rough integers" (§6, first lines). "On the major arcs we exploit
   cancellation in the rough Mobius factor from the first coefficient" (§8, first line), through Prop. 8.1 = [LWW,
   Prop. 2.2 and (2.11)] with zeta in place of 0.24 and D <= 3x ("both changes follow from their proof"; we did not
   check this claim). The cancellation in the major-arc proof (Prop. 8.2) is |M_chi(t)| << L^{-A'} for the Dirichlet
   polynomial of alpha_m chi(m) (p. 23). The target's characters never appear: after (6.10) there is no target left.
   - Reading note: p. 6 says "neither source of saving requires cancellation in the coefficients' signs". In context this
     refers to the two minor-arc steps (Fourier orthogonality and the count of live primes), as p. 9 line 533 says
     ("neither minor arc step uses Mobius cancellation"). Read literally for the whole Type II, it would contradict §8.
     Wording only.
3. **"One rough variable" (p. 3, p. 6):** Prop. 7.1 asks for alpha rough and lets beta be arbitrary with |beta| <= L^C.
   This lets the smooth-part weight U(s_n) and mu(s_n) ride in beta (Cor. 7.2, Prop. 7.3), which is what the exact
   prime-interval split (typical/exceptional, §2) needs. It is a source-side relaxation; the target is used as in 1.
   So (ii): no change to the S50 location.
4. **Type I (P3):** Prop. 5.5 ("Type I cancellation", p. 13) with G(n) = mu(n+1)phi(n+1), via a weighted BV estimate
   (Lemma 5.4; statement only read). A Lambda-type target would bring a main term here, as in S40. Not re-done.
5. **(iii) Prime source.** Theorem 1.1's source is mu(n) (Vaughan, Prop. 5.2), giving alpha_m = mu(m)R_z(m) directly.
   For Theorem 1.2 the source is a prime; v1 contains no proof (search of the whole extract for "1.2", "p + 2", "shifted
   prime": only pp. 1-3). Whether the prime-source Type II has a rough mu-coefficient of the form Prop. 7.1 requires is
   not written. So v1 gives no second written route to the S39-S40 implication. LWW's own route (their Prop. 4.2 and
   5.3 with a prime source) remains the only written one.

## Computation
code/parity/lichtman_ramare_check.py [N] (/usr/bin/python3 -I; ~1 s at N = 1e5; exact Fractions; output
code/parity/lichtman_ramare_check.out). Toy active intervals {5, 7} and the primes in [11, 100] (k = 2, |A| = 42),
passive factor phi_-(v) = (-1)^{v_2(v)} (satisfies (6.3)).
- (6.4) sum <= 1: 0 failures for v <= 1e5.
- (6.5) for mu*phi: 91327 P0-squarefree v checked, 0 failures.
- Twin target: Lambda(v)phi_+(v) = 0 for every v (k = 2 forces two distinct prime factors), while the extracted form
  sum_a Lambda(v/a)/prod(...) is nonzero for 3868 v. So the (6.5)-analogue fails for Lambda: P2 is exactly what Lambda
  lacks.
This is a sanity check of the identity as read, not a check of Lichtman's analysis.

## Literature scope
Only Lichtman v1 and our own cards (S39, S40, S49 audit, S50, S51). No search for comments on Lichtman's paper beyond
the S51 news search (24 Nov, 09:34 UTC).

## Audit
(appended below after the fresh-context audit)
