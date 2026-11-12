# Source notes: enlarged supports in the Maynard–Tao sieve

Compiled 2026-11-12 by reading the sources (arXiv PDFs and the Axiom PDF via a text-extraction fetch).
Nothing here is a new result; every formula is attributed. The text extraction garbled some
formulas, so **UNSURE** marks anything I could not confirm character-for-character.
Notation: $R_k=\{t\in[0,\infty)^k:\ t_1+\dots+t_k\le 1\}$, and $\widehat{dt_i}$ means $dt_i$ is omitted.

---------------------------------------------------------------------------------------------
## 1. Polymath8b, "Variants of the Selberg sieve, and bounded intervals containing many primes"
arXiv:1407.4897 (Res. Math. Sci. 1 (2014), Art. 12)

### 1(a) $M_k$ and the basic criterion (Thm 3.8, eqs. (31)–(33))
For fixed, compactly supported, square-integrable $F:[0,\infty)^k\to\mathbb R$:
$$I(F)=\int_{[0,\infty)^k}F(t)^2\,dt,\qquad
J_i(F)=\int_{[0,\infty)^{k-1}}\Big(\int_0^\infty F\,dt_i\Big)^2 dt_1\cdots\widehat{dt_i}\cdots dt_k ,$$
$$M_k=\sup_F\ \frac{\sum_{i=1}^k J_i(F)}{I(F)},$$
where the sup runs over square-integrable $F\not\equiv0$ supported on $R_k$.

**Thm 3.8 (sieving on the standard simplex).** Let $k\ge2$, $m\ge1$ be fixed. Suppose $\mathrm{EH}[\vartheta]$ holds for some
fixed $0<\vartheta<1$ and $M_k>2m/\vartheta$. Then $\mathrm{DHL}[k,m+1]$ holds.
- $\mathrm{EH}[\vartheta]$ means: for $Q\lessapprox x^{\vartheta}$ and fixed $A$,
  $\sum_{q\le Q}\sup_{a}|\Delta(\Lambda 1_{[x,2x]};a\ (q))|\ll x\log^{-A}x$ (Claim 2.2, roughly).
- **Thm 2.3 (Bombieri–Vinogradov):** $\mathrm{EH}[\vartheta]$ holds for every fixed $0<\vartheta<1/2$.
- So the unconditional criterion with $m=1$ is $M_k>4$, i.e. $M_k>2/\vartheta$ with $\vartheta\uparrow 1/2$.
- Thm 3.10 is a truncated-simplex variant with the $\mathrm{MPZ}[\varpi,\delta]$ input. It uses $M_k^{[\alpha]}$, with support
  $\{t\in[0,\alpha]^k:\sum t_i\le1\}$ and threshold $m/(1/4+\varpi)$. **UNSURE** about the exact sub/superscripts.

### 1(b) The $\varepsilon$-enlarged simplex (Thm 3.12; proof in §5.3)
**Statement (near-verbatim).**
- Setup: let $k\ge2$ and $m\ge1$ be fixed integers, and let $0<\varepsilon<1$ be fixed.
- Functional: for fixed compactly supported square-integrable $F:[0,\infty)^k\to\mathbb R$, define
$$J_{i,1-\varepsilon}(F)=\int_{(1-\varepsilon)\cdot R_{k-1}}\Big(\int_0^\infty F(t_1,\dots,t_k)\,dt_i\Big)^2
 dt_1\cdots\widehat{dt_i}\cdots dt_k .$$
- Quantity:
$$M_{k,\varepsilon}=\sup_F\frac{\sum_{i=1}^kJ_{i,1-\varepsilon}(F)}{I(F)}.$$
  The sup runs over square-integrable $F\not\equiv0$ **supported on**
  $(1+\varepsilon)\cdot R_k=\{t\in[0,\infty)^k:\ t_1+\dots+t_k\le 1+\varepsilon\}$.
- Hypotheses: there is a fixed $0<\vartheta<1$ such that one of the following holds:
  - (i) $\mathrm{EH}[\vartheta]$ holds and $1+\varepsilon<1/\vartheta$;
  - (ii) $\mathrm{GEH}[\vartheta]$ holds and $\varepsilon<1/(k-1)$.
