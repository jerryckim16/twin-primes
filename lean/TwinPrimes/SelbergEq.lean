import TwinPrimes.SelbergOpt

/-!
# The equality case of Selberg's lower bound, every `D`

`selberg_lower` says `W (λ₁ L)² ≤ selbergLHS D λ · G` (`L = lcm(1..D)`, `W = lcm(φ(1..D))`,
`G = ∑_{r ≤ D} μ(r)² (W / φ(r))`). Here we exhibit, for every `D ≥ 1`, explicit integer
weights attaining equality.

Construction. Put `y_r = μ(r) · (W / φ(r))` (Cauchy–Schwarz is tight exactly when
`φ(r) y_r ∝ μ(r)`), and define `t_d` for `1 ≤ d ≤ D` by downward recursion
`t_d = y_d - ∑_{d < e ≤ D, d ∣ e} t_e`, so that `∑_{d ≤ e ≤ D, d ∣ e} t_e = y_d` (this is
Möbius inversion over the divisibility order on `[1, D]`, `t_d = ∑ μ(e/d) y_e`, but the
recursion makes the inversion identity hold by construction). Set `λ_d = d · t_d`. Then
`selbergY D λ r = L · y_r`, and both sides of `selberg_lower` equal `W L² G²`; moreover
`λ₁ = G > 0`.

* `selbergEqY`, `selbergEqT`, `selbergEqLam`: the construction (`selbergEqT` is fuel-indexed).
* `selbergEqT_sum`: `∑_{d ≤ D, r ∣ d} t_d = y_r` for `1 ≤ r ≤ D`.
* `selbergEq_Y`: `selbergY D λ r = L · y_r` for `1 ≤ r ≤ D`.
* `selbergEq_lam_one`: `λ₁ = G`; `selbergG_pos`: `0 < G`.
* `selbergEq_LHS`: `selbergLHS D λ = W L² G`, i.e. `Q(λ) = W G = λ₁² / (G / W)`.
* `selberg_lower_eq`: `W (λ₁ L)² = selbergLHS D λ · G` for these weights.
* `selberg_lower_attained`: `∃ λ, λ₁ ≠ 0 ∧ W (λ₁ L)² = selbergLHS D λ · G`.
* `selbergEq_D6`: for `D = 6` the weights are `(13, -12, -12, 0, -5, 12) = selbergOpt6`.
-/

namespace TwinPrimes

/-- `y_r = μ(r) · (W / φ(r))`, `W = lcm(φ(1..D))`. -/
def selbergEqY (D r : Nat) : Int := mu r * ((phiLcm D / totient r : Nat) : Int)

/-- Fuel-indexed downward recursion `t_d = y_d - ∑_{d < e ≤ D, d ∣ e} t_e`. -/
def selbergEqT (D : Nat) : Nat → Nat → Int
  | 0, _ => 0
  | k + 1, d => selbergEqY D d -
      ((((List.range D).map (· + 1)).filter (fun e => d < e && e % d == 0)).map
        (selbergEqT D k)).sum

/-- The weights `λ_d = d · t_d` (with enough fuel `D + 1 - d`). -/
def selbergEqLam (D d : Nat) : Int := (d : Int) * selbergEqT D (D + 1 - d) d

namespace SelbergEq

open Gauss SelbergOpt

theorem T_stable (D : Nat) : ∀ k j e, e ≤ D → D + 1 ≤ e + k → D + 1 ≤ e + j →
    selbergEqT D k e = selbergEqT D j e := by
  intro k
  induction k with
  | zero => intro j e he h; omega
  | succ k ih =>
    intro j e he hk hj
    cases j with
    | zero => omega
    | succ j =>
      simp only [selbergEqT]
      congr 2
      apply List.map_congr_left
      intro x hx
      have h1 := List.mem_filter.mp hx
      have h2 := mem_range_succ_map.mp h1.1
      have h3 : e < x := by simp at h1; omega
      exact ih j x h2.2 (by omega) (by omega)

theorem isum_single (f : Nat → Int) : ∀ D r, 1 ≤ r → r ≤ D →
    (((List.range D).map (· + 1)).map fun d => if d = r then f d else 0).sum = f r
  | 0, _, h1, h2 => by omega
  | D + 1, r, h1, h2 => by
    rw [List.range_succ, List.map_append, List.map_append, List.sum_append]
    by_cases hr : r = D + 1
    · subst hr
      rw [isum_congr (g := fun _ => (0 : Int)), isum_zero]
      · simp
      · intro x hx
        have := mem_range_succ_map.mp hx
        simp; omega
    · rw [isum_single f D r h1 (by omega)]
      simp; omega

