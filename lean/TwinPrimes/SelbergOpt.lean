import TwinPrimes.Gauss

/-!
# Selberg's lower bound `Q(λ) ≥ λ₁² / G(D)` for every `D`

With `L = lcm(1..D)` and `y_r = ∑_{d ≤ D, r ∣ d} λ_d (L / d)`, `selberg_diag` gives
`selbergLHS D λ = ∑_{r ≤ D} φ(r) y_r²` (this is `L² Q(λ)`, `Q(λ) = ∑ λ_d λ_e / [d,e]`).

* `mu`: the Möbius function, defined *without factorisation* by the recursion
  `μ(1) = 1`, `μ(n) = -∑_{r ∣ n, r < n} μ(r)` (`n ≥ 2`), `μ(0) = 0`;
  `mu_divisor_sum`: `∑_{r ∣ n} μ(r) = [n = 1]` for all `n ≥ 1`;
  `mu_upto_12`: the first twelve values, by `decide`.
* `weighted_cauchy_schwarz`: for integer weights `w_x ≥ 0`, `c_x` with `w_x c_x = W > 0`,
  `W (∑ a_x b_x)² ≤ (∑ w_x b_x²)(∑ c_x a_x²)` (i.e. `(∑ a b)² ≤ (∑ w b²)(∑ a²/w)`).
* `mu_y_sum`: `∑_{r ≤ D} μ(r) y_r = λ₁ L`.
* `selberg_lower`: `W (λ₁ L)² ≤ selbergLHS D λ · G` where `W = lcm(φ(1), …, φ(D))` and
  `G = ∑_{r ≤ D} μ(r)² (W / φ(r))`; dividing by `W L²`:
  `Q(λ) ≥ λ₁² / G(D)` with `G(D) = G / W = ∑_{r ≤ D} μ²(r) / φ(r)`.
* `selberg_lower_D6_consts`: for `D = 6`, `W = 4`, `G = 13` (so `G(6) = 13/4`, as in
  `selberg_opt_D6`).
-/

namespace TwinPrimes

/-- Fuel-indexed Möbius recursion: `muF (k+1) n = -∑_{1 ≤ r < n, r ∣ n} muF k r` for `n ≥ 2`. -/
def muF : Nat → Nat → Int
  | 0, _ => 0
  | k + 1, n =>
    if n = 0 then 0 else if n = 1 then 1 else
      -((((List.range n).filter fun r => r != 0 && n % r == 0).map (muF k)).sum)

/-- The Möbius function, via `μ(1) = 1`, `μ(n) = -∑_{r ∣ n, r < n} μ(r)`; `μ(0) = 0`. -/
def mu (n : Nat) : Int := muF (n + 1) n

namespace SelbergOpt

theorem muF_stable : ∀ k j n, n < k → n < j → muF k n = muF j n := by
  intro k
  induction k with
  | zero => intro j n h; omega
  | succ k ih =>
    intro j n hk hj
    cases j with
    | zero => omega
    | succ j =>
      simp only [muF]
      split
      · rfl
      · split
        · rfl
        · congr 2
          apply List.map_congr_left
          intro r hr
          have : r < n := List.mem_range.mp (List.mem_filter.mp hr).1
          exact ih j r (by omega) (by omega)

theorem mu_rec (n : Nat) (hn : 2 ≤ n) :
    mu n = -((((List.range n).filter fun r => r != 0 && n % r == 0).map mu).sum) := by
  unfold mu
  simp only [muF]
  have h0 : n ≠ 0 := by omega
  have h1 : n ≠ 1 := by omega
  simp only [h0, h1, ↓reduceIte]
  congr 2
  apply List.map_congr_left
  intro r hr
  have : r < n := List.mem_range.mp (List.mem_filter.mp hr).1
  exact muF_stable n (r + 1) r (by omega) (by omega)

end SelbergOpt

open SelbergOpt in
/-- **Möbius inversion identity** `∑_{r ∣ n} μ(r) = [n = 1]`, for every `n ≥ 1`. -/
theorem mu_divisor_sum (n : Nat) (hn : 1 ≤ n) :
    (((List.range (n + 1)).filter (fun r => r != 0 && n % r == 0)).map mu).sum =
      if n = 1 then 1 else 0 := by
  rw [List.range_succ, List.filter_append]
  have hself : (([n] : List Nat).filter fun r => r != 0 && n % r == 0) = [n] := by
    simp; omega
  rw [hself, List.map_append, List.sum_append]
  by_cases h1 : n = 1
  · subst h1; decide
  · simp only [h1, ↓reduceIte]
    simp only [List.map_cons, List.map_nil, List.sum_cons, List.sum_nil]
    rw [mu_rec n (by omega)]
    omega

