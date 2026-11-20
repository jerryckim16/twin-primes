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


/-!
## Chen's target as a consistency test (parity paper, Remark `rem:chen`)

Two positions `(n, n+2)` with Liouville signs `(a, b)`.  Chen's target "`n` prime and `n+2 ∈ P₂`"
does not restrict `b` (a `P₂` number can have either sign), so a weight that kills it vanishes on
both patterns with `a = -1`.  Its two halves are each killed by a fair weight: `1 - a b` kills
"`n+2` prime" (pattern `(-1,-1)`), `1 + a b` kills "`n+2` a product of two primes" (pattern `(-1,1)`).
-/

/-- Sum of `f` over the four sign patterns of a pair. -/
def patSum2 (f : Int → Int → Int) : Int := f 1 1 + f 1 (-1) + f (-1) 1 + f (-1) (-1)

/-- No non-negative, weakly fair weight kills Chen's target: it is identically zero. -/
theorem chen_no_weakly_fair_weight (w : Int → Int → Int)
    (hnn : ∀ a b, 0 ≤ w a b)
    (k1 : w (-1) 1 = 0) (k2 : w (-1) (-1) = 0)
    -- weakly fair at the first position: singleton coefficient `≤ 0`
    (f1 : patSum2 (fun a b => w a b * a) ≤ 0) :
    patSum2 w = 0 := by
  simp only [patSum2] at *
  have := hnn 1 1; have := hnn 1 (-1)
  omega

/-- The twin-prime half: `1 - a b` is non-negative, fair, and kills `(-1,-1)` but not `(-1,1)`. -/
theorem chen_twin_half_weight :
    (∀ a ∈ signs, ∀ b ∈ signs, 0 ≤ 1 - a * b) ∧
    patSum2 (fun a b => (1 - a * b) * a) = 0 ∧ patSum2 (fun a b => (1 - a * b) * b) = 0 ∧
    patSum2 (fun a b => 1 - a * b) = 4 ∧
    (1 - (-1) * (-1) : Int) = 0 ∧ (1 - (-1) * 1 : Int) ≠ 0 := by decide

/-- The semiprime half: `1 + a b` is non-negative, fair, and kills `(-1,1)` but not `(-1,-1)`. -/
theorem chen_semiprime_half_weight :
    (∀ a ∈ signs, ∀ b ∈ signs, 0 ≤ 1 + a * b) ∧
    patSum2 (fun a b => (1 + a * b) * a) = 0 ∧ patSum2 (fun a b => (1 + a * b) * b) = 0 ∧
    patSum2 (fun a b => 1 + a * b) = 4 ∧
    (1 + (-1) * 1 : Int) = 0 ∧ (1 + (-1) * (-1) : Int) ≠ 0 := by decide

/-!
## Almost-prime 3-tuples (route card `notes/parity-attempts/2026-11-20-almost-prime-tuples.md`)

For three positions, the sign patterns compatible with `Ω(L₁(n) L₂(n) L₃(n)) ≤ 4` are exactly those with at
least two `-1` signs (a `+1` sign means an even `Ωᵢ ≥ 2`).  So the target `DHL_Ω[3; 4]` is not blocked even by
weakly fair weights (singleton coefficients `≤ 0`, i.e. sign `-1` of density `≥ 1/2` at each position).
-/

/-- A non-negative, weakly fair weight that vanishes on every pattern with at least two `-1` signs is 0. -/
theorem omega4_no_weakly_fair_weight (w : Int → Int → Int → Int)
    (hnn : ∀ a b c, 0 ≤ w a b c)
    (k1 : w (-1) (-1) 1 = 0) (k2 : w (-1) 1 (-1) = 0) (k3 : w 1 (-1) (-1) = 0)
    (k4 : w (-1) (-1) (-1) = 0)
    (f1 : patSum (fun a b c => w a b c * a) ≤ 0)
    (f2 : patSum (fun a b c => w a b c * b) ≤ 0)
    (f3 : patSum (fun a b c => w a b c * c) ≤ 0) :
    patSum w = 0 := by
  simp only [patSum] at *
  have := hnn 1 1 1; have := hnn (-1) 1 1; have := hnn 1 (-1) 1; have := hnn 1 1 (-1)
  omega

/-- `Ω ≤ 3` (three primes) is blocked: `3 - (ab + bc + ca)` is non-negative, fair, and vanishes at `(-1,-1,-1)`. -/
theorem omega3_weight :
    (∀ a ∈ signs, ∀ b ∈ signs, ∀ c ∈ signs, 0 ≤ 3 - (a * b + b * c + c * a)) ∧
    patSum (fun a b c => (3 - (a * b + b * c + c * a)) * a) = 0 ∧
    patSum (fun a b c => (3 - (a * b + b * c + c * a)) * b) = 0 ∧
    patSum (fun a b c => (3 - (a * b + b * c + c * a)) * c) = 0 ∧
    patSum (fun a b c => 3 - (a * b + b * c + c * a)) = 24 ∧
    (3 - ((-1) * (-1) + (-1) * (-1) + (-1) * (-1)) : Int) = 0 := by decide

end TwinPrimes
