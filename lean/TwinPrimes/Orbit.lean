/-!
# The orbit-sign lemma behind Ramaré-type weights

Let `f : ℕ → ℤ`, let `A` be a set of "K-products" (given by a Boolean predicate `isA`) and let
`s = ±1` be a sign with the multiplicativity hypothesis

  `f (a * h) = s * f h`  whenever `a ∈ A` and `gcd(a, h) = 1`.

* `orbit_sign`: for `a, b ∈ A` both coprime to `h`, `f (a h) = f (b h)`: `f` is constant on the
  "orbit" `{a h : a ∈ A, gcd(a,h) = 1}`.
* `orbit_two_step`: if `N = a h = b h'` with `a, b ∈ A`, `gcd(a,h) = gcd(b,h') = 1`, then
  `f h = f h'` (since `s * s = 1`).
* `orbit_example_hmul`, `orbit_example_check`: a concrete non-trivial instance with `s = -1`,
  `A = {3, 5, 7}` and `f n = (-1)^#{p ∈ {3,5,7} : p ∣ n}`; the hypothesis is proved for all
  `a, h`, and also checked by `decide` on `h < 50`.

NOT formalised here: any analytic statement about Ramaré weights; this is only the finite
algebraic sign bookkeeping.
-/
namespace TwinPrimes

/-- Orbit sign: `f` takes the same value on `a h` and `b h` for `a, b ∈ A` coprime to `h`. -/
theorem orbit_sign (f : Nat → Int) (isA : Nat → Bool) (s : Int)
    (hmul : ∀ a h, isA a = true → Nat.gcd a h = 1 → f (a * h) = s * f h)
    {a b h : Nat} (ha : isA a = true) (hb : isA b = true)
    (hah : Nat.gcd a h = 1) (hbh : Nat.gcd b h = 1) :
    f (a * h) = f (b * h) := by
  rw [hmul a h ha hah, hmul b h hb hbh]

/-- Two-step orbit: `N = a h = b h'` with `a, b ∈ A` coprime to `h, h'` forces `f h = f h'`. -/
theorem orbit_two_step (f : Nat → Int) (isA : Nat → Bool) (s : Int) (hs : s = 1 ∨ s = -1)
    (hmul : ∀ a h, isA a = true → Nat.gcd a h = 1 → f (a * h) = s * f h)
    {N a b h h' : Nat} (hN : N = a * h) (hN' : N = b * h')
    (ha : isA a = true) (hb : isA b = true)
    (hah : Nat.gcd a h = 1) (hbh : Nat.gcd b h' = 1) :
    f h = f h' := by
  have e1 := hmul a h ha hah
  have e2 := hmul b h' hb hbh
  rw [← hN] at e1
  rw [← hN'] at e2
  have e : s * f h = s * f h' := e1.symm.trans e2
  rcases hs with rfl | rfl <;> omega

/-! ## A concrete instance with `s = -1` -/

/-- `A = {3, 5, 7}`. -/
def orbA (a : Nat) : Bool := a == 3 || a == 5 || a == 7

/-- Number of `p ∈ {3, 5, 7}` dividing `n`. -/
def orbV (n : Nat) : Nat :=
  (if n % 3 = 0 then 1 else 0) + (if n % 5 = 0 then 1 else 0) + (if n % 7 = 0 then 1 else 0)

/-- `f n = (-1)^{orbV n}`. -/
def orbF (n : Nat) : Int := if orbV n % 2 = 0 then 1 else -1

theorem orbit_mod_ne_zero {p h : Nat} (hp : 1 < p) (hg : Nat.gcd p h = 1) : h % p ≠ 0 := by
  intro h0
  have : Nat.gcd p h = p := Nat.gcd_eq_left (Nat.dvd_of_mod_eq_zero h0)
  omega

/-- The hypothesis of `orbit_sign` holds for `orbF`, `orbA`, `s = -1`, for all `a, h`. -/
theorem orbit_example_hmul :
    ∀ a h, orbA a = true → Nat.gcd a h = 1 → orbF (a * h) = -1 * orbF h := by
  intro a h ha hg
  have hm := orbit_mod_ne_zero (by simp [orbA] at ha; omega) hg
  simp only [orbA, Bool.or_eq_true, beq_iff_eq] at ha
  rcases ha with (rfl | rfl) | rfl <;>
    (simp only [orbF, orbV]; repeat' split) <;> omega

/-- Decidable sanity check of the same hypothesis on `h < 50`, `a ∈ {3, 5, 7}`. -/
theorem orbit_example_check :
    [3, 5, 7].all (fun a => orbA a && (List.range 50).all (fun h =>
      Nat.gcd a h != 1 || orbF (a * h) == -1 * orbF h)) = true := by decide

/-- The instance is non-trivial: `f` is not identically zero and `A` contains elements whose
orbits are genuinely compared (e.g. `f 3 = f 5 = -1`, `f 1 = 1`). -/
theorem orbit_example_nontrivial : orbF 1 = 1 ∧ orbF 3 = -1 ∧ orbF 5 = -1 ∧ orbF 15 = 1 := by
  decide

end TwinPrimes
