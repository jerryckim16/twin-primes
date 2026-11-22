import TwinPrimes.Selberg
import TwinPrimes.Counting

/-!
# Gauss's identity `∑_{r ∣ n} φ(r) = n` for all `n ≥ 1`

Uses exactly the definitions `totient` and `divisorTotientSum` of `TwinPrimes.Selberg`.

Proof: partition `{1, …, n}` by the value `r = n / gcd(k, n)` (a divisor of `n`). For
`r ∣ n` with `g = n / r`, the `k` with `n / gcd(k, n) = r` are exactly `k = j g` with
`1 ≤ j ≤ r`, `gcd(j, r) = 1`, so there are `φ(r)` of them.

* `gauss_totient`: `divisorTotientSum n = n` for every `n ≥ 1`.
* `selberg_diag`: `selbergLHS D λ = selbergRHS D λ` for every `D` and every `λ : ℕ → ℤ`
  (general-`D` version of `selberg_diag_D6`), via `gcd(d, e) = ∑_{r ∣ d, r ∣ e} φ(r)`.
-/

namespace TwinPrimes

namespace Gauss

/-- `#{0 ≤ k < n : P k}`. -/
def cnt (n : Nat) (P : Nat → Bool) : Nat := ((List.range n).filter P).length

/-- `∑_{v < N} F v`. -/
def sumTo (N : Nat) (F : Nat → Nat) : Nat := ((List.range N).map F).sum

theorem cnt_zero (P : Nat → Bool) : cnt 0 P = 0 := rfl

theorem cnt_succ (n : Nat) (P : Nat → Bool) :
    cnt (n + 1) P = cnt n P + if P n then 1 else 0 := by
  unfold cnt
  rw [List.range_succ, List.filter_append, List.length_append]
  cases h : P n <;> simp [h]

theorem sumTo_zero (F : Nat → Nat) : sumTo 0 F = 0 := rfl

theorem sumTo_succ (N : Nat) (F : Nat → Nat) : sumTo (N + 1) F = sumTo N F + F N := by
  unfold sumTo
  rw [List.range_succ, List.map_append, List.sum_append]
  simp

theorem cnt_congr (n : Nat) (P Q : Nat → Bool) (h : ∀ k, k < n → P k = Q k) :
    cnt n P = cnt n Q := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [cnt_succ, cnt_succ, ih (fun k hk => h k (by omega)), h n (by omega)]

theorem sumTo_congr (N : Nat) (F G : Nat → Nat) (h : ∀ v, v < N → F v = G v) :
    sumTo N F = sumTo N G := by
  induction N with
  | zero => rfl
  | succ N ih =>
    rw [sumTo_succ, sumTo_succ, ih (fun v hv => h v (by omega)), h N (by omega)]

theorem cnt_eq_zero (n : Nat) (P : Nat → Bool) (h : ∀ k, k < n → P k = false) :
    cnt n P = 0 := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [cnt_succ, ih (fun k hk => h k (by omega)), h n (by omega)]
    rfl

theorem sumTo_add (N : Nat) (F G : Nat → Nat) :
    sumTo N (fun v => F v + G v) = sumTo N F + sumTo N G := by
  induction N with
  | zero => rfl
  | succ N ih => rw [sumTo_succ, sumTo_succ, sumTo_succ, ih]; omega

theorem sumTo_indicator (N c : Nat) (hc : c < N) :
    sumTo N (fun v => if (c == v) = true then 1 else 0) = 1 := by
  induction N with
  | zero => omega
  | succ N ih =>
    rw [sumTo_succ]
    by_cases h : c = N
    · subst h
      have h0 : sumTo c (fun v => if (c == v) = true then 1 else 0) = 0 := by
        have := sumTo_congr c (fun v => if (c == v) = true then 1 else 0) (fun _ => 0)
          (fun v hv => by
            have : (c == v) = false := by simp; omega
            simp [this])
        rw [this]
        clear this hc ih
        induction c with
        | zero => rfl
        | succ c ih => rw [sumTo_succ, ih]
      rw [h0]; simp
    · have hne : (c == N) = false := by simp; omega
      rw [ih (by omega)]
      simp [hne]

