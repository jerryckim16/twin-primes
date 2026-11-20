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

* `crt_residue`, `crt_count_bounds`, `crt_count_div`: for `gcd(d, W) = 1` and `v₀ < W`,
  `#{n < N : n ≡ v₀ (W), d ∣ n + h}` is a single residue class mod `W d`, hence equals
  `N / (W d)` up to an error `< 1`;
* `crt_selberg_expand`, `crt_selberg_error`: the analogues of the above for
  `∑_{n < N, n ≡ v₀ (W)} λ(n + h)²` when every `d ∈ D` is coprime to `W`.

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

/-! ## CRT step: counting in a residue class `n ≡ v₀ (mod W)` -/

/-- Bezout over `Int`. -/
theorem crt_bezout (a b : Nat) : ∃ x y : Int, (a : Int) * x + (b : Int) * y = (Nat.gcd a b : Int) := by
  refine Nat.gcd.induction a b (fun n => ⟨0, 1, by simp⟩) ?_
  intro m n _ ih
  obtain ⟨x, y, h⟩ := ih
  rw [Nat.gcd_rec m n]
  refine ⟨y - ((n / m : Nat) : Int) * x, x, ?_⟩
  have e : ((n % m : Nat) : Int) + (m : Int) * ((n / m : Nat) : Int) = n := by
    exact_mod_cast Nat.mod_add_div n m
  rw [← h, ← e]
  generalize ((n % m : Nat) : Int) = r
  generalize ((n / m : Nat) : Int) = q
  grind

/-- A multiplicative inverse of `W` modulo `d` (for coprime `W`, `d`). -/
theorem crt_inverse {W d : Nat} (hd : 0 < d) (hc : Nat.gcd W d = 1) :
    ∃ u : Nat, (W * u) % d = 1 % d := by
  obtain ⟨x, y, h⟩ := crt_bezout W d
  rw [hc] at h
  refine ⟨(x % d).toNat, ?_⟩
  have hnn : 0 ≤ x % (d : Int) := Int.emod_nonneg _ (by omega)
  apply Int.ofNat_inj.mp
  push_cast
  rw [Int.toNat_of_nonneg hnn]
  have h2 : (W : Int) * (x % d) = 1 + (d : Int) * (-(y + W * (x / d))) := by
    have := Int.emod_add_mul_ediv x d
    grind
  rw [h2, Int.add_mul_emod_self_left]

/-- CRT uniqueness: agreeing modulo coprime `W` and `d` means agreeing modulo `W * d`. -/
theorem crt_mod_eq {W d a b : Nat} (hc : Nat.gcd W d = 1)
    (h1 : a % W = b % W) (h2 : a % d = b % d) : a % (W * d) = b % (W * d) := by
  have key : ∀ a b : Nat, a % W = b % W → a % d = b % d → b ≤ a →
      a % (W * d) = b % (W * d) := by
    intro a b h1 h2 hab
    have dW : W ∣ a - b := Nat.dvd_of_mod_eq_zero (Nat.sub_mod_eq_zero_of_mod_eq h1)
    have dd : d ∣ a - b := Nat.dvd_of_mod_eq_zero (Nat.sub_mod_eq_zero_of_mod_eq h2)
    obtain ⟨k, hk⟩ := Nat.Coprime.mul_dvd_of_dvd_of_dvd hc dW dd
    have : a = b + W * d * k := by omega
    rw [this, Nat.add_mul_mod_self_left]
  rcases Nat.le_total b a with hab | hab
  · exact key a b h1 h2 hab
  · exact (key b a h1.symm h2.symm hab).symm

theorem crt_add_mod_cancel {a b h k : Nat} (H : (a + h) % k = (b + h) % k) : a % k = b % k := by
  obtain ⟨k₁, k₂, e⟩ := Nat.mod_eq_mod_iff.mp H
  exact Nat.mod_eq_mod_iff.mpr ⟨k₁, k₂, by omega⟩

