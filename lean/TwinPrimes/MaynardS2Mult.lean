import TwinPrimes.MaynardS2Y

/-!
# Multiplicativity facts for `φ` and `g = μ ∗ φ`; the `S₂` theorems without `hphi` / `hg`

Discharges the arithmetic hypotheses of `MaynardS2Y`:

* `totient_prime_mul`: `φ(p x) = p φ(x)` if `p ∣ x`, `= (p − 1) φ(x)` if `p ∤ x` (`p` prime, all `x`),
  by counting residues (no CRT bijection needed).
* `totient_lcm_mul_gcd`: **`φ([a,b]) φ((a,b)) = φ(a) φ(b)` for ALL `a, b`** (exactly the
  hypothesis `hphi` of `MaynardS2Y.maynard_S2_diag_lcm`, without the side conditions).
  `totient_mul_coprime`: `φ(m n) = φ(m) φ(n)` for coprime `m, n`.
* `gM_prime_mul`: `g(p n) = (p − 2) g(n)` for `p` prime, `p ∤ n`, `n ≥ 1`.
  `gM_mul_coprime_sqf`: `g(m n) = g(m) g(n)` for coprime `m, n` with `m` squarefree
  (`n` arbitrary). `gM_pos_of_odd_sqf`: `g(n) > 0` for odd squarefree `n ≥ 1`.
* `maynard_S2_diag_lcm_all`: `maynard_S2_diag_lcm` with `hphi` removed (every `R`, `k`).
* `maynard_S2_lam_of_y_odd`: `maynard_S2_lam_of_y` with `hg` replaced by Maynard's support
  condition "entries odd" (`(dᵢ, W) = 1`, `2 ∣ W`); `maynard_S2_lam_of_y_W` in the `W` form.

NOT covered: multiplicativity of `gM` when neither argument is squarefree (not needed: `gM`
only enters at squarefree arguments).
-/

namespace TwinPrimes
namespace MaynardS2Mult

open Gauss SelbergOpt MaynardInv MuMult MaynardDiag MaynardS2Y

/-! ## Counting lemmas -/

theorem cnt_add (a : Nat) (P : Nat → Bool) : ∀ b,
    cnt (a + b) P = cnt a P + cnt b (fun t => P (a + t))
  | 0 => rfl
  | b + 1 => by
    rw [← Nat.add_assoc, cnt_succ, cnt_add a P b, cnt_succ]; omega

theorem periodic_iter (n : Nat) (P : Nat → Bool) (hP : ∀ k, P (k + n) = P k) :
    ∀ j t, P (j * n + t) = P t
  | 0, t => by rw [Nat.zero_mul, Nat.zero_add]
  | j + 1, t => by
    rw [Nat.succ_mul, Nat.add_assoc, Nat.add_comm n t, ← Nat.add_assoc, hP, periodic_iter n P hP j t]

theorem cnt_periodic (n : Nat) (P : Nat → Bool) (hP : ∀ k, P (k + n) = P k) :
    ∀ j, cnt (j * n) P = j * cnt n P
  | 0 => by simp [cnt]
  | j + 1 => by
    rw [Nat.succ_mul, cnt_add, cnt_periodic n P hP j, Nat.succ_mul]
    congr 1
    exact cnt_congr n _ _ (fun t _ => periodic_iter n P hP j t)

theorem cnt_split (P Q : Nat → Bool) : ∀ n,
    cnt n P = cnt n (fun k => P k && Q k) + cnt n (fun k => P k && !Q k)
  | 0 => rfl
  | n + 1 => by
    rw [cnt_succ, cnt_succ, cnt_succ, cnt_split P Q n]
    cases P n <;> cases Q n <;> simp <;> omega

theorem totient_eq_cnt (n : Nat) : totient n = cnt n (fun k => Nat.gcd (k + 1) n == 1) := rfl

theorem totient_zero : totient 0 = 0 := rfl

/-- `#{0 ≤ k < j n : gcd(k+1, n) = 1} = j φ(n)`. -/
theorem cnt_coprime_mul (n j : Nat) :
    cnt (j * n) (fun k => Nat.gcd (k + 1) n == 1) = j * totient n := by
  rw [cnt_periodic n _ (fun k => by
    rw [show k + n + 1 = (k + 1) + n by omega, Nat.gcd_add_self_left]) j]
  rfl

