import TwinPrimes.Basic

/-!
# Parity-pattern weights (parity-barrier paper, Prop. `prop:bipartite`)

Finite combinatorial core of the "bipartite criterion".  A parity-pattern weight on a 3-tuple is a
function `w : Int → Int → Int → Int` of the Liouville signs `(a, b, c) ∈ {±1}^3` at the three positions.
It is *fair* if every singleton Fourier coefficient vanishes, i.e. `Σ w(ε) ε_i = 0`, and it *kills* a pair
of positions if it vanishes whenever both signs there are `-1` (primes have Liouville sign `-1`).

* `triangle_no_fair_weight`: a non-negative fair weight that kills all three pairs is identically zero
  (the target "two primes among three" = `DHL[3,2]` is not blocked by any such weight).
* `pm8b_path_weight_*`: the Polymath8b weight `(1 - a b)(1 - b c)` for `{0, 2, 6}` is non-negative, fair,
  and kills the pairs `{0,2}` and `{2,6}` (the path is bipartite), but not `{0,6}`.
-/

namespace TwinPrimes

/-- The eight sign patterns, with the value of a weight at each. -/
def signs : List Int := [1, -1]

/-- Sum of `f` over all sign patterns. -/
def patSum (f : Int → Int → Int → Int) : Int :=
  f 1 1 1 + f 1 1 (-1) + f 1 (-1) 1 + f 1 (-1) (-1) +
  f (-1) 1 1 + f (-1) 1 (-1) + f (-1) (-1) 1 + f (-1) (-1) (-1)

theorem triangle_no_fair_weight (w : Int → Int → Int → Int)
    (hnn : ∀ a b c, 0 ≤ w a b c)
    -- kills every pair of positions (patterns with two or more `-1`)
    (k1 : w (-1) (-1) 1 = 0) (k2 : w (-1) 1 (-1) = 0) (k3 : w 1 (-1) (-1) = 0)
    (k4 : w (-1) (-1) (-1) = 0)
    -- fair: singleton Fourier coefficients vanish
    (f1 : patSum (fun a b c => w a b c * a) = 0)
    (f2 : patSum (fun a b c => w a b c * b) = 0)
    (f3 : patSum (fun a b c => w a b c * c) = 0) :
    patSum w = 0 := by
  simp only [patSum] at *
  have := hnn 1 1 1; have := hnn (-1) 1 1; have := hnn 1 (-1) 1; have := hnn 1 1 (-1)
  omega

/-- The Polymath8b weight for the tuple `{0, 2, 6}` (positions a, b, c). -/
def pm8bWeight (a b c : Int) : Int := (1 - a * b) * (1 - b * c)

theorem pm8b_path_weight_nonneg :
    ∀ a ∈ signs, ∀ b ∈ signs, ∀ c ∈ signs, 0 ≤ pm8bWeight a b c := by decide

theorem pm8b_path_weight_fair :
    patSum (fun a b c => pm8bWeight a b c * a) = 0 ∧
    patSum (fun a b c => pm8bWeight a b c * b) = 0 ∧
    patSum (fun a b c => pm8bWeight a b c * c) = 0 ∧
    patSum pm8bWeight = 8 := by decide

theorem pm8b_path_weight_kills :
    (∀ c ∈ signs, pm8bWeight (-1) (-1) c = 0) ∧ (∀ a ∈ signs, pm8bWeight a (-1) (-1) = 0) ∧
    pm8bWeight (-1) 1 (-1) ≠ 0 := by decide

/-- Narrowest admissible 5- and 7-tuples used for `H(5) = 12`, `H(7) = 20` (admissibility only;
minimality is a computation, `code/parity/bipartite_obstruction.py`). -/
theorem narrow5_admissible : Admissible [0, 2, 6, 8, 12] := admissible_of_check (by decide)
theorem narrow7_admissible : Admissible [0, 2, 6, 8, 12, 18, 20] := admissible_of_check (by decide)

end TwinPrimes
