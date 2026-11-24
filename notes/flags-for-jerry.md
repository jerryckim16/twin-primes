# Flags for Jerry (newest first; entries are updated, never deleted)

## 2026-11-24 (Session 51) — News: an independent expert sharpens Lü–Wang–Wu's theorem (strong outside evidence that it holds; not a check by us), and binary Chowla is reported resolved
- **What.** (1) Lichtman, arXiv:2611.28392v1 (20 Nov 2026), Thm 1.2 (p. 2): sum_{p<=X} mu(p+2) << pi(X)/(log X)^{1/2-eps},
  "a quantitative refinement of Lü, Wang, and Wu" (he cites their v1). The method replaces LWW's averaged weights by an
  exact partition into prime intervals and uses that only one Type II variable needs to be rough (p. 3, his Prop. 7.1).
  (2) The same paper states (p. 1) that the two-point (Cesàro) Chowla conjecture "was recently resolved ... by OpenAI"
  (OpenAI Math Release preprint, Sept 2026, 87 pp.; we have not found or read it) and proves sum mu(n)mu(n+1) <<
  X/(log X)^{1-eps} (Thm 1.1). (3) Gou–Wang–Xu, arXiv:2611.18825v1 (13 Nov): the Hardy–Littlewood prime-pair asymptotic
  under RH plus a Ratios Conjecture (after S. Lee, arXiv:2610.32672v2), and, unconditionally, prime-pair asymptotics in
  F_q[T] for every fixed odd q > 10^200, including prime fields q = p (Thm 1.6, p. 4; new for q = p, p^2 by their account).
- **Why it might matter.** (1) is the first outside expert work that re-proves and improves LWW's claimed parity-breaking
  theorem; it shifts the LWW flag towards "probably correct" (still unrefereed and AI-assisted). Our location of the key
  step (P2 => T3 small) should be compared with his Prop. 7.1. (2) If correct, statements in our notes and papers that
  call two-point Chowla open are out of date. (3) Conditional twin-prime asymptotics from L-function ratio statistics are
  consistent with the parity paper's position (parity limits sieves, not conjectural L-function inputs); none of this
  proves anything about twin primes over Z unconditionally.
- **Evidence label.** Claimed (unrefereed preprints; we read only the introductions, pages cited in notes/news-2026-11-24.md).
- **Checked.** Abstracts and pp. 1-3 (Lichtman), pp. 1-6 (Gou–Wang–Xu), SHA-256 recorded. **Not checked:** any proof; the
  OpenAI preprint (not located); Lee's paper beyond its abstract.
- **Files.** notes/news-2026-11-24.md. **Needs outside expert review:** yes (as for the whole LWW flag).

## 2026-11-24 (Session 50) — Update to the Lü–Wang–Wu flag: which properties of μ their argument uses as the target, and a fake target that fails only one of them (locates the step further; not an error found)
- **What.** Reading arXiv:2610.20242v2 for every use of the target μ(n+2): Sections 2-3, p. 15, (4.6) and the removal
  of W on p. 70 use only (P1) |f| ≤ 1, (P2) a fixed sign f(pv) = σ f(v) at the auxiliary primes in
  R = (exp(L^{1/10}), exp(2L^{1/5})], and (P3) Bombieri–Vinogradov with zero main term to moduli x^{2/5+o(1)}
  ((3.1), p. 13). Props. 2.2 and 5.3 concern the prime variable, not the target. λ passes after routine changes.
  μχ and Remark 1's "general bounded multiplicative f" are not covered verbatim; a split by residue classes mod q₀,
  or pigeonhole thinning of the auxiliary primes, would reduce them to a twist of their Prop. 5.3, which we have
  not checked. A fake target g3' built from Λ(N−2) satisfies P1 and (heuristically) P3, and its correlation with
  the primes is about 1, but it fails P2. So, heuristically, all of the parity-breaking weight sits on
  "P2 ⟹ the Type II sum T₃ is small" (p. 15 + (4.6) + Props. 4.2 and 5.3), the same place found in Sessions 39-40.
