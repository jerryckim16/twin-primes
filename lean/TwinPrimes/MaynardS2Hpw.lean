import TwinPrimes.MaynardS2

/-!
# Bad pairs do not contribute to `S₂^{(m)}`

The `S₂` analogue of `MaynardHpw.lean`. In the expansion (`maynard_S2_expand_W`)

  `S₂^{(m)} = ∑_{d,e ∈ Dk} λ_d λ_e #{N₀ ≤ n < N : n ≡ v₀ (W), pr(n+h_m), dᵢ,eᵢ ∣ n+hᵢ ∀ i}`

a pair `(d, e)` is *bad* when two of the moduli `[dᵢ, eᵢ]`, `[dⱼ, eⱼ]` (`i ≠ j`) share a factor.
Exactly as for `S₁`, such a pair has count `0`: a common divisor of `[dᵢ,eᵢ]` and `[dⱼ,eⱼ]`
divides `hᵢ − hⱼ`, hence (under `ShiftsCop hs W`) is coprime to itself, i.e. is `1`. The prime
condition plays no role here; the S₂ count is a sub-count of the S₁ one.

* `count_zero_of_not_good_S2`: a bad pair has S₂ count `0`;
* `count_zero_reduced_of_not_good`: the same for the reduced count of `maynard_S2_reduced`
  (the `(k−1)`-tuples with coordinate `m` erased), when the erased pair is bad;
* `maynard_S2_good_W`: `S₂^{(m)}` equals the double sum over good pairs only (no prime hypotheses);
* `maynard_S2_good_support`: combined with `maynard_S2_support`: only good pairs with
  `d_m = e_m = 1`;
* `maynard_S2_good_reduced`: combined with `maynard_S2_reduced`: only pairs with `d_m = e_m = 1`
  whose erased moduli `[dᵢ,eᵢ]` (`i ≠ m`) are pairwise coprime, which is exactly the hypothesis
  `hpw` of `maynard_S2_count_residue`;
* `maynard_S2_good_example` and the `decide` checks: a support with a bad pair having
  `d_m = e_m = 1` (`k = 3`, `h = (0,2,6)`, `W = 6`, `m = 0`, `d = (1,5,1)`, `e = (1,1,5)`).

NOT formalised: any analytic estimate (prime counts in APs, Bombieri–Vinogradov, the main term).
-/

namespace TwinPrimes
namespace MaynardS2Hpw

open MaynardHpw MaynardS2

/-- **Bad pairs have S₂ count `0`.** -/
theorem count_zero_of_not_good_S2 (hs ds es : List Nat) (W v0 N0 N m : Nat) (pr : Nat → Bool)
    (hd : ds.length = hs.length) (he : es.length = hs.length) (hH : ShiftsCop hs W)
    (hdW : ∀ d ∈ ds, Nat.gcd d W = 1) (heW : ∀ e ∈ es, Nat.gcd e W = 1)
    (hbad : goodPair ds es = false) :
    (List.range N).countP (s2Pred hs W v0 N0 m pr ds es) = 0 := by
  apply List.countP_eq_zero.mpr
  intro n _ hn
  have hnp : ¬ (List.zipWith Nat.lcm ds es).Pairwise Nat.Coprime := by
    intro h; simp [goodPair, h] at hbad
  apply hnp
  simp only [s2Pred, Bool.and_eq_true] at hn
  have ht : tupleDvd hs n (List.zipWith Nat.lcm ds es) = true := by
    rw [← tupleDvd_lcm hs ds es n hd he, hn.1.2, hn.2]; rfl
  exact pairwise_coprime_of_solvable (n := n) _ hs
    (by rw [List.length_zipWith, hd, he, Nat.min_self]) hH (lcm_entries_coprime hdW heW) ht

/-- `ShiftsCop` passes to the shifts with one coordinate erased. -/
theorem shiftsCop_eraseIdx {hs : List Nat} {W : Nat} (hH : ShiftsCop hs W) (m : Nat) :
    ShiftsCop (hs.eraseIdx m) W :=
  List.Pairwise.sublist (List.eraseIdx_sublist hs m) hH

