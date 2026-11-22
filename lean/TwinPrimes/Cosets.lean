/-!
# Counting `j`-tuples of nonzero residues with a prescribed sum

For `m ≥ 1`, `cnt m j s` is the number of `j`-tuples `(x_1, …, x_j)` with every
`x_i ∈ {1, …, m-1}` (the nonzero residues mod `m`) and `x_1 + ⋯ + x_j ≡ s (mod m)`. It is defined
by recursion on `j` (conditioning on the last coordinate `x_{j+1} = a`):

  `cnt m 0 s = [s ≡ 0]`,  `cnt m (j+1) s = ∑_{a=1}^{m-1} cnt m j ((s + m - a) % m)`.

* `cnt_eq_AB`: `cnt m j s` depends only on whether `s ≡ 0 (mod m)`; it equals `A m j` if so and
  `B m j` otherwise, where `A (j+1) = (m-1) B j`, `B (j+1) = A j + (m-2) B j`;
* `coset_count_zero`: `m · cnt m j 0 = (m-1)^j + (-1)^j (m-1)` (in `ℤ`), for all `m ≥ 2`, `j`;
* `coset_count_nonzero`: `m · cnt m j s = (m-1)^j - (-1)^j` for `s ≢ 0 (mod m)`, all `m ≥ 2`, `j`;
* `coset_prob_two`: `cnt m 2 0 = m - 1`; `coset_count_three`: `m · cnt m 3 0 = (m-1)^3 - (m-1)`;
* small values checked by `decide`.
-/

namespace TwinPrimes

namespace Cosets

/-- `cnt m j s` = number of `(x_1, …, x_j) ∈ {1, …, m-1}^j` with `x_1 + ⋯ + x_j ≡ s (mod m)`.
Recursion on `j`: the last coordinate `a = x_{j+1} ∈ {1, …, m-1}` leaves the residue
`(s + m - a) % m` for the first `j` coordinates (meant for `s < m`, or any `s` after `% m`). -/
def cnt (m : Nat) : Nat → Nat → Nat
  | 0, s => if s % m = 0 then 1 else 0
  | j + 1, s => ((List.range (m - 1)).map (fun a => cnt m j ((s + m - (a + 1)) % m))).sum

mutual
/-- Count when the target residue is `0`: `A 0 = 1`, `A (j+1) = (m-1) B j`. -/
def A (m : Nat) : Nat → Nat
  | 0 => 1
  | j + 1 => (m - 1) * B m j
/-- Count when the target residue is nonzero: `B 0 = 0`, `B (j+1) = A j + (m-2) B j`. -/
def B (m : Nat) : Nat → Nat
  | 0 => 0
  | j + 1 => A m j + (m - 2) * B m j
end

theorem cnt_three_two_zero : cnt 3 2 0 = 2 := by decide
theorem cnt_three_three_zero : cnt 3 3 0 = 2 := by decide
theorem cnt_four_three_zero : cnt 4 3 0 = 6 := by decide
theorem cnt_four_three_one : cnt 4 3 1 = 7 := by decide
theorem cnt_five_four_zero : cnt 5 4 0 = 52 := by decide

/-- A sum over `a < n` whose summand is `X` exactly when `a + 1 = r` and `Y` otherwise. -/
theorem sum_ite (n r X Y : Nat) (g : Nat → Nat) (h : ∀ a, a < n → g a = if a + 1 = r then X else Y) :
    ((List.range n).map g).sum = if 1 ≤ r ∧ r ≤ n then X + (n - 1) * Y else n * Y := by
  induction n with
  | zero => rw [ite_eq_right (by omega)]; simp
  | succ n ih =>
    rw [List.range_succ, List.map_append, List.sum_append, ih (fun a ha => h a (by omega))]
    simp only [List.map_cons, List.map_nil, List.sum_cons, List.sum_nil, Nat.add_zero]
    rw [h n (by omega)]
    by_cases h1 : n + 1 = r
    · subst h1
      simp only [ite_true]
      rw [ite_eq_right (by omega), ite_eq_left (by omega)]
      simp [Nat.mul_comm, Nat.add_comm]
    · rw [ite_eq_right h1]
      by_cases h2 : 1 ≤ r ∧ r ≤ n
      · rw [ite_eq_left h2, ite_eq_left (by omega)]
        rw [Nat.add_assoc, ← Nat.succ_mul]
        cases n with
        | zero => omega
        | succ n => simp
      · rw [ite_eq_right h2, ite_eq_right (by omega), Nat.succ_mul]

