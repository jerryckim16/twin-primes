# Audit of parity-barrier paper v0.6 (new parts only)

Fresh-context adversarial referee, 15 Nov 2026. File audited: papers/parity-barrier/main.tex (working tree on top
of ff56a61; I did not edit it). Note: the file changed while I was reading it (Corollary cor:consistent appeared
between rem:k2 and rem:pm65); it is audited too. Sources: PM8b arXiv:1407.4897v4 (scratchpad pm8b/pm.txt, page
headers "Page n of 80"), MR16 arXiv:1501.04585v4 (scratchpad mrtxt/mr.txt; Corollary 2 checked on the rendered
p. 3 because pdftotext drops the absolute-value bars). Scripts re-run: `geh_ceiling.py` (ALL PASS, exit 0) and
`k2_thm314_numeric.py`. Independent check: my own non-symmetric k=2 optimiser that also includes the half-cells
on the diagonal x+y=2 (scratchpad audit/k2gen2.py; floating point, not a certificate).

Severity: **ERROR** = false statement; **GAP** = missing justification or misleading omission;
**WORDING** = imprecise but harmless; **OK** = checked, no issue.

## Theorem thm:k2 (k = 2)

1. **OK**: definitions. In PM8b Thm 3.12 (p. 15), J_{i,1-ε} integrates F over t_i and squares, then integrates
   over (t_j)_{j≠i} ∈ (1-ε)R_{k-1}. Thm 3.14 (p. 16) uses the same J, support (k/(k-1))R_k = {x+y≤2} at k=2,
   range 0<ε<1/(k-1) = 1. So J_1 = ∫_0^a g², J_2 = ∫_0^a f², and J = ‖f‖²+‖g‖² is correct. The marginal condition
   (35) for i=1 is ∫F dt_1 = 0 when t_2 > 1+ε, that is g(y)=0 for y>B. For i=2 it is f(x)=0 for x>B. Both are
   stated for the right variable.
2. **OK**: region split. For x≤a we have 2-x≥B, so D∩{x≤a} = S ∪ T_1 ∪ U_1 exactly. T_1 lies inside D, and U_1
   (y>B, x≤2-y) automatically has x<a. The five regions are disjoint (U_1∩U_2 = ∅ because 2B>2). The rest of D is
   D∩(a,B]², where Φ=0.
3. **OK**: the identity. For y>B the fibre is [0,2-y]⊂[0,a), and g(y)=0 gives ∬_{U_1} f̄(y)F = 0. Adding the
   symmetric identity gives J = ∬_D FΦ.
4. **OK**: the bounds. In ∬_S Φ² = a‖f‖²+a‖g‖²+2(∫f)(∫g), using 2uv≤u²+v² and (∫_0^a f)² = a‖f‖²-aV_f is
   correct. T_1 contributes 2ε‖f‖². In U_1, the deviation from f̄(y) is at most the deviation from m_f, the
   pointwise integral is ≤ V_f because [0,2-y]⊆[0,a], and the y-length is 2-B = a. Total: (2a+2ε)J = 2J. Then
   Cauchy–Schwarz gives J ≤ 2I. Every step checks.
5. **OK**: the equality case. F_ε is supported in D. It vanishes for x>B or y>B, so (35) holds trivially. For x≤a,
   f = a+ε = 1. J = 2a, I = a² + aε = a, ratio 2. Admissible for every 0<ε<1.
6. **OK (numerics)**: no counterexample. My non-symmetric optimiser, with diagonal half-cells and the constraint
   imposed also on cells that straddle x=B, gives maxima ≤ 2 for ε ∈ {0.1, 0.2, 0.3, 0.5} and n=4..16. It gives
   exactly 2 on grids aligned with a and B. A first version that left the straddling cells unconstrained gave
   values above 2. That was a bug in my script, and it shows that the constraint really matters. Without the
   constraint (n=8) I get 2.517 (ε=0.1), 2.453 (0.2), 2.391 (0.3), 2.289 (0.5).
7. **WORDING**: k=2 subsection, first paragraph, "which the parity argument of [Section 8] rules out". PM8b
   Sec. 8 (p. 68) calls its discussion "informal and heuristic". Fix: "which the heuristic
   parity argument of [PM8b, Section 8] rules out".
8. **WORDING**: rem:k2(2), "the threshold is missed only because ϑ<1". The criterion needs a ratio strictly
   above 2m/ϑ. Since the supremum 2 is attained, no F has ratio > 2, so even ϑ = 1 would not help (and the theorem
   only allows ϑ < 1). Fix: "the criterion reaches the parity value 2 exactly but never exceeds it, so no ϑ ≤ 1
   would suffice".
9. **WORDING**: rem:k2(2), "M_{2,ε} (Theorem 3.12 under EH)". At k=2, Thm 3.12(ii) is a GEH criterion for every
   ε<1 = 1/(k-1). The class it uses is contained in the Thm 3.14 class: (1+ε)R_2 ⊂ 2R_2, and the marginal condition
   is automatic. So thm:k2 gives M_{2,ε} ≤ 2 independently, consistent with PM8b's exact formula on p. 46. Fix: drop
   "under EH", or add this observation as a cross-check.
