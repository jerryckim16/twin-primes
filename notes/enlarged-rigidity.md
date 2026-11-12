# Pigeonhole rigidity on the $\varepsilon$-enlarged simplex

Status: **Proved here** (Theorem E and Lemmas E1–E3), **Computed** (Table E), with the scope limits listed in the last section (**Open**).
Nothing here is a new bound on $H_1$, and nothing here bears on the twin prime conjecture.

Script: `code/enlarged_pigeonhole.py`. Raw output: `out/enlarged_pigeonhole_d5_d10.txt`.

## Setting (Polymath8b, Theorem 3.12)

Write $\mathcal R_k=\{t\in[0,\infty)^k:\ t_1+\dots+t_k\le 1\}$ and $|t|=t_1+\dots+t_k$.
For $0\le\varepsilon<1$ and square-integrable $F$ supported on $(1+\varepsilon)\mathcal R_k$, Polymath8b
(arXiv:1407.4897, Theorem 3.12) uses
$$
I_k(F)=\int_{(1+\varepsilon)\mathcal R_k}F^2,\qquad
J^{(m)}_{k,\varepsilon}(F)=\int_{(1-\varepsilon)\mathcal R_{k-1}}\left(\int_0^\infty F\,dt_m\right)^2 dt_1\cdots \widehat{dt_m}\cdots dt_k ,
$$
and $M_{k,\varepsilon}=\sup_F\sum_{m=1}^k J^{(m)}_{k,\varepsilon}(F)/I_k(F)$.
(For a point of $(1-\varepsilon)\mathcal R_{k-1}$ the inner integral runs over $0\le t_m\le 1+\varepsilon-\sum_{i\ne m}t_i$.)
Theorem 3.12 there: if $M_{k,\varepsilon}>2m/\vartheta$ and either (i) $\mathrm{EH}[\vartheta]$ holds and $1+\varepsilon<1/\vartheta$, or (ii) $\mathrm{GEH}[\vartheta]$ holds and $\varepsilon<1/(k-1)$, then $\mathrm{DHL}[k,m+1]$.

For weights $c\in[0,\infty)^k$ put
$$
M_{k,\varepsilon}[c]=\sup_{F\neq 0}\frac{\sum_{m}c_mJ^{(m)}_{k,\varepsilon}(F)}{I_k(F)} .
$$
The proof of Theorem 3.12 bounds $\sum_n\nu(n)$ from above and each $\sum_n\nu(n)\theta(n+h_m)$ from below separately, so by linearity (as in the plain case of Proposition 5) the weighted pigeonhole criterion reads: under (i) or (ii),
$$
\tfrac{\vartheta}{2}\,M_{k,\varepsilon}[c]>\alpha_D(c)\ \Longrightarrow\ H_1\le D .
$$
For $k=1$ we use the convention $(1-\varepsilon)\mathcal R_0=\{0\}$, so $J^{(1)}_{1,\varepsilon}(F)=(\int F)^2$ and, by Cauchy–Schwarz, $M_{1,\varepsilon}=1+\varepsilon$.

## Statement

**Theorem E (enlarged pigeonhole rigidity; Proved here).**
Let $0\le\varepsilon<1$, let $h_1<\dots<h_k$, $D\ge0$, and let $\omega$ be the largest number of $h_i$ in an interval of length $D$. Then for every $c\ge0$, $c\ne0$,
$$
\frac{M_{k,\varepsilon}[c]}{\alpha_D(c)}\ \le\ M_{\omega,\varepsilon},
$$
with equality for $c=\mathbf 1_K$, $K$ a largest clique. In particular, for every $K\subseteq\{1,\dots,k\}$ with $|K|=j\ge1$,
$$
M_{k,\varepsilon}[\mathbf 1_K]=M_{j,\varepsilon}. \tag{E.1}
$$