/-- For `a < m - 1`, `(s + m - (a+1)) % m = 0` iff `a + 1 = s % m`. -/
theorem mod_zero_iff (m s a : Nat) (hm : 2 ≤ m) (ha : a < m - 1) :
    (s + m - (a + 1)) % m = 0 ↔ a + 1 = s % m := by
  have hr : s % m < m := Nat.mod_lt _ (by omega)
  have hs : s = s % m + m * (s / m) := (Nat.mod_add_div s m).symm
  have he : s + m - (a + 1) = (s % m + m - (a + 1)) + m * (s / m) := by omega
  rw [he, Nat.add_mul_mod_self_left]
  by_cases hx : s % m + m - (a + 1) < m
  · rw [Nat.mod_eq_of_lt hx]; omega
  · rw [Nat.mod_eq_sub_mod (by omega), Nat.mod_eq_of_lt (by omega)]; omega

/-- `cnt m j s` depends only on whether `s ≡ 0 (mod m)`. -/
theorem cnt_eq_AB (m : Nat) (hm : 2 ≤ m) :
    ∀ j s, cnt m j s = if s % m = 0 then A m j else B m j
  | 0, s => by simp [cnt, A, B]
  | j + 1, s => by
    rw [cnt, sum_ite (m - 1) (s % m) (A m j) (B m j)]
    · have hr : s % m < m := Nat.mod_lt _ (by omega)
      by_cases h0 : s % m = 0
      · rw [ite_eq_right (by omega), ite_eq_left h0, A]
      · rw [ite_eq_left (by omega), ite_eq_right h0, B]
        have : m - 1 - 1 = m - 2 := by omega
        rw [this]
    · intro a ha
      rw [cnt_eq_AB m hm j, Nat.mod_mod]
      by_cases h : a + 1 = s % m
      · rw [ite_eq_left ((mod_zero_iff m s a hm ha).2 h), ite_eq_left h]
      · rw [ite_eq_right (fun h' => h ((mod_zero_iff m s a hm ha).1 h')), ite_eq_right h]

/-- Closed forms for `A` and `B` (in `ℤ`). -/
theorem AB_closed (m : Nat) (hm : 2 ≤ m) : ∀ j,
    (m : Int) * A m j = ((m : Int) - 1) ^ j + (-1) ^ j * ((m : Int) - 1) ∧
    (m : Int) * B m j = ((m : Int) - 1) ^ j - (-1) ^ j
  | 0 => by simp only [A, B, Int.pow_zero]; omega
  | j + 1 => by
    obtain ⟨hA, hB⟩ := AB_closed m hm j
    have c1 : ((m - 1 : Nat) : Int) = (m : Int) - 1 := by omega
    have c2 : ((m - 2 : Nat) : Int) = (m : Int) - 2 := by omega
    constructor
    · rw [A, Int.natCast_mul, c1]
      rw [Int.pow_succ, Int.pow_succ]
      grind
    · rw [B, Int.natCast_add, Int.natCast_mul, c2]
      rw [Int.pow_succ, Int.pow_succ]
      grind

/-- `m · #{x ∈ {1..m-1}^j : ∑ x ≡ 0} = (m-1)^j + (-1)^j (m-1)` for all `m ≥ 2`, `j`. -/
theorem coset_count_zero (m j : Nat) (hm : 2 ≤ m) :
    (m : Int) * cnt m j 0 = ((m : Int) - 1) ^ j + (-1) ^ j * ((m : Int) - 1) := by
  rw [cnt_eq_AB m hm, ite_eq_left (Nat.zero_mod m)]
  exact (AB_closed m hm j).1

/-- `m · #{x ∈ {1..m-1}^j : ∑ x ≡ s} = (m-1)^j - (-1)^j` for `s ≢ 0 (mod m)`, all `m ≥ 2`, `j`. -/
theorem coset_count_nonzero (m j s : Nat) (hm : 2 ≤ m) (hs : s % m ≠ 0) :
    (m : Int) * cnt m j s = ((m : Int) - 1) ^ j - (-1) ^ j := by
  rw [cnt_eq_AB m hm, ite_eq_right hs]
  exact (AB_closed m hm j).2

/-- `j = 2`: `cnt m 2 0 = m - 1` (so the sum of two nonzero residues is `0` with probability
`1/(m-1)`). -/
theorem coset_prob_two (m : Nat) (hm : 2 ≤ m) : cnt m 2 0 = m - 1 := by
  have h := coset_count_zero m 2 hm
  have hz : ((cnt m 2 0 : Nat) : Int) * m = ((m - 1 : Nat) : Int) * m := by
    rw [Int.mul_comm, h]
    have c1 : ((m - 1 : Nat) : Int) = (m : Int) - 1 := by omega
    rw [c1]
    grind
  have hm0 : (m : Int) ≠ 0 := by omega
  exact Int.ofNat.inj (Int.eq_of_mul_eq_mul_right hm0 hz)

/-- `j = 3`: `m · cnt m 3 0 = (m-1)^3 - (m-1)`. -/
theorem coset_count_three (m : Nat) (hm : 2 ≤ m) :
    (m : Int) * cnt m 3 0 = ((m : Int) - 1) ^ 3 - ((m : Int) - 1) := by
  rw [coset_count_zero m 3 hm]
  grind

end Cosets

end TwinPrimes
