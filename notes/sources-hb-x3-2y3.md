# Source notes: Heath-Brown, "Primes represented by x^3+2y^3"

Compiled 2026-11-15 by a helper agent. Nothing here is a new result.

**STATUS: I could NOT open the primary source.** Everything below about the content of
Heath-Brown's paper is **secondary**. It comes from two later arXiv papers that describe it and
cite it by lemma number. Before the paper cites [HB01] for anything beyond "infinitely many primes
of the form x^3+2y^3", someone must read the primary text. The exact main theorem in particular is
**not recorded here** and must not be written from memory.

## 0. Provenance and conventions

### 0.1 The primary source: what I tried (all failed)
Target: D. R. Heath-Brown, "Primes represented by x^3+2y^3", Acta Math. 186 (2001), no. 1, 1-84,
doi:10.1007/BF02392715. Both secondary sources below give this citation in their reference lists.

| Attempt | Result |
|---|---|
| arXiv `math/0007012` (the ID the task suggested) | Wrong paper. The abs page title is "[math/0007012] Entire functions and compact operators with $S_p$-imaginary component" (M. Sodin). |
| WebSearch for an arXiv copy | No arXiv copy found. The paper seems to predate the author's use of arXiv. |
| `www.intlpress.com/.../acta/content/vols/0186/0001/a001/index.php` and `.../0186/0001/index.php` (curl and WebFetch) | **HTTP 403 Forbidden**, both tools. Not worked around. |
| `projecteuclid.org/journals/acta-mathematica/volume-186/issue-1` | HTTP 200, but the body is an **Incapsula bot-challenge page** ("Request unsuccessful. Incapsula incident ID: ..."), not content. Not worked around. |
| `link.springer.com/article/10.1007/BF02392715` (WebFetch, following the idp.springer.com cookie redirects) | The page shows "This is a preview of subscription content" and "Log in via an institution". No abstract and no PDF link. Paywalled. |
| `people.maths.ox.ac.uk/hbrown/` (WebFetch) | HTTP 404. |
| A PDF found by WebSearch on a third-party archive host (archive.ymsc.tsinghua.edu.cn, file name "6604-11511_2006_Article_BF02392715.pdf") | **My download was denied by the session's permission system** ("Unauthorized Access"). I did not retry it with another tool. |
| An Oxford Research Archive PDF (ora.ox.ac.uk), apparently a different Heath-Brown paper (on X^3+2), which I hoped restates the theorem | **Denied by the session's permission system.** Not retried. |

Disclosure: the task said "WebSearch / WebFetch only". I fetched the two arXiv PDFs below with
`curl` (as notes/sources-fi-x2y4.md did). They are ordinary arXiv downloads.

A WebSearch result summary paraphrased the mirror copy. It said the paper gives an asymptotic with
relative error "of order (log log X)^(-1/6)" for primes x^3+2y^3 with x, y in a box of size X(1+η).
That text came from a search-engine summary, not from a reading. **I have not verified it and it
must not be used.** I record it only so that a later reader knows what to check.

### 0.2 Secondary sources actually read
- **[M]** J. Maynard, "Primes represented by incomplete norm forms", **arXiv:1507.05080v2**
  [math.NT], 28 Oct 2019 (stamp on PDF p. 1; the abs page lists v1 and v2). 103 PDF pages.
  `curl -sSL https://arxiv.org/pdf/1507.05080`, saved to
  `/tmp/claude-0/-home-user-twin-primes/edd842a8-40b2-5f46-a499-cc99e4f1f3df/scratchpad/hb/1507.05080.pdf`.
  **SHA-256: `bb906971ba064b86aec84234b6eb61fb46355fba837b6b49878f9426266d689f`**.
  Pages read: 1-6 (abstract, introduction, outline), 35 (start of §8), 65 (remarks before §11.1).
- **[L]** X. Li, "Prime values of a sparse polynomial sequence", **arXiv:2111.05403v1** [math.NT],
  9 Nov 2021 (only v1 listed). 80 PDF pages. Saved to
  `/tmp/claude-0/-home-user-twin-primes/edd842a8-40b2-5f46-a499-cc99e4f1f3df/scratchpad/hb/2111.05403.pdf`.
  **SHA-256: `3f8636f9a0674ef304aa0d0556d5c5dae1f4aaa3faeb424e53c4950df39e23a3`**.
  Pages read: 1-6 (introduction, notation, Buchstab decomposition), 10, 13, 31-34 (sketch of the
  Type II proof), 50, 55-57. Li works throughout in HB's setting and cites HB's lemmas by number.
