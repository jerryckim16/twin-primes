import TwinPrimes.MaynardS1
import TwinPrimes.MaynardDiag

/-!
# Maynard's `S₁` in diagonal form, with the explicit finite error

Combines `maynard_S1_error` (`MaynardS1.lean`: `S₁` is `(N/W) ∑_{d,e} λ_d λ_e / ∏ᵢ [dᵢ,eᵢ]` up to
`∑ |λ_d λ_e|`) with `maynard_diag_y_sqfree` (`MaynardDiag.lean`: that quadratic form equals
`∑_u y_u² / ∏ᵢ φ(uᵢ)`). Result (`maynard_S1_diag`), over `ℚ`:

  `|S₁ − (N/W) ∑_{u ∈ {1..R}^k} y_u² / φ(u)| ≤ ∑_{d,e ∈ Dk} |λ_d λ_e|`.

**Support.** The weights live on `Dk = (box R k).filter P` for a Boolean predicate `P` (Maynard's
support, e.g. "entries pairwise coprime, coprime to `W`, `∏ dᵢ < R`"), and `λ = 0` on the rest of
the box, so the diagonal identity over the whole box applies unchanged.
The hypotheses `hDW` (entries coprime to `W`) and `hpw` (for `d, e ∈ Dk` the `lcm(dᵢ, eᵢ)` are
pairwise coprime across `i`) are only required on `Dk`. They can NOT be imposed on the whole box:
for `R ≥ 2`, `k ≥ 2` the pair `d = e = (2,2,…)` violates `hpw` (`box_hpw_fails`), so a version with
`Dk = box R k` would be vacuous. On Maynard's support `hpw` holds for the pairs that matter
because a common prime of `lcm(dᵢ,eᵢ)` and `lcm(dⱼ,eⱼ)` would divide `hᵢ − hⱼ ∣ W`; that
argument is NOT formalised in this file, `hpw` stays a hypothesis here (it is removed in
`MaynardHpw.lean`, `maynard_S1_diag_W`) (see `maynard_S1_diag_example` for a
concrete support where all hypotheses hold).

The auxiliary common multiple `M` of `maynard_S1_error` is constructed internally.
-/

namespace TwinPrimes
namespace MaynardS1Diag

open SelbergOpt MaynardInv MaynardDiag

theorem dvd_prod_of_mem {x : Nat} : ∀ {L : List Nat}, x ∈ L → x ∣ L.prod
  | _ :: L, h => by
    rw [List.prod_cons]
    rcases List.mem_cons.mp h with rfl | h
    · exact Nat.dvd_mul_right _ _
    · exact Nat.dvd_trans (dvd_prod_of_mem h) (Nat.dvd_mul_left _ _)

theorem prod_pos {L : List Nat} (h : ∀ x ∈ L, 0 < x) : 0 < L.prod := by
  have := nat_prod_pos (f := id) h
  rwa [List.map_id] at this

/-- A sum over `l.filter P` equals the sum over `l` when `f` vanishes off `P`. -/
theorem rsum_filter_of_zero {α} (P : α → Bool) (f : α → Rat) : ∀ l : List α,
    (∀ x ∈ l, P x = false → f x = 0) → ((l.filter P).map f).sum = (l.map f).sum
  | [], _ => rfl
  | x :: l, h => by
    have ih := rsum_filter_of_zero P f l (fun y hy => h y (List.mem_cons_of_mem _ hy))
    cases hx : P x
    · rw [List.filter_cons_of_neg (by simp [hx]), ih, List.map_cons, List.sum_cons,
        h x List.mem_cons_self hx, Rat.zero_add]
    · rw [List.filter_cons_of_pos hx, List.map_cons, List.sum_cons, ih, List.map_cons,
        List.sum_cons]

theorem rat_abs_le {x e : Rat} (h1 : -e ≤ x) (h2 : x ≤ e) : Rat.abs x ≤ e := by
  unfold Rat.abs; split <;> grind

