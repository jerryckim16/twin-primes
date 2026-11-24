import TwinPrimes.MaynardS1Diag

/-!
# Discharging `hpw`: pairs with non-coprime `lcm`s do not contribute to `S₁`

`maynard_S1_diag` (`MaynardS1Diag.lean`) assumes `hpw`: for all `d, e` in the support the moduli
`lcm(dᵢ, eᵢ)` are pairwise coprime across `i`. On Maynard's actual support this is FALSE for some
pairs (e.g. `h = (0, 2)`, `d = (3, 1)`, `e = (1, 3)` gives the moduli `(3, 3)`), so `hpw` can not
simply be proved for the support. What is true (Maynard 2015, Sect. 5) is that such pairs
contribute nothing to `S₁`: if `p ∣ lcm(dᵢ,eᵢ)` and `p ∣ lcm(dⱼ,eⱼ)` with `i ≠ j`, then
`p ∣ (n + hᵢ) − (n + hⱼ) = hᵢ − hⱼ`, hence `p ∣ W`, contradicting `gcd(dᵢ eᵢ, W) = 1`.

Formalised (the shift condition is `ShiftsDvd hs W`: `|hᵢ − hⱼ| ∣ W` for all `i < j`):
* `pairwise_coprime_of_solvable`: if `L` (entries coprime to `W`) admits an `n` with
  `Lᵢ ∣ n + hᵢ` for all `i`, then the `Lᵢ` are pairwise coprime (no primes needed: the gcd
  divides `hᵢ − hⱼ`, hence `W`);
* `hpw_of_solvable`: the exact `hpw` hypothesis of `maynard_S1_diag`, for every pair of the
  support whose congruence systems are jointly solvable;
* `count_zero_of_not_pairwise`: for a "bad" pair the count `#{n < N : n ≡ v₀ (W), dᵢ,eᵢ ∣ n+hᵢ}`
  in the expansion of `S₁` is `0`;
* `maynard_S1_error_W`: `maynard_S1_error` WITHOUT `hpw`, the main term running over good pairs;
* `maynard_S1_diag_W`: `maynard_S1_diag` WITHOUT `hpw`:
  `|S₁ − (N/W) (∑_u y_u²/φ(u) − B)| ≤ ∑_{d,e} |λ_d λ_e|`, where
  `B = ∑_{d,e bad} λ_d λ_e / ∏ᵢ lcm(dᵢ,eᵢ)` is the (explicit) main-term contribution of the bad
  pairs that Maynard removes; `B = 0` when all pairs are good.
* `maynard_S1_diag_W_example`: a support WITH a bad pair (`(3,1)`, `(1,3)`, `h = (0,2)`, `W = 2`)
  where all hypotheses hold, and `B = 2/9 ≠ 0` there (`ex_B_eq`).

