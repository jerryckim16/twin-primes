# Rung 186: check of Lemma 2.4 of [14] (whole-bin Palm envelopes of the rank-two bins)

Source [14]: OpenAI, "Numerical certificate for prime gaps at most 186", dated 30 August 2026,
`code/third_party/openai186/short_gaps_numerics.pdf`. It was read with `pdftotext -layout`, and the extract was kept
in the scratch directory only, not committed. The display (2.9) loses its over- and under-bars in the extraction, so
printed p. 14 was also rendered with `pdftoppm` (300 dpi) and read from the image. Page numbers are the printed page
numbers.

Script: `code/oai186_lemma24_check.py`, output `code/oai186_lemma24_check.out`. Every decision is either exact
(`fractions.Fraction`, integers, including the Lemma 2.2 recurrence in exact dyadic integers) or a certain
comparison of python-flint 0.9.0 arb balls. Floats are used only for printing. **36 checks, 0 failures.** A run
takes about 32 s wall and 776 MB peak RSS (`ru_maxrss`).

**Verdict: verified as stated, under the readings in §5.** No repair is needed. Lemma 2.4 is the q-uniform
version of the rank-two Palm bound (1.40)-(1.41). The arrays P, A, B, C of (2.9) bound the four coordinate roles
of the ring (1.42) uniformly over the bin (a, b]. The A and C arrays are then multiplied by the Lemma 1.7 fractions.
The checks were:
- each proof step, by reading (§3);
- every index and cap claim, exhaustively over all 30 x 98264 (bin, cell) pairs, in integers;
- the (2.9) arrays against a rigorous, independently computed Dickman ρ, on 36 325 sampled (bin, cell) pairs as
  whole-bin suprema and at 326 925 exact (q, t) points;
- an end-to-end check of the q-integrated majorisation on 155 two-coordinate instances from the actual bins;
- the authors' implementation, which on two bins agrees with our reading of (2.9) to 3·10^-44.

**Two points to note.** (i) The array letters of (2.9) do not match the letters A, B of (1.40)/(1.41) and of the
proof: (2.9)'s A is the proof's B on the owner coordinate (§5, R1). (ii) The arrays are fairly tight. In the
end-to-end test the rigorous upper bound of the true mass reaches 0.949 of the Lemma 2.4 bound on one instance.

## 1. Definitions (with page references)

- p. 1. ν_c := e^γ c L(Π_c), where Π_c is the Poisson process on (0, c] with intensity dv/v. The total-size density
  is ρ_D(t/c), and ν_c restricted to {max X ≤ b} is ν_b.
- p. 2, (1.3). N = 98304, h = S/N, n = N − 40, cells C_j = [jh, (j+1)h).
- p. 9, Sec. 1.5.1. The 30 rank-two bins (q0 + t_{j−1}(z_G − q0), q0 + t_j(z_G − q0)], with q0 = U_G/(m_G+1).
  These are the bins (a, b] of (2.9).
- p. 10, Sec. 1.5.3:
  - (1.39) gives the rank-two condition q > U/(m+1), p > d(q), q ≤ z. "Omitting p_G, ξ from the maximum enlarges
    the event and gives the positive kernels in Lemma 2.4."
  - D_c(t) := ρ_D(t/c).
  - (1.40) is the one-largest Palm density Σ_j ∫ (A_j Π_{i≠j} A_i − B_j Π_{i≠j} B_i) dq/q. Here A_i = D_q(t_i) and
    B_i = D_{d(q)}(t_i), with t_j shifted to t_j − q on the coordinate holding q.
  - (1.41) is the positive upper bound (A_j − B_j) Π A_i + B_j Σ_i (A_i − B_i) Π_{v≠i,j} A_v.
  - (1.42): Q = P + xA + yB + xyC. Here P is ordinary, A is the coordinate holding the largest fragment, B is a
    secondary fragment in a different coordinate, and C is both in the same coordinate.