/-- **Maynard's `S₁` in `y`-variables, with explicit error.** Over `ℚ`, for integer weights `λ`
supported on `Dk = (box R k).filter P` (`λ = 0` elsewhere in the box) with squarefree entries,
entries of `Dk` coprime to `W`, and `lcm(dᵢ,eᵢ)` pairwise coprime across `i` for `d, e ∈ Dk`:
`|S₁ − (N/W) ∑_{u ∈ box} y_u² / φ(u)| ≤ ∑_{d,e ∈ Dk} |λ_d λ_e|`, where
`S₁ = ∑_{n < N, n ≡ v₀ (W)} (∑_{d ∈ Dk, dᵢ ∣ n + hᵢ} λ_d)²` and `y = maynardY R k λ`. -/
theorem maynard_S1_diag (R k : Nat) (P : List Nat → Bool) (hs : List Nat) (lam : List Nat → Int)
    (W v0 N : Nat) (hv : v0 < W) (hlen : hs.length = k)
    (hoff : ∀ d ∈ box R k, P d = false → lam d = 0)
    (hsq : ∀ d ∈ box R k, lam d ≠ 0 → ∀ x ∈ d, mu x ≠ 0)
    (hDW : ∀ ds ∈ (box R k).filter P, ∀ d ∈ ds, Nat.gcd d W = 1)
    (hpw : ∀ ds ∈ (box R k).filter P, ∀ es ∈ (box R k).filter P,
      (List.zipWith Nat.lcm ds es).Pairwise Nat.Coprime) :
    Rat.abs (((((List.range N).map fun n =>
          if n % W = v0 then mSieveSum ((box R k).filter P) hs lam n
            * mSieveSum ((box R k).filter P) hs lam n else 0).sum : Int) : Rat)
        - (N : Rat) / (W : Rat) * ((box R k).map fun u =>
            maynardY R k (fun d => (lam d : Rat)) u * maynardY R k (fun d => (lam d : Rat)) u
              / tphi u).sum)
      ≤ ((((box R k).filter P).map fun ds => (((box R k).filter P).map fun es =>
          (lam ds * lam es).natAbs).sum).sum : Nat) := by
  generalize hD : (box R k).filter P = Dk at hDW hpw ⊢
  have hDbox : ∀ d ∈ Dk, d ∈ box R k := fun d hd => by
    rw [← hD] at hd; exact (List.mem_filter.mp hd).1
  have hpos : ∀ ds ∈ Dk, ∀ d ∈ ds, 0 < d := fun ds hds d hd =>
    (mem_rng.mp ((mem_box_entries (hDbox ds hds)).2 d hd)).1
  have hlenD : ∀ ds ∈ Dk, ds.length = hs.length := fun ds hds => by
    rw [(mem_box_entries (hDbox ds hds)).1, hlen]
  -- the common multiple `M`
  let Lp : List Nat := Dk.flatMap fun ds => Dk.map fun es => (List.zipWith Nat.lcm ds es).prod
  have hLpos : ∀ ds ∈ Dk, ∀ es ∈ Dk, 0 < (List.zipWith Nat.lcm ds es).prod := by
    intro ds hds es hes
    apply prod_pos; intro x hx
    obtain ⟨a, ha, b, hb, rfl⟩ := mem_zipWith_exists hx
    exact Nat.lcm_pos (hpos ds hds a ha) (hpos es hes b hb)
  have hM : ∀ ds ∈ Dk, ∀ es ∈ Dk, (List.zipWith Nat.lcm ds es).prod ∣ Lp.prod := by
    intro ds hds es hes
    apply dvd_prod_of_mem
    exact List.mem_flatMap.mpr ⟨ds, hds, List.mem_map.mpr ⟨es, hes, rfl⟩⟩
  have hM0 : 0 < Lp.prod := by
    apply prod_pos; intro x hx
    obtain ⟨ds, hds, hx⟩ := List.mem_flatMap.mp hx
    obtain ⟨es, hes, rfl⟩ := List.mem_map.mp hx
    exact hLpos ds hds es hes
  have herr := maynard_S1_error Dk hs lam W v0 N Lp.prod hv hlenD hpos hDW hpw hM
  generalize Lp.prod = M at hM hM0 herr
  -- the main term: `∑_{d,e ∈ Dk} λλ (M / ∏ lcm) = M ∑_{u} y_u² / φ(u)`
  have hmain : ((((Dk.map fun ds => (Dk.map fun es =>
          lam ds * lam es * ((M / (List.zipWith Nat.lcm ds es).prod : Nat) : Int)).sum).sum
          : Int)) : Rat)
      = (M : Rat) * ((box R k).map fun u =>
            maynardY R k (fun d => (lam d : Rat)) u * maynardY R k (fun d => (lam d : Rat)) u
              / tphi u).sum := by
    rw [← maynard_diag_y_sqfree R k _ (fun d hd hl => hsq d hd (fun h0 => hl (by rw [h0]; rfl)))]
    have hR : ((box R k).map fun d => (M : Rat) *
          ((box R k).map fun e => (lam d : Rat) * (lam e : Rat) / tlcm d e).sum).sum
        = (Dk.map fun d => (M : Rat) *
          (Dk.map fun e => (lam d : Rat) * (lam e : Rat) / tlcm d e).sum).sum := by
      rw [← hD, rsum_filter_of_zero]
      · apply rsum_congr; intro ds _
        rw [rsum_filter_of_zero]
        intro es hes hP
        rw [hoff es hes hP]; simp [Rat.mul_zero, rat_div_zero]
      · intro ds hds hP
        rw [hoff ds hds hP]
        rw [rsum_congr (g := fun _ => 0), rsum_zero, Rat.mul_zero]
        intro es _; simp [Rat.zero_mul, rat_div_zero]
    rw [← rsum_mul_left, hR, rsum_cast]
    apply rsum_congr; intro ds hds
    rw [rsum_cast, ← rsum_mul_left]
    apply rsum_congr; intro es hes
    have hdv := Nat.mul_div_cancel' (hM ds hds es hes)
    have hpL := hLpos ds hds es hes
    unfold tlcm
    generalize M / (List.zipWith Nat.lcm ds es).prod = q at hdv
    generalize (List.zipWith Nat.lcm ds es).prod = L at hdv hpL
    subst hdv
    have hL : (L : Rat) ≠ 0 := by
      intro h0; have := Rat.natCast_inj.mp (show (L : Rat) = ((0 : Nat) : Rat) from h0); omega
    rw [Rat.intCast_mul, Rat.intCast_mul, Rat.intCast_natCast, Rat.natCast_mul]
    grind
  generalize ((box R k).map fun u =>
      maynardY R k (fun d => (lam d : Rat)) u * maynardY R k (fun d => (lam d : Rat)) u
        / tphi u).sum = Y at hmain ⊢
  generalize (Dk.map fun ds => (Dk.map fun es =>
      lam ds * lam es * ((M / (List.zipWith Nat.lcm ds es).prod : Nat) : Int)).sum).sum = T
    at hmain herr
  generalize ((List.range N).map fun n =>
      if n % W = v0 then mSieveSum Dk hs lam n * mSieveSum Dk hs lam n else 0).sum = S at herr ⊢
  generalize (Dk.map fun ds => (Dk.map fun es => (lam ds * lam es).natAbs).sum).sum = E at herr ⊢
  -- `|W M S − N T| ≤ W M E` in `ℤ`, then in `ℚ`
  have hi1 : -(((W * M * E : Nat) : Int)) ≤ ((W * M : Nat) : Int) * S - (N : Int) * T := by omega
  have hi2 : ((W * M : Nat) : Int) * S - (N : Int) * T ≤ ((W * M * E : Nat) : Int) := by omega
  have hq1 := Rat.intCast_le_intCast.mpr hi1
  have hq2 := Rat.intCast_le_intCast.mpr hi2
  simp only [Rat.intCast_neg, Rat.intCast_sub, Rat.intCast_mul, Rat.intCast_natCast,
    Rat.natCast_mul, hmain] at hq1 hq2
  have hW : (0 : Rat) < (W : Rat) := Rat.natCast_pos.mpr (by omega)
  have hMq : (0 : Rat) < (M : Rat) := Rat.natCast_pos.mpr hM0
  have hc : (0 : Rat) < (W : Rat) * (M : Rat) := by
    have := Rat.mul_lt_mul_left (a := 0) (b := (M : Rat)) hW; rw [Rat.mul_zero] at this
    exact this.mpr hMq
  have key : (W : Rat) * (M : Rat) * ((S : Rat) - (N : Rat) / (W : Rat) * Y)
      = (W : Rat) * (M : Rat) * (S : Rat) - (N : Rat) * ((M : Rat) * Y) := by
    have : (W : Rat) ≠ 0 := fun h => by rw [h] at hW; exact absurd hW (by decide)
    grind
  apply rat_abs_le
  · apply Rat.le_of_mul_le_mul_left _ hc
    rw [key]; grind
  · apply Rat.le_of_mul_le_mul_left _ hc
    rw [key]; grind

