# Referee audit: parity-barrier paper v0.2 (new parts only)

Scope: papers/parity-barrier/main.tex, Section sec:bip (l.227-405), subsec:fi-x2y4 + rem:fi-transfer
(l.549-611), open questions 1-2 (l.646-667). Line numbers are those of the working-tree file as of the
audit (the file was edited concurrently: HMBOUNDS at l.372 was filled in while the audit ran).
Classes: ERROR / GAP (fixable) / WORDING / FINE.

Checks run: `lake build` (succeeds; no sorry/axiom in Parity.lean or Basic.lean);
`python3 code/parity/bipartite_obstruction.py` (rc 0; it overwrites the committed JSON, which I then
restored byte-for-byte); an independent script for the Remark 8.1 variants
(scratchpad chk81.py, n < 20000).

## A. Section sec:bip

1. **ERROR (l.351-352, Cor. cor:six).** "the class ... blocks no attempt at $H_1\le 6$" is too strong.
   The corollary shows only that *not every* admissible tuple is blocked at $g=6$. Some tuples are
   blocked at $g=6$: for $\{0,2,8,12\}$ (admissible mod 2 and mod 3) every closed window of length 6 holds
   at most 2 elements, so (c) gives a fair weight that kills the $g=6$ target. Fix: "does not block every
   attempt at $H_1\le6$; in particular it does not block the one through $\{0,2,6\}$ (the target graph at
   $g=6$ is a triangle)". The same applies at l.372, "forbids exactly $H_2<12$, $H_3<20$": say "forbids
   (for every tuple) exactly the attempts at $H_2\le 10$, $H_3\le 18$, and no smaller $g$ is blocked for
   all tuples". The equivalence in the corollary itself ("blocked for every admissible tuple iff
   $g<H(2m+1)$") is correct.

2. **ERROR (citation, l.270).** "\cite[p.~70, after (147)]" for the weight
   $(1-\lambda(n)\lambda(n+2))(1-\lambda(n+2)\lambda(n+6))$ is wrong. In arXiv v4 the "Page N of 80" lines
   are page *headers* (page 2's header comes after the abstract). The weight, (147) and (148) are all on
   **p.69**. Remark 8.1, "conclude (heuristically, at least) ..." and "essentially due to Selberg" are on
   p.70 (correct). The bilinear sentence and the FI citation run over pp.70-71 (p.71 as cited is
   acceptable). §8 is on pp.68-71 (correct).

3. **GAP (l.381-403 vs. Remark rem:marg l.341-343).** The Remark 8.1 weights, both printed and
   corrected, depend on $n \bmod 3$ (resp. $\bmod 6$) through the coprimality conditions. They are
   therefore *not* pattern weights in the sense of l.243-246, and rem:marg explicitly says that such
   weights "are not covered". So "In the language of Proposition prop:bipartite, the printed graph has odd
   cycles" (l.397) needs a bridging sentence. Fix: "restricted to a fixed class $n\equiv r \pmod 6$ (as the
   $W$-trick does anyway), the weight is a pattern weight on the fixed set of positions $i\in[0,H]$ with
   $(r+i,6)=1$ (resp. $(r+i,3)=1$), and the target is $\{$pairs at distance $\le4\}$." Then also state
   that the corrected product over a path is **fair**. That is easy: it is supported on the two
   alternating sign patterns, with equal mass. Right now l.399-403 show only that it vanishes on the
   target and is not identically zero, not that it is fair, and fairness is the property that matters.

4. **GAP (l.392, "Computed for $n<2000$").** The script cited for the section
   (bipartite_obstruction.py) computes only (i) the printed weight *including* $i=i'$, where the count 0
   is trivial, and (ii) the corrected weight. It never computes the $i<i'$, mod-3-only variant, and it
   has no $n<2000$ run. I reproduced the claim independently: for $i<i'$ with the mod-3 condition,
   $\omega\equiv0$ for all $n<20000$ at $H=4,6,8,12$, while at $H=3$ it is non-zero for 3342 values of
   $n$ (so "$H\ge4$" is sharp). Fix: add this variant to the script, or drop the Computed tag (the Proved
   argument suffices).
   *Triangle argument re-derived:* among $n,\dots,n+4$, the integers prime to 3 contain $\{n+1,n+2,n+4\}$
   if $n\equiv0$, $\{n,n+1,n+3\}$ if $n\equiv1$ and $\{n,n+2,n+3\}$ if $n\equiv2 \pmod 3$. Each has
   pairwise distances $\le4$. On a triangle, three non-zero factors would need $ab=bc=ca=-1$, whose product
   is $(abc)^2=-1$, which is impossible. So the claim is correct. "Identically zero as printed (factor
   $i=i'$)" holds for every integer $H\ge1$. The criticism is fair, correct and appropriately labelled a
   typo-level slip. The corrected graph (positions $\equiv\pm1 \pmod 6$, gaps 4,2,4,...) is a path
   (correct). The exceptions $n=1,2$ at $H=4$ are confirmed and involve the prime 3 (and 2). "vanishes
   whenever two primes $>3$ at distance $\le4$ lie in $[n,n+H]$" is in fact provable (such a pair is an
   edge), so it could be tagged Proved rather than only Computed.

