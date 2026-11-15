# Flags for Jerry (newest first; entries are updated, never deleted)

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
- **Status:** reported in the verification note as a located inconsistency for the authors to resolve,
  not as an error in their result.
