# Source notes: Friedlander and Iwaniec, "The polynomial X^2+Y^4 captures its primes"

Compiled 2026-11-15 by a helper agent. Nothing here is a new result.

## 0. Provenance and conventions

- Source: J. Friedlander and H. Iwaniec, "The polynomial X^2+Y^4 captures its primes", Annals of Math. 148 (1998), 945-1040.
  The arXiv copy is **arXiv:math/9811185v1** [math.NT], 1 Nov 1998. The abs page lists only v1 ("[v1] Sun, 1 Nov 1998 00:00:00 UTC (294 KB)").
  The PDF's first page reads "Annals of Mathematics, 148 (1998), 945–1040" and carries the stamp "arXiv:math/9811185v1 [math.NT] 1 Nov 1998".
  The title on the abs page is "The polynomial X^2+Y^4 captures its primes" (authors Friedlander, John; Iwaniec, Henryk). It matches.
- File: `curl -sSL -o fi.pdf https://arxiv.org/pdf/math/9811185`, saved to
  `/tmp/claude-0/-home-user-twin-primes/54430104-a9b2-55b9-836e-bd3a5496257d/scratchpad/fi_x2y4/fi.pdf`
  (96 pages, PDF 1.4). It is not committed.
  **SHA-256: `7c1ef7c50fe5ac405560c0bf56baea5fd6c014bdc6fc5d248727b96f66cdb07a`**
- Text was taken with `pdftotext -layout`. Nothing from the download was executed.
- **Page numbers:** "p. P/N" means PDF page P and printed (Annals) page N. Throughout, N = P + 944. PDF page 1 is the
  title/contents page (printed 945).
- **Q:** marks a verbatim quotation of prose from the extracted text. Words split across lines by hyphenation are kept as
  `-` (e.g. "intrin-sic"). Inside quotations, inline formulas the extraction flattened are given in `$...$`, rendered from the
  layout. Where the rendering is mine and not literal, it is marked **[formula rendered from layout]**.
- Displayed formulas are **transcriptions**: I rebuilt them from the layout output, which splits superscripts across lines.
  They are not literal text. Every display was checked against its surrounding prose, and doubtful pieces are flagged.
- **Mine:** marks my own reading or arithmetic.

---------------------------------------------------------------------------------------------

## 1. Main theorem (p. 2/946)

**Q:** "In this paper we prove that there are infinitely many primes of the form a2 + b4 , in fact getting the asymptotic
formula. Our main result is" (p. 2/946)

Theorem 1, display (1.1) **[formula rendered from layout]**:
$$\sum\sum_{a^2+b^4\le x}\Lambda(a^2+b^4)=4\pi^{-1}\kappa\,x^{3/4}\Big(1+O\Big(\frac{\log\log x}{\log x}\Big)\Big)$$
**Q:** "where a, b run over positive integers and" (p. 2/946)

Display (1.2) **[formula rendered from layout]**: $\kappa=\int_0^1(1-t^4)^{1/2}\,dt=\Gamma(\tfrac14)^2/6\sqrt{2\pi}$.

**Q:** "Here of course, Λ denotes the von Mangoldt function and Γ the Euler gamma function. The factor 4/π is meaningful; it
comes from the product (2.17) which in our case is computed in (4.8)." (p. 2/946)

The arXiv abstract gives the same statement in TeX: "\sum_{a^2 + b^4\le x} \Lambda(a^2 + b^4) = 4\pi^{-1}\kappa x^{3/4} (1 +
O(\log\log x / \log x))".

Further statements in the paper:
- Theorem 2 (p. 4/948): spin equidistribution. **Q:** "Given a Fermat prime p we define its spin σp to be the Jacobi symbol
  $(s/r)$ where p = r2 + s2 is the unique representation in positive integers with r odd." **[inline formula rendered]**
  Display (1.7): $\sum\sum_{r^2+s^2=p\le x}(s/r)\ll x^{76/77}$, with **Q:** "where r, s run over positive integers with r odd
  and $(s/r)$ is the Jacobi symbol." **[formula rendered from layout]**
- Ineffectivity. **Q:** "For this reason the constant implied in (16.41) is not effectively computable nor is the one in our
  main Theorem 1. All the other arguments in this paper give effective results, such as Theorem 2." (p. 68/1012)