/-- **Bad erased pairs have reduced count `0`.** If the `[dᵢ, eᵢ]`, `i ≠ m`, are not pairwise
coprime, the inner count of `maynard_S2_reduced` vanishes. -/
theorem count_zero_reduced_of_not_good (hs ds es : List Nat) (W v0 N0 N m : Nat)
    (pr : Nat → Bool) (hm : m < hs.length)
    (hd : ds.length = hs.length) (he : es.length = hs.length) (hH : ShiftsCop hs W)
    (hdW : ∀ d ∈ ds, Nat.gcd d W = 1) (heW : ∀ e ∈ es, Nat.gcd e W = 1)
    (hbad : goodPair (ds.eraseIdx m) (es.eraseIdx m) = false) :
    ((List.range N).countP fun n =>
      decide (N0 ≤ n) && n % W == v0 && pr (n + hs.getD m 0) &&
        tupleDvd (hs.eraseIdx m) n
          (List.zipWith Nat.lcm (ds.eraseIdx m) (es.eraseIdx m))) = 0 := by
  apply List.countP_eq_zero.mpr
  intro n _ hn
  have hnp : ¬ (List.zipWith Nat.lcm (ds.eraseIdx m) (es.eraseIdx m)).Pairwise Nat.Coprime := by
    intro h; simp [goodPair, h] at hbad
  apply hnp
  simp only [Bool.and_eq_true] at hn
  exact pairwise_coprime_of_solvable (n := n) _ (hs.eraseIdx m)
    (by simp [List.length_zipWith, List.length_eraseIdx, hd, he, hm])
    (shiftsCop_eraseIdx hH m)
    (lcm_entries_coprime (fun d hd' => hdW d (mem_eraseIdx_mem hd'))
      (fun e he' => heW e (mem_eraseIdx_mem he'))) hn.2

/-- **`S₂^{(m)}` over good pairs only** (no primality hypotheses):
`S₂^{(m)} = ∑_{d ∈ Dk} ∑_{e ∈ Dk, (d,e) good} λ_d λ_e #{…}`. -/
theorem maynard_S2_good_W (Dk : List (List Nat)) (hs : List Nat) (lam : List Nat → Int)
    (W v0 N0 N m : Nat) (pr : Nat → Bool)
    (hlen : ∀ ds ∈ Dk, ds.length = hs.length)
    (hDW : ∀ ds ∈ Dk, ∀ d ∈ ds, Nat.gcd d W = 1)
    (hH : ShiftsCop hs W) :
    ((List.range N).map fun n =>
        if N0 ≤ n ∧ n % W = v0 ∧ pr (n + hs.getD m 0) = true then
          mSieveSum Dk hs lam n * mSieveSum Dk hs lam n else 0).sum
      = (Dk.map fun ds => ((Dk.filter fun es => goodPair ds es).map fun es =>
          lam ds * lam es *
            (((List.range N).countP (s2Pred hs W v0 N0 m pr ds es) : Nat) : Int)).sum).sum := by
  rw [maynard_S2_expand_W]
  apply isum_congr; intro ds hds
  symm
  apply isum_filter_of_zero
  intro es hes hbad
  rw [count_zero_of_not_good_S2 hs ds es W v0 N0 N m pr (hlen ds hds) (hlen es hes) hH
    (hDW ds hds) (hDW es hes) hbad]
  simp

/-- **Good pairs with `d_m = e_m = 1`.** Under the hypotheses of `maynard_S2_support` plus
`ShiftsCop hs W` and entries coprime to `W`. -/
theorem maynard_S2_good_support (Dk : List (List Nat)) (hs : List Nat) (lam : List Nat → Int)
    (W v0 N0 N m : Nat) (pr : Nat → Bool)
    (hpr : ∀ p, pr p = true → IsPrime p) (hm : m < hs.length)
    (hlen : ∀ ds ∈ Dk, ds.length = hs.length)
    (hsmall : ∀ ds ∈ Dk, ds.getD m 1 < N0 + hs.getD m 0)
    (hDW : ∀ ds ∈ Dk, ∀ d ∈ ds, Nat.gcd d W = 1)
    (hH : ShiftsCop hs W) :
    ((List.range N).map fun n =>
        if N0 ≤ n ∧ n % W = v0 ∧ pr (n + hs.getD m 0) = true then
          mSieveSum Dk hs lam n * mSieveSum Dk hs lam n else 0).sum
      = ((Dk.filter fun ds => ds.getD m 1 == 1).map fun ds =>
          (((Dk.filter fun es => es.getD m 1 == 1).filter fun es => goodPair ds es).map fun es =>
            lam ds * lam es *
              (((List.range N).countP (s2Pred hs W v0 N0 m pr ds es) : Nat) : Int)).sum).sum := by
  rw [maynard_S2_support Dk hs lam W v0 N0 N m pr hpr hm hlen hsmall]
  apply isum_congr; intro ds hds
  have hdD := (List.mem_filter.mp hds).1
  symm
  apply isum_filter_of_zero
  intro es hes hbad
  have heD := (List.mem_filter.mp hes).1
  rw [count_zero_of_not_good_S2 hs ds es W v0 N0 N m pr (hlen ds hdD) (hlen es heD) hH
    (hDW ds hdD) (hDW es heD) hbad]
  simp

