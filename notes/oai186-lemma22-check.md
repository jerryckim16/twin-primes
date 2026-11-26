# Rung 186: independent check of Lemma 2.2 of [14] (Dickman cell enclosures)

Source [14]: OpenAI, "Numerical certificate for prime gaps at most 186", 30 Aug 2026,
`code/third_party/openai186/short_gaps_numerics.pdf`, printed p. 12 (text from `pdftotext -layout`; the bars in
(2.1) were confirmed on a 220 dpi render of p. 12). Parameters come from pp. 2, 6 and 9.

Script: `code/oai186_lemma22_check.py`, output `code/oai186_lemma22_check.out`, run with `/usr/bin/python3` and
python-flint 0.9.0. **2,736 aggregated checks, 0 failures, 200 s, peak RSS 2.48 GB.** The checks cover 134 values of
M and 13,172,870 grid points. The peak memory comes from the full-range `fmpq` run at M = 49152.
I wrote the script and its output before opening `code/oai186_lemma23_check*.py` and `code/oai186_lemma24_check*.py`.

**Verdict: verified as stated (Proved here + Computed).** The printed proof is terse but has no gap. The facts it
uses without proof (ρ > 0, ρ ≤ 1, 0 ≤ ρ'' ≤ 1 on (1,∞)) are proved below from the delay equation alone. Its constant
6c⁻³ is valid, and 5c⁻³ would also do.

## 1. Statement (p. 12)

D_c(t) := ρ(t/c) for t ≥ 0 and 0 for t < 0. A_j(c) := ∫_{C_j} D_c, with C_j = [jh,(j+1)h). For c = Mh, M ∈ Z≥1:
d̲_j = d̄_j = 1 for 0 ≤ j ≤ M, and for j ≥ M

    d̲_{j+1} = max{0, ↓(d̲_j − d̄_{j−M}/(2j) − d̄_{j+1−M}/(2(j+1)))}
    d̄_{j+1} = min{1, ↑(d̄_j − d̲_{j−M}/(2j) − d̲_{j+1−M}/(2(j+1)) + 1/(2M³))}          (2.1)

Claim: d̲_j ≤ D_c(jh) ≤ d̄_j. The certificate accepts only ordered intervals in [0,1] with both sequences
nonincreasing. Also A_j(c) = h for j < M, and for j ≥ M
max{0, ↓(h/2)(d̲_j+d̲_{j+1}) − h³/(12c²)} ≤ A_j(c) ≤ ↑(h/2)(d̄_j+d̄_{j+1}) (2.2), which may be intersected with
[0,h]. ↓/↑ denote outward dyadic rounding. Since D_c(jh) = ρ(j/M), (2.1) depends on M only.

## 2. Proof (Proved here)

The only input is the definition of ρ (Literature: [14] cites its [1, (2.4)-(2.6)]): ρ = 1 on [0,1], ρ is continuous,
and uρ'(u) = −ρ(u−1) for u > 1.

**P1. Facts about ρ.** (a) (uρ)' = ρ(u) − ρ(u−1), and at u = 1 both sides of the next identity equal 1, so
uρ(u) = ∫_{u−1}^{u} ρ for u ≥ 1.
(b) ρ > 0. Let u₀ be the first zero. Then u₀ > 1, and u₀ρ(u₀) = ∫_{u₀−1}^{u₀} ρ > 0, a contradiction.
(c) ρ' = −ρ(u−1)/u ≤ 0, so 0 < ρ ≤ 1, ρ is nonincreasing, and −ρ'(u) ≤ 1/u ≤ 1.
(d) ρ' is continuous on (1,∞), so ρ is C¹ there. ρ'' = 1/u² on (1,2). On (2,∞),
ρ''(u) = ρ(u−2)/(u(u−1)) + ρ(u−1)/u² ≤ 1/2 + 1/4. So 0 ≤ ρ'' ≤ 1 on (1,∞) \ {2}. ρ'' jumps only at 1 and 2.

**P2. D_c.** For t > c, D_c'(t) = −D_c(t−c)/t, so 0 ≤ −D_c' ≤ 1/c. Also 0 ≤ D_c'' ≤ 1/c² away from t = 2c.
D_c is C¹ on (c,∞) and C² on (c,2c), (2c,3c) and (3c,∞).

**P3. K(t) := D_c(t−c)/t on t ≥ c.** Write f(t) = D_c(t−c). Then K'' = f''/t − 2f'/t² + 2f/t³. Each term is
≥ 0, and K'' ≤ 1/c³ + 2/c³ + 2/c³ = 5/c³ ≤ 6/c³ as printed. On [c,2c], K = 1/t. K' jumps only at 2c, and K'' jumps
only at 2c and 3c. These are grid points because c = Mh. So on every closed cell [jh,(j+1)h] with j ≥ M, K is C¹
with an absolutely continuous derivative and a bounded, nonnegative K''.