/-! ## Why the support cannot be the whole box -/

/-- Pairwise coprimality of the `lcm(dᵢ, eᵢ)` fails on the full box `{1,2}²` (`d = e = (2,2)`), so
requiring `hpw` for all pairs of `box R k` (`R ≥ 2`, `k ≥ 2`) would make the statement vacuous. -/
theorem box_hpw_fails : ¬ ∀ ds ∈ box 2 2, ∀ es ∈ box 2 2,
    (List.zipWith Nat.lcm ds es).Pairwise Nat.Coprime := by
  intro h
  have := h [2, 2] (by decide) [2, 2] (by decide)
  revert this; decide

/-! ## Non-vacuity: a concrete support where all hypotheses hold -/

/-- Support `{(1,1), (3,1), (1,5)} ⊆ {1..5}²` (`k = 2`, `h = (0, 2)`, `W = 2`, `v₀ = 1`). -/
def exP (d : List Nat) : Bool := d == [1, 1] || d == [3, 1] || d == [1, 5]

def exLam (d : List Nat) : Int := if d = [1, 1] then 2 else if exP d = true then -1 else 0

theorem ex_hoff : ∀ d ∈ box 5 2, exP d = false → exLam d = 0 := by decide

theorem ex_hsq : ∀ d ∈ box 5 2, exLam d ≠ 0 → ∀ x ∈ d, mu x ≠ 0 := by decide