- **Why it might matter.** It tells an expert exactly where to look: the fixed-sign step and their Prop. 4.2. It is
  consistent with LWW's own heuristics and implies no error by them. Nothing here concerns twins.
- **Evidence label.** Literature (read in v2, pages cited in the card) plus Heuristic (P3 for the fake targets;
  numerical toy checks in code/parity/lww_mu_vs_lambda.py).
- **Checked.** A fresh-context adversarial audit re-read the PDF (SHA-256 matched) and re-ran the script with
  identical output. It found 1 error (the q = 1 Type I term of the fake target does not vanish; it is small only by P3,
  heuristically), 2 gaps and 4 overstatements; all were applied. **Not checked:** LWW Props. 4.2 and 5.3, and whether
  Prop. 5.3 accepts a character twist or thinned prime sets.
- **Files.** notes/parity-attempts/2026-11-24-lww-mu-vs-lambda.md, code/parity/lww_mu_vs_lambda.py (.out).
- **Needs outside expert review:** yes (as for the whole LWW flag).

## 2026-11-23 (Session 47) — (minor) Green, arXiv:1604.04481v4, p. 2: the example showing that his Theorem 1.1 needs prime moduli is misprinted
- **What.** Green writes that Theorem 1.1 fails without the restriction to prime moduli, "as may be seen by taking
  f(n) = (−1)^n μ²(n)", whose mean is "very small". As printed the function is not multiplicative (its value at 1 is −1);
  the multiplicative variant (−1)^{n+1} μ²(n) has mean 2/π², not a small number. The point itself survives: for
  (−1)^{n+1} μ²(n) the theorem does fail for even moduli (class means 0.81 for a = 1 and −0.40 for a = 2 mod 2018 and
  20014, against the global mean 0.2026).
- **Why it might matter.** It doesn't, beyond a misprint. No result in the paper depends on it.
- **Evidence label.** Literature (read in v4) plus Computed (code/parity/green_example_check.py, N = 4·10⁶).
- **Checked.** Found by the fresh-context audit of the Session 47 route card and confirmed by the card's author. The
  journal version was not checked.
- **Files.** notes/parity-attempts/2026-11-23-granville-shao-level-half.md. **Needs outside expert review:** no (typo-level).

## 2026-11-21 (Session 40) — Update to the Lü–Wang–Wu flag: the Session 39 gap is closed in outline; the strong consequence now rests only on their Prop. 4.2 and Prop. 5.3 (a red flag for those, not an error found)
- **What.** Session 39 left one gap: the main term of the modified count. This run closes it in outline without computing
  main terms by hand. LWW's Type I sums (Section 3) use the target only through its sums in reduced residue classes to
  moduli up to x^{2/5+o(1)}, and their Type II bound does not see the target at all. So one can compare the target
  with a sieve model f = kappa_D 1_{(h,P(D))=1}: it has the same distribution in progressions as the primes, and its count
  is computed directly as 2 C_2 x (C_2 the twin-prime constant). If LWW's Prop. 4.2 and Prop. 5.3 hold, then
  >> x/(log x)^2 primes p in (x, 2x] have p + 2 = a·l, l prime, a a product of K primes each at most exp(2(log x)^{1/5}).
  Hence P^+(p+2) >= p·exp(-2K(log p)^{1/5}) infinitely often. Unconditionally only P^+(p+2) > p^{0.677} is known; exponents
  near 1 are known only under Elliott–Halberstam, and the cofactor here is smaller than even that argument gives.
- **Why it might matter.** It makes the Session 39 observation a complete conditional implication: either LWW's Type II
  estimate proves much more than they claim, or it fails. An expert should check Prop. 4.2 (about 45 pages) and
  Prop. 5.3 first. Nothing here brings twin primes closer (twins are the case K = 0, where nothing is gained).
- **Evidence label.** Proved here in outline, conditional on LWW Prop. 4.2 and Prop. 5.3 (Claimed). The classical inputs
  are Bombieri–Vinogradov and the fundamental lemma.