**P4. Trapezoid (Peano kernel).** For such g on [a,b] with b − a = h, (h/2)(g(a)+g(b)) − ∫_a^b g =
½∫(t−a)(b−t)g''(t)dt, which lies in [0, (h³/12)·sup g''].

**P5. (2.1) by induction on j.** For j ≤ M, D_c(jh) = 1. For j ≥ M, integrate D_c' = −K over C_j, using
K(jh) = D_c((j−M)h)/(jh):
D_{j+1} = D_j − D_{j−M}/(2j) − D_{j+1−M}/(2(j+1)) + e_j, with e_j ∈ [0, (h³/12)(6/c³)] = [0, 1/(2M³)].
Since M ≥ 1, the delayed indices j−M and j+1−M are ≤ j and are already enclosed. The right side increases in D_j
and decreases in the delayed values. So the lower bound uses d̲_j, the delayed d̄ and e = 0, and the upper bound uses
d̄_j, the delayed d̲ and e = 1/(2M³). This is exactly the bar placement on the rendered page. Clipping is valid by
P1(c), and outward rounding only widens. ∎(2.1)

**P6. (2.2).** For j < M, C_j ⊂ [0,c], where D_c = 1. For j ≥ M, apply P4 to D_c with 0 ≤ D_c'' ≤ 1/c² (P2) on a
cell whose break points (2c, 3c) are endpoints. The excess of the trapezoid over A_j lies in [0, h³/(12c²)]. Then
insert the endpoint enclosures, and use 0 ≤ D_c ≤ 1 for the cap [0,h]. ∎

**P7. Acceptance is a filter and plays no part in validity.** The enclosure holds for every M ≥ 1.
- d̲ is always nonincreasing, given d̄ ≥ 0.
- When d̄_j < 1, d̄_{j+1} ≤ d̄_j holds iff d̲_{j−M}/(2j) + d̲_{j+1−M}/(2(j+1)) ≥ 1/(2M³).
- So acceptance fails once the delayed lower sequence has decayed to about M⁻²/u. This is why small M is rejected.
- Unaligned caps (p. 12): D_c(t) = ρ(t/c) increases in c by P1(c), so c⁻ = h⌊c/h⌋ and c⁺ = h⌈c/h⌉ are valid.

**P8. Sandwich (used by the program).** Order pairs (L,U) by width: (L,U) ⪯ (L',U') iff L' ≤ L and U ≤ U'. One step
of (2.1), clipping included, is monotone for ⪯. By induction, a run rounded outward is ⪰ the exact-rational run,
and a run rounded inward is ⪯ it. Hence L_out ≤ L_exact ≤ L_in and U_in ≤ U_exact ≤ U_out at every j.

Gaps found: none. The following are stated without proof in [14], and are supplied above:
- positivity and the bound 1 for ρ;
- the bounds on ρ'';
- the location of the K and D_c break points;
- why outward rounding preserves validity (P8).

## 3. Computation (Computed, exact; script above)

**Parameters (134 distinct M, every run to j = N = 98304):**
- From the PDF directly:
  - grid caps z/h of (1.5): 68225, 49152, 46580, 44781, 35265, 44976, 35419 (p. 2);
  - p_G/h of (1.24): 24576, 19660, 22390, 17912, 22488, 17990 (p. 6).
- Taken from the authors' derived inputs: the 61 low-bin cutoffs L = ⌊ℓ₀/h⌋ (30 distinct, 3..24270) and the 89
  distinct Lemma 2.4 caps (90 used, 20689..49152).
  - These depend on the source ladders, which I did not rebuild.
  - I read them (read only) with `build_inputs` of `code/third_party/openai186/prime_gap_186_certificate.py`.
  - The counts and ranges agree with the Lemma 2.3 and 2.4 notes.
  - The same `build_inputs` output contains exactly the 13 printed values above.
- Plus generic M = 1..10, 63, 64.

**Ranges needed:** survival and rank-two arrays j ≤ n = 98264, low kernels j ≤ N−1, factorial grid j ≤ N.

**Method:**
- (2.1) in exact integer fixed point (2⁻²⁵⁶), rounded outward and rounded inward. By P8 these sandwich the
  exact-rational sequences, and every statement about the exact sequences is decided from the sandwich.
  0 steps were undecided.
- A third run rounds outward to 160 significant bits per step. This is a proxy for the PDF's 160-bit balls.
- Rigorous ρ is my own Taylor model of ρ(u) = ρ(s) − ∫_s^u ρ(v−1)/v dv:
  - cells of width 1/16 up to u = 24, degree 62, arb at 320 bits;
  - explicit bounds for the 1/v truncation and the product truncation;
  - total error ≤ 1e−76, and ≤ 1.3e−75 for F(u) = ∫₀^u ρ.
  - For u ≥ 24 − 1/16 the program uses only 0 < ρ(u) ≤ ρ(23.94) ≈ 2.7e−37 (monotonicity, P1).