5. **GAP (minor) (l.259).** "$\lambda(n+h_i)=-1$ on the support" of $\Lambda$ is false at even prime
   powers ($\lambda(p^2)=+1$). Fix: "on primes; prime powers contribute negligibly".

6. **GAP (minor) (l.264-268, weakly fair).** For a weakly fair weight the $S=\{i\}$ term is
   $-\widehat\Omega(\{i\})\sum\nu f\lambda(n+h_i)$. Its effect is the claimed one only for $f=\Lambda$
   (and $f=1$). For GEH-type $f=\alpha\star\beta$ the twist $f\lambda$ has a different main term, so "the
   prime sums only grow" is not a statement about all the inputs (142)-(143). For *fair* weights there is
   no issue, since only $S=\emptyset$ survives for every $f$. This is harmless because (2)⇒(1), but
   either say so ("by (2)⇔(1) we may always use fair weights") or restrict the sentence to $f=\Lambda$.
   Also, "does not hurt an argument that needs lower bounds for them" should say "*only* lower bounds".

7. **GAP (edge case) (l.322-325, part (b)).** The witness "uniformly random $m$-subset with probability
   $k/(2m)$" does not exist for $k<m$, and divides by 0 for $m=0$. Fix: assume $m\ge1$. If $k\le m$ then
   $\mathcal E=\emptyset$; take $I=\{1..k\}$ with probability 1/2. The statement stays true.

8. **WORDING (l.296-297, part (c)).** Say "closed interval $[a,a+g]$" so that it matches
   $\max-\min\le g$ at the boundary. The proof is then correct in both directions: forward via
   $J$ = indices in the window, any $m+1$ of which form an $e$; converse via odd/even indices, at most $m$
   of each among $\le 2m$ consecutive indices. Corollary proof (l.359-366): correct, including "subsets of
   admissible tuples are admissible" and the $H(3)=6$ argument.

