# Rung 186: second, independent check of Lemma 2.3 of [14]

Source [14]: OpenAI, "Numerical certificate for prime gaps at most 186", 30 Aug 2026,
`code/third_party/openai186/short_gaps_numerics.pdf` (read with `pdftotext -layout`; printed pages 10, 12, 13, 14
also rendered at 150 dpi to confirm (1.40)-(1.43), (2.1)-(2.8) and the bars in (2.1)). Page numbers are the
printed ones.

Script: `code/oai186_lemma23_check2.py`, output `code/oai186_lemma23_check2.out`. Exact arithmetic
(`fractions.Fraction`, `sympy`, flint `fmpq_poly`) and python-flint 0.9.0 `arb` balls (256 bits); floats only in
printed ratios. No repository code or data was used; every number is recomputed from the PDF.
**3,798,432 checks, 0 failures, 170 s, peak RSS 508 MB.** Sections 1-5 were written after the script and its
output were final, and before I opened the first program's files.

**Verdict: verified as stated**, under the readings in section 2. One point of the set-up worth recording: the
choice between the delay and renewal kernel is not cosmetic. With the PDF's acceptance tests the delay recurrence
is rejected for 33 of the 53 bins with M = L >= 64 (section 4). Lemma 2.3 holds with either kernel.

## 1. Statement and definitions used

- p. 13, **Lemma 2.3**: "The coefficients of B_θ, M_θ majorize, respectively, the physical-cell masses of
  (e^{−θt} D_ℓ(t) dt) ∗ exp_∗(1_(ℓ,z](v) dv/v) and 1_(ℓ,u](v) dv/v ∗ (e^{−θt} D_ℓ(t) dt) ∗ exp_∗(1_(ℓ,z](v) dv/v).
  No small-fragment mass or high-fragment count is omitted."
- p. 12-13, (2.4)-(2.7): L = ⌊ℓ0/h⌋, H = ⌈u0/h⌉, K = ⌈z0/h⌉, (ℓ,u,z) = (Lh,Hh,Kh), 2 <= L < H <= K <= N;
  Q = Σ_{a=L}^{K−1} X^a/a, M = Σ_{a=L}^{H−1} X^a/a, D_θ = h Σ_{j<N} d*_j(ℓ) e^{−θjh} X^j; Eu(r,a) by (2.5),
  E_r = r!^{−1} Σ Eu(r,a) X^a, R_r = 1 + ... + X^{r−1}; q_r = Q^r/r!; J = min(32, ⌊(N−1)/L⌋);
  T_e = Σ_r q_r R_{r+e+1} = (exp Q − X^{e+1} exp(XQ))/(1−X) mod X^N;
  T̂_e = Σ_{r<=J} q_r E_{r+e+1} + ↑(T_e − Σ_{r<=J} q_r R_{r+e+1}); B_θ = D_θ T̂_0, M_θ = D_θ M T̂_1.