- p. 11, Lemma 1.7: the feasible-logarithmic-mass fractions. They were checked in `notes/oai186-lemma17-check.md`.
- p. 12, Lemma 2.2 and (2.1): the endpoint sequences d̲_j ≤ D_c(jh) ≤ d̄_j for c = Mh. p. 12 also gives the grid caps
  c^- = h⌊c/h⌋ (lower) and c^+ = h⌈c/h⌉ (upper), "since D_c increases with c".
- **p. 14, (2.9).** For a largest-fragment bin (a, b] with U/(m+1) ≤ a < b ≤ z0 < U and m ∈ {2, 5/2}:
  - r(q) := (U − q)/m ≤ q, r_- := (U − b)/m, r_+ := (U − a)/m;
  - s^-_j := max(0, j − ⌈b/h⌉), s^+_j := max(0, j + 1 − ⌊a/h⌋), t^+_j := (j+1)h, ŵ_j^{(e)} := ↑w_j^{(e)};
  - β_j := 0 for jh < b, and β_j := d̲_{s^+_j}(r_-^-) otherwise.

  "With upward caps in upper grids and downward caps in lower grids":

      P_j := ↑(ŵ_j d̄_j(b^+)),            A_j := 1[t^+_j > a] ↑(ŵ_j d̄_{s^-_j}(r_+^+)),
      B_j := ↑(ŵ_j [d̄_j(b^+) − d̲_{j+1}(r_-^-)]_+),   C_j := 1[t^+_j > a + r_+] ↑(ŵ_j [d̄_{s^-_j}(b^+) − β_j]_+).

  Differences are enclosed upward before clipping.
- **p. 14, Lemma 2.4** and its proof (quoted in substance in §2 and §3).
- Downstream use (p. 15, (2.16)): the Palm ring P + xA + yB + xyC with coefficient [xy]. The external factor Λ is
  log(q+/q−) for a rank-two bin. It appears once in each of (2.17), (2.19) and (2.21).

## 2. Statement in my notation

Fix a bin (a, b]. Let q ∈ (a, b] be the largest fragment and r = r(q). The four coordinate densities of the
q-integrand ((1.41), equivalently [xy] of the ring (1.42)) are:

| role (ring) | density at coordinate total t | (2.9) array |
|---|---|---|
| ordinary P | D_q(t) | P_j |
| owner without secondary, x A | D_r(t − q), t ≥ q | A_j |
| secondary elsewhere, y B | D_q(t) − D_r(t) | B_j |
| owner with secondary, xy C | D_q(t − q) − D_r(t − q), t ≥ q | C_j |

The claim is: for every q ∈ (a, b] and every t ∈ C_j, each density is ≤ the corresponding array divided by ŵ_j.
For the owner roles this is taken with t ≥ q. The arrays are bounds on densities, so the cell mass is at most h
times the array. Consequently

    ∫_{(a,b]} [(1.41) integrated over a cell tuple] dq/q
        ≤ Λ · [xy] Π_v (P + x A λ(t^+) + y B + xy C λ(min{t^+, (m t^+ − U)/(m − 1)})) · h^d.

This uses Lemma 1.7: the fractions are the feasible q-parts, and each monomial has exactly one owner factor.

## 3. The proof, line by line

1. "Off the coordinate containing the largest fragment use A = D_q(t), B = D_{r(q)}(t); on that coordinate use
   A = D_q(t − q), B = D_{r(q)}(t − q), with t ≥ q." This is (1.40) with d(q) replaced by r(q) ≤ d(q). Omitting
   p_G and ξ enlarges the event. The Lemma 1.7 check found d(q) = r(q) on every bin anyway.

   (1.40) itself follows from Mecke's formula with the void probability:
   ν_z restricted to {largest fragment = q} = (ν_q ⊕ {q}) dq/q, because e^γ z · (q/z) = e^γ q, and ν_z|{max ≤ q} = ν_q.
   **Correct; checked by reading.**
2. "All differences are positive since r(q) ≤ q." D_c(t) = ρ(t/c) is nondecreasing in c, so D_q − D_r ≥ 0
   ("positive" means nonnegative). The inequality r(q) ≤ q needs q ≥ U/(m+1), which follows from a ≥ U/(m+1).
   **Correct.** [0] checks this exactly.
