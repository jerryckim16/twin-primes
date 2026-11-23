# Small-results papers

Each line of work that grows into its own result gets its own paper here: `papers/<slug>/main.tex`, author Jerry Kim. Each paper has its own version number and its own changelog. The PDFs are published at `docs/papers/<slug>.pdf`.

| slug | title | version | status | one line |
|---|---|---|---|---|
| `parity-barrier` | The parity barrier and twin primes: what is known and what is missing | 1.0.1 (20 Nov 2026; status note on a claimed result, arXiv:2610.20242) | frozen (v1.1 in preparation: staged in `papers/parity-barrier/v11/`, not yet in main.tex) | Survey of the obstacle between bounded gaps and twin primes with own results (window form of Tao's convex-hull criterion; GEH ceilings, k = 2 at the parity value, the k = 3 eps-window; Pintz's dichotomy with Maynard weights, 12 for Pintz's 16; consistency tests; why Gowers norms and averages over the shift stop at the mean gap; asymptotic sieves; F_q[T], a^2+b^4, x^3+2y^3; Siegel zeros). Frozen after a five-lane internal referee pass (referee/2026-11-18-parity-barrier-v1/); errata only as 1.0.x; new results go into a v1.1 or a short note only if they prove something not already implied. No claim of progress on the twin prime conjecture. |
| `verification-note` | An independent exact verification of the variational step behind the claimed 2026 bounds $H_1\le240$ and $H_1\le236$, with a remark on the caps of a $212$ draft | 1.0.1 (17 Nov 2026; erratum) | frozen | Exact recomputation of the variational criteria of Stadlmann (240), Kintali / Song–Yue (236) and Charton et al. (212, Table 3 caps); ceiling < 3.99 for the Lemma 9.1 caps (one-program Gram certificate; weights checked at a random point against both programs); the main terms and all 97 raw loss bounds of OpenAI's 186 companion recomputed (the decisive group by two independent programs). A section states per number what rests on one program, two programs or a probabilistic check. The analytic inputs are not verified. |

## Updating `verification-note`

- When `capped_exact.py` finishes on the Song–Yue witness:
  - If it matches Jref exactly, remove the "one program so far" qualifiers from Theorem 5, Corollary 7, the abstract and the results table ("one program", "second running"), and the status paragraph after Theorem 5.
  - If it does not match, report the discrepancy precisely.
- (Done in v0.4, Session 13) Proposition 6 (our own k = 48 vector) confirmed by the second program.
- (Done in v0.11, Session 24) `capped_exact.py` evaluated the random point used for the Lemma 9.1 weights: exact agreement.
- Bump the version, add a changelog line at the end of the paper, recompile, and copy the PDF to `docs/papers/verification-note.pdf`.

## Status note (Session 27)

- Verification note frozen as v1.0 after an internal referee pass (referee/2026-11-16-verification-note-v1/); deferred minor items listed in STATE.md. Further changes only as dated errata (v1.0.x) if an error is found.

## Weekly review decisions (16 Nov 2026)

- Verification note: finish and freeze as v1.0 (top priority). Parity paper: apply the cuts listed in `notes/reviews/2026-11-16.md` toward a ~20 pp. v1.0; at most one short subsection or remark per parity attempt. Do NOT start a capped-variational-theory paper (appendix of the verification note instead). k = 3 GEH thread stopped. Rung 182 paused until its data exist.

## Scoped, not started as a paper

- H_m programme (3g (1)): `notes/hm-programme.md` (15 Nov 2026). Polymath8b's Thm 6.7 lower bound reproduced (`code/hm/pm8b_mk_lower.py`: k = 35410 with MPZ, 41588 with BV only, both equal to Polymath8b's). Any gain from the 2026 inputs hinges on an explicit (varpi, delta) region that no source states; the capped k ~ 40-50 supports are irrelevant for m >= 2. Decision: not started as a paper; first step if resumed: derive the admissible (varpi, delta) region of each 2026 input set.

## Status note (Session 32)

- Parity paper frozen as v1.0 (18 Nov 2026): cut from 33 to 24 pages, notation renamed (y_d, Psi with signs s_i, region T), referee items of 16 Nov applied, five-lane referee pass (referee/2026-11-18-parity-barrier-v1/) applied. No paper is active now; per Jerry's rules, at most 3 active at a time. Candidates for the next active line: a short note only if a parity attempt proves something not already implied by v1.0.

## Status note (Session 33)

- No paper changed except the main paper (v0.33). Parity attempt (E2 pairs at a fixed difference, 2-adic no-go for 4 ∤ d) recorded as a route card only; together with the Session 32 E2 card it is a candidate for one remark in a parity-paper v1.1, to be decided by the weekly review of 23 Nov. Programme (4) started in Lean only (`lean/TwinPrimes/Reduction.lean`), not as a paper.

## Status note (Session 34)

- No small-results paper changed (both papers frozen). Parity attempt (Green–Sawhney's Gowers-norm Type II sums vs a fixed-shift twin condition: located) recorded as a route card only. Programme (4) continues in Lean only (`Reduction.lean`: the limit step from two-sided asymptotics to the sieve inequality). Main paper v0.34.

## Status note (Session 38)

- Parity paper v1.0.1: status note only (no new results). Lü–Wang–Wu (arXiv:2610.20242) claim sum_p mu(p+2) = o(pi(x)), which the paper called open; marked Claimed in Remarks rem:ford-twin, rem:ss-transfer, one open question and the history appendix. Parity attempt (odd-order Chowla, located) recorded as a route card only. Programme (4) continues in Lean only (`Fano.lean`). Main paper v0.38.

## Weekly review decisions (23 Nov 2026)

- Both papers stay frozen, except ONE planned parity-paper v1.1 (the Lü–Wang–Wu conditional observation as one short subsection, the E2 consistency tests as one remark, one summary paragraph of the other post-freeze route cards; then refreeze). Next active line: a short Lean note for programme (4) once the k-dimensional Maynard identity is formalised (started in Session 47, `lean/TwinPrimes/MaynardS1.lean`). Paused: the exact-certification toolkit note (5), H_m. See `notes/reviews/2026-11-23.md`.
