/-!
# Finite counting identities behind the Selberg/Maynard sum `S₁`

The main term of a Selberg-type sieve sum

  `S₁ = ∑_{n < N} (∑_{d ∈ D, d ∣ n} y_d)²`

comes from expanding the square and counting multiples of `lcm(d, e)` below `N`.  This file
checks the purely finite, combinatorial part of that computation in core Lean (no reals,
no Mathlib, list-based sums):

* `countRes_bounds`, `countDvd_bounds`, `countDvd_eq`: the number of `n < N` in a residue
  class mod `d` is `N / d` up to an error `< 1` (stated division-free);
* `selberg_expand`: the exact identity
  `S₁ = ∑_{d,e ∈ D} y_d y_e · #{n < N : lcm(d,e) ∣ n}`;
* `selberg_error`: for any common multiple `M` of the `lcm(d,e)`,
  `|M · S₁ − N · ∑_{d,e} y_d y_e (M / lcm(d,e))| ≤ M · ∑_{d,e} |y_d y_e|`,
  the division-free form of `|S₁ − N ∑ y_d y_e / lcm(d,e)| ≤ ∑ |y_d y_e|`.

NOT formalised here: the asymptotic evaluation of the main term
`N ∑ y_d y_e / lcm(d,e)` for the Maynard weights.
-/

namespace TwinPrimes

/-! ## Counting residue classes -/

/-- `#{n < N : n % d = a}`. -/
def countRes (d a N : Nat) : Nat := (List.range N).countP (fun n => n % d == a)

/-- `#{n < N : d ∣ n}` (as `n % d = 0`). -/
def countDvd (d N : Nat) : Nat := (List.range N).countP (fun n => n % d == 0)

theorem countDvd_eq_countRes (d N : Nat) : countDvd d N = countRes d 0 N := rfl

theorem countRes_succ (d a N : Nat) :
    countRes d a (N + 1) = countRes d a N + if N % d = a then 1 else 0 := by
  simp [countRes, List.range_succ, List.countP_append]

/-- Residue classes: for `a < d`, `c = #{n < N : n % d = a}` satisfies
`N ≤ a + d·c < N + d`, i.e. `|c − (N − a)/d| < 1` when `a ≤ N` (and `c = 0` when `N ≤ a`). -/
theorem countRes_bounds {d a : Nat} (hd : 0 < d) (ha : a < d) :
    ∀ N : Nat, N ≤ a + d * countRes d a N ∧ a + d * countRes d a N < N + d
  | 0 => by simp [countRes]; omega
  | N + 1 => by
    obtain ⟨h1, h2⟩ := countRes_bounds hd ha N
    rw [countRes_succ]
    have key := Nat.mod_add_div N d
    by_cases hN : N % d = a
    · simp only [hN, ite_true]
      -- in this case `a + d * c = N` exactly
      have hc : countRes d a N = N / d := by
        have e1 : d * (N / d) ≤ d * countRes d a N := by omega
        have e2 : d * countRes d a N < d * (N / d + 1) := by rw [Nat.mul_add]; omega
        have := Nat.le_of_mul_le_mul_left e1 hd
        have := Nat.lt_of_mul_lt_mul_left e2
        omega
      rw [Nat.mul_add, hc]; omega
    · simp only [hN, ite_false, Nat.add_zero]
      have hne : a + d * countRes d a N ≠ N := by
        intro h
        apply hN
        rw [← h, Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt ha]
      omega

/-- Multiples: `N ≤ d · #{n < N : d ∣ n} < N + d`, i.e. the count is `⌈N / d⌉`. -/
theorem countDvd_bounds {d : Nat} (hd : 0 < d) (N : Nat) :
    N ≤ d * countDvd d N ∧ d * countDvd d N < N + d := by
  have := countRes_bounds hd hd N
  rw [countDvd_eq_countRes]
  omega

/-- Exact form: `#{n < N : d ∣ n} = ⌈N / d⌉ = (N + d - 1) / d`. -/
theorem countDvd_eq {d : Nat} (hd : 0 < d) (N : Nat) :
    countDvd d N = (N + d - 1) / d := by
  obtain ⟨h1, h2⟩ := countDvd_bounds hd N
  symm
  apply Nat.div_eq_of_lt_le
  · rw [Nat.mul_comm]; omega
  · rw [Nat.add_mul, Nat.one_mul, Nat.mul_comm]; omega

/-! ## List-sum helpers over `Int` -/

theorem isum_zero {α} : ∀ l : List α, (l.map fun _ => (0 : Int)).sum = 0
  | [] => rfl
  | _ :: l => by simp only [List.map_cons, List.sum_cons, isum_zero l]; rfl

