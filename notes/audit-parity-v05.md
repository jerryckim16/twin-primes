# Audit of parity-barrier paper v0.5 (new parts only)

Fresh-context adversarial referee, 15 Nov 2026. File audited: papers/parity-barrier/main.tex (working tree,
uncommitted diff on top of a942738). I did not edit main.tex. Sources: /tmp/claude-0/ss/ss.txt (SHA-256 of ss.pdf
re-checked: 5b762a08...0687), /tmp/claude-0/li21/li.txt, /tmp/claude-0/c25/c.txt. Page numbers come from
form-feed counts in the pdftotext output.

Severity: **error** = false statement or broken build; **gap** = missing justification or misleading omission;
**wording** = imprecise but harmless.

## Issues

1. **error (build)**: thebibliography (l. 1064-1084). `SS19`, `Li21`, `MV17` and `Cit26` are cited in sec:ss
   and rem:ss-transfer, but none has a \bibitem. They will print as [?]. Fix: add
   - SS19: W. Sawin, M. Shusterman, *On the Chowla and twin primes conjectures over F_q[T]*, arXiv:1808.04001v2 (7 Sep 2019), cited by its page numbers.
   - Li21: J. D. Lichtman, *Averages of the Möbius function on shifted primes*, arXiv:2009.08969v2 (20 Oct 2021).
   - Cit26: M. Cantarini, *Averages of diagonal Elliott-Halberstam problem twisted by Möbius function with Sobolev and Hölder-Zygmund weights*, arXiv:2607.09110v1 (10 Jul 2026).
   - MV17: M. R. Murty, A. Vatwani, 2017, marked "not consulted; quoted from Cit26".
2. **error (citation)**: rem:ss-transfer, bullet 2, "\cite[Theorem~3, p.~2]{Cit26}". Theorem 3 of Cantarini is
   on **p. 3**. Conjecture 2 (EHμ_h) is on p. 2. Fix: "Theorem 3, p. 3" (it is MV17's Theorem 1.1 there).
3. **gap (honesty)**: in the abstract the v0.5 diff deletes "(whose proof we have not checked)" after the
   Tao-Teräväinen preprint, and also "(from Tao's two-point theorem)". Neither deletion is mentioned anywhere.
   "Unrefereed" remains, but the paper's own standard is to say the proof was not checked. Fix: restore
   "(whose proof we have not checked)".
4. **gap**: rem:ss-transfer, bullet 1, on strength. The e=1 term Σ_p μ(p−2) log p log(p−2) has trivial size
   ≍ x log x, and the proposition needs T_D(x)=o(x), a saving of more than a full logarithm. By partial
   summation, the folklore conjecture Σ_{p≤X} μ(p+h)=o(π(X)) only gives o(x log x) for this term. So even the
   folklore conjecture would not settle the e=1 term. Placing it next to the conjecture invites the opposite
   reading. Fix: add "(the needed bound o(x) is stronger than this conjecture by more than a factor log x)".
5. **wording**: rem:ss-transfer, bullet 1. Lichtman states the conjecture "for any fixed shift h > 0" (p. 1,
   both in the abstract and the introduction), not h≠0. The term here has shift −2. His Theorem 1.1 also assumes
   H < X. Fix: "for fixed h>0 (the shift −2 needed here is the same kind of statement)", and add "H<X".
6. **gap/wording**: prop:ss-split heading says "essentially contained in \cite{MV17} as quoted in \cite{Cit26}",
   and bullet 2 says MV states "the same equivalence". As quoted (Cit26, Thm 3), MV assume EH at level
   N^θ(log N)^C **and** EHμ_h at level N^{1−θ}. Their condition is Σ_{n≤N} Λ(n)μ(n+h)=o(N), which is a different
   quantity from T_D(x), and their form is conditional. The proposition here is unconditional at
   D=x^{1/2}(log x)^{-B}. Cit26 does not show MV's proof, so "essentially contained" cannot be checked. Fix:
   "a related equivalence (MV17, Thm 1.1, as quoted in Cit26, Thm 3; MV17 not consulted)". Say also that the
   two hypotheses sit at the complementary levels θ and 1−θ.
7. **wording**: sec:ss, step 4, second bullet: "once q is large compared with p^2 (Section 2; Corollary 2.7)".
   Corollary 2.7 (p. 13) needs only q ≥ (e/η)^{2/(1−2β)}, with no p. The p^2 enters in Theorem 4.5 (4.33),
   because Lemma 3.2 shortens the sums by the factor p. Fix: "…from vanishing cycles and Deligne's theorem
   (Section 2; Corollary 2.7, p. 13). Through Lemma 3.2 this needs q large compared with p^2 (Theorem 4.5, (4.33))".
8. **wording**: step 1: "(6.19)-(6.22), pp. 30-31". All four displays are on p. 30. The split continues to
   (6.26) on pp. 30-31. Fix: "(6.19)-(6.26), pp. 30-31" or "(6.19)-(6.22), p. 30".
9. **wording**: sec:ss, "their Remark 1.6, p. 5, contrasts it with that regime". Remark 1.6 describes the
   large-finite-field limit and says their methods "likely give an improved savings" there. It does not
   explicitly contrast. Fix: "(their Remark 1.6, p. 5, discusses that regime separately)".
10. **wording**: rem:ss-transfer, bullet 3: "T_D is exactly what Cor 6.1 bounds". The F_q[T] analogue of T_D is
    (6.22), and SS bound it by applying Cor 6.1 (n=1) to each innermost sum (p. 30). Fix: "the analogue of T_D is
    (6.22), which SS bound by applying Corollary 6.1 to each innermost sum".
11. **wording**: rem:ss-transfer, bullet 4 cites "Proposition B-parity(3)". The parity content (no cancellation
    for a^+) is in items (1)-(2). Item (3) is the reduction to (OD). Fix: "(1)-(2)".
12. **wording**: prop:ss-split, last sentence: "under the Elliott-Halberstam conjecture for the residue class 2".
    Make it precise: "if (EH_D) holds for D=x^θ (that is, EH with absolute values for the fixed residue 2 and odd
    moduli)". Also, the O_A in the main formula depends on c too: write O_{A,c}.
