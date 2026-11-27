# Rung 186: check of the directed arithmetic of Sec. 2.3 of [14], ending in (2.26)

Source [14]: OpenAI, "Numerical certificate for prime gaps at most 186" (30 August 2026),
`code/third_party/openai186/short_gaps_numerics.pdf`. I read it with `pdftotext -layout` into
`/tmp/claude-0/oai186-sec23/`, which is not in the repo. Pages 16-17 were also rendered with `pdftoppm -r 110`,
because the extraction drops the floor and ceiling brackets of (2.22) and (2.23). Page numbers below are the
printed ones. Sec. 2.3 runs from p. 16 ("2.3. Interval evaluation") to p. 17 (the paragraph after (2.26), up to
"Acceptance requires (2.33) ...").

Program: `code/oai186_directed_check.py` (run with `/usr/bin/python3`; uses fractions and python-flint 0.9.0).
Output: `code/oai186_directed_check.out`.
**31 checks, 0 failures. 19 negative controls, all caught. Runtime 54.5 s wall, peak RSS 49 MB.**
I wrote the program from the PDF alone. I opened the authors' script only after the output was saved (§6).

**Verdict: verified as stated.** Every rounding direction in Sec. 2.3 is correct for the quantity it bounds. The
error terms of the binary64 reductions are fully accounted for, including gradual underflow. (2.26) holds
exactly for every 1 <= r <= 98264, and it implies that the endpoints enclose the sum. No repair is needed.
Secondary result: the renewal majorant (2.3) is proved by a general argument valid for every M >= 2 (§5). That
covers every M at which the paper can use it, including a fallback from the delay branch at any M >= 64.

## 0. Criteria (fixed in the script header before deriving)

- **Success.**
  - (2.26) holds exactly for all r <= 98264, and its printed numerator and printed lower bound are exact.
  - Each link of the reduction proof holds exactly on every tested instance, and the endpoints enclose the exact
    sum.
  - (2.22)-(2.25), zero-prefix removal and the four-product hull are sound on all instances.
  - Every negative control is caught.
- **No-go.** Either of these, confirmed by re-running:
  - an exact counterexample to a positive check;
  - a negative control that is not caught (it would make the corresponding check vacuous).

## 1. The claims of Sec. 2.3, and how each is settled