3. "The product difference splits as in (1.41), giving the four coordinate roles." This is telescoping with
   0 ≤ B ≤ A. **Correct.** [6] checks (1.40) ≤ (1.41) exactly on random rationals for d = 2..8, every owner. It also
   checks that Σ_owners (1.41) = [xy] Π_v (P_v + xA_v + yB_v + xyC_v) under the role map of §2.
4. "Monotonicity in cap and nonnegative total, together with r_- ≤ r(q) ≤ r_+ and t − q ≥ max(0, jh − b), gives
   the upper endpoints." The steps are:
   - P: D_q(t) ≤ D_{b^+}(jh) ≤ d̄_j(b^+).
   - A: D_r(t − q) ≤ D_{r_+^+}(t − q) ≤ D_{r_+^+}(s^-_j h) ≤ d̄_{s^-_j}(r_+^+). This uses s^-_j h ≤ max(0, jh − b),
     which holds because ⌈b/h⌉h ≥ b.
   - B, upper part: D_q(t) ≤ d̄_j(b^+). B, lower part: D_r(t) ≥ D_{r_-^-}(t) ≥ D_{r_-^-}((j+1)h) ≥ d̲_{j+1}(r_-^-),
     because t < (j+1)h and D is nonincreasing in t.
   - C, upper part: D_q(t − q) ≤ d̄_{s^-_j}(b^+).

   **Correct.** [1] checks the index facts exhaustively. [4] checks the resulting bounds against rigorous ρ.
5. "For jh ≥ b, also t − q ≤ t^+_j − a, giving the lower endpoint in the same-coordinate difference."
   t − q < t^+_j − a ≤ s^+_j h, so D_r(t − q) ≥ D_{r_-^-}(s^+_j h) ≥ d̲_{s^+_j}(r_-^-) = β_j. **Correct.**
   *Difference of reading:* the inequality t − q ≤ t^+_j − a holds for every j, not only for jh ≥ b ([1] (ii),
   exhaustive). Taking β_j = 0 for jh < b is a weaker, still valid, lower bound. The restriction is a choice and
   costs nothing in validity. The authors' code makes the same choice.
6. "A cell containing the largest fragment is empty if t^+_j ≤ a, and a same-coordinate cell if t^+_j ≤ a + r_+,
   since q + r(q) increases." The reasons:
   - t ≥ q > a.
   - For the same-coordinate case, t ≥ q + p > q + r(q) > a + r(a) = a + r_+. The map q + r(q) has slope
     1 − 1/m > 0.

   **Correct.** The zero sets were matched exhaustively in the Lemma 1.7 check. [4] confirms that no sampled
   positive density falls in an indicator-zero cell.
7. "No negative residual total is evaluated." The residual indices s^±_j are clipped at 0, and D_c(t) := 0 for
   t < 0 is never needed. **Correct.**
8. "A largest fragment requires q < t^+_j ... integrating dq/q ... each applied once to the sole factor carrying
   its largest fragment." This is Lemma 1.7 verbatim. λ(v) here is the same function as Lf(v)/L in (1.45), with
   (q−, q+) = (a, b). **Correct**; see `notes/oai186-lemma17-check.md` (36 checks), which includes the one-owner
   property of every monomial of (1.43)/(1.44).
9. "Use a positive lower bound for Λ in the denominator, clip at one, and bound the second fraction by the first if
   helpful. Lemma 2.1 supplies the enclosures." Outward rounding only. Λ > 0 was checked in the Lemma 1.7 note.
   **Correct.**

## 4. Computations (script sections)