9. **FINE (main proposition, l.281-334).** $\widehat\Omega(\{i\})=2^{-k}(\sum\Omega)(1-2\mu(i\in I))$
   is correct. Kills ⇔ supported on $\mathcal E$-free sets, (1)⇔(3), and (2)⇒(1) by independent deletion
   with probability $1-1/(2p_i)\in[0,1/2]$ are all correct. (a): isolated vertices are fine; the
   odd-cycle bound $\sum_C x_i\le r<(2r+1)/2$ is correct. The "iff" is honestly scoped: it is an
   equivalence of three properties of the stated class, and l.234-237 say so. Remark rem:marg: averaging
   keeps non-negativity, killing and the singleton coefficients (the normalisation check gives
   $\widehat{\Omega'}(\{i\})=\widehat\Omega(\{i\})$). Correct.
   The heuristic main-term display (l.261-262) is correct: $S=\emptyset$ gives $\widehat\Omega(\emptyset)$,
   $S=\{i\}$ gives $-\widehat\Omega(\{i\})$, and the other $S$ are negligible by Möbius randomness.

10. **WORDING (l.231-232).** "It explains why the parity limit of the method is 6" is acceptable, but it
    would be more accurate to say "why this class of obstructions stops at 6".

11. **FINE / LITERATURE.** Condition (3) says that the hypergraph $\mathcal E$ has fractional chromatic
    number $\le 2$, i.e. $\tfrac12\mathbf 1$ lies in the convex hull of $\mathcal E$-free (independent)
    sets. For graphs, "$\tfrac12\mathbf 1\in\mathrm{STAB}(G)$ iff $G$ bipartite" is a standard
    polyhedral-combinatorics fact (odd-cycle inequalities). Suggest noting this, so that "possibly
    folklore" points somewhere concrete for the combinatorics. I know of no source for the sieve
    application to general targets / $H_m$ beyond Polymath8b §8 and Remark 8.1 (only $m=1$). I do not
    claim there is none.

12. **FINE.** $H(3..9)=6,8,12,16,20,26,30$ is correct (matches known values; the script reproduces it).
    Theorem 1.4(xii) is $H_1\le6$ under GEH, deduced from DHL[3,2] (p.68, and Theorem 3.2(xii)). The
    newly inserted "$H_2\le270$ under EH, $\le252$ under GEH, Theorem 1.4(vii),(xiii)" is verbatim
    correct. DHL[3,2] is not blocked by (b) since $3>2$ (correct).

13. **Lean (Parity.lean): FINE, one WORDING point.** `triangle_no_fair_weight` concludes
    `patSum w = 0`, not pointwise vanishing. With `hnn` the two are equivalent, but the paper's
    "identically zero" (l.378-379) is not literally the Lean statement. Either add a one-line corollary
    or say "has total mass zero (hence, being non-negative, is zero)". The kill hypotheses are exactly the
    four patterns with $\ge2$ minus signs, and fairness is the three singleton sums (correct). `hnn` is
    quantified over all `Int` (stronger than needed, harmless). `pm8b_path_weight_*` say what l.273-275
    say. `narrow5/7_admissible` are correct, and l.368-371 correctly call minimality Computed and only
    admissibility Lean-checked. The "rational/real reduce to integer" remark (l.379-380) is correct (a
    rational polyhedral cone; Lean's `omega` argument is linear anyway).

14. **Code hygiene (WORDING).** The docstring of bipartite_obstruction.py claims an "exact rational LP ...
    exact rational witness / odd-cycle certificate" and a part (4) "window version". The code uses
    floating HiGHS `linprog` only, and (4) is not implemented. Fix the docstring. The committed JSON is
    stale: it has `"2": [0,[0,0]]`, while the current code gives `[2,[0,2]]`. Regenerate it.

## B. FI $a^2+b^4$ (l.549-611)

Page check: printed page = PDF page + 944, cross-checked with running heads.
- Theorem 1 p.946, formula, $\kappa$, positive $a,b$: correct. Not effective, p.1012 (l.3542 of the
  text): correct.
- "In its classical format ... parity problem": verbatim, **p.947**. "we introduce (see (2.11)) an
  additional axiom which overcomes the parity problem": verbatim, **p.947** (the 948 header follows the
  word "we are"). **WORDING (l.561):** "pp.~947--948" should be "p.~947".
- $a_n$ via $a^2+c^4=n$: p.962 (correct). Prop. 3.5 p.962 with $D=x^{3/4-5\varepsilon}$: correct. Prop. 4.1
  p.963, range $x^{1/4+\eta}<N<x^{1/2}(\log x)^{-B}$, bound $A(x)(\log x)^{4-A}$, $1\le C\le N^{1-\eta}$:
  correct. **WORDING (l.564-570):** $\beta(n)=\mu(n)\sum_{c|n,c\le C}\mu(c)$ is their **(2.12)**, not
  (4.3)-(4.4). (4.3) is $B(x;N)$ and (4.4) is the range of $P$. In §4 $\Pi$ is over $p\le P$ (in §2,
  $p<P$). Also add "$B=B(\eta,A)$".
- $Z$: p.960 (correct). (5.2) with the factor $\tfrac14$: p.967 (correct). Lemma 17.1 p.1013, Prop. 17.2
  p.1016, Theorem 2 p.948: correct. "fails however to produce primes ... non-homogeneous quadratic
  polynomial": verbatim, p.947 (correct).
- **WORDING (l.599): quotation not verbatim.** FI write "we **release** that part of the multiplicity
  which is accommodated in the outer variable" (p.966). The paper quotes "released". Quote the phrase
  exactly, or drop the quotation marks.
- **WORDING (l.588-589).** "The paper says nothing about twin primes or linear forms" is literally
  false. FI §22 is "Linear forms in Jacobi-Kubota symbols", and p.946 mentions linear polynomials
  (Dirichlet). Say "nothing about twin primes or about primes represented by pairs of linear forms".
- **WORDING (rem:fi-transfer, l.597-605).** "a lattice-point problem in which the primality is no longer
  present" suggests that FI lose primality at that step. In fact their $a_n$ never carries primality:
  the primes enter only through $\beta$. Suggest "the sequence $a_n$ carries no prime-detecting factor,
  so the off-diagonal is a pure lattice-point count". Also, "the thinness ... makes the Type I level
  $x^{3/4}$ attainable" attributes to thinness what FI credit to a Davenport-Halberstam deduction for
  this special form (p.947). Since the remark is labelled Heuristic this is acceptable, but soften it to
  "the Type I level $D\approx A(x)$, which FI obtain from [FI] via Davenport-Halberstam". The Polymath8b
  quotes at l.606-609 are verbatim and on p.71 (correct).

## C. Open questions (l.646-667)

- **TT25 Theorem 3.1** is on p.24 (correct). The summary is correct: 1-bounded multiplicative $g_1,g_2$,
  $W\in[L^c]$, $b,h_1,h_2=O(L^c)$, $1\le L\le\log X$, an exceptional set $E\subset[\sqrt X,X]$ of log
  density $\ll L^{-c}$ chosen *before* $W,b,h$. Missing: the theorem requires case (i) or (ii); for
  $\lambda$ it is (ii), via (3.3). "Remarks 3.2" is the correct title, and the special case there is
  exactly $\lambda$ with $L$ a power of $\log N$.
- **GAP (l.657-659).** "it should allow levels $R=(\log x)^{c_0}$" does not follow by the route of
  Prop. prop:tao-weight. That proof uses periodicity mod $\mathrm{lcm}(d\le R)\approx e^{R}$, which only
  gives $W\le L^c$, i.e. $R\asymp\log\log x$. To reach $R=(\log x)^{c_0}$ one must expand the square
  $w=\sum_{d_1,d_2}\lambda_{d_1}\lambda_{d_2}1_{[d_1,d_2]\mid n(n+2)}$ and apply TT25 with
  $W=[d_1,d_2]\le R^2$ on the $\rho([d_1,d_2])$ classes. The error is
  $\ll N L^{-c}\sum|\lambda_{d_1}\lambda_{d_2}|\rho([d_1,d_2])/[d_1,d_2]$, which is acceptable for
  bounded $\lambda_d$ and small $c_0$. One must also pass from dyadic natural averages outside $E$ to log
  averages. Say this explicitly. "We have not checked" is present, which is good.
- **WORDING (l.664-667).** "block a non-bipartite target, for instance DHL[5,3]": the DHL[5,3] target is
  a 3-uniform hypergraph, so "non-bipartite" is undefined for it. Say "a target for which (1)-(3) fail".
  "DHL[5,3], i.e. $H_2\le12$" should read "DHL[5,3] (for $\{0,2,6,8,12\}$; it implies $H_2\le12$)". It
  is not an equivalence. The question itself is reasonable and correctly states that (b) does not block
  it ($5>4$).

## Placeholders
- l.721 `AUDITNOTE` is still a literal token in the changelog. (`HMBOUNDS`, l.372, has been filled in.)