**Corollary E′.** If $(\vartheta,\varepsilon)$ satisfies (i) or (ii) of Theorem 3.12 for $k$ and $\tfrac{\vartheta}{2}M_{k,\varepsilon}[c]>\alpha_D(c)$, then $M_{\omega,\varepsilon}>2/\vartheta$ and $(\vartheta,\varepsilon)$ satisfies (i) or (ii) for $\omega$ (condition (i) does not involve $k$, and $1/(k-1)\le 1/(\omega-1)$). Hence Theorem 3.12 gives $\mathrm{DHL}[\omega,2]$ with the same $\varepsilon$, and applying it to the clique sub-tuple (admissible, diameter $\le D$) gives $H_1\le D$. So on the $\varepsilon$-enlarged simplex the weighted criterion never certifies more than the standard criterion applied to the best sub-tuple of diameter at most $D$. (If $\omega=1$ the hypothesis is impossible: $\tfrac\vartheta2(1+\varepsilon)<\tfrac12$ under (i), and $\vartheta\le 1$, $\varepsilon<1$ under (ii).)

The key new input is the slicing lemma E1, where the enlargement produces a *different* effective parameter on each slice, and Lemma E2, which shows that this does not help.

## The slice is an enlarged problem with parameter $\varepsilon/\sigma$

Fix $K$ with $|K|=j$, write $t=(s,u)$ with $s\in[0,\infty)^K$ and $u$ the remaining $r=k-j$ coordinates, and set $F_u=F(\cdot,u)$.
The support condition gives $|s|\le 1+\varepsilon-|u|$. For $m\in K$, the outer region of $J^{(m)}_{k,\varepsilon}$ is $|s_{-m}|+|u|\le 1-\varepsilon$, where $s_{-m}$ is $s$ without $s_m$. By Fubini,
$$
J^{(m)}_{k,\varepsilon}(F)=\int_{|u|\le 1-\varepsilon}\ \int_{|s_{-m}|\le 1-\varepsilon-|u|}\left(\int_0^\infty F_u\,ds_m\right)^2 ds_{-m}\,du,\qquad
I_k(F)=\int I_j(F_u)\,du. \tag{E.2}
$$
So, for fixed $u$ with $|u|\le1-\varepsilon$, the slice carries a $j$-dimensional problem with support $B\,\mathcal R_j$ and $J$-region $A\,\mathcal R_{j-1}$, where $B=1+\varepsilon-|u|$ and $A=1-\varepsilon-|u|$.
Rescaling by $\sigma(u)=(A+B)/2=1-|u|$ turns this into exactly the enlarged problem with
$$
\varepsilon'(u)=\frac{B-A}{A+B}=\frac{\varepsilon}{1-|u|}=\frac{\varepsilon}{\sigma(u)}\in[\varepsilon,1],
$$
and the usual scaling ($I_j$ scales by $\sigma^j$, each $J$ by $\sigma^{j+1}$) gives
$$
\sum_{m\in K}J^{(m)}_{\text{slice}}(F_u)\le \sigma(u)\,M_{j,\varepsilon/\sigma(u)}\,I_j(F_u). \tag{E.3}
$$
This is the expected "different $\varepsilon'$" phenomenon. The naive consequence $M_{k,\varepsilon}[\mathbf 1_K]\le\sup_{\varepsilon\le\eta\le1}M_{j,\eta}$ would leave a gap, since $M_{j,\eta}$ increases with $\eta$ on the range we computed (Table E). The factor $\sigma(u)$ closes the gap, by the following lemma.

**Lemma E2 (Proved here).** For $j\ge1$ and $0\le\eta_1\le\eta_2<1$,
$$
\frac{M_{j,\eta_2}}{1+\eta_2}\le\frac{M_{j,\eta_1}}{1+\eta_1}.
$$
The same holds for $M_{j,\eta}[c]$, for any $c\ge0$.

