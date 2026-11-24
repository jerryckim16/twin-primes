import TwinPrimes.MuTuple

/-!
# Diagonalisation of Maynard's main-term quadratic form (finite, exact)

Maynard (2015, Lemma 5.1 / proof of Prop. 4.1) diagonalises the main term of `S₁`,
`∑_{d,e} λ_d λ_e / ∏ᵢ [dᵢ, eᵢ]`, via Gauss's identity `gcd(a, b) = ∑_{u ∣ a, u ∣ b} φ(u)`
in each coordinate.  For tuples `d, e ∈ {1,…,R}^k` this gives

  `∏ᵢ gcd(dᵢ, eᵢ) = ∑_{u ∈ {1,…,R}^k, u ∣ d, u ∣ e} ∏ᵢ φ(uᵢ)`                 (`tgcd_eq_sum`)

and hence, for **any** weights `w : List Nat → ℚ` on the box (an arbitrary finite support is
`w = 0` off it),

  `∑_{d,e} w_d w_e ∏ᵢ gcd(dᵢ,eᵢ) = ∑_u ∏ᵢ φ(uᵢ) · (∑_{u ∣ d} w_d)²`               (`maynard_diag`).

Taking `w_d = λ_d / ∏ᵢ dᵢ` and using `gcd · lcm = d e` coordinatewise:

  `∑_{d,e} λ_d λ_e / ∏ᵢ [dᵢ,eᵢ] = ∑_u ∏ᵢ φ(uᵢ) · (∑_{u ∣ d} λ_d / ∏ᵢ dᵢ)²`         (`maynard_diag_lcm`),

and with Maynard's `y_u = μ(u) φ(u) ∑_{u ∣ d} λ_d / d` (`maynardY`), whenever `μ(u)² = 1` or the
inner sum vanishes (e.g. `λ` supported on tuples of squarefree entries, `maynard_diag_y_sqfree`):

  `∑_{d,e} λ_d λ_e / ∏ᵢ [dᵢ,eᵢ] = ∑_u y_u² / ∏ᵢ φ(uᵢ)`                           (`maynard_diag_y`).

No coprimality between coordinates is needed for these identities (that enters only in
`maynard_S1_error`, to replace the count by `N / (W ∏ lcm)`).
-/

namespace TwinPrimes
namespace MaynardDiag

open Gauss SelbergOpt MaynardInv MuMult

/-- `∏ᵢ gcd(dᵢ, eᵢ)` as a rational. -/
def tgcd (d e : List Nat) : Rat := (((List.zipWith Nat.gcd d e).prod : Nat) : Rat)

/-- `∏ᵢ lcm(dᵢ, eᵢ)` as a rational. -/
def tlcm (d e : List Nat) : Rat := (((List.zipWith Nat.lcm d e).prod : Nat) : Rat)

theorem rsum_natCast {α} (f : α → Nat) : ∀ l : List α,
    (((l.map f).sum : Nat) : Rat) = (l.map fun x => (f x : Rat)).sum
  | [] => rfl
  | x :: l => by simp only [List.map_cons, List.sum_cons, Rat.natCast_add, rsum_natCast f l]

/-- One coordinate of Gauss's identity, over `ℚ` and the range `{1,…,R}`. -/
theorem gcd_sum_rat (R a b : Nat) (ha : a ∈ rng R) :
    ((Nat.gcd a b : Nat) : Rat)
      = ((rng R).map fun x => if (a % x == 0 && b % x == 0) = true then (totient x : Rat) else 0).sum := by
  obtain ⟨h1, h2⟩ := mem_rng.mp ha
  rw [gcd_eq_sum_totient R a b h1 h2, rsum_natCast]
  apply rsum_congr; intro x _
  split <;> rfl

