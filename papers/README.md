# Small-results papers

Each line of work that grows into its own result gets its own paper here: `papers/<slug>/main.tex`, author Jerry Kim. Each paper has its own version number and its own changelog. The PDFs are published at `docs/papers/<slug>.pdf`.

| slug | title | version | status | one line |
|---|---|---|---|---|
| `verification-note` | An independent exact verification of the variational step behind the 2026 bounds $H_1\le240$ and $H_1\le236$, with a remark on the caps of a $212$ draft | 0.1 (draft, 13 Nov 2026) | active | Exact, two-program recomputation of the variational criteria of Stadlmann (240), Kintali / Song–Yue (236) and Charton et al. (212, Table 3 caps); ceiling < 3.99 for the Lemma 9.1 caps. The analytic inputs are not verified. |

## Updating `verification-note`

- When `capped_exact.py` finishes on the Song–Yue witness:
  - If it matches Jref exactly, remove the "one program so far" qualifiers from Theorem 5 item (2), the abstract and the results table.
  - If it does not match, report the discrepancy precisely.
- When the second program confirms Proposition 6 (our own k = 48 vector), remove its "one program" label.
- When `capped_exact.py` evaluates the random point used for the Lemma 9.1 weights, record that in the paragraph after Proposition 9.
- Bump the version, add a changelog line at the end of the paper, recompile, and copy the PDF to `docs/papers/verification-note.pdf`.