- How the formula with $\Lambda$ is reached. Display (4.7), p. 19/963: $\sum_{p\le x}a_p\log p=HA(x)(1+O(\log\log x/\log x))$,
  with $a_n$ = number of integral solutions of $a^2+c^4=n$ (4.1). Display (4.8): $H=\prod_p(1-\chi_4(p)p^{-1})=L(1,\chi_4)^{-1}=4/\pi$.
  **Q:** "Therefore (4.7), (4.8) and (4.2) yield the asymptotic formula (1.1) of our main theorem. Note that in the formulation
  of Theorem 1 we restricted to representations by positive integers thus obtaining a constant equal to one fourth of that in
  (4.7)." (p. 20/964). **Mine:** so the theorem is proved with a sum over primes weighted by $\log p$. Prime powers $p^k$,
  $k\ge2$, contribute negligibly to the $\Lambda$-sum; the paper does not spell this out at this point.

## 2. How the asymptotic sieve is applied

### 2.1 Which version of the sieve is used
The paper does **not** cite the companion paper [FI3] by its theorem numbers. Section 2 restates it as **Proposition 2.1**.
[FI3] is "Asymptotic sieve for primes, Ann. of Math., 148 (1998), 1041–1065" (reference list, p. 96/1040). I did not download
arXiv:math/9811186. So the matching between Proposition 2.1 here and Theorems 1-3 / hypotheses (R), (B) of [FI3] is **not
verified**.

**Q:** "In this section we state a result of [FI3] in a form which is suitable for the proof of the main theorem. Let A = (an )
be a sequence of real, nonnegative numbers for n = 1, 2, 3, ... Our objective is an asymptotic formula for $S(x)=\sum_{p\le
x}a_p\log p$ subject to various hypotheses familiar from sieve theory." (p. 8/952)

Hypotheses as stated on pp. 8-10/952-954 (displays transcribed):
- (2.1) $A(x)\gg A(\sqrt x)(\log x)^2$. (2.2) $A(x)\gg x^{1/3}(\sum_{n\le x}a_n^2)^{1/2}$.
- (2.3) $A_d(x)=\sum_{n\le x,\,n\equiv0(d)}a_n=g(d)A(x)+r_d(x)$. (2.4) $0\le g(p^2)\le g(p)<1$. (2.5) $g(p)\ll p^{-1}$.
  (2.6) $g(p^2)\ll p^{-2}$. (2.7) $\sum_{p\le y}g(p)=\log\log y+c+O((\log y)^{-10})$.
  (2.8) $A_d(x)\ll d^{-1}\tau(d)^8A(x)$ uniformly in $d\le x^{1/3}$.
- **Type I / remainder, (2.9)-(2.10):** $\sum^3_{d\le DL^2}|r_d(t)|\le A(x)L^{-2}$ uniformly in $t\le x$, for some $D$ with
  $x^{2/3}<D<x$. **Q:** "Here the superscript 3 in (2.9) restricts the summation to cubefree moduli and L = (log x)2 ." The
  exponent of $L$ is **[garbled]**. The layout shows a superscript "24" over "2", so most likely $L=(\log x)^{2^{24}}$.
- **Type II / bilinear, (2.11)-(2.15)** (p. 9-10/953-954):
  $$\Big|\sum_m\sum_{\substack{N<n\le2N\\ mn\le x\\ (n,m\Pi)=1}}\beta(n)a_{mn}\Big|\le A(x)(\log x)^{-2^{26}}$$
  The exponent is **[garbled]**. The layout shows "26" above "−2", so most likely $-2^{26}$. Here (2.12)
  $\beta(n)=\beta(n,C)=\mu(n)\sum_{c\mid n,\,c\le C}\mu(c)$. **Q:** "This is required for every C with (2.13) 1 ⩽ C ⩽ xD−1 ,
  and for every N with (2.14) ∆−1 √D < N < δ−1 √x , for some ∆ ⩾ δ ⩾ 2. Here Π is the product of all primes p < P with P which
  can be chosen at will subject to (2.15) 2 ⩽ P ⩽ ∆1/2 35 log log x ." The exponent in (2.15) is **[garbled]**. It reads
  $P\le\Delta^{1/(2\cdot35\log\log x)}$ or something close to it; check the printed paper.
- Conclusion, (2.16)-(2.17): $S(x)=HA(x)(1+O(\log\delta/\log\Delta))$ with $H=\prod_p(1-g(p))(1-\frac1p)^{-1}$.
- **Q:** "In practice δ is a large power of log x and ∆ is a small power of x. For most sequences all of the above hypotheses
  are easy to verify with the exception of (2.9) and (2.11). The hypothesis (2.9) is a traditional one while (2.11) is quite new
  in sieve theory." (p. 10/954)