/-- **Tensorised Gauss identity.** For `d, e ∈ {1,…,R}^k`,
`∏ᵢ gcd(dᵢ, eᵢ) = ∑_{u ∈ {1,…,R}^k, u ∣ d, u ∣ e} ∏ᵢ φ(uᵢ)`. -/
theorem tgcd_eq_sum (R : Nat) : ∀ (k : Nat) (d e : List Nat), d ∈ box R k → e ∈ box R k →
    tgcd d e = ((box R k).map fun u =>
      if (tdvd u d && tdvd u e) = true then tphi u else 0).sum
  | 0, d, e, hd, he => by
    rw [box_zero, List.mem_singleton] at hd he; subst hd; subst he
    simp [box_zero, tgcd, tdvd, tphi, Rat.add_zero]
  | k + 1, d, e, hd, he => by
    obtain ⟨a, d', rfl, ha, hd'⟩ := mem_box_succ hd
    obtain ⟨b, e', rfl, _, he'⟩ := mem_box_succ he
    rw [rsum_box_succ]
    have hsplit : tgcd (a :: d') (b :: e') = ((Nat.gcd a b : Nat) : Rat) * tgcd d' e' := by
      simp only [tgcd, List.zipWith_cons_cons, List.prod_cons, Rat.natCast_mul]
    rw [hsplit, gcd_sum_rat R a b ha, ← rsum_mul_right]
    apply rsum_congr; intro x _
    rw [tgcd_eq_sum R k d' e' hd' he', ← rsum_mul_left]
    apply rsum_congr; intro t _
    simp only [tdvd, tphi, List.map_cons, List.prod_cons, Rat.natCast_mul]
    cases a % x == 0 <;> cases b % x == 0 <;> cases tdvd t d' <;> cases tdvd t e' <;>
      simp [Rat.mul_zero, Rat.zero_mul]

/-- **Diagonalisation of the gcd quadratic form on the box.** For all `w : List Nat → ℚ`,
`∑_{d,e ∈ {1..R}^k} w_d w_e ∏ᵢ gcd(dᵢ,eᵢ) = ∑_{u ∈ {1..R}^k} ∏ᵢ φ(uᵢ) · (∑_{u ∣ d} w_d)²`. -/
theorem maynard_diag (R k : Nat) (w : List Nat → Rat) :
    ((box R k).map fun d => ((box R k).map fun e => w d * w e * tgcd d e).sum).sum
      = ((box R k).map fun u => tphi u * (upSum R k w u * upSum R k w u)).sum := by
  generalize hB : box R k = B
  let x : List Nat → List Nat → Rat := fun u d => if tdvd u d = true then w d else 0
  have hA : ∀ d ∈ B, ∀ e ∈ B, w d * w e * tgcd d e
      = (B.map fun u => tphi u * (x u d * x u e)).sum := by
    intro d hd e he
    rw [tgcd_eq_sum R k d e (hB ▸ hd) (hB ▸ he), hB, ← rsum_mul_left]
    apply rsum_congr; intro u _
    simp only [x]
    cases tdvd u d <;> cases tdvd u e <;> simp <;> grind
  calc (B.map fun d => (B.map fun e => w d * w e * tgcd d e).sum).sum
      = (B.map fun d => (B.map fun e =>
          (B.map fun u => tphi u * (x u d * x u e)).sum).sum).sum := by
        apply rsum_congr; intro d hd; apply rsum_congr; intro e he; exact hA d hd e he
    _ = (B.map fun d => (B.map fun u =>
          (B.map fun e => tphi u * (x u d * x u e)).sum).sum).sum := by
        apply rsum_congr; intro d _
        exact rsum_comm (fun e u => tphi u * (x u d * x u e)) B B
    _ = (B.map fun u => (B.map fun d =>
          (B.map fun e => tphi u * (x u d * x u e)).sum).sum).sum :=
        rsum_comm (fun d u => (B.map fun e => tphi u * (x u d * x u e)).sum) B B
    _ = (B.map fun u => tphi u * (upSum R k w u * upSum R k w u)).sum := by
        apply rsum_congr; intro u _
        unfold upSum; rw [hB]
        change _ = tphi u * ((B.map (x u)).sum * (B.map (x u)).sum)
        rw [← rsum_mul_right, ← rsum_mul_left]
        apply rsum_congr; intro d _
        rw [← rsum_mul_left, ← rsum_mul_left]

theorem natprod_gcd_mul_lcm : ∀ d e : List Nat, d.length = e.length →
    (List.zipWith Nat.gcd d e).prod * (List.zipWith Nat.lcm d e).prod = d.prod * e.prod
  | [], [], _ => rfl
  | a :: d, b :: e, h => by
    simp only [List.zipWith_cons_cons, List.prod_cons]
    have ih := natprod_gcd_mul_lcm d e (by simpa using h)
    have hg := Nat.gcd_mul_lcm a b
    calc Nat.gcd a b * (List.zipWith Nat.gcd d e).prod * (Nat.lcm a b * (List.zipWith Nat.lcm d e).prod)
        = (Nat.gcd a b * Nat.lcm a b) *
            ((List.zipWith Nat.gcd d e).prod * (List.zipWith Nat.lcm d e).prod) := by ac_rfl
      _ = (a * b) * (d.prod * e.prod) := by rw [hg, ih]
      _ = a * d.prod * (b * e.prod) := by ac_rfl
  | [], _ :: _, h => by simp at h
  | _ :: _, [], h => by simp at h