13. **wording**: cor:maynard-logc. (a) x_0 is not introduced: say "there is an absolute x_0". (b) "e" means
    both e_1,e_2 and e=[A,B]: rename the second pair (d_1',d_2'). (c) Open question 5 says "Maynard's
    two-variable weights". Maynard's actual λ are not normalized to |λ|≤1=λ_{1,1}. The inequality is homogeneous,
    so max|λ| ≤ M|λ_{1,1}| costs a factor M^2. Say that, or say "weights of Maynard's two-variable form".
14. **wording (honesty)**: open question 5, and the corollary, have no sentence like the one in
    rem:tao-weight-logc. Add: "this, too, confirms the input of the obstruction and gives no lower bound for twin
    primes; the proof of [TT25, Thm 3.1] was not checked."
15. **wording**: the date says Version 0.5, but the changelog has no 0.5 entry for sec:ss, cor:maynard-logc or
    this audit. Add one.

## Checked and found correct

- **Corollary cor:maynard-logc**
  - Expansion of the square: correct.
  - CRT step: A|n, B|n+2 means n≡0 (A), n≡−2 (B). This is solvable iff (A,B)|2, and then there is exactly one
    class mod [A,B]. Correct.
  - e=[A,B] ≤ AB ≤ R^4 ≤ (log x)^{c/8} = (log x)^{κ/2} with κ=c/4. This is the range where the one-class bound
    |S(e,c;x)| ≪ (log x)^{1−κ/2}/e + 1 is proved, and that bound holds for every residue. Correct.
  - Error-term count: there are ≤ R^4 quadruples, so the term is R^4. Correct.
  - g is multiplicative with g(p^a)=(a+1)^4−a^4 ≤ 4(a+1)^3, so g(p)=15. The Euler product over p≤R
    (all primes of e are ≤ R; the a≥2 terms are O(p^{-2})) gives ≪ (log R+1)^15. Correct.
  - Main term: d_1|n with n odd and coprime to the primes in [3,R] forces d_1=1, and the same for n+2. So
    w=λ_{1,1}^2=1, w≥0, and the δ_R argument carries over. Correct.
  - Exponents: the ratio is ≪ (log R+1)^{17}(log x)^{−κ/2} + R^4(log R+1)^2/log x
    ≤ (log x)^{−κ/2+o(1)} + (log x)^{κ/2−1+o(1)} ≤ (log x)^{−κ/8}, since 5κ/8<1. Correct, and κ/8=c/32.
    (Exponent κ/4 would also follow. c/32 is safe.)
