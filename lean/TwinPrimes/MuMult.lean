import TwinPrimes.MaynardInv

/-!
# Multiplicativity of `μ` and the sign identity `MuSign c` for every squarefree `c`

From the recursive definition `mu` (via `mu_divisor_sum` only), splitting the divisors of `p n`
by divisibility by a prime `p` (`dsum_split`) gives
* `mu_prime_mul`: `μ(p n) = -μ(n)` for `p ∤ n`; `mu_prime_mul_dvd`: `μ(p n) = 0` for `p ∣ n`;
  hence `mu_one`, `mu_prime` (`μ(p) = -1`), `mu_eq_zero_of_sq_dvd` (`p² ∣ n ⇒ μ(n) = 0`);
* `mu_sign_sqf`, `muSign_of_sqfree`: `μ(a) μ(x) = μ(x/a)` for `a ∣ x ∣ c`, `c ≥ 1`, `μ(c) ≠ 0`;
* `mu_mul_coprime`: `μ(m n) = μ(m) μ(n)` for coprime `m, n`;
* `maynard_lam_of_y_sqfree_all`, `maynard_y_of_lam_sqfree_all`: Maynard's inversion, both
  directions, for squarefree-supported weights on `{1,…,R}^k`, **every `R` and `k`**.
-/

namespace TwinPrimes
namespace MuMult

open Gauss SelbergOpt MaynardInv

/-- `p` is prime: `p ≥ 2` and its only divisors are `1` and `p`. -/
def IsPrime (p : Nat) : Prop := 2 ≤ p ∧ ∀ d, d ∣ p → d = 1 ∨ d = p

/-- `n` is squarefree: no `p²` with `p` prime divides `n`. -/
def Sqf (n : Nat) : Prop := ∀ p, IsPrime p → ¬ p * p ∣ n

/-- Divisor sum `∑_{r ∣ n} f(r)` (over `1 ≤ r ≤ n`). -/
def dsum (n : Nat) (f : Nat → Int) : Int :=
  ((List.range (n + 1)).map fun r => if 0 < r ∧ r ∣ n then f r else 0).sum

/-- `∑_{r ∣ n, p ∤ r} μ(r)`. -/
def tsum (p n : Nat) : Int :=
  ((List.range (n + 1)).map fun r => if 0 < r ∧ r ∣ n ∧ ¬ p ∣ r then mu r else 0).sum

theorem isum_neg {α} (f : α → Int) : ∀ l : List α, (l.map fun x => -f x).sum = -(l.map f).sum
  | [] => by simp
  | x :: l => by simp only [List.map_cons, List.sum_cons, isum_neg f l]; omega

theorem ite_congr' {c d : Prop} [Decidable c] [Decidable d] (h : c ↔ d) (a b : Int) :
    (if c then a else b) = (if d then a else b) := by
  by_cases hc : c
  · simp [hc, h.mp hc]
  · have hd : ¬ d := fun hd => hc (h.mpr hd)
    simp [hc, hd]

theorem mu_one : mu 1 = 1 := by decide

theorem mu_zero : mu 0 = 0 := by decide

theorem dsum_mu (n : Nat) (hn : 2 ≤ n) : dsum n mu = 0 := by
  have h := mu_divisor_sum n (by omega)
  rw [isum_filter] at h
  have hn1 : n ≠ 1 := by omega
  simp only [hn1, ↓reduceIte] at h
  rw [← h]; unfold dsum
  apply isum_congr; intro r _
  apply ite_congr'
  by_cases h0 : r = 0
  · subst h0; simp
  · simp [h0, Nat.dvd_iff_mod_eq_zero]; omega

theorem prime_coprime {p d : Nat} (hp : IsPrime p) (h : ¬ p ∣ d) : Nat.Coprime p d := by
  rcases hp.2 _ (Nat.gcd_dvd_left p d) with h1 | h1
  · exact h1
  · exact absurd (h1 ▸ Nat.gcd_dvd_right p d) h