| # | Claim (page) | Status | Script |
|---|---|---|---|
| 1 | (2.22) p. 16. If 0 <= A⁻/Q <= A <= A⁺/Q (and the same for B), then ⌊A⁻B⁻/Q⌋/Q <= AB mod Xⁿ <= ⌈A⁺B⁺/Q⌉/Q coefficientwise | Proved by reading (monotonicity of products of nonnegative polynomials, and ⌊x⌋ <= x <= ⌈x⌉). Computed exactly for single products and for chains P⁴⁰ and 40P³⁹R + 1560P³⁸S² at b = 8 (coarse) and b = 224. Also checked for a 160-bit arb → 224-bit fixed point → K⁵ chain against an independent 400-bit arb product (certain comparison) | B2, B3, B8 |
| 2 | (2.23) p. 16: ⌈P/Q⌉ = ⌊(P + (Q−1)(1+…+X^{r−1}))/Q⌋ for deg P < r | Proved (it is ⌈p/Q⌉ = ⌊(p+Q−1)/Q⌋ for every integer p, Q >= 1, including negative p). 18000 exact cases | B1 |
| 3 | Zero-prefix removal (p. 17) commutes with truncation and with coefficientwise division | Proved (⌊0⌋ = ⌈0⌉ = 0). Gives identical results in 300 cases, including v_A + v_B >= n | B9 |
| 4 | (2.24) reversed correlation, p. 17 | Proved by index substitution r' = n−1−r. Exact on 200 random signed cases, for all j | B10 |
| 5 | (2.25) and "converted outwards by one predecessor or successor after binary scaling", including gradual underflow, p. 17 | Proved by reading. In the normal range RN has error <= ½ spacing. In the subnormal range the two roundings (int → double, then the scaling) together err by less than 2⁻¹⁰⁷⁴, which is the subnormal spacing. Exact on 28000 cases, 9614 of them with a subnormal result | B11, B12 |
| 6 | "Enclose all four endpoint products and take their interval hull" (each product rounded outward) | Proved (pred(fl(y)) <= y for RN, including underflow to 0). Exact on 20000 interval pairs that include subnormal and underflowing products | B14 |
| 7 | Reduction rule: lower = pred(fl(s − fl(γ_r t))), upper = succ(fl(s + fl(γ_r t))), γ_r = ru/(1−ru) computed in RN | Proved here (chain below). Every link checked exactly on 1294 reductions | C1, C2 |
| 8 | (2.26) for 1 <= r <= 98264, the numerator formula, and the lower bound 1 − (M²+M)u − 3Mu² − 2M²u³ > 0 at M = 98264 | Computed exactly, for all r (not only at M) | A1-A6 |
| 9 | "ru and 1 − ru are exactly representable" | Computed for all r <= 98264. The computed γ̂_r is the RN quotient, with relative error <= u | A8, A9 |
| 10 | 2.3.1 signed shell sums: "neither operation replaces signed shell coefficients by absolute values"; the sum of complete squares is an upper bound | Checked by reading only. This is the (2.18)/(2.19) prefix argument, already verified in `notes/oai186-contractions-check.md` §3C | none |
| 11 | "Their positive coordinate endpoints are fixed before any signed polynomial is expanded … one coherent positive measure" (p. 17; also p. 11) | Checked by reading. The true form ∫\|F\|² dK^⊗d is increasing in each K_j. Interval-enclosing each moment M_η(K) between M_η(K⁻)⁻ and M_η(K⁺)⁺ and then contracting with the signed Q_η by interval arithmetic encloses the true value. Using one fixed array (K⁻ or K⁺) per endpoint is also sound. Both readings are sound; they differ only in tightness | none |
| 12 | "validated as in Lemma 2.1" (series tails for log and exp, p. 11) | Certain arb comparisons at 135 (v, M) pairs. The bounds are also elementary by reading (geometric majorant of the tail) | D1 |

**Proof chain for claim 7, in my words, checked exactly link by link (C2).** Let S = Σx_j, T = Σ|x_j|, u = 2⁻⁵³, and
let r be the number of summands.

1. Any summation tree satisfies |s − S| <= γ_{r−1} T. A subnormal sum is exact, so the model fl(a+b) = (a+b)(1+δ)
   holds without an underflow term.
2. t >= (1−u)^{r−1} T >= (1 − γ_{r−1}) T. This is Bernoulli's inequality (A11).
3. γ̂_r >= (1−u) γ_r (A9). Also fl(γ̂_r t) >= (1−u) γ̂_r t − 2⁻¹⁰⁷⁵, where the 2⁻¹⁰⁷⁵ term appears only when the
   product is subnormal.
4. For any real y, pred(RN(y)) <= y − 2⁻¹⁰⁷⁵. This holds because RN(y) is within half a spacing of y, and every
   spacing is at least 2⁻¹⁰⁷⁴. The outward step therefore absorbs both the underflow term of link 3 and the rounding
   of the final addition. This is the PDF's "absorbed … by the adjacent endpoint".
5. Combining links 1-4: lower <= s − (1−u)² γ_r (1−γ_{r−1}) T <= s − γ_{r−1} T <= S, where the middle step uses
   (2.26). The upper endpoint is symmetric. Even the non-strict form of (2.26) suffices.

## 2. Numbers

- (2.26) holds exactly iff r <= r* = 94,906,265 ≈ 9.49·10⁷. The numerator 1 + c₁r + c₂r² has c₁, c₂ < 0, so it is
  strictly decreasing for r >= 0 (A6). This makes one check at the largest length sufficient.
- At r = 98264 the left side of (2.26) is ≈ 1.11·10⁻¹⁶ (relative margin ≈ 1/r). The numerator is
  0.999998927978…, and the printed lower bound has the same value to 15 digits.
