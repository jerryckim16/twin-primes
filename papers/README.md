# Small-results papers

Each line of work that grows into its own result gets its own paper here: `papers/<slug>/main.tex`, author Jerry Kim. Each paper has its own version number and its own changelog. The PDFs are published at `docs/papers/<slug>.pdf`.

| slug | title | version | status | one line |
|---|---|---|---|---|
| `parity-barrier` | The parity barrier and twin primes: what is known and what is missing | 0.12 (draft, 16 Nov 2026) | active | Survey of the obstacle between bounded gaps and twin primes with own results: which targets Polymath8b-type weights can block (bipartite criterion, as in Tao 2014; window form H_m < H(2m+1)); where PM8b's GEH criteria stop (k = 2 at the parity value; the k = 3 eps-window); Pintz's parity-sensitive dichotomy with Maynard weights (some even 0 < \|d\| <= 12 has lambda(p+d) = -1 infinitely often; Pintz: 16; possibly folklore); Chen's theorem as a consistency test (v0.12). Being cut toward a ~20 pp. v1.0 (weekly review, 16 Nov). No claim of progress on the twin prime conjecture. |
| `verification-note` | An independent exact verification of the variational step behind the claimed 2026 bounds $H_1\le240$ and $H_1\le236$, with a remark on the caps of a $212$ draft | 1.0 (16 Nov 2026) | frozen | Exact recomputation of the variational criteria of Stadlmann (240), Kintali / Song–Yue (236) and Charton et al. (212, Table 3 caps); ceiling < 3.99 for the Lemma 9.1 caps (one-program Gram certificate; weights checked at a random point against both programs); the main terms and all 97 raw loss bounds of OpenAI's 186 companion recomputed (the decisive group by two independent programs). A section states per number what rests on one program, two programs or a probabilistic check. The analytic inputs are not verified. |

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