/-- **Inversion identity by construction:** `∑_{d ≤ D, r ∣ d} t_d = y_r` for `1 ≤ r ≤ D`. -/
theorem selbergEqT_sum (D r : Nat) (hr1 : 1 ≤ r) (hrD : r ≤ D) :
    ((((List.range D).map (· + 1)).filter (fun d => d % r == 0)).map
      fun d => selbergEqT D (D + 1 - d) d).sum = selbergEqY D r := by
  generalize hI : (List.range D).map (· + 1) = I
  let T' : Nat → Int := fun d => selbergEqT D (D + 1 - d) d
  have split : ((I.filter (fun d => d % r == 0)).map T').sum =
      (I.map fun d => if d = r then T' d else 0).sum +
      ((I.filter (fun d => r < d && d % r == 0)).map T').sum := by
    rw [isum_filter, isum_filter, ← isum_add]
    apply isum_congr; intro d hd
    have hd' := mem_range_succ_map.mp (hI ▸ hd)
    by_cases hm : d % r = 0
    · have hle : r ≤ d := Nat.le_of_dvd (by omega) (Nat.dvd_of_mod_eq_zero hm)
      by_cases hdr : d = r
      · subst hdr; simp
      · have : r < d := by omega
        simp [hm, hdr, this]
    · have hdr : d ≠ r := by intro h; subst h; simp at hm
      simp [hm, hdr]
  show ((I.filter (fun d => d % r == 0)).map T').sum = _
  rw [split, ← hI, isum_single T' D r hr1 hrD, hI]
  have hT : T' r = selbergEqY D r -
      ((I.filter (fun d => r < d && d % r == 0)).map T').sum := by
    show selbergEqT D (D + 1 - r) r = _
    rw [show D + 1 - r = (D - r) + 1 by omega, selbergEqT, hI]
    congr 2
    apply List.map_congr_left
    intro x hx
    have h1 := List.mem_filter.mp hx
    have h2 := mem_range_succ_map.mp (hI ▸ h1.1)
    have h3 : r < x := by simp at h1; omega
    exact T_stable D _ _ x h2.2 (by omega) (by omega)
  rw [hT]; omega

theorem lcmUpto_pos (D : Nat) : 0 < lcmUpto D :=
  foldl_lcm_pos _ _ (by decide) (fun x hx => (mem_range_succ_map.mp hx).1)

end SelbergEq

open Gauss SelbergOpt SelbergEq in
/-- **`selbergY D λ r = L · y_r`** for the constructed weights and `1 ≤ r ≤ D`. -/
theorem selbergEq_Y (D r : Nat) (hr1 : 1 ≤ r) (hrD : r ≤ D) :
    selbergY D (selbergEqLam D) r = (lcmUpto D : Int) * selbergEqY D r := by
  unfold selbergY
  rw [← selbergEqT_sum D r hr1 hrD, ← isum_mul_left]
  apply isum_congr
  intro d hd
  have hd' := mem_range_succ_map.mp (List.mem_filter.mp hd).1
  have hdvd := dvd_lcmUpto hd'.1 hd'.2
  have hc : ((lcmUpto D / d : Nat) : Int) * (d : Int) = (lcmUpto D : Int) := by
    rw [← Int.natCast_mul, Nat.div_mul_cancel hdvd]
  unfold selbergEqLam
  rw [← hc]
  grind

open Gauss SelbergOpt SelbergEq in
/-- `0 < G` for `D ≥ 1` (the `r = 1` term is `W > 0`, all terms are `≥ 0`). -/
theorem selbergG_pos (D : Nat) (hD : 1 ≤ D) : 0 < selbergG D := by
  obtain ⟨D', rfl⟩ : ∃ D', D = D' + 1 := ⟨D - 1, by omega⟩
  unfold selbergG
  rw [List.range_succ_eq_map, List.map_cons, List.map_cons, List.sum_cons]
  have h1 : totient (0 + 1) = 1 := by decide
  have hm : mu (0 + 1) = 1 := by decide
  rw [h1, hm, Nat.div_one]
  have hW := phiLcm_pos (D' + 1)
  have hrest := isum_nonneg (fun r => ((phiLcm (D' + 1) / totient r : Nat) : Int) * mu r ^ 2)
    (((List.range D').map Nat.succ).map (· + 1))
    (fun x _ => Int.mul_nonneg (Int.natCast_nonneg _) (Int.sq_nonneg _))
  simp only [List.map_map] at hrest ⊢
  have : ((phiLcm (D' + 1) : Nat) : Int) * 1 ^ 2 > 0 := by simp; omega
  omega

open Gauss SelbergOpt SelbergEq in
/-- **`λ₁ = G`** for the constructed weights (`D ≥ 1`). -/
theorem selbergEq_lam_one (D : Nat) (hD : 1 ≤ D) : selbergEqLam D 1 = selbergG D := by
  have h := mu_y_sum D hD (selbergEqLam D)
  rw [isum_congr (g := fun r => (lcmUpto D : Int) *
      (((phiLcm D / totient r : Nat) : Int) * mu r ^ 2))] at h
  · rw [isum_mul_left] at h
    have hL : (0 : Int) < lcmUpto D := by have := lcmUpto_pos D; omega
    unfold selbergG
    have h' : (lcmUpto D : Int) * selbergEqLam D 1 = (lcmUpto D : Int) * (((List.range D).map
        (· + 1)).map fun r => ((phiLcm D / totient r : Nat) : Int) * mu r ^ 2).sum := by
      rw [Int.mul_comm]; exact h.symm
    exact Int.eq_of_mul_eq_mul_left (by omega) h'
  · intro r hr
    have hr' := mem_range_succ_map.mp hr
    rw [selbergEq_Y D r hr'.1 hr'.2]
    unfold selbergEqY
    grind

open Gauss SelbergOpt SelbergEq in
/-- **`selbergLHS D λ = W L² G`** for the constructed weights, i.e. `Q(λ) = W G`. -/
theorem selbergEq_LHS (D : Nat) :
    selbergLHS D (selbergEqLam D) =
      (phiLcm D : Int) * (lcmUpto D : Int) ^ 2 * selbergG D := by
  rw [selberg_diag]
  unfold selbergG
  rw [← isum_mul_left]
  unfold selbergRHS
  apply isum_congr
  intro r hr
  have hr' := mem_range_succ_map.mp hr
  have hY := selbergEq_Y D r hr'.1 hr'.2
  unfold selbergY at hY
  show _ = _
  rw [hY]
  have hc : (totient r : Int) * ((phiLcm D / totient r : Nat) : Int) = (phiLcm D : Int) := by
    rw [← Int.natCast_mul, Nat.mul_div_cancel' (totient_dvd_phiLcm D r hr'.1 hr'.2)]
  unfold selbergEqY
  rw [← hc]
  grind

/-- **Equality in `selberg_lower`, every `D ≥ 1`:** for the weights `selbergEqLam D`,
`W (λ₁ L)² = selbergLHS D λ · G` (both sides are `W L² G²`). -/
theorem selberg_lower_eq (D : Nat) (hD : 1 ≤ D) :
    (phiLcm D : Int) * (selbergEqLam D 1 * (lcmUpto D : Int)) ^ 2 =
      selbergLHS D (selbergEqLam D) * selbergG D := by
  rw [selbergEq_LHS, selbergEq_lam_one D hD]
  grind

/-- **Selberg's bound is sharp, every `D ≥ 1`:** there is an integer weight vector with
`λ₁ ≠ 0` attaining equality in `selberg_lower`. -/
theorem selberg_lower_attained (D : Nat) (hD : 1 ≤ D) :
    ∃ lam : Nat → Int, lam 1 ≠ 0 ∧
      (phiLcm D : Int) * (lam 1 * (lcmUpto D : Int)) ^ 2 = selbergLHS D lam * selbergG D :=
  ⟨selbergEqLam D, by rw [selbergEq_lam_one D hD]; have := selbergG_pos D hD; omega,
    selberg_lower_eq D hD⟩

/-- Sanity check, `D = 6`: the constructed weights are `(13, -12, -12, 0, -5, 12)`, i.e.
`selbergOpt6`, with `λ₁ = G = 13`. -/
theorem selbergEq_D6 :
    (List.range 6).map (fun d => selbergEqLam 6 (d + 1)) = [13, -12, -12, 0, -5, 12] ∧
    (∀ d, d < 6 → selbergEqLam 6 (d + 1) = selbergOpt6 (d + 1)) ∧
    selbergEqLam 6 1 = selbergG 6 := by
  decide

end TwinPrimes
