# Exploration log (newest first)

Each entry: date, session, idea, what was tried, outcome (dead end / inconclusive / promising), why.
"Promising" is not a result: it goes to the ideas ledger (origin "exploration") and needs the usual checks.

## 2026-11-14, Session 15 -- Moebius autocorrelations and twin irreducibles in F_2[T] at small degree (function fields)
- Idea: in F_q[T] the twin-prime analogue is proved for large q (Sawin-Shusterman), but q = 2 is the most
  "integer-like" case and characteristic 2 is known to be special for Chowla-type sums. Risky question: at the
  degrees we can reach, does F_2[T] show any parity-type structure in sum mu(f) mu(f + h), or any deviation of the twin
  count from the Hardy-Littlewood shape, that could point to a mechanism with an integer analogue?
- Tried: code/explore/ff_chowla.py (sieve for mu and irreducibility over F_2, polynomials as bit masks, checked against
  trial-division factorisation for deg <= 10 and the count 99 of irreducibles of degree 10). Output for n <= 22 in
  code/explore/ff_chowla_out22.txt. Shift 1 is NOT admissible over F_2 (f(0) = f(1) = 1 forces T | f + 1), so the
  twin count uses H = T^2 + T, with singular series S(H) = 3.3315 (product over irreducibles of degree <= 22).
- Outcome: INCONCLUSIVE, no usable mechanism. (i) P_2^H(n) / (S 2^n / n^2) = 1.016, 1.001, 0.995 at n = 20, 21, 22
  (HL shape fits). (ii) |C_h(n)| / 2^{n/2} stays between 0 and 2.3 for h in {1, T, T+1, T^2+T}, n = 12..22:
  square-root-size cancellation, no sign of a non-vanishing correlation at these degrees. (iii) C_T = C_{T+1}
  identically (the automorphism T -> T+1). (iv) A small curiosity: C_1(n) > 0 for every even n in 12..22 (largest
  4660 = 2.28 * 2^11 at n = 22), mixed signs for odd n; with six data points this may be noise. The characteristic-2
  literature on Chowla sums (Carmon-Rudnick; Conrad-Conrad-Gross) was NOT opened this session, so no comparison is
  claimed. Heuristic / exploratory only. If revisited: open those sources first, then test whether the even-degree
  sign pattern persists to n = 26 (bytearray sieve needs ~2^27 bytes, a few minutes).

## 2026-11-14, Session 14 -- Is there enough slack in Song-Yue's exponent conditions to save one step k = 48 -> 47? (exponential sums / Type III)
- Idea: the D182 level theta = 253/500 (omega = 3/1000) is set by many exponent inequalities of [SY26, Sec. 4],
  and the audit (notes/audit-sy236-thm418/) lists their exact margins. If one margin were loose, raising omega a
  little might move the variational criterion from k = 48 to k = 47 (a smaller tuple). Compare the omega the
  k = 47 criterion would need with the omega the printed margins allow.
- Tried: code/explore/level_slack.py. Criterion M_{k,eps} * 2 theta > 4 (eps = 15/506 as in
  cert_kin48_capfree_D22e). M_{47,eps} - M_{48,eps} at degree 16: 3.909715 vs 3.925064 (mk_general, Session 14),
  so M_{47,eps}(D22) is about 3.94356; k = 47 needs theta >= 0.507157, i.e. d omega >= 5.8e-4. With all other
  parameters fixed, the Type III margin (52) (1 - 1/3000, coefficient 7/3 on omega) allows d omega <= 1.4e-4 and
  the IIa margin (33) at gamma = 11/25 allows <= 2.2e-5.
- Outcome: DEAD END. The needed increase is 4 times the loosest margin and 26 times the IIa one, before the
  cap cost (about 3e-4 in the ratio) and before re-tuning eps and the caps to the new omega. Saving one k needs a
  genuinely stronger equidistribution estimate, not tighter bookkeeping. Heuristic only (the margins can be
  re-balanced by moving eta2, tau0, s3, eta3, which this toy does not do).

