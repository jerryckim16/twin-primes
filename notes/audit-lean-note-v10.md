# Referee audit: papers/lean-reduction/main.tex (v1.0, "The finite part of Maynard's reduction ... in core Lean")

Checked against lean/TwinPrimes/*.lean (Reduction, MaynardS1, MaynardHpw, MaynardInv, MuMult,
MaynardDiag, MaynardS1Diag, MuTuple, Tuples, Basic), a fresh `lake build` (Lean 4.35.0, 24 jobs, OK),
`lake env lean Audit.lean`, and the text of arXiv:1311.4600v3 (SHA-256 of the PDF verified:
dce1a7a0...5050d63cda9, matches the bibliography).

What is right (no action): every Lean name cited in the note exists, is in Audit.lean, and depends
only on propext / Quot.sound / Classical.choice. The axiom counts are exact: 208 declarations;
116 {propext, Classical.choice, Quot.sound}; 53 {propext, Quot.sound}; 11 {propext}; 28 none; no
sorryAx. 21 files, 5720 lines, the subtotal 2543 are right (but see item 1). No `sorry`,
`native_decide` or `axiom` in TwinPrimes/. Theorem 1 (1)-(5) match Reduction.lean exactly
(including a=p+4q, b=4p and m=2ac'+2). Maynard (4.2)-(4.3), Prop. 4.1, Prop. 4.2 (pp. 5-6 of
arXiv v3), Lemma 5.1, (5.2), Lemma 5.2 (error O(y_max^2 N/(log N)^A)), Lemmas 6.2, 6.3 are cited for
what they contain. Lean's `maynardY` uses prod_i mu(u_i) (`tmu`), which matches Maynard's Lemma 5.1
exactly (Lemma 5.1 writes prod_i mu(r_i)phi(r_i)), so line 164 is correct. The Polymath8b sentence
(l. 249-252) matches the abstract.

## Findings

1. **error** (l. 261) "the six `Maynard*` files": there are five (MaynardDiag, MaynardHpw,
   MaynardInv, MaynardS1, MaynardS1Diag). 202+244+369+778+283+208+352+107 = 2543 with five.
   Fix: "the five \tl{Maynard*} files".

2. **error** (l. 208-209, Hypothesis 7) Wrong normalisation of B. In Theorem 6(4) B enters as
   (N/W)B, and B itself is dimensionless (B = 2/9 in `ex_B_eq`). "B = o(phi(W)^k N (log R)^k/W^{k+1})"
   is weaker by a factor N/W than what is needed. Fix: "$\sum_{d,e}|\lambda_d\lambda_e|$ and
   $\frac NW B$ are $o(\varphi(W)^kN(\log R)^k/W^{k+1})$ (\lbl{Literature}, \cite[(5.3), (5.9) and the
   $s_{i,j}\ne1$ terms in the proof of Lemma~5.1]{May15})". (For the record: B is exactly minus the
   $s_{i,j}\neq1$ part of (5.6). Maynard bounds that part by $O(y_{\max}^2\varphi(W)^kN(\log R)^k/(W^{k+1}D_0))$,
   so the corrected statement is the one the literature gives.)

3. **gap** (l. 146-148, 149, 179, and the abstract l. 41-42) The hypothesis `ShiftsDvd hs W`,
   i.e. $|h_i-h_j|\mid W$, can never hold for Maynard's $W=\prod_{p\le D_0}p$ once some difference
   has a square factor, because that W is squarefree. In the 50-tuple of `narrow50` the difference
   12-0=12 already fails, and so do 20, 32, 44, etc. So Theorem 5(3)-(4) and Theorem 6(4) as checked do
   not apply to Maynard's setting for k=50 (or for any tuple with a difference divisible by 4 or 9).
   The proof only needs "every prime factor of $h_i-h_j$ divides W". It shows that gcd(x,y) divides
   $h_i-h_j$ and is coprime to W.
   Fix (Lean): weaken `ShiftsDvd` to
   `hs.Pairwise fun a b => ∀ x, Nat.gcd x W = 1 → Nat.Coprime x ((a:Int)-(b:Int)).natAbs`
   (the proof of `coprime_of_dvd_shift` adapts in a few lines). Fix (paper, if Lean is not changed):
   in (3) add "This hypothesis is stronger than Maynard's (he needs only that the primes dividing
   $h_i-h_j$ divide $W$). For squarefree $W$ it fails as soon as some $h_i-h_j$ has a square factor,
   so as stated (3), (4) and Theorem~\ref{thm:diag}(4) need $W$ replaced by a multiple of all
   $|h_i-h_j|$."

4. **gap** (l. 133, 161-186, 213-218, 237-239) Integer weights. `maynard_S1_error_W` and
   `maynard_S1_diag_W` take `lam : List Nat → Int`; (1)-(3) of Theorem 6 take `Rat`. Maynard's
   λ built from a smooth F are real. The note never says how its integer- or rational-valued
   theorems reach real λ (scaling handles rationals because S1 is quadratic, but real λ need
   approximation). The integrality is also needed because Theorem 1(4) wants `w : Nat → Nat`.
   Fix: in Hypothesis 8 and in the closing paragraph (l. 237) add "with $\lambda$ replaced by
   rational (hence, after scaling, integer) weights, at a cost absorbed in the error terms; this is
   not formalised".

5. **overstatement** (l. 237-241) "Granting Hypotheses 7-10, with real constants replaced by
   rationals ..., the hypothesis of Theorem 1(5) holds". Finite glue that is neither formalised nor
   listed among the hypotheses is also needed:
   (a) Lean's S1 runs over n<N with `n % W = v0`. Maynard's range is a difference of two such sums,
   which doubles the error, and this is not in Lean.
   (b) The Int/Rat S1 of Section 3 has to be converted into `wsum w (fun _ => 1) ns` with Nat w and
   a Nat B(N) (floor of the normalisation).
   (c) Item 3 (W) and item 4 (integer λ).
   The abstract's "lists precisely the analytic statements that stay hypotheses" (l. 34-35) is
   accurate only for analytic statements. Fix: add a fifth item to Section 4, "Hypothesis (glue). The
   translation of Theorems 5-6 into the form of Theorem 1(4): range $N\le n<2N$, integer weights,
   Nat normalisation $B(N)$, and the choice of $W$", and say "Granting Hypotheses 7-11".

6. **overstatement** (l. 76-77) "In core Lean they appear only as hypotheses of theorems". The
   analytic statements of Section 4 (I_k, J_k, y_max, Bombieri-Vinogradov) are not stated in Lean at
   all. Only the abstract two-sided bound (`hfam` of `sieveInequality_of_asymptotics`) appears as a
   hypothesis. Fix: "In Lean only their abstract consequence, the two-sided bound in
   Theorem~\ref{thm:skeleton}(4), appears, as a hypothesis; none is stated or assumed as an axiom."

7. **overstatement** (l. 45 vs l. 80-83) The abstract says the other formalisation "exists". The body
   says "has been announced" and that its code was not inspected. Fix (l. 45): "A Mathlib
   formalisation of $H_1\le246$ by another group has been announced".

8. **slip** (l. 138-141) "(no hypotheses)" is true, but Lean's condition is `n % W = v0`, not
   n ≡ v0 (mod W). The two differ when v0 ≥ W: Lean's sum is then empty. Fix: write
   "$n\bmod W=v_0$" or add "($v_0<W$ in all later items)".

9. **slip** (l. 143-145) `crt_tuple_count_bounds` also assumes v0<W, all L_i>0, and |L| = |h|.
   `tupleDvd_lcm` assumes |d| = |e| = |h|. Lean's conclusion is the division-free pair
   N < WP(c+1), WPc < N+WP. Fix: "if $v_0<W$, the $L_i\ge1$ (one per shift) are pairwise coprime
   and coprime to $W$, then $|c-N/(W\prod L_i)|<1$ (in the division-free form $N<WP(c+1)$,
   $WPc<N+WP$)".

10. **slip** (l. 149-154) `maynard_S1_error_W` is stated division-free: it takes a common multiple
    M of all prod_i[d_i,e_i] and bounds |WM·S1 − N Σ_good λλ M/∏[d_i,e_i]| ≤ WM Σ|λλ|. It also
    assumes v0<W, positive entries and length k. The displayed rational inequality is what
    `maynard_S1_diag_W` proves internally. Fix: "\tl{maynard\_S1\_error\_W} (division-free, with an
    auxiliary common multiple $M$ of the $\prod_i[d_i,e_i]$), under (3) and $v_0<W$, entries
    $\ge1$:" and keep the display "after division by $WM$".

11. **slip** (l. 158-159) Maynard's Σ' requires $W,[d_1,e_1],\dots,[d_k,e_k]$ to be pairwise
    coprime. Lean's `goodPair` drops W. The two agree only because the entries are coprime to W
    (hDW). Fix: "Maynard's restricted sum $\sum'$ is our sum over good pairs (they agree since the
    entries are coprime to $W$)."

12. **slip** (l. 169-172) "the formula ... and its inverse": `maynard_y_of_lam_sqfree_all`
    assumes that **y** (not λ) is supported on squarefree-entry tuples, and both hold only at
    points of the box. Fix: "... hold for every $R$, $k$ and every $d$ in the box; conversely, for
    every $y$ supported on tuples with squarefree entries, $y$ is recovered from the $\lambda$ so
    defined."

13. **slip** (l. 161-163) The theorem's files list omits MaynardHpw.lean (`maynard_S1_diag_W` lives
    there). Item (4) also takes λ integer-valued while (1)-(3) are over ℚ. Fix: add
    \tl{MaynardHpw.lean} to the header. In (4) add "for integer-valued $\lambda$, supported on
    $D_k=$ (box filtered by a predicate), with $\lambda=0$ elsewhere in the box, $v_0<W$, $|h|=k$".

14. **slip** (l. 192-193) `box_hpw_fails` is only the case R=k=2, d=e=(2,2) in {1,2}^2. Fix: "on
    the full box $\{1,2\}^2$ the pair $d=e=(2,2)$ fails it (\tl{box\_hpw\_fails}; the same pair
    works for all $R,k\ge2$, not formalised)".

15. **slip** (l. 123-124) In Maynard's normalisation $B(N)=\varphi(W)^kN(\log R)^k/W^{k+1}$,
    $S_2\sim(\log R/\log N)\sum_mJ_k^{(m)}(F)\,B=(\theta/2-\delta)\sum_mJ^{(m)}_k(F)\,B$. Fix:
    "$a/a'$ and $c/c'$ are rational upper and lower bounds for $I_k(F)$ and
    $(\theta/2-\delta)\sum_mJ^{(m)}_k(F)$", with $B(N)$ the normalisation above.

16. **slip** (l. 91) "All objects are natural numbers or finite lists" is true for Section 2 only.
    Section 3 uses ℤ and ℚ. Fix: "In this section all objects are ...".

17. **slip** (l. 68) "pp. 5-6" are arXiv v3 page numbers. The Annals pagination (383-413) differs.
    Fix: "\cite[pp.~5--6 of arXiv v3]{May15}".

18. **style / mild overstatement** (l. 247-252) Theorem 1(1) holds for arbitrary weights, and
    `SieveInequality 2` is trivially equivalent to `DHL 2` (put all weight on a twin). So "the route
    of Theorem 1" adds nothing for k=2. The obstruction lies in the sieve weights. Even before parity
    enters, Maynard's criterion $\theta M_2/2>1$ fails for every $\theta\le1$ because $M_2<2$. Fix: "For $k=2$ \tl{SieveInequality 2} is equivalent to \tl{DHL 2}, so the
    reduction gives nothing. With Maynard-Selberg weights the criterion fails ($M_2<2$), and the
    parity barrier rules out sieve-theoretic routes in general: Polymath8b show ... that DHL[3,2]
    under GEH ($H_1\le6$) is the best possible ...". The Polymath8b paraphrase itself is accurate;
    "their $k=3$ result" should name DHL[3,2].

19. **style** (l. 252-253) "the project's parity-barrier paper" has no citation. Fix: add a
    bibitem with URL/version, or drop it.

20. **style** (l. 233-234) "Our main paper re-certifies this inequality exactly (Computed)" cannot
    be checked from this note. Fix: give a pointer (section/file of the main paper, or the
    certificate's path in the repo).

21. **style** (l. 281-283) The Axiom26 author list "R. Aanegola, ..., J. Thorner, ..." could not
    be verified here. Fix: check it against the site, or cite as "Axiom Math team".

22. **style (readability)** The same letter does several jobs: N is the naturals, the range bound
    and `ns ⊂ [N,∞)`; B is the normalisation in Theorem 1(4) and the bad-pair sum in Theorem 6(4);
    h is a shift tuple and an element of H. Fix: rename the bad-pair sum to $B_{\rm bad}$ (also in
    Hypothesis 7 and the Remark) and write $\mathbb N$ only for the set.

23. **style (Lean docs, not the paper)** These docstrings are stale and contradict the note:
    MaynardInv.lean l. 6-8 and l. 547-550 say Maynard's y uses μ(∏r_i), but Lemma 5.1 uses
    ∏μ(r_i), which is what the code does. MaynardS1.lean l. 36-41 and MaynardS1Diag.lean l. 19-22
    still say the bad-pair argument is "NOT formalised", but MaynardHpw.lean now does it. Fix the
    docstrings so a reader following the note to the code is not misled.
