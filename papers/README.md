# Small-results papers

Each line of work that grows into its own result gets its own paper here: `papers/<slug>/main.tex`, author Jerry Kim. Each paper has its own version number and its own changelog. The PDFs are published at `docs/papers/<slug>.pdf`.

| slug | title | version | status | one line |
|---|---|---|---|---|
| `verification-note` | An independent exact verification of the variational step behind the claimed 2026 bounds $H_1\le240$ and $H_1\le236$, with a remark on the caps of a $212$ draft | 0.5 (draft, 14 Nov 2026; one-sided Bonferroni certificates; main terms of the 186 companion) | active | Exact recomputation of the variational criteria of Stadlmann (240), Kintali / Song–Yue (236) and Charton et al. (212, Table 3 caps); ceiling < 3.99 for the Lemma 9.1 caps; the main terms of OpenAI's 186 companion recomputed. The analytic inputs are not verified. |

## Updating `verification-note`

- When `capped_exact.py` finishes on the Song–Yue witness:
  - If it matches Jref exactly, remove the "one program so far" qualifiers from Theorem 5, Corollary 7, the abstract and the results table ("one program", "second running"), and the status paragraph after Theorem 5.
  - If it does not match, report the discrepancy precisely.
- (Done in v0.4, Session 13) Proposition 6 (our own k = 48 vector) confirmed by the second program.
- When `capped_exact.py` evaluates the random point used for the Lemma 9.1 weights, record that in the paragraph after Proposition 9.
- Bump the version, add a changelog line at the end of the paper, recompile, and copy the PDF to `docs/papers/verification-note.pdf`.