- Conclusion: if $M_{k,\varepsilon}>2m/\vartheta$, then $\mathrm{DHL}[k,m+1]$ holds.
- Remark right after the theorem: by continuity of $M_{k,\varepsilon}$ in $\varepsilon$, the strict inequalities in (i) and (ii)
  can be replaced by non-strict ones.

So the support of $F$ grows to $\sum t_i\le1+\varepsilon$. The marginals in $J$ are integrated only over the
**smaller** simplex $\sum_{j\ne i}t_j\le 1-\varepsilon$. Since $F$ is supported on $(1+\varepsilon)R_k$, the inner integral
$\int_0^\infty F\,dt_i$ runs effectively over $0\le t_i\le 1+\varepsilon-\sum_{j\ne i}t_j$.

**Admissible $\varepsilon$ in the Bombieri–Vinogradov case** (my deduction from (i) and Thm 2.3; the paper does not say this
explicitly):
- For any fixed $0<\varepsilon<1$, pick $\vartheta<1/2$ close enough to $1/2$ that $2/\vartheta<M_{k,\varepsilon}$.
- Then $1/\vartheta>2>1+\varepsilon$, so (i) holds automatically.
- Hence, **unconditionally, $M_{k,\varepsilon}>4$ for some $0<\varepsilon<1$ implies $\mathrm{DHL}[k,2]$.**
- The only constraint is $\varepsilon<1$, which is also built into the theorem's standing hypothesis.
- The restriction $\varepsilon<1/(k-1)$ applies **only** in the GEH case (ii).
- Under full EH ($\vartheta\to1$), (i) forces $\varepsilon\to0$, so the enlargement gives nothing there.

**Proof idea (§5.3, from my reading; verify details before citing):**
- Same tensor-product approximation as §5.1.
- Sieve weights have total support $\le(1+\varepsilon)\vartheta/2$ in the normalisation $\log d/\log x$.
- Main term $\sum\nu$:
  - Under (i), $(1+\varepsilon)\vartheta<1$ allows the trivial case Thm 3.6(i).
  - Under (ii), pigeonhole (Lemma 3.4) with $(1+\varepsilon)\vartheta<k\vartheta/(k-1)$ yields an index whose complementary
    supports have sum $<\vartheta$, and GEH (Thm 3.6(ii)) applies.
- Prime term $\sum\nu\,\theta(n+h_k)$:
  - Use $(a+b)^2\ge(a+2b)a$.
  - Keep only the tensor components with $\sum_{i<k}S(f_{i,j})<(1-\varepsilon)\vartheta/2$, where level-$\vartheta$
    equidistribution (BV/EH) applies.
  - Drop the rest as a lower bound.
- This is exactly why $J$ is restricted to $(1-\varepsilon)R_{k-1}$.

### 1(c) Numerical values (Thm 3.9, Thm 3.13, §7.1–7.2)
- **Thm 3.9(vii):** $M_{54}>4.00238$ (§7.1).
  - Under EH ($\vartheta\to1$, $m=2$) this gives $\mathrm{DHL}[54,3]$ (Thm 3.2(vii)).
  - With BV it gives the weaker unconditional $\mathrm{DHL}[54,2]$ (the paper remarks this).
- Table 3: the Krylov method gives $M_{54}\ge4.00223$, slightly worse than 4.00238.
- **Thm 3.13(i):** $M_{50,1/25}>4.0043$ with $\varepsilon=1/25$. Via Thm 3.12(i) plus BV this gives $\mathrm{DHL}[50,2]$
  (Thm 3.2(i)). With $H(50)=246$ this gives $H_1\le246$.
- §7.2 degree dependence: $d=25$ gives $M_{50,1/25}>4.00124$; $d=27$ gives $M_{50,1/25}>4.0043$.
- **Thm 3.13(xiii):** $M_{51,1/50}>4.00156$ (GEH case; $\varepsilon=1/50=1/(k-1)$, allowed by the non-strict
  remark; $d=22$). This gives $\mathrm{DHL}[51,3]$ under GEH, Thm 3.2(xiii).
  **UNSURE** about the label "(xiii)" for 3.13; it was garbled.
