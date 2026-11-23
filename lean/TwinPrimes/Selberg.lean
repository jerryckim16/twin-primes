/-!
# Selberg's diagonalisation of the sieve quadratic form (finite, exact checks)

Gauss's identity `∑_{r ∣ n} φ(r) = n` gives
`1/[d,e] = gcd(d,e)/(d e) = (1/(d e)) ∑_{r ∣ gcd(d,e)} φ(r)`, and hence

  `Q(λ) = ∑_{d,e ≤ D} λ_d λ_e / [d,e] = ∑_{r ≤ D} φ(r) y_r²`,  `y_r = ∑_{d ≤ D, r ∣ d} λ_d / d`.

To stay in `Int`, multiply by `L²` with `L = lcm(1, …, D)`:

  `∑_{d,e ≤ D} λ_d λ_e · (L² gcd(d,e) / (d e)) = ∑_{r ≤ D} φ(r) (∑_{d ≤ D, r ∣ d} λ_d (L / d))²`,

where every division is exact (`L² gcd(d,e)/(d e) = L²/[d,e]`, `L/d ∈ ℕ`).

* `totient`, `divisorTotientSum`, `gauss_totient_upto`: Gauss's identity for `1 ≤ n ≤ 60`,
  checked by `decide`;
* `selbergLHS`, `selbergRHS`, `selberg_diag_D6`: the scaled identity for `D = 6` and **all**
  `λ : ℕ → ℤ` (a polynomial identity in `λ 1, …, λ 6`);
* `selberg_diag_example`: a concrete evaluation with `λ = μ` on `d ≤ 6`.

* `selberg_sos_D6`, `selberg_opt_D6`, `selberg_opt_D6_eq`, `selberg_opt_D6_eq_iff`: Selberg's
  optimum for `D = 6`: `Q(λ) ≥ λ₁² / G` with `G = ∑_{r ≤ 6 sqfree} 1/φ(r) = 13/4`, attained exactly
  at multiples of the Selberg weights `(13, -12, -12, 0, -5, 12) / 13`.

The identity for general `D` is `selberg_diag` in `TwinPrimes/Gauss.lean` (with Gauss's identity
`gauss_totient` for all `n ≥ 1`). The lower bound `Q(λ) ≥ λ₁²/G(D)` for general `D` is `selberg_lower` in
`TwinPrimes/SelbergOpt.lean` (Session 44); attainment for every `D` (explicit weights, `selberg_lower_attained`) is in
`TwinPrimes/SelbergEq.lean` (Session 46); uniqueness of the extremal weights is formalised only for `D = 6`.
-/

namespace TwinPrimes

/-- Euler's totient: `#{1 ≤ k ≤ n : gcd(k, n) = 1}` (so `totient 0 = 0`). -/
def totient (n : Nat) : Nat :=
  ((List.range n).filter (fun k => Nat.gcd (k + 1) n == 1)).length

/-- `∑_{r ∣ n, r ≥ 1} φ(r)`. -/
def divisorTotientSum (n : Nat) : Nat :=
  (((List.range (n + 1)).filter (fun r => r != 0 && n % r == 0)).map totient).sum

set_option maxRecDepth 100000 in
/-- Gauss's identity `∑_{r ∣ n} φ(r) = n`, checked for `1 ≤ n ≤ 60`. -/
theorem gauss_totient_upto : ∀ n, n ≤ 60 → 1 ≤ n → divisorTotientSum n = n := by
  decide

/-- `lcm(1, …, D)`. -/
def lcmUpto (D : Nat) : Nat := ((List.range D).map (· + 1)).foldl Nat.lcm 1

/-- `L² · ∑_{d,e ≤ D} λ_d λ_e / [d,e]`, written as
`∑_{d,e ≤ D} λ_d λ_e · (L² gcd(d,e) / (d e))` with `L = lcm(1..D)`. -/
def selbergLHS (D : Nat) (lam : Nat → Int) : Int :=
  let L := lcmUpto D
  (((List.range D).map (· + 1)).map fun d =>
    (((List.range D).map (· + 1)).map fun e =>
      lam d * lam e * ((L * L * Nat.gcd d e / (d * e) : Nat) : Int)).sum).sum

