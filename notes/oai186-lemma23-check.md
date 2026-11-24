# Rung 186: check of Lemma 2.3 of [14] (Eulerian cell kernels of the low bins)

Source [14]: OpenAI, "Numerical certificate for prime gaps at most 186", dated 30 August 2026,
`code/third_party/openai186/short_gaps_numerics.pdf`, read with `pdftotext -layout` (extract kept in the scratch
directory only, not committed). Page numbers are the printed page numbers (the number at the foot of each page).

Script: `code/oai186_lemma23_check.py`, output `code/oai186_lemma23_check.out`. Every decision is exact
(`fractions.Fraction`, integers) or a certain comparison of python-flint 0.9 arb balls (log, exp, Ei, Li2,
`acb.integral`). Floats are used only for printing. **41 checks, 0 failures**, about 30 s wall and 136 MB peak RSS
(`ru_maxrss`).

**"Lemma 2.3" and "(2.3)" are different objects.** Equation (2.3) (p. 12) is the renewal majorant R_j of the
Dickman function for small caps. Lemma 2.3 (p. 13, "Eulerian cell kernels") is the statement that the polynomials
B_θ, M_θ of (2.4)-(2.7) majorise the tilted (and count-marked) coordinate measures of a low bin. Lemma 2.3 uses
(2.3) through d*_j in the renewal branch, so (2.3) is checked here as an input (§4 [4]). The line in
`notes/sources-186-forms.md` ("the renewal majorant (2.3) is used only for the small source-loss caps") refers to
the equation. It is consistent with what is found here: (2.3) is used only for the 8 low bins with L < 64.

**Verdict: verified as stated, under the readings in §5.** No repair is needed. The proof is a short
measure-theoretic argument. Each step was checked by reading (§3), and every finite or combinatorial claim it rests
on was checked by computation (§4): the Eulerian carry formula, the generating-function identity for T_e, the
truncation and remainder, and the (2.4) data of all 61 bins. In addition, an end-to-end rigorous comparison on the
actual 61 bins (§4 [5]) found the true cell masses below the kernel coefficients on 1842 cells. These are the cells
with at most one large fragment (j < 2L). Cells with two or more large fragments are covered by the proof and by
the exact small-instance checks, not by an end-to-end evaluation (§6).

## 1. Definitions (with page references)

- p. 1. ν_c := e^γ c L(Π_c), with Π_c the Poisson process on (0, c] with intensity dv/v. Its total-size
  pushforward is ν̄_c(dt) = ρ_D(t/c) dt. "νc restricted to {max X ≤ b} = νb."
- p. 2, (1.3). N = 98304, h = S/N, cells C_j = [jh, (j+1)h).
- p. 9, (1.36)-(1.37). The low-bin Palm majorant Σ_{p ∈ X∩(ℓ,u]} exp(θ{s + (m−1)u − U − L_{≤ℓ}}), followed by
  "Lemma 2.3 supplies every small-fragment completion and every possible number of remaining large fragments."
  Sec. 1.5.1 gives the 61 low bins (endpoint lists U_1..U_6) and slopes θ.
- p. 12. D_c(t) := ρ_D(t/c) for t ≥ 0, 0 for t < 0. Lemma 2.2: the delay recurrence (2.1) gives an upper
  sequence d̄_j ≥ D_c(jh) for c = Mh. (2.3): R_j = 1 for j ≤ M, R_j = (1/j) Σ_{a=j−M}^{j−1} R_a for j > M, with
  M ≥ 2. Then R_j ≥ ρ_D(j/M), the 10^−40 tail, and the branch rule "delay when M ≥ 64 and its acceptance tests
  pass, otherwise renewal". d*_j(Mh) is the chosen majorant.
- p. 12, (2.4). For a low bin (ℓ0, u0] with hard cap z0: L = ⌊ℓ0/h⌋, H = ⌈u0/h⌉, K = ⌈z0/h⌉,
  (ℓ, u, z) = (Lh, Hh, Kh), and the data satisfy 2 ≤ L < H ≤ K ≤ N. Q = Σ_{a=L}^{K−1} X^a/a,
  M = Σ_{a=L}^{H−1} X^a/a, D_θ = h Σ_{j<N} d*_j(ℓ) e^{−θjh} X^j.