theorem euclid {p d n : Nat} (hp : IsPrime p) (h : ¬ p ∣ d) (hd : d ∣ p * n) : d ∣ n :=
  Nat.Coprime.dvd_of_dvd_mul_left (Nat.Coprime.symm (prime_coprime hp h)) hd

theorem isum_mult (p : Nat) (hp : 1 ≤ p) (g : Nat → Int) (hg : ∀ d, ¬ p ∣ d → g d = 0) :
    ∀ N, ((List.range (p * N + 1)).map g).sum =
      ((List.range (N + 1)).map fun e => g (p * e)).sum
  | 0 => by simp
  | N + 1 => by
    rw [List.range_succ, List.map_append, List.sum_append, List.range_succ (n := N + 1),
      List.map_append, List.sum_append, ← isum_mult p hp g hg N,
      isum_range_extend (p * N + 1) (p * (N + 1)) g (by rw [Nat.mul_succ]; omega)]
    · simp
    intro v h1 h2
    apply hg
    intro ⟨k, hk⟩
    subst hk
    have : N < k := Nat.lt_of_mul_lt_mul_left (a := p) (by omega)
    have : k < N + 1 := Nat.lt_of_mul_lt_mul_left h2
    omega
  
/-- Splitting the divisors of `p n` by whether `p` divides them. -/
theorem dsum_split (p n : Nat) (hp : IsPrime p) (hn : 1 ≤ n) :
    dsum (p * n) mu = tsum p n + dsum n (fun e => mu (p * e)) := by
  have hp1 : 0 < p := by have := hp.1; omega
  have hnp : n ≤ p * n := Nat.le_mul_of_pos_left n hp1
  have e1 : dsum (p * n) mu =
      ((List.range (p * n + 1)).map fun r =>
        if 0 < r ∧ r ∣ p * n ∧ ¬ p ∣ r then mu r else 0).sum +
      ((List.range (p * n + 1)).map fun r =>
        if 0 < r ∧ r ∣ p * n ∧ p ∣ r then mu r else 0).sum := by
    unfold dsum; rw [← isum_add]; apply isum_congr; intro r _
    by_cases h1 : 0 < r ∧ r ∣ p * n
    · by_cases h2 : p ∣ r <;> simp [h1, h2]
    · have h3 : ¬ (0 < r ∧ r ∣ p * n ∧ ¬ p ∣ r) := fun h => h1 ⟨h.1, h.2.1⟩
      have h4 : ¬ (0 < r ∧ r ∣ p * n ∧ p ∣ r) := fun h => h1 ⟨h.1, h.2.1⟩
      simp only [h1, h3, h4, ↓reduceIte, Int.add_zero]
  have e2 : ((List.range (p * n + 1)).map fun r =>
        if 0 < r ∧ r ∣ p * n ∧ ¬ p ∣ r then mu r else 0).sum = tsum p n := by
    rw [isum_range_extend (n + 1) (p * n + 1) _ (by omega)]
    · unfold tsum; apply isum_congr; intro r _
      apply ite_congr'
      constructor
      · intro ⟨h1, h2, h3⟩; exact ⟨h1, euclid hp h3 h2, h3⟩
      · intro ⟨h1, h2, h3⟩; exact ⟨h1, Nat.dvd_trans h2 (Nat.dvd_mul_left n p), h3⟩
    · intro v h1 _
      have : ¬ (0 < v ∧ v ∣ p * n ∧ ¬ p ∣ v) := by
        intro ⟨_, h2, h3⟩
        have := Nat.le_of_dvd hn (euclid hp h3 h2)
        omega
      simp only [this]; rfl
  have e3 : ((List.range (p * n + 1)).map fun r =>
        if 0 < r ∧ r ∣ p * n ∧ p ∣ r then mu r else 0).sum = dsum n (fun e => mu (p * e)) := by
    rw [isum_mult p hp1 _ (fun d hd => by simp [hd])]
    unfold dsum; apply isum_congr; intro e _
    apply ite_congr'
    rw [Nat.mul_dvd_mul_iff_left hp1]
    constructor
    · intro ⟨h1, h2, _⟩; exact ⟨Nat.pos_of_mul_pos_left h1, h2⟩
    · intro ⟨h1, h2⟩; exact ⟨Nat.mul_pos hp1 h1, h2, Nat.dvd_mul_right p e⟩
  rw [e1, e2, e3]