10. **GAP (reproducibility)**: rem:k2(1), "ratio 2.518 ... 8 cells per unit length". It names no ε, and no script
    in the repo produces 2.518 (grep finds the number only in main.tex). The unconstrained value depends on ε
    (see item 6). Fix: name ε (2.517–2.518 matches ε=0.1), and add the computation to k2_thm314_numeric.py or
    name the script.
11. **WORDING**: rem:k2(3) overstates what the script does.
    - The script maximises over **symmetric** F only. That restriction is not stated. It is not harmless a
      priori, because the top eigenvector could be antisymmetric. My non-symmetric run (item 6) closes this
      heuristically.
    - At n=8, ε=0.9 the script returns 0, not 2, because no cell lies in t≤0.1.
    - ε=0.2 and ε=0.3 are run only at n=30 and n=32.

    Fix: "over symmetric piecewise-constant F", and state the grids for each ε.
12. **OK**: "Theorem 3.14 can never give DHL[2,2]". With m=1 the criterion needs a ratio > 2/ϑ > 2.

## Proposition prop:ceil, Corollary cor:ceil, Remark rem:ceil-locates

13. **OK**: the scaling. With G(t)=F(ct), I(F)=c^k I(G), and the marginal integral picks up c^{k+1}. The three
    supports lie in (k/(k-1))R_k: Thm 3.8 trivially; Thm 3.12(ii) because ε<1/(k-1); Thm 3.14 by definition.
    (1-ε)R_{k-1} ⊆ cR_{k-1}, and the integrands are nonnegative. The bound c·M_k ≤ (k/(k-1))² log k = c(k) follows,
    and so does the second bound (1+ε)(k/(k-1)) log k.
14. **OK**: the GEH ranges and the threshold. Thm 3.8 is stated under EH[ϑ], which follows from GEH[ϑ] by PM8b
    Prop. 2.7 (p. 7). The ranges ε<1/(k-1) are right. The threshold 2m/ϑ > 2m makes "needs ratio > 2m" right.
15. **OK**: the numbers. Re-run (python-flint, 200 bits): c(45)=3.98166<4<c(46)=4.00069; c(391)=5.99936<6<c(392);
    thresholds 2965 and 22007; c(5)=2.51475. Printed comparisons: 4.152 (k=50, ε=1/25), 4.091 (k=51), 2.159
    (k=4, ε=0.168), c(3)=2.472. All correct.
16. **WORDING (script, not main.tex)**: the geh_ceiling.py docstring says "c is increasing for k ≥ 3". This is
    false: c(3)=2.4719 > c(4)=2.4645. Harmless, because every k is checked. Fix: "c is increasing for k ≥ 4".
17. **GAP (attribution)**: the second statement of prop:ceil, M_{k,ε} ≤ (1+ε)(k/(k-1)) log k, is the endpoint
    a=1/(1+ε) of PM8b Remark 6.6 (p. 45). Put a=1/(1+ε) into the displayed bound and the second term vanishes,
    leaving (k/(a(k-1))) log k. With that a, the weight 1+a(kt_i-Σt) ≥ 1-a(1+ε) = 0 on the whole support, so
    Remark 6.6's argument is valid there. PM8b states the open range 1/(1+ε)<a<1/(1-ε), so the endpoint is a limit.
    Fix: in prop:ceil or rem:pm65 say "(this is also the limiting case a→1/(1+ε) of [PM8b, Remark 6.6], where the
    weight is nonnegative)". Downgrade "Proved here" for that part to "essentially in PM8b".
18. **WORDING (mild overstatement)**: rem:ceil-locates, "reachable by the GEH criteria (k≥46)". c(k)>4 is
    necessary, not sufficient, so k ≥ 46 is only not excluded by the ceiling. Fix: "not excluded by the ceiling
    (k≥46; k=51 is what PM8b achieved)". The same applies to "is a gap in the method": it is accurate only as "the
    criteria cannot close it".
