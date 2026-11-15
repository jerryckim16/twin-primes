# Rung 182: second program for the cap tail term E_{H_C^c} (report)

Status: **finished**. This is a second, independently written program for one numerical ingredient of a **Claimed**
preprint: the Lean premise trialTailUpper (GPT-6 Astra / R. Sharifi, bundle [M], k = 39). It does not verify the 182
claim. The first program is `code/sharifi182_tail.py`, reported in notes/tail-182-report.md.

- Program: `code/sharifi182_tail2.py`.
- Per-cap checkpoints: `code/data182/tail2_cap_<b>.json`. Combined: `code/data182/tail2_result.json`.
- Logs: `runs/tail2_182_A.log` (caps 141720, 177528, 186253), `runs/tail2_182_B.log` (196608, 186491),
  `runs/tail2_182_246256.log`, `runs/tail2_182_combine.log` and `runs/tail2_182_selftest.log`.
- Precision cross-check: `code/data182/tail2_cap_196608_P192B160.json`, log `runs/tail2_182_196608_P192B160.log`.

## What was computed

    T = sum_i int 1_{H_C^c}(Y) K(Y) |E_i F(Y)|^2 dnu^38(Y) / (hZ)^39

This is the same definition as program 1. K is the step kernel (5.5)-(5.6), constant on blocks of 768 values of r'.

**Kernel.** I wrote my own kernel in exact Python Fractions, working from notes/sources-182-tail.md. The constants are
parsed from the Lean file: trialRoughness = lambda, trialMinorantA = a, trialHingeThreshold = t, trialAuxiliaryRetreat,
trialPairBins and trialRadialBlocks.

**Contraction.** It follows the architecture of program 1 (`code/sharifi182_J.py` / `code/sharifi182_I.py`): Kronecker
products of GMP fixed-point arrays (P = 256 bits for p, B = 224 bits for the coordinate arrays) and exact integer sums.
The code is new. It does **not** import or copy `sharifi182_check2*.py` or `sharifi182_tail.py`. What is new or
different:
- **Rigorous rounding.** Every fixed-point array carries an integer radius. Each floor gets a directed error bound, and
  products, correlations and the final contraction get explicit integer error bounds. The inputs (g, Z, t^e and the
  Dickman cell masses) are arb balls at 384 bits. The result is an **enclosure**. Program 1 for J and I was
  floor-only and not rigorous.
- **Tail rows only.** chi_T = 0 for r' < R0 = 352699, so p is built only on rows [R0, n0), the erased cells are
  a' < n0 - R0, and the moments are sliced to [R0, n0). The moments are computed by a DFS over the prefix tree, so
  little is held in memory at once.
- **B-splines.** They come from my own literal Cox-de Boor recursion in exact Fractions. On each knot span the cubic in
  r is obtained by exact interpolation through 4 cells.
- **Dickman cell masses.** I derived Phi(u) = int_0^u rho myself for u <= 3 and evaluate it in arb (the Li2 is arb's
  polylog). My formula turned out to be algebraically the same as program 1's G(u).
- **Per-block output.** Each cap stores its 512 per-block integer sums, so T for any block kernel, and M_T (K = 1), is
  a cheap recombination.