/-- `L² · ∑_{r ≤ D} φ(r) y_r²`, written as `∑_{r ≤ D} φ(r) (∑_{d ≤ D, r ∣ d} λ_d (L / d))²`. -/
def selbergRHS (D : Nat) (lam : Nat → Int) : Int :=
  let L := lcmUpto D
  (((List.range D).map (· + 1)).map fun r =>
    (totient r : Int) *
      ((((List.range D).map (· + 1)).filter (fun d => d % r == 0)).map fun d =>
        lam d * ((L / d : Nat) : Int)).sum ^ 2).sum

/-- **Selberg's diagonalisation, `D = 6`.** For every `λ : ℕ → ℤ`,
`∑_{d,e ≤ 6} λ_d λ_e (L² gcd(d,e)/(de)) = ∑_{r ≤ 6} φ(r) (∑_{d ≤ 6, r ∣ d} λ_d (L/d))²`
with `L = lcm(1..6) = 60`; dividing by `L²` this is
`∑ λ_d λ_e / [d,e] = ∑_{r ≤ 6} φ(r) y_r²`, `y_r = ∑_{r ∣ d ≤ 6} λ_d / d`. -/
theorem selberg_diag_D6 (lam : Nat → Int) : selbergLHS 6 lam = selbergRHS 6 lam := by
  have hL : lcmUpto 6 = 60 := by decide
  have h1 : totient 1 = 1 := by decide
  have h2 : totient 2 = 1 := by decide
  have h3 : totient 3 = 2 := by decide
  have h4 : totient 4 = 2 := by decide
  have h5 : totient 5 = 4 := by decide
  have h6 : totient 6 = 2 := by decide
  simp [selbergLHS, selbergRHS, hL, h1, h2, h3, h4, h5, h6, List.range_succ, List.filter]
  grind

/-- Möbius weights `λ_d = μ(d)` for `d ≤ 6` (and `0` beyond). -/
def muUpto6 (d : Nat) : Int :=
  if d = 1 then 1 else if d = 2 then -1 else if d = 3 then -1 else if d = 5 then -1
  else if d = 6 then 1 else 0

/-- Concrete instance with `λ = μ` on `d ≤ 6`, `L = 60`: both sides equal `1440`, i.e.
`Q(μ) = 1440 / 60² = 2/5`, with `L·y_r = 8, -20, -10, 0, -12, 10` for `r = 1, …, 6`
and `1440 = 1·8² + 1·20² + 2·10² + 2·0² + 4·12² + 2·10²`. -/
theorem selberg_diag_example :
    lcmUpto 6 = 60 ∧ selbergLHS 6 muUpto6 = 1440 ∧ selbergRHS 6 muUpto6 = 1440 ∧
    (((List.range 6).map (· + 1)).map fun r =>
      ((((List.range 6).map (· + 1)).filter (fun d => d % r == 0)).map fun d =>
        muUpto6 d * ((lcmUpto 6 / d : Nat) : Int)).sum) = [8, -20, -10, 0, -12, 10] := by
  decide

/-- **Sum-of-squares certificate for the `D = 6` Selberg optimum.** With `Y_r = L y_r`
(`L = 60`) and `Z_r = φ(r) μ(r) Y_r` for squarefree `r ∈ {1,2,3,5,6}`
(`Z = Y₁, -Y₂, -2Y₃, -4Y₅, 2Y₆`), Lagrange's identity for Cauchy–Schwarz gives
`2 (13 L² Q - 4 L² λ₁²) = 52 Y₄² + ∑_{r<s} (8 / (φ(r) φ(s))) (Z_r - Z_s)²`,
using `λ₁ = ∑_r μ(r) y_r` and `G = ∑_{r ≤ 6, r squarefree} 1/φ(r) = 13/4`. -/
theorem selberg_sos_D6 (lam : Nat → Int) :
    2 * (13 * selbergLHS 6 lam - 14400 * lam 1 ^ 2) =
      let Y1 := 60 * lam 1 + 30 * lam 2 + 20 * lam 3 + 15 * lam 4 + 12 * lam 5 + 10 * lam 6
      let Y2 := 30 * lam 2 + 15 * lam 4 + 10 * lam 6
      let Y3 := 20 * lam 3 + 10 * lam 6
      let Y4 := 15 * lam 4
      let Y5 := 12 * lam 5
      let Y6 := 10 * lam 6
      52 * Y4 ^ 2 +
      8 * (Y1 + Y2) ^ 2 + 4 * (Y1 + 2 * Y3) ^ 2 + 2 * (Y1 + 4 * Y5) ^ 2 + 4 * (Y1 - 2 * Y6) ^ 2 +
      4 * (2 * Y3 - Y2) ^ 2 + 2 * (4 * Y5 - Y2) ^ 2 + 4 * (Y2 + 2 * Y6) ^ 2 +
      (4 * Y5 - 2 * Y3) ^ 2 + 2 * (2 * Y3 + 2 * Y6) ^ 2 + (2 * Y6 + 4 * Y5) ^ 2 := by
  rw [selberg_diag_D6]
  have hL : lcmUpto 6 = 60 := by decide
  have h1 : totient 1 = 1 := by decide
  have h2 : totient 2 = 1 := by decide
  have h3 : totient 3 = 2 := by decide
  have h4 : totient 4 = 2 := by decide
  have h5 : totient 5 = 4 := by decide
  have h6 : totient 6 = 2 := by decide
  simp [selbergRHS, hL, h1, h2, h3, h4, h5, h6, List.range_succ, List.filter]
  grind