### 2.2 The sequence
**Q:** "Throughout an denotes the number of integral solutions a, c to (4.1) a2 + c4 = n ." (p. 18/962). Equivalently, (3.1)
$a_n=\sum\sum_{a^2+b^2=n}Z(b)$ with **Q:** "From now on Z(b) is equal to 2 if b = c2 > 0, Z(0) = 1, and Z(b) = 0 otherwise."
(p. 16/960), and **Q:** "Note that Z(b) is the Fourier coefficient of the classical theta function." (p. 16/960).
(4.2) $A(x)=\sum_{n\le x}a_n=4\kappa x^{3/4}+O(x^{1/2})$ (p. 18/962). $g$ is given by (3.16): $g(p)p=1+\chi_4(p)(1-\frac1p)$,
$g(p^2)p^2=1+\rho(p)(1-\frac1p)$, "except that g(4) = 14" (**[garbled]**; this is $g(4)=\tfrac14$) (p. 17/961).

### 2.3 Type I verification (Section 3)
Proposition 3.5 (p. 18/962): "We have for all t ⩽ x," (3.19) $\sum^3_{d\le D}|r_d(t)|\ll D^{1/4}x^{9/16+\varepsilon}$.
**Q:** "Proposition 3.5 verifies one of the two major hypotheses of the ASP (Asymptotic Sieve for Primes), namely (2.9) with
D = x 4 −5ε by a comfort-able margin and indeed is, apart from the ε, the best that one can hope for." (p. 18/962). The
exponent is $D=x^{3/4-5\varepsilon}$ (the "3" sits on the line above). **Q:** "Therefore we are left with the problem of
establishing the second major hypothesis of the ASP, namely the bilinear form bound (2.11)." (p. 18/962)

The input is Lemma 3.1 (p. 12/956), a modification of Lemma 4 of Fouvry-Iwaniec [FI]. It rests on the Davenport-Halberstam
large sieve for the well-spaced roots $\nu/d$ of $\nu^2+1\equiv0\pmod d$ (Lemma 3.2, p. 13/957). **Q:** "Of course, in [FI]
the authors had no reason to consider such a thin sequence so their version did not take advantage of the lacunarity of the
squares." (p. 12/956)

### 2.4 The Type II estimate: Proposition 4.1 (p. 19/963)
Display (4.3): $B(x;N)=\sum_m\sum_{N<n\le2N,\ mn\le x,\ (n,m\Pi)=1}\beta(n)a_{mn}$, **Q:** "with coefficients β(n) given by
(2.12) and Π the product of primes p ⩽ P with P in the range (4.4) (log log x)2 ⩽ log P ⩽ (log x)(log log x)−2 ."

**Q (Proposition 4.1):** "Let η > 0 and A > 0. Then we have (4.5) B(x; N ) ≪ A(x)(log x)4−A for every N with (4.6) $x^{1/4+\eta}
< N < x^{1/2}(\log x)^{-B}$ and the coefficients β(n, C) given by (2.12) with 1 ⩽ C ⩽ N 1−η . Here B and the implied constant
in (4.5) need to be taken sufficiently large in terms of η and A." (p. 19/963) **[(4.6) rendered from layout]**

**Q:** "(it suffices to have (4.5) with A = 226 + 4 and x3/8−η < N < x1/2 (log x)−B for some η > 0 and B > 0)" (p. 19/963).
"226 + 4" is **[garbled]**, almost certainly $2^{26}+4$, which matches the exponent in (2.11).
**Mine:** the lower limit $x^{3/8}$ is $\sqrt D$ with $D\approx x^{3/4}$ from Section 2.3, as (2.14) requires. The proposition
covers the wider range from $x^{1/4+\eta}$.

**Q:** "It remains to prove Proposition 4.1, and this is the heart of the problem." (p. 20/964)

Form of the coefficients:
- Outer variable: after dyadic splitting, **Q:** "(4.20) $B^*(M,N)=\sum\sum_{(m,n)=1}\alpha(m)\beta(n)a_{mn}$, where we allow α(m)
  to be any complex numbers supported on (4.18) with |α(m)| ⩽ 1, while β(n) are given by (4.13)." (p. 22/966). (4.18) is
  $M<m\le2M$. **[formula rendered from layout]**
- Inner variable: (4.13) $\beta(n)=p(n)\mu(n)\sum_{c\mid n,\,c\le C}\mu(c)$, with $p$ a smooth bump on $N'<n\le(1+\theta)N'$
  (4.12), $\theta=(\log x)^{-A'}$ (4.15). The support is restricted to $(n,\Pi)=1$ (4.21) and $\tau(n)\le\tau$ (4.22). Also
  (4.19) $\vartheta x<MN<x$, with $\vartheta=(\log x)^{-A}$ (4.16). **Q:** "Note that (4.6) and (4.19) imply M ⩾ N since we may
  require B ⩾ 2A." (p. 22/966)
- Target (4.23): $B^*(M,N)\ll\vartheta\theta(MN)^{3/4}(\log MN)^4$.
- **Q:** "When resolving these problems we wish to preserve the nature of the coef-ficients β(n) (think of β(n) as being the
  Möbius function). Thus we should avoid any technique which uses long integration because it corrupts β(n)." (p. 20/964)

