# Referee report: papers/verification-note/main.tex, candidate version 1.0

Date: 16 November 2026 (Session 27). Fresh-context, adversarial helper agent; main.tex read in full, not edited by the
referee. Line numbers refer to HEAD 0ec48bd. The helper could not write files; the coordinator saved its report here.

Evidence consulted: log/entries.json (Sessions 6-14, 24); paper/main.tex sec:stad, Props. exact/bonf/bonf2, Remarks 186/182;
notes/*report*.md (kappa-, tail-, tail2-, check2-J-182, arith-182, loss-outer2); lean/TwinPrimes/Caps.lean; code/cap6/
check_/res_ pairs, compare_*.json, compare_rand45_lemma91.out, I0_sy236.json, J0_sy236.json; runs/gram45_*.log, runs/exact_rand45*.log.

## Checked and correct
- Two-program claims: I_T and J_T string-equal in check_*.json and res_*.json for capfree_D20, opt49_D20r, ax45_D21,
  kin48_D22r, rand45_lemma91; for sy236 only J_T in both (I_T in check_sy236.json alone), as the note says.
- SY cap-free values: res_sy236_jonly I / I0_sy236 I0 = 2^96 3^10 7^2 11^2 521^50 exactly (J: same times 2^2); coordinate factors.
- Appendix A cap costs (0.004137, 0.000330, 0.000536, 0.009537, 0.038585) and regain fractions (9.2%, 30.7%) correct;
  ceilings 4.14 (337 pieces), 4.126 (495 pieces); margins 1.6492e-4, 6.6e-4; Bonferroni gap 3.5487e-8; Kintali's digits;
  182 arithmetic; Lean counts and cap conditions; ceiling runs (sigma = 4 and 3.99) and random-point self-test; abstract ~199
  words; no version tags in headings; Lemma egf correct; Prop. fibre correct.

## Items (ERROR / GAP / MINOR)
1. ERROR l.537, l.568: headings of rem:186, rem:182 say "two independent programs" though parts rest on one program.
2. ERROR: the 182 tail T second program saw part of program 1 (kernel function) and shares the parser sharifi182_data.py
   (tail2-182-report.md); does not meet the note's definition of independent programs.
3. ERROR abstract (iv): "most loss ingredients agree" is false for 182 (197 restoration integrals unchecked); 186
   restoration step also unchecked.
4. ERROR Appendix A item 5: Bonferroni levels reversed (J_T lower bound: level 2 for Corr_1 and Corr_2^R, level 1 for
   Corr_2^U; I_T upper bound: level 1 for the removed mass).
5. ERROR rem:bonf: int_V P^2, Corr_1, Corr_2, Q(u',U) undefined in the note; V clashes with V_21; U is called theta.
6. ERROR l.248 vs l.469-475: says only capped_check.py covers the Lemma 9.1 caps, but capped_exact.py evaluated them.
7. ERROR l.286-288: Gram method labelled "Proved here"; the paper labels it a method description, validated by self-tests.
8. ERROR l.480-482: "cannot give their 4.00438" too strong; the paper says "suggests", conventions not compared in every detail.
9. GAP: 186 restoration step missing from the "not checked" list; 186 main terms share one transcription.
10. GAP: abstract lacks the one-program label of the Lemma 9.1 ceiling.
11. GAP: polygon reduction needs g >= L - tau, never stated.
12. GAP: 236 corollary omits the unverified reduction theorem.
13. GAP l.114-117: "all three claimed bounds" omits 186, 182.
14. GAP results table: witness row leads with the one-program 48 J_T/I_T.
15. GAP: two definitions of "two programs"; the 182 I, J_0 checks are numerical agreement (program 1 fixed point, not
    rigorous; for 3 caps its values lie outside program 2's balls, check2-J-182-report.md).
16. GAP: companion cited as version 0.27; tree has 0.26 (fine if 0.27 is published at freeze).
17-28. MINOR: formal power series in lem:egf, notation; fibre wording, empty interval, only C_{m+1} <= C_m + g used; Lean
    lemma hypotheses; label for 4.012038868; "0.0038" vs same-P 0.0034; version tag "In versions 0.6--0.7" in rem:186;
    "58 digits" vs 47 guaranteed; "relative" 7e-17, 89.4% vs 89.5%; random point seed (MT, 20261113); 5000 vs 4800 bits in
    the paper; four vs three cores; title omits 186/182; rem:lemma5 run-on sentence; misc. Appendix wording.

## Disposition (coordinator, Session 27)
See the changelog item 1.0 of the note: items 1-16 addressed; minor items 17 (formal series), 18 (fibre remark), 20, 21, 22,
23, 24, 25, 27 addressed; 19, 26, 28 deferred (recorded in STATE.md).