/-- `∏ᵢ gcd(dᵢ,eᵢ) · ∏ᵢ lcm(dᵢ,eᵢ) = ∏ᵢ dᵢ · ∏ᵢ eᵢ` (as rationals). -/
theorem tgcd_mul_tlcm {R k : Nat} {d e : List Nat} (hd : d ∈ box R k) (he : e ∈ box R k) :
    tgcd d e * tlcm d e = tN d * tN e := by
  unfold tgcd tlcm tN
  rw [← Rat.natCast_mul, ← Rat.natCast_mul,
    natprod_gcd_mul_lcm d e (by rw [(mem_box_entries hd).1, (mem_box_entries he).1])]

/-- **Diagonalisation in Maynard's `1/[d,e]` form.** For all `λ : List Nat → ℚ`,
`∑_{d,e ∈ {1..R}^k} λ_d λ_e / ∏ᵢ [dᵢ,eᵢ] = ∑_u ∏ᵢ φ(uᵢ) · (∑_{u ∣ d} λ_d / ∏ᵢ dᵢ)²`. -/
theorem maynard_diag_lcm (R k : Nat) (lam : List Nat → Rat) :
    ((box R k).map fun d => ((box R k).map fun e => lam d * lam e / tlcm d e).sum).sum
      = ((box R k).map fun u => tphi u *
          (upSum R k (fun d => lam d / tN d) u * upSum R k (fun d => lam d / tN d) u)).sum := by
  rw [← maynard_diag]
  apply rsum_congr; intro d hd; apply rsum_congr; intro e he
  have h := tgcd_mul_tlcm hd he
  have hdn := tN_ne_zero hd
  have hen := tN_ne_zero he
  have hl : tlcm d e ≠ 0 := by
    intro h0; rw [h0, Rat.mul_zero] at h
    grind
  have : tgcd d e = tN d * tN e / tlcm d e := by grind
  rw [this]
  grind

/-- **Diagonalisation in Maynard's `y`-variables.** If for every `u` in the box either
`μ(u)² = 1` (coordinatewise product) or `∑_{u ∣ d} λ_d / d = 0`, then
`∑_{d,e} λ_d λ_e / ∏ᵢ [dᵢ,eᵢ] = ∑_u y_u² / ∏ᵢ φ(uᵢ)` with `y = maynardY R k λ`. -/
theorem maynard_diag_y (R k : Nat) (lam : List Nat → Rat)
    (hsq : ∀ u ∈ box R k, tmu u * tmu u = 1 ∨ upSum R k (fun d => lam d / tN d) u = 0) :
    ((box R k).map fun d => ((box R k).map fun e => lam d * lam e / tlcm d e).sum).sum
      = ((box R k).map fun u => maynardY R k lam u * maynardY R k lam u / tphi u).sum := by
  rw [maynard_diag_lcm]
  apply rsum_congr; intro u hu
  have hp := tphi_ne_zero hu
  unfold maynardY
  have hs := hsq u hu
  generalize upSum R k (fun d => lam d / tN d) u = U at hs ⊢
  rcases hs with h | h
  · have : tmu u * tphi u * U * (tmu u * tphi u * U) / tphi u
        = (tmu u * tmu u) * (tphi u * (U * U)) * tphi u / tphi u := by grind
    rw [this, h, Rat.one_mul]
    grind
  · subst h; simp [Rat.mul_zero, rat_div_zero]

/-! ## Squarefree support -/

theorem rat_mu_sq {x : Nat} (hx : 1 ≤ x) (h : Sqf x) : (mu x : Rat) * (mu x : Rat) = 1 := by
  rw [← Rat.intCast_mul, mu_mul_self_sqf x hx h]; rfl