- **Thm 3.13(xii'):** $M_{4,0.168}>2.00558$. The test function is $F=(1-\alpha\sum t_i)\,1_{\sum t_i\le1+\varepsilon}$ with
  $\varepsilon=0.168$, $\alpha=0.784$ (§7.3). This gives $\mathrm{DHL}[4,2]$ under GEH. **UNSURE:** Thm 3.2(xii) is $\mathrm{DHL}[3,2]$ under GEH,
  which needs a separate non-convex/piecewise argument (§7.4, Thm 3.15, $\varepsilon=1/4$).
- Remark 7.4: $M_{3,\varepsilon}\ge1.91726$ ($\varepsilon=56/113$) and $M_{4,\varepsilon}\ge2.05411$ ($\varepsilon=5/21$), both with cubic
  polynomials. **UNSURE** of the exact wording.
- §7.2: $\varepsilon=1/m$ with $m$ having only small prime factors was chosen for run-time reasons.

### 1(d) Upper bound (Lemma 6.1, Cor 6.4; also Prop 6.5)
**Lemma 6.1.**
- Hypothesis: $G_i:R_k\to(0,\infty)$ are measurable with $\int_0^\infty G_i(t)\,dt_i\le1$ for all values of the other
  variables.
- Conclusion: $M_k\le\operatorname{ess\,sup}_{t\in R_k}\sum_{i=1}^k G_i(t)^{-1}$.
- Proof: Cauchy–Schwarz,
  $\big(\int F\,dt_i\big)^2\le\int G_i\,dt_i\cdot\int F^2/G_i\,dt_i$. Then sum over $i$ and integrate.

**Cor 6.4.** $M_k\le\frac{k}{k-1}\log k$ for all $k\ge2$.
- Proof: take $G_i(t)=\frac{k-1}{\log k}\cdot\frac{1}{1-t_1-\dots-t_k+k\,t_i}$.
- Direct calculation gives $\int_0^{1-\sum_{j\ne i}t_j}G_i\,dt_i\le1$.
- And $\sum_i 1/G_i=\frac{\log k}{k-1}\sum_i(1-\sum_j t_j+kt_i)=\frac{\log k}{k-1}\big(k-(k-1)\textstyle\sum_jt_j\big)$, which is
  $\le\frac{k}{k-1}\log k$ on $R_k$.
  - **UNSURE:** the extraction said "identically $=$". By my arithmetic it is $\le$, with equality only at $t=0$. The sup is
    what matters.
- Lower bound for comparison: Thm 3.9(xi) gives $M_k\ge\log k-C$.
- **Prop 6.5:** $M_{k,\varepsilon}\le\frac{k}{k-1}\log(2k-1)$, and Remark 6.6 gives a weighted variant. The paper calls the gain
  from $M_k$ to $M_{k,\varepsilon}$ "asymptotically modest". **UNSURE:** I read this only via a summary, not verbatim.

### 1(e) Polynomial basis (§7.1, Lemmas 7.1–7.2)
- **Signatures:** $\alpha$ is a non-increasing tuple of positive integers.
- **$P_\alpha$:** the *monomial* symmetric polynomial $\sum t^{a}$ over all exponent tuples $a$ whose non-increasing
  rearrangement is $\alpha$. For example $P_{(1)}=\sum t_i$ and $P_{(1,1)}=\sum_{i<j}t_it_j$.
- **Basis for $k=54$:** $(1-P_{(1)})^a P_\alpha$ with $a\ge0$, $\alpha$ having **only even entries**, and
  $a+|\alpha|\le d=23$.
  - Allowing odd entries gained only about 0.005, at much higher cost.
  - Basis dimension: **not stated** (UNSURE). One can count the pairs $(a,\alpha)$ with $\alpha$ even and
    $a+|\alpha|\le23$.
- **Lemma 7.2 (integration formula):**
  $\int_{R_k}(1-\sum t_i)^a\,t_1^{a_1}\cdots t_k^{a_k}\,dt=\frac{a!\,a_1!\cdots a_k!}{(k+a+a_1+\dots+a_k)!}$.
- **Method:** matrices $M_1$ (for $I$) and $M_2$ (for $\sum J_i$) are given by eqs. (126) and (127); (127) was garbled.
  - Entries are computed exactly using structure constants for $P_\alpha P_\beta$.
  - A generalized eigenvalue problem gives the approximate optimum.
  - Exact rational arithmetic then certifies that $C M_1-M_2$ is not positive semidefinite for some $C>4$.
  - Run time: under an hour.
- **$\varepsilon$-case (§7.2):**
  - Basis on $(1+\varepsilon)R_k$: $(1+\varepsilon-P_{(1)})^aP_\alpha$ with $\alpha$ having **no 1's**. The text says
    "even entries" were used again, which "greatly reduced execution time while only reducing M by a few thousandths".
  - Integrals for $J_{i,1-\varepsilon}$ over $(1-\varepsilon)R_{k-1}$ use the rewrite
    $(1+\varepsilon-P_{(1)})^a=(2\varepsilon+(1-\varepsilon-P_{(1)}))^a$, expanded binomially.
  - Lemma 7.2 then applies after rescaling.

---------------------------------------------------------------------------------------------
## 2. J. Stadlmann, "Bounded gaps between primes", arXiv:2608.31126 (v1, 31 Aug 2026)
**Main result:** Thm 1 gives $H_1\le240$, via an admissible 49-tuple of diameter 240.
- Effectively this is DHL[49,2]; the notation DHL is not used.
- Thm 1 is misprinted as "$H_m$".

### 2(a) Support region (Def. 1; §1.1)
Parameters:
- $-\varepsilon=A_0<A_1<\dots<A_n<\tfrac12-\varepsilon$;
- $\delta>0$;
- caps $B_{j,m}$ with $\delta<B_{j,m}\le B_{j,m+1}\le B_{j,m}+\delta$.

$$T_k(\delta,\underline A,\underline B,\varepsilon)=\bigcup_{j=1}^n\Big\{t\in[0,1]^k:\ \sum_{i=1}^kt_i\in[A_{j-1}+\varepsilon,A_j+\varepsilon),\
\sum_{i\in I}t_i\le B_{j,|I|}\text{ for }I=\{i:t_i>\delta\}\Big\}.$$

Coordinates are $t_i=\log_x d_i$, and the weights are $\lambda_F(n)=\sum_{d\mid n}\mu(d)F(\log_x d)$ (Def. 4).
So "$\sum t_i\le 1/4$" corresponds to Polymath's $R_k$ at level $\vartheta=1/2$.

Heuristic picture (§1.1): $S=S_{BV}\cup S_Z$, where
- $S_{BV}=\{\sum t_i\le\tfrac14\}$;
- $S_Z=\{\sum t_i\in[\tfrac14,\tfrac14+\omega],\ \sum_{i\in I}t_i\le b_{|I|}\}$.

The cap on the "large" coordinates (those $>x^\delta$) forces moduli from $(S\times S)\setminus(S_{BV}\times S_{BV})$ to have
a large $x^\delta$-smooth factor. "To increase the support further, we will also apply the epsilon-enlargement trick of
Polymath."

### 2(b) Functionals and criterion (Def. 5, Prop. 1, eq. (2.1))
**Functionals.**
$$I(F)=\int_{T_k}F^2\,dt,$$
$$J(F)=\sum_{m,m'=1}^n\ \int\!\!\cdots\!\!\int_{\substack{t_1+\dots+t_{k-1}\le\max\{A_m-\varepsilon,\,A_{m'}-\varepsilon\}\\
t_1+\dots+t_k\in[A_{m-1}+\varepsilon,A_m+\varepsilon]\\ t_1+\dots+t_{k-1}+t_k'\in[A_{m'-1}+\varepsilon,A_{m'}+\varepsilon]}}
F(t_1,\dots,t_{k-1},t_k)\,F(t_1,\dots,t_{k-1},t_k')\,dt_1\cdots dt_k\,dt_k'.$$
- $K(F)$ has the same double sum and band conditions, but with $t_1+\dots+t_{k-1}>\max\{\cdot\}$ and integrand
  $F(t)^2$. **UNSURE** about the exact domain variables of $K$.
- For $n=1$, $J$ reduces to the Polymath-type quantity
  $\int_{\sum_{i<k}t_i\le A_1-\varepsilon}\big(\int F\,dt_k\big)^2$ (my reduction).

**Prop. 1 hypotheses.**
1. $-c_2\le\rho(n;x)\le1_{\mathbb P}(n)$.
2. $\rho$ is equidistributed for the moduli "corresponding to" $T_k$ (Def. 3).
3. If $\rho(n)\neq0$, every prime factor of $n$ exceeds $x^\beta$, with $\beta>\max_jB_{j,1}$.
4. $\sum_{n\in[x,2x]}\rho=(1-c_1+o(1))x/\log x$.

For symmetric $F$ supported on $T_k$, the criterion is
$$\text{(2.1)}\qquad \frac{k(1-c_1)J(F)-kc_2K(F)}{I(F)}>1 \ \Longrightarrow\ H_1\le H(k).$$

**Normalisation check (mine).** With $G(u)=F(u/4)$ one gets $kJ(F)/I(F)=\tfrac14\,kJ(G)/I(G)$. So "$>1$" is Polymath's "$>4$" on
the $\times4$-dilated region.

### 2(c) Equidistribution input (§3.2, Lemmas 3–7; Props. 2–3)
- Moduli lie in $[1,x^{1/2+2\omega}]$ and have $x^\delta$-smooth-type factorisations. Below $x^{1/2}$, BV is used.
- Conditions on $(\omega,\gamma,\delta)$, where $\gamma=\log_x$ (convolution variable):

| Lemma | Estimate | Conditions |
|---|---|---|
| Lemma 3 | Type IIa (Polymath8a) | $24\omega+7\delta-5\gamma<-2$, $8\omega+3\delta-\gamma<0$ |
| Lemma 4 | Type IIb | $24\omega+7\delta-3\gamma<-1$, $8\omega+3\delta-\gamma<0$ |
| Lemma 5 | Type I (Baker–Irving) | $3\gamma-12\omega-3\delta>1$ for $\gamma\le\tfrac12$; $68\omega+14\delta<1$ for $\gamma\in(\tfrac12,\tfrac12+2\omega+\varepsilon]$ |
| Lemma 6 | Type IIc (Stadlmann [6]) | $8\omega+4\delta+2\gamma<1$, $32\omega+10\delta-\gamma<0$, $48\omega+16\delta-4\gamma<-1$ |
| Lemma 7 | Type III (Polymath8a) | $28\omega+9\gamma+8\delta<4$ |

- Level parameter (Prop. 3(A)): $\omega(j,j')=\frac{A_j+A_{j'}}2-\frac14$.
- Minorant (Prop. 2, Harman's sieve):
  - Constraints: $2\xi_1+3\xi_2<2$, $\xi_2\le\xi_3$, $\xi_1+9\xi_2<4$, $2\xi_1+\xi_2>1$, $17\xi_2<7$.
  - $c_2=24$ if $\xi_2>2/5$, else $c_2=0$.
  - $c_1=\int_{1-2\xi_2}^{\xi_2}\int_{1-2\xi_2}^{\min(\alpha_1,\xi_2-\alpha_1)}\cdots+\int_{1-2\xi_2}^{8\xi_2-3}\cdots$. Both ranges are
    empty at $\xi_2=0.4$, consistent with $c_1=0$ (my check).

### 2(d) Final choice (§6.2) and numerics (§5.1)
- **Support parameters:** $\varepsilon=0.0075$, $\underline A=(-\varepsilon,0.253)$ (so $n=1$), $\delta=0.028$.
  - Caps: $B_{1,1}=B_{1,2}=0.15$ and $B_{1,m}=0.17$ for $m\ge3$.
  - Effective region: $\sum t_i<0.2605$, with $J$ restricted to $\sum_{i<k}t_i\le0.2455$. In Polymath scaling ($\times4$):
    support $\le1.042$, marginal domain $\le0.982$.
  - $\omega_{\max}=A_1-\tfrac14=0.003$ (my computation; not stated as such).
- **Minorant:** $\xi=(0.38,0.4,0.4)$, which gives $\rho=1_{\mathbb P}$ and $c_1=c_2=0$. The criterion is then $kJ/I>1$ with
  $k=49$.
- **Basis** $\mathcal B_D=\{p^2(1-\sum t_i)^b\}$ with $p$ symmetric of degree $a$ and $2a+b\le D$; the result uses $D=19$.
  The text says $\mathcal B_{27}$ was what gave 246. **UNSURE** whose computation that refers to.
- **Value:** only "$\underline cM_2\underline c^T/\underline cM_1\underline c^T>1$" is stated; **no numerical value** was found.
  The basis dimension is not stated.

---------------------------------------------------------------------------------------------
## 3. Charton, Hong, Lau, Ono, Remy, Siu, Swaminathan, Thorner, Xie, "A New Bound for Small Gaps Between Primes"
primegaps.axiommath.ai/bgp212.pdf (preliminary draft, 3 Sep 2026)

**Main result:** Thm 1.1 gives $H_1\le212$, via $\mathrm{DHL}[45,2]$ and an admissible 45-tuple of diameter 212 (Lemma 12.1).
The proof route is Thm 4.10 + Thm 7.11 + Thm 11.1.

**Support (Def. 4.1, "Stadlmann support").** Same $T_k(\delta,A,B,\varepsilon)$ as §2(a), written with
- $S(t)=\sum t_i$;
- $R_\delta(t)=\{i:t_i>\delta\}$;
- $M_\delta(t)=\sum_{i\in R_\delta}t_i\le B_{j,|R_\delta(t)|}$;
- $B_{j,0}=0$, and $B$ is an $n\times\lfloor1/\delta\rfloor$ matrix.

**Functionals.** $I_T$, $J_T$ and $K$ are as in §2(b), with the identical $J$ domain. The criterion is Prop. 4.7, and
Thm 4.10 is its $\rho=1_{\mathbb P}$ form: if
$$kJ_T(F)>I_T(F)$$
for some symmetric $F\neq0$ in $L^2(T)$, and $1_{\mathbb P}$ is equidistributed on the moduli generated by $T$, then
$\mathrm{DHL}[k,2]$ holds. After dilating by 4 the threshold becomes 4.

**Moduli (Def. 4.3).** $q=ee'\prod f_a\prod f'_b$, where
- each $f_a,f'_b\ge x^\delta$ is rough;
- $ee'$ is $x^\delta$-smooth;
- $\log_x\prod f_a\le(1-\varepsilon_0)B_{j,m}$;
- $\log_x(e\prod f_a)\le(1-\varepsilon_0)(A_j-\varepsilon)$.

The same five Type I/II/III estimates as Stadlmann are used (§5 table), plus an explicit treatment of the $x^{1/2}$
transition (§8).

**Parameters (Table 3, §9).**
- Basic: $k=45$, $\delta=41/2500$, $\omega=7/1000$, $(A_0,A_1)=(-1/125,257/1000)$, $\varepsilon_s=1/125$.
- Minorant: $(\xi_1,\xi_2,\xi_3)=(19/50,2/5,2/5)$, so $\rho=1_{\mathbb P}$ and $c_1=c_2=0$.
- Caps: $B_{1,m}=(777,794,875,917,953,983,1016,1042,1063,1081)/5000$ for $m\le10$, and $1081/5000$ for $m\ge11$.
  **UNSURE** about the $/5000$ denominator.
- Rescaled ($\times4$): $L=4(A_1+\varepsilon)=53/50=1.06$ (support), $\tau=4(A_1-\varepsilon)=249/250$ (marginal cutoff),
  $g=4\delta=41/625$.
- The draft has internal inconsistencies, e.g. Lemma 9.1 caps vs Table 3, and §9.2 arithmetic. **UNSURE.**

**Certificate (Thm 11.1).**
- Basis: $\mathcal B_{21}=\mathrm{span}_{\mathbb Q}\{(L-P_1)^aP_\lambda:\ a\ge0,\ \lambda\text{ even parts},\ a+|\lambda|\le21\}$,
  dimension 846.
- Result: $J_T(F^\star)/I_T(F^\star)=4.00438409833460131937\ldots>4$, in exact rational arithmetic.
- The coefficients are not printed in the visible text.

---------------------------------------------------------------------------------------------
## 4. Side-by-side (Polymath-normalised: support $\sum t_i\le L$, marginals over $\sum_{j\ne i}t_j\le\tau$, threshold 4)
| source | k | L (support) | tau (marginal domain) | extra constraint | input | ratio |
|---|---|---|---|---|---|---|
| PM8b Thm 3.9(vii) | 54 | 1 | 1 | none | BV | $>4.00238$ |
| PM8b Thm 3.13(i) | 50 | 1.04 | 0.96 | none | BV | $>4.0043$ |
| Stadlmann §6.2 | 49 | 1.042 | 0.982 | rough-mass caps $4B_{1,m}$ | BV + smooth-moduli level $1/2+2\omega$ | $>4$ (value not stated) |
| Axiom Thm 11.1 | 45 | 1.06 | 0.996 | rough-mass caps | same, optimised | $4.004384\ldots$ |
