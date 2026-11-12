# Twin Prime Notebook

A working paper by **Jerry Kim** (prepared with the assistance of Claude) on small gaps between primes, toward the twin prime conjecture, with a Lean 4 development and exact computer certificates. Research sessions run six times a day; each one opens a pull request that is merged automatically, so the commit history is the research log.

**Website:** https://jerryckim16.github.io/twin-primes/

> No proof of the twin prime conjecture is claimed here. The conjecture is open, and the sieve methods behind every bound in this repository cannot reach 2 (the parity barrier). Nothing here has been peer reviewed.

## Three numbers, kept separate

| | Bound on liminf (p<sub>n+1</sub> − p<sub>n</sub>) | Source |
|---|---|---|
| Established in the literature | 246 | Polymath8b (2014) |
| Claimed in 2026 preprints | 186 | OpenAI; also 240, 236, 212 by others |
| Reproduced by this project | see `status.json` | own certificates + Lean |

## How sessions work

Each session reads `STATE.md`, does one reproduction step and tests one idea of its own, updates the paper, the Lean code and the log, then pushes a branch `session/YYYY-MM-DD-HHMM`, opens a pull request and merges it. Failures are logged too.

## Layout

| Path | What it is |
|---|---|
| `paper/main.tex` | The paper (amsart). `latexmk -pdf main.tex` |
| `lean/` | Core Lean 4.35.0 project, no Mathlib, no `sorry`. `lake build`, then `lake env lean Audit.lean` |
| `code/mk_general.py` | Exact Gram matrices for Maynard's M_k with all symmetric polynomials; certified lower bounds |
| `code/cert_*.json` | Exact rational certificates (coefficient vectors) for M_k > 4 |
| `code/admissible.py`, `code/gen_lean.py` | Admissible-tuple search and Lean generation |
| `log/bound-history.json` | Every improvement of the project's own bound, starting from 578 (drawn as a log-scale chart on the website) |
| `status.json`, `log/entries.json` | Bounds, results ledger, ideas ledger, research log (drive the website) |
| `STATE.md` | Handoff notes for the next session |
| `notes/` | Reading notes and working notes |
| `docs/` | The generated website (GitHub Pages). Rebuild with `python3 code/build_site.py` |

## Labels

Every statement in the paper carries one of: **Lean-checked**, **Computed** (exact certificate), **Proved here**, **Literature**, **Claimed** (preprint not yet independently verified), **Open**.