theorem dsum_last (n : Nat) (hn : 1 ≤ n) (f : Nat → Int) :
    dsum n f = ((List.range n).map fun r => if 0 < r ∧ r ∣ n then f r else 0).sum + f n := by
  unfold dsum
  rw [List.range_succ, List.map_append, List.sum_append]
  have : 0 < n ∧ n ∣ n := ⟨hn, Nat.dvd_refl n⟩
  simp [this]

/-- **`μ(p n) = -μ(n)`** for `p` prime, `p ∤ n`, `n ≥ 1`. -/
theorem mu_prime_mul (p : Nat) (hp : IsPrime p) :
    ∀ n, 1 ≤ n → ¬ p ∣ n → mu (p * n) = - mu n := by
  intro n
  induction n using Nat.strongRecOn with
  | ind n ih =>
  intro hn hpn
  have hp2 := hp.1
  have hs := dsum_split p n hp hn
  rw [dsum_mu (p * n) (by have := Nat.mul_le_mul hp2 hn; omega)] at hs
  have ht : tsum p n = dsum n mu := by
    unfold tsum dsum; apply isum_congr; intro r _; apply ite_congr'
    constructor
    · intro ⟨a, b, _⟩; exact ⟨a, b⟩
    · intro ⟨a, b⟩; exact ⟨a, b, fun h => hpn (Nat.dvd_trans h b)⟩
  rw [ht, dsum_last n hn, dsum_last n hn] at hs
  have hA : ((List.range n).map fun r => if 0 < r ∧ r ∣ n then mu (p * r) else 0).sum =
      -((List.range n).map fun r => if 0 < r ∧ r ∣ n then mu r else 0).sum := by
    rw [← isum_neg]; apply isum_congr; intro r hr
    have hr' := List.mem_range.mp hr
    by_cases h : 0 < r ∧ r ∣ n
    · simp only [h, and_self, ↓reduceIte]
      exact ih r hr' h.1 (fun hpr => hpn (Nat.dvd_trans hpr h.2))
    · simp only [h, ↓reduceIte, Int.neg_zero]
  rw [hA] at hs
  omega