/-- Sanity check: `μ(1), …, μ(12) = 1, -1, -1, 0, -1, 1, -1, 0, 0, 1, -1, 0`. -/
theorem mu_upto_12 :
    (List.range 12).map (fun n => mu (n + 1)) = [1, -1, -1, 0, -1, 1, -1, 0, 0, 1, -1, 0] := by
  decide

namespace SelbergOpt

theorem isum_nonneg {α} (f : α → Int) : ∀ l : List α, (∀ x ∈ l, 0 ≤ f x) → 0 ≤ (l.map f).sum
  | [], _ => by simp
  | x :: l, h => by
    simp only [List.map_cons, List.sum_cons]
    have h1 := h x (List.mem_cons_self ..)
    have h2 := isum_nonneg f l (fun y hy => h y (List.mem_cons_of_mem _ hy))
    omega

end SelbergOpt

open SelbergOpt in
/-- **Weighted Cauchy–Schwarz over a list.** If `w x ≥ 0` and `w x · c x = W > 0` for all `x`
(so `c x = W / w x`), then `W (∑ a b)² ≤ (∑ w b²)(∑ c a²)`, i.e.
`(∑ a_x b_x)² ≤ (∑ w_x b_x²)(∑ a_x² / w_x)`. -/
theorem weighted_cauchy_schwarz {α} (l : List α) (a b w c : α → Int) (W : Int) (hW : 0 < W)
    (hw : ∀ x ∈ l, 0 ≤ w x) (hwc : ∀ x ∈ l, w x * c x = W) :
    W * (l.map fun x => a x * b x).sum ^ 2 ≤
      (l.map fun x => w x * b x ^ 2).sum * (l.map fun x => c x * a x ^ 2).sum := by
  let T : α → α → Int := fun x y =>
    W * ((w x * b x ^ 2) * (c y * a y ^ 2)) - W * (W * ((a x * b x) * (a y * b y)))
  have hT : (l.map fun x => (l.map fun y => T x y).sum).sum =
      W * ((l.map fun x => w x * b x ^ 2).sum * (l.map fun x => c x * a x ^ 2).sum -
        W * (l.map fun x => a x * b x).sum ^ 2) := by
    have inner : ∀ x, (l.map fun y => T x y).sum =
        W * ((w x * b x ^ 2) * (l.map fun y => c y * a y ^ 2).sum) -
          W * (W * ((a x * b x) * (l.map fun y => a y * b y).sum)) := by
      intro x
      simp only [T]
      rw [isum_sub, isum_mul_left, isum_mul_left, isum_mul_left, isum_mul_left, isum_mul_left]
    rw [isum_congr (fun x _ => inner x), isum_sub, isum_mul_left, isum_mul_left, isum_mul_left,
      isum_mul_right, isum_mul_right]
    grind
  have hsym : 0 ≤ (l.map fun x => (l.map fun y => T x y + T y x).sum).sum := by
    apply isum_nonneg; intro x hx
    apply isum_nonneg; intro y hy
    have hx' := hwc x hx
    have hy' := hwc y hy
    have e : T x y + T y x =
        (w x * w y) * (c y * a y * b x - c x * a x * b y) ^ 2 := by
      simp only [T]
      grind
    rw [e]
    exact Int.mul_nonneg (Int.mul_nonneg (hw x hx) (hw y hy)) (Int.sq_nonneg _)
  have h2 : (l.map fun x => (l.map fun y => T x y + T y x).sum).sum =
      2 * (l.map fun x => (l.map fun y => T x y).sum).sum := by
    have hc := isum_comm (fun x y => T y x) l l
    rw [show (2 : Int) * _ = _ + _ from Int.two_mul _]
    conv => rhs; rhs; rw [← hc]
    rw [← isum_add]
    apply isum_congr; intro x _
    rw [isum_add]
  rw [h2, hT] at hsym
  have : 0 ≤ (l.map fun x => w x * b x ^ 2).sum * (l.map fun x => c x * a x ^ 2).sum -
      W * (l.map fun x => a x * b x).sum ^ 2 := by
    have h3 : 0 ≤ 2 * W * ((l.map fun x => w x * b x ^ 2).sum *
        (l.map fun x => c x * a x ^ 2).sum - W * (l.map fun x => a x * b x).sum ^ 2) := by
      rw [Int.mul_assoc]; exact hsym
    rw [Int.mul_comm] at h3
    exact Int.nonneg_of_mul_nonneg_left h3 (by omega)
  omega

