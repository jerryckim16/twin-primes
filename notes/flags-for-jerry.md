# Flags for Jerry (newest first; entries are updated, never deleted)

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
- **Status:** reported in the verification note as a located inconsistency for the authors to resolve,
  not as an error in their result.