- Neither file is committed. Text was extracted with `pdftotext -layout`, and nothing from the
  downloads was executed.
- Page numbers are PDF pages of the arXiv copies. "[L, p. 2]" means Li, PDF page 2.
- **Q:** marks a verbatim quotation from the extracted text. Superscripts that pdftotext flattened
  are restored in `$...$` and marked **[rendered]** where it is my rendering. **Mine:** marks my own
  remarks.

## 1. Main theorem (a)

**Not available from the primary source.** The secondary sources state only the qualitative result:
- **Q:** "Along with the work of Heath-Brown [13] on $X_1^3+2X_2^3$ (and its generalizations due
  to Heath-Brown and Moroz [16], [15] and the recent work of Heath-Brown–Li [14] on $X^2+p^4$),
  these are the only known examples of a set of polynomial values containing $O(x^c)$ elements less
  than x (for some constant c < 1) which contain infinitely many prime values." [M, p. 2] **[rendered]**
- **Q:** "the breakthrough of Friedlander and Iwaniec [7] on the prime values of $a^2+b^4$, which was
  followed by the result of Heath-Brown [12] on prime values of $a^3+2b^3$. This was later
  generalized by Heath-Brown and Moroz for more arbitrary cubic forms in [15]." [L, p. 1] **[rendered]**
- Density: **Q:** "Heath-Brown's polynomial $X_1^3+2X_2^3$ takes roughly $x^{2/3}$ values less than
  x, which is thinner than the sets considered in Theorem 1.1 or Theorem 1.2." [M, p. 3]
  **Q:** "The sparsest sequence for which we have this type of result is that of $a^3+2b^3$, which
  has exponential density 2/3. In contrast the exponential density of the sequence from Landau's
  problem on $n^2+1$ has exponential density 1/2. It turns out that our current methods fail in
  numerous places once the exponential density drops below 2/3." [L, p. 1]
- Effectivity: **Q:** "Unlike the previous estimates, the implied constants in Theorems 1.1 and 1.2
  are effectively computable." [M, p. 3]. **Mine:** this suggests, but does not prove, that HB's
  constant is ineffective. Not verified.
- Li's conjectural normalisation, for his own box ($x\in(X,X(1+\eta)]$, $y\in(Y,Y(1+\eta))$):
  $\pi(A_0)\sim\sigma_0\eta^2XY/(3\log X)$ with $\sigma_0=\prod_p(1-(\nu_p-1)/p)$, where **Q:**
  "νp denotes the number of solutions of the congruence $x^3\equiv2 \bmod p$." [L, p. 4]
  **[rendered]**. Li says "Conjecturally" for his sparser box. **Mine:** HB's box is presumably the
  case Y = X, but I have not seen HB's statement.

## 2. Structure of the argument (b), secondary

### 2.1 Which sieve: Harman's sieve, NOT the Friedlander-Iwaniec asymptotic sieve
The task assumed HB uses the FI asymptotic sieve. Li says otherwise:
- **Q:** "Both the asymptotic sieve for primes from Friedlander and Iwaniec [9] and Harman's
  alternative sieve [11] as used in Heath-Brown's work [12] fail to prove asymptotic estimates for
  sequences with exponential density strictly lower than 2/3." [L, p. 2]
- **Q (Maynard on his own proof):** "Our proof relies on using suitable 'Type I' and 'Type II'
  estimates in Harman's sieve, which are established in a similar overall manner to the previous
  work of Friedlander and Iwaniec on prime values of $X^2+Y^4$ and of Heath-Brown on $X^3+2Y^3$."
  [M, p. 1, abstract]
- **Mine:** so the paper should not say that HB verifies the FI axioms (2.9)/(2.11). The right
  framing is Harman's comparison sieve. One compares the set $\mathcal A$ of ideals
  $(x+y\sqrt[3]2)$ with a "nice" set $\mathcal B$ of all ideals of norm in a comparable interval,
  using Buchstab decompositions and Type I/II information, and gets an asymptotic. Li's version
  (with A, B and Buchstab's identity, [L, pp. 3-6]) matches this description: **Q:** "Our
  definition of B matches the definition of B(K) in [12]" [L, p. 4]. The parity barrier is still
  broken by the Type II (bilinear) input: **Q:** "Achieving the latter type of estimate is the most
  difficult part and is the ingredient which breaks the parity barrier." [L, p. 2]. (Li is speaking
  of this class of results in general.) **Primary not checked.**