- **Checked.** A fresh-context adversarial audit read LWW Sections 2-5 line by line. Findings 1-3 hold. It corrected
  the prime count (x/L^2, not x/L) and the wording of the comparison with EH, and found two errors and one gap in a side
  remark (the fake target 1_S), which has been rewritten. Exploration: real primes behave like the random model for that
  side test, so it gives no contradiction. **Not checked:** LWW Prop. 4.2 and Prop. 5.3 themselves.
- **Files.** notes/parity-attempts/2026-11-21-lww-main-term.md, notes/parity-attempts/2026-11-20-lww-orbit-test.md,
  notes/sources-lww26.md, code/explore/fake_target_density.py.
- **Needs outside expert review:** yes.

- **Jerry's decision (23 Nov 2026, 19:45 UTC, via the coordinator session):** Jerry has seen this flag and approved ONE short LWW subsection in the parity paper (v1.1), as specified in the weekly review of 23 Nov, section 4(a): at most about one page; what LWW claim (Claimed); the structural reading; the Sessions 39-40 conditional implication labelled "Proved here in outline, conditional on [LWW] Prop. 4.2 and Prop. 5.3"; the comparison with 0.677; "does not give twins (K = 0)". The other two conditions still apply before release: a literature check that the transfer is not already remarked (LWW v3 if it exists, or elsewhere), and neutral wording (a consistency observation, not an error found).
- **Update (Session 49, 23 Nov 2026):** released as Section 6.4 of the parity paper v1.1 (refrozen). Release conditions met: LWW still v2 (no v3, no public comment found; notes/sources-lww26.md); neutral wording ("a consistency observation ... not an error found ... unless our outline has a gap"); a fresh-context adversarial audit (notes/audit-parity-v11.md) found one real error in the draft's wording (the Type II bound holds for targets of the form prod V_i^{-1} sum_{a|N} g(N/a), not for every bounded target; the conditional implication itself was confirmed) plus mis-citations, all fixed. 0.677 is cited only as quoted by Li and Ding-Wang (Baker-Harman not opened). The flag stays open: LWW Props. 4.2 and 5.3 still need an expert's check.

## 2026-11-20 (Session 39) — Update to the Lü–Wang–Wu flag: their Type II estimate, if correct, would also give an Elliott–Halberstam-strength theorem they do not state (a red flag for their Prop. 4.2, not an error found)
- **What.** Reading Section 4.1 of arXiv:2610.20242v2: after writing n + 2 = a h with a a product of K auxiliary primes,
  the authors apply Cauchy–Schwarz over h and discard mu(h) ((4.6)); the remaining quantity Q_Y does not involve the
  target, and the saving comes from Prop. 4.2 plus a major-arc bound (Section 5). Replacing mu(h) by Lambda(h) costs only a
  factor (log x)^{1/2}, so the same estimate would give infinitely many primes p with p + 2 = a·l, l prime, a = x^{o(1)},
  i.e. the largest prime factor of p + 2 exceeds p^{1-o(1)} infinitely often. The best unconditional exponent in print
  is 0.677 (Baker–Harman 1998; 0.679 claimed by R. Li, arXiv:2508.18285v3, who writes that even 0.678 "seems impossible
  without any new things"); exponents near 1 are known only under Elliott–Halberstam.
- **Why it might matter.** Either LWW's Type II estimate (Prop. 4.2, about 40 pages) is an even larger breakthrough than
  they claim, or it fails. This is where an expert should look first. It does not bring twin primes closer: the twin case
  is K = 0, where the argument gains nothing.
- **Evidence label.** Proved here in outline, conditional on LWW's Prop. 4.2 and Section 5; one gap left open (the Type I
  main term of the modified sum must be computed; it needs Bombieri–Vinogradov for mu averaged over the auxiliary
  moduli). Literature values opened in arXiv:2508.18285v3 and arXiv:2510.04026v2.