/-- **Reduced form over good erased pairs.** Under the hypotheses of `maynard_S2_reduced` plus
`ShiftsCop hs W` and entries coprime to `W`, `S₂^{(m)}` is the double sum over `d, e ∈ Dk` with
`d_m = e_m = 1` and `[dᵢ,eᵢ]` (`i ≠ m`) pairwise coprime of `λ_d λ_e` times the reduced count. -/
theorem maynard_S2_good_reduced (Dk : List (List Nat)) (hs : List Nat) (lam : List Nat → Int)
    (W v0 N0 N m : Nat) (pr : Nat → Bool)
    (hpr : ∀ p, pr p = true → IsPrime p) (hm : m < hs.length)
    (hlen : ∀ ds ∈ Dk, ds.length = hs.length)
    (hsmall : ∀ ds ∈ Dk, ds.getD m 1 < N0 + hs.getD m 0)
    (hDW : ∀ ds ∈ Dk, ∀ d ∈ ds, Nat.gcd d W = 1)
    (hH : ShiftsCop hs W) :
    ((List.range N).map fun n =>
        if N0 ≤ n ∧ n % W = v0 ∧ pr (n + hs.getD m 0) = true then
          mSieveSum Dk hs lam n * mSieveSum Dk hs lam n else 0).sum
      = ((Dk.filter fun ds => ds.getD m 1 == 1).map fun ds =>
          (((Dk.filter fun es => es.getD m 1 == 1).filter fun es =>
              goodPair (ds.eraseIdx m) (es.eraseIdx m)).map fun es =>
            lam ds * lam es * (((List.range N).countP fun n =>
              decide (N0 ≤ n) && n % W == v0 && pr (n + hs.getD m 0) &&
                tupleDvd (hs.eraseIdx m) n
                  (List.zipWith Nat.lcm (ds.eraseIdx m) (es.eraseIdx m)) : Nat) : Int)).sum).sum := by
  rw [maynard_S2_reduced Dk hs lam W v0 N0 N m pr hpr hm hlen hsmall]
  apply isum_congr; intro ds hds
  have hdD := (List.mem_filter.mp hds).1
  symm
  apply isum_filter_of_zero
  intro es hes hbad
  have heD := (List.mem_filter.mp hes).1
  rw [count_zero_reduced_of_not_good hs ds es W v0 N0 N m pr hm (hlen ds hdD) (hlen es heD) hH
    (hDW ds hdD) (hDW es heD) hbad]
  simp

/-! ## Non-vacuity: a bad pair with `d_m = e_m = 1` -/

/-- Support `{(1,1,1), (1,5,1), (1,1,5)}`, `h = (0,2,6)`, `W = 6`, `v₀ = 5`, `m = 0`. The pair
`((1,5,1), (1,1,5))` has moduli `(1,5,5)`: it is bad, survives the `d_m = 1` filter, and its
count is `0` since `5 ∣ n+2` and `5 ∣ n+6` are incompatible. -/
def exDk : List (List Nat) := [[1, 1, 1], [1, 5, 1], [1, 1, 5]]

def exLam (d : List Nat) : Int := if d = [1, 1, 1] then 2 else -1

/-- `ShiftsCop` holds although `ShiftsDvd` fails (`|2 − 6| = 4 ∤ 6`). -/
theorem ex_hH : ShiftsCop [0, 2, 6] 6 := by
  have h2 : ∀ x : Nat, Nat.gcd x 6 = 1 → Nat.Coprime x 2 := fun x hx =>
    Nat.Coprime.coprime_dvd_right (show 2 ∣ 6 by decide) (show Nat.Coprime x 6 from hx)
  have h6 : ∀ x : Nat, Nat.gcd x 6 = 1 → Nat.Coprime x 6 := fun x hx => hx
  have h4 : ∀ x : Nat, Nat.gcd x 6 = 1 → Nat.Coprime x 4 := fun x hx =>
    Nat.Coprime.mul_right (h2 x hx) (h2 x hx)
  simp only [ShiftsCop, List.pairwise_cons, List.mem_cons, List.not_mem_nil, or_false,
    forall_eq_or_imp, forall_eq, List.Pairwise.nil, and_true]
  exact ⟨⟨h2, h6⟩, h4, fun _ h => h.elim⟩