| § | Claim | Result |
|---|-------|--------|
| 0 | Support data. Hypotheses U/(m+1) ≤ a < b ≤ z_G < U on all 30 bins. The grid caps b^+, r_+^+ (up) and r_-^- (down) bracket correctly, with r_-^- ≥ 64h (M from 20 689 to 49 152). r_- ≤ r(q) ≤ r_+ and r(q) ≤ q. Unstated fact: r_+ ≤ a on every bin. Every argument t/c stays below 4.75 | 7 PASS |
| 1 | Exhaustive over 30 × 98264 pairs, in integers. (i) s^-_j h ≤ max(0, jh − b). (ii) s^+_j h ≥ t^+_j − a for every j. (iii) All indices lie in 0..n. (iv) ⌈b/h⌉ and ⌊a/h⌋ as used. β_j ≠ 0 on 1 834 579 pairs | 4 PASS |
| 2 | Independent rigorous ρ on [0, 6]: a Taylor series per unit segment from (k − ξ)ρ_k' = ρ_{k−1}, 110 terms, with a proved tail bound \|c_i\| ≤ G 2^{−i} (§6). Cross-checked against 1 − log u, the Li2 closed form on [2, 3], and acb.integral of the delay equation on [3, 5]. ρ(3), ρ(4), ρ(5) = 0.0486083882911, 0.00491092564776, 0.000354724700456. Also checked: monotonicity and the antiderivative Φ | 5 PASS |
| 3 | (2.1) as printed, in exact dyadic integers at 2^-160 with outward rounding, for the 89 distinct grid caps of (2.9). The acceptance tests (ordered, in [0, 1], both sequences nonincreasing) pass on **all** j ≤ n. Rigorous d̲_j ≤ ρ(j/M) ≤ d̄_j at 1755 sampled (cap, j) with j up to n; the smallest d̄ − ρ is 2.8·10^-15 | 2 PASS |
| 4 | e = 0 arrays (ŵ = 1) on the 30 actual bins, 36 325 sampled cells: a stride of 97, all cells within ±3 of a, b, a + r_+, 2b, r_±, b + r_-, the last three cells, and 150 random cells. (a) A rigorous upper bound for the supremum over q ∈ (a, b] and t ∈ C_j of each role density (D_b(jh), D_{r_+}(max(0, jh−b)), and so on, with the *exact* caps) is ≤ the array. (b) True densities at 326 925 exact (q, t) points, including q = b, q = a + 10^-9 (b−a) and t at both cell ends, are ≤ the array, certainly. (c) The indicators are consistent. (d) Negative controls: A with cap r_-^- instead of r_+^+, and C without the shift s^-_j, each violate (a) | 10 PASS |
| 5 | End to end, d = 2, on 155 actual (bin, cell-pair) instances. These include partial-owner cells, first same-coordinate cells, cells near b and far tails. A rigorous upper Riemann bound of ∫_a^b dq/q of (1.40) over C_{j1} × C_{j2}, both owners, ≤ Λ h² [xy] of the ring with the (2.9) arrays and λ fractions. Cell integrals use Φ(u) = Σ_{i<⌊u⌋}(u−i)ρ(u−i) + (u − ⌊u⌋), and q-pieces are bounded by monotonicity. The largest ratio is 0.949. Five instances are exactly 0 on both sides by the zero-set argument of step 6 | 1 PASS |
| 6 | (1.40) ≤ (1.41), the ring role map (exact), λ = Lf/L, and the Palm formula (by reading) | 4 PASS |
| 7 | Authors' script (comparison only). TASKS gives the same 30 bins with (U, m). In `LargestFragmentPalmFactory.kernels` the caps, shifts, β rule and zero tests match (2.9) (source text). **Running** their kernels (profile power 0) on O2 P2 and O5/2 P6 gives the same zero pattern as our (2.9) arrays, with max \|difference\| = 3.1·10^-44 over 4 × 98264 entries | 3 PASS |

## 5. Readings taken

1. **R1, role letters.** The four arrays are, in order, the ring's P (ordinary, D_q(t)), x-A (owner whose
   residual has all fragments ≤ r(q), D_r(t − q)), y-B (D_q(t) − D_r(t)) and xy-C (D_q(t−q) − D_r(t−q)). The (2.9)
   array A is therefore the proof's B on the owner coordinate. The same letter means two different things on
   p. 10 / p. 14. This reading is forced by (1.41)/(1.42) and the caps used. The authors' docstring says the same:
   "A + u·B_owner + v·(A−B) + u·v·(A_owner−B_owner)".