- p. 13, (2.5)-(2.7). E_r = (1/r!) Σ_{a=0}^{r−1} Eu(r,a) X^a with the Eulerian recurrence (2.5), and
  R_r = 1 + ... + X^{r−1}. q_r = Q^r/r!, J = min(32, ⌊(N−1)/L⌋). T_e = Σ_r q_r R_{r+e+1} =
  (exp Q − X^{e+1} exp(XQ))/(1−X) mod X^N, and T̂_e = Σ_{r≤J} q_r E_{r+e+1} + ↑(T_e − Σ_{r≤J} q_r R_{r+e+1}).
  B_θ = D_θ T̂_0 and M_θ = D_θ M T̂_1.
- **p. 13, Lemma 2.3** and its proof. References: [7, Thm. 5.2] (independence of disjoint Poisson restrictions) and
  [7, Thm. 4.5] (reduced Mecke formula).
- After the lemma (p. 13): "Fix the upward endpoints of w_j^{(e)} [X^j]B_θ/h ... Apply (1.38) at the full index
  before erasure." This is the downstream use. It is not part of the lemma.

## 2. Statement in my notation

Fix a low bin with (L, H, K, θ) as above, θ > 0. For a coordinate X with fragment cap z, let s(X) be the total of
its fragments ≤ ℓ and t(X) its total. Define two positive measures on totals:

    μ_B := push_t( e^{−θ s(X)} ν_z(dX) ) = (e^{−θt} D_ℓ(t) dt) * exp_*(1_{(ℓ,z]}(v) dv/v),
    μ_M := push_t( N_{(ℓ,u]}(X) e^{−θ s(X)} ν_z(dX) ) = 1_{(ℓ,u]} dv/v * μ_B.

The claim is μ_B(C_j) ≤ [X^j]B_θ and μ_M(C_j) ≤ [X^j]M_θ for every 0 ≤ j < N. Here exp_*(μ) = Σ_r μ^{*r}/r! is the
convolution exponential.

## 3. The proof, line by line (checked by reading; finite parts also by computation)

1. "ν̄_z = ν̄_ℓ * exp_*(1_{(ℓ,z]} dv/v): the void factor ℓ/z cancels the change in normalization." Π_z is the
   independent union of Π_ℓ and the restriction of Π_z to (ℓ, z]. The law of the latter is
   e^{−log(z/ℓ)} exp_*(1_{(ℓ,z]} dv/v) = (ℓ/z) exp_*(·). Multiplying by e^γ z gives
   e^γ ℓ L(Π_ℓ) * exp_*(·) = ν_ℓ * exp_*(·). **Correct.** An independent check by Laplace transforms:
   log(c ρ̂(cs)) = log c + γ + ∫_0^{cs}(e^{−w}−1)/w dw, so the ratio for c = z and c = ℓ is
   exp(∫_ℓ^z e^{−sv} dv/v). Script [3] also checks the density identity D_2 = D_1 * exp_*(1_{(1,2]} dv/v)
   rigorously at 8 points of (0, 3), using closed forms of ρ on [0, 3] (Li2 on [2, 3], itself cross-checked against
   the delay equation by `acb.integral`). The tilt e^{−θ s} acts only on the Π_ℓ factor, which gives the
   e^{−θt} D_ℓ(t) factor.
2. "Reduced Mecke marking adds the designated factor." E Σ_{p∈Π∩A} f(p, Π) = ∫_A E f(v, Π ∪ {v}) dv/v. The
   designated v > ℓ is not part of s, so μ_M = 1_{(ℓ,u]} dv/v * μ_B. **Correct.** (Standard; checked by reading.)
3. "On C_a, dv/v is bounded by constant density 1/(ah), of mass 1/a." Here a ≥ L ≥ 2 > 0 ([0]). The cells
   C_L..C_{K−1} = [Lh, Kh) cover (ℓ, z] up to the null set {Kh}. **Correct.**
4. "On C_j, the tilted low density is bounded by d*_j(ℓ) e^{−θjh}." Both D_ℓ and e^{−θt} (θ > 0) are
   nonincreasing, so the supremum on C_j is at jh. The step needs d*_j ≥ D_ℓ(jh) = ρ_D(j/L). This comes from
   Lemma 2.2 in the delay branch and from (2.3) in the renewal branch. (2.3) holds by the left-Riemann argument:
   (j/M)ρ(j/M) = ∫_{(j−M)/M}^{j/M} ρ ≤ (1/M) Σ_{a=j−M}^{j−1} ρ(a/M), then induction. The 10^−40 tail holds because
   ρ is nonincreasing. **Correct.** See [4] for the rigorous spot checks.