/-- Partition of `{0, …, n-1}` by the value of `f` (all values `< N`). -/
theorem partition (n N : Nat) (f : Nat → Nat) (hf : ∀ k, k < n → f k < N) :
    sumTo N (fun v => cnt n (fun k => f k == v)) = n := by
  induction n with
  | zero =>
    clear hf
    induction N with
    | zero => rfl
    | succ N ih => rw [sumTo_succ, ih]; rfl
  | succ n ih =>
    have e : (fun v => cnt (n + 1) (fun k => f k == v)) =
        (fun v => cnt n (fun k => f k == v) + if (f n == v) = true then 1 else 0) := by
      funext v; rw [cnt_succ]
    rw [e, sumTo_add, ih (fun k hk => hf k (by omega)), sumTo_indicator N (f n) (hf n (by omega))]

/-- Counting in blocks of length `g`: if `P k` forces `g ∣ k + 1`, only the last element
`j g + (g - 1)` of each block can satisfy `P`. -/
theorem cnt_mul (r g : Nat) (hg : 0 < g) (P : Nat → Bool)
    (hP : ∀ k, P k = true → g ∣ k + 1) :
    cnt (r * g) P = cnt r (fun j => P (j * g + (g - 1))) := by
  induction r with
  | zero => simp [cnt]
  | succ r ih =>
    rw [cnt_succ, ← ih, Nat.succ_mul]
    -- block `[r g, r g + g)`
    obtain ⟨h, rfl⟩ : ∃ h, g = h + 1 := ⟨g - 1, by omega⟩
    have hblock : ∀ i, cnt (r * (h + 1) + i) P =
        cnt (r * (h + 1)) P + cnt i (fun t => P (r * (h + 1) + t)) := by
      intro i
      induction i with
      | zero => rfl
      | succ i ihi =>
        rw [← Nat.add_assoc, cnt_succ, ihi, cnt_succ]; omega
    rw [hblock (h + 1), cnt_succ]
    have hz : cnt h (fun t => P (r * (h + 1) + t)) = 0 := by
      apply cnt_eq_zero
      intro t ht
      cases hpt : P (r * (h + 1) + t) with
      | false => rfl
      | true =>
        exfalso
        have hd := hP _ hpt
        rw [Nat.add_assoc, Nat.dvd_add_right (Nat.dvd_mul_left _ _)] at hd
        have := Nat.le_of_dvd (by omega) hd
        omega
    rw [hz]
    simp

/-- The fibre over a divisor `r` of `n ≥ 1`: `#{0 ≤ k < n : n / gcd(k+1, n) = r} = φ(r)`. -/
theorem fibre (n r : Nat) (hn : 0 < n) (hr : 0 < r) (hrn : n % r = 0) :
    cnt n (fun k => n / Nat.gcd (k + 1) n == r) = totient r := by
  obtain ⟨g, rfl⟩ := Nat.dvd_of_mod_eq_zero hrn
  have hg : 0 < g := by
    cases g with
    | zero => simp at hn
    | succ g => omega
  rw [cnt_mul r g hg]
  · show _ = cnt r _
    apply cnt_congr
    intro j _
    have e1 : j * g + (g - 1) + 1 = (j + 1) * g := by rw [Nat.succ_mul]; omega
    rw [e1, Nat.gcd_mul_right, Nat.mul_div_mul_right _ _ hg]
    have hc : 0 < Nat.gcd (j + 1) r := Nat.gcd_pos_of_pos_right _ hr
    have hcd : Nat.gcd (j + 1) r ∣ r := Nat.gcd_dvd_right _ _
    generalize Nat.gcd (j + 1) r = c at hc hcd
    apply Bool.eq_iff_iff.mpr
    simp only [beq_iff_eq]
    constructor
    · intro h
      have h2 := Nat.div_mul_cancel hcd
      rw [h] at h2
      have : r * c = r * 1 := by rw [h2, Nat.mul_one]
      exact Nat.eq_of_mul_eq_mul_left hr this
    · intro h; subst h; exact Nat.div_one r
  · intro k hk
    simp only [beq_iff_eq] at hk
    have hd : Nat.gcd (k + 1) (r * g) ∣ r * g := Nat.gcd_dvd_right _ _
    have h2 := Nat.div_mul_cancel hd
    rw [hk] at h2
    have : Nat.gcd (k + 1) (r * g) = g :=
      Nat.eq_of_mul_eq_mul_left hr h2
    rw [← this]
    exact Nat.gcd_dvd_left _ _

