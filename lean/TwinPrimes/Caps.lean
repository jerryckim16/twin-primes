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

end TwinPrimes