/-- CRT existence: for coprime `d`, `W` the conditions `n ≡ v₀ (mod W)`, `n ≡ -h (mod d)`
cut out a single residue class `r` modulo `W * d`. -/
theorem crt_residue {W d v0 : Nat} (h : Nat) (hv : v0 < W) (hd : 0 < d)
    (hc : Nat.gcd d W = 1) :
    ∃ r, r < W * d ∧ ∀ n, (n % W = v0 ∧ (n + h) % d = 0) ↔ n % (W * d) = r := by
  have hW : 0 < W := by omega
  obtain ⟨u, hu⟩ := crt_inverse hd (by rw [Nat.gcd_comm]; exact hc)
  obtain ⟨s, hs_def⟩ : ∃ s, s = (v0 + h) % d := ⟨_, rfl⟩
  have hs : s < d := hs_def ▸ Nat.mod_lt _ hd
  obtain ⟨t, ht⟩ : ∃ t, t + s = d := ⟨d - s, by omega⟩
  obtain ⟨m, hm⟩ : ∃ m, m = v0 + W * (u * t) := ⟨_, rfl⟩
  have hmW : m % W = v0 := by
    rw [hm, Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt hv]
  have hmd : (m + h) % d = 0 := by
    have e1 := Nat.mod_add_div (v0 + h) d
    rw [← hs_def] at e1
    have e2 := Nat.mod_add_div (W * u) d
    rw [hu] at e2
    apply Nat.mod_eq_zero_of_dvd
    by_cases hd1 : d = 1
    · subst hd1; exact Nat.one_dvd _
    have h1 : 1 % d = 1 := Nat.mod_eq_of_lt (by omega)
    rw [h1] at e2
    refine ⟨(v0 + h) / d + (W * u) / d * t + 1, ?_⟩
    generalize (v0 + h) / d = q at e1
    generalize (W * u) / d = k at e2
    rw [hm, ← Nat.mul_assoc, ← e2]
    clear hm hs_def hu hc
    grind
  refine ⟨m % (W * d), Nat.mod_lt _ (Nat.mul_pos hW hd), fun n => ⟨?_, ?_⟩⟩
  · rintro ⟨h1, h2⟩
    apply crt_mod_eq (by rw [Nat.gcd_comm]; exact hc)
    · rw [h1, hmW]
    · exact crt_add_mod_cancel (h := h) (by rw [h2, hmd])
  · intro hn
    have h1 : n % W = m % W := by
      rw [← Nat.mod_mul_right_mod n W d, hn, Nat.mod_mul_right_mod]
    have h2 : n % d = m % d := by
      rw [← Nat.mod_mul_left_mod n W d, hn, Nat.mod_mul_left_mod]
    refine ⟨by rw [h1, hmW], ?_⟩
    rw [Nat.add_mod, h2, ← Nat.add_mod, hmd]

/-- The CRT count is a plain residue-class count modulo `W * d`. -/
theorem crt_count_eq_countRes {W d v0 : Nat} (h : Nat) (hv : v0 < W) (hd : 0 < d)
    (hc : Nat.gcd d W = 1) :
    ∃ r, r < W * d ∧ ∀ N, (List.range N).countP (fun n => n % W == v0 && (n + h) % d == 0)
      = countRes (W * d) r N := by
  obtain ⟨r, hr, hiff⟩ := crt_residue h hv hd hc
  refine ⟨r, hr, fun N => ?_⟩
  unfold countRes
  congr 1
  funext n
  rw [Bool.eq_iff_iff]
  simp only [Bool.and_eq_true, beq_iff_eq]
  exact hiff n

/-- CRT counting, division-free: `c = #{n < N : n ≡ v₀ (W), d ∣ n + h}` satisfies
`N < W d (c + 1)` and `W d c < N + W d`, i.e. `|W d · c − N| < W d`. -/
theorem crt_count_bounds {W d v0 : Nat} (h : Nat) (hv : v0 < W) (hd : 0 < d)
    (hc : Nat.gcd d W = 1) (N : Nat) :
    N < W * d * ((List.range N).countP (fun n => n % W == v0 && (n + h) % d == 0) + 1) ∧
    W * d * (List.range N).countP (fun n => n % W == v0 && (n + h) % d == 0) < N + W * d := by
  obtain ⟨r, hr, heq⟩ := crt_count_eq_countRes h hv hd hc
  rw [heq N]
  have hWd : 0 < W * d := Nat.mul_pos (by omega) hd
  obtain ⟨b1, b2⟩ := countRes_bounds hWd hr N
  rw [Nat.mul_add, Nat.mul_one]
  omega