/-- If `u ∣ d` coordinatewise, all `dᵢ ≥ 1` squarefree, then `μ(u)² = 1`. -/
theorem tmu_sq_of_tdvd : ∀ u d : List Nat, tdvd u d = true →
    (∀ y ∈ d, 1 ≤ y ∧ Sqf y) → tmu u * tmu u = 1
  | [], [], _, _ => by simp [tmu]
  | a :: u, b :: d, h, hd => by
    simp only [tdvd, Bool.and_eq_true, beq_iff_eq] at h
    obtain ⟨hab, hud⟩ := h
    have hb := hd b List.mem_cons_self
    have hadv : a ∣ b := Nat.dvd_of_mod_eq_zero hab
    have ha1 : 1 ≤ a := by
      rcases Nat.eq_zero_or_pos a with h0 | h0
      · subst h0; rw [Nat.mod_zero] at hab; omega
      · exact h0
    have ih := tmu_sq_of_tdvd u d hud (fun y hy => hd y (List.mem_cons_of_mem _ hy))
    have ha := rat_mu_sq ha1 (sqf_of_dvd hb.2 hadv)
    unfold tmu at ih ⊢
    simp only [List.map_cons, List.prod_cons]
    calc (mu a : Rat) * (u.map fun x => (mu x : Rat)).prod *
          ((mu a : Rat) * (u.map fun x => (mu x : Rat)).prod)
        = ((mu a : Rat) * (mu a : Rat)) *
            ((u.map fun x => (mu x : Rat)).prod * (u.map fun x => (mu x : Rat)).prod) := by
          grind
      _ = 1 := by rw [ha, ih, Rat.one_mul]
  | [], _ :: _, h, _ => by simp [tdvd] at h
  | _ :: _, [], h, _ => by simp [tdvd] at h

/-- **Maynard's diagonal form for squarefree-supported `λ`.** If `λ_d ≠ 0` only when every `dᵢ`
has `μ(dᵢ) ≠ 0`, then `∑_{d,e} λ_d λ_e / ∏ᵢ [dᵢ,eᵢ] = ∑_u y_u² / ∏ᵢ φ(uᵢ)`. -/
theorem maynard_diag_y_sqfree (R k : Nat) (lam : List Nat → Rat)
    (hlam : ∀ d ∈ box R k, lam d ≠ 0 → ∀ x ∈ d, mu x ≠ 0) :
    ((box R k).map fun d => ((box R k).map fun e => lam d * lam e / tlcm d e).sum).sum
      = ((box R k).map fun u => maynardY R k lam u * maynardY R k lam u / tphi u).sum := by
  apply maynard_diag_y
  intro u _
  apply Classical.byCases (p := ∃ d ∈ box R k, tdvd u d = true ∧ lam d ≠ 0)
  · rintro ⟨d, hd, hud, hl⟩
    left
    apply tmu_sq_of_tdvd u d hud
    intro y hy
    have hy1 := (mem_rng.mp ((mem_box_entries hd).2 y hy)).1
    exact ⟨hy1, sqf_of_mu y hy1 (hlam d hd hl y hy)⟩
  · intro hn
    right
    unfold upSum
    rw [rsum_congr (g := fun _ => 0), rsum_zero]
    intro d hd
    by_cases hud : tdvd u d = true
    · have : lam d = 0 := Classical.byContradiction fun hl => hn ⟨d, hd, hud, hl⟩
      simp [hud, this, rat_div_zero]
    · simp [hud]

/-! ## Examples -/

/-- `∏ gcd((4,6),(6,9)) = 2 · 3 = 6 = ∑_{u ∣ (2,3)} φ(u₁) φ(u₂) = (1+1)(1+2)`. -/
example : (List.zipWith Nat.gcd [4, 6] [6, 9]).prod = 6 ∧
    (((box 3 2).filter fun u => tdvd u [4, 6] && tdvd u [6, 9]).map
      fun u => (u.map totient).prod).sum = 6 := by decide

/-- A concrete instance of the gcd form of `maynard_diag` (`R = 3`, `k = 2`, `w = ∑ dᵢ − 3`):
both sides equal the same integer. -/
example :
    let B := box 3 2
    let w : List Nat → Int := fun d => (d.sum : Int) - 3
    (B.map fun d => (B.map fun e =>
        w d * w e * (((List.zipWith Nat.gcd d e).prod : Nat) : Int)).sum).sum
      = (B.map fun u => (((u.map totient).prod : Nat) : Int) *
          ((B.filter fun d => tdvd u d).map w).sum ^ 2).sum := by decide

end MaynardDiag
end TwinPrimes