/-! ## The Selberg lower bound -/

/-- `W = lcm(φ(1), …, φ(D))`. -/
def phiLcm (D : Nat) : Nat := (((List.range D).map (· + 1)).map totient).foldl Nat.lcm 1

/-- `G = ∑_{r ≤ D} μ(r)² · (W / φ(r))`, so that `G / W = ∑_{r ≤ D} μ²(r) / φ(r)`. -/
def selbergG (D : Nat) : Int :=
  (((List.range D).map (· + 1)).map fun r =>
    ((phiLcm D / totient r : Nat) : Int) * mu r ^ 2).sum

/-- `y_r = ∑_{d ≤ D, r ∣ d} λ_d (L / d)` (`L = lcm(1..D)`), the quantity squared in
`selbergRHS`. -/
def selbergY (D : Nat) (lam : Nat → Int) (r : Nat) : Int :=
  ((((List.range D).map (· + 1)).filter (fun d => d % r == 0)).map fun d =>
    lam d * ((lcmUpto D / d : Nat) : Int)).sum

namespace SelbergOpt

open Gauss

theorem isum_range_extend (N M : Nat) (f : Nat → Int) (hNM : N ≤ M)
    (h : ∀ v, N ≤ v → v < M → f v = 0) :
    ((List.range M).map f).sum = ((List.range N).map f).sum := by
  induction M with
  | zero => have : N = 0 := by omega
            subst this; rfl
  | succ M ih =>
    by_cases hN : N = M + 1
    · subst hN; rfl
    · rw [List.range_succ, List.map_append, List.sum_append,
        ih (by omega) (fun v h1 h2 => h v h1 (by omega))]
      simp [h M (by omega) (by omega)]

/-- `∑_{r ≤ D, r ∣ d} μ(r) = [d = 1]` for `1 ≤ d ≤ D`. -/
theorem mu_divisor_sum_upto (D d : Nat) (hd1 : 1 ≤ d) (hdD : d ≤ D) :
    (((List.range D).map (· + 1)).map fun r => if d % r == 0 then mu r else 0).sum =
      if d = 1 then 1 else 0 := by
  rw [← mu_divisor_sum d hd1, isum_filter]
  rw [← isum_range_extend (d + 1) (D + 1) _ (by omega)]
  · rw [List.range_succ_eq_map, List.map_cons, List.sum_cons, List.map_map]
    simp only [bne_self_eq_false, Bool.false_and, Bool.false_eq_true, ite_false, Int.zero_add,
      List.map_map]
    apply isum_congr
    intro x _
    simp
  · intro v hv _
    have : (d % v == 0) = false := by
      simp only [beq_eq_false_iff_ne, ne_eq]
      rw [Nat.mod_eq_of_lt (by omega)]; omega
    simp [this]

theorem isum_I_single (D : Nat) (hD : 1 ≤ D) (g : Nat → Int) :
    (((List.range D).map (· + 1)).map fun d => g d * (if d = 1 then 1 else 0)).sum = g 1 := by
  obtain ⟨D', rfl⟩ : ∃ D', D = D' + 1 := ⟨D - 1, by omega⟩
  rw [List.range_succ_eq_map, List.map_cons, List.map_cons, List.sum_cons, List.map_map,
    List.map_map]
  simp only [Nat.zero_add, ite_true, Int.mul_one]
  rw [isum_congr (g := fun _ => (0 : Int)), isum_zero, Int.add_zero]
  intro x _
  simp

theorem totient_pos (r : Nat) (hr : 1 ≤ r) : 0 < totient r := by
  unfold totient
  apply List.length_pos_of_mem (a := 0)
  simp; omega

theorem foldl_lcm_pos : ∀ (l : List Nat) (a : Nat), 0 < a → (∀ x ∈ l, 0 < x) →
    0 < l.foldl Nat.lcm a
  | [], _, ha, _ => ha
  | x :: l, a, ha, h => by
    rw [List.foldl_cons]
    exact foldl_lcm_pos l _ (Nat.lcm_pos ha (h x (List.mem_cons_self ..)))
      (fun y hy => h y (List.mem_cons_of_mem _ hy))

