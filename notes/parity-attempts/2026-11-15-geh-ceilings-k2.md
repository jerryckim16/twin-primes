# Route card: where Polymath8b's GEH criteria stop (ceilings), and k = 2 exactly at the parity value

Date: 15 Nov 2026, Session 21 (bonus run started 14:54 UTC). Parity programme, Part 2 (one bounded attempt).

## Question
Open question 2 of the parity paper asks for the converse of the bipartite criterion: Liouville-pattern weights block
DHL[k, m+1] only for k <= 2m, so is DHL[5,3] (H_2 <= 12) provable under GEH? And how close does the variational method come to the
parity value where parity does block?

## Success / no-go criteria (stated before computing)
- Success: a proved upper bound (ceiling) for the ratio in all three GEH criteria of PM8b (Thms 3.8, 3.12(ii), 3.14) that
  decides DHL[5,3] for them; and at k = 2 an exact statement of how the Theorem 3.14 ratio compares with the parity value 2.
- No-go: if any admissible F gave ratio > 2 at k = 2, the reading of Thm 3.14 (or of the parity argument) would be wrong:
  stop and recheck the formulation before anything else.

## Sources read (in the source)
- PM8b arXiv:1407.4897v4 (SHA-256 4085a675...6a7, same file as before): Thms 3.8 (p. 13), 3.12-3.13 (p. 15), 3.14-3.15 (p. 16),
  Cor 6.4 and Prop 6.5 (p. 44), Remark 6.6 (p. 45), exact M_{2,eps} (pp. 45-46), Sec. 7.4 (pp. 62-68, k = 3 certificate:
  J/I = 2 + 286648173/4966595189139280, exact fraction re-checked here).

## What was done
1. Prop. prop:ceil (Proved here, elementary, by scaling Cor 6.4): ratio <= c(k) = k^2 log k/(k-1)^2 for all three criteria;
   also M_{k,eps} <= (1+eps) k/(k-1) log k for every eps. Cor. cor:ceil: no DHL[k,3] for k <= 45, no DHL[k,4] for k <= 391
   (code/parity/geh_ceiling.py, arb balls; PM8b's printed lower bounds all lie below).
2. Thm thm:k2 (Proved here): at k = 2, every F admissible in Thm 3.14 has J_1 + J_2 <= 2 I, with equality for an explicit step
   function. Proof: write J = <F, Phi> using the vanishing marginal condition, then ||Phi||^2 <= 2J by a variance argument.
   Numerics (code/parity/k2_thm314_numeric.py, floating point): grid maxima = 2.000000000000000.
3. Cor. cor:consistent: for every parity-blocked pair (2 <= k <= 2m) the three criteria cannot give DHL[k, m+1].
4. Remark rem:pm65: the printed proof of PM8b Prop 6.5 integrates a weight that can be negative off the fibres used; a corrected
   argument gives (k/(k-1) + eps) log(2k-1). Nothing in PM8b depends on it.

## Classification
**Proved (confirms the obstruction; locates it).** Nothing here breaks or sidesteps parity. The content is:
(a) for m = 2 and 5 <= k <= 45 the obstacle for these criteria is the variational ceiling, not parity;
(b) at k = 2 the strongest GEH criterion sits exactly at the parity value, so it misses DHL[2,2] only because theta < 1;
(c) the criteria and the parity class agree on every blocked case.
First unresolved implication: none for this route (it is a closed statement). The open follow-ups are open question 6 of the
paper (the exact k = 3 supremum, between 2 and 2.472; the grid exploration of this run extrapolates to about 2.003 at eps = 1/4,
Heuristic) and whether the variance argument gives sharp ceilings for k >= 3.

## Not to repeat
Ceilings by scaling / Cauchy-Schwarz for the PM8b criteria are done. Do not redo the k = 2 problem.