- **Checked.** A fresh-context adversarial audit (helper agent, read LWW pp. 1-20 and 61-71) confirmed the structural
  reading and the conditional implication, found one wrong justification (fixed) and the main-term gap; one point of
  disagreement (on parity) is recorded in the route card. **Not checked:** LWW's Prop. 4.2 itself.
- **Files.** notes/parity-attempts/2026-11-20-lww-orbit-test.md, notes/sources-lww26.md, lean/TwinPrimes/Orbit.lean.
- **Needs outside expert review:** yes (both the preprint and this consistency observation).

## 2026-11-20 (Session 38) — A 2026 preprint claims a proof of a standard parity-problem model case: sum_{p<=x} mu(p+2) = o(pi(x)) (Lü–Wang–Wu, arXiv:2610.20242)
- **What.** G. Lü, Z. Wang, J. Wu, "On the Hardy–Littlewood–Chowla conjecture", arXiv:2610.20242 (v1 14 Oct 2026, v2 19 Nov
  2026, 75 pp.). Theorem 1 claims that the Möbius function cancels on the shifted primes p + 2 (Hildebrand's 1989
  conjecture, which they call "a well-known model case for the parity problem in sieve theory"); Theorem 2 claims that
  mu(p+2) = +1 and = -1 each occur for half of the primes with p + 2 squarefree. Their Remark 1 says the method should also
  give the Liouville version (not done there). Their Remark 4 cites an OpenAI release of 6 Oct 2026 claiming infinitely
  many primes with mu(p-1) = 1 (not opened by us).
- **Why it might matter.** Until now this was known only on average over the shift (Lichtman 2022, Lichtman–Teräväinen
  2022). If correct, it is parity-breaking for a binary problem with a prime variable. It does NOT give twin primes:
  the twin problem needs Lambda at both places, and the mechanism (as far as we read it: auxiliary small prime factors
  of n + 2 via the multiplicativity of mu, then Cauchy–Schwarz and a counting problem for b m n - a r s = 2(a - b)) has no
  analogue for Lambda(n+2). In our reformulation (parity paper, Prop. ss-split) the twin asymptotic would still need a
  saving of a full log x and uniformity over many progressions.
- **Evidence label:** Claimed (preprint). We read Sections 1, 2.2-2.3, 4.1 and the statement of Prop. 4.2 (notes in
  notes/sources-lww26.md); the 70 pages of proof are not checked. Computed sanity check only (not a verification):
  code/parity/lww_numerics.py gives sum_{p<=x} mu(p+2)/pi(x) = -0.000060 and sum lambda(p+2)/pi(x) = -0.000126 at
  x = 10^9, and the two counts of Theorem 2 within 0.01% of the predicted (1/2)(0.74791...) pi(x).
- **What changed here.** Parity paper v1.0.1 (status note only): the places that called this problem open now say
  "Claimed in [LWW26], not verified here".
- **Needs outside expert review:** yes, for the preprint itself. This is not our result. An expert's opinion on whether the
  Type II argument (Section 4) is sound would decide how the parity paper should describe it.

