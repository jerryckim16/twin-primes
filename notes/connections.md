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
- Prop. prop:tao-weight: confirms the obstruction's input in a weak regime; could be strengthened via Tao–Teräväinen (preprint).
- Props. prop:fi-twin, prop:B-parity, Remark rem:fi-transfer: what the asymptotic sieve would need for Lambda(n+2); the bilinear
  estimate is exactly the parity-sensitive missing piece; FI's a^2+b^4 shows which structure made it provable there.
- Missing for twin primes: a bilinear (Type II) estimate for Lambda(n+2)-type sequences, or any non-sieve input. Not in sight.

## H_m programme (scoped, not started as a paper; notes/hm-programme.md)
- PM8b Thm 6.7 lower bound reproduced (code/hm/pm8b_mk_lower.py): k = 35410 (MPZ) and 41588 (BV only) match.
- Possible gain from 2026 inputs depends on an admissible (varpi, delta) region nobody has made explicit; modest at best.
