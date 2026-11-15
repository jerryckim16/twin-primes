# Connections between the project's results (keep honest; update each run)

The twin prime conjecture is open. Nothing below is a step that is known to lead to it.

## Bound work (main paper, verification note)
- Depends on: the 2026 preprints' analytic inputs (equidistribution estimates; NOT verified by us) and their reductions.
- Feeds into: the reproduced conditional bounds (240, 236; 212 / 186 / 182 variational parts). These are statements about
  DHL[k,2] for k around 39-50, i.e. far from k = 2 (twin primes) and, by the parity barrier, unable to reach below 6 even under GEH.
- Missing for anything bigger: the analytic inputs themselves; and nothing in this line can touch parity.

## Parity-barrier paper (papers/parity-barrier)
- Prop. prop:bipartite / Cor. cor:six: within Liouville-pattern weights, the obstruction blocks exactly H_m < H(2m+1). Depends
  only on the PM8b heuristic framework (the heuristic part is that this class captures what sieves can see).
  Feeds into: a sharp statement of the barrier; the H_m line (the parity limit of this class for H_2 is 12, far below the
  known 270 (EH) / 252 (GEH)); the open question whether weights outside the class block DHL[5,3].
- Prop. prop:tao-weight: confirms the obstruction's input in a weak regime. Prop. prop:tao-weight-logc (Session 19): the same at
  level (log x)^{c0}, conditional on Tao–Teräväinen arXiv:2512.01739v2 Thm 3.1 (unrefereed). Depends on: that preprint, MRT (1.12).
  Feeds into: nothing that lowers a bound; it sharpens how far the obstruction's input is a theorem. Missing to reach the sieve
  level x^theta: (3.4)-type cancellation for moduli far beyond powers of log x (no source). Even then it would only confirm the
  obstruction. Session 19 exploration: extra Liouville coordinates cannot enlarge the weight class (dead end).
- Props. prop:fi-twin, prop:B-parity, Remark rem:fi-transfer: what the asymptotic sieve would need for Lambda(n+2); the bilinear
  estimate is exactly the parity-sensitive missing piece; FI's a^2+b^4 shows which structure made it provable there.
- Missing for twin primes: a bilinear (Type II) estimate for Lambda(n+2)-type sequences, or any non-sieve input. Not in sight.

## Bound work, rung 182 (Session 19)
- All four ingredients of the 182 cap quotient (I, J0, J+, tail T) now by two programs; q_H - 1 >= mu-. Missing before 182 could
  even be considered reproduced: the restoration losses (197 source integrals, partly underspecified), and the analytic inputs.

## H_m programme (scoped, not started as a paper; notes/hm-programme.md)
- PM8b Thm 6.7 lower bound reproduced (code/hm/pm8b_mk_lower.py): k = 35410 (MPZ) and 41588 (BV only) match.
- Possible gain from 2026 inputs depends on an admissible (varpi, delta) region nobody has made explicit; modest at best.
