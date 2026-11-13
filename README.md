# Twin Prime Notebook

A working paper by **Jerry Kim** (prepared with the assistance of Claude) on small gaps between primes, toward the twin prime conjecture, with a Lean 4 development and exact computer certificates. Research sessions run six times a day; each one opens a pull request that is merged automatically, so the commit history is the research log.

**Website:** https://jerryckim16.github.io/twin-primes/

> No proof of the twin prime conjecture is claimed here. The conjecture is open, and the sieve methods behind every bound in this repository cannot reach 2 (the parity barrier). Nothing here has been peer reviewed.

## Three numbers, kept separate

| | Bound on liminf (p<sub>n+1</sub> − p<sub>n</sub>) | Source |
|---|---|---|
| Established in the literature | 246 | Polymath8b (2014) |
| Claimed in 2026 preprints | 182 | GPT-6 Astra prompted by R. Sharifi; also 186 (OpenAI), 240, 236, 212 by others |
| Reproduced by this project | 240 (conditional); 246 unconditional | 240: the variational step of Stadlmann's argument (arXiv:2608.31126) reproduced exactly — capped ratio k J_T/I_T = 4.0120 > 4 at k = 49 (`code/cap6/P_capfree_D20_u.json`, checked by two independent programs `code/capped_exact.py` and `code/capped_check.py`) + Lean-checked 49-tuple; **conditional on Stadlmann's equidistribution estimates, which this project has not verified**. 246: Polymath8b reproduced (M_{50,1/25} > 4, `code/cert_M50e25_D27e.json`, + Lean-checked 50-tuple), given Bombieri–Vinogradov. Neither is new. Session 7: the variational criterion of Charton et al. (212, k = 45) also checks out exactly (4.0027 > 4) for the caps of their Table 3, but not with our test function for the different caps of their Lemma 9.1 (3.9737), so 212 is not adopted. Session 8: with the test function optimised on Stadlmann's capped support itself the margin is 4.0124 (`code/cap6/P_opt49_D20r_u.json`, two exact programs); Kintali's 236 support (k = 48) recorded, not yet evaluated |

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