/-- CRT counting with floors: `⌊N / (W d)⌋ ≤ c ≤ ⌊N / (W d)⌋ + 1`. -/
theorem crt_count_div {W d v0 : Nat} (h : Nat) (hv : v0 < W) (hd : 0 < d)
    (hc : Nat.gcd d W = 1) (N : Nat) :
    N / (W * d) ≤ (List.range N).countP (fun n => n % W == v0 && (n + h) % d == 0) ∧
    (List.range N).countP (fun n => n % W == v0 && (n + h) % d == 0) ≤ N / (W * d) + 1 := by
  obtain ⟨b1, b2⟩ := crt_count_bounds h hv hd hc N
  generalize (List.range N).countP (fun n => n % W == v0 && (n + h) % d == 0) = c at b1 b2 ⊢
  have hWd : 0 < W * d := Nat.mul_pos (by omega) hd
  constructor
  · have := (Nat.div_lt_iff_lt_mul hWd).mpr (by rw [Nat.mul_comm]; exact b1)
    omega
  · have e := Nat.mod_add_div N (W * d)
    have hm := Nat.mod_lt N hWd
    have : W * d * c < W * d * (N / (W * d) + 2) := by rw [Nat.mul_add]; omega
    have := Nat.lt_of_mul_lt_mul_left this
    omega


/-! ## Selberg expansion restricted to a residue class `n ≡ v₀ (mod W)` -/

/-- Pointwise square expansion of the sieve weight (as in `selberg_expand`). -/
theorem crt_sieveSum_sq (D : List Nat) (y : Nat → Int) (m : Nat) :
    sieveSum D y m * sieveSum D y m
      = (D.map fun d => (D.map fun e =>
          if m % Nat.lcm d e == 0 then y d * y e else 0).sum).sum := by
  unfold sieveSum
  rw [isum_sq]
  apply isum_congr; intro d _; apply isum_congr; intro e _
  have : (m % Nat.lcm d e == 0) = (decide (d ∣ m) && decide (e ∣ m)) := by
    have := @lcm_dvd_iff d e m
    rw [Nat.dvd_iff_mod_eq_zero] at this
    by_cases hd : d ∣ m <;> by_cases he : e ∣ m <;> simp_all
  rw [this]
  by_cases hd : d ∣ m <;> by_cases he : e ∣ m <;> simp [hd, he]

/-- Selberg expansion on `n ≡ v₀ (mod W)` for the shifted weight `λ(n + h)`:
`∑_{n<N, n%W=v₀} λ(n+h)² = ∑_{d,e ∈ D} y_d y_e · #{n < N : n%W = v₀, lcm(d,e) ∣ n + h}`. -/
theorem crt_selberg_expand (D : List Nat) (y : Nat → Int) (W v0 h N : Nat) :
    ((List.range N).map fun n =>
        if n % W = v0 then sieveSum D y (n + h) * sieveSum D y (n + h) else 0).sum
      = (D.map fun d => (D.map fun e =>
          y d * y e * (((List.range N).countP fun n =>
            n % W == v0 && (n + h) % Nat.lcm d e == 0 : Nat) : Int)).sum).sum := by
  have h1 : ∀ n, (if n % W = v0 then sieveSum D y (n + h) * sieveSum D y (n + h) else 0)
      = (D.map fun d => (D.map fun e =>
          if (n % W == v0 && (n + h) % Nat.lcm d e == 0) then y d * y e else 0).sum).sum := by
    intro n
    by_cases hn : n % W = v0
    · simp only [hn, ite_true, beq_self_eq_true, Bool.true_and]
      exact crt_sieveSum_sq D y (n + h)
    · simp only [hn, ite_false]
      have hb : (n % W == v0) = false := by simp [hn]
      simp only [hb, Bool.false_and]
      symm
      simp only [Bool.false_eq_true, ite_false]
      rw [isum_congr (fun d _ => isum_zero D)]
      exact isum_zero D
  rw [isum_congr (fun n _ => h1 n), isum_comm]
  apply isum_congr; intro d _
  rw [isum_comm]
  apply isum_congr; intro e _
  exact isum_ite_count (fun n => n % W == v0 && (n + h) % Nat.lcm d e == 0) _ _

