# Rung 182: the cap tail term E_{H_C^c} (report)

Status: **finished**. This is **one program** for the tail. It is not checked by a second implementation of the tail
contraction. It checks one numerical ingredient (the Lean premise trialTailUpper) of a **Claimed** preprint
(GPT-6 Astra / R. Sharifi, bundle [M], k = 39). It does not verify the 182 claim.

Program: `code/sharifi182_tail.py`. It imports `code/sharifi182_check2_J.py`, which imports
`code/sharifi182_check2.py`.
Per-cap results: `code/data182/tail_cap_<b>.json`. Combined: `code/data182/tail_result.json`.
Logs: `runs/tail182_A.log` (caps 141720, 177528, 186253), `runs/tail182_B.log` (caps 186491, 196608, 246256) and
`runs/tail182_combine.log`.

## What was computed

The tail is normalised by (hZ)^39, like I, J0 and J+:

    T = sum_i int 1_{H_C^c}(Y) K(Y) |E_i F(Y)|^2 dnu^38(Y).

- **Kernel K.** K is the step kernel (5.6), constant on blocks of 768 consecutive retained index sums r'. It is
  computed exactly in fmpq:
  - W_j^+ is (5.5) rounded up to a multiple of 1e-25, with 1024 bins on [2 lambda, a];
  - lambda = 8639/50000 (Lean trialRoughness), a = 41361/100000, t = 19/50;
  - L21 is the 21-term alternating series;
  - the hinge is evaluated at the bin's upper endpoint;
  - z_j(q) = min(lambda - 1e-4, (1 - s_j)/2 - q - 1e-4);
  - q+ = rho* (r_max + 38) h, with r_max = min(768b + 767, n0 - 1).
- **Contraction.** It is the same as for J (same marginal v^a, same 38-fold moments, prefactor 39h/Z). It has one
  mask per layer, chi_{T,a}(r') = 1 - [capC(r') >= b_a], with capC = 0 outside the H_C rows. Each row is weighted by
  K of its block.
- **Layers.** The layer cap set is {141720, 177528, 186253, 186491, 196608, 246256}h: the components, the outer
  shells and the H_C caps. The face caps of H_0 and H_1 do not enter.