/-- **`φ(p n) = p φ(n)`** if `p ∣ n` (any `p`). -/
theorem totient_mul_of_dvd (p n : Nat) (h : p ∣ n) : totient (p * n) = p * totient n := by
  rw [totient_eq_cnt, ← cnt_coprime_mul n p]
  apply cnt_congr; intro k _
  apply Bool.eq_iff_iff.mpr
  simp only [beq_iff_eq]
  change Nat.Coprime (k + 1) (p * n) ↔ Nat.Coprime (k + 1) n
  rw [Nat.coprime_mul_iff_right]
  exact ⟨fun h' => h'.2, fun h' => ⟨Nat.Coprime.coprime_dvd_right h h', h'⟩⟩

/-- **`φ(p n) = (p − 1) φ(n)`** for `p` prime, `p ∤ n`. -/
theorem totient_mul_of_not_dvd (p n : Nat) (hp : IsPrime p) (h : ¬ p ∣ n) :
    totient (p * n) = (p - 1) * totient n := by
  have hp2 := hp.1
  have hcop : Nat.Coprime p n := prime_coprime hp h
  have hs := cnt_split (fun k => Nat.gcd (k + 1) n == 1) (fun k => Nat.gcd (k + 1) p == 1) (p * n)
  rw [show p * n = n * p from Nat.mul_comm p n] at hs
  rw [show cnt (n * p) (fun k => Nat.gcd (k + 1) n == 1) = p * totient n by
    rw [Nat.mul_comm n p]; exact cnt_coprime_mul n p] at hs
  have h1 : cnt (n * p) (fun k => (Nat.gcd (k + 1) n == 1) && (Nat.gcd (k + 1) p == 1))
      = totient (p * n) := by
    rw [totient_eq_cnt, Nat.mul_comm n p]
    apply cnt_congr; intro k _
    apply Bool.eq_iff_iff.mpr
    simp only [Bool.and_eq_true, beq_iff_eq]
    change Nat.Coprime (k + 1) n ∧ Nat.Coprime (k + 1) p ↔ Nat.Coprime (k + 1) (p * n)
    rw [Nat.coprime_mul_iff_right]
    exact ⟨fun ⟨a, b⟩ => ⟨b, a⟩, fun ⟨a, b⟩ => ⟨b, a⟩⟩
  have h2 : cnt (n * p) (fun k => (Nat.gcd (k + 1) n == 1) && !(Nat.gcd (k + 1) p == 1))
      = totient n := by
    rw [cnt_mul n p (by omega)]
    · rw [totient_eq_cnt]
      apply cnt_congr; intro j _
      have e1 : j * p + (p - 1) + 1 = (j + 1) * p := by rw [Nat.succ_mul]; omega
      rw [e1, Nat.Coprime.gcd_mul_right_cancel (j + 1) hcop, Nat.gcd_mul_left_left]
      have : (p == 1) = false := by simp; omega
      simp [this]
    · intro k hk
      simp only [Bool.and_eq_true, Bool.not_eq_true', beq_eq_false_iff_ne] at hk
      rcases hp.2 _ (Nat.gcd_dvd_right (k + 1) p) with h' | h'
      · exact absurd h' hk.2
      · exact h' ▸ Nat.gcd_dvd_left (k + 1) p
  rw [h1, h2] at hs
  rw [Nat.sub_mul, Nat.one_mul]
  omega

/-- `φ(p x) = (p if p ∣ x else p − 1) · φ(x)` for `p` prime and every `x`. -/
theorem totient_prime_mul (p x : Nat) (hp : IsPrime p) :
    totient (p * x) = (if p ∣ x then p else p - 1) * totient x := by
  by_cases h : p ∣ x
  · rw [ite_eq_left h]; exact totient_mul_of_dvd p x h
  · rw [ite_eq_right h]; exact totient_mul_of_not_dvd p x hp h

/-- **`φ([a,b]) φ((a,b)) = φ(a) φ(b)` for all `a, b`** (Maynard's (5.21) in the form used by
`MaynardS2Y.maynard_S2_diag_lcm`, hypothesis `hphi`). -/
theorem totient_lcm_mul_gcd (a : Nat) : ∀ b,
    totient (Nat.lcm a b) * totient (Nat.gcd a b) = totient a * totient b := by
  induction a using Nat.strongRecOn with
  | ind a ih =>
  intro b
  rcases Nat.lt_or_ge a 2 with ha | ha
  · rcases (show a = 0 ∨ a = 1 by omega) with rfl | rfl
    · rw [Nat.lcm_zero_left, Nat.gcd_zero_left]
    · rw [Nat.lcm_one_left, Nat.gcd_one_left, Nat.mul_comm]
  · obtain ⟨p, hp, a', rfl⟩ := exists_prime_dvd _ ha
    have hp2 := hp.1
    have ha' : 1 ≤ a' := by
      rcases Nat.eq_zero_or_pos a' with h | h
      · subst h; omega
      · exact h
    have hlt : a' < p * a' := by
      have := Nat.mul_le_mul_right a' hp2; omega
    have IH := ih a' hlt b
    have hGL := Nat.gcd_mul_lcm a' b
    have hG : 0 < Nat.gcd a' b := Nat.gcd_pos_of_pos_left _ ha'
    have hHL := Nat.gcd_mul_lcm (p * a') b
    have hGH : Nat.gcd a' b ∣ Nat.gcd (p * a') b :=
      Nat.dvd_gcd (Nat.dvd_trans (Nat.gcd_dvd_left _ _) (Nat.dvd_mul_left a' p))
        (Nat.gcd_dvd_right _ _)
    have hHp : Nat.gcd (p * a') b ∣ Nat.gcd a' b * p := by
      rw [Nat.mul_comm _ p, ← Nat.gcd_mul_left]
      exact Nat.dvd_gcd (Nat.gcd_dvd_left _ _)
        (Nat.dvd_trans (Nat.gcd_dvd_right _ _) (Nat.dvd_mul_left b p))
    obtain ⟨t, ht⟩ := hGH
    rw [ht] at hHp
    have htp : t ∣ p := Nat.dvd_of_mul_dvd_mul_left hG hHp
    rcases hp.2 t htp with h1 | h1
    · -- `gcd(p a', b) = gcd(a', b)`, `lcm(p a', b) = p lcm(a', b)`
      rw [h1, Nat.mul_one] at ht
      have hL : Nat.lcm (p * a') b = p * Nat.lcm a' b := by
        apply Nat.eq_of_mul_eq_mul_left hG
        have e := hHL; rw [ht] at e
        rw [e, Nat.mul_left_comm, hGL, Nat.mul_assoc]
      have hc : p ∣ Nat.lcm a' b ↔ p ∣ a' := by
        constructor
        · intro hpl
          apply Classical.byContradiction; intro hpa
          have hab : p ∣ a' * b :=
            Nat.dvd_trans hpl (Nat.lcm_dvd (Nat.dvd_mul_right a' b) (Nat.dvd_mul_left b a'))
          have hpb : p ∣ b := Nat.Coprime.dvd_of_dvd_mul_left (prime_coprime hp hpa) hab
          have : p ∣ Nat.gcd (p * a') b := Nat.dvd_gcd (Nat.dvd_mul_right p a') hpb
          rw [ht] at this
          exact hpa (Nat.dvd_trans this (Nat.gcd_dvd_left a' b))
        · intro hpa; exact Nat.dvd_trans hpa (Nat.dvd_lcm_left a' b)
      have hcc : (if p ∣ Nat.lcm a' b then p else p - 1) = (if p ∣ a' then p else p - 1) := by
        by_cases h : p ∣ a'
        · rw [ite_eq_left h, ite_eq_left (hc.mpr h)]
        · rw [ite_eq_right h, ite_eq_right (fun h' => h (hc.mp h'))]
      rw [hL, ht, totient_prime_mul p _ hp, totient_prime_mul p a' hp, hcc, Nat.mul_assoc, IH,
        Nat.mul_assoc]
    · -- `gcd(p a', b) = p gcd(a', b)`, `lcm(p a', b) = lcm(a', b)`
      rw [h1] at ht
      have hGp : 0 < Nat.gcd a' b * p := Nat.mul_pos hG (by omega)
      have hL : Nat.lcm (p * a') b = Nat.lcm a' b := by
        apply Nat.eq_of_mul_eq_mul_left hGp
        have e := hHL; rw [ht] at e
        rw [e, Nat.mul_right_comm (Nat.gcd a' b) p, hGL, Nat.mul_comm (a' * b) p, Nat.mul_assoc]
      have hc : p ∣ Nat.gcd a' b ↔ p ∣ a' := by
        constructor
        · intro h; exact Nat.dvd_trans h (Nat.gcd_dvd_left a' b)
        · intro hpa
          have hpb : p ∣ b := by
            have : Nat.gcd a' b * p ∣ b := ht ▸ Nat.gcd_dvd_right (p * a') b
            exact Nat.dvd_trans (Nat.dvd_mul_left p _) this
          exact Nat.dvd_gcd hpa hpb
      have hcc : (if p ∣ Nat.gcd a' b then p else p - 1) = (if p ∣ a' then p else p - 1) := by
        by_cases h : p ∣ a'
        · rw [ite_eq_left h, ite_eq_left (hc.mpr h)]
        · rw [ite_eq_right h, ite_eq_right (fun h' => h (hc.mp h'))]
      rw [hL, ht, Nat.mul_comm _ p, totient_prime_mul p _ hp, totient_prime_mul p a' hp, hcc,
        Nat.mul_left_comm, IH, Nat.mul_assoc]

/-- **Multiplicativity of `φ`:** `φ(m n) = φ(m) φ(n)` for coprime `m, n`. -/
theorem totient_mul_coprime (m n : Nat) (h : Nat.Coprime m n) :
    totient (m * n) = totient m * totient n := by
  have e := totient_lcm_mul_gcd m n
  have hl : Nat.lcm m n = m * n := by
    have := Nat.gcd_mul_lcm m n
    rw [h.gcd_eq_one, Nat.one_mul] at this; exact this
  rw [hl, h.gcd_eq_one, totient_one, Nat.mul_one] at e
  exact e

/-! ## `g = μ ∗ φ` -/

/-- Divisor sum `∑_{v ∣ n} F(v)` over `1 ≤ v ≤ n`. -/
def dvs (n : Nat) (F : Nat → Rat) : Rat :=
  ((rng n).map fun v => if n % v = 0 then F v else 0).sum

theorem gM_eq_dvs (x : Nat) :
    gM x = dvs x (fun v => (mu (x / v) : Rat) * (totient v : Rat)) := rfl

theorem gM_zero : gM 0 = 0 := rfl

theorem gM_one : gM 1 = 1 := gM_values.1

theorem natCast_sub_one (p : Nat) (h : 1 ≤ p) : ((p - 1 : Nat) : Rat) = (p : Rat) - 1 := by
  obtain ⟨q, rfl⟩ : ∃ q, p = q + 1 := ⟨p - 1, by omega⟩
  rw [Nat.add_sub_cancel, Rat.natCast_add]
  have : ((1 : Nat) : Rat) = 1 := rfl
  rw [this]; grind

/-- Splitting the divisors of `p n` (`p` prime, `p ∤ n`) into those of `n` and `p` times those. -/
theorem dvs_prime_mul (p n : Nat) (hp : IsPrime p) (hn : 1 ≤ n) (hpn : ¬ p ∣ n)
    (F : Nat → Rat) : dvs (p * n) F = dvs n F + dvs n (fun e => F (p * e)) := by
  have hp1 : 1 ≤ p := by have := hp.1; omega
  have hpn1 : 1 ≤ p * n := Nat.mul_pos hp1 hn
  have hnpn : n ≤ p * n := Nat.le_mul_of_pos_left n hp1
  unfold dvs
  have e1 : ((rng (p * n)).map fun v => if (p * n) % v = 0 then F v else 0).sum
      = ((rng (p * n)).map fun v =>
          if v % p = 0 then 0 else (if (p * n) % v = 0 then F v else 0)).sum
        + ((rng (p * n)).map fun v =>
          if v % p = 0 then (if (p * n) % v = 0 then F v else 0) else 0).sum := by
    rw [← rsum_add]; apply rsum_congr; intro v _
    by_cases h : v % p = 0
    · rw [ite_eq_left h, ite_eq_left h, Rat.zero_add]
    · rw [ite_eq_right h, ite_eq_right h, Rat.add_zero]
  have hn0 : n % 0 ≠ 0 := by rw [Nat.mod_zero]; omega
  have hpn0 : (p * n) % 0 ≠ 0 := by rw [Nat.mod_zero]; omega
  rw [e1]; congr 1
  · rw [rsum_rng (p * n) _ (by simp), rsum_rng n _ (by rw [ite_eq_right hn0]),
      rsum_range_extend (n + 1) (p * n + 1) _ (by omega)]
    · apply rsum_congr; intro v hv
      have hv := List.mem_range.mp hv
      by_cases h0 : v = 0
      · subst h0; rw [ite_eq_right hn0]; simp
      by_cases h : v % p = 0
      · rw [ite_eq_left h, ite_eq_right]
        intro hnv
        exact hpn (Nat.dvd_trans (Nat.dvd_of_mod_eq_zero h) (Nat.dvd_of_mod_eq_zero hnv))
      · rw [ite_eq_right h]
        have hpv : ¬ p ∣ v := fun h' => h (Nat.mod_eq_zero_of_dvd h')
        have : (p * n) % v = 0 ↔ n % v = 0 := by
          rw [← Nat.dvd_iff_mod_eq_zero, ← Nat.dvd_iff_mod_eq_zero]
          exact ⟨euclid hp hpv, fun h' => Nat.dvd_trans h' (Nat.dvd_mul_left n p)⟩
        by_cases h' : n % v = 0
        · rw [ite_eq_left h', ite_eq_left (this.mpr h')]
        · rw [ite_eq_right h', ite_eq_right (fun e => h' (this.mp e))]
    · intro v h1 _
      by_cases h : v % p = 0
      · rw [ite_eq_left h]
      · rw [ite_eq_right h, ite_eq_right]
        intro hv
        have hpv : ¬ p ∣ v := fun h' => h (Nat.mod_eq_zero_of_dvd h')
        have := Nat.le_of_dvd hn (euclid hp hpv (Nat.dvd_of_mod_eq_zero hv))
        omega
  · rw [rsum_rng (p * n) _ (by rw [ite_eq_left (Nat.zero_mod p), ite_eq_right hpn0]), rsum_rng n _ (by rw [ite_eq_right hn0]),
      ← rsum_range_extend (p * n + 1) (p * (n + 1)) _ (by rw [Nat.mul_succ]; omega)]
    · rw [rsum_multiples p hp1 (fun v => if (p * n) % v = 0 then F v else 0) (n + 1)]
      apply rsum_congr; intro m _
      have : (p * n) % (p * m) = 0 ↔ n % m = 0 := by
        rw [Nat.mul_mod_mul_left]
        constructor
        · intro h; rcases Nat.mul_eq_zero.mp h with h | h
          · omega
          · exact h
        · intro h; rw [h, Nat.mul_zero]
      by_cases h' : n % m = 0
      · rw [ite_eq_left h', ite_eq_left (this.mpr h')]
      · rw [ite_eq_right h', ite_eq_right (fun e => h' (this.mp e))]
    · intro v h1 _
      have : (p * n) % v ≠ 0 := by rw [Nat.mod_eq_of_lt (by omega)]; omega
      by_cases h : v % p = 0
      · rw [ite_eq_left h, ite_eq_right this]
      · rw [ite_eq_right h]

/-- **`g(p n) = (p − 2) g(n)`** for `p` prime, `p ∤ n`, `n ≥ 1`. -/
theorem gM_prime_mul (p n : Nat) (hp : IsPrime p) (hn : 1 ≤ n) (hpn : ¬ p ∣ n) :
    gM (p * n) = ((p : Rat) - 2) * gM n := by
  have hp1 : 0 < p := by have := hp.1; omega
  rw [gM_eq_dvs, dvs_prime_mul p n hp hn hpn, gM_eq_dvs]
  have hA : dvs n (fun v => (mu (p * n / v) : Rat) * (totient v : Rat))
      = -1 * dvs n (fun v => (mu (n / v) : Rat) * (totient v : Rat)) := by
    unfold dvs; rw [← rsum_mul_left]; apply rsum_congr; intro v hv
    by_cases h : n % v = 0
    · rw [ite_eq_left h, ite_eq_left h]; dsimp only
      have hvd : v ∣ n := Nat.dvd_of_mod_eq_zero h
      have hv1 := (mem_rng.mp hv).1
      rw [Nat.mul_div_assoc p hvd, mu_prime_mul p hp (n / v)
        (Nat.div_pos (Nat.le_of_dvd hn hvd) hv1)
        (fun h' => hpn (Nat.dvd_trans h' (Nat.div_dvd_of_dvd hvd))), Rat.intCast_neg]
      grind
    · rw [ite_eq_right h, ite_eq_right h, Rat.mul_zero]
  have hB : dvs n (fun e => (mu (p * n / (p * e)) : Rat) * (totient (p * e) : Rat))
      = ((p : Rat) - 1) * dvs n (fun v => (mu (n / v) : Rat) * (totient v : Rat)) := by
    unfold dvs; rw [← rsum_mul_left]; apply rsum_congr; intro v _
    by_cases h : n % v = 0
    · rw [ite_eq_left h, ite_eq_left h]; dsimp only
      have hvd : v ∣ n := Nat.dvd_of_mod_eq_zero h
      rw [Nat.mul_div_mul_left n v hp1,
        totient_mul_of_not_dvd p v hp (fun h' => hpn (Nat.dvd_trans h' hvd)), Rat.natCast_mul,
        natCast_sub_one p hp1]
      grind
    · rw [ite_eq_right h, ite_eq_right h, Rat.mul_zero]
  rw [hA, hB]
  grind