19. **OK**: prop:bipartite(b) at m=2 gives blocked iff k≤4. The Corollary 6.4 remark on p. 44 ("cannot hope to
    establish DHL[4,2] (or DHL[3,2]) solely through Theorem 3.8 even when assuming GEH") is quoted correctly.
    Thm 3.2(xiii) DHL[51,3] is confirmed.
20. **GAP (small)**: in the proof of cor:consistent, the case m=1 is "which is Theorem thm:k2". thm:k2 covers
    only Thm 3.14. Two further sentences are needed:
    - Thm 3.12(ii) at k=2 is a subclass of Thm 3.14 (item 9).
    - Thm 3.8 gives M_2 = 1.3859 < 2 (PM8b Cor. 6.3, p. 43).

    Fix: add both sentences.

## Remark rem:pm65 (PM8b Proposition 6.5)

21. **OK (gap confirmed)**.
    - **The printed proof** (pp. 44–45). For (t_j)_{j≠i} ∈ (1-ε)R_{k-1} we have s ≥ ε, and w_i = s+(k-1)t_i > 0 on
      the fibre [0, s+ε]. After Cauchy–Schwarz the proof needs Σ_i∫_{U_i} w_i F² ≤ ∫Σ_i w_i F² = kI. So it needs
      w_i ≥ 0 on supp F \ U_i.
    - **Why this fails.** Off U_i we have s ∈ [-ε, ε), and with t_i=0 we get w_i = s, down to -ε. So the needed
      inequality does not hold.
    - **Pointwise counterexample** (k=2, point (0, 1+ε)): only U_2 contains the point. Σ_i 1_{U_i}w_i = w_2 = 2+ε,
      which exceeds k=2. So an F concentrated there violates Σ_i∫_{U_i}w_iF² ≤ kI.
    - **What remains open.** The region of integration and the sign were read correctly. The gap is in the proof
      as printed. Whether the stated bound is false is open; the remark says so.
22. **OK**: the corrected bound. w_i ≥ s_i ≥ -ε on the support. Not all w_i are negative, because Σw_i = k > 0.
    So Σ_i 1_{U_i} w_i ≤ k+(k-1)ε, which gives (k/(k-1)+ε) log(2k-1). Also checked: the comparison
    k^ε < 2-1/k ⇔ (1+ε)log k < log(2k-1), and the example "all ε ≤ 1/(k-1) when k ≥ 4" (fails at k=2,3, holds
    from k=4).
23. **WORDING**: rem:pm65 would be stronger with three additions.
    - At ε=0 the proof is fine (w_i ≥ 0 on R_k).
    - The same gap affects Remark 6.6 for a > 1/(1+ε).
    - At k=2 the printed constant 2 log 3 = 2.197 does hold: by prop:ceil, M_{2,ε} ≤ 2(1+ε)log 2 ≤ 2.197 for
      ε ≤ 0.585; by thm:k2, M_{2,ε} ≤ 2 for all ε<1. So "not decided" applies only to k ≥ 3.

    Grep confirms that Prop. 6.5 is cited again only in Remark 6.6 (text l. 3140).

## Subsection subsec:mr16, Remark rem:mr16-transfer

24. **OK**: Theorem 1 (pp. 1–2) is quoted exactly: constants C, C' > 1, 2 ≤ h ≤ X, δ > 0, both exceptional terms,
    C' = 20000. Checked: Corollary 2 with absolute value on rendered p. 3, "for every integer h ≥ 1"; Corollary 4
    (p. 4, hypotheses right); the [n, n+C√n] statement (p. 5, after Corollary 5); "at least as deep as the twin
    prime conjecture" (p. 3); "large primes factors which is completely arbitrary for general f" (p. 2); the
    complex counterexample f(p)=p^{it} (p. 5); "parity" absent (case-insensitive grep). Proof-structure pages also
    check: Q_1 ≤ exp(√log X) p. 6; T_0 = (log X)^{1/15} p. 7; Ramaré variant p. 9 and Lemma 12 p. 19; Lemma 14 p. 21;
    Lemmas 9 and 11 pp. 16–17; f real p. 11; fundamental lemma p. 31; Corollary 2 via sign changes pp. 37–38.
25. **WORDING**: rem:mr16-transfer, "Step (3) needs f(pm)=f(p)f(m) (p. 9)". On p. 9 identity (9) is written for
    completely multiplicative f, and "the same ideas work" for general f, through the 1_{(p,m)=1} term. Fix: "uses
    multiplicativity to factor n=pm (p. 9; written there for completely multiplicative f)".
26. **WORDING**: rem:mr16-transfer ends "Nothing in [MR16] addresses that correlation (Open)". This sentence is a
    fact about the source, not an open problem. Fix: put the Open label on a separate sentence ("estimating
    ΣΛ(n)Λ(n+2) is open"), or drop it.

## Abstract and overstatement

27. **OK / WORDING**: the abstract is accurate and repeats that nothing here proves twin primes or comes close.
    Nothing in the new material claims progress on twin primes or on breaking parity. thm:k2 and cor:consistent
    are presented as consistency with the obstruction. One phrase to soften: "its failure to give three primes is
    a variational ceiling, not parity". "Not parity" means "not blocked by the pattern weights of Section bip"
    (a heuristic class). Fix: "a variational ceiling, not a parity block of the kind in Section 3".
28. **WORDING**: open question 2, "A proof of DHL[5,3] would need a genuinely different criterion, not a better
    test function". This is correct for these three criteria only. Fix: add "than these three".

## Verdict

- Theorem thm:k2: correct. Every step was verified, the equality case is admissible, and independent
  non-symmetric numerics find no ratio above 2 under the constraint.
- Remark rem:pm65: the gap is real, and the corrected bound is right. Add items 17 and 23.
- No ERRORs. GAPs: 10, 17, 20.