5. Comparison of positive measures: if 0 ≤ μ_i ≤ μ_i^+, then μ_1 * ... * μ_k ≤ μ_1^+ * ... * μ_k^+ and
   exp_*(μ) ≤ exp_*(μ^+). (Implicit in the proof; elementary.)
6. "For r uniform fractional cell coordinates, unit-cube inclusion-exclusion gives carry mass
   (1/r!) Σ_{b=0}^{a+1} (−1)^b C(r+1,b)(a+1−b)^r = [X^a]E_r." This is the Irwin-Hall cell mass. **Correct.** [1]
   checks it exactly against the recurrence (2.5) for r ≤ 60, and against an independent exact piecewise-polynomial
   convolution for r ≤ 14.
7. "Thus the carry is E_{r+1}, or E_{r+2} with a designated fragment." There is one small-part coordinate plus r
   large fragments, plus one if designated. Each is uniform on its cell after step 3/4. So the r-th term of μ_B is
   majorised coefficientwise by D_θ q_r E_{r+1}, and that of μ_M by D_θ M q_r E_{r+2}. **Correct.** [2] checks this
   end to end on an exact instance by direct piecewise-polynomial convolution of the cell-uniform measures (no
   Eulerian numbers involved).
8. "Since 0 ≤ E_r ≤ R_r coefficientwise, the replicated remainder bounds every omitted term." This uses
   Σ_{r>J} q_r E_{r+e+1} ≤ Σ_{r>J} q_r R_{r+e+1} = T_e − Σ_{r≤J} q_r R_{r+e+1}, together with the closed form
   Σ_r Q^r/r! (1 − X^{r+e+1})/(1−X) = (e^Q − X^{e+1} e^{XQ})/(1−X). **Correct.** [1] and [2] check this exactly.
9. "Terms with rL ≥ N vanish, so the construction is finite." Q has order L, so q_r ≡ 0 mod X^N when rL ≥ N.
   If J = ⌊(N−1)/L⌋, the remainder is exactly 0. **Correct.** [2] checks both.

## 4. Finite claims checked by computation (script sections)

| § | Claim | Result |
|---|-------|--------|
| 0 | 61 low bins rebuilt from Sec. 1.5.1. "2 ≤ L < H ≤ K ≤ N" (min L = 3, max K = 49152). (Lh, Hh] ⊇ (ℓ0, u0]. θ is a positive integer. z0 := z_G equals the largest mask cap (1.5) on the group's retained cells (1.25), so the true per-fragment cap is ≤ Kh. Branches: renewal for L ∈ {3, 6, 12, 25, 50} (8 bins), delay candidates for 25 distinct L ∈ [93, 24270]. 24 bins have J = 32 < ⌊(N−1)/L⌋ (nonzero remainder), 37 are exact | 8 PASS |
| 1 | (2.5) equals the inclusion-exclusion of the proof, r ≤ 60. Degree r−1, row sums r!, 0 ≤ E_r ≤ R_r. Irwin-Hall cell masses by independent exact piecewise convolution, r ≤ 14 | 6 PASS |
| 2 | Six exact instances (N ∈ {40, 70, 75, 100}, L ∈ {2, 3, 4, 5, 13}, random positive D), with J = 32 < ⌊(N−1)/L⌋ in three of them. T_e closed form. q_r ≡ 0 for rL ≥ N. Omitted sum ≥ 0. T̂_e ≥ complete Eulerian sum, with equality when J = ⌊(N−1)/L⌋. Independent piecewise convolution of the cell-uniform majorant measures (N = 14) equals D Σ q_r E_{r+1} and D M Σ q_r E_{r+2}, and is ≤ B, M | 7 PASS |
| 3 | Poisson split (total masses; rigorous pointwise density identity at 8 points). ρ closed form on [2, 3] matches the delay equation. Mecke (by reading) | 4 PASS |
| 4 | (2.3) exactly for every M = 2..63: positive, sliding window = definition, the 10^−40 switch is reached (j* = 88, 166, 319, 652, 1292 for M = 3, 6, 12, 25, 50). R_j ≥ ρ(j/M) rigorously for all j ≤ 3M (min relative slack 1.25·10^−4). Delay recurrence (2.1) as printed, 160-bit, for all 25 delay caps: ordered, nonincreasing on j ≤ 3M; d̄_j ≥ ρ(j/M) at 1376 sampled j ∈ [M, 3M]; the left-Riemann induction (by reading) | 7 PASS |
| 5 | End to end, all 61 bins: rigorous true μ_B(C_j), μ_M(C_j) (closed forms with Ei, acb.integral) ≤ [X^j]B_θ, [X^j]M_θ on 1842 cells j < 2L (all such cells for L < 64; 29 including boundary cells otherwise). The smallest relative slack is 1.5·10^−4 (O_2 L10, j = 2L−1) | 2 PASS |
| 6 | Authors' script (comparison only): same 61 (low, high, slope) and hard caps. `eulerian_carry_polynomial` contains E_r. The renewal arrays contain R_j and then 10^−40. The delay array equals ours (cap 93, j ≤ 3M). `_low_eulerian_envelopes` dominates our exact B, M on the instances of [2]. `source_low_measures` index ranges and low cells match (2.4) (source text) | 7 PASS |

