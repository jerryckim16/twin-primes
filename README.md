# Twin Prime Notebook

A working paper by **Jerry Kim** (prepared with the assistance of Claude) on small gaps between primes, toward the twin prime conjecture, with a Lean 4 development and exact computer certificates. Research sessions run three times a day (every eight hours); each one opens a pull request that is merged automatically, so the commit history is the research log.

**Website:** https://jerryckim16.github.io/twin-primes/

> No proof of the twin prime conjecture is claimed here. The conjecture is open, and the sieve methods behind every bound in this repository cannot reach 2 (the parity barrier). Nothing here has been peer reviewed.

## Three numbers, kept separate

| | Bound on liminf (p<sub>n+1</sub> − p<sub>n</sub>) | Source |
|---|---|---|
| Established in the literature | 246 | Polymath8b (2014) |
| Claimed in 2026 preprints | 182 | GPT-6 Astra prompted by R. Sharifi; also 186 (OpenAI), 240, 236, 212 by others |
| Reproduced by this project | **236 (conditional)**; 240 (conditional); 246 unconditional | 236: the variational step of Song–Yue (IACR ePrint 2026/1893; same support as Kintali's 236) reproduced exactly — for their published witness the capped numerator and cap-free denominator **equal their reference integers digit for digit** (715 and 655 digits), criterion 48 J/I0 = 1.000664921591 > 2001/2000, with the capped numerator computed by two independent exact programs (`code/capped_check.py`, `code/capped_exact.py --jonly`; `code/cap6/compare2_sy236.json`) + Lean-checked 48-tuple; **conditional on Song–Yue's equidistribution theorem (their Thm 4.18), which this project has not verified** (Sessions 10–12). 240: the variational step of Stadlmann (arXiv:2608.31126) reproduced exactly — k J_T/I_T = 4.0120 > 4 at k = 49 (`code/cap6/P_capfree_D20_u.json`, two programs) + Lean-checked 49-tuple; **conditional on Stadlmann's equidistribution estimates, not verified here** (Song–Yue's Remark 4.23 points out a possible missing hypothesis in his Lemma 5). 246: Polymath8b reproduced (M_{50,1/25} > 4, `code/cert_M50e25_D27e.json`, + Lean-checked 50-tuple), given Bombieri–Vinogradov. None of these is new. Other rungs: Charton et al.'s 212 (k = 45) criterion checks out for their Table 3 caps (4.0027 > 4) but not for their Lemma 9.1 caps (certified ceiling < 3.99), so 212 is not adopted; OpenAI's 186 uses a different (fragment-measure) criterion that our pipeline does not cover yet (`notes/sources-186.md`, `notes/sources-186-forms.md`). |

## Small results

- [`verification-note`](papers/verification-note/main.tex) — *An independent exact verification of the variational step behind the claimed 2026 bounds H<sub>1</sub> ≤ 240 and H<sub>1</sub> ≤ 236* (v0.3, draft; [PDF](https://jerryckim16.github.io/twin-primes/papers/verification-note.pdf)). Index: `papers/README.md`.

## How sessions work

Each session reads `STATE.md`, does one reproduction step and tests one idea of its own, updates the paper, the Lean code and the log, then pushes a session branch, opens a pull request and merges it. Failures are logged too.

## Layout

| Path | What it is |
|---|---|
| `paper/main.tex` | The paper (amsart). `latexmk -pdf main.tex` |
| `lean/` | Core Lean 4.35.0 project, no Mathlib, no `sorry`: twin primes ⇔ `BoundedGaps 2`, admissibility certificates, explicit tuples, `DHL.mono`, `not_boundedGaps_one`, counting large coordinates (`Caps.lean`). `lake build`, then `lake env lean Audit.lean` |
| `code/mk_general.py` | Exact Gram matrices for Maynard's M_k with all symmetric polynomials, and (`--eps p/q`) for Polymath8b's epsilon-enlarged simplex M_{k,eps}; certified lower bounds |
| `code/scan_eps.py`, `code/extrapolate_eps.py`, `runs/scan_k*.jsonl` | Certified M_{k,eps} on a grid of (k, degree, eps) and the heuristic degree extrapolation (Remark 20) |
| `code/dual_lp.py`, `runs/dual_lp_*.log` | Convex optimisation of dual weights depending on (t_m, S) (Proposition 19; floating point) |
| `code/cert_M*.json` | Exact rational certificates (coefficient vectors) for M_k > 4. Re-check any of them with `python3 code/verify_cert.py <file>` |
| `code/dual_eps_cert.py`, `code/check_floor_cert.py`, `code/cert_floor_k29.json` | Theorem 15: the epsilon-enlarged simplex cannot reach k ≤ 29 (certificate, and an independent re-check with a second interval library) |
| `code/floor_hybrid.py`, `code/cert_floor_hybrid_*.json` | Theorem 31: floor for one-band Stadlmann-type supports (any caps), as a function of the level ω; `--check` re-verifies with a second interval library |
| `code/capped_exact.py`, `code/capped_check.py`, `code/cap6/` | Session 6: EXACT capped functionals I_T, J_T on Stadlmann's support (Proposition 25, Theorem 26). Two independent programs; `python3 code/capped_exact.py code/cap6/P_capfree_D20_u.json --procs 3` (≈45 min) and `python3 code/capped_check.py code/cap6/P_capfree_D20_u.json --procs 4` (≈6 min) both give k J_T/I_T = 4.0120389 > 4. `code/to_ucoords.py` converts certificates to Stadlmann's scaling; tests in `code/capped_check_tests.py`, `code/cap6/mc_test.py` |
| `code/songyue_convert.py`, `code/songyue_I0.py`, `code/songyue_J0.py`, `code/songyue_compare.py`, `code/songyue_compare2.py` | Sessions 10–12: Song–Yue's 236 witness converted exactly to our format; cap-free I0 and J0 directly in the monomial basis; exact comparison with their Appendix C reference integers (`code/cap6/compare_sy236.json`) |
| `code/capped_gram.py` | Session 8: Gram matrices of I_T, J_T by reverse mode (exact weights, exact self-test with `--check`), optimisation of P on the capped support (`--out`), rigorous ceilings (`--ceiling sigma`). `python3 code/capped_gram.py code/cap6/P_capfree_D20_u.json --procs 3 --check code/cap6/check_capfree_D20.json --out P_opt.json` (≈30 min) |
| `code/stadlmann_caps.py` | Stadlmann's support with rough-mass caps: exact cap-violation integrals and a rigorous lower bound from a cap-free certificate |
| `code/dual_eps.py` | Floating-point exploration of dual weights (Remarks 17 and 18) |
| `code/admissible.py`, `code/gen_lean.py` | Admissible-tuple search and Lean generation |
| `log/bound-history.json` | Every improvement of the project's own bound, starting from 578 (drawn as a log-scale chart on the website) |
| `status.json`, `log/entries.json` | Bounds, results ledger, ideas ledger, research log (drive the website) |
| `STATE.md` | Handoff notes for the next session |
| `notes/` | Reading notes and working notes |
| `docs/` | The generated website (GitHub Pages). Rebuild with `python3 code/build_site.py` |

## Labels

Every statement in the paper carries one of: **Lean-checked**, **Computed** (exact certificate), **Proved here**, **Literature**, **Claimed** (preprint not yet independently verified), **Open**.