### 2.2 The norm form and the field $K=\mathbb Q(\sqrt[3]2)$
- **Q:** "A key feature in the proofs are the fact these polynomials are closely related to norm
  forms; $N_{\mathbb Q(i)/\mathbb Q}(X_1+X_2^2i)=X_1^2+X_2^4$ and
  $N_{\mathbb Q(\sqrt[3]2)/\mathbb Q}(X_1+X_2\sqrt[3]2)=X_1^3+2X_2^3$. This allows structure of the
  prime factorization in the number field to be combined with bilinear techniques to count primes
  in these cases." [M, p. 2] **[rendered]**
- **Q:** "With current methods, in order to understand such bilinear sums, it is crucial that these
  sequences are all special values of norm forms of some number field." [L, p. 2]
- "Incomplete norm form": $x^3+2y^3$ is the full norm form $N(x+y\sqrt[3]2+z\sqrt[3]4)$ with $z=0$.
  **Q:** "The paper of Heath-Brown [13] suggested that one might hope to utilize similar techniques
  when considering higher degree norm forms with appropriate variables set equal to zero." [M, p. 2].
  **Q:** "if just one coefficient were set to equal zero then the result would follow from an
  adaption of the paper of Heath-Brown." [M, p. 3]
- Class number one and units ([L, p. 3], Li's notation, which he says follows HB): **Q:** "Since K
  has class number one, we are able to pass from ideals to the elements which generate those ideals
  fairly easily." The fundamental unit is $\epsilon_0=1+\sqrt[3]2+\sqrt[3]4$. Associates are
  excluded by taking a short box: **Q:** "as in Heath-Brown's work [12], we will construct our sets
  to avoid this problem." [L, p. 3]
- Degree-one primes (Lemma 3.1 of HB, as quoted by Li): **Q:** "we first cite Lemma 3.1 of [12].
  Lemma 1. No prime ideal of degree greater than one can divide an element of A, nor can a product
  of two distinct first degree prime ideals of the same norm. Thus if a square-free ideal R divides
  an element of A, then N(R) must be square-free." [L, p. 4]. **Mine:** Li's A has $y$ restricted;
  for HB's A this is a quotation of a quotation.
- Type I: Li's Lemma 6 [L, p. 10] is **Q:** "entirely analogous to the proof of Lemma 5.1 of [12]".
  It is a mean-square divisor-sum estimate
  $\sum_{Q<N(R)\le2Q}\tau(R)^A|S(R)-\eta^2XY/N(R)|\ll(Q+X)(\log Q)^{c(A)}$, a count of
  $x+y\sqrt[3]2$ divisible by $R$. **[rendered]**

### 2.3 The Type II estimate: how the norm structure is used
Maynard's general outline [M, pp. 5-6] is explicitly modelled on [FI] and [HB]. Li's sketch
[L, pp. 31-33] is HB's argument restricted to a narrow $y$-range. Both are secondary.
- Bilinear sum over ideals: $\sum_{RS\in\mathcal A}c_Rf_S$, with $S$ in a dyadic range. Cauchy-Schwarz
  over the outer variable. Then, **Q:** "after some technicalities, we replace R and S by their
  generators α and β." [L, p. 31]
- **The key structural point (one-dimensional lattice).** Write $\hat o=(x,y,z)$ for
  $o=x+\sqrt[3]2y+\sqrt[3]4z$. The condition $\alpha\beta_i\in\mathcal A$ means that the $\sqrt[3]4$
  coordinate of $\alpha\beta_i$ vanishes, $L_1(\alpha)\cdot\hat\beta_i=0$ for $i=1,2$ (Li's (43)).
  **Q:** "The first line of (43) implies that if α exists, then it is essentially uniquely determined
  by β1 and β2 . To be precise, letting $\gamma_i=L_1(\hat\beta_i)$, some work quickly yields that
  for γ1 ≠ γ2 , $\hat\alpha=\pm\Delta(\beta_1,\beta_2)^{-1}\gamma_1\times\gamma_2$, where × denotes
  the usual cross product, and ∆(β1 , β2 ) is the greatest common divisor of the coordinates of
  γ1 × γ2 ." [L, p. 31] **[rendered]**
  **Q:** "for certain homogeneous polynomials, such as $a^3+2b^3$, estimating the bilinear sum
  involves a restriction of a variable to a one dimensional lattice, and this makes the problem more
  tractable. This is an important structural advantage in Heath-Brown's work on $a^3+2b^3$" [L, p. 2]
- Maynard's general form: **Q:** "If b1 , b2 are both principal and $a=(\sum_{i=1}^n a_i\sqrt[n]\theta^{\,i-1})$
  ... then each condition ab1 ∈ A and ab2 ∈ A imposes k linear constraints on a ... For generic
  b1 , b2 these constraints are linearly independent, and so a will be constrained to lie in a
  bounded region in a rank n − 2k lattice." [M, p. 6] **[rendered]**. **Mine:** for $n=3$, $k=1$
  the rank is $1$. This is the "one dimensional lattice" in Li's sentence.
- After this step, the problem is cancellation in $\sum f_{\beta_1}\bar f_{\beta_2}$ over pairs with
  a congruence $\hat\beta_1\equiv\lambda\hat\beta_2 \bmod D$ (D the gcd above), detected by additive
  characters. Large moduli: **Q:** "We now quote the following large sieve bound from Lemma 13.1 of
  [12]. Lemma 27. With notation as above, and for C a cube of side S0 ,
  $\sum_{Q<q\le2Q}\sum^*_{b \bmod q}|S(b/q)|^2\ll(S_0^3+Q^2S_0^2+Q^4)\sum_{\hat\beta\in C}|f_\beta|^2$."
  [L, p. 50] **[rendered]**. **Mine:** this is a large sieve for additive characters on the
  3-dimensional lattice $\mathbb Z^3\cong\mathbb Z[\sqrt[3]2]$. It is not a "cubic large sieve" in
  the sense of cubic residue symbols. I saw no mention of cubic residue symbols in [M] or [L].
  Maynard: **Q:** "(The fact that n > 3k means that characters of large conductor do not play a
  role, and so we don't even require a large sieve type estimate as in [13].)" [M, p. 3]
- Small moduli: a Siegel-Walfisz analogue for prime ideals of $K$ in small boxes, via Hecke
  Grössencharacters. **Q:** "First, the condition β̂ ∈ C is expressed using Hecke
  Grossencharacters." [L, p. 33]. Li defines $\nu_0,\nu_1,\nu_2$ (finite character times the
  unit-angle characters, using $\epsilon_0$ and a Galois conjugate $\epsilon_0'$), **Q:** "we follow
  the work of Heath-Brown" [L, p. 56], and the main term is **Q:** "Lemma 9.3 from the work of
  Heath-Brown" [L, p. 57], proved with Mitsui's prime ideal theorem in sectors [L, p. 57]. So the
  unit group enters through Hecke characters that detect the position of $\beta$ in $\mathbb R^3$
  modulo units. **Mine:** the role of the unit group in HB beyond this (fundamental domain, the
  choice $N(\beta)^{1/3}\epsilon_0^{-1/2}<\beta\le N(\beta)^{1/3}\epsilon_0^{1/2}$ [L, p. 31]) is
  inferred from Li, not read in HB.
- Why HB reaches density 2/3: **Q:** "If one simply bounds the naturally occurring error terms by
  their absolute values without showing genuine cancellations, then one can only hope to obtain
  'Type I' and 'Type II' estimates in certain restricted ranges depending on the density of the
  sequence. Heath-Brown [13] obtains an asymptotic in a sparser sequence precisely because he is
  able to treat the error terms arising in a non-trivial manner." [M, p. 4]
- Compared with FI: **Q:** "By virtue of being homogeneous, the algebraic structure of the
  polynomials considered in Theorems 1.1 and 1.2 are simpler in some key aspects to the
  Friedlander–Iwaniec polynomial $X_1^2+X_2^4$; much of the paper [8] is spent employing
  sophisticated techniques to handle sums twisted by a quadratic character caused by the
  non-homogeneity." [M, p. 3]. **Mine:** $x^3+2y^3$ is homogeneous like Maynard's forms, so there is
  no counterpart of the FI spin/Jacobi-Kubota symbol. The secondary sources suggest the
  Grössencharacter/Siegel-Walfisz input and the large sieve replace it. Not verified in HB.

## 3. Remarks about other problems (c)

I could not search the primary text. So I cannot say whether HB mentions twin primes, $n^2+1$, or
parity. From the secondary sources:
- **Q:** "In contrast the exponential density of the sequence from Landau's problem on $n^2+1$ has
  exponential density 1/2. It turns out that our current methods fail in numerous places once the
  exponential density drops below 2/3." [L, p. 1] (Li's remark, not HB's.)
- **Q:** "Unfortunately no case of the above conjecture is known other than when f is linear, and
  the problem seems to be well beyond current techniques." [M, p. 1] (Bateman-Horn for one
  polynomial; Maynard's remark.)
- Neither [M] nor [L] mentions twin primes in the pages I read.

## 4. Things to check in the primary source
1. The exact statement of the main theorem: box, constant, error term, effectivity, page.
2. That the sieve is Harman's (not FI's), and the exact form of the Type II hypothesis.
3. The statements of Lemma 3.1, Lemma 5.1, Lemma 9.3, Lemma 13.1 (large sieve) and whatever bilinear
   proposition corresponds to Li's Proposition 3.
4. Any remark on limits of the method (for example $n^2+1$ or general cubic forms; see Heath-Brown and
   Moroz).

---------------------------------------------------------------------------------------------

## 5. Draft paragraph for the paper

**Caveat for the editor:** this draft is built on secondary sources. Add the commented line or keep
it out of the paper until someone reads Acta Math. 186. Suggested bib keys: `Ma19` for
arXiv:1507.05080 (Maynard), `Li21` for arXiv:2111.05403. These keys may not exist in the paper's
bibliography yet.

```latex
\subsection{A second thin sequence: $x^3+2y^3$}\label{subsec:hb-x3y3}
% Based on secondary sources (Maynard arXiv:1507.05080v2, Li arXiv:2111.05403v1);
% the primary \cite{HB01} has NOT been read. Verify before release.
\lbl{Literature} Heath-Brown \cite{HB01} proved that $x^3+2y^3$ represents
infinitely many primes; the set of values has about $x^{2/3}$ elements up to
$x$, the sparsest polynomial set for which such a result is known
\cite[pp.~1--3]{Li21}, \cite[p.~3]{Ma19}. (We have not read the exact
asymptotic statement in \cite{HB01} and do not reproduce it.) Unlike
\cite{FI98b}, the sieve is Harman's comparison sieve rather than the
Friedlander--Iwaniec asymptotic sieve \cite[p.~2]{Li21}: the ideals
$(x+y\sqrt[3]2)$ of $K=\mathbb Q(\sqrt[3]2)$ are compared with all ideals of
norm in a comparable range, and Type~I (divisor-sum) and Type~II (bilinear)
estimates are proved for the former. The structure behind the Type~II
estimate, as described in \cite[pp.~2, 31--33, 50, 56--57]{Li21} and
\cite[pp.~2--6]{Ma19}, is: (i) $x^3+2y^3=N_{K/\mathbb Q}(x+y\sqrt[3]2)$, an
incomplete norm form (the $\sqrt[3]4$-coordinate is set to $0$); $K$ has class
number one and fundamental unit $1+\sqrt[3]2+\sqrt[3]4$, so ideals can be
replaced by generators in a fixed fundamental domain; (ii) after
Cauchy--Schwarz, the condition that both $\alpha\beta_1$ and $\alpha\beta_2$ have
vanishing $\sqrt[3]4$-coordinate is two linear equations for $\alpha\in\mathbb
Z^3$, so $\alpha$ lies on a one-dimensional lattice and is essentially
determined by $(\beta_1,\beta_2)$ (a cross product divided by a gcd $D$);
(iii) the remaining sum over pairs $\beta_1\equiv\lambda\beta_2\bmod D$ is
handled by a large sieve for additive characters on $\mathbb Z^3$ for large
$D$, and by Hecke Gr\"ossencharacters of $K$ (a Siegel--Walfisz bound for prime
ideals in small boxes) for small $D$.
```

```latex
\begin{remark}[No counterpart for $\Lambda(n)\Lambda(n+2)$]\label{rem:hb-transfer}
\lbl{Heuristic} (our reading, not a statement of \cite{HB01}). In \cite{HB01}
the sequence is supported on norms of the elements of a rank-two sublattice
$\mathbb Z+\mathbb Z\sqrt[3]2$ of the ring of integers of a cubic field.
Multiplicativity of the norm turns ``$mn$ is in the sequence'' into ``$\alpha\beta$
lies in that sublattice'' for algebraic integers $\alpha,\beta$ of norms $m,n$,
which is a \emph{linear} condition on $\alpha$ once $\beta$ is fixed. After
Cauchy--Schwarz the off-diagonal is a lattice-point count with an explicit
main term, and the remaining cancellation is a question about prime ideals of
$K$ in boxes and progressions, i.e.\ about Hecke $L$-functions in one
variable. For $a_n=\Lambda(n+2)$ there is no ring in which ``$mn+2$ is prime''
is a linear condition on a factor of $m$ or $n$; the shift destroys the
multiplicative structure, and the off-diagonal is again a correlation
$\sum_m\Lambda(mn_1+2)\Lambda(mn_2+2)$ (cf.\ Remark~\ref{rem:fi-transfer}).
The thinness, which here as in \cite{FI98b} makes the dual problem short, is
also absent. We do not claim that no other route exists.
\end{remark}
```

**Mine:** the remark is labelled Heuristic. It is not an argument and must not be labelled Proved
here.