## 2026-11-13, Session 13 -- Primes in translates of the 236-tuple vs Hardy-Littlewood (probabilistic models of primes)
- Idea: test the probabilistic (Hardy-Littlewood) model directly on the Lean-checked admissible 48-tuple narrow48
  (diameter 236) that the conditional 236 rests on, and ask whether numerical data could say anything about
  DHL[48,2] (infinitely many n with at least 2 primes among n + h_i).
- Tried: code/explore/tuple_counts_hl.py (numpy sieve; HL 2-tuple prediction sum_{i<j} S(h_j - h_i) int dt/(log t log(t+d))).
  X = 1e6 / 1e7 / 1e8: prime pairs in translates 15612870 / 111570638 / 837030982, ratio to HL 0.99642 / 0.99885 /
  0.99969; n <= X with >= 2 primes in n + H: 496425 / 4903811 / 48078484 (about 48% of n at X = 1e8).
- Outcome: DEAD END (as expected). HL fits to 3e-4, which is well known. The data cannot bear on DHL[48,2]: the
  average number of primes in a translate is about 48/log X, which stays above 1 until X is about e^48 = 7e20, so in
  any computable range "two primes in a translate" is the typical event, not a rare one; the content of DHL is
  asymptotic. Not worth repeating with other tuples. Heuristic only.

## 2026-11-13, Session 12 -- Per-m caps in the toy capped problem: do caps on SUMS cause a large regain? (variational)
- Idea: Session 11's toy (one uniform cap) left open whether the 31% regain at k = 45 (Lemma 9.1 caps, Session 9)
  comes from the per-m pattern of the caps (separate caps on single coordinates and on sums of several). Smallest
  test: k = 3, T = {t >= 0, sum t <= 1, t_i <= c1, t_i + t_j <= c2}, symmetric polynomials of degree d = 5, 8.
- Tried: code/explore/toy_capped_perm.py (floating point; fibre in t_1 split into the four polytopes where
  min(c1, 1 - y2 - y3, c2 - y2, c2 - y3) is attained). Sanity: c2 = 1 reproduces Session 11's uniform-cap numbers
  (c1 = 0.8: trunc 1.614592, regain 0.101). Log: runs/explore_toy_capped_perm.log. d = 5 and d = 8 agree to 2 digits.
  regain: pair caps only (c1 = 1): c2 = 0.9 / 0.8 / 0.75 / 0.7 -> 0.085 / 0.067 / 0.051 / 0.037 (it FALLS as the
  pair cap tightens); mixed c1/c2 = 0.6/0.9, 0.6/0.8, 0.7/0.8, 0.5/0.9 -> 0.131, 0.110, 0.081, 0.126; single cap
  c1 = 0.6 -> 0.126.
- Outcome: DEAD END for the hypothesis. In the toy, caps on sums give a SMALLER regain than caps on single
  coordinates, and mixing them never exceeds about 13%. So the cap pattern alone does not explain the 31% regain at
  k = 45; remaining candidates are the enlarged (L > 1) part of the hybrid support and the size of k, which a k = 3
  toy cannot show. Not worth more toy work; if the question returns, test on the real k = 45 support with fewer caps
  switched on (the adjoint Gram machinery of capped_gram.py does this exactly). Heuristic only.

## 2026-11-13, Session 11 -- Toy model of the capped problem: what decides the "regain" fraction? (variational/spectral)
- Idea: Session 9's registered prediction failed because re-optimising on the capped support regained 31% of the
  truncation loss at k = 45 (Lemma 9.1 caps) against 9% at k = 49. Is the regain fraction a property of k, of the
  cap severity, or of the cap pattern? Test in the smallest model where everything is cheap: region
  T_c = {t >= 0, sum t <= 1, t_i <= c} (one uniform cap, no enlarged support), symmetric polynomials of degree d.
