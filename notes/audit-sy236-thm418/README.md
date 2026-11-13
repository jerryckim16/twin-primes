# Audit of Song–Yue's analytic theorem (Theorem 4.18) behind the claimed $H_1\le236$

**Date:** 14 November 2026 (UTC), coordinator session, at Jerry Kim's request ("try to prove Song–Yue's analytic theorem").
**Source audited:** Z. Song, S. Yue, *Bounded gaps between primes: an upper bound of 236*, IACR ePrint 2026/1893, version of 2 September 2026 (PDF supplied by Jerry; not committed). Theorem 4.18 is the "D182 prime distribution" estimate: for the squarefree D182 moduli up to level $253/500$, the sum of discrepancies of primes is $O(X(\log X)^{-C})$. It is proved in §§4.1–4.7 (pp. 14–38). The link to the sieve is in §§4.13–4.14.

## What was done, and what it can and cannot mean

We did **not** prove Theorem 4.18 from scratch. It rests on deep published inputs:
- bilinear Bombieri–Vinogradov;
- Deligne's bounds for hyper-Kloosterman sums;
- the Polymath8a toolkit.

What we did is an independent, adversarial **check of the proof**, in two parts:
- **Audits A–E:** five auditors, one per part of the proof. Each re-derived the steps, verified every exponent inequality in exact rational arithmetic, stress-tested the combinatorial lemmas, and checked each cited result's hypotheses against how it is used.
- **Literature check F:** compared every cited Polymath8a statement word for word with arXiv:1402.0811v3 and the published version (Algebra & Number Theory 8 (2014) 2067–2199).

Labels:
- Our overall conclusion is **Literature, audited**. It is not "Proved here".
- The deep inputs remain **Literature**.
- Each section was read by **one** AI auditor. This is not peer review.

## Verdict

Theorem 4.18 appears **correct as a deduction from the cited literature, after one local repair** (eq. (49), below). The repair does not change any exponent or margin. No other demonstrated error was found.

| Part | Auditor | Result |
|---|---|---|
| §4.1 parameters; §4.5 Heath–Brown classification, Lemma 4.8, Lemma 4.9 (three-way grouping), routing | A | No defect. Every case of Lemma 4.9 is covered with strictly positive reserves (59,998 exact test vectors; MILP counterexample search found nothing; at s = 1/10 the lemma fails, and the paper uses s = 1001/10000). 72 exact numeric checks pass. |
| §4.2 IIa (Prop 4.2, Lemma 4.3) | B | No defect. The tightest margin, (33), turns negative only for γ > 0.439894, against the range end 0.44. |
| §4.3 IIb (Prop 4.4, Lemma 4.5) | C | No defect. The reused §4.2 steps carry over. |
| §4.4 Type III (Prop 4.6, Lemma 4.7) | D | **Eq. (49), p. 27, is false as printed; repairable.** Everything else is verified. |
| §§4.6–4.7, Theorem 4.18, link to §§4.13–4.14 | E | No defect. 37 exact checks pass. The sieve uses exactly what Theorem 4.18 provides. |
| Polymath8a citations | F | All hypotheses met (Thm 2.9, Cor 4.16 second bound, Prop 5.10, Lemmas 1.3, 3.1, 3.3, 3.4(iii), 5.2, Cor 5.3, §7.2). The exception is Lemma 6.25 / Cor 6.26: see below. |

**Swapped-factor issue.** Song–Yue's Remark 4.23 points to a step in [Sta26, Lemma 5] that applies a Type II estimate with the factors swapped, without the Siegel–Walfisz hypothesis for the swapped factor. **Nothing of that kind** occurs in Song–Yue's own proof (auditors A, B, C). The Siegel–Walfisz factor is always in the slot that needs it.

## The one defect: eq. (49), and its source in Polymath8a

**What (49) says.** For $g=\gcd(r_1,r_2)$ and $D=m_1r_1^3-m_2r_2^3$, (49) bounds the correlation of two $\mathrm{Kl}_3$ sums. Its correction factor is $\gcd(g,m_1-m_2)^{1/2}\gcd(D,s)^{1/2}$.

**Why it is wrong.** Write $r_i=gt_i$, so $(t_i,g)=1$. At a prime $p\mid g$, the CRT factorisation gives local arguments proportional to $m_i^{-1}t_i^{-3}$. The local correlation is of size about $p$ (instead of $O(1)$) exactly when
$$m_1t_1^3\equiv m_2t_2^3 \pmod p,$$
not when $m_1\equiv m_2$. As printed, (49) can be off by a factor of about $g^{1/2}$.