*Proof.* Let $H\neq0$ be supported on $(1+\eta_2)\mathcal R_j$ and put $\lambda=(1+\eta_1)/(1+\eta_2)\in(0,1]$, $G(s)=H(s/\lambda)$. Then $G$ is supported on $(1+\eta_1)\mathcal R_j$ and $I_j(G)=\lambda^jI_j(H)$. Write $h_m(x')=\int_0^\infty H\,dx_m$. Then $\int_0^\infty G\,ds_m=\lambda h_m(s_{-m}/\lambda)$, so
$$
J^{(m)}_{j,\eta_1}(G)=\lambda^{j+1}\int_{|x'|\le(1-\eta_1)/\lambda}h_m(x')^2\,dx'\ \ge\ \lambda^{j+1}J^{(m)}_{j,\eta_2}(H),
$$
because $(1-\eta_1)/\lambda=(1-\eta_1)(1+\eta_2)/(1+\eta_1)\ge 1-\eta_2$. This is equivalent to $(1-\eta_1)(1+\eta_2)\ge(1-\eta_2)(1+\eta_1)$, that is to $2\eta_2\ge2\eta_1$, and the integrand is nonnegative. For $j=1$ both $J$-regions are the point $\{0\}$ and the same identity holds with equality. Summing over $m$ with weights $c_m\ge0$: $M_{j,\eta_1}[c]\ge\lambda\,\sum_mc_mJ^{(m)}_{j,\eta_2}(H)/I_j(H)$. Take the supremum over $H$. $\square$

Applying Lemma E2 with $\eta_1=\varepsilon$ and $\eta_2=\varepsilon/\sigma$ in (E.3):
$$
\sigma\,M_{j,\varepsilon/\sigma}\le\sigma\,\frac{1+\varepsilon/\sigma}{1+\varepsilon}\,M_{j,\varepsilon}
=\frac{1+\varepsilon-|u|}{1+\varepsilon}\,M_{j,\varepsilon}\le M_{j,\varepsilon}.
$$
The same constant comes out of a one-step rescaling, which we use as the official proof.

## Proofs

**Lemma E1 (slicing on the enlarged simplex; Proved here).** Let $0\le\varepsilon<1$, $K\subseteq\{1,\dots,k\}$, $|K|=j\ge1$, and $F$ square-integrable on $(1+\varepsilon)\mathcal R_k$. With $\mu(u)=(1+\varepsilon-|u|)/(1+\varepsilon)\in[0,1]$,
$$
\sum_{m\in K}J^{(m)}_{k,\varepsilon}(F)\ \le\ M_{j,\varepsilon}\int_{|u|\le1-\varepsilon}\mu(u)\,I_j(F_u)\,du\ \le\ M_{j,\varepsilon}\,I_k(F).
$$

*Proof.* $F\in L^2$ of a bounded set, so $F\in L^1$ and (E.2) holds by Fubini–Tonelli. Slices with $|u|>1-\varepsilon$ contribute nothing to the left side. Fix $u$ with $|u|\le1-\varepsilon$ and $F_u\ne0$. Put $B=1+\varepsilon-|u|>0$ (if $\varepsilon=0$ the set $|u|=1$ is null), $\mu=B/(1+\varepsilon)$ and $H(x)=F_u(\mu x)$, which is supported on $(1+\varepsilon)\mathcal R_j$. Then $I_j(F_u)=\mu^jI_j(H)$.

For $j\ge2$ and $m\in K$, with $h_m(x')=\int_0^\infty H\,dx_m$ we have $\int_0^\infty F_u\,ds_m=\mu\,h_m(s_{-m}/\mu)$, hence
$$
\int_{|s_{-m}|\le1-\varepsilon-|u|}\left(\int_0^\infty F_u\,ds_m\right)^2ds_{-m}
=\mu^{j+1}\int_{|x'|\le(1-\varepsilon-|u|)/\mu}h_m^2\,dx'\le\mu^{j+1}J^{(m)}_{j,\varepsilon}(H).
$$
The inequality uses $h_m^2\ge0$ and
$$
\frac{1-\varepsilon-|u|}{\mu}=\frac{(1-\varepsilon-|u|)(1+\varepsilon)}{1+\varepsilon-|u|}\le1-\varepsilon
\iff -|u|(1+\varepsilon)\le-|u|(1-\varepsilon),
$$
which is true. Summing over $m\in K$ gives at most $\mu^{j+1}M_{j,\varepsilon}I_j(H)=\mu\,M_{j,\varepsilon}\,I_j(F_u)$.

For $j=1$, $K=\{m\}$, the slice term is $(\int_0^BF_u)^2\le B\,I_1(F_u)=\mu\,M_{1,\varepsilon}\,I_1(F_u)$ by Cauchy–Schwarz.

Integrating over $u$ and using $\mu\le1$ together with (E.2) for $I_k$ proves the lemma. $\square$

**Lemma E3 (embedding; Proved here).** For $|K|=j\ge1$, $M_{k,\varepsilon}[\mathbf 1_K]\ge M_{j,\varepsilon}$. Consequently $M_{j,\varepsilon}\le M_{k,\varepsilon}[\mathbf 1_K]\le M_{k,\varepsilon}$, so $j\mapsto M_{j,\varepsilon}$ is non-decreasing.

*Proof.* Let $H\ne0$ be supported on $(1+\varepsilon)\mathcal R_j$, let $r=k-j\ge 1$, $0<\delta<(1-\varepsilon)/r$, $\mu_\delta=1-r\delta/(1+\varepsilon)$, and
$$
F_\delta(s,u)=H(s/\mu_\delta)\,\mathbf 1_{[0,\delta]^r}(u).
$$
It is supported on $(1+\varepsilon)\mathcal R_k$, because $|s|+|u|\le\mu_\delta(1+\varepsilon)+r\delta=1+\varepsilon$, and $I_k(F_\delta)=\delta^r\mu_\delta^jI_j(H)$.
For $m\in K$ and $j\ge2$, since $|u|\le r\delta$ on the support,
$$
J^{(m)}_{k,\varepsilon}(F_\delta)\ge\delta^r\mu_\delta^{j+1}\int_{|x'|\le\rho_\delta}h_m^2\,dx',\qquad\rho_\delta=\frac{1-\varepsilon-r\delta}{\mu_\delta}\to1-\varepsilon\quad(\delta\to0).
$$
Here $h_m\in L^2$ by Cauchy–Schwarz, so by dominated convergence the last integral tends to $J^{(m)}_{j,\varepsilon}(H)$ (the boundary $|x'|=1-\varepsilon$ is null). For $j=1$ we get $J^{(m)}_{k,\varepsilon}(F_\delta)=\delta^r\mu_\delta^2(\int H)^2$ directly. Dropping the nonnegative terms $m\notin K$ and letting $\delta\to0$ gives the ratio $\sum_{m\in K}J^{(m)}_{j,\varepsilon}(H)/I_j(H)$ in the limit. Finally $M_{k,\varepsilon}[\mathbf 1_K]\le M_{k,\varepsilon}$ because $\mathbf 1_K\le\mathbf 1$ and every $J\ge0$. $\square$

*Proof of Theorem E.* Lemmas E1 and E3 give (E.1). The rest is the argument of Proposition 5 unchanged, since it uses only two facts about the functional: $c\mapsto M_{k,\varepsilon}[c]$ is a supremum of linear functionals (hence convex and positively homogeneous), and (E.1).

In detail: normalise $\alpha_D(c)=1$. The interval graph $G$ on the shifts (edges $|h_i-h_l|\le D$) is perfect, so $\{c\ge0:\ c(S)\le1\ \text{for every stable } S\}=\operatorname{conv}\{\mathbf 1_K:\ K\text{ a clique}\}$. By convexity $M_{k,\varepsilon}[c]\le\max_KM_{k,\varepsilon}[\mathbf 1_K]=\max_KM_{|K|,\varepsilon}\le M_{\omega,\varepsilon}$, the last step by Lemma E3. Equality for a largest clique $K$ follows from $\alpha_D(\mathbf 1_K)=1$ and (E.1). $\square$

*Remark.* Lemma E1 is strict in a quantitative sense: the slice at height $|u|$ is penalised by $\mu(u)=1-|u|/(1+\varepsilon)$. So for $|K|<k$ the supremum in (E.1) is approached only by $F$ concentrating near $u=0$, and it is not attained. This is why the polynomial lower bounds for $c=(1,1,0)$ below converge slowly towards $M_{2,\varepsilon}$.

## Numerics (Computed)

Test space: span of $t^\alpha\mathbf 1[|t|\le\rho]$ with $|\alpha|\le d$ and $\rho\in\{1-\varepsilon,1,1+\varepsilon\}$ (no symmetry imposed). All Gram entries are exact rationals. The $I$-entries are Dirichlet integrals. For the $J$-entries, the inner integral of $t^\alpha\mathbf 1[|t|\le\rho]$ in $t_m$ is $x^{\alpha'}(\rho-|x|)_+^{a_m+1}/(a_m+1)$, and on a $q$-simplex
$$
\int_{\rho\mathcal R_q}x^\gamma g(|x|)\,dx=\frac{\gamma!}{(|\gamma|+q-1)!}\int_0^\rho s^{|\gamma|+q-1}g(s)\,ds,
$$
so each entry is a one-variable polynomial integral over $0\le s\le\min(1-\varepsilon,\rho_1,\rho_2)$. The top generalised eigenvalue, computed at 60 digits with mpmath, is a lower bound for the corresponding $M$.

Cross-checks:
- At $\varepsilon=0$ the code reproduces $M_2=1/(1-W(1/e))=1.3859332\ldots$ and the paper's $k=3$ values.
- $M_{1,\varepsilon}=1+\varepsilon$ is reproduced.
- The exact $J$-matrices agree with independent adaptive or Gauss–Legendre quadrature for random $F$ to $10$–$12$ digits ($k=2,3$; $\varepsilon=1/5,1/3$).

**Table E.** Lower bounds. Columns: $M_{2,\varepsilon}$ (degree 10, 198 basis functions; 66 at $\varepsilon=0$); $M_{3,\varepsilon}[c]$ (degree 5, 168 basis functions; 56 at $\varepsilon=0$).

| $\varepsilon$ | $M_{2,\varepsilon}\ge$ | $M_{3,\varepsilon}[(1,1,0)]\ge$ | $M_{3,\varepsilon}[(\frac12,1,\frac12)]\ge$ | $M_{3,\varepsilon}[(1,1,1)]\ge$ |
|---|---|---|---|---|
| $0$ | $1.385933$ | $1.349844$ | $1.160121$ | $1.646427$ |
| $1/10$ | $1.518567$ | $1.482143$ | $1.264698$ | $1.793492$ |
| $1/5$ | $1.627161$ | $1.585674$ | $1.341926$ | $1.882282$ |
| $1/3$ | $1.717104$ | $1.663743$ | $1.413309$ | $1.917001$ |

Readings:
1. Every weighted value lies below the corresponding $M_{2,\varepsilon}$ lower bound, as Theorem E requires ($\alpha_1=1$ for both weight vectors on the shifts $(0,1,2)$ with $D=1$).
2. For $(1,1,0)$ the gap to $M_{2,\varepsilon}$ shrinks with the degree. At $\varepsilon=1/5$ it goes $1.5108$ (degree 2), $1.5719$ (4), $1.5857$ (5) against $1.6272$. This is consistent with the equality (E.1) and the non-attainment remark.
3. For $(\frac12,1,\frac12)=\frac12(1,1,0)+\frac12(0,1,1)$ the value stays far below $M_{2,\varepsilon}$ for every $\varepsilon$: the weights lose, they do not gain.
4. $M_{2,\eta}/(1+\eta)$ is $1.3859,\ 1.3805,\ 1.3560,\ 1.2878$ for $\eta=0,\frac1{10},\frac15,\frac13$. It is decreasing, consistent with Lemma E2, while $M_{2,\eta}$ itself increases. So the naive slice bound $\sup_{\eta\ge\varepsilon}M_{j,\eta}$ is genuinely weaker than (E.1). Rigorously: Lemma E2 and the exact value of $M_2$ give $M_{2,1/10}\le1.1\,M_2<1.5246$, while $M_{2,1/3}\ge1.7171$.

These are lower bounds only. They are consistency checks, not part of the proof. (All test values satisfy the GEH constraint $\varepsilon<1/(k-1)=1/2$ for $k=3$.)

## Verdict, and what is not ruled out

**Ruled out (Proved here):** On the $\varepsilon$-enlarged simplex of Polymath8b (Theorem 3.12, one common $\varepsilon$ for all $m$, $F$ on $(1+\varepsilon)\mathcal R_k$, $J$ on $(1-\varepsilon)\mathcal R_{k-1}$), unequal pigeonhole weights cannot certify any $D$ beyond the best sub-tuple. Precisely, $\sup_{c}M_{k,\varepsilon}[c]/\alpha_D(c)=M_{\omega,\varepsilon}$, and the sub-tuple may use the same $\varepsilon$ under either hypothesis (i) or (ii). The slice does see a larger effective parameter $\varepsilon/\sigma$, but the accompanying scale factor $\sigma$ more than pays for it (Lemma E2). There is no gap.

**Open (not covered by this note):**
- Polymath8b's further enlargements beyond Theorem 3.12, namely general polytopes $R$ subject to $R+R\subseteq\ldots$ conditions, as used for $k=3$ under GEH. A slice of a general polytope is not a scaled copy of it, so Lemma E1 does not apply as stated.
- Stadlmann's 2026 hybrid supports.
- Variants in which the truncation of $J^{(m)}$ depends on $m$.
- Criteria that are not linear in the prime indicators (outside Proposition 5 as well).