- p. 12, Lemma 2.2 (2.1) delay recurrence and acceptance ("ordered intervals in [0,1] with both endpoint
  sequences nonincreasing"); (2.3) renewal majorant R_j, the 10^−40 floor, the branch rule "delay when M >= 64 and
  its acceptance tests pass, otherwise renewal"; d*_j and its enclosure I_j.
- p. 1: ν̄_c(dt) = ρ_D(t/c) dt. p. 2, (1.3): N = 98304, h = S/N, n = N − 40, C_j = [jh,(j+1)h).
- p. 4-6, (1.13)-(1.24); p. 9, §1.5.1: the 61 low bins (lists U_1..U_6, a_j = (6/5)^j/20) and slopes
  θ = ⌈7/u_j⌉, 120 at (G1, L3), ⌈9/u_j⌉ on G6.

## 2. Readings I had to fix

- "Physical-cell mass" of a measure on total size = its mass on C_j; compared with [X^j] (j < N). "Majorize" is
  checked strictly in balls: rigorous upper bound of the true mass <= lower endpoint of the coefficient ball
  (stronger than comparing with the PDF's upward endpoints).
- The measures use the rounded (ℓ,u,z) = (Lh,Hh,Kh); I check (ℓ0,u0] ⊆ (ℓ,u] and z >= z0, with z0 = z_G (the
  aligned cap of (1.24)) for all 61 bins.
- Kernel branch: delay is used only if (2.1), run to j = N − 1 with M = L, passes the acceptance tests; else
  renewal (exact rationals, with the optional 10^−40 floor). My dyadic recurrence rounds once per step at 2^−160
  (the PDF rounds per operation); either is a valid enclosure.
- J: the PDF's J = min(32, ⌊(N−1)/L⌋). In toys I also use smaller artificial J to exercise the replicated
  remainder; the proof does not depend on the value 32.
- Weights w_j^(e) and the array step ("Fix the upward endpoints of w_j [X^j]B_θ/h ...") are outside the lemma and
  not checked.

## 3. Method, and why it is independent

- **A (data).** Rebuilds S, T0, T1, ρ, e, both ladders (29/43 rows), the six groups (printed z/h, p/h and
  2h < ξ < p <= z re-derived), and the 61 low bins with slopes; checks 2 <= L < H <= K <= N, θ > 0 and the
  rounding containments. L ranges 3..24270, θ 27..133874; J = 32 with truncation active in 24 bins.
- **B (combinatorics, exact).** The recurrence (2.5) against the proof's inclusion-exclusion formula for all
  r <= 70, and against an independent exact piecewise-polynomial convolution of uniform densities (Irwin-Hall
  cell masses) for r <= 12; E_r(1) = 1 and 0 <= E_r <= R_r. The closed form of T_e against an exp computed by the
  ODE recurrence e_n = n^−1 Σ k Q_k e_{n−k} (24 identities on random toy Q), and again exactly inside every exact
  construction below.
- **Rigorous Dickman ρ (my own).** 1 and 1 − log u on [0,2]; on [k,k+1], k >= 2, a power series about k + 1/2
  from uρ' = −ρ(u−1), with an inductive tail bound |c_n| <= K(2/3)^n; accuracy about 1e−50. Validated against the
  dilogarithm closed form on [2,3], the integral equation uρ(u) = ∫_{u−1}^u ρ (monotone Riemann sandwich) and
  literature values ρ(3), ρ(10).
- **C (majorants).** Renewal R_j >= ρ(j/M) (M = 2..40, 30M points) and the delay enclosures d_j <= ρ(j/M) <= d̄_j
  (M = 64, 100, 1000), all rigorous; 21,570 grid points.
- **D (toy end-to-end, the main test).** For 14 toy grids (h from 1/1000 to 2, L = 2..64, θ from 1/100 to 2000,
  renewal and delay branches, J = 0..32 incl. the genuine J = 32 < ⌊69/2⌋ truncation) I compute rigorous upper
  and lower bounds of the TRUE cell masses of both measures directly: on a k-times finer grid (k = 2..16) with the
  sup (inf) of the true ρ(t/ℓ), the true tilt e^{−θt} and the true 1/v, all fragment counts r and no truncation;
  every coefficient of B_θ, M_θ must exceed the upper bound. The Poisson normalization of the proof,
  ν̄_ℓ ∗ exp_∗(1_(ℓ,z] dv/v) = ν̄_z, is checked at θ = 0 by sandwiching ∫_{C_j} ρ(t/z) dt (3 toys, 28 cells).
  Negative controls are detected: dropping the replicated remainder (3 toys), dropping the one-fragment term and
  tilting by the cell infimum e^{−θ(j+1)h} (4 toys each).
- **E (real parameters).** The same comparison with the real h, L, H, K, θ, J and d* of all 61 bins on the prefix
  j < jmax (prefix coefficients of power-series products are exact): jmax = 40L for L <= 25 (r up to 39, so
  the J = 32 truncation and its remainder are exercised, in 21..175 cells per bin), jmax = 2L + 100 otherwise
  (r <= 3). Exact rational T̂_e for L <= 25, arb otherwise.

Independence: the "truth" side never uses the construction (no sup over coarse cells, no J, no remainder, no
closed form, true ρ instead of d*), and the carry law it relies on is checked against an exact convolution.

## 4. Findings

- All 3,798,432 checks pass. Largest ratio true-upper/coefficient: 0.7147-0.9622 for the small-L bins, and
  1 − O(θh) (printed 0.9997-1.0000) on the large-L prefixes, where only the tilt's sup over a cell separates them.
- **Kernel branch.** With +1/(2M³) per step, the upper sequence of (2.1) starts to increase once the lower one has
  reached 0, which violates "both endpoint sequences nonincreasing". On the full grid this happens for every
  M = L <= 9753 among the bins (first rise from j = 553 for M = 93 up to j = 85833 for M = 9753), and not for
  M >= 11704. So **20 bins use the delay kernel and 41 the renewal kernel** (8 forced by L < 64, 33 by rejection).
  The PDF does not say on which j-range acceptance is tested; this count assumes j <= N − 1. The lemma holds with
  either kernel (both are verified majorants), but anyone reproducing the arrays must use the same rule.
- One carry too few (E_{r+e} for E_{r+e+1}) is not detected in the toys: the coarse sup-density slack absorbs it.
  This only shows slack in the bound, not an error; the PDF uses the correct carry.
- The proof's appeal to Poisson-process theorems ([7, Thm. 5.2, 4.5]) is not checked beyond the θ = 0 total-size
  identity.

## 5. Coverage limits

- Real-parameter tests cover prefixes only (up to j < 40L or j < 2L + 100), not all j < N. The omitted-sum
  inequality T_e − Σ_{r<=J} q_r R >= Σ_{r>J} q_r E >= 0 is coefficientwise and is checked exactly wherever it is
  active in the prefixes, so I do not see a mechanism that could fail only for larger j.
- I did not rebuild the full-length (N = 98304) B_θ, M_θ arrays, so the "negative upper endpoint is rejected"
  test is only checked on the prefixes, where the omitted sum is exact and nonnegative.

## 6. Comparison with the first program (notes/oai186-lemma23-check.md, read after the above was final)

- **Verdict: agree** (verified as stated). Same readings: exp_* is the convolution exponential, a physical-cell
  mass is the mass of C_j, z0 = z_G, the delay-branch d*_j is the upper sequence d̄_j. Same data facts: 61 bins,
  L from 3 to 24270, max K = 49152, 24 bins with an active J = 32 remainder, renewal forced for
  L ∈ {3, 6, 12, 25, 50} (8 bins).
- **Kernel branch, an addition rather than a disagreement.** The first program checked the delay acceptance tests
  only on j <= 3M and left open which branch the 53 bins with L >= 64 use (its §6). I ran (2.1) to j = N − 1. It
  fails acceptance for every M <= 9753 and passes for M >= 11704, so 33 of those 53 bins fall back to renewal:
  20 delay and 41 renewal in total. After finishing, I also read the authors' `_low_positive_dickman` in
  `code/third_party/openai186/prime_gap_186_certificate.py`. It runs the recurrence to `count = size − 1` and falls
  back to renewal on any loss of monotonicity, which is the same rule. The validity of the lemma does not depend on
  the branch.
- **10^−40 switch.** The first program (and the authors' code) replace R_{j*} itself. My script keeps R_{j*} and
  switches from j* + 1. Both are valid majorants (the first program's reading 4 says so too). The difference only
  affects the d* values on the prefix of the L <= 25 bins, not any verdict.
- **End-to-end coverage.** The first program compares true masses (closed forms, Ei, acb.integral) with the
  coefficients on 1842 cells with j < 2L, i.e. at most one large fragment. Its smallest slack is 1.5·10^−4
  (O2 L10). Mine uses fine-grid upper bounds and is consistent with that: on the large-L prefixes my ratio rounds
  to 0.9997-1.0000. My Part E goes further on the small-L bins (j < 40L, up to 39 large fragments, the J = 32
  remainder active in 21-175 cells per bin) and to j < 2L + 100 elsewhere. My toys include multi-fragment cells
  and truncated J. So the first program's §6 item "no end-to-end evaluation on cells with two or more large
  fragments" is covered here, on prefixes.
- The Irwin-Hall convolution check (r <= 14 there, r <= 12 here), the T_e closed form and the Poisson split agree.
  The first program also audits the authors' script, which I did not do beyond the branch rule above.
- No disagreement found. I made no change to my script after reading the first program.