/-- **`μ(p n) = 0`** for `p` prime, `p ∣ n`, `n ≥ 1` (so `μ` vanishes on multiples of `p²`). -/
theorem mu_prime_mul_dvd (p : Nat) (hp : IsPrime p) :
    ∀ n, 1 ≤ n → p ∣ n → mu (p * n) = 0 := by
  intro n
  induction n using Nat.strongRecOn with
  | ind n ih =>
  intro hn hpn
  have hp2 := hp.1
  have hs := dsum_split p n hp hn
  rw [dsum_mu (p * n) (by have := Nat.mul_le_mul hp2 hn; omega)] at hs
  have ht : tsum p n = ((List.range n).map fun r =>
      if 0 < r ∧ r ∣ n ∧ ¬ p ∣ r then mu r else 0).sum := by
    unfold tsum
    rw [List.range_succ, List.map_append, List.sum_append]
    simp [hpn]
  rw [ht, dsum_last n hn] at hs
  have hA : ((List.range n).map fun r => if 0 < r ∧ r ∣ n then mu (p * r) else 0).sum =
      -((List.range n).map fun r => if 0 < r ∧ r ∣ n ∧ ¬ p ∣ r then mu r else 0).sum := by
    rw [← isum_neg]; apply isum_congr; intro r hr
    have hr' := List.mem_range.mp hr
    by_cases h : 0 < r ∧ r ∣ n
    · by_cases hpr : p ∣ r
      · simp only [h, hpr, not_true_eq_false, and_false, and_self, ↓reduceIte, Int.neg_zero]
        exact ih r hr' h.1 hpr
      · have h' : 0 < r ∧ r ∣ n ∧ ¬ p ∣ r := ⟨h.1, h.2, hpr⟩
        simp only [h, h', and_self, ↓reduceIte]
        exact mu_prime_mul p hp r h.1 hpr
    · have h' : ¬ (0 < r ∧ r ∣ n ∧ ¬ p ∣ r) := fun h'' => h ⟨h''.1, h''.2.1⟩
      simp only [h, h', ↓reduceIte, Int.neg_zero]
  rw [hA] at hs
  omega

/-- **`μ(p) = -1`** for every prime `p`. -/
theorem mu_prime (p : Nat) (hp : IsPrime p) : mu p = -1 := by
  have := mu_prime_mul p hp 1 (Nat.le_refl 1)
    (fun h => by have := Nat.le_of_dvd (by omega) h; have := hp.1; omega)
  rw [Nat.mul_one, mu_one] at this
  exact this

/-- **`μ(n) = 0` if `p² ∣ n`** (`p` prime, `n ≥ 1`). -/
theorem mu_eq_zero_of_sq_dvd (p n : Nat) (hp : IsPrime p) (hn : 1 ≤ n) (h : p * p ∣ n) :
    mu n = 0 := by
  obtain ⟨m, rfl⟩ := h
  rw [Nat.mul_assoc]
  apply mu_prime_mul_dvd p hp (p * m) _ (Nat.dvd_mul_right p m)
  cases m with
  | zero => simp at hn
  | succ m => have := hp.1; have := Nat.mul_le_mul (Nat.le_refl p) (Nat.le_add_left 1 m); omega

theorem exists_prime_dvd : ∀ n, 2 ≤ n → ∃ p, IsPrime p ∧ p ∣ n := by
  intro n
  induction n using Nat.strongRecOn with
  | ind n ih =>
  intro hn
  by_cases h : ∀ d, d ∣ n → d = 1 ∨ d = n
  · exact ⟨n, ⟨hn, h⟩, Nat.dvd_refl n⟩
  · have : ∃ d, d ∣ n ∧ d ≠ 1 ∧ d ≠ n := by
      apply Classical.byContradiction; intro hc; apply h; intro d hd
      by_cases h1 : d = 1
      · exact Or.inl h1
      · by_cases h2 : d = n
        · exact Or.inr h2
        · exact absurd ⟨d, hd, h1, h2⟩ hc
    obtain ⟨d, hd, h1, h2⟩ := this
    have hle := Nat.le_of_dvd (by omega) hd
    have hd0 : d ≠ 0 := by
      rintro rfl; have := Nat.eq_zero_of_zero_dvd hd; omega
    obtain ⟨p, hp, hpd⟩ := ih d (by omega) (by omega)
    exact ⟨p, hp, Nat.dvd_trans hpd hd⟩

/-- `μ(n) ≠ 0` implies `n` squarefree. -/
theorem sqf_of_mu (n : Nat) (hn : 1 ≤ n) (h : mu n ≠ 0) : Sqf n :=
  fun p hp hd => h (mu_eq_zero_of_sq_dvd p n hp hn hd)

theorem sqf_of_dvd {m n : Nat} (h : Sqf n) (hmn : m ∣ n) : Sqf m :=
  fun p hp hd => h p hp (Nat.dvd_trans hd hmn)

/-- Core of the sign identity: `μ(a) μ(x) = μ(x / a)` for `a ∣ x`, `x ≥ 1` squarefree. -/
theorem mu_sign_sqf : ∀ x, 1 ≤ x → Sqf x → ∀ a, a ∣ x → mu a * mu x = mu (x / a) := by
  intro x
  induction x using Nat.strongRecOn with
  | ind x ih =>
  intro hx hsq a ha
  by_cases hx1 : x = 1
  · subst hx1
    have := Nat.eq_one_of_dvd_one ha
    subst this
    decide
  obtain ⟨p, hp, x', rfl⟩ := exists_prime_dvd x (by omega)
  have hp2 := hp.1
  have hp0 : 0 < p := by omega
  have hx' : 1 ≤ x' := by
    cases x' with
    | zero => simp at hx
    | succ _ => omega
  have hpx' : ¬ p ∣ x' := fun h => hsq p hp (Nat.mul_dvd_mul_left p h)
  have hsq' : Sqf x' := sqf_of_dvd hsq (Nat.dvd_mul_left x' p)
  have hlt : x' < p * x' := by
    have := Nat.mul_le_mul_right x' hp2; omega
  rw [mu_prime_mul p hp x' hx' hpx']
  by_cases hpa : p ∣ a
  · obtain ⟨a', rfl⟩ := hpa
    have ha' : a' ∣ x' := (Nat.mul_dvd_mul_iff_left hp0).mp ha
    have hpa' : ¬ p ∣ a' := fun h => hpx' (Nat.dvd_trans h ha')
    have ha1 : 1 ≤ a' := by
      cases a' with
      | zero => have := Nat.eq_zero_of_zero_dvd ha'; omega
      | succ _ => omega
    rw [mu_prime_mul p hp a' ha1 hpa', Nat.mul_div_mul_left x' a' hp0, Int.neg_mul_neg]
    exact ih x' hlt hx' hsq' a' ha'
  · have ha' : a ∣ x' := euclid hp hpa ha
    have hq : x' / a ∣ x' := Nat.div_dvd_of_dvd ha'
    have hq1 : 1 ≤ x' / a := by
      cases h : x' / a with
      | zero => rw [h] at hq; have := Nat.eq_zero_of_zero_dvd hq; omega
      | succ _ => omega
    rw [Nat.mul_div_assoc p ha', mu_prime_mul p hp (x' / a) hq1 (fun h => hpx' (Nat.dvd_trans h hq)),
      ← ih x' hlt hx' hsq' a ha', Int.mul_neg]

/-- **The 1-d sign identity for every squarefree `c ≥ 1`.** -/
theorem muSign_of_sqfree (c : Nat) (h1 : 1 ≤ c) (hmu : mu c ≠ 0) : MuSign c := by
  intro a x hx ha
  have hxc : x ∣ c := Nat.dvd_of_mod_eq_zero hx
  have hx1 : 1 ≤ x := by
    cases x with
    | zero => have := Nat.eq_zero_of_zero_dvd hxc; omega
    | succ _ => omega
  exact mu_sign_sqf x hx1 (sqf_of_dvd (sqf_of_mu c h1 hmu) hxc) a (Nat.dvd_of_mod_eq_zero ha)

theorem exists_sq_of_not_sqf {n : Nat} (h : ¬ Sqf n) : ∃ p, IsPrime p ∧ p * p ∣ n :=
  Classical.byContradiction fun hc => h fun p hp hd => hc ⟨p, hp, hd⟩

theorem sqf_mul {m n : Nat} (hc : Nat.Coprime m n) (hm : Sqf m) (hn : Sqf n) : Sqf (m * n) := by
  intro p hp hd
  have hp1 : ¬ p ∣ 1 := fun h => by have := Nat.le_of_dvd (by omega) h; have := hp.1; omega
  by_cases hpm : p ∣ m
  · have hpn : ¬ p ∣ n := fun h => hp1 (hc ▸ Nat.dvd_gcd hpm h)
    have hcop := prime_coprime hp hpn
    exact hm p hp (Nat.Coprime.dvd_of_dvd_mul_right (Nat.Coprime.mul_left hcop hcop) hd)
  · have hcop := prime_coprime hp hpm
    rw [Nat.mul_comm m n] at hd
    exact hn p hp (Nat.Coprime.dvd_of_dvd_mul_right (Nat.Coprime.mul_left hcop hcop) hd)

/-- `μ(n)² = 1` for squarefree `n ≥ 1`. -/
theorem mu_mul_self_sqf (n : Nat) (hn : 1 ≤ n) (h : Sqf n) : mu n * mu n = 1 := by
  have := mu_sign_sqf n hn h n (Nat.dvd_refl n)
  rw [Nat.div_self (by omega), mu_one] at this
  exact this

/-- **Multiplicativity of `μ`:** `μ(m n) = μ(m) μ(n)` for coprime `m, n`. -/
theorem mu_mul_coprime (m n : Nat) (hc : Nat.Coprime m n) : mu (m * n) = mu m * mu n := by
  by_cases hm0 : m = 0
  · subst hm0; simp [mu_zero]
  by_cases hn0 : n = 0
  · subst hn0; simp [mu_zero]
  have hmn : 1 ≤ m * n := Nat.mul_pos (by omega) (by omega)
  by_cases hm : Sqf m
  · by_cases hn : Sqf n
    · have h1 := mu_sign_sqf (m * n) hmn (sqf_mul hc hm hn) m (Nat.dvd_mul_right m n)
      rw [Nat.mul_div_cancel_left n (by omega)] at h1
      have h2 := mu_mul_self_sqf m (by omega) hm
      calc mu (m * n) = (mu m * mu m) * mu (m * n) := by rw [h2, Int.one_mul]
        _ = mu m * (mu m * mu (m * n)) := Int.mul_assoc ..
        _ = mu m * mu n := by rw [h1]
    · obtain ⟨p, hp, hd⟩ := exists_sq_of_not_sqf hn
      rw [mu_eq_zero_of_sq_dvd p n hp (by omega) hd, Int.mul_zero,
        mu_eq_zero_of_sq_dvd p (m * n) hp hmn (Nat.dvd_trans hd (Nat.dvd_mul_left n m))]
  · obtain ⟨p, hp, hd⟩ := exists_sq_of_not_sqf hm
    rw [mu_eq_zero_of_sq_dvd p m hp (by omega) hd, Int.zero_mul,
      mu_eq_zero_of_sq_dvd p (m * n) hp hmn (Nat.dvd_trans hd (Nat.dvd_mul_right m n))]

end MuMult

open MuMult MaynardInv

/-- **Maynard's inversion `λ ↦ y ↦ λ`, every `R`, every `k`**, for weights supported on tuples
with squarefree entries (`μ(eᵢ) ≠ 0`); `maynard_lam_of_y_sqfree` with `hMu` discharged. -/
theorem maynard_lam_of_y_sqfree_all (R k : Nat) (lam : List Nat → Rat)
    (hS : ∀ e ∈ box R k, lam e ≠ 0 → ∀ c ∈ e, mu c ≠ 0)
    (d : List Nat) (hd : d ∈ box R k) :
    maynardLam R k (maynardY R k lam) d = lam d :=
  maynard_lam_of_y_sqfree R k (fun c h1 _ hmu => muSign_of_sqfree c h1 hmu) lam hS d hd

/-- **Maynard's inversion `y ↦ λ ↦ y`, every `R`, every `k`**, for squarefree-supported `y`. -/
theorem maynard_y_of_lam_sqfree_all (R k : Nat) (y : List Nat → Rat)
    (hS : ∀ e ∈ box R k, y e ≠ 0 → ∀ c ∈ e, mu c ≠ 0)
    (r : List Nat) (hr : r ∈ box R k) :
    maynardY R k (maynardLam R k y) r = y r :=
  maynard_y_of_lam_sqfree R k (fun c h1 _ hmu => muSign_of_sqfree c h1 hmu) y hS r hr

end TwinPrimes