theorem ex_not_shiftsDvd : ¬ ShiftsDvd [0, 2, 6] 6 := by decide

/-- The bad pair lies in the filtered support (`d_m = e_m = 1`) and is bad, also after erasing `m`. -/
theorem ex_bad_pair :
    [1, 5, 1] ∈ exDk.filter (fun ds => ds.getD 0 1 == 1) ∧
    [1, 1, 5] ∈ exDk.filter (fun ds => ds.getD 0 1 == 1) ∧
    goodPair [1, 5, 1] [1, 1, 5] = false ∧
    goodPair ([1, 5, 1].eraseIdx 0) ([1, 1, 5].eraseIdx 0) = false := by decide

/-- Its S₂ count vanishes (here up to `N = 200`), as `count_zero_of_not_good_S2` predicts. -/
theorem ex_bad_count :
    (List.range 200).countP (s2Pred [0, 2, 6] 6 5 10 0 primeB [1, 5, 1] [1, 1, 5]) = 0 := by
  decide +kernel

/-- …whereas the good diagonal pair `((1,5,1),(1,5,1))` has a positive count, so the filter
removes a pair that would not trivially be zero for other reasons. -/
theorem ex_good_count_pos :
    0 < (List.range 200).countP (s2Pred [0, 2, 6] 6 5 10 0 primeB [1, 5, 1] [1, 5, 1]) := by
  decide +kernel

/-- `maynard_S2_good_reduced` instantiated with every hypothesis discharged (`N₀ = 10`, all `N`). -/
theorem maynard_S2_good_example (N : Nat) :
    ((List.range N).map fun n =>
        if 10 ≤ n ∧ n % 6 = 5 ∧ primeB (n + [0, 2, 6].getD 0 0) = true then
          mSieveSum exDk [0, 2, 6] exLam n * mSieveSum exDk [0, 2, 6] exLam n else 0).sum
      = ((exDk.filter fun ds => ds.getD 0 1 == 1).map fun ds =>
          (((exDk.filter fun es => es.getD 0 1 == 1).filter fun es =>
              goodPair (ds.eraseIdx 0) (es.eraseIdx 0)).map fun es =>
            exLam ds * exLam es * (((List.range N).countP fun n =>
              decide (10 ≤ n) && n % 6 == 5 && primeB (n + [0, 2, 6].getD 0 0) &&
                tupleDvd ([0, 2, 6].eraseIdx 0) n
                  (List.zipWith Nat.lcm (ds.eraseIdx 0) (es.eraseIdx 0)) : Nat) : Int)).sum).sum :=
  maynard_S2_good_reduced exDk [0, 2, 6] exLam 6 5 10 N 0 primeB primeB_sound (by decide)
    (by decide) (by decide) (by decide) ex_hH

/-- The good-pair filter removes exactly the two bad pairs: 9 pairs before, 7 after. -/
theorem ex_filter_sizes :
    ((exDk.filter fun ds => ds.getD 0 1 == 1).map fun ds =>
        (((exDk.filter fun es => es.getD 0 1 == 1).filter fun es =>
          goodPair (ds.eraseIdx 0) (es.eraseIdx 0)).length)).sum = 7 := by decide

/-- Numerical check at `N = 120` of `maynard_S2_good_support` (both sides evaluated). -/
theorem maynard_S2_good_example_eval :
    ((List.range 120).map fun n =>
        if 10 ≤ n ∧ n % 6 = 5 ∧ primeB (n + [0, 2, 6].getD 0 0) = true then
          mSieveSum exDk [0, 2, 6] exLam n * mSieveSum exDk [0, 2, 6] exLam n else 0).sum
      = ((exDk.filter fun ds => ds.getD 0 1 == 1).map fun ds =>
          (((exDk.filter fun es => es.getD 0 1 == 1).filter fun es => goodPair ds es).map fun es =>
            exLam ds * exLam es *
              (((List.range 120).countP (s2Pred [0, 2, 6] 6 5 10 0 primeB ds es) : Nat) : Int)).sum).sum := by
  decide +kernel

end MaynardS2Hpw
end TwinPrimes