- **Section sec:ss, (a) Literature**, all verified in ss.txt:
  - Thm 1.1 p. 2 (q > 685090 p^2, p odd, nonzero h, X through powers of q, power saving).
  - Thm 6.3 p. 30; the "parity barrier" quote p. 2.
  - (5.7) p. 25; Thm 1.9 p. 6 (δ<1/126); "cannot give anything above 1/6", pp. 6-7.
  - Cor 6.1 p. 27; Thm 4.5 p. 22; Thm 1.7 p. 5; Lemma 3.2 p. 15 (Pellet's formula).
  - "special properties ... (in positive characteristic)" p. 3; "exponent 1/4 ... (even conditionally)" p. 4.
  - Cor 2.7 p. 13. The exponent 1−β/p in (4.35) against "q^{dβ/2p}" in the proof on p. 22: the inconsistency is
    correctly recorded.
  - Type I/II only in Appendix A: consistent with the helper's notes.
- **prop:ss-split, (b)**
  - Λ = −Σ_{d|n} μ(d) log d: correct.
  - The d>D part is exactly −T_D: n=de, e≤x/d<x/D, d≤x/e. Correct.
  - Even d: n+2 is then even, so only powers of 2 count, giving ≪ D(log x)^2. This is negligible since D ≤ x^{1−c}.
  - Odd-d errors: the log d ≤ log x factor is absorbed by the (log x)^{A+1} in (EH_D). Correct.
  - Euler product: p(p−2)/(p−1)^2 = 1−1/(p−1)^2, and the factor at p=2 is 2. F·ζ(s+1) converges for
    Re s > −1/2, so F'(0)=2C_2 and the sum is −2C_2. Sign of the main term: +2C_2 x. Correct.
  - Numerical check (sieve to 10^7): the partial sums of Σ_{d odd} μ(d) log d/φ(d) are −1.3450, −1.3243, −1.3171,
    −1.3191 at 10^4..10^7, against −2C_2 = −1.32032. Consistent.
  - Tail: ≪ (log D)^{−A} from PNT-type bounds, and D ≥ x^c turns this into (log x)^{−A}. Standard, and it is why
    the lower end of the range is needed.
  - BV: for odd d the inner sum is ψ(x+2;d,2) − log 2, i.e. +O(1). 2 is coprime to d. BV with max over residues
    at Q=X^{1/2}(log X)^{−B}, X=x+2, covers the fixed residue. The O(1)+2/φ(d) discrepancies add up to O(D).
    Correct. D=x^{1/2}(log x)^{−B} lies in [x^c, x^{1−c}].
- **(c)**
  - Lichtman quote "folklore conjecture" p. 1 and Theorem 1.1 (log H/log_2 X → ∞): correct apart from items 5-6.
  - Cantarini's description of MV (EH + EHμ_h, the equivalence with Σ Λ(n)μ(n+h)=o(N), h even ≠0): content
    correct apart from items 2 and 6.
  - The last bullet's "reformulation, not progress" is accurate.
- **(3) Honesty**
  - Abstract, introduction and sec:ss all say the conjecture is open. The equivalence is presented as a
    reformulation. Nothing claims progress on twin primes.
  - The only weakening is item 3.