2. **R2, d̄_j(c), d̲_j(c)** are the grid-point endpoint sequences of Lemma 2.2 for the cap c, enclosing
   D_c(jh) = ρ(j/M). They are not the cell averages d_c(j) := A_j(c)/h defined a few lines later on p. 14. The
   arrays are therefore sup-densities over the cell, which dominate the cell averages. The authors' code
   (`outward_dickman_grid(...).upper[j]`) confirms this. The other reading would be no less valid for P but is not
   what is computed.
3. **R3, c^± notation.** b^+ and r_+^+ are upward grid caps, and r_-^- is a downward grid cap (p. 12, "c^- below,
   c^+ above"; the bars are visible only in the rendered page).
4. **R4, "physical cell"** means the cell of the owner coordinate's total including q, as in the Lemma 1.7 note
   (R1 there).
5. The β restriction to jh ≥ b is read as an optional weakening (§3 step 5). It is not an error.

No alternative reading of the statement makes the lemma false. R1 is purely notational.

## 6. What is NOT covered

- **Profile power e = 2.** Only ŵ = 1 (e = 0) was computed. For e = 2, ŵ_j = ↑(g_j²/Z) is a positive factor
  common to the true and bounded densities, and only its outward rounding matters. That rounding was not
  re-evaluated.
- **Sampling.** The comparison with rigorous ρ (§4 [4]) covers 36 325 of the 2 947 920 (bin, cell) pairs. The
  index and cap facts that the proof rests on are exhaustive (§4 [1]), and monotonicity is a theorem, so this is a
  consistency check of the composed bound, not the proof itself.
- **Lemma 2.2.** Its proof was not re-proved. The recurrence was implemented as printed and its acceptance tests
  pass on all j ≤ n for these 89 caps. It was spot-checked against rigorous ρ at 1755 points. The smallest slack,
  2.8·10^-15, is small but certain.
- **End to end only for d = 2.** The d = 40 (and 39 + erased) statement rests on the per-coordinate bounds, the
  exact algebra of [6], and Lemma 1.7. Nothing 40-dimensional was integrated.
- **The Palm/Mecke formula (1.40)** was checked by reading only.
- **Downstream contractions.** The contractions (2.16)-(2.21), the erased-coordinate placements in (2.20), the
  conditioning of the inner rank-two components on (q−, q+) (P(q−, q+) in (2.19)), and the production arb/FLINT
  evaluation were not checked.
- **The ρ tail bound** is proved in the script's comment. In outline: if |e_i| ≤ E 2^{−i} for i ≥ I and
  |c_I| ≤ g 2^{−I}, then 2(E + iG)/(k(i+1)) ≤ G for k ≥ 2 and G = max(E, g). This gives |c_i| ≤ G 2^{−i}. Analyticity
  of ρ_k on |ξ| < 2 is by induction. The proof was checked by me, not by a second person.

**Restoration threshold (Prop. 4.6 of the main 186 paper; `prop:oai186-budget`): not addressed.** Lemma 2.4 says
nothing about it. The companion states only the following:
- the certified margin is > 1/50000 (abstract; Cor. 2.6, (2.35), p. 21);
- "This is the numerical input to the restoration proposition in [8, Prop. 4.6]" (p. 21);
- Prop. 1.3 (p. 8) applies [8, Prop. 4.6] and [8, (4.33)].

Which threshold (> 0 or > 1/50000) Prop. 4.6 requires is stated, if at all, in the main paper [8]. The main paper
is not in this repository.

## 7. Commands

```
pdftotext -layout code/third_party/openai186/short_gaps_numerics.pdf <scratch>/sgn.txt      # not committed
pdftoppm -f 14 -l 14 -r 300 -png code/third_party/openai186/short_gaps_numerics.pdf <scratch>/z14   # bars of (2.9)
/usr/bin/python3 code/oai186_lemma24_check.py > code/oai186_lemma24_check.out               # 36 checks, 0 failures
bash -c 'time /usr/bin/python3 code/oai186_lemma24_check.py > /dev/null'                    # ~32 s wall; RSS 776 MB
```