theorem isum_add {α} (f g : α → Int) : ∀ l : List α,
    (l.map fun x => f x + g x).sum = (l.map f).sum + (l.map g).sum
  | [] => by simp
  | x :: l => by simp only [List.map_cons, List.sum_cons, isum_add f g l]; omega

theorem isum_sub {α} (f g : α → Int) : ∀ l : List α,
    (l.map fun x => f x - g x).sum = (l.map f).sum - (l.map g).sum
  | [] => by simp
  | x :: l => by simp only [List.map_cons, List.sum_cons, isum_sub f g l]; omega

theorem isum_mul_left {α} (c : Int) (f : α → Int) : ∀ l : List α,
    (l.map fun x => c * f x).sum = c * (l.map f).sum
  | [] => by simp
  | x :: l => by simp only [List.map_cons, List.sum_cons, isum_mul_left c f l, Int.mul_add]

theorem isum_mul_right {α} (c : Int) (f : α → Int) (l : List α) :
    (l.map fun x => f x * c).sum = (l.map f).sum * c := by
  rw [Int.mul_comm, ← isum_mul_left]; simp only [Int.mul_comm]

theorem isum_congr {α} {f g : α → Int} {l : List α} (h : ∀ x ∈ l, f x = g x) :
    (l.map f).sum = (l.map g).sum := by rw [List.map_congr_left h]

/-- Interchanging two finite list sums. -/
theorem isum_comm {α β} (f : α → β → Int) (l₁ : List α) : ∀ l₂ : List β,
    (l₁.map fun a => (l₂.map fun b => f a b).sum).sum
      = (l₂.map fun b => (l₁.map fun a => f a b).sum).sum
  | [] => by simp only [List.map_nil, List.sum_nil]; exact isum_zero l₁
  | b :: l₂ => by
    simp only [List.map_cons, List.sum_cons]
    rw [isum_add (fun a => f a b) (fun a => (l₂.map fun b => f a b).sum), isum_comm f l₁ l₂]

/-- The square of a sum is the double sum. -/
theorem isum_sq {α} (f : α → Int) (l : List α) :
    (l.map f).sum * (l.map f).sum = (l.map fun a => (l.map fun b => f a * f b).sum).sum := by
  rw [← isum_mul_right]; apply isum_congr; intro a _; rw [isum_mul_left]

/-- Summing a constant over the elements satisfying `p` gives `c · countP p`. -/
theorem isum_ite_count {α} (p : α → Bool) (c : Int) : ∀ l : List α,
    (l.map fun x => if p x then c else 0).sum = c * (l.countP p : Int)
  | [] => by simp
  | x :: l => by
    simp only [List.map_cons, List.sum_cons, isum_ite_count p c l, List.countP_cons]
    cases p x <;> simp [Int.mul_add] <;> omega

/-- `|∑ f| ≤ ∑ |f|` (with `natAbs`). -/
theorem natAbs_isum_le {α} (f : α → Int) : ∀ l : List α,
    (l.map f).sum.natAbs ≤ (l.map fun x => (f x).natAbs).sum
  | [] => by simp
  | x :: l => by
    simp only [List.map_cons, List.sum_cons]
    exact Nat.le_trans (Int.natAbs_add_le _ _) (Nat.add_le_add_left (natAbs_isum_le f l) _)

theorem nsum_le {α} {f g : α → Nat} : ∀ {l : List α}, (∀ x ∈ l, f x ≤ g x) →
    (l.map f).sum ≤ (l.map g).sum
  | [], _ => by simp
  | x :: l, h => by
    simp only [List.map_cons, List.sum_cons]
    exact Nat.add_le_add (h x List.mem_cons_self)
      (nsum_le fun z hz => h z (List.mem_cons_of_mem _ hz))

theorem nsum_mul_left {α} (c : Nat) (f : α → Nat) : ∀ l : List α,
    (l.map fun x => c * f x).sum = c * (l.map f).sum
  | [] => by simp
  | x :: l => by simp only [List.map_cons, List.sum_cons, nsum_mul_left c f l, Nat.mul_add]

/-! ## The Selberg expansion of `S₁` -/

/-- `d ∣ n ∧ e ∣ n ↔ lcm(d, e) ∣ n`. -/
theorem lcm_dvd_iff {d e n : Nat} : Nat.lcm d e ∣ n ↔ d ∣ n ∧ e ∣ n :=
  ⟨fun h => ⟨Nat.dvd_trans (Nat.dvd_lcm_left d e) h, Nat.dvd_trans (Nat.dvd_lcm_right d e) h⟩,
   fun h => Nat.lcm_dvd h.1 h.2⟩

