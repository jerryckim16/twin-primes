# Lü–Wang–Wu, "On the Hardy–Littlewood–Chowla conjecture", arXiv:2610.20242 (news found 20 Nov 2026, Session 38)

Status: **Claimed** (preprint; not verified by this project; 75 pp., v1 14 Oct 2026 (53 KB), v2 19 Nov 2026 (78 KB),
SHA-256 of the v2 PDF read: 7ac34131...2d423000). Authors: Guangshi Lü, Zhiwei Wang, Jie Wu (Shandong University).
Read: abstract, Section 1 (pp. 1-4), Sections 2.2-2.3 (Vaughan decomposition, auxiliary weight W, Prop. 2.3),
Section 4.1 (reduction of the Type II sum, Lemma 4.1, equation (4.12)), statement of Prop. 4.2, references.
Not read: the proofs of Sections 3-6 and the appendix (about 70 pages). Not checked.

## What is claimed
- Theorem 1: sum_{p <= x} mu(p+2) = o(pi(x)), equivalently sum_{n <= x} Lambda(n) mu(n+2) = o(x).
  The authors call this "a folklore conjecture and a well-known model case for the parity problem in sieve
  theory", in print since Hildebrand 1989 (also Pintz, Murty–Vatwani).
- Theorem 2: #{p <= x : mu(p+2) = kappa} = (1/2) prod_{p>2}(1 - 1/(p(p-1))) pi(x) (1 + o(1)), kappa = +-1.
- Remark 1: the approach is "very likely applicable" to other bounded multiplicative f with a Bombieri–Vinogradov
  type property, "such as the Liouville function" (not done). Remark 2: a bound pi(x)/(log log x)^A should be
  possible. Remark 3: shifts h << x under quasi-RH (not done).
- Remark 4: cites an OpenAI release of 6 Oct 2026 (722 manuscripts), one of which ("Prime Predecessors with an
  Even Number of Prime Factors", their ref. [18]) states that infinitely many primes p have mu(p-1) = 1.
  Not opened by us.

## Mechanism (as far as read)
- Vaughan's identity for Lambda(n) with U = V = x^{1/5}, sifted variables (no prime factors below
  Z = exp(L^{0.24})); Type I sums by a Bombieri–Vinogradov-type estimate for mu (Section 3).
- An auxiliary weight W(n+2) = prod_i omega_i(n+2) rho^{omega_i(n+2)-1}/V_i built from K disjoint sets of primes
  P_i = (exp(L^{a_i}), exp(2 L^{a_i})], 1/10 < a_i < 1/5 (so of size x^{o(1)}); on average W(p+2)/m_W is about 1 on
  primes (Prop. 2.3). Writing mn + 2 = a h with a = p_1...p_K uses the multiplicativity of mu at the shifted
  point: mu(ah) = (-1)^K mu(h).
- After Cauchy–Schwarz the Type II sum becomes a count Q_Y of solutions of b m n - a r s = 2(a - b) with
  weights (4.12), compared with a major-arc model Q_Y^maj (Prop. 4.2: Q_Y - Q_Y^maj << X Y L^{-A}); a
  circle-method / operator analysis (Sections 4.2-4.7, about 45 pages) and a character–Mellin estimate
  for the major arcs (Section 5).
- So the parity-sensitive input is (if the proof is correct) the small-prime multiplicativity of mu at n+2
  combined with the bilinear (Type II) structure of Lambda(n); this is outside the Liouville-pattern class of
  the parity paper (`rem:marg`: weights of other kinds are not covered), consistent with that class.

## Distance to twin primes (Proved here, elementary; see the parity paper, `prop:ss-split`, `rem:ss-transfer`)
- The mechanism needs multiplicativity at n+2; Lambda(n+2) has none (Lambda(ah) = 0 for a > 1 composite
  and h > 1), so the weight-W step has no analogue for twins.
- In `prop:ss-split`, the twin asymptotic is equivalent to T_D(x) = o(x) with D = x^{1/2}(log x)^{-B}; the
  e = 1 term of T_D is essentially sum_p mu(p-2) log p log(p-2), which needs o(x), i.e. a saving of a full
  log x beyond Theorem 1 (rem:ss-transfer), and T_D needs all e up to x/D with uniformity. Theorem 1 gives
  o(x) for sum Lambda(n) mu(n+2), hence only o(x log x) for the log-weighted e = 1 term.