**H_C and outer rows.** Both are derived from the Lean trialShells (H_C: lower <= (r'+38)h < upper; outer: (r+39)h).
They are asserted equal to the [M] Sec. 7.2 table. The layer set is {141720, 177528, 186253, 186491, 196608, 246256}.

## Numbers

**Kernel** (from `--kernel`, my code):
- 506 of the 1024 W_j^+ are nonzero, with sum 0.0478156.
- K_0 = 0.276903, K_459 = 0.954174, K_483 = 1.289196 and K_511 = 2.193543.
- K is monotone, and (5.7) 0 <= K <= 2.194 holds.

**Tail:**

| | value |
|---|---|
| T2 (this program) | 5.2863488059280771006442311847462e-13, radius 1.36e-45 (rel 2.6e-33) |
| T1 (program 1) | [5.28634880592807710064423118475e-13 +/- 1.03e-40] |
| trialTailUpper | 5.286348805972699e-13 |

- T2 / T1 - 1 = **-2.04e-32**. The T2 ball lies inside the T1 ball.
- T2 / trialTailUpper - 1 = **-8.44e-12**. The exact upper end of the T2 ball is <= trialTailUpper.
- M_T (K = 1) = 3.49797744197484e-13, so T / M_T = 1.51126, the same as program 1.

**Per cap:**

| cap | T2 part | rel. diff vs program 1 |
|---|---|---|
| 141720 | 8.601568597247790298e-14 | -2.36e-32 |
| 177528 | 1.460768450551653004e-13 | -1.90e-32 |
| 186253 | 2.812321923122470493e-13 | -2.01e-32 |
| 186491 | -4.235161557207584129e-13 | -2.05e-32 |
| 196608 | 4.388263129736758702e-13 | -2.05e-32 |
| 246256 | exactly 0 | 0 |

- For cap 246256 every marginal vanishes on the tail rows, so the moments are never computed.
- Each T2 part ball lies inside the corresponding program 1 ball.
- Program 1's midpoints lie outside my much smaller balls, by a nearly uniform -2.0e-32 relative (about 1.1e-44
  absolute against my radius of 1.4e-45). This is inside program 1's radii, so it is not a discrepancy between the
  enclosures.
  - Likely cause (checked only indirectly): Z summed at 128 bits instead of 384 bits gives (Z_128/Z_384)^39 - 1 =
    -2.04e-32, which is exactly the observed offset. Program 1 works at 128 bits. I did not inspect how it sums Z.

**Precision cross-check.** I reran cap 196608 at P = 192, B = 160. The result moved by 6.5e-30, and its rigorous
radius of 1.2e-27 covers this. The bound scales by 2^64 between the two runs, as expected, and the two balls overlap.

**Nominal block end, r_max = 768 x 512 - 1 (optional).**
- K_511 = 2.196370, so (5.7) fails.
- T_nominal = 5.28635147448903e-13. This is 5.05e-7 relative above the n0 - 1 value and **above trialTailUpper** by
  5.05e-7 relative.
- Only caps 141720, 177528 and 186253 change, because block 511 lies in the third outer shell.
- So the ambiguity does matter for the premise: the Lean bound is consistent only with r_max = n0 - 1, which is the
  reading used by both programs.
- For q_H the effect would be about 7.9e-5 x 5e-7, about 4e-11, which is negligible against the margin of 6.5e-5.

## Readings: where this agrees or differs with program 1

I found **no difference in reading.** Each of the following is the same in both programs:
- W_j^+ is the ceiling of the exact (5.5) value to a multiple of 1e-25.
- The hinge is evaluated at the upper bin endpoint.
- L21 is the 21-term alternating series.
- z_j(q) = min(lambda - eps0, (1 - s_j)/2 - q - eps0).
- q+ = rho* (r_max + k - 1) h, with r_max = min(768b + 767, n0 - 1), and blocks start at r' = 0.
- "Retained sum index" is read as r'.
- The complement is taken in the ambient retained space.
- The mask is chi_{T,a} = 1 - [capC(r') >= b_a].
- The layer set is the same 6 caps.
- The erased cell mass is d_{min(c, C_s)}. On the tail rows a' <= 40477 is below every cap, so these masses are all 1.
- The prefactor is 39h/Z.

Only the implementations differ:
- I derived the outer rows from the Lean shells, where program 1 for J hard-codes them. The results are equal.
- My error tracking is rigorous.
- The B-spline method is different.

The kernel values agree with program 1's to the printed digits.

## Self-test (`--selftest`, PASSED, about 22 s)

- **Real configuration.** The H_C and outer rows derived from Lean equal the [M] table, and the first tail row is
  352699. The B-splines satisfy partition of unity.
- **Kernel.** I re-evaluated (5.5)-(5.6) literally in mpmath (60 digits), with L21 >= log(1+v) checked.
  - All 1024 bins satisfy 0 <= W - W_exact <= 1e-25.
  - At 7 sampled r', K - K_literal lies in [1.4e-22, 9.8e-22]. It is expected to lie within [0, 6e-21].
  - Mutation `hinge_lo` (hinge at the lower endpoint) was **caught**: 506 bins fail.
- **Dickman masses.** These were compared against quadrature of rho from the delay equation, including cap 141720 at
  j = 393176. The maximum relative deviation is 8.4e-37.
- **Brute force of the whole tail form.** The setups were k = 3 with 32 cells and k = 4 with 24 cells, using 26 test
  knots with a 4-fold interior knot, random rational coefficients for 3 components x 11 signatures x 22 splines,
  artificial cell caps (5-6 layers), and an artificial block-constant K (block length 4).
  - The brute force uses literal definitions in mpmath at 60 digits: every retained and erased cell with its
    largest-fragment level, F literally, H_O and H_C tested directly, and division by (hZ)^k.
  - Relative deviation: 4e-58 (k = 3) and 6e-57 (k = 4).
  - At low precision (P = B = 40) the ball **contains** the brute-force value, with relative radius 3e-6 and 1.3e-4.
  - Mutations, all **caught**:

    | mutation | k = 3 rel. effect | k = 4 rel. effect |
    |---|---|---|
    | `noK` (no K weight) | 0.74 | 0.63 |
    | `gt` (">" in the H_C mask) | 0.61 | 3.7 |
    | `cmin` (erased mass with c instead of min(c, C_s)) | 1.8e-3 | 2.3e-3 |

  - The test configuration was chosen so that `cmin` actually matters on the tail rows; with my first configuration it
    did not.

## Runtime and memory

- 2 workers in parallel: worker A took 834 s for 3 caps and worker B 518 s for 2 caps. Cap 246256 took 11 s. Total
  wall time was about 14 min.
- Each cap took 250-295 s.
- Peak RSS was 1.50 GB per worker.

## What is shared with program 1 (honest)

- **The reading of the source.** Both programs rest on the same transcription (notes/sources-182-tail.md) and the same
  layered derivation of the contraction from program 1 (layer rule, subset expansion of P_sigma, set-partition moments,
  d_{min(c,C_s)}, 39h/Z). My code re-implements that derivation; it does not re-derive it from the PDF. I did not
  re-download the PDF.
- **The data.** Both use the same trial F (the 726 Lean coefficients, knots and shells) and the same Lean parser
  (`code/sharifi182_data.py`).
- **The kernel.** Program 1's kernel reading is the same as mine. While checking program 1's command line I saw the
  first ~60 lines of `code/sharifi182_tail.py`, including its kernel function. I had already designed my kernel from
  the transcription and did not copy any code, but the two are not blind to each other.
- **The Dickman formula.** My closed form is algebraically the same as program 1's. It is independently checked here
  against quadrature.
- **Not checked by either program:** the analytic content, i.e. that (5.8) holds with this K, and that
  trialTailUpper is meant to be this quantity. The latter rests on the 8.4e-12 agreement.

## Rerun

    python3 code/sharifi182_tail2.py --selftest
    nohup python3 code/sharifi182_tail2.py --cap 141720,177528,186253 > runs/tail2_182_A.log 2>&1 &
    nohup python3 code/sharifi182_tail2.py --cap 196608,186491,246256 > runs/tail2_182_B.log 2>&1 &
    python3 code/sharifi182_tail2.py --combine

Existing checkpoints are skipped, so delete `code/data182/tail2_cap_<b>.json` to recompute a cap.
