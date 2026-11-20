# Flags for Jerry (newest first; entries are updated, never deleted)

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
