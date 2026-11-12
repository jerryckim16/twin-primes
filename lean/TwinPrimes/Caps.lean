/-!
# Counting large coordinates (Stadlmann's support, integer units)

If every entry of a list of natural numbers exceeds `g`, then `length * g` is at most the sum
(strictly less when the list is non-empty). With coordinates measured in units of 1/1000 in the
Polymath scaling (`g = 112` for `4 δ = 0.112`, total `≤ 1042` for `L = 1.042`) this shows that at most
nine coordinates of a point of Stadlmann's support can exceed `g`, and (with caps `≤ 680`) that a
point whose large set has at least seven elements violates every cap (`7 * 112 = 784 > 680`).
-/

namespace TwinPrimes

theorem length_mul_le_sum (g : Nat) : ∀ l : List Nat, (∀ x ∈ l, g < x) → l.length * g ≤ l.sum
  | [], _ => by simp
  | x :: xs, h => by
    have hx : g < x := h x (by simp)
    have ih := length_mul_le_sum g xs (fun y hy => h y (by simp [hy]))
    simp only [List.length_cons, List.sum_cons, Nat.succ_mul]
    omega

/-- At most nine coordinates of a point with total `≤ 1042` exceed `112`. -/
theorem stadlmann_large_count (l : List Nat) (h : ∀ x ∈ l, 112 < x) (hs : l.sum ≤ 1042) :
    l.length ≤ 9 := by
  have := length_mul_le_sum 112 l h
  omega

/-- Seven or more coordinates above `112` always carry more than the largest cap `680`. -/
theorem stadlmann_seven_large (l : List Nat) (h : ∀ x ∈ l, 112 < x) (hl : 7 ≤ l.length) :
    680 < l.sum := by
  have := length_mul_le_sum 112 l h
  have : 7 * 112 ≤ l.length * 112 := Nat.mul_le_mul_right 112 hl
  omega

/-- Stadlmann's caps in units of 1/1000 (Polymath scaling): `C₁ = C₂ = 600`, `Cₘ = 680` for `m ≥ 3`. -/
def stadCap (m : Nat) : Nat := if m ≤ 2 then 600 else 680

/-- Every coordinate of a point of Stadlmann's support is at most `600` (that is, `u_i ≤ 0.6`):
if `x` lies in the large set `x :: l` (all entries above `112`) whose sum respects the cap, then
`x ≤ 600`. -/
theorem stadlmann_coord_le (x : Nat) (l : List Nat) (h : ∀ y ∈ l, 112 < y)
    (hcap : x + l.sum ≤ stadCap (l.length + 1)) : x ≤ 600 := by
  have hl := length_mul_le_sum 112 l h
  unfold stadCap at hcap
  split at hcap
  · omega
  · omega

/-- In every correction piece of Session 6 the large set already carries at least `600`, so at most
three further coordinates can exceed `112` below the total `1042` (inclusion-exclusion stops at
`j = 3`). -/
theorem stadlmann_extra_le_three (l : List Nat) (h : ∀ y ∈ l, 112 < y) (s : Nat) (hs : 600 ≤ s)
    (htot : s + l.sum ≤ 1042) : l.length ≤ 3 := by
  have := length_mul_le_sum 112 l h
  omega

/-! ### Charton et al.'s parameters (Table 3 of their draft), in units of 1/1250 of the Polymath scaling:
`g = 4 δ = 82`, `L = 1325`, caps `Cₘ = 4 B_{1,m}` = 777, 794, 875, 917, 953, 983, 1016, 1042, 1063, 1081, then 1081. -/

/-- Charton et al.'s caps in units of 1/1250. -/
def chartonCap (m : Nat) : Nat :=
  [777, 794, 875, 917, 953, 983, 1016, 1042, 1063, 1081].getD (m - 1) 1081

/-- Stadlmann's admissibility condition `δ < B_m ≤ B_{m+1} ≤ B_m + δ` for these caps (checked for
`1 ≤ m ≤ 40`; for `m ≥ 11` the caps are constant). -/
theorem charton_caps_valid :
    ∀ m ∈ List.range' 1 40, 82 < chartonCap m ∧ chartonCap m ≤ chartonCap (m + 1) ∧
      chartonCap (m + 1) ≤ chartonCap m + 82 := by
  decide

/-- At most sixteen coordinates of a point with total `≤ 1325` exceed `82`. -/
theorem charton_large_count (l : List Nat) (h : ∀ x ∈ l, 82 < x) (hs : l.sum ≤ 1325) :
    l.length ≤ 16 := by
  have := length_mul_le_sum 82 l h
  omega

/-- In the correction pieces the large set carries at least `777`, so at most six further
coordinates exceed `82` below `1325` (inclusion-exclusion stops at `j = 6`). -/
theorem charton_extra_le_six (l : List Nat) (h : ∀ y ∈ l, 82 < y) (s : Nat) (hs : 777 ≤ s)
    (htot : s + l.sum ≤ 1325) : l.length ≤ 6 := by
  have := length_mul_le_sum 82 l h
  omega

end TwinPrimes