## 2026-11-16 (Session 26) — (minor) Pintz's 2010 parity-sensitive theorem improved from 16 to 12 with Maynard weights (probably folklore)
- **What.** J. Pintz (arXiv:1004.1065v1, 2010) proved that some even d with 0 < |d| <= 16 has lambda(p+d) = -1 for infinitely
  many primes p (lambda = Liouville), a statement that sidesteps the parity barrier. Redone with Maynard's weights, the same
  argument needs only theta M_k > 1 instead of the GPY condition, so 5-tuples suffice under Bombieri-Vinogradov
  (M_5 >= 1417255/708216, Maynard 2015 (8.17)), giving 0 < |d| <= 12. Also 0 < d <= 14 (Pintz 18), and better conditional
  thresholds (0.72154 / 0.60752 / 0.54230 against Pintz's 0.729 / 0.616 / 0.554).
- **Why it might matter.** Only as a small, honest improvement of a published parity-sensitive result, and as a test of the
  parity paper's criterion (it predicts exactly this: the disjunction is reachable, a single prescribed d is not). It says
  nothing about lambda(p+2) alone and nothing about twin primes.
- **Evidence label:** Proved here (parity paper v0.11, Thm. thm:pintz-maynard, Cor. cor:pintz12); the ratios are Computed
  and agree exactly between two independent programs (code/parity/pintz_maynard.py, code/parity/pintz_maynard_check2.py).
  Fresh-context adversarial audit: notes/audit-parity-v011.md.
- **Not checked:** whether this is already in the literature. Three web searches found no improvement of Pintz's 16, but
  someone (Pintz himself, or a survey) has very likely noted it after 2013. No MathSciNet / citation search.
- **Needs outside expert review:** only a literature question (is it known?). Most likely folklore.

## 2026-11-15 (Session 24) — (minor) Debouzy, "Twins almost prime under a Elliott-Halberstam's conjecture": the main constant appears to be off by a factor 2 (qualitative result unaffected)
- **What.** N. Debouzy, arXiv:1907.06393v1 (2019; no journal version found). Theorem 0.2 and Corollaries 0.3, 2.7 state, under an EH-type
  conjecture, that the twin-prime sum plus a localised semiprime sum equals 2 S_2 X (1+o(1)), with S_2 = prod_{p>=3} p(p-2)/(p-1)^2 = 0.66.
  The constant should apparently be 4 S_2. (a) For nu1 = nu2 = 1 her Cor. 2.7 gives sum Lambda(n+2) Lambda_2(n) ~ 2 S_2 X log X,
  but Bombieri's theorem (as quoted by Ford, arXiv:math/0401215v1, (1.3), H = 2 S_2) gives 4 S_2 X log X. (b) Her eq. (65) takes the
  local-factor product over 3 <= p <= z, dropping the p = 2 factor (1 - 0)/(1 - 1/2) = 2. If her coprime-to-2 convention is meant
  to remove p = 2, the model sum of 1 over odd n has density 1/2, not the 1/d used, and the same factor is lost. (c) Her own text
  says sum Lambda(n)Lambda(n+2) ~ S_2 X "as a consequence of Hardy-Littlewood", while the standard prediction, which she
  also uses (Pi(X) = 2 S_2 X / log^2 X), is 2 S_2 X.
- **Why it might matter.** Only as a correction of a constant in a preprint. Her conclusion (infinitely many twins almost prime
  under EH) does not change. It came up in this run's parity work (paper v0.9, Remark rem:debouzy).
- **Evidence label:** our reading of pp. 1-3, 36-37 (rendered pages checked), plus Heuristic numerics: code/parity/bombieri_twin_split.py
  gives (P+Q)/(2 * 2 S_2 (x log x - x)) = 0.968, 0.974, 0.975 at x = 1e6, 1e7, 3e7. This tends to 1 under the corrected constant and
  would tend to 1/2 under the printed one. A fresh-context adversarial audit tried to find a normalisation that makes the printed
  constant right and could not (verdict: CONFIRMED). The same audit found a bug in our script, now fixed; the fix moves the numbers
  further from the printed constant.
- **Not checked:** the rest of her proof; whether a later version exists outside arXiv; Bombieri's original papers (not opened).
- **Needs outside expert review:** no. It is a pointer to a likely slip in a constant, not a claim against the method.

## 2026-11-15 (Session 21) — (minor) Polymath8b, Proposition 6.5: one step of the printed proof is not justified (no result changes)
- **What.** In D. H. J. Polymath, *Variants of the Selberg sieve...* (arXiv:1407.4897v4, Prop. 6.5, p. 44), the bound
  M_{k,eps} <= k/(k-1) log(2k-1) is proved by Cauchy-Schwarz on fibres with the weight w_i = 1 - t_1 - ... - t_k + k t_i, followed by
  "integrating and summing". That last step needs w_i >= 0 also off the fibres used. This fails when t_1 + ... + t_k > 1: for
  example t_i = 0 and sum = 1 + eps give w_i = -eps. The same issue affects Remark 6.6 for a > 1/(1+eps). At eps = 0 the proof is fine.
- **Why it might matter.** Hardly at all. Nothing in Polymath8b depends on it; the authors use it only to say that the gains from
  enlarging the support are modest. A corrected argument gives (k/(k-1) + eps) log(2k-1). For small eps the scaling bound
  (1+eps) k/(k-1) log k (the endpoint a = 1/(1+eps) of their own Remark 6.6) is stronger anyway. At k = 2 the printed constant
  does hold, by this run's Theorem thm:k2.
- **Evidence label:** Proved here (our reading of the printed proof; parity paper v0.6, Remark rem:pm65). Found while working on
  this run's parity attempt; confirmed by a fresh-context adversarial auditor (notes/audit-parity-v06.md item 23: "the gap is
  real ... the corrected bound is right"; at k = 2 the point (0, 1+eps) breaks the needed inequality pointwise).
- **Not checked:** the journal version (Res. Math. Sci. 2014); whether the printed constant is true for all eps < 1 and k >= 3.
- **Needs outside expert review:** no. It is a pointer to a proof slip in a remark-level proposition.

## 2026-11-15 (bonus run) — (minor) Sawin–Shusterman, Theorem 4.5: two different saving exponents in one proof (most likely a harmless slip)
- **What.** In W. Sawin, M. Shusterman, *On the Chowla and twin primes conjectures over F_q[T]* (arXiv:1808.04001v2), the
  saving of Theorem 4.5 is stated as << |M_d|^{1 - beta/p} ((4.8), (4.35)). The proof on p. 22 says "we obtain a savings in each
  term of q^{(d-t')beta/2p} ... To obtain our desired savings of q^{d beta/2p}". So the exponent is beta/p in one place and
  beta/(2p) in the other.
- **Why it might matter.** Hardly at all. Every later use only needs some power saving proportional to 1/p. It came up while reading
  the paper for the parity paper (v0.5, Section sec:ss).
- **Evidence label:** Literature (read in arXiv v2, SHA-256 5b762a08...0e687). It was spotted by the helper and confirmed in the
  extracted text by an independent auditor (notes/audit-parity-v05.md).
- **Not checked:** the Annals of Math. (2022) version, which may already be corrected; whether either constant is the one the proof
  actually gives.
- **Needs outside expert review:** no. It is a pointer only, and most likely a typo.

## 2026-11-15 — Polymath8b Remark 8.1: the printed parity weight is identically zero (typo-level; no result changes)
- **What.** In D. H. J. Polymath, *Variants of the Selberg sieve, and bounded intervals containing many primes*
  (arXiv:1407.4897v4, Remark 8.1, p. 70), the weight meant to block H_1 <= 4 in every window is printed as a product of
  (1 - lambda(n+i)lambda(n+i')) over 0 <= i <= i' <= H with (n+i,3) = (n+i',3) = 1 and i' - i <= 4.
  - As written it vanishes identically: the factor with i = i' is 1 - lambda^2 = 0.
  - Even with i < i' it vanishes for every n once H >= 4, because the positions prime to 3 include even integers and contain
    a triangle of pairwise distances <= 4 (e.g. n+1, n+2, n+4 when 3 | n).
  - The intended weight (i < i', odd positions only, i.e. positions = +-1 mod 6, which form a path) works.
- **Why it might matter.** Only as a correction to a widely read remark (the authors "leave the details to the interested
  reader"). It came out of this run's parity attempt, which gives an exact criterion for when such weights exist
  (parity paper v0.2, Prop. prop:bipartite: the target graph must be bipartite; the printed graph has odd cycles).
- **Evidence label:** Proved here (elementary) + Computed (code/parity/bipartite_obstruction.py: printed weight 0 for all
  n < 20000; i < i' variant 0 for all n < 20000 at H = 4, 6, 8, 12, non-zero at H = 3; corrected weight non-zero and vanishing
  whenever two primes > 3 at distance <= 4 lie in the window).
- **What has been checked:** the printed formula in the arXiv v4 text extraction (the formula as quoted above); the triangle
  argument for each n mod 3 (coordinator and an independent fresh-context audit, notes/audit-parity-v02.md).
- **What has not:** the journal version (Res. Math. Sci. 1 (2014)) was not opened, so the slip may have been fixed there; no
  erratum search beyond the arXiv listing (v4 is the latest).
- **Needs outside expert review:** not really (elementary); worth a one-line note to the authors only if the journal version
  has the same text.

- **Update (15 Nov, coordinator):** the journal version (Res. Math. Sci. 1 (2014), Art. 12, Open Access, CC-BY; Remark 45 there) prints the same weight, 0 <= i <= i' <= H, so the slip is in the published text as well. A one-line note to the authors is reasonable; it changes no result.

## 2026-11-14 — Polymath8a Lemma 6.25 (and Cor. 6.26) is false as stated; repairable, no result changes
- **What.** The gcd factor $(a_2-a_1,n,r_1,r_2)^{1/2}$ in the hyper-Kloosterman correlation bound of
  D. H. J. Polymath, *New equidistribution estimates of Zhang type* (ANT 8 (2014); arXiv:1402.0811v3)
  is wrong when $r_1\ne r_2$ share a factor.
  - The correct factor, which is what the paper's own proof gives, is $(a_1t_2^3-a_2t_1^3,n,g)^{1/2}$,
    where $g=(r_1,r_2)$ and $r_i=gt_i$.
  - Song–Yue's eq. (49) (236 preprint) copies the wrong factor.
- **Evidence label:** Proved here (elementary), plus Computed.
  - An explicit family ($s=1$, $n=0$, $r_1=5g$, $r_2=7g$) has
    $|\mathrm{LHS}|=\frac1{35}\prod_{p\mid g}(p-1-1/p-1/p^2)$ exactly, while the lemma predicts
    $\ll(35g)^{1/2+\varepsilon}$.
  - The proof and the script are in `code/audit_sy236/pm8a_lemma625/`. The ratio grows from 0.014 to
    $8.3\times10^6$ over the first 13 primes $\ge 11$.
- **What has been checked:**
  - the exact statement, read in the v3 LaTeX source (the published text is identical);
  - the CRT factorisation, by brute force;
  - the identity $S(p)=p-1-1/p-1/p^2$, proved via Gauss sums and checked numerically for all primes $3\le p<60$;
  - the direct sum, for two values of $g$;
  - two earlier independent AI checks (audits D and F, `notes/audit-sy236-thm418/`).
- **What has not been checked:**
  - whether the error is already known: one extended web search found no erratum, and Polymath8a has
    no arXiv version after v3;
  - the downstream summation in Polymath8a §7 (Lemma 7.4) was checked by audit F, not re-derived by the
    coordinator.
- **Why it matters:** this is a genuine mis-statement in a widely cited paper. It changes no results,
  since the corrected factor gives the same final bounds. It is worth telling the Polymath authors and
  Song–Yue.
- **Needs outside expert review:** recommended before anything is sent or published, though the
  counterexample is elementary.

## 2026-11-13 — Charton et al. 212 draft: Table 3 caps vs Lemma 9.1 caps are inconsistent
- **What.** With the Table 3 caps, the variational criterion holds: $4.0027>4$ (two programs). With the
  different caps stated in Lemma 9.1, no polynomial in their own 846-dimensional space reaches $3.99$.
- **Evidence label:** Computed (ball arithmetic). The ceiling uses one program's Gram weights, checked
  at a random point.
- **Update (16 Nov 2026, Session 26):** since Session 24 the second exact program (capped_exact.py) also evaluates
  the random point and agrees exactly. The Gram certificate itself is still one program's; the random-point agreement is a
  probabilistic (Schwartz-Zippel) check of its weights, not a second derivation of the ceiling.
- **Status:** reported in the verification note as a located inconsistency for the authors to resolve,
  not as an error in their result.