- The adversarial sum [1, u × (r−1)] reaches |s − S| = 1.0000 γ_{r−1} T. So the tree bound is tight to first order,
  and the factors (1−u)² and (1−γ_{r−1}) in (2.26) are genuinely needed. The margin comes only from using γ_r in place
  of γ_{r−1}.
- Machine hypotheses on this machine: 1,745,854 binary64 additions and multiplications (Sec. C), 80,000 products
  (B15), and all int → double and ldexp conversions (B13) agree with an independent exact round-to-nearest-even
  oracle with gradual underflow.

## 3. Negative controls (19, all caught)

| Group | Controls |
|---|---|
| (2.26) algebra | perturbed numerator coefficient (4r²−2r); r = 10⁸ > r*; γ_{r−1} in place of γ_r |
| (2.22)-(2.23) | ceil in the lower product; floor in the upper product; negative lower endpoints; upper endpoints in the lower product; plain floor as upper division |
| Zero prefix and (2.24) | shift not restored; correlation without the reversal |
| Conversion and products | no outward step; outward step *before* a subnormal scaling (the wrong order fails); floor in place of ceil for v₊; endpoint products without the outward step |
| Reductions | correction γt/4; γ computed for r/2 terms; plain fl sum with no correction and no outward step (each fails on [1, u × k]) |
| Lemma 2.1 | halved log-tail bound |
| (2.3) | window of M−1 terms (R₁₃ < ρ(13/12) at M = 12) |

## 4. Readings where the extraction was unclear

1. (2.22) and (2.23): pdftotext loses the brackets. The rendered p. 16 shows ⌊A⁻B⁻/Q⌋, ⌈A⁺B⁺/Q⌉ and
   ⌈P/Q⌉ = ⌊(P + (Q−1)(1+…+X^{r−1}))/Q⌋.
2. "Enclose all four endpoint products": I read this as each binary64 product rounded outward by one pred/succ,
   then the hull. The authors' `interval_multiply` does the same (§6).
3. The r in (2.26) is the number of summands in one binary64 reduction. In the code this is at most n = 98264;
   reductions across signatures are combined in arb (§6).
4. The order in the conversion is: convert, scale, then step outward. The reverse order can fail in the subnormal
   range (negative control B12n).

## 5. Secondary: the renewal majorant (2.3), p. 12

**Proved for every M >= 2, by reading.** For j > M, put u = j/M > 1. Then uρ(u) = ∫_{u−1}^{u} ρ <=
(1/M) Σ_{a=j−M}^{j−1} ρ(a/M) by a left Riemann sum of the nonincreasing ρ. By induction this is
<= (1/M) Σ R_a = (j/M) R_j. The base case is R_j = 1 = ρ(j/M) for j <= M. The 10⁻⁴⁰ tail is valid because ρ is
nonincreasing. The argument does not depend on M, so it covers the 8 renewal bins (L ∈ {3, 6, 12, 25, 50}) and any
delay bin with M >= 64 that falls back to renewal.

Computed:

- The interval-carried scheme of p. 12 contains the exact rational R_j for M = 2..63 (12090 values) (E1).
- R_j > ρ(j/M) is certain on (M, 2M] for every M <= 63 (E2), and on (2M, 3M] for M ∈ {3, 6, 12, 25, 50} via
  acb.integral (E5). The closed form for ρ on [2, 3] was self-tested against the integrated delay equation (E6).
- The lower endpoints stay positive up to the switch for every M <= 63 (E3; j* = 88, 166, 319, 652, 1292 for
  M = 3, 6, 12, 25, 50, the same values as in the Lemma 2.3 note).
- For M ∈ {64, 93, 300, 1000, 4096, 24270} the lower endpoints stay positive for all j < 98304 or until the switch
  (E4).

**Fact not stated in the PDF.** The interval width of the sliding sum grows through cancellation. At 160 bits the
relative width reaches about 2·10⁻³ for M = 4096 at j = 98303 (R ≈ 2·10⁻³⁷) and about 10⁻³ for M = 24270. This
costs precision only: the upper endpoint is still a valid majorant, and positivity was never lost in the tested M.

## 6. Comparison with the authors' script (opened after the output was saved)