theorem sum_filter_map (l : List Nat) (p : Nat → Bool) (f : Nat → Nat) :
    ((l.filter p).map f).sum = (l.map fun x => if p x then f x else 0).sum := by
  induction l with
  | nil => rfl
  | cons a l ih =>
    cases h : p a <;> simp [h, ih]

end Gauss

open Gauss in
/-- **Gauss's identity** `∑_{r ∣ n} φ(r) = n`, for every `n ≥ 1`. -/
theorem gauss_totient (n : Nat) (hn : 1 ≤ n) : divisorTotientSum n = n := by
  have hpart := partition n (n + 1) (fun k => n / Nat.gcd (k + 1) n)
    (fun k _ => Nat.lt_succ_of_le (Nat.div_le_self _ _))
  unfold divisorTotientSum
  rw [sum_filter_map]
  show sumTo (n + 1) _ = n
  conv => rhs; rw [← hpart]
  apply sumTo_congr
  intro v _
  by_cases hv : v = 0
  · subst hv
    simp only [bne_self_eq_false, Bool.false_and, Bool.false_eq_true, ite_false]
    symm
    apply cnt_eq_zero
    intro k _
    have hpos : 0 < n / Nat.gcd (k + 1) n :=
      Nat.div_pos (Nat.gcd_le_right _ (by omega)) (Nat.gcd_pos_of_pos_right _ (by omega))
    simp only [beq_eq_false_iff_ne, ne_eq]
    omega
  · by_cases hm : n % v = 0
    · have : (v != 0 && n % v == 0) = true := by simp [hv, hm]
      simp only [this, ite_true]
      rw [fibre n v (by omega) (by omega) hm]
    · have : (v != 0 && n % v == 0) = false := by simp [hm]
      rw [this]; simp only [Bool.false_eq_true, ite_false]
      symm
      apply cnt_eq_zero
      intro k _
      cases h : (n / Nat.gcd (k + 1) n == v) with
      | false => rfl
      | true =>
        exfalso
        simp only [beq_iff_eq] at h
        have := Nat.div_dvd_of_dvd (Nat.gcd_dvd_right (k + 1) n)
        rw [h] at this
        exact hm (Nat.mod_eq_zero_of_dvd this)

/-! ## Selberg's diagonalisation for every `D` -/

namespace Gauss

theorem dvd_foldl_lcm (l : List Nat) :
    ∀ a, a ∣ l.foldl Nat.lcm a ∧ ∀ x ∈ l, x ∣ l.foldl Nat.lcm a := by
  induction l with
  | nil => intro a; simp
  | cons y l ih =>
    intro a
    rw [List.foldl_cons]
    obtain ⟨h1, h2⟩ := ih (Nat.lcm a y)
    refine ⟨Nat.dvd_trans (Nat.dvd_lcm_left a y) h1, ?_⟩
    intro x hx
    rcases List.mem_cons.mp hx with rfl | hx
    · exact Nat.dvd_trans (Nat.dvd_lcm_right a x) h1
    · exact h2 x hx

theorem mem_range_succ_map {D d : Nat} : d ∈ (List.range D).map (· + 1) ↔ 1 ≤ d ∧ d ≤ D := by
  simp only [List.mem_map, List.mem_range]
  constructor
  · rintro ⟨a, ha, rfl⟩; omega
  · intro h; exact ⟨d - 1, by omega, by omega⟩

theorem dvd_lcmUpto {D d : Nat} (h1 : 1 ≤ d) (h2 : d ≤ D) : d ∣ lcmUpto D :=
  (dvd_foldl_lcm _ 1).2 d (mem_range_succ_map.mpr ⟨h1, h2⟩)

theorem sumTo_succ_eq (D : Nat) (F : Nat → Nat) :
    sumTo (D + 1) F = F 0 + (((List.range D).map (· + 1)).map F).sum := by
  unfold sumTo
  rw [List.range_succ_eq_map, List.map_cons, List.sum_cons, List.map_map]

