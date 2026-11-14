# Polymath8a Lemma 6.25 as stated is false: a proof by explicit family

**Date:** 14 Nov 2026, coordinator session, at Jerry Kim's request ("check if the Polymath is truly an error").

**Source:** D. H. J. Polymath, *New equidistribution estimates of Zhang type*, arXiv:1402.0811v3
(LaTeX source, Lemma `lm-c-kl`, "Correlation of hyper-Kloosterman sums"; Lemma 6.25 in the
numbering). The statement text is identical in the published version, Algebra & Number Theory 8
(2014) 2067–2199. Corollary 6.26 has the same gcd factor.

## Statement as printed

Let $s, r_1, r_2$ be squarefree with $(s, r_1) = (s, r_2) = 1$, let $a_i \in (\mathbb Z/r_is)^\times$, and let
$n \in \mathbb Z/[r_1,r_2]s$. With $\mathrm{Kl}_3(x;q) = q^{-1}\sum_{x_1x_2x_3=x} e_q(x_1+x_2+x_3)$ (eq. `kl-def`),
the lemma states
$$\Bigl|\sum_{h\in(\mathbb Z/s[r_1,r_2])^\times}\mathrm{Kl}_3(a_1h;r_1s)\overline{\mathrm{Kl}_3(a_2h;r_2s)}e_{[r_1,r_2]s}(nh)\Bigr|
\ll_\varepsilon (s[r_1,r_2])^{\varepsilon}s^{1/2}[r_1,r_2]^{1/2}(a_2-a_1,n,r_1,r_2)^{1/2}(a_2r_1^3-a_1r_2^3,n,s)^{1/2}.$$

## Counterexample family (Proved here; elementary)

- **Parameters.** Take $s=1$, $n=0$, $t_1=5$, $t_2=7$. Let $g$ be a product of distinct primes
  $p\ge11$ with $p\ne109$, and set $r_1=gt_1$, $r_2=gt_2$, $a_2=1$. Choose $a_1$ (by CRT) with
  $a_1t_2^3\equiv a_2t_1^3 \pmod g$ and $a_1\equiv1 \pmod 5$.
- **The printed gcd factor is 1.** Since $t_1^3-t_2^3=-218=-2\cdot109$ is a unit mod $g$, we have
  $a_1\not\equiv a_2 \pmod p$ for every $p\mid g$, so $(a_2-a_1,0,r_1,r_2)=(a_2-a_1,g)=1$. The lemma
  therefore predicts $|\mathrm{LHS}|\ll_\varepsilon(35g)^{1/2+\varepsilon}$.
- **The sum factors over primes.** By CRT, $\mathrm{Kl}_3(x;q)=\prod_{p\mid q}\mathrm{Kl}_3(\overline{(q/p)}^{\,3}x;p)$
  (the paper's own formula after `kl-def`), and $h$ runs over $\prod_p\mathbb F_p^\times$. The local factors
  are:
  - **At $p\in\{5,7\}$:** only one Kloosterman sum has a $p$-component, so the factor is
    $\sum_{x\in\mathbb F_p^\times}\mathrm{Kl}_3(x;p)=p^{-1}\bigl(\sum_{y\ne0}e_p(y)\bigr)^3=-1/p$.
  - **At $p\mid g$:** the two arguments are $a_i\,\overline{(g/p)}^{\,3}\,\overline{t_i}^{\,3}h$, which coincide
    because $a_1t_2^3\equiv a_2t_1^3$. The factor is therefore
    $S(p)=\sum_{x\in\mathbb F_p^\times}|\mathrm{Kl}_3(x;p)|^2$.
- **Evaluating $S(p)$.** Expanding in multiplicative characters gives
  $\sum_{x\ne0}|K(x)|^2=\frac1{p-1}\sum_\chi|G(\chi)|^6$ for the unnormalised $K=p\,\mathrm{Kl}_3$, where
  $|G(\chi)|^2=p$ for $\chi\ne\chi_0$ and $|G(\chi_0)|=1$. This equals
  $\frac{(p-2)p^3+1}{p-1}=p^3-p^2-p-1$. Hence $S(p)=p-1-1/p-1/p^2\ge p-2$.
- **Conclusion.**
  $$|\mathrm{LHS}|=\tfrac1{35}\prod_{p\mid g}S(p)\ \ge\ \tfrac1{35}\prod_{p\mid g}(p-2),$$
  so for every fixed $\varepsilon<1/2$,
  $$\frac{|\mathrm{LHS}|}{(35g)^{1/2+\varepsilon}}\ \ge\ c\prod_{p\mid g}p^{1/2-\varepsilon}\Bigl(1-\frac2p\Bigr)\ \longrightarrow\ \infty$$
  as $g$ runs over products of more and more primes. **The lemma as stated is false.**

## The repair

The proof of the lemma reduces to the local estimate (`eq-ckl-goal`) with arguments
$b_i = a_i\bar s^3(r_i/p)^{-3}$, not $a_i$. Writing $r_i=gt_i$ with $g=(r_1,r_2)$, what the proof actually gives
is the gcd factor $(a_1t_2^3-a_2t_1^3,\,n,\,g)^{1/2}$ in place of $(a_2-a_1,n,r_1,r_2)^{1/2}$. On the family
above this factor is $g^{1/2}$, and the bound becomes $\ll (35)^{1/2}g$, consistent with
$|\mathrm{LHS}|\asymp g$. The $s$-factor $(a_2r_1^3-a_1r_2^3,n,s)$ is correct as printed. The printed
$g$-factor is correct when $r_1=r_2$.

## Consequences

- **Downstream use** (our audit `F-report.md`, auditor's derivation; not re-derived here). Where the
  lemma is used (Polymath8a Lemma 7.4 / Thm 2.8(v); Song–Yue eq. (49)), the factor is summed over the
  $m$-variables. The corrected factor still satisfies
  $\sum_{m_1,m_2\asymp M}(g,m_1t_1^3-m_2t_2^3)^{1/2}\ll\tau(g)M(M+g^{1/2})$, the same bound as before.
  The coordinator checked this summation step for the Song–Yue use.
- **Effect on results:** none of the exponents or results of Polymath8a or Song–Yue change.
- **This is a mis-stated lemma, not a gap in either paper.**
- **Erratum search:** an extended web search on 14 Nov 2026 found no erratum. That does not show that
  none exists.

## Reproduce

`python3 code/audit_sy236/pm8a_lemma625/counterexample.py` (under a second) does the following:
- checks the CRT factorisation of $\mathrm{Kl}_3$ by brute force;
- checks $S(p)=p-1-1/p-1/p^2$ for all primes $3\le p<60$;
- checks the factorisation of the sum by direct summation over $h$ for the two smallest $g$;
- prints $|\mathrm{LHS}|/(35g)^{1/2}$ growing from $0.014$ to $8.3\times10^6$ as $g$ runs through
  $11, 11\cdot13, \dots, 11\cdots59$.