**Numerical confirmation.** `code/audit_sy236/kl3_coordinator_check.py` (p = 31, t₁ = 2, t₂ = 3), with normalised Kl₃ correlations:
- $m_1=m_2$ gives at most $1.03$;
- $m_1t_1^3\equiv m_2t_2^3$ gives at least $29.97$.

Auditors D and F confirmed the same independently, at p = 7, 13, 31, 61 and composite g = 35.

**The source.** Song–Yue transcribed the bound correctly from Polymath8a, Lemma 6.25 / Corollary 6.26 (v3 pp. 79–80). That lemma states the factor $(a_2-a_1,n,r_1,r_2)^{1/2}$. Its proof splits prime by prime, with local arguments $b_i=a_i\bar s^3(r_i/p)^{-3}$, so what the proof actually gives is $(a_1t_2^3-a_2t_1^3,\,n,\,g)^{1/2}$. The stated factor is right only when $r_1=r_2$; the $s$-factor is right.

We checked the coordinator's reading against the LaTeX source of v3. The published version has the same statement text. One web search found no erratum, which does not show that none exists. The issue may well be known.

**Repair and consequence.** Replace $\gcd(g,m_1-m_2)$ by $\gcd(g,m_1t_1^3-m_2t_2^3)$. Since $t_1$ is invertible mod $g$,
$$\sum_{m_1,m_2\asymp M}\gcd(g,m_1t_1^3-m_2t_2^3)^{1/2}\le\sum_{m_2}\sum_{e\mid g}e^{1/2}(M/e+1)\ll\tau(g)\,M(M+g^{1/2}),$$
which is the $X^{o(1)}(M^2+Mg^{1/2})$ that Song–Yue use next. Also, $D=g^3(m_1t_1^3-m_2t_2^3)$, so the diagonal/off-diagonal split is unchanged. So are (50)–(52) and the three exponent margins $1-1/3000$, $1-137/3000$ and $1-71/2400$.

The same repair applies to Polymath8a's own Lemma 7.4 and Theorem 2.8(v), whose conclusions are likewise unaffected (auditor F). This is a **local error in a displayed bound, not a gap in either result.**

## Exposition gaps (not errors)

Each of these is a step left implicit or sketched, which an expert could fill:
- Lemma 4.9's proof skips the case with no pivotal indices.
- Corollary 4.16 is applied "on each class mod $q_0$" without the change of variables. Its coprimality indicators are removed by a Möbius step at cost $X^{o(1)}$.
- The Poisson/Taylor separation in §4.4 is sketched.
- Lemma 4.13 (58) is sketched.
- $\|W^{(r)}\|_1\ll h^{-r}$ is stated without proof (trivially true).
- In Lemma 4.30, the assignment of small factors to $e$ versus $e'$ is implicit.
- Lemma 4.28 is redundant.
- "m, m' ≤ 54" in the definition of Q182 is vacuous.
- The constants are ineffective (through Siegel–Walfisz), which is irrelevant to $H_1\le236$.

## What remains for the 236 bound to count as established

1. Expert human review of Song–Yue §4 (this audit is not that), in particular the Type III re-derivation.
2. The deep inputs, which stay Literature: Deligne–Katz, bilinear Bombieri–Vinogradov, Siegel–Walfisz.
3. The rest of the paper outside §§4.1–4.7 and 4.13–4.14, which this audit did not cover:
   - §4.12 (the reduction to the variational criterion);
   - the Selberg main term ([D14b, Lemma 4.1]);
   - Lemma 4.32.
4. The variational step (Prop. 4.21), which this project has independently reproduced by two exact programs (see `papers/verification-note`).

## Suggested action

Tell Song and Yue about (49) and its source, and the authors of Polymath8a (D. H. J. Polymath; Terence Tao's blog hosted the project) about Lemma 6.25. Both are courtesy notes about a repairable mis-statement. That decision is Jerry's.

## Files

- `A-report.md` … `E-report.md`: the five section audits. A and E were delivered as messages and saved by the coordinator.
- `F-report.md`: the Polymath8a literature check, with short quotations and locators.
- `code/audit_sy236/<A–F>/`: the auditors' exact-arithmetic and simulation scripts with their outputs.
- `code/audit_sy236/kl3_coordinator_check.py`: the coordinator's independent Kl₃ check.

Rendered pages of the Song–Yue PDF and the downloaded Polymath8a files were used locally and are **not** committed.
