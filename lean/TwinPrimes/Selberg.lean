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

NOT formalised here: the identity for general `D`, or the minimisation of `Q` under `λ_1 = 1`.
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

end TwinPrimes
