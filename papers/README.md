# Small-results papers

Each line of work that grows into its own result gets its own paper here: `papers/<slug>/main.tex`, author Jerry Kim. Each paper has its own version number and its own changelog. The PDFs are published at `docs/papers/<slug>.pdf`.

| slug | title | version | status | one line |
|---|---|---|---|---|
| `parity-barrier` | The parity barrier and twin primes: what is known and what is missing | 0.9 (draft, 15 Nov 2026) | active | The Polymath8b parity obstruction and Selberg's example read in the sources; which close-prime targets a Polymath8b-type (Liouville-pattern) weight can block: target graph bipartite, DHL[k,m+1] iff k <= 2m (both already in Tao's 2014 blog post, credited from v0.7), and our window form: the class forbids exactly H_m < H(2m+1) (= 6 for m = 1), with a correction to Polymath8b's Remark 8.1; the Friedlander–Iwaniec asymptotic sieve specialised to Λ(n+2) and what their a^2+b^4 bilinear estimate uses; the twisted Type I input proved in a weak, log-averaged form from Tao's two-point theorem, and at level (log x)^{c0} conditionally on a Tao–Teräväinen preprint (also for Maynard's two-variable weights); Sawin–Shusterman's twin primes in F_q[T] read in the source, with the integer version of their split (a reformulation as a Möbius–prime correlation, related to Murty–Vatwani) and the step with no integer analogue; ceilings for Polymath8b's GEH criteria (no DHL[k,3] for k <= 45) and, at k = 2, the strongest criterion exactly at the parity value 2; a dual formula showing why this fails to extend to k = 3 (overlapping constraints), with an exact step-function check of Polymath8b's DHL[3,2] under GEH (ratio 2 + 1.8e-4); for which eps the k = 3 criterion works (above 2 at eps = 2/9, 1/4, 7/24; provably below 2 for eps >= 0.439); Matomaki–Radziwill read in the source; what the level of distribution alone gives (Bombieri's asymptotic sieve via Ford: under EH twin primes ⇔ a weighted count of p-2 = p1p2), with a probable factor-2 slip in a 2019 preprint's constant. No claim of progress on the twin prime conjecture. |
| `verification-note` | An independent exact verification of the variational step behind the claimed 2026 bounds $H_1\le240$ and $H_1\le236$, with a remark on the caps of a $212$ draft | 0.11 (draft, 15 Nov 2026; the Lemma 9.1 ceiling's weights now checked against both exact programs) | active | Exact recomputation of the variational criteria of Stadlmann (240), Kintali / Song–Yue (236) and Charton et al. (212, Table 3 caps); ceiling < 3.99 for the Lemma 9.1 caps (weights checked by two programs); the main terms and all 97 raw loss bounds of OpenAI's 186 companion recomputed (the decisive group by two independent programs). The analytic inputs are not verified. |

## Updating `verification-note`

- When `capped_exact.py` finishes on the Song–Yue witness:
  - If it matches Jref exactly, remove the "one program so far" qualifiers from Theorem 5, Corollary 7, the abstract and the results table ("one program", "second running"), and the status paragraph after Theorem 5.
  - If it does not match, report the discrepancy precisely.
- (Done in v0.4, Session 13) Proposition 6 (our own k = 48 vector) confirmed by the second program.
- (Done in v0.11, Session 24) `capped_exact.py` evaluated the random point used for the Lemma 9.1 weights: exact agreement.
- Bump the version, add a changelog line at the end of the paper, recompile, and copy the PDF to `docs/papers/verification-note.pdf`.

## Scoped, not started as a paper

- H_m programme (3g (1)): `notes/hm-programme.md` (15 Nov 2026). Polymath8b's Thm 6.7 lower bound reproduced (`code/hm/pm8b_mk_lower.py`: k = 35410 with MPZ, 41588 with BV only, both equal to Polymath8b's). Any gain from the 2026 inputs hinges on an explicit (varpi, delta) region that no source states; the capped k ~ 40-50 supports are irrelevant for m >= 2. Decision: not started as a paper; first step if resumed: derive the admissible (varpi, delta) region of each 2026 input set.