## 5. Readings taken

1. **exp_*** is the convolution exponential Σ μ^{*r}/r!. A **physical-cell mass** is the mass of C_j = [jh,
   (j+1)h), 0 ≤ j < N. Only these readings make the proof's carry argument meaningful.
2. **z0** (the "hard cap", undefined in (2.4)) is the group cap z_G of (1.24), as in the authors' `hard_cap`.
   Lemma 2.3 is correct for any z0 ≥ the true per-fragment cap. [0] checks that z_G is the largest cap met by the
   group's retained cells. A smaller z0 would make the use of the lemma, not the lemma itself, invalid.
3. **"In the delay branch these are d_j"**: the overbar is lost in extraction. It must be the upper sequence d̄_j
   of (2.1). The lower one is not a majorant, and the authors' code returns `.upper`.
4. **The 10^−40 switch**: "only once its upper bound is at most a lower bound for 10^−40" is read as replacing R_j
   from the first such j* on, j* included. This is what the code does. Both possible readings (j* included or
   excluded) are valid, since 10^−40 ≥ R_{j*} ≥ ρ.
5. **Tilt cutoff**: the lemma tilts the fragments ≤ ℓ = Lh, not ≤ ℓ0. That ℓ ≤ ℓ0 only enlarges the bound was
   checked in the Lemma 1.5 note (row 6). It is not repeated here.

No alternative reading of the lemma text makes it false. The only freedom that could matter is z0 (reading 2), and
that concerns the use of the lemma.

## 6. Facts the PDF does not state, and what is not checked

Facts not stated in the PDF:
- 8 bins use the renewal branch (L ∈ {3, 6, 12, 25, 50}). 24 of 61 bins carry a nonzero replicated remainder.
- The end-to-end slack is small (≥ 1.5·10^−4 relative on j < 2L). The kernels are tight there, not generous.

Not checked:
- Whether the delay acceptance tests pass on the full range j < N for each of the 25 delay caps. I checked
  j ≤ 3M only. If they fail, the code falls back to (2.3), which is valid for every M ≥ 2. So the lemma holds in
  either case, but which branch is used for those bins is not determined here.
- Lemma 2.2 itself. It was spot-checked against rigorous ρ on [M, 3M] only.
- End-to-end evaluation on cells with two or more large fragments (j ≥ 2L). These rest on steps 5-8 of §3 and on
  the exact instances of [2].
- The authors' production arb evaluation of the N = 98304 kernels (outward rounding of exp(Q) etc.). I compared
  their routines only on small instances.
- The Poisson/Mecke theorems [7] themselves (standard; spot-checked numerically in [3]).

## 7. Commands

```
pdftotext -layout code/third_party/openai186/short_gaps_numerics.pdf <scratch>/oai.txt   # not committed
/usr/bin/python3 code/oai186_lemma23_check.py > code/oai186_lemma23_check.out            # 41 checks, 0 failures
bash -c 'time /usr/bin/python3 code/oai186_lemma23_check.py > /dev/null'                 # ~30 s wall; RSS 136 MB
```