In `code/third_party/openai186/prime_gap_186_certificate.py` I read lines 610-830, 1130-1210, 1640-1666 and
1890-1965. They agree with the reading above on every point:

- **Reductions.** `outward_sum` computes γ = len·u/(1 − len·u) in binary64 and returns
  `nextafter(sum(low) − γ·sum(|low|), −inf)`, symmetrically for the upper endpoint. Its arguments are arrays of
  length n = 98264 or masked subsets. Sums over signatures and shells are accumulated as arb balls.
- **Slack check.** `_verify_directed_reduction_range(n)` checks the (2.26) slack exactly at the maximum only, and
  requires n < 2²⁶. A check at the maximum suffices by the monotonicity in A6, and 2²⁶ ≈ 6.7·10⁷ < r*.
- **Fixed-point products.** `PositiveFixedPolynomial.multiply` uses `mul_low(...) // 2^b` for the lower endpoint
  and adds (2^b − 1)·(1+…+X^{len−1}) before division for the upper. That is (2.22)/(2.23).
- **Conversions.** `from_arb` takes ⌊·⌋ and ⌈·⌉ of the exact arb endpoints and clips the lower one at 0.
  `_outward_scaled_positive_integer` uses the prefix threshold of 1000 bits, then `ldexp`, then `nextafter`. That
  is (2.25) with the order convert, scale, step outward.
- **Interval operations.** `interval_multiply` is the four-product hull with an outward step. Additions take one
  outward step, and scaling is only by 1 or 2.
- **Environment.** `_cap_check_environment` checks radix 2, 53 bits, FE_TONEAREST and gradual underflow. These are
  "the machine hypotheses".
- **Renewal.** `_low_positive_dickman` uses the delay branch for cutoff >= 64 and falls back to renewal on an
  ArithmeticError. The window is initialised to arb(M). It switches to the 10⁻⁴⁰ ball when
  value.upper() <= floor.lower(). It updates with `window += value − values[j−M]`, an order that is immaterial
  in interval arithmetic.

There is no discrepancy. One extra test was run separately (`/tmp/claude-0/oai186-sec23/fltest.py`, not part of the
counts): the code also converts arb endpoints with `float(arb.lower())` plus one outward step (`float_interval`),
and this enclosed the exact value in 200,000 random cases, including subnormal ones. The PDF does not describe
this conversion beyond "converted outwards".

## 7. Not covered

- The production run itself: the values of I_H, J and the 97 component bounds, and whether every reduction there
  has r <= n. The second is a fact about the code, as read in §6, and was not observed at run time.
- The correctness of FLINT/Arb, of the FLINT signed-FFT correction (PR 2790), and of numpy's `np.sum`. I assume
  `np.sum` is a tree of round-to-nearest additions; any such tree is covered by the proof.
- That overflow does not occur. The PDF says this is checked in the producing process, and the code checks
  `isfinite`.
- Lemma 2.1 beyond the 135 sampled (v, M) pairs and the reading. Lemma 2.2 and the delay acceptance tests.
- Layer-difference clipping (`_cap_positive_difference`): read in the code only. It is valid given the positivity
  of layer measures that the PDF states.
- Renewal (2.3): numerical checks only for M <= 63 and six larger M. The general proof covers all M.

## 8. Commands

```
pdftotext -layout code/third_party/openai186/short_gaps_numerics.pdf /tmp/claude-0/oai186-sec23/oai.txt
/usr/bin/python3 code/oai186_directed_check.py > code/oai186_directed_check.out   # 31 checks, 0 failures; 19/19 controls
```

## Independent spot check (Session 60, main session, 27 Nov 2026)
Re-run of the program here: identical output apart from timing (54.2 s, 48 MB). Separately, a five-line exact
Fraction computation written in the main session (reading (2.26) as (1-u)^2 γ_r (1-γ_{r-1}) >= γ_{r-1}, γ_r = ru/(1-ru),
u = 2^-53, as in link 5 above) gives: true at r = 98264, true at r = 94,906,265, false at r = 94,906,266, i.e. the
same threshold r* as §2. One helper program plus this spot check; not a second full program for the rest of §1.