/-- Error term of the restricted `S₁`, division-free: if every `d ∈ D` is positive and coprime
to `W`, `v₀ < W`, and `M` is a common multiple of all `lcm(d,e)`, then
`|W M · S₁(v₀) − N · ∑_{d,e} y_d y_e (M / lcm(d,e))| ≤ W M · ∑_{d,e} |y_d y_e|`,
i.e. `|S₁(v₀) − (N/W) ∑ y_d y_e / lcm(d,e)| ≤ ∑ |y_d y_e|` after dividing by `W M`. -/
theorem crt_selberg_error (D : List Nat) (y : Nat → Int) (W v0 h N M : Nat) (hv : v0 < W)
    (hD : ∀ d ∈ D, 0 < d) (hDW : ∀ d ∈ D, Nat.gcd d W = 1)
    (hM : ∀ d ∈ D, ∀ e ∈ D, Nat.lcm d e ∣ M) :
    (((W * M : Nat) : Int) * ((List.range N).map fun n =>
          if n % W = v0 then sieveSum D y (n + h) * sieveSum D y (n + h) else 0).sum
      - (N : Int) * (D.map fun d => (D.map fun e =>
          y d * y e * ((M / Nat.lcm d e : Nat) : Int)).sum).sum).natAbs
      ≤ W * M * (D.map fun d => (D.map fun e => (y d * y e).natAbs).sum).sum := by
  rw [crt_selberg_expand, ← isum_mul_left, ← isum_mul_left, ← isum_sub, ← nsum_mul_left]
  refine Nat.le_trans (natAbs_isum_le _ _) (nsum_le ?_)
  intro d hd
  rw [← isum_mul_left, ← isum_mul_left, ← isum_sub, ← nsum_mul_left]
  refine Nat.le_trans (natAbs_isum_le _ _) (nsum_le ?_)
  intro e he
  have hL : 0 < Nat.lcm d e := Nat.lcm_pos (hD d hd) (hD e he)
  have hLW : Nat.gcd (Nat.lcm d e) W = 1 := by
    have hde : Nat.Coprime (d * e) W := Nat.Coprime.mul_left (hDW d hd) (hDW e he)
    exact Nat.Coprime.coprime_dvd_left
      (Nat.lcm_dvd (Nat.dvd_mul_right d e) (Nat.dvd_mul_left e d)) hde
  obtain ⟨b1, b2⟩ := crt_count_bounds h hv hL hLW N
  generalize (List.range N).countP (fun n => n % W == v0 && (n + h) % Nat.lcm d e == 0) = c
    at b1 b2 ⊢
  have hk := Nat.mul_div_cancel' (hM d hd e he)
  generalize M / Nat.lcm d e = k at hk
  generalize Nat.lcm d e = L at hL b1 b2 hk
  subst hk
  have : (↑(W * (L * k)) : Int) * (y d * y e * (c : Int)) - (N : Int) * (y d * y e * (k : Int))
      = y d * y e * ((k : Int) * ((W * L * c : Nat) - (N : Int))) := by
    simp only [Int.natCast_mul, Int.mul_sub]
    simp only [Int.mul_assoc, Int.mul_comm, Int.mul_left_comm]
  rw [this, Int.natAbs_mul, Nat.mul_comm (W * (L * k))]
  apply Nat.mul_le_mul_left
  rw [Int.natAbs_mul, Int.natAbs_natCast,
    show W * (L * k) = k * (W * L) by rw [Nat.mul_comm k, Nat.mul_assoc]]
  apply Nat.mul_le_mul_left
  rw [Nat.mul_add, Nat.mul_one] at b1
  omega

/-! ## `S₂`-type sums: one extra (prime-type) condition `g n`

Bookkeeping only.  `g` is an arbitrary Boolean condition (think: `n + h'` is prime); no
property of primes is used.  In the error theorem the hypothesis on the counts carries all of
the analysis (it is where a Bombieri–Vinogradov-type input would enter). -/

/-- `#{n < N : n ≡ v₀ (W), L ∣ n + h, g n}`. -/
def s2Count (g : Nat → Bool) (W v0 h L N : Nat) : Nat :=
  (List.range N).countP fun n => n % W == v0 && (n + h) % L == 0 && g n