- Tried: code/explore/toy_capped.py (floating point, Delaunay + collapsed Gauss quadrature, exact for these degrees;
  sanity check M_2 = 1.3859333, M_3 = 1.646440 as in Polymath8b). Log: runs/explore_toy_capped.log.
  regain = (opt_T - trunc)/(opt_free - trunc), degrees d = 6, 10 (k = 2) and d = 5, 8 (k = 3) agree to 2 digits:
  k = 2: c = 0.95 / 0.9 / 0.8 / 0.7 / 0.6 -> 0.045 / 0.069 / 0.088 / 0.089 / 0.080.
  k = 3: c = 0.95 / 0.9 / 0.8 / 0.7 / 0.6 / 0.5 / 0.45 -> 0.025 / 0.060 / 0.101 / 0.120 / 0.126 / 0.126 / 0.120.
- Outcome: INCONCLUSIVE. With one uniform cap the regain stays small (<= 13%) and plateaus as the cap tightens,
  rising slowly with k; this fits k = 49 (9%, uniform cap 0.6 on Stadlmann's support) but not k = 45 (31%), which
  suggests the large regain there comes from the non-uniform per-m caps of Lemma 9.1 (different caps for m = 1, 2,
  3+), not from k. Not tested: per-m caps in the toy (needs k >= 3 with caps on sums of pairs) -- the natural next
  step if this question matters again. Heuristic only; nothing enters a paper.

## 2026-11-13, Session 10 -- Is Song-Yue's objection to [Sta26, Lemma 5] real? (exponential sums / Type I-II area)
- Idea: [SY26, Remark 4.23] says the large-gamma step of the proof of [Sta26, Lemma 5] (Baker-Irving Type I)
  applies the Type IIa lemma with the factors swapped, although Type IIa needs the shorter factor to be
  Siegel-Walfisz and Lemma 5 assumes nothing about it. Read the arXiv v1 text (fetched 13 Nov, pdftotext) and
  check the claim against the statements.
- What we read (arXiv:2608.31126v1, Sec. 3.2, 3.3.5, Def. 9, proof of Prop. 3, Case I):
  * Lemma 3 (Polymath Type II): f = alpha * beta, beta at scale N = x^gamma <= x^{1/2}, "Suppose also that beta has
    the Siegel-Walfisz property".
  * Lemma 5 (Baker-Irving Type I): alpha an arbitrary coefficient sequence at scale M, beta smooth at scale
    N = x^gamma; no Siegel-Walfisz hypothesis on alpha.
  * Proof of Lemma 5, range gamma in (1/2, 1/2 + 2 omega + eps]: "we can apply our Lemma 3 (with the roles of alpha
    and beta swapped and gamma replaced by 1 - gamma)". After the swap the shorter factor is alpha (scale x^{1-gamma}
    <= x^{1/2}), so Lemma 3 needs alpha to be Siegel-Walfisz.
  * Definition 9 (I) and Case I of the proof of Prop. 3 apply Lemma 5 to "alpha a coefficient sequence at scale M"
    (again no Siegel-Walfisz hypothesis); Case (II) states the hypothesis explicitly for both factors.
- Outcome: INCONCLUSIVE, but the textual gap is CONFIRMED: as written in v1, that step uses a hypothesis that neither
  Lemma 5 nor Def. 9 (I) provides. Whether it matters is open: the alpha's that occur in a Harman-sieve
  decomposition are usually built from primes / rough numbers and may well be Siegel-Walfisz (then adding the
  hypothesis to Def. 9 (I) for that gamma-range repairs the proof); alternatively that gamma-range might be covered
  differently. We have not checked either repair. Status for the paper: "possible gap in the analytic input of 240,
  raised by [SY26, Rem. 4.23]; the cited step reads as they say (checked against arXiv v1); repair not checked".
- Why it matters: 240 (and 236, which reuses Stadlmann's estimates) rests on this analytic input; our reproduced
  240 is already labelled conditional on it.