- **H_C rows.** They are derived from Lean trialShells[3] with lower <= (r'+38)h < upper. They equal the [M] Sec. 7.2
  table (0:352698 cap 246256, 352699:371671 cap 186491); this is asserted in the program.
- **Unweighted check.** The program also computes the same form with K = 1, giving M_T.

## Numbers

**Kernel.**
- 506 of the 1024 W_j^+ are nonzero, and their sum is 0.0478156.
- K = 0.27690 on block 0, 0.95417 at block 459 (where the tail starts, r' = 352699), 1.28920 at block 483 and
  2.19354 on block 511.
- K increases monotonically. **(5.7), 0 <= K <= 2.194, holds** with r_max = n0 - 1 = 393176 on the last block.

**Tail.**
- T = [5.28634880592807710064423118475e-13 +/- 1.03e-40].
- Published trialTailUpper = 5.286348805972699e-13.
- The upper end of the ball is below the published bound. T / trialTailUpper = 1 - 8.44e-12.

**Per cap** (the parts are not individually nonnegative):

| cap | T part |
|---|---|
| 141720 | 8.6016e-14 |
| 177528 | 1.4608e-13 |
| 186253 | 2.8123e-13 |
| 186491 | -4.2352e-13 |
| 196608 | 4.3883e-13 |
| 246256 | exactly 0 |

The 246256 part is exactly 0 because the top layer's outer shell ends at r = 352697, below the tail rows.

**Unweighted mass.**
- M_T = 3.49797744197e-13, so T / M_T = 1.5113.
- This lies inside [K_459, K_511] = [0.954, 2.194], as it must.

**Effect on q_H.** q_H - 1 = rho* (J0 + (1-ell) J+ - d_h T)/I - 1 was computed exactly from the ball endpoints:
- ell = 6308693370963335/2^59 and kappa-bar = 46653544162031/5e17, so d_h = kappa-bar(1/ell - 1) = 0.00843268572.
- The inputs are I from check2_I_result.json, J0 and J+ from check2_J_result.json, and T from above.
- The lower and upper ends agree to far below 1e-15. The result is **mu = 2.767058949e-4**, against the published
  mu- = 9968877639291/2^55 = 2.766919371e-4, so mu >= mu-.
  - The excess of 1.4e-8 comes almost entirely from the denominator: we use the actual I (its ball) rather than
    I+ = 1.48963412e-11.
  - With the published premises (J0lo, J+lo, TailUp, I+) one gets 2.766919373e-4, as in qH_check.json.
- The tail costs rho* d_h T / I = 7.855e-5 of q_H.
- mu - L-bar = 6.5228e-5, against (10.3) 6.5214e-5. This difference also comes from using the I ball instead of I+.

## Readings

All of these were checked against the bundle PDF text (pdftotext of [M] in the scratch directory src182/: M.txt, with
Mraw.txt for the raw layout).
- **The definition of the tail.** Prop. 6.1, p. 28, reads "E_i^tail = int_{C^c} K |V|^2 dnu^{k-1}", and (6.7) "sums of
  J_{0,i}, J_{+,i}, E_i^tail". The C^c subscript sits on the next line in the -layout extraction. Sec. 7.6 replaces
  C by H_C. Our value is 8.4e-12 below trialTailUpper, the same pattern as J0 and J+ (4.0e-11 and 5.2e-12 above
  their lower bounds). This strongly supports the reading that **trialTailUpper is the summed tail
  sum_i int_{H_C^c} K |E_i F|^2 / N, with the step kernel (5.6) and prefactor 39h/Z**. The PDF does not say this in
  words.
- **The helper's transcription (notes/sources-182-tail.md)** of (5.2), (5.4)-(5.7), the H_C table, (6.5)-(6.7) and
  (7.4)-(7.6) agrees with the PDF text. I found no differences that matter. One addition: Sec. 5.1 also states
  "t >= 2 lambda", which holds (.38 >= .34556).
- **Block-end ambiguity (5.6).** "Divide retained sum indices into blocks of length ceil(n0/512) = 768" does not say
  which r_max closes the last block.
  - With r_max = n0 - 1 = 393176, K_511 = 2.19354 and (5.7) holds.
  - With the nominal 768 x 512 - 1 = 393215, K_511 = 2.19637 > 2.194, so (5.7) fails.
  - I used n0 - 1. The 8e-12 agreement with trialTailUpper is consistent with this choice. I did not compute T with
    the other choice, so I have not shown that it would differ by more than 8e-12.
  - Blocks are taken to start at r' = 0.
- **Other readings.**
  - The rounding of W_j^+ is read as the ceiling of the exact (5.5) value.
  - "Retained sum index" is read as r', the sum of the 38 retained cell indices. This is consistent with
    q+ = rho*(r_max + k - 1)h.
  - The complement is read as all of the 38-coordinate ambient space outside H_C (p. 27: "Complements are taken in
    the retained-root ambient space").
  - Lean trialLambda is ell, not the paper's lambda.

## Self-test (`--selftest`, passed for k = 3 and k = 4)

- Setup: a 48-cell grid with distinct artificial caps (186491 maps to 24) and an artificial block-constant K (blocks
  of 4, values 7/6 to 11/6).
- The pipeline is compared against a brute force over all cells, using the literal definitions in mpmath:
  - layers over **all 10** cap values, which is a finer layer set than the program's 6, so the reduced layer set is
    tested too;
  - the H_C membership tested directly;
  - the K weight per r'.
- Agreement is about 4e-36 relative.
- Two deliberate mutations were caught: dropping the K weight, and using ">" instead of ">=" in the H_C mask.
- The exact kernel formula is not tested by brute force. Its values reproduce the other helper's independent
  Fractions prototype (0.27690, 0.95417, 1.28920, 2.19354, and 506 nonzero W) and (5.7).

## Independence (honest)

- This is ONE program. Its marginal, moments, Dickman masses, Cox-de Boor and parser are those of the check2 I/J
  programs. Those agreed with program 1 for I and J to 1e-22 or better, but nothing independent recomputes the tail.
- The reading of the kernel (5.5)-(5.6) was made by me and by the transcription helper from the same PDF.
- Agreement with the Lean premise at 8e-12 is strong evidence that our reading matches the authors' certificate. It
  is not an independent derivation of the kernel's correctness: the proof of (5.8) and the hinge bound is not
  checked.

## Runtime and memory

- 2 workers, about 21 min per cap (moments dominate). Total wall time about 66 min (A 3974 s, B 3661 s).
- Peak RSS 3.55 GB per worker.

Rerun:

    python3 code/sharifi182_tail.py --selftest
    nohup python3 code/sharifi182_tail.py --caps 141720,177528,186253 > runs/tail182_A.log 2>&1 &
    nohup python3 code/sharifi182_tail.py --caps 186491,196608,246256 > runs/tail182_B.log 2>&1 &
    python3 code/sharifi182_tail.py --combine