theorem sumTo_extend (N M : Nat) (F : Nat → Nat) (hNM : N ≤ M)
    (h : ∀ v, N ≤ v → v < M → F v = 0) : sumTo M F = sumTo N F := by
  induction M with
  | zero => have : N = 0 := by omega
            subst this; rfl
  | succ M ih =>
    by_cases hN : N = M + 1
    · subst hN; rfl
    · rw [sumTo_succ, ih (by omega) (fun v h1 h2 => h v h1 (by omega)), h M (by omega) (by omega)]
      rfl

/-- `gcd(d, e) = ∑_{r ≤ D, r ∣ d, r ∣ e} φ(r)` for `1 ≤ d, e ≤ D` (from Gauss's identity). -/
theorem gcd_eq_sum_totient (D d e : Nat) (hd1 : 1 ≤ d) (hdD : d ≤ D) :
    Nat.gcd d e = (((List.range D).map (· + 1)).map fun r =>
      if (d % r == 0 && e % r == 0) then totient r else 0).sum := by
  have hg1 : 0 < Nat.gcd d e := Nat.gcd_pos_of_pos_left _ (by omega)
  have hgD : Nat.gcd d e ≤ D := Nat.le_trans (Nat.gcd_le_left _ (by omega)) hdD
  generalize hG : Nat.gcd d e = g at hg1 hgD
  have hgauss := gauss_totient g hg1
  unfold divisorTotientSum at hgauss
  rw [sum_filter_map] at hgauss
  change sumTo (g + 1) (fun r => if (r != 0 && g % r == 0) = true then totient r else 0) = g
    at hgauss
  rw [← sumTo_extend (g + 1) (D + 1) _ (by omega)] at hgauss
  · rw [sumTo_succ_eq] at hgauss
    simp only [bne_self_eq_false, Bool.false_and, Bool.false_eq_true, ite_false,
      Nat.zero_add] at hgauss
    rw [← hgauss]
    congr 1
    apply List.map_congr_left
    intro r hr
    have hr1 := (mem_range_succ_map.mp hr).1
    have key : (d % r == 0 && e % r == 0) = (r != 0 && g % r == 0) := by
      have hr0 : (r != 0) = true := by simp; omega
      rw [hr0, Bool.true_and]
      apply Bool.eq_iff_iff.mpr
      simp only [Bool.and_eq_true, beq_iff_eq, ← Nat.dvd_iff_mod_eq_zero, ← hG]
      exact Nat.dvd_gcd_iff.symm
    rw [key]
  · intro v hv _
    have : (g % v == 0) = false := by
      simp only [beq_eq_false_iff_ne, ne_eq]
      intro hm
      have := Nat.le_of_dvd hg1 (Nat.dvd_of_mod_eq_zero hm)
      omega
    simp [this]

theorem isum_natCast {α} (f : α → Nat) : ∀ l : List α,
    (((l.map f).sum : Nat) : Int) = (l.map fun x => (f x : Int)).sum
  | [] => rfl
  | x :: l => by simp only [List.map_cons, List.sum_cons, Int.natCast_add, isum_natCast f l]

theorem isum_filter {α} (l : List α) (p : α → Bool) (f : α → Int) :
    ((l.filter p).map f).sum = (l.map fun x => if p x then f x else 0).sum := by
  induction l with
  | nil => rfl
  | cons a l ih =>
    cases h : p a <;> simp [h, ih]

end Gauss

open Gauss in
/-- **Selberg's diagonalisation, every `D`.** For every `D` and every `λ : ℕ → ℤ`,
`∑_{d,e ≤ D} λ_d λ_e (L² gcd(d,e)/(de)) = ∑_{r ≤ D} φ(r) (∑_{d ≤ D, r ∣ d} λ_d (L/d))²`
with `L = lcm(1..D)`; dividing by `L²` this is
`∑ λ_d λ_e / [d,e] = ∑_{r ≤ D} φ(r) y_r²`, `y_r = ∑_{r ∣ d ≤ D} λ_d / d`. -/
theorem selberg_diag (D : Nat) (lam : Nat → Int) : selbergLHS D lam = selbergRHS D lam := by
  unfold selbergLHS selbergRHS
  generalize hI : (List.range D).map (· + 1) = I
  generalize hL : lcmUpto D = L
  have hmem : ∀ d, d ∈ I → 1 ≤ d ∧ d ≤ D := fun d hd => mem_range_succ_map.mp (hI ▸ hd)
  let x : Nat → Nat → Int := fun r d => if d % r == 0 then lam d * ((L / d : Nat) : Int) else 0
  -- pointwise expansion of each LHS term
  have hA : ∀ d ∈ I, ∀ e ∈ I,
      lam d * lam e * ((L * L * Nat.gcd d e / (d * e) : Nat) : Int) =
        (I.map fun r => x r d * x r e * (totient r : Int)).sum := by
    intro d hd e he
    obtain ⟨hd1, hdD⟩ := hmem d hd
    obtain ⟨he1, heD⟩ := hmem e he
    obtain ⟨a, ha⟩ := (hL ▸ dvd_lcmUpto hd1 hdD : d ∣ L)
    obtain ⟨b, hb⟩ := (hL ▸ dvd_lcmUpto he1 heD : e ∣ L)
    have hLd : L / d = a := by rw [ha]; exact Nat.mul_div_cancel_left _ (by omega)
    have hLe : L / e = b := by rw [hb]; exact Nat.mul_div_cancel_left _ (by omega)
    have hdiv : L * L * Nat.gcd d e / (d * e) = a * b * Nat.gcd d e := by
      have : L * L * Nat.gcd d e = (d * e) * (a * b * Nat.gcd d e) := by
        calc L * L * Nat.gcd d e = (d * a) * (e * b) * Nat.gcd d e := by rw [← ha, ← hb]
          _ = (d * e) * (a * b * Nat.gcd d e) := by ac_rfl
      rw [this]; exact Nat.mul_div_cancel_left _ (Nat.mul_pos (by omega) (by omega))
    rw [hdiv, gcd_eq_sum_totient D d e hd1 hdD, hI, Int.natCast_mul, Int.natCast_mul,
      isum_natCast]
    rw [show ∀ s : Int, lam d * lam e * ((a : Int) * (b : Int) * s) =
      (lam d * lam e * (a : Int) * (b : Int)) * s from fun s => by grind, ← isum_mul_left]
    apply isum_congr
    intro r _
    simp only [x, hLd, hLe]
    cases h1 : (d % r == 0) <;> cases h2 : (e % r == 0) <;> simp <;> grind
  calc (I.map fun d => (I.map fun e =>
          lam d * lam e * ((L * L * Nat.gcd d e / (d * e) : Nat) : Int)).sum).sum
      = (I.map fun d => (I.map fun e =>
          (I.map fun r => x r d * x r e * (totient r : Int)).sum).sum).sum := by
        apply isum_congr; intro d hd; apply isum_congr; intro e he; exact hA d hd e he
    _ = (I.map fun d => (I.map fun r =>
          (I.map fun e => x r d * x r e * (totient r : Int)).sum).sum).sum := by
        apply isum_congr; intro d _
        exact isum_comm (fun e r => x r d * x r e * (totient r : Int)) I I
    _ = (I.map fun r => (I.map fun d =>
          (I.map fun e => x r d * x r e * (totient r : Int)).sum).sum).sum :=
        isum_comm (fun d r => (I.map fun e => x r d * x r e * (totient r : Int)).sum) I I
    _ = (I.map fun r => (totient r : Int) *
          ((I.filter (fun d => d % r == 0)).map fun d =>
            lam d * ((L / d : Nat) : Int)).sum ^ 2).sum := by
        apply isum_congr; intro r _
        rw [isum_filter, Int.pow_succ, Int.pow_succ, Int.pow_zero, Int.one_mul]
        change _ = (totient r : Int) * ((I.map (x r)).sum * (I.map (x r)).sum)
        rw [isum_sq, Int.mul_comm, ← isum_mul_right]
        apply isum_congr; intro d _
        rw [← isum_mul_right]
end TwinPrimes