/-- **Multiplicativity of `g`, squarefree left factor:** `g(m n) = g(m) g(n)` for coprime `m, n`
with `m` squarefree (`n` arbitrary). -/
theorem gM_mul_coprime_sqf (m : Nat) : Sqf m → ∀ n, Nat.Coprime m n →
    gM (m * n) = gM m * gM n := by
  induction m using Nat.strongRecOn with
  | ind m ih =>
  intro hm n hc
  rcases Nat.lt_or_ge m 2 with h2 | h2
  · rcases (show m = 0 ∨ m = 1 by omega) with rfl | rfl
    · rw [Nat.zero_mul, gM_zero, Rat.zero_mul]
    · rw [Nat.one_mul, gM_one, Rat.one_mul]
  · obtain ⟨p, hp, m', rfl⟩ := exists_prime_dvd _ h2
    have hp2 := hp.1
    have hm' : 1 ≤ m' := by
      rcases Nat.eq_zero_or_pos m' with h | h
      · subst h; omega
      · exact h
    have hlt : m' < p * m' := by
      have := Nat.mul_le_mul_right m' hp2; omega
    have hpm' : ¬ p ∣ m' := fun h => hm p hp (Nat.mul_dvd_mul_left p h)
    have hn : 1 ≤ n := by
      rcases Nat.eq_zero_or_pos n with h | h
      · subst h
        have := hc.gcd_eq_one
        rw [Nat.gcd_zero_right] at this; omega
      · exact h
    have hpn : ¬ p ∣ n := fun h => by
      have := Nat.le_of_dvd (by omega) (hc.gcd_eq_one ▸ Nat.dvd_gcd (Nat.dvd_mul_right p m') h)
      omega
    have hc' : Nat.Coprime m' n := Nat.Coprime.coprime_dvd_left (Nat.dvd_mul_left m' p) hc
    have hpmn : ¬ p ∣ m' * n := fun h => by
      have hcop := Nat.Coprime.mul_right (prime_coprime hp hpm') (prime_coprime hp hpn)
      have := Nat.le_of_dvd (by omega) (hcop.gcd_eq_one ▸ Nat.dvd_gcd (Nat.dvd_refl p) h)
      omega
    rw [Nat.mul_assoc, gM_prime_mul p (m' * n) hp (Nat.mul_pos hm' hn) hpmn,
      ih m' hlt (sqf_of_dvd hm (Nat.dvd_mul_left m' p)) n hc', gM_prime_mul p m' hp hm' hpm',
      Rat.mul_assoc]

/-- **`g(n) > 0` for odd squarefree `n ≥ 1`** (so `g(n) = ∏_{p ∣ n} (p − 2) ≠ 0` on Maynard's
support, where all entries are coprime to `W`, `2 ∣ W`). -/
theorem gM_pos_of_odd_sqf (n : Nat) : 1 ≤ n → Sqf n → n % 2 = 1 → 0 < gM n := by
  induction n using Nat.strongRecOn with
  | ind n ih =>
  intro hn hs ho
  rcases Nat.lt_or_ge n 2 with h2 | h2
  · rw [show n = 1 by omega, gM_one]; decide
  · obtain ⟨p, hp, n', rfl⟩ := exists_prime_dvd _ h2
    have hp2 := hp.1
    have hn' : 1 ≤ n' := by
      rcases Nat.eq_zero_or_pos n' with h | h
      · subst h; omega
      · exact h
    have hlt : n' < p * n' := by
      have := Nat.mul_le_mul_right n' hp2; omega
    have hpn' : ¬ p ∣ n' := fun h => hs p hp (Nat.mul_dvd_mul_left p h)
    have hp3 : 3 ≤ p := by
      apply Classical.byContradiction; intro h
      have : p = 2 := by omega
      subst this
      rw [Nat.mul_mod_right] at ho; omega
    have ho' : n' % 2 = 1 := by
      apply Classical.byContradiction; intro h
      have h2 : 2 ∣ n' := Nat.dvd_of_mod_eq_zero (by omega)
      have := Nat.mod_eq_zero_of_dvd (Nat.dvd_trans h2 (Nat.dvd_mul_left n' p))
      omega
    rw [gM_prime_mul p n' hp hn' hpn']
    apply Rat.mul_pos _ (ih n' hlt hn' (sqf_of_dvd hs (Nat.dvd_mul_left n' p)) ho')
    obtain ⟨q, rfl⟩ : ∃ q, p = q + 3 := ⟨p - 3, by omega⟩
    rw [Rat.natCast_add]
    have : (0 : Rat) ≤ (q : Rat) := Rat.natCast_nonneg
    grind

/-! ## Tuples: `∏ g(uᵢ) > 0` below odd squarefree tuples -/

theorem tg_pos_of_tdvd : ∀ u d : List Nat, tdvd u d = true →
    (∀ y ∈ d, 1 ≤ y ∧ Sqf y ∧ y % 2 = 1) → 0 < tg u
  | [], [], _, _ => by simp [tg]; decide
  | a :: u, b :: d, h, hd => by
    simp only [tdvd, Bool.and_eq_true, beq_iff_eq] at h
    obtain ⟨hab, hud⟩ := h
    have hb := hd b List.mem_cons_self
    have hadv : a ∣ b := Nat.dvd_of_mod_eq_zero hab
    have ha1 : 1 ≤ a := by
      rcases Nat.eq_zero_or_pos a with h0 | h0
      · subst h0; rw [Nat.mod_zero] at hab; omega
      · exact h0
    have ha2 : a % 2 = 1 := by
      apply Classical.byContradiction; intro h'
      have h2 : 2 ∣ a := Nat.dvd_of_mod_eq_zero (by omega)
      have := Nat.mod_eq_zero_of_dvd (Nat.dvd_trans h2 hadv)
      omega
    have ih := tg_pos_of_tdvd u d hud (fun y hy => hd y (List.mem_cons_of_mem _ hy))
    unfold tg at ih ⊢
    simp only [List.map_cons, List.prod_cons]
    exact Rat.mul_pos (gM_pos_of_odd_sqf a ha1 (sqf_of_dvd hb.2.1 hadv) ha2) ih
  | [], _ :: _, h, _ => by simp [tdvd] at h
  | _ :: _, [], h, _ => by simp [tdvd] at h

/-- **`hg` of `maynard_S2_lam_of_y` holds** for `λ` supported on tuples with odd squarefree
entries. -/
theorem hg_of_odd (R k m : Nat) (lam : List Nat → Rat)
    (hsq : ∀ d ∈ box R k, lam d ≠ 0 → ∀ x ∈ d, mu x ≠ 0)
    (hodd : ∀ d ∈ box R k, lam d ≠ 0 → ∀ x ∈ d, x % 2 = 1) :
    ∀ r ∈ box R k, tg r = 0 → upSum R k (fS2 m lam) r = 0 := by
  intro r _ h0
  unfold upSum
  rw [rsum_congr (g := fun _ => 0), rsum_zero]
  intro d hd
  by_cases hrd : tdvd r d = true
  · rw [ite_eq_left hrd]
    by_cases hl : lam d = 0
    · unfold fS2; simp [hl, rat_div_zero]
    · exfalso
      have := tg_pos_of_tdvd r d hrd (fun y hy => by
        have hy1 := (mem_rng.mp ((mem_box_entries hd).2 y hy)).1
        exact ⟨hy1, sqf_of_mu y hy1 (hsq d hd hl y hy), hodd d hd hl y hy⟩)
      rw [h0] at this; exact Rat.lt_irrefl this
  · rw [ite_eq_right hrd]

/-! ## The `MaynardS2Y` main theorems with the arithmetic hypotheses removed -/

/-- **`maynard_S2_diag_lcm` without `hphi`**, every `R`, `k`, `m`: for `λ` supported on tuples
with squarefree entries,
`∑_{d_m = e_m = 1} λ_d λ_e / ∏ᵢ φ([dᵢ,eᵢ]) = ∑_u (y^{(m)}_u)² / ∏ᵢ g(uᵢ)`. -/
theorem maynard_S2_diag_lcm_all (R k m : Nat) (lam : List Nat → Rat)
    (hsq : ∀ d ∈ box R k, lam d ≠ 0 → ∀ x ∈ d, mu x ≠ 0) :
    (((box R k).filter fun d => d.getD m 1 == 1).map fun d =>
      (((box R k).filter fun e => e.getD m 1 == 1).map fun e =>
        lam d * lam e / tphiLcm d e).sum).sum
      = ((box R k).map fun u => yS2 R k m lam u * yS2 R k m lam u / tg u).sum :=
  maynard_S2_diag_lcm R k m lam (fun a b _ _ _ _ => totient_lcm_mul_gcd a b) hsq

/-- **`maynard_S2_lam_of_y` without `hg`**: for `λ` supported on tuples with odd squarefree
entries, for every `d` in the box,
`μ(d) φ(d) ∑_{d ∣ r} y^{(m)}_r / g(r) = [d_m = 1] λ_d`. -/
theorem maynard_S2_lam_of_y_odd (R k m : Nat) (lam : List Nat → Rat)
    (hsq : ∀ d ∈ box R k, lam d ≠ 0 → ∀ x ∈ d, mu x ≠ 0)
    (hodd : ∀ d ∈ box R k, lam d ≠ 0 → ∀ x ∈ d, x % 2 = 1)
    (d : List Nat) (hd : d ∈ box R k) :
    tmu d * tphi d * upSum R k (fun r => yS2 R k m lam r / tg r) d
      = if d.getD m 1 = 1 then lam d else 0 :=
  maynard_S2_lam_of_y R k m lam hsq (hg_of_odd R k m lam hsq hodd) d hd

/-- Same, with Maynard's literal support condition `(dᵢ, W) = 1` for some even `W`. -/
theorem maynard_S2_lam_of_y_W (R k m W : Nat) (hW : 2 ∣ W) (lam : List Nat → Rat)
    (hsq : ∀ d ∈ box R k, lam d ≠ 0 → ∀ x ∈ d, mu x ≠ 0)
    (hcop : ∀ d ∈ box R k, lam d ≠ 0 → ∀ x ∈ d, Nat.Coprime x W)
    (d : List Nat) (hd : d ∈ box R k) :
    tmu d * tphi d * upSum R k (fun r => yS2 R k m lam r / tg r) d
      = if d.getD m 1 = 1 then lam d else 0 := by
  apply maynard_S2_lam_of_y_odd R k m lam hsq _ d hd
  intro e he hl x hx
  apply Classical.byContradiction; intro h
  have h2 : 2 ∣ x := Nat.dvd_of_mod_eq_zero (by omega)
  have := Nat.le_of_dvd (by omega) ((hcop e he hl x hx).gcd_eq_one ▸ Nat.dvd_gcd h2 hW)
  omega

/-! ## Checks -/

/-- `MaynardS2Y.lamEx` (support `(1,1)`, `(1,3)`) has odd entries. -/
theorem ex_hodd : ∀ d ∈ box 3 2, MaynardS2Y.lamEx d ≠ 0 → ∀ x ∈ d, x % 2 = 1 := by
  decide +kernel

/-- `maynard_S2_lam_of_y_odd` instantiated at `lamEx` (no `decide` of `hg`). -/
theorem maynard_S2_lam_of_y_odd_example (d : List Nat) (hd : d ∈ box 3 2) :
    tmu d * tphi d * upSum 3 2 (fun r => yS2 3 2 0 MaynardS2Y.lamEx r / tg r) d
      = if d.getD 0 1 = 1 then MaynardS2Y.lamEx d else 0 :=
  maynard_S2_lam_of_y_odd 3 2 0 MaynardS2Y.lamEx MaynardS2Y.ex_hsq ex_hodd d hd

/-- Spot values: `φ(36) = 12 = φ(4) φ(9)`, `g(105) = 1·3·5 = 15`, `g(9) = 4` (so `g` is not
`∏ (p − 2)` off squarefree arguments). -/
theorem mult_values : totient 36 = totient 4 * totient 9 ∧ gM 105 = 15 ∧ gM 9 = 4 := by
  decide +kernel

end MaynardS2Mult
end TwinPrimes