/-- **Selberg's optimum, `D = 6`, lower bound.** For every `λ : ℕ → ℤ` (no support condition
needed: `λ₄` only adds `52 Y₄² ≥ 0`), `13 · L² Q(λ) ≥ 4 · L² λ₁²`, i.e. `Q(λ) ≥ λ₁² / G`
with `G = 13/4`. Here `selbergLHS 6 λ = 60² Q(λ)` and `14400 = 4 · 60²`. -/
theorem selberg_opt_D6 (lam : Nat → Int) : 14400 * lam 1 ^ 2 ≤ 13 * selbergLHS 6 lam := by
  have h := selberg_sos_D6 lam
  simp only at h
  generalize hA : 60 * lam 1 + 30 * lam 2 + 20 * lam 3 + 15 * lam 4 + 12 * lam 5 + 10 * lam 6 = A at h
  generalize hB : 30 * lam 2 + 15 * lam 4 + 10 * lam 6 = B at h
  generalize hC : 20 * lam 3 + 10 * lam 6 = C at h
  generalize hE : 12 * lam 5 = E at h
  generalize hF : 10 * lam 6 = F at h
  have q0 := Int.sq_nonneg (15 * lam 4)
  have q1 := Int.sq_nonneg (A + B)
  have q2 := Int.sq_nonneg (A + 2 * C)
  have q3 := Int.sq_nonneg (A + 4 * E)
  have q4 := Int.sq_nonneg (A - 2 * F)
  have q5 := Int.sq_nonneg (2 * C - B)
  have q6 := Int.sq_nonneg (4 * E - B)
  have q7 := Int.sq_nonneg (B + 2 * F)
  have q8 := Int.sq_nonneg (4 * E - 2 * C)
  have q9 := Int.sq_nonneg (2 * C + 2 * F)
  have q10 := Int.sq_nonneg (2 * F + 4 * E)
  omega