theorem ex_hDW : ∀ ds ∈ (box 5 2).filter exP, ∀ d ∈ ds, Nat.gcd d 2 = 1 := by decide

theorem ex_hpw : ∀ ds ∈ (box 5 2).filter exP, ∀ es ∈ (box 5 2).filter exP,
    (List.zipWith Nat.lcm ds es).Pairwise Nat.Coprime := by decide

/-- All hypotheses of `maynard_S1_diag` hold for this support (for every `N`). -/
theorem maynard_S1_diag_example (N : Nat) :
    Rat.abs (((((List.range N).map fun n =>
          if n % 2 = 1 then mSieveSum ((box 5 2).filter exP) [0, 2] exLam n
            * mSieveSum ((box 5 2).filter exP) [0, 2] exLam n else 0).sum : Int) : Rat)
        - (N : Rat) / (2 : Nat) * ((box 5 2).map fun u =>
            maynardY 5 2 (fun d => (exLam d : Rat)) u * maynardY 5 2 (fun d => (exLam d : Rat)) u
              / tphi u).sum)
      ≤ ((((box 5 2).filter exP).map fun ds => (((box 5 2).filter exP).map fun es =>
          (exLam ds * exLam es).natAbs).sum).sum : Nat) :=
  maynard_S1_diag 5 2 exP [0, 2] exLam 2 1 N (by decide) rfl ex_hoff ex_hsq ex_hDW ex_hpw

end MaynardS1Diag
end TwinPrimes
