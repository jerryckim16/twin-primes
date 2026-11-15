# Rung 182: second program for the cap numerators J_0, J_+ (report)

Status: **finished**. This checks one numerical ingredient (the two cap numerators J_0,H and J_+,H in (6.7)/(7.4))
of a **Claimed** preprint (GPT-6 Astra / R. Sharifi, bundle [M], k = 39). It does **not** verify the 182 claim. It
does not check the tail term E_{H_C^c} (with kernel K), the restoration loss, or anything analytic.

Program: `code/sharifi182_check2_J.py`. Per-cap results: `code/data182/check2_J_cap_<b>.json`. Combined:
`code/data182/check2_J_result.json`. Logs: `runs/check2_J_A.log` (caps 140306..177542) and `runs/check2_J_B.log`
(caps 179967..246256).

## What was computed

Each form is divided by (hZ)^39:

    J_0 = sum_i int 1_{H_0}(Y) |E_i F(Y)|^2 dnu^38,
    J_+ = sum_i int 1_{H_1}(Y)(1 - 1_{H_0}(Y)) |E_i F(Y)|^2 dnu^38,

for the 726-coefficient trial F of [M] (7.3) on the 393216-cell grid. I wrote down my own derivation of the finite form
before reading program 1's arithmetic. It is in the docstring of the program. In short:
- I split Y by the layer of its largest fragment over the 9 cap values
  {140306, 141720, 141724, 177528, 177542, 179967, 186253, 196608, 246256}h (components, outer shells, base and
  enlarged faces).
- The erased coordinate carries g d_{min(c, C_s)}.
- I use the subset expansion of P_sigma.
- The 38-fold moments come from the A(y)^38 series.
- The prefactor is 39h/Z.

All arithmetic is in arb balls (python-flint 0.9.0, 128 bits).

## Numbers

| | this program (ball) | program 1 | rel. diff | published lower bound | ball >= bound? |
|---|---|---|---|---|---|
| J_0 | 5.63645908992367166973506277169e-11 +/- 1.64e-39 | 5.6364590899236716e-11 | 1.96e-23 | 5.636459089698676e-11 (trialJ0Lower) | yes, rel. excess 3.99e-11 |
| J_+ | 4.08240742966433656776654431018e-13 +/- 2.48e-40 | 4.0824074296643364e-13 | 2.03e-32 | 4.0824074296431434e-13 (trialJPlusLower) | yes, rel. excess 5.19e-12 |

The lower ends of both balls, as exact rationals in the JSON file, lie above the published lower bounds. The relative
margins above the bounds are small: 4.0e-11 for J_0 and 5.2e-12 for J_+. The ball radii (about 3e-29 relative) are far
below these margins.

### Per cap, against program 1

- **J_+ agrees for all 9 caps** to about 2e-32 relative, and program 1's exact value lies inside my ball in every case.
- **J_0 agrees to at most 1e-29 relative for 6 caps.** Program 1 lies inside my ball for those 6.
- **J_0 differs at about 1e-23 relative for 3 caps.** These are the component caps 141720, 177528 and 246256, with
  relative differences 3.9e-23, 2.2e-23 and 7.1e-24. Program 1's value is outside my ball there, by about 1e-33 in
  absolute terms against radii of about 2e-36.
  - The same three caps showed the same size of difference (about 1e-22 relative) in the I check
    (`code/data182/check2_I_result.json`).
  - My guess, not verified, is that this is program 1's floored fixed-point rounding, which is not a rigorous enclosure.
  - It is 12 orders of magnitude below the margin over the published bound, so it does not affect the comparison.
- For caps 141724 and 179967 the J_0 part is exactly 0 in program 1 and [0 +/- 3e-40] here. These caps occur only in
  the enlarged face, so the two layer terms cancel for J_0.

## Self-test (`--selftest`, passed)

- Setup: k = 3 (and also k = 4, with `--k 4`), a 48-cell grid, the real coefficients and knots, and the shells
  re-derived on that grid.