private theorem sq_eq_zero' {a : Int} (h : a ^ 2 = 0) : a = 0 := by
  have h' : a * a = 0 := by grind
  exact (Int.mul_eq_zero.mp h').elim id id

/-- Selberg's optimal weights for `D = 6`, scaled by `13` to be integers:
`λ_d = 13 · μ(d) (d/φ(d)) (∑_{r ≤ 6/d, (r,d)=1, r sqfree} 1/φ(r)) / G` with `G = 13/4`,
i.e. `(λ₁, …, λ₆) = (13, -12, -12, 0, -5, 12)`. -/
def selbergOpt6 (d : Nat) : Int :=
  if d = 1 then 13 else if d = 2 then -12 else if d = 3 then -12 else if d = 5 then -5
  else if d = 6 then 12 else 0

/-- **The optimum is attained** by `selbergOpt6`: `L² Q = 187200`, i.e. `Q = 52 = 13² / G`. -/
theorem selberg_opt_D6_eq :
    selbergLHS 6 selbergOpt6 = 187200 ∧
    13 * selbergLHS 6 selbergOpt6 = 14400 * selbergOpt6 1 ^ 2 := by decide

/-- **Equality case, `D = 6`.** `Q(λ) = λ₁² / G` holds exactly when `λ_d` (for `1 ≤ d ≤ 6`) is
`λ₁ / 13` times `selbergOpt6 d`, i.e. `λ` is proportional to the Selberg weights (in
particular `λ₄ = 0`). -/
theorem selberg_opt_D6_eq_iff (lam : Nat → Int) :
    13 * selbergLHS 6 lam = 14400 * lam 1 ^ 2 ↔
      ∀ d, 1 ≤ d → d ≤ 6 → 13 * lam d = lam 1 * selbergOpt6 d := by
  have h := selberg_sos_D6 lam
  simp only at h
  constructor
  · intro heq
    generalize hA : 60 * lam 1 + 30 * lam 2 + 20 * lam 3 + 15 * lam 4 + 12 * lam 5 + 10 * lam 6 = A at h
    generalize hB : 30 * lam 2 + 15 * lam 4 + 10 * lam 6 = B at h
    generalize hC : 20 * lam 3 + 10 * lam 6 = C at h
    generalize hE : 12 * lam 5 = E at h
    generalize hF : 10 * lam 6 = F at h
    have q0 := Int.sq_nonneg (15 * lam 4)
    have q1 := Int.sq_nonneg (A + B)
    have q2 := Int.sq_nonneg (A + 2 * C)
    have q3 := Int.sq_nonneg (A + 4 * E)
    have q4 := Int.sq_nonneg (A - 2 * F)
    have q5 := Int.sq_nonneg (2 * C - B)
    have q6 := Int.sq_nonneg (4 * E - B)
    have q7 := Int.sq_nonneg (B + 2 * F)
    have q8 := Int.sq_nonneg (4 * E - 2 * C)
    have q9 := Int.sq_nonneg (2 * C + 2 * F)
    have q10 := Int.sq_nonneg (2 * F + 4 * E)
    have z0 := sq_eq_zero' (a := 15 * lam 4) (by omega)
    have z1 := sq_eq_zero' (a := A + B) (by omega)
    have z2 := sq_eq_zero' (a := A + 2 * C) (by omega)
    have z3 := sq_eq_zero' (a := A + 4 * E) (by omega)
    have z4 := sq_eq_zero' (a := A - 2 * F) (by omega)
    intro d hd1 hd6
    have : d = 1 ∨ d = 2 ∨ d = 3 ∨ d = 4 ∨ d = 5 ∨ d = 6 := by omega
    rcases this with rfl | rfl | rfl | rfl | rfl | rfl <;> simp [selbergOpt6] <;> omega
  · intro hw
    have e2 := hw 2 (by decide) (by decide)
    have e3 := hw 3 (by decide) (by decide)
    have e4 := hw 4 (by decide) (by decide)
    have e5 := hw 5 (by decide) (by decide)
    have e6 := hw 6 (by decide) (by decide)
    simp [selbergOpt6] at e2 e3 e4 e5 e6
    generalize hA : 60 * lam 1 + 30 * lam 2 + 20 * lam 3 + 15 * lam 4 + 12 * lam 5 + 10 * lam 6 = A at h
    generalize hB : 30 * lam 2 + 15 * lam 4 + 10 * lam 6 = B at h
    generalize hC : 20 * lam 3 + 10 * lam 6 = C at h
    generalize hE : 12 * lam 5 = E at h
    generalize hF : 10 * lam 6 = F at h
    have q0 := Int.sq_nonneg (15 * lam 4)
    have q1 := Int.sq_nonneg (A + B)
    have q2 := Int.sq_nonneg (A + 2 * C)
    have q3 := Int.sq_nonneg (A + 4 * E)
    have q4 := Int.sq_nonneg (A - 2 * F)
    have q5 := Int.sq_nonneg (2 * C - B)
    have q6 := Int.sq_nonneg (4 * E - B)
    have q7 := Int.sq_nonneg (B + 2 * F)
    have q8 := Int.sq_nonneg (4 * E - 2 * C)
    have q9 := Int.sq_nonneg (2 * C + 2 * F)
    have q10 := Int.sq_nonneg (2 * F + 4 * E)
    have b0 : 15 * lam 4 = 0 := by omega
    have b1 : A + B = 0 := by omega
    have b2 : A + 2 * C = 0 := by omega
    have b3 : A + 4 * E = 0 := by omega
    have b4 : A - 2 * F = 0 := by omega
    have b5 : 2 * C - B = 0 := by omega
    have b6 : 4 * E - B = 0 := by omega
    have b7 : B + 2 * F = 0 := by omega
    have b8 : 4 * E - 2 * C = 0 := by omega
    have b9 : 2 * C + 2 * F = 0 := by omega
    have b10 : 2 * F + 4 * E = 0 := by omega
    rw [b0, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10] at h
    simp at h
    omega
end TwinPrimes