NOT formalised: the analytic size of `B` (Maynard's treatment via the extra Möbius variables).
-/

namespace TwinPrimes
namespace MaynardHpw

open SelbergOpt MaynardInv MaynardDiag MaynardS1Diag

/-- All pairwise differences of the shifts divide `W`: `|hᵢ − hⱼ| ∣ W` for `i < j`. -/
abbrev ShiftsDvd (hs : List Nat) (W : Nat) : Prop :=
  hs.Pairwise fun (a b : Nat) => ((a : Int) - (b : Int)).natAbs ∣ W

/-- A pair `(d, e)` is good when the `lcm(dᵢ, eᵢ)` are pairwise coprime. -/
def goodPair (ds es : List Nat) : Bool :=
  decide ((List.zipWith Nat.lcm ds es).Pairwise Nat.Coprime)

theorem coprime_of_dvd_shift {x y a b n W : Nat} (hx : x ∣ n + a) (hy : y ∣ n + b)
    (hab : ((a : Int) - (b : Int)).natAbs ∣ W) (hxW : Nat.gcd x W = 1) : Nat.Coprime x y := by
  have g1 : ((Nat.gcd x y : Nat) : Int) ∣ ((n + a : Nat) : Int) :=
    Int.natCast_dvd_natCast.mpr (Nat.dvd_trans (Nat.gcd_dvd_left x y) hx)
  have g2 : ((Nat.gcd x y : Nat) : Int) ∣ ((n + b : Nat) : Int) :=
    Int.natCast_dvd_natCast.mpr (Nat.dvd_trans (Nat.gcd_dvd_right x y) hy)
  have g3 := Int.dvd_sub g1 g2
  have he : ((n + a : Nat) : Int) - ((n + b : Nat) : Int) = (a : Int) - (b : Int) := by omega
  rw [he] at g3
  have g4 : Nat.gcd x y ∣ W := Nat.dvd_trans (Int.ofNat_dvd_left.mp g3) hab
  have g5 : Nat.gcd x y ∣ Nat.gcd x W := Nat.dvd_gcd (Nat.gcd_dvd_left x y) g4
  rw [hxW] at g5
  exact Nat.dvd_one.mp g5

theorem tupleDvd_cons (h x n : Nat) (hs L : List Nat) :
    tupleDvd (h :: hs) n (x :: L) = ((n + h) % x == 0 && tupleDvd hs n L) := rfl

theorem exists_shift_of_tupleDvd {n : Nat} : ∀ (L hs : List Nat), tupleDvd hs n L = true →
    ∀ y ∈ L, L.length = hs.length → ∃ b ∈ hs, y ∣ n + b
  | [], _, _, _, hy, _ => by simp at hy
  | _ :: _, [], _, _, _, hl => by simp at hl
  | x :: L, h :: hs, ht, y, hy, hl => by
    rw [tupleDvd_cons, Bool.and_eq_true, beq_iff_eq] at ht
    rcases List.mem_cons.mp hy with rfl | hy
    · exact ⟨h, List.mem_cons_self, Nat.dvd_of_mod_eq_zero ht.1⟩
    · obtain ⟨b, hb, hd⟩ := exists_shift_of_tupleDvd L hs ht.2 y hy (by simpa using hl)
      exact ⟨b, List.mem_cons_of_mem _ hb, hd⟩

/-- **Core lemma.** If the shifts satisfy `|hᵢ − hⱼ| ∣ W`, the entries of `L` are coprime to `W`
and some `n` satisfies `Lᵢ ∣ n + hᵢ` for all `i`, then the `Lᵢ` are pairwise coprime. -/
theorem pairwise_coprime_of_solvable {W n : Nat} : ∀ (L hs : List Nat), L.length = hs.length →
    ShiftsDvd hs W → (∀ x ∈ L, Nat.gcd x W = 1) → tupleDvd hs n L = true →
    L.Pairwise Nat.Coprime
  | [], _, _, _, _, _ => List.Pairwise.nil
  | _ :: _, [], hl, _, _, _ => by simp at hl
  | x :: L, h :: hs, hl, hH, hW, ht => by
    have hl' : L.length = hs.length := by simpa using hl
    have hH' := List.pairwise_cons.mp hH
    have ht' := ht
    rw [tupleDvd_cons, Bool.and_eq_true, beq_iff_eq] at ht'
    refine List.pairwise_cons.mpr ⟨fun y hy => ?_, pairwise_coprime_of_solvable L hs hl' hH'.2
      (fun z hz => hW z (List.mem_cons_of_mem _ hz)) ht'.2⟩
    obtain ⟨b, hb, hyb⟩ := exists_shift_of_tupleDvd L hs ht'.2 y hy hl'
    exact coprime_of_dvd_shift (Nat.dvd_of_mod_eq_zero ht'.1) hyb (hH'.1 b hb)
      (hW x List.mem_cons_self)

theorem lcm_entries_coprime {W : Nat} {ds es : List Nat} (hd : ∀ d ∈ ds, Nat.gcd d W = 1)
    (he : ∀ e ∈ es, Nat.gcd e W = 1) : ∀ x ∈ List.zipWith Nat.lcm ds es, Nat.gcd x W = 1 := by
  intro x hx
  obtain ⟨a, ha, b, hb, rfl⟩ := mem_zipWith_exists hx
  have hab : Nat.Coprime (a * b) W := Nat.Coprime.mul_left (hd a ha) (he b hb)
  exact Nat.Coprime.coprime_dvd_left
    (Nat.lcm_dvd (Nat.dvd_mul_right a b) (Nat.dvd_mul_left b a)) hab

/-- **`hpw` for solvable pairs**: under `ShiftsDvd hs W` and `hDW`, every pair `(d, e)` of the
support whose systems `dᵢ ∣ n + hᵢ`, `eᵢ ∣ n + hᵢ` have a common solution `n` satisfies the
`hpw` condition of `maynard_S1_diag`. -/
theorem hpw_of_solvable (Dk : List (List Nat)) (hs : List Nat) (W : Nat)
    (hlen : ∀ ds ∈ Dk, ds.length = hs.length) (hH : ShiftsDvd hs W)
    (hDW : ∀ ds ∈ Dk, ∀ d ∈ ds, Nat.gcd d W = 1)
    (hsol : ∀ ds ∈ Dk, ∀ es ∈ Dk, ∃ n, tupleDvd hs n ds = true ∧ tupleDvd hs n es = true) :
    ∀ ds ∈ Dk, ∀ es ∈ Dk, (List.zipWith Nat.lcm ds es).Pairwise Nat.Coprime := by
  intro ds hds es hes
  obtain ⟨n, h1, h2⟩ := hsol ds hds es hes
  have ht : tupleDvd hs n (List.zipWith Nat.lcm ds es) = true := by
    rw [← tupleDvd_lcm hs ds es n (hlen ds hds) (hlen es hes), h1, h2]; rfl
  exact pairwise_coprime_of_solvable (n := n) _ hs
    (by rw [List.length_zipWith, hlen ds hds, hlen es hes, Nat.min_self]) hH
    (lcm_entries_coprime (hDW ds hds) (hDW es hes)) ht

/-- **Bad pairs do not count**: if the `lcm(dᵢ, eᵢ)` are not pairwise coprime, no `n` satisfies
`dᵢ ∣ n + hᵢ` and `eᵢ ∣ n + hᵢ` for all `i`, so the pair's count in the expansion of `S₁` is `0`. -/
theorem count_zero_of_not_pairwise (hs ds es : List Nat) (W v0 N : Nat)
    (hd : ds.length = hs.length) (he : es.length = hs.length) (hH : ShiftsDvd hs W)
    (hdW : ∀ d ∈ ds, Nat.gcd d W = 1) (heW : ∀ e ∈ es, Nat.gcd e W = 1)
    (hbad : ¬ (List.zipWith Nat.lcm ds es).Pairwise Nat.Coprime) :
    (List.range N).countP (fun n => n % W == v0 && tupleDvd hs n ds && tupleDvd hs n es) = 0 := by
  apply List.countP_eq_zero.mpr
  intro n _ hn
  apply hbad
  rw [Bool.and_assoc, Bool.and_eq_true, tupleDvd_lcm hs ds es n hd he] at hn
  exact pairwise_coprime_of_solvable (n := n) _ hs
    (by rw [List.length_zipWith, hd, he, Nat.min_self]) hH (lcm_entries_coprime hdW heW) hn.2

/-- **`maynard_S1_error` without `hpw`.** Replacing `hpw` by `ShiftsDvd hs W`, the same bound holds
with the main term restricted to good pairs:
`|W M · S₁ − N ∑_{d,e good} λ_d λ_e (M / ∏ᵢ lcm(dᵢ,eᵢ))| ≤ W M ∑_{d,e} |λ_d λ_e|`. -/
theorem maynard_S1_error_W (Dk : List (List Nat)) (hs : List Nat) (lam : List Nat → Int)
    (W v0 N M : Nat) (hv : v0 < W)
    (hlen : ∀ ds ∈ Dk, ds.length = hs.length)
    (hpos : ∀ ds ∈ Dk, ∀ d ∈ ds, 0 < d)
    (hDW : ∀ ds ∈ Dk, ∀ d ∈ ds, Nat.gcd d W = 1)
    (hH : ShiftsDvd hs W)
    (hM : ∀ ds ∈ Dk, ∀ es ∈ Dk, (List.zipWith Nat.lcm ds es).prod ∣ M) :
    (((W * M : Nat) : Int) * ((List.range N).map fun n =>
          if n % W = v0 then mSieveSum Dk hs lam n * mSieveSum Dk hs lam n else 0).sum
      - (N : Int) * (Dk.map fun ds => (Dk.map fun es =>
          lam ds * lam es * ((if goodPair ds es then M / (List.zipWith Nat.lcm ds es).prod
            else 0 : Nat) : Int)).sum).sum).natAbs
      ≤ W * M * (Dk.map fun ds => (Dk.map fun es => (lam ds * lam es).natAbs).sum).sum := by
  rw [maynard_S1_expand_W, ← isum_mul_left, ← isum_mul_left, ← isum_sub, ← nsum_mul_left]
  refine Nat.le_trans (natAbs_isum_le _ _) (nsum_le ?_)
  intro ds hds
  rw [← isum_mul_left, ← isum_mul_left, ← isum_sub, ← nsum_mul_left]
  refine Nat.le_trans (natAbs_isum_le _ _) (nsum_le ?_)
  intro es hes
  cases hg : goodPair ds es
  · -- bad pair: the count vanishes and so does the main term
    have hbad : ¬ (List.zipWith Nat.lcm ds es).Pairwise Nat.Coprime := by
      intro h; simp [goodPair, h] at hg
    rw [count_zero_of_not_pairwise hs ds es W v0 N (hlen ds hds) (hlen es hes) hH
      (hDW ds hds) (hDW es hes) hbad]
    simp
  · have hgood : (List.zipWith Nat.lcm ds es).Pairwise Nat.Coprime := by
      simpa [goodPair] using hg
    simp only [ite_true]
    have hlenL : (List.zipWith Nat.lcm ds es).length = hs.length := by
      rw [List.length_zipWith, hlen ds hds, hlen es hes, Nat.min_self]
    have hposL : ∀ x ∈ List.zipWith Nat.lcm ds es, 0 < x := by
      intro x hx
      obtain ⟨a, ha, b, hb, rfl⟩ := mem_zipWith_exists hx
      exact Nat.lcm_pos (hpos ds hds a ha) (hpos es hes b hb)
    have hcount : ((List.range N).countP fun n =>
        n % W == v0 && tupleDvd hs n ds && tupleDvd hs n es)
        = (List.range N).countP fun n =>
            n % W == v0 && tupleDvd hs n (List.zipWith Nat.lcm ds es) := by
      congr 1; funext n
      rw [Bool.and_assoc, tupleDvd_lcm hs ds es n (hlen ds hds) (hlen es hes)]
    rw [hcount]
    obtain ⟨b1, b2⟩ := crt_tuple_count_bounds hv _ hs hlenL hposL
      (lcm_entries_coprime (hDW ds hds) (hDW es hes)) hgood N
    generalize (List.range N).countP
      (fun n => n % W == v0 && tupleDvd hs n (List.zipWith Nat.lcm ds es)) = c at b1 b2 ⊢
    have hk := Nat.mul_div_cancel' (hM ds hds es hes)
    generalize M / (List.zipWith Nat.lcm ds es).prod = k at hk
    generalize (List.zipWith Nat.lcm ds es).prod = L at b1 b2 hk
    subst hk
    have : (↑(W * (L * k)) : Int) * (lam ds * lam es * (c : Int))
          - (N : Int) * (lam ds * lam es * (k : Int))
        = lam ds * lam es * ((k : Int) * ((W * L * c : Nat) - (N : Int))) := by
      simp only [Int.natCast_mul, Int.mul_sub]
      simp only [Int.mul_assoc, Int.mul_comm, Int.mul_left_comm]
    rw [this, Int.natAbs_mul, Nat.mul_comm (W * (L * k))]
    apply Nat.mul_le_mul_left
    rw [Int.natAbs_mul, Int.natAbs_natCast,
      show W * (L * k) = k * (W * L) by rw [Nat.mul_comm k, Nat.mul_assoc]]
    apply Nat.mul_le_mul_left
    rw [Nat.mul_add, Nat.mul_one] at b1
    omega

theorem rsum_sub {α} (f g : α → Rat) : ∀ l : List α,
    (l.map fun x => f x - g x).sum = (l.map f).sum - (l.map g).sum
  | [] => by simp only [List.map_nil, List.sum_nil]; grind
  | x :: l => by
    simp only [List.map_cons, List.sum_cons]
    rw [rsum_sub f g l]; grind

/-- **Maynard's `S₁` in `y`-variables, without `hpw`.** Same setting as `maynard_S1_diag`, but
instead of `hpw` only `|hᵢ − hⱼ| ∣ W` is assumed. With
`B = ∑_{d,e ∈ Dk, (d,e) bad} λ_d λ_e / ∏ᵢ lcm(dᵢ,eᵢ)` (the bad-pair part of the main term):
`|S₁ − (N/W) (∑_u y_u² / φ(u) − B)| ≤ ∑_{d,e ∈ Dk} |λ_d λ_e|`. -/
theorem maynard_S1_diag_W (R k : Nat) (P : List Nat → Bool) (hs : List Nat)
    (lam : List Nat → Int) (W v0 N : Nat) (hv : v0 < W) (hlen : hs.length = k)
    (hoff : ∀ d ∈ box R k, P d = false → lam d = 0)
    (hsq : ∀ d ∈ box R k, lam d ≠ 0 → ∀ x ∈ d, mu x ≠ 0)
    (hDW : ∀ ds ∈ (box R k).filter P, ∀ d ∈ ds, Nat.gcd d W = 1)
    (hH : ShiftsDvd hs W) :
    Rat.abs (((((List.range N).map fun n =>
          if n % W = v0 then mSieveSum ((box R k).filter P) hs lam n
            * mSieveSum ((box R k).filter P) hs lam n else 0).sum : Int) : Rat)
        - (N : Rat) / (W : Rat) * (((box R k).map fun u =>
            maynardY R k (fun d => (lam d : Rat)) u * maynardY R k (fun d => (lam d : Rat)) u
              / tphi u).sum
          - (((box R k).filter P).map fun ds => (((box R k).filter P).map fun es =>
              if goodPair ds es then (0 : Rat)
              else (lam ds : Rat) * (lam es : Rat) / tlcm ds es).sum).sum))
      ≤ ((((box R k).filter P).map fun ds => (((box R k).filter P).map fun es =>
          (lam ds * lam es).natAbs).sum).sum : Nat) := by
  -- `y`-form of the full quadratic form, restricted to the support
  have hY : ((box R k).map fun u =>
        maynardY R k (fun d => (lam d : Rat)) u * maynardY R k (fun d => (lam d : Rat)) u
          / tphi u).sum
      = (((box R k).filter P).map fun d => (((box R k).filter P).map fun e =>
          (lam d : Rat) * (lam e : Rat) / tlcm d e).sum).sum := by
    rw [← maynard_diag_y_sqfree R k _ (fun d hd hl => hsq d hd (fun h0 => hl (by rw [h0]; rfl)))]
    rw [rsum_filter_of_zero]
    · apply rsum_congr; intro ds _
      rw [rsum_filter_of_zero]
      intro es hes hP
      rw [hoff es hes hP]; simp [Rat.mul_zero, rat_div_zero]
    · intro ds hds hP
      rw [hoff ds hds hP]
      rw [rsum_congr (g := fun _ => 0), rsum_zero]
      intro es _; simp [Rat.zero_mul, rat_div_zero]
  rw [hY]
  generalize hD : (box R k).filter P = Dk at hDW ⊢
  have hDbox : ∀ d ∈ Dk, d ∈ box R k := fun d hd => by
    rw [← hD] at hd; exact (List.mem_filter.mp hd).1
  have hpos : ∀ ds ∈ Dk, ∀ d ∈ ds, 0 < d := fun ds hds d hd =>
    (mem_rng.mp ((mem_box_entries (hDbox ds hds)).2 d hd)).1
  have hlenD : ∀ ds ∈ Dk, ds.length = hs.length := fun ds hds => by
    rw [(mem_box_entries (hDbox ds hds)).1, hlen]
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
  have herr := maynard_S1_error_W Dk hs lam W v0 N Lp.prod hv hlenD hpos hDW hH hM
  generalize Lp.prod = M at hM hM0 herr
  -- main term over good pairs `= M (Y − B)`
  have hmain : ((((Dk.map fun ds => (Dk.map fun es =>
          lam ds * lam es * ((if goodPair ds es then M / (List.zipWith Nat.lcm ds es).prod
            else 0 : Nat) : Int)).sum).sum : Int)) : Rat)
      = (M : Rat) * ((Dk.map fun d => (Dk.map fun e =>
          (lam d : Rat) * (lam e : Rat) / tlcm d e).sum).sum
        - (Dk.map fun ds => (Dk.map fun es =>
              if goodPair ds es then (0 : Rat)
              else (lam ds : Rat) * (lam es : Rat) / tlcm ds es).sum).sum) := by
    rw [← rsum_sub, ← rsum_mul_left, rsum_cast]
    apply rsum_congr; intro ds hds
    rw [← rsum_sub, ← rsum_mul_left, rsum_cast]
    apply rsum_congr; intro es hes
    cases hg : goodPair ds es
    · simp only [Bool.false_eq_true, ite_false]
      simp only [Int.mul_zero, Int.natCast_zero, Rat.intCast_zero, Rat.sub_self, Rat.mul_zero]
    · simp only [ite_true]
      have hdv := Nat.mul_div_cancel' (hM ds hds es hes)
      have hpL := hLpos ds hds es hes
      unfold tlcm
      generalize M / (List.zipWith Nat.lcm ds es).prod = q at hdv
      generalize (List.zipWith Nat.lcm ds es).prod = L at hdv hpL
      subst hdv
      have hL : (L : Rat) ≠ 0 := by
        intro h0
        have := Rat.natCast_inj.mp (show (L : Rat) = ((0 : Nat) : Rat) from h0); omega
      rw [Rat.intCast_mul, Rat.intCast_mul, Rat.intCast_natCast, Rat.natCast_mul]
      grind
  generalize (Dk.map fun d => (Dk.map fun e =>
      (lam d : Rat) * (lam e : Rat) / tlcm d e).sum).sum = Y at hmain ⊢
  generalize (Dk.map fun ds => (Dk.map fun es =>
      if goodPair ds es then (0 : Rat)
      else (lam ds : Rat) * (lam es : Rat) / tlcm ds es).sum).sum = B at hmain ⊢
  generalize (Dk.map fun ds => (Dk.map fun es =>
      lam ds * lam es * ((if goodPair ds es then M / (List.zipWith Nat.lcm ds es).prod
        else 0 : Nat) : Int)).sum).sum = T at hmain herr
  generalize ((List.range N).map fun n =>
      if n % W = v0 then mSieveSum Dk hs lam n * mSieveSum Dk hs lam n else 0).sum = S at herr ⊢
  generalize (Dk.map fun ds => (Dk.map fun es => (lam ds * lam es).natAbs).sum).sum = E
    at herr ⊢
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
  have key : (W : Rat) * (M : Rat) * ((S : Rat) - (N : Rat) / (W : Rat) * (Y - B))
      = (W : Rat) * (M : Rat) * (S : Rat) - (N : Rat) * ((M : Rat) * (Y - B)) := by
    have : (W : Rat) ≠ 0 := fun h => by rw [h] at hW; exact absurd hW (by decide)
    grind
  apply rat_abs_le
  · apply Rat.le_of_mul_le_mul_left _ hc
    rw [key]; grind
  · apply Rat.le_of_mul_le_mul_left _ hc
    rw [key]; grind

/-! ## Non-vacuity: a support containing a bad pair -/

/-- Support `{(1,1), (3,1), (1,3)} ⊆ {1..3}²`, `h = (0, 2)`, `W = 2`, `v₀ = 1`. The pair
`((3,1), (1,3))` is bad (`lcm`s `(3,3)`), so `hpw` FAILS here, but `maynard_S1_diag_W` applies. -/
def exP (d : List Nat) : Bool := d == [1, 1] || d == [3, 1] || d == [1, 3]

def exLam (d : List Nat) : Int := if d = [1, 1] then 2 else if exP d = true then -1 else 0

theorem ex_hoff : ∀ d ∈ box 3 2, exP d = false → exLam d = 0 := by decide

theorem ex_hsq : ∀ d ∈ box 3 2, exLam d ≠ 0 → ∀ x ∈ d, mu x ≠ 0 := by decide

theorem ex_hDW : ∀ ds ∈ (box 3 2).filter exP, ∀ d ∈ ds, Nat.gcd d 2 = 1 := by decide

theorem ex_hH : ShiftsDvd [0, 2] 2 := by decide

/-- `hpw` of `maynard_S1_diag` fails on this support. -/
theorem ex_not_hpw : ¬ ∀ ds ∈ (box 3 2).filter exP, ∀ es ∈ (box 3 2).filter exP,
    (List.zipWith Nat.lcm ds es).Pairwise Nat.Coprime := by
  intro h
  have := h [3, 1] (by decide) [1, 3] (by decide)
  revert this; decide

/-- The bad-pair correction `B` is nonzero here (`B = 2/9`). -/
theorem ex_B_eq : (((box 3 2).filter exP).map fun ds => (((box 3 2).filter exP).map fun es =>
    if goodPair ds es then (0 : Rat)
    else (exLam ds : Rat) * (exLam es : Rat) / tlcm ds es).sum).sum = 2 / 9 := by
  decide +kernel

theorem maynard_S1_diag_W_example (N : Nat) :
    Rat.abs (((((List.range N).map fun n =>
          if n % 2 = 1 then mSieveSum ((box 3 2).filter exP) [0, 2] exLam n
            * mSieveSum ((box 3 2).filter exP) [0, 2] exLam n else 0).sum : Int) : Rat)
        - (N : Rat) / (2 : Nat) * (((box 3 2).map fun u =>
            maynardY 3 2 (fun d => (exLam d : Rat)) u * maynardY 3 2 (fun d => (exLam d : Rat)) u
              / tphi u).sum
          - (((box 3 2).filter exP).map fun ds => (((box 3 2).filter exP).map fun es =>
              if goodPair ds es then (0 : Rat)
              else (exLam ds : Rat) * (exLam es : Rat) / tlcm ds es).sum).sum))
      ≤ ((((box 3 2).filter exP).map fun ds => (((box 3 2).filter exP).map fun es =>
          (exLam ds * exLam es).natAbs).sum).sum : Nat) :=
  maynard_S1_diag_W 3 2 exP [0, 2] exLam 2 1 N (by decide) rfl ex_hoff ex_hsq ex_hDW ex_hH

end MaynardHpw
end TwinPrimes