/-- Expansion of `S₂`: for any condition `g`,
`∑_{n<N, n%W=v₀, g n} λ(n+h)² = ∑_{d,e ∈ D} y_d y_e · #{n < N : n%W = v₀, lcm(d,e) ∣ n+h, g n}`. -/
theorem s2_expand (D : List Nat) (y : Nat → Int) (g : Nat → Bool) (W v0 h N : Nat) :
    ((List.range N).map fun n =>
        if (n % W == v0 && g n) = true then sieveSum D y (n + h) * sieveSum D y (n + h)
        else 0).sum
      = (D.map fun d => (D.map fun e =>
          y d * y e * (s2Count g W v0 h (Nat.lcm d e) N : Int)).sum).sum := by
  have h1 : ∀ n, (if (n % W == v0 && g n) = true then
        sieveSum D y (n + h) * sieveSum D y (n + h) else 0)
      = (D.map fun d => (D.map fun e =>
          if (n % W == v0 && (n + h) % Nat.lcm d e == 0 && g n) = true then y d * y e
          else 0).sum).sum := by
    intro n
    cases hb : (n % W == v0 && g n)
    · have hz : ∀ L, (n % W == v0 && (n + h) % L == 0 && g n) = false := by
        intro L
        cases h1 : (n % W == v0) <;> cases h2 : g n <;> simp_all
      simp only [hz, Bool.false_eq_true, ite_false]
      rw [isum_congr (fun d _ => isum_zero D)]
      exact (isum_zero D).symm
    · have hz : ∀ L, (n % W == v0 && (n + h) % L == 0 && g n) = ((n + h) % L == 0) := by
        intro L
        cases h1 : (n % W == v0) <;> cases h2 : g n <;> simp_all
      simp only [hz, ite_true]
      exact crt_sieveSum_sq D y (n + h)
  rw [isum_congr (fun n _ => h1 n), isum_comm]
  apply isum_congr; intro d _
  rw [isum_comm]
  apply isum_congr; intro e _
  exact isum_ite_count (fun n => n % W == v0 && (n + h) % Nat.lcm d e == 0 && g n) _ _

/-- Abstract error term of `S₂`: if for all `d, e ∈ D` the count
`#{n < N : n%W = v₀, lcm(d,e) ∣ n+h, g n}` is within `E(lcm d e)` of `X(lcm d e)`, then
`|S₂ − ∑_{d,e} y_d y_e X(lcm d e)| ≤ ∑_{d,e} |y_d y_e| E(lcm d e)`.
`X` and `E` are arbitrary; the hypothesis `hX` is the whole arithmetic content. -/
theorem s2_error (D : List Nat) (y : Nat → Int) (g : Nat → Bool) (W v0 h N : Nat)
    (X : Nat → Int) (E : Nat → Nat)
    (hX : ∀ d ∈ D, ∀ e ∈ D,
      ((s2Count g W v0 h (Nat.lcm d e) N : Int) - X (Nat.lcm d e)).natAbs ≤ E (Nat.lcm d e)) :
    (((List.range N).map fun n =>
          if (n % W == v0 && g n) = true then sieveSum D y (n + h) * sieveSum D y (n + h)
          else 0).sum
      - (D.map fun d => (D.map fun e => y d * y e * X (Nat.lcm d e)).sum).sum).natAbs
      ≤ (D.map fun d => (D.map fun e =>
          (y d * y e).natAbs * E (Nat.lcm d e)).sum).sum := by
  rw [s2_expand, ← isum_sub]
  refine Nat.le_trans (natAbs_isum_le _ _) (nsum_le ?_)
  intro d hd
  rw [← isum_sub]
  refine Nat.le_trans (natAbs_isum_le _ _) (nsum_le ?_)
  intro e he
  rw [← Int.mul_sub, Int.natAbs_mul]
  exact Nat.mul_le_mul_left _ (hX d hd e he)

/-- Non-vacuity check: `D = [1, 2]`, `y = (1, -1)`, `W = 1`, `h = 0`, `N = 30`,
`g n = (n + 2 prime)` (trial division); both sides equal `10` (odd `n < 30` with `n + 2` prime). -/
theorem s2_expand_example :
    let D := [1, 2]
    let y : Nat → Int := fun d => if d = 1 then 1 else -1
    let g : Nat → Bool := fun n => decide (2 ≤ n + 2) &&
      (List.range (n + 2)).all fun k => decide (k < 2) || (n + 2) % k != 0
    ((List.range 30).map fun n =>
        if (n % 1 == 0 && g n) = true then sieveSum D y n * sieveSum D y n else 0).sum = 10 ∧
    (D.map fun d => (D.map fun e =>
        y d * y e * (s2Count g 1 0 0 (Nat.lcm d e) 30 : Int)).sum).sum = 10 := by
  decide

end TwinPrimes