/-- The sieve weight `λ(n) = ∑_{d ∈ D, d ∣ n} y_d`. -/
def sieveSum (D : List Nat) (y : Nat → Int) (n : Nat) : Int :=
  (D.map fun d => if d ∣ n then y d else 0).sum

/-- Selberg expansion: `∑_{n<N} λ(n)² = ∑_{d,e ∈ D} y_d y_e · #{n < N : lcm(d,e) ∣ n}`.
(No positivity of `D` is needed: `0 ∣ n ↔ n = 0 ↔ n % 0 = 0`.) -/
theorem selberg_expand (D : List Nat) (y : Nat → Int) (N : Nat) :
    ((List.range N).map fun n => sieveSum D y n * sieveSum D y n).sum
      = (D.map fun d => (D.map fun e =>
          y d * y e * (countDvd (Nat.lcm d e) N : Int)).sum).sum := by
  have h1 : ∀ n, sieveSum D y n * sieveSum D y n
      = (D.map fun d => (D.map fun e =>
          if n % Nat.lcm d e == 0 then y d * y e else 0).sum).sum := by
    intro n
    unfold sieveSum
    rw [isum_sq]
    apply isum_congr; intro d _; apply isum_congr; intro e _
    have : (n % Nat.lcm d e == 0) = (decide (d ∣ n) && decide (e ∣ n)) := by
      have := @lcm_dvd_iff d e n
      rw [Nat.dvd_iff_mod_eq_zero] at this
      by_cases hd : d ∣ n <;> by_cases he : e ∣ n <;> simp_all
    rw [this]
    by_cases hd : d ∣ n <;> by_cases he : e ∣ n <;> simp [hd, he]
  rw [isum_congr (fun n _ => h1 n), isum_comm]
  apply isum_congr; intro d _
  rw [isum_comm]
  apply isum_congr; intro e _
  exact isum_ite_count (fun n => n % Nat.lcm d e == 0) _ _

/-- Error term of `S₁`, division-free: for positive `D` and any common multiple `M` of all
`lcm(d,e)`,
`|M · S₁ − N · ∑_{d,e} y_d y_e (M / lcm(d,e))| ≤ M · ∑_{d,e} |y_d y_e|`,
i.e. `|S₁ − N ∑ y_d y_e / lcm(d,e)| ≤ ∑ |y_d y_e|` after dividing by `M`.
(Each pair contributes `y_d y_e · (M/L)(L · count − N)` with `0 ≤ L · count − N < L`.) -/
theorem selberg_error (D : List Nat) (y : Nat → Int) (N M : Nat)
    (hD : ∀ d ∈ D, 0 < d) (hM : ∀ d ∈ D, ∀ e ∈ D, Nat.lcm d e ∣ M) :
    ((M : Int) * ((List.range N).map fun n => sieveSum D y n * sieveSum D y n).sum
      - (N : Int) * (D.map fun d => (D.map fun e =>
          y d * y e * ((M / Nat.lcm d e : Nat) : Int)).sum).sum).natAbs
      ≤ M * (D.map fun d => (D.map fun e => (y d * y e).natAbs).sum).sum := by
  rw [selberg_expand, ← isum_mul_left, ← isum_mul_left, ← isum_sub, ← nsum_mul_left]
  refine Nat.le_trans (natAbs_isum_le _ _) (nsum_le ?_)
  intro d hd
  rw [← isum_mul_left, ← isum_mul_left, ← isum_sub, ← nsum_mul_left]
  refine Nat.le_trans (natAbs_isum_le _ _) (nsum_le ?_)
  intro e he
  have hL : 0 < Nat.lcm d e := Nat.lcm_pos (hD d hd) (hD e he)
  obtain ⟨b1, b2⟩ := countDvd_bounds hL N
  generalize countDvd (Nat.lcm d e) N = c at b1 b2
  have hk := Nat.mul_div_cancel' (hM d hd e he)
  generalize M / Nat.lcm d e = k at hk
  generalize Nat.lcm d e = L at hL b1 b2 hk
  subst hk
  have : (↑(L * k) : Int) * (y d * y e * (c : Int)) - (N : Int) * (y d * y e * (k : Int))
      = y d * y e * ((k : Int) * ((L * c : Nat) - (N : Int))) := by
    simp only [Int.natCast_mul, Int.mul_sub]
    simp only [Int.mul_assoc, Int.mul_comm, Int.mul_left_comm]
  rw [this, Int.natAbs_mul, Nat.mul_comm (L * k)]
  apply Nat.mul_le_mul_left
  rw [Int.natAbs_mul, Int.natAbs_natCast, Nat.mul_comm L k]
  apply Nat.mul_le_mul_left
  omega

end TwinPrimes