- The 9 caps are replaced by the distinct artificial values 15, 16, 17, 19, 20, 21, 23, 25 and 30 cells, keeping their
  order, so that every layer is non-trivial.
- The pipeline is compared against a brute-force sum over all retained cells Y and erased cells X:
  - mpmath at 45 digits;
  - power sums computed directly on the k t-values (no subset expansion);
  - the M0 layer measure taken literally as prod h g^2 d_{b_a} - prod h g^2 d_{b_(a-1)};
  - the min(c, C_s) cap conditions tested directly;
  - the B-splines from the recursive Cox-de Boor formula in Fractions;
  - the literal division by (hZ)^k.
- Agreement is about 1e-35 relative.
- Two deliberate mutations were caught: using the component cap instead of min(c, C_s) in the erased cell mass, and
  using a wrong pair product.
- The self-test does not test the Dickman cell masses, which come from the same function (shared with check2).

## Reading: differences from program 1 and from the source

- I found **no difference in reading** from program 1's docstring. The 9 cap values, the layer rule, the face masks
  and the erased marginal with d_{min(c, C_s)} all agree. The numerical agreement supports this, though it does not
  prove that the shared reading is what the source means.
- Outer and face row ranges:
  - Program 1 hard-codes them. I **derived** them from the Lean shells with lower <= (r + d)h < upper, using d = 39 for
    the outer shells and d = 38 for the faces.
  - They equal the table in [M] Sec. 7.2 (notes/sources-182.md Sec. 3); this is asserted in the program.
  - No shell boundary falls on a cell total inside the range, so "<" and "<=" give the same rows.
- J_+ mask:
  - I compute it literally as chi_1 (1 - chi_0). Program 1 does the same in effect.
  - I assert H_0 c H_1 row by row (base cap <= enlarged cap). The assertion holds.
- Points where the source is not explicit, and where both programs make the same choice:
  - which cap values make up the layers;
  - the definition of "face mask in layer a";
  - that the face domains use the whole-cell upper total with d = 38.
  These are the same open points as for 186 (notes/sources-186-forms.md Sec. 3).

## What is shared with program 1 and with check2 (how independent this is)

Shared with program 1:
- the reading above, including the layered decomposition. It is derived independently, but it is the same formula.
- the Lean data files;
- the Dickman cell-mass convention d_b(j) = (1/h) int_{C_j} rho_D(t/b).

Shared with `code/sharifi182_check2.py` (imported, not re-implemented), so this check is only as independent as that
program:
- the Lean parser;
- the Dickman closed form, with arb log and acb polylog;
- the fmpq Cox-de Boor;
- the y-series algebra.

Independent of program 1:
- arb balls everywhere (program 1 uses fixed point with floors and is not rigorous);
- row tables derived from the Lean shells;
- moments from the y-series instead of set partitions;
- erased marginals as arb_poly products of per-group arrays cut to their support (program 1 uses GMP correlation);
- pointwise B-splines instead of span polynomials.

The balls are "rigorous in spirit". Their correctness depends on python-flint/FLINT and on the code being right. The
JSON ball strings are printed with 25 digits; the exact binary midpoint and radius are stored as well.

## Runtime and memory

- 2 workers, each about 21 min per cap. Total wall time about 107 min (worker A 6369 s, worker B 4708 s).
- Peak RSS 3.69 GB per worker.
- The layer marginals took 1.5-3 min each. A worker reuses the shared layer of consecutive caps.

Rerun:

    python3 code/sharifi182_check2_J.py --selftest
    nohup python3 code/sharifi182_check2_J.py --caps 140306,141720,141724,177528,177542 > runs/check2_J_A.log 2>&1 &
    nohup python3 code/sharifi182_check2_J.py --caps 179967,186253,196608,246256 > runs/check2_J_B.log 2>&1 &
    python3 code/sharifi182_check2_J.py --combine