- Within the Liouville-pattern class, "p prime and lambda(p+2) = -1 infinitely often" (a star target, single
  prescribed d) is blocked (parity paper `prop:pintz` discussion, Pintz p. 3). The Liouville analogue of
  Theorem 1 (Remark 1, not proved) would give it; then the "first unresolved implication" of the Session 26
  card (one prescribed d) would be claimed in the literature.

## Numerical sanity check (Computed; NOT a verification)
code/parity/lww_numerics.py [X] (segmented sieve; .out): sum_{p <= x} mu(p+2)/pi(x), sum lambda(p+2)/pi(x) and
the two counts against Theorem 2's constant, x = 10^4, ..., 10^9. Results in code/parity/lww_numerics.out
(values copied into the Session 38 log entry).

## Effect on our papers
- Parity paper v1.0 (frozen) says in several places that sum_p mu(p+h) = o(pi(X)) is open / known only on
  average (sections on Bombieri's sieve, `rem:ss-transfer`, `subsec:lt22`, open questions). Erratum-level
  status note v1.0.1 added: "claimed in [LWW26], not verified here". No new section.
- Flag for Jerry (notes/flags-for-jerry.md, 20 Nov 2026).

## Session 39 (20 Nov 2026, 11:34 AM CT run): Type II structure and a consequence
Read further: pp. 4-11 and 14-19 (Prop. 2.1-2.3, Section 3 start/end, Section 4.1, Lemma 4.1, Prop. 4.2, start of
4.2); the audit helper also read Section 5 (pp. 61-71, proof of Theorem 1 in (5.31)-(5.33)).
- In (4.6) Cauchy–Schwarz over h uses only |mu(h) rho^{omega(h)}| <= 1; Q_Y does not contain the target. The target
  is used only through boundedness and mu(ah) = (-1)^K mu(h); the Type I part uses BV for mu (3.1).
- Prop. 4.2 holds for arbitrary coefficients; K must be large in terms of A (operator bound << L^{1-0.005K} + L^{-A}).
- Consequence (conditional, with one gap): the same argument with Lambda(h) would give P^+(p+2) > p^{1-o(1)}
  infinitely often, an EH-strength statement (record unconditional exponent 0.677, Baker–Harman 1998; 0.679 claimed
  in arXiv:2508.18285v3). Route card: notes/parity-attempts/2026-11-20-lww-orbit-test.md. Flag updated.

## Session 40 (21 Nov 2026, 7:34 PM CT run): Section 3 read line by line
Read pp. 4-5, 7-14 (Prop. 2.1, Prop. 2.3 with proof, Section 3 in full), 15-18, 61, 63, 69-70 of the same v2 file (SHA-256 7ac34131...2d423000; still v2 on 21 Nov, no public comment found). Result: the Type I sums use the target only through residue-class sums (route card notes/parity-attempts/2026-11-21-lww-main-term.md), which closes the Session 39 main-term gap in outline.

## Literature check for the v1.1 subsection (Session 47, 23 Nov 2026; preliminary, one search)
- arXiv:2610.20242 abs page: still v1 (14 Oct) and v2 (19 Nov), no comments field (checked 23 Nov, ~09:45 UTC).
- Search scope: one web search for any source deriving a largest-prime-factor consequence for p + 2 from the LWW Type II
  estimate. None found. Hits checked by abstract only: Z. Yang, arXiv:2609.24347v1 (liminf density of
  P^+(p-1) >= p^c for c <= 1/2) and arXiv:2608.13299 (limsup density for e^{-5/16} < c < 1, using level x^{5/8} for
  well-factorable convolution forms); R. Li arXiv:2508.18285v3 and arXiv:2510.04026 already in this file. None of them
  concerns exponents near 1 or uses LWW, so the comparison with 0.677 (0.679 claimed) stands.
- Still to do before v1.1: a second search (Google Scholar-style terms, "Hildebrand conjecture mu(p+2)", citations of
  2610.20242), and a check that LWW's own v2 text does not already remark the transfer (Section 1 and Remarks 1-4 were read
  in Session 38; re-read them for this point).