Chain of reductions, as stated in Section 18 (p. 72-74/1016-1018):
Proposition 4.1 ⇐ (4.23) for $B^*$ ⇐ (5.15) for $B(M,N)$ on a polar box ⇐ (via Cauchy, (5.17)) (5.20)/(5.25) for
$D^*(M,N)$ ⇐ (9.10) [error term of the lattice count] + main term $D_0$ (10.10) ⇐ **Proposition 10.2**
($T(\beta)\ll N^2(\log N)^{-\sigma}+P^{-1}N^2\log N$, p. 42/986) ⇐ $T=U+V+W$ (10.14), handled by Proposition 16.3 ($U$, small
moduli), Proposition 15.1 / 14.1 ($V$, medium) and Proposition 17.3 ($W$, large). Proposition 17.3 ⇐ **Proposition 17.2** ⇐
Section 25 (Proposition 23.1 + combinatorial identity (24.13) / Proposition 24.2 + Theorem 2ψ).
**Q:** "Assuming only Proposition 17.2 we have all the pieces finally in place for the proof of Theorem 1." (p. 73/1017)

Proposition 17.2 (p. 72/1016) **[formula rendered from layout]**: "For every character (17.17) we have (17.18)
$S_{\chi k}(\beta')\ll N^{1-\delta}$ uniformly in $d(|k|+1)\le N^\delta$ for some positive constant δ."
Here (17.14) $S_{\chi k}(\beta')=\sum^\wedge_{(z,\Pi)=1}\beta_z[z]\chi(z)(z/|z|)^k$.

## 3. The arithmetic structure behind the Type II estimate

### 3.1 Gaussian integers and the norm factorisation (Section 5)
**Q:** "However in the case of our special form B ∗ (M, N ) the application of Cauchy's inequality at this stage would be
premature. This is due to the multiplicity of representations (5.1) $a_{mn}=\sum_{a^2+c^4=mn}1$ where a, c run over all
integers. This multiplicity is locked into the inner sum and we do not wish to amplify it by squaring since that would have
fatal effects on the harmonic analysis when the time comes to count the lattice points. Therefore, we release that part of the
multiplicity which is accommodated in the outer variable and we smooth out this part rather than amplify by applying Cauchy's
inequality. In order to be able to extract this hidden part of the multiplicity we shall write the solutions a2 +b2 = mn in a, b
∈ Z in terms of Gaussian integers w, z ∈ Z[i]. Not only is our entry to the Gaussian domain necessary but it will also clarify
the arguments. The arithmetic we are going to apply lies truly in the field Q(i)." (p. 22/966)

**Q:** "Since (m, n) = 1 we have by the unique factorization in Z[i] (5.2) $a_{mn}=\frac14\sum_{|w|^2=m}\sum_{|z|^2=n}Z(\mathrm{Re}\,wz)$
where 14 accounts for the four units 1, i, i2 , i3 in Z[i]." (p. 23/967). Here "14" is **[garbled]** for $\frac14$.
Then (5.6) $B^*(M,N)=\sum\sum_{(w\bar w,z\bar z)=1}\alpha_w\beta_z Z(\mathrm{Re}\,wz)$ **Q:** "where αw = α(|w|2 ) and βz =
β(|z|2 )." (p. 23/967). The $z$ are primary, $z\equiv1\pmod{2(1+i)}$ (5.3).

**Mine:** this is exactly the point where "n is a norm" is used. The condition $mn\in\{a^2+c^4\}$ becomes the bilinear condition
$\mathrm{Re}(wz)=c^2$ on a pair of Gaussian integers $(w,z)$ with $|w|^2=m$, $|z|^2=n$. The outer variable $w$ is then free (after
(5.10)), and Cauchy-Schwarz is applied over $w$ (5.17)-(5.18):
$D(M,N)=\sum_wf(w)|\sum_z\beta_zZ(\mathrm{Re}\,wz)|^2$.

### 3.2 Lattice-point count: where thinness enters (Sections 6-9)
After squaring out, (5.27) $C(z_1,z_2)=\sum_wf(w)Z(\mathrm{Re}\,wz_1)Z(\mathrm{Re}\,wz_2)$. The pairs with $\mathrm{Re}\,wz_j=c_j^2$
are parametrised by **Q:** "i∆w = c21 z2 − c22 z1 ." (p. 29/973), which is equivalent to the congruence (6.4)
$c_1^2z_2\equiv c_2^2z_1\pmod{|\Delta|}$. The modulus is the determinant (6.1) $\Delta=\mathrm{Im}\,\bar z_1z_2$, with (6.2)
$1\le|\Delta|<4\pi\theta N$. **Q:** "The problem reduces to counting lattice points inside the curve t41 − 2γt21 t22 + t42 = x for
fixed γ with 0 < γ < 1, namely γ = cos(α2 − α1 ) where αj = arg zj . This particular curve arises because of the particular
choice (3.14) of Z(b) as the Fourier coefficient of the classical theta function. The counting requires quite subtle harmonic
analysis because the points involved are also constrained by a congruence to a large modulus, so there are very few points
relative to the area of the region." (p. 28-29/972-973)

Poisson summation gives (6.9) with zero frequency (6.13) $C_0=|z_1z_2|^{-1/2}F_0G_0$. The dual length is (Lemma 7.1, p. 32/976)
$H=M^{-1/4}N^{3/4}$. **Q:** "Note that for N in (4.6) and M N satisfying (4.19) we have (9.3) xη < H < N 2 ." (p. 36/980). The
upper bound is **[garbled]**; it should be $N^{1/2}$. **Mine:** with $MN\asymp x$, $H\asymp x^{-1/4}N$. So $H>x^\eta$ holds exactly
when $N>x^{1/4+\eta}$, and this is where the lower end of (4.6) comes from.

Where the authors locate the thinness:
- **Q:** "It is in this counting that we exploit the great regularity in the distribution of the squares and after this step
  the problem of the thinness of the sifting set is gone." (p. 4/948)
- **Q:** "The lacunarity of the original sequence A = (an ) has featured in the estimation for the error term in (9.10), and it is
  no longer an issue in the main term D0 (M, N )." (p. 40/984)
- The density $x^{3/4}$ also sets the level in the Type I estimate (Section 2.3 above): $D=x^{3/4-5\varepsilon}$ "is, apart from the ε,
  the best that one can hope for" (p. 18/962). (3.4) and (3.5) give the trivial bound $x^{3/4}(\log x)^2$.

### 3.3 The quadratic symbol in the main term (Sections 8, 10)
$G_0(z_1,z_2)=|\Delta|^{-1}\#\{\gamma_1,\gamma_2:\gamma_1^2z_2\equiv\gamma_2^2z_1\ (\mathrm{mod}\ |\Delta|)\}$ (6.12).
Lemma 8.4 (p. 36/980) **[formula rendered from layout]**: under $(z_1,z_2)=(z_1,\bar z_1)=(z_2,\bar z_2)=1$ and
$z_1\equiv z_2\pmod 8$, (8.16) $G_0(z_1,z_2)=2\sum_{4d\mid\Delta}\frac{\varphi(d)}{d}\Big(\frac{z_2/z_1}{d}\Big)$. This uses that
$z_2/z_1$ is congruent to a rational integer mod $|\Delta|$, by (6.6).

**Q:** "The required improvement by a factor ϑ2 (actually a saving of arbitrary power of log N ) will result from the cancellation
of terms due to the sign change of βz1 β̄z2 which involve the Möbius function. These are twisted by the arithmetic kernel G0 (z1 ,
z2 ) which is rather sophisticated; it involves the Jacobi symbol (10.2) $\chi_d(z_2/z_1)=\big(\frac{z_2/z_1}{d}\big)$ which in turn
originated (in Section 8) from the roots to the congruence (10.3) ω 2 ≡ z2 /z1 (mod |∆|) ." (p. 40/984)

**Q:** "Retrospectively, the treatment of the main term D0 (M, N ) should be regarded as the core of our proof of the main Theorem
1, though it did not seem a central matter when we got the very first ideas." (p. 40/984)

$T(\beta)$ (10.13) is split by the size of $d$ into $U$ ($d\le X$), $V$ (medium) and $W$ ($d>|\Delta|/4X$) (10.15)-(10.17).
The three ranges get their cancellation from different places:
- **Medium $d$, $V(\beta)$:** **Q:** "No special properties of βz are needed. The source of cancellation is the sign change of
  the symbol χd (z2 /z1 ), not the sign change of the Möbius function which is a component of βz ." (p. 43/987). These are the
  Barban-Davenport-Halberstam-type "Jacobi-twisted sums" (11.5) $\sum\sum_{\bar rs\equiv a(d)}\alpha_{rs}(r/d')$ of Sections 11-14.
  **Q:** "But nothing like (11.12) holds in our case! The absence of such a factorization and the presence of the Jacobi symbol
  necessitate new ideas to pursue the goal." (p. 45/989). (11.12) is $\alpha_{rs}=\beta_r\gamma_s$.
- **Small $d$, $U(\beta)$:** **Q:** "Here the moduli are small and the source of cancellation will be the sign change of the Möbius
  function which is part of βz . Therefore we can afford to estimate Ud (β) individually for every d ⩽ X. In view of the
  multiplicative structure of βz it is natural to employ Hecke characters." (p. 60/1004). This range needs a Siegel-Walfisz
  analogue for Gaussian primes (Goldfeld's argument, p. 5/949), which is why Theorem 1 is ineffective.
- **Large $d$, $W(\beta)$:** the divisor is flipped to $|\Delta|/4d$, and quadratic reciprocity produces the "spin". Lemma 17.1
  (p. 69/1013) **[formula rendered from layout]**: assuming (17.2)-(17.4), (17.5)
  $\Big(\frac{z_2/z_1}{|\Delta|}\Big)=\Big(\frac{s_1}{|r_1|}\Big)\Big(\frac{s_2}{|r_2|}\Big)$, where $\Delta=r_1s_2-r_2s_1$ for
  $z_j=r_j+is_j$. The proof appeals to "(17.6)" quadratic reciprocity with the Hilbert symbol at ∞. This gives (17.8)
  $\beta'_z=i^{(r-1)/2}(s/|r|)\beta_z$ and the Jacobi-Kubota symbol (17.16)/(20.1) $[z]=i^{(r-1)/2}(s/|r|)$, $z=r+is$.
  **Q:** "This extra spin of β ′ will be vital in producing cancellation inSχk (β ′ )." (p. 71/1015). **Q:** "This time the source
  of cancellation is the symbol [z] which is attached to βz , not the character ψ(z) nor the Möbius function µ(|z|2 ).
  Therefore the conductor of ψ plays a minor role." (p. 72/1016)
- From the introduction: **Q:** "An interesting feature in our case is that, due to the presence of the Jacobi symbol, the law
  of quadratic reciprocity plays a crucial role in this involution and an extra Jacobi symbol (of the type occurring in Theorem
  2) emerges in the transformed sum (see Lemma 17.1)." (p. 5-6/949-950). **Q:** "Now however the presence of the Jacobi-Kubota
  symbol destroys the previous argument, that is the theory of Hecke L-functions is not applicable here." (p. 6/950)

### 3.4 Real characters in Z[i] and the spin sums (Sections 19-26)
- Dirichlet symbol (19.2): for odd $q$ and a root $\omega$ of $\omega^2+1\equiv0\pmod q$, $\xi(z)=\big(\frac{r+\omega s}{q}\big)$
  for $z=r+is$. **Q:** "Therefore ξ is a character on Gaussian integers modulo q; it is an extension of the Jacobi symbol on the
  rational integers" (p. 74/1018).
- Multiplier rule, Lemma 20.1 (p. 77/1021): **Q:** "If w is primary primitive and z ≡ 1 (mod 2) then (20.3) $[wz]=\varepsilon[w][z]\big(\frac zw\big)$
  with ε = ±1 depending only on the quadrants in which w, z, wz are located." **[(20.3) rendered from layout]**
  **Q:** "Of course, [z] is not multiplicative per se, yet it is nearly so, up to a factor which is the Dirichlet symbol." (p.
  77/1021)
- Bilinear forms (Type II for the spin): Proposition 21.4 (p. 84/1028): for $\alpha_w,\beta_z$ on primary numbers in $|w|^2\le M$,
  $|z|^2\le N$, bounded by 1, (21.13) $K(M,N)=\sum\sum\alpha_w\beta_z[wz]\ll(M+N)^{1/12}(MN)^{11/12+\varepsilon}$.
  Proposition 23.1 (p. 88/1032) is the same bound for $L(M,N)=\sum\sum\alpha(m)\beta(n)\lambda(cmn)$, with an extra factor
  $\tau(c)$ (23.8), where (23.1) $\lambda(n)=\sum^\wedge_{z\bar z=n}\psi(z)[z]$ is the "quadratic eigenvalue".
  **Q:** "This time a cancellation is received from the sign changes of these symbols rather than from those of the Möbius
  function which also makes an appearance arising as coefficients from our particular sieve theory." (p. 6/950)
- Linear forms: Proposition 22.1 / 23.2 (p. 85/1029, 89/1033), via Pólya-Vinogradov (p. 6/950).
- Theorem 2ψ (p. 93/1037): (26.2) $\sum_{n\le x}\Lambda(n)\lambda(cn)\ll cf\,x^{76/77}$ with $f=d(|k|+1)$. It is proved with Vaughan's
  identity (26.3) and Propositions 23.1-23.2.
- Proposition 17.2 is deduced in Section 25 from Proposition 23.1 and Theorem 2ψ, through the identity (24.13) (p. 92-93/1036-1037).

**Mine (summary of §3):** the Type II cancellation comes from three sources. (i) The norm structure turns $a_{mn}$ into a sum over
$(w,z)$ with a linear constraint $\mathrm{Re}\,wz=c^2$. (ii) The squares are equidistributed in residue classes, which handles
the nonzero frequencies; this is where the thinness is absorbed. (iii) The zero-frequency term is a twisted sum with a real
quadratic character of $z_2/z_1$. Its cancellation comes from the Möbius function for small moduli, from the quadratic symbol
for medium moduli, and, after quadratic reciprocity, from the spin $[z]$ for large moduli.

## 4. Remarks in the paper about limits, parity, other problems

All are quoted exactly. A search of the extracted text found **no mention** of twin primes, $n(n+2)$, Goldbach, shifted primes,
or prime values of linear forms in several variables. The words "twin", "Goldbach" and "shifted" do not occur, and "n + 2" does
not occur as such. The only mention of linear polynomials is the historical sentence below.

- **Q:** "Polynomials in one variable are naturally more difficult and only the case of linear polynomials is settled, due to
  Dirichlet." (p. 2/946)
- **Q:** "We expect, but did not check, that the methods carry over to the prime val-ues of φ(a, b2 ) for φ a quite general
  binary quadratic form. The method fails however to produce primes of the type φ(a, b2 ) where φ is a non-homogeneous
  quadratic polynomial." (p. 3/947). No reason is given at that point.
- **Q:** "In the first case one would begin with a rather dense set but would then have to select a very thin subset. In our
  approach we begin with a very thin set but one which is sufficiently regular in behaviour for us to detect primes." (p. 3/947)
- Parity. **Q:** "In its classical format the sieve is unable to detect primes for a very intrin-sic reason, first pointed out by
  Selberg [Se] and known as the parity problem. The asymptotic sieve of Bombieri [Bo1], [FI1] clearly exhibits this problem. We
  base our proof on a new version of the sieve [FI3], which should be regarded as a development of Bombieri's sieve and was
  designed specifically to break this barrier and to simultaneously treat thinner sets of primes." (p. 3/947)
- **Q:** "In departing from the classical sieve, we introduce (see (2.11)) an addi-tional axiom which overcomes the parity
  problem. As a result of this we are now required also to verify estimates for sums of the type (1.6) $\sum_\ell\sum_m\beta(m)a_{\ell m}$
  where β(m) is very much like the Möbius function and an is the number of representations of (1.5) for given n = ℓm." (p.
  3-4/947-948)
- **Q:** "The hypothesis (2.9) is a traditional one while (2.11) is quite new in sieve theory." (p. 10/954)
- Method-specific failures (these are about techniques inside the proof, not about other problems):
  - **Q:** "Since the Jacobi symbol for the enlarged modulus dp2 is essentially the same as that for d this gives us a multiple
    counting of the original sum. Without this multiplicity we would gain nothing and for this reason the method fails for
    general characters." (p. 55/999)
  - **Q:** "However such an approach fails because it ignores the intrinsic nature of the factor J (χ) (which is a partial
    character sum over the subgroup of rational residue classes given by (16.13))." (p. 68/1012)
  - **Q:** "However (16.39) cannot be weakened, given the current state of knowlege concerning exceptional zeros." (p. 68/1012)
- Other targets the authors suggest. **Q:** "Further interesting connections to elliptic curves hold for primes of the form 27a2
  + 4b6 and there is some hope to produce such primes using our arguments in the domain Z[ζ3 ]." (p. 8/952)
- The word "parity" also appears in the elliptic-curve remark ("The parity conjecture asserts in this case that the rank of Ep
  is odd if a ≡ 0(mod 4) and even if a ≡ 2(mod 4).", p. 7/951). That is the root-number parity, not the sieve parity problem.

---------------------------------------------------------------------------------------------

## 5. Helper's analysis, not from the source

Take the sequence $a_n=\Lambda(n+2)$, or $a_n=\mathbf 1[n+2\text{ prime}]$, and feed it into Proposition 2.1. Its conclusion would
then be the twin-prime asymptotic. Feature by feature:

**No counterpart for twin primes**
1. **Norm factorisation of $a_{mn}$ (5.2).** For $X^2+Y^4$, the event "$mn$ lies in the sequence" is a polynomial condition,
   $\mathrm{Re}(wz)=c^2$, on factors $w,z$ of $m,n$ in $\mathbb Z[i]$. This holds because the ambient set $\{a^2+b^2\}$ is the
   image of the multiplicative norm map. For $\Lambda(mn+2)$ there is no ring in which "$mn+2$ is prime" factors through
   $(m,n)$. The shift $+2$ breaks every multiplicative structure. After Cauchy over $m$, one gets
   $\sum_m|\sum_n\beta(n)\Lambda(mn+2)|^2$, and squaring out gives correlations $\sum_m\Lambda(mn_1+2)\Lambda(mn_2+2)$. These are
   binary problems at least as hard as the original. They are not lattice-point counts with a computable main term. Nothing
   plays the role of the free variable $w$ with an explicit parametrisation $i\Delta w=c_1^2z_2-c_2^2z_1$.
2. **An explicit arithmetic main term with a real character.** For FI, the zero-frequency term $G_0$ is an exact local density,
   (8.16), a divisor sum of the Jacobi symbol $(\frac{z_2/z_1}{d})$. All of the remaining cancellation (Möbius for small moduli,
   the quadratic symbol for medium moduli, the spin $[z]$ for large moduli) lives in this explicit kernel. For twin primes the
   corresponding "main term" of a Type II sum still contains $\Lambda$ (the primality of $mn+2$). It is not an explicit
   character twist of $\beta_{z_1}\bar\beta_{z_2}$. So there is no analogue of Lemma 8.4 or Lemma 17.1.
3. **The spin and quadratic reciprocity (Lemma 17.1, Sections 19-26).** The cancellation for large divisors comes from
   $[z]=i^{(r-1)/2}(s/|r|)$ along Gaussian primes (Theorem 2ψ). This is a statement about a real character attached to the
   coordinates of a Gaussian integer. It is "parity-breaking" only because the sieve weight has already been turned into an
   oscillating sum of a *different* arithmetic function, the quadratic eigenvalue $\lambda(n)$, which is not $\mu$ and not
   $\Lambda$. I see no candidate for an analogous auxiliary oscillating function for $\Lambda(n+2)$.
4. **Type I level.** Proposition 2.1 needs (2.9) with $D>x^{2/3}$, summed with absolute values over all cubefree $d$. For
   $\Lambda(n+2)$ this is an Elliott-Halberstam-type level beyond $2/3$. Bombieri-Vinogradov gives $1/2$, and the
   BFI/Zhang/Polymath extensions beyond $1/2$ need well-factorable or smooth moduli and do not allow absolute values over all
   moduli. So hypothesis (2.9) is also out of reach for twin primes, independent of (2.11). (FI get $x^{3/4}$ only because their
   sequence is so thin: the level is relative to the density $x^{3/4}$.)
5. **Thinness as an asset.** In FI the lacunarity of the squares makes the dual sum short ($H=M^{-1/4}N^{3/4}$), and they state
   that it is used up in the error term (9.10). Twin primes form a dense sequence, so this resource does not exist. Thinness is
   not the obstacle there.

**Features that might have counterparts**
- Proposition 2.1 itself is axiomatic: it applies to any nonnegative sequence. For twin primes, the whole difficulty is
  concentrated in proving (2.9) at level $>x^{2/3}$ and (2.11) for $N$ in $(\Delta^{-1}\sqrt D,\delta^{-1}\sqrt x)$ with
  Möbius-like $\beta$ and arbitrary bounded $\alpha$. By the parity heuristic, (2.11) for $\Lambda(mn+2)$ with $\beta\approx\mu$
  is essentially a "Chowla-twisted twin prime" statement. I would not expect it to be easier than the target.
- Generic tools in the paper apply to other sequences: Barban-Davenport-Halberstam-type mean values (Sections 11-14,
  "the results pertain for linear forms with very general coefficients", p. 5/949), the divisor-switching and
  moduli-enlarging tricks (Sections 12-13), and the combinatorial identity of Section 24 and Vaughan's identity.
- The general pattern does transfer in spirit. One uses an auxiliary multiplicative or algebraic structure to rewrite
  $\sum\alpha_m\beta_na_{mn}$, so that Cauchy-Schwarz lands on a sum with explicit harmonic analysis. This is the pattern of
  Heath-Brown's $x^3+2y^3$ and of later work on norm forms. All such successes known to me use sequences supported on values of
  (incomplete) norm forms. A shifted-prime sequence is not of that kind.

**Uncertain / not checked**
- I did not read [FI3] (arXiv:math/9811186). I cannot confirm how Proposition 2.1 here corresponds to its Theorems 1-3 or to
  labels such as (R) and (B).
- Several exponents in the extraction are garbled (the power of $L$ in (2.9), the exponent in (2.11), (2.15), "226 + 4",
  the upper bound in (9.3)). Check them against the printed paper before citing.