| Check | Result |
|---|---|
| ρ(2..6), ρ(10) agree to 1e−12 with commonly tabulated values (sanity only; no page reference checked) | PASS |
| 1601 points of [1,2]: model overlaps 1 − log u; 211 points of [1,24): uρ(u) = F(u) − F(u−1) | PASS |
| Every M, every j ≤ N: L_in ≤ ρ(j/M) ≤ U_in, hence exact d̲_j ≤ ρ(j/M) ≤ d̄_j; also L_out ≤ L_in, U_in ≤ U_out | 134/134 PASS, 0 bad points |
| (2.2) for every cell j < N, every M, against rigorous A_j/h = M(F((j+1)/M) − F(j/M)); j < M gives A/h = 1 | 134/134 PASS |
| First delay interval: d̲_j ≤ 1 − log(j/M) ≤ d̄_j, every j ∈ [M, 2M] | 134/134 PASS |
| Acceptance of the exact sequences (via the sandwich), outward and 160-bit runs: same first-failure index for every M | PASS |
| All 7 survival, 6 factorial and 89 rank-two caps accept on their needed range (in fact on all j ≤ N) | PASS |
| fmpq exact rationals on prefixes (j ≤ M + 1500, or 200M), all 134 M; full range j ≤ N for M = 68225 and M = 49152 (denominator of d̲_N: 112k and 142k bits): inside the sandwich, and acceptance agrees | PASS |
| Negative controls, M ∈ {64, 11704, 24576, 68225}, on j ≤ M + 20000: NC1 drop +1/(2M³) breaks the upper bound (1407/20000/20000/20000 points); NC2 add +1/(2M³) to the lower bound breaks it; NC3 comparing at a one-cell shift is detected; NC4 (2.2) without −h³/(12c²) fails | all fail as required |

**Acceptance (exact = outward = 160-bit):**
- Every M ≥ 11704 accepts on all j ≤ N.
- Every M ≤ 9753 in the list is rejected. M = 9753 first fails at j = 85834 (u = 8.80); M = 93 fails at j = 554.
- So the low kernels use the delay branch only for L ∈ {11704, 14045, 16854, 18257, 20225, 22247, 24270}. The rest
  use the renewal branch (2.3), which is not checked here.

**Smallest slacks**, all at j = M + 1, all certain:
- d̄ − ρ: 1.05e−15 (M = 68225), 2.81e−15 (M = 49152), 2.08e−13 (M = 11704);
- ρ − d̲: 5.2e−16 (M = 68225).
- (2.2) upper, over every cell with u < 23.94: at least 1.79e−11 (M = 68225).

**Informational:**
- NC5, putting d̄ instead of d̲ in the delayed terms of the upper bound, produced no violations. The bar placement
  in the upper line therefore matters for the proof but not numerically at these M.
- The full-range enclosure holds even for the rejected M, as P5 predicts.

## 4. Comparison with the first programs (read after the above was final)

- `oai186_lemma23_check.py` (`delay_upper`, 160-bit arb), `oai186_lemma23_check2.py` and
  `oai186_lemma24_check2.py` (160-bit dyadics, one rounding per step), and `oai186_lemma24_check.py` (outward
  integer dyadics): all use the same bar placement and the same tests as mine. They round outward only and do not
  re-prove the lemma.
- Agreement:
  - The rejection threshold: fails for M ≤ 9753 and passes for M ≥ 11704. This gives 7 distinct delay L, or 20 of
    61 bins, as in lemma23-check2.
  - All rank-two and grid caps accept on j ≤ N, as in lemma24-check and lemma24-check2.
  - The smallest upper slack at M = 49152 is 2.8e−15, the same as the lemma24-check figure.
- New here:
  - the comparison runs at every grid point on all j ≤ N, not on 1376 to 18,269 samples or only on [M, 3M];
  - (2.2) is checked against the true cell integrals;
  - the exact-rational sequences, as opposed to only their rounded versions;
  - the factorial caps p_G/h and the low cutoffs below 11704;
  - negative controls.
- No disagreement.

## 5. Not covered / open

- The low-bin cutoffs and the Lemma 2.4 caps were taken from the authors' derived inputs, not re-derived from the
  source ladders. The lemma itself holds for every M ≥ 1 (P5), so this affects only which runs are representative.
- The authors' per-operation 160-bit ball rounding was not reproduced bit for bit. My 160-bit proxy rounds once per
  step. Any outward rounding is valid by P8. Acceptance agreed for all three of my roundings at every M. The
  closest rejected case (M = 9753) fails 12,469 steps before its needed range ends. For the accepted M, I did not
  measure how far past N the first failure lies, so a much coarser rounding is not excluded from changing
  acceptance. That would only switch a low kernel to the renewal branch, or make the authors' code raise an
  error. It would not make an enclosure invalid.
- The renewal branch (2.3) and the downstream uses of d̲, d̄ and A_j (cap arrays, (2.9), (2.13)) were not checked.
- The delay-equation definition of ρ is taken from the literature, as [14] does.