theorem phiLcm_pos (D : Nat) : 0 < phiLcm D := by
  apply foldl_lcm_pos _ _ (by decide)
  intro x hx
  obtain ⟨r, hr, rfl⟩ := List.mem_map.mp hx
  exact totient_pos r (mem_range_succ_map.mp hr).1

theorem totient_dvd_phiLcm (D r : Nat) (hr1 : 1 ≤ r) (hrD : r ≤ D) : totient r ∣ phiLcm D :=
  (dvd_foldl_lcm _ 1).2 _ (List.mem_map.mpr ⟨r, mem_range_succ_map.mpr ⟨hr1, hrD⟩, rfl⟩)

end SelbergOpt

open SelbergOpt Gauss in
/-- **`∑_{r ≤ D} μ(r) y_r = λ₁ L`** for `D ≥ 1`, `L = lcm(1..D)`. -/
theorem mu_y_sum (D : Nat) (hD : 1 ≤ D) (lam : Nat → Int) :
    (((List.range D).map (· + 1)).map fun r => mu r * selbergY D lam r).sum =
      lam 1 * (lcmUpto D : Int) := by
  unfold selbergY
  generalize hI : (List.range D).map (· + 1) = I
  let X : Nat → Int := fun d => lam d * ((lcmUpto D / d : Nat) : Int)
  calc (I.map fun r => mu r * ((I.filter (fun d => d % r == 0)).map X).sum).sum
      = (I.map fun r => (I.map fun d => mu r * (if d % r == 0 then X d else 0)).sum).sum := by
        apply isum_congr; intro r _; rw [isum_filter, isum_mul_left]
    _ = (I.map fun d => (I.map fun r => mu r * (if d % r == 0 then X d else 0)).sum).sum :=
        isum_comm _ I I
    _ = (I.map fun d => X d * (if d = 1 then 1 else 0)).sum := by
        apply isum_congr; intro d hd
        obtain ⟨hd1, hdD⟩ := mem_range_succ_map.mp (hI ▸ hd)
        rw [← mu_divisor_sum_upto D d hd1 hdD, hI, ← isum_mul_left]
        apply isum_congr; intro r _
        cases d % r == 0 <;> simp [Int.mul_comm]
    _ = X 1 := by rw [← hI]; exact isum_I_single D hD X
    _ = lam 1 * (lcmUpto D : Int) := by simp [X]

open SelbergOpt Gauss in
/-- **Selberg's lower bound, every `D ≥ 1`.** With `L = lcm(1..D)`, `W = lcm(φ(1..D))` and
`G = ∑_{r ≤ D} μ(r)² (W / φ(r))`:
`W (λ₁ L)² ≤ selbergLHS D λ · G`. Since `selbergLHS D λ = L² Q(λ)` with
`Q(λ) = ∑_{d,e ≤ D} λ_d λ_e / [d,e]`, this is `Q(λ) ≥ λ₁² / G(D)`,
`G(D) = G / W = ∑_{r ≤ D} μ²(r) / φ(r)`. -/
theorem selberg_lower (D : Nat) (hD : 1 ≤ D) (lam : Nat → Int) :
    (phiLcm D : Int) * (lam 1 * (lcmUpto D : Int)) ^ 2 ≤ selbergLHS D lam * selbergG D := by
  rw [← mu_y_sum D hD lam, selberg_diag]
  have hcs := weighted_cauchy_schwarz ((List.range D).map (· + 1)) mu (selbergY D lam)
    (fun r => (totient r : Int)) (fun r => ((phiLcm D / totient r : Nat) : Int))
    (phiLcm D : Int) (by have := phiLcm_pos D; omega)
    (fun x _ => Int.natCast_nonneg _)
    (fun r hr => by
      obtain ⟨hr1, hrD⟩ := mem_range_succ_map.mp hr
      rw [← Int.natCast_mul, Nat.mul_div_cancel' (totient_dvd_phiLcm D r hr1 hrD)])
  exact hcs

/-- For `D = 6`: `W = lcm(1,1,2,2,4,2) = 4` and `G = 4 + 4 + 2 + 0 + 1 + 2 = 13`, so
`G(6) = 13/4` (agreeing with `selberg_opt_D6`). -/
theorem selberg_lower_D6_consts : phiLcm 6 = 4 ∧ selbergG 6 = 13 := by decide

end TwinPrimes
