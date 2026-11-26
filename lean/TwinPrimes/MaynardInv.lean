import TwinPrimes.SelbergOpt

/-!
# Möbius inversion over `k`-tuples and Maynard's change of variables `λ ↔ y`

Motivation: Maynard, *Small gaps between primes* (Ann. of Math. 2015, arXiv:1311.4600),
Lemma 5.1 / eq. (5.8): for weights `λ_{d₁,…,d_k}` supported on squarefree tuples, put
`y_r = ∏ μ(rᵢ) φ(rᵢ) ∑_{rᵢ ∣ dᵢ ∀i} λ_d / ∏ dᵢ` (as printed in Lemma 5.1); then
`λ_d = μ(∏ dᵢ) ∏ dᵢ ∑_{dᵢ ∣ rᵢ ∀i} y_r / ∏ φ(rᵢ)`.
This file proves the finite, combinatorial core of that statement in core Lean (no Mathlib),
over `Rat` (core `Init.Data.Rat`), with list-based sums.

Setting: tuples are `List Nat`; the ambient finite set is the box `box R k = {1,…,R}^k`
(any finite support lies in some box, and the box is closed under componentwise divisors);
`tdvd r d` is componentwise divisibility; `tmuq r d = ∏ᵢ μ(dᵢ / rᵢ)`; `μ` is `TwinPrimes.mu`.

Proved (all `R`, all `k`, no hypotheses beyond membership in the box):
* `mob1_lower`, `mob1_upper`: 1-d relative Möbius sums
  `∑_{x ≤ R, a ∣ x ∣ c} μ(x/a) = [a = c] = ∑_{x ≤ R, a ∣ x ∣ c} μ(c/x)` for `1 ≤ a, c ≤ R`
  (from `mu_divisor_sum`);
* `tuple_mobius_lower`, `tuple_mobius_upper`: the tuple Möbius sums
  `∑_{d ∈ box, r ∣ d ∣ e} ∏ μ(dᵢ/rᵢ) = [r = e] = ∑_{d ∈ box, r ∣ d ∣ e} ∏ μ(eᵢ/dᵢ)`
  (in particular `r = (1,…,1)` gives `∑_{d ∣ e} μ(d) = [e = 1]`);
* `mobInv_upSum`, `upSum_mobInv`: **Möbius inversion over `k`-tuples, both directions**: with
  `(U f)(r) = ∑_{r ∣ d} f(d)` and `(M F)(r) = ∑_{r ∣ d} μ(d/r) F(d)` (sums over the box),
  `M (U f) = f` and `U (M F) = F` on the box.

Maynard's normalisation (`maynardY`, `maynardLam`; `μ(r)` is taken as `∏ᵢ μ(rᵢ)`, which equals
`μ(∏ rᵢ)` for pairwise coprime entries as on Maynard's support — proved in `MuTuple.lean`, `tmu_eq_mu_prod`):
* `maynard_lam_of_y`, `maynard_y_of_lam`: both round trips `λ ↦ y ↦ λ`, `y ↦ λ ↦ y` hold on the
  box whenever every tuple `e` in the support satisfies the sign identity `SignOK e`:
  `∏ μ(dᵢ) ∏ μ(rᵢ) = ∏ μ(rᵢ/dᵢ)` for all `d ∣ r ∣ e`;
* `signOK_of_entries`: `SignOK e` follows from the 1-d identity `MuSign c`
  (`μ(a) μ(x) = μ(x/a)` for `a ∣ x ∣ c`) at each entry; `maynard_lam_of_y_sqfree`,
  `maynard_y_of_lam_sqfree`: the round trips for squarefree-supported weights (`μ(eᵢ) ≠ 0`),
  assuming `MuSign c` for squarefree `c ≤ R`;
* `muSignCheck_31` (`decide`): `MuSign c` for every squarefree `c ≤ 30`; hence
  `maynard_inversion_R30`, `maynard_inversion_R30'`: Maynard's inversion, both directions,
  **unconditionally** for squarefree-supported weights on `{1,…,R}^k`, `R ≤ 30`, every `k`;
* `tuple_mobius_example`, `maynard_inversion_example`, `maynard_inversion_needs_sqfree`:
  concrete `k = 2` checks by kernel `decide` (the last shows the squarefree hypothesis is needed).

NOT proved here: the general 1-d sign identity `MuSign c` for every squarefree `c` (proved in
`TwinPrimes/MuMult.lean`: `muSign_of_sqfree`, giving `maynard_lam_of_y_sqfree_all` /
`maynard_y_of_lam_sqfree_all` for every `R`); the identity `∏ μ(rᵢ) = μ(∏ rᵢ)`; the restriction of the support to
`∏ dᵢ < R`, `(dᵢ, W) = 1` (any such support sits inside a box, so the box statements apply to it,
but the size/coprimality bookkeeping of Maynard's Lemma 5.1 is not formalised); the remaining
parts of Lemma 5.1 (the diagonalisation of the `S₁` quadratic form in terms of `y`, the bound
`y_max ≪ λ_max`-type estimates) and anything analytic.
-/

namespace TwinPrimes
namespace MaynardInv

open Gauss SelbergOpt

/-! ## Rational list sums -/

theorem rsum_congr {α} {f g : α → Rat} {l : List α} (h : ∀ x ∈ l, f x = g x) :
    (l.map f).sum = (l.map g).sum := by rw [List.map_congr_left h]

theorem rsum_zero {α} : ∀ l : List α, (l.map fun _ => (0 : Rat)).sum = 0
  | [] => rfl
  | _ :: l => by simp only [List.map_cons, List.sum_cons, rsum_zero l, Rat.add_zero]

theorem rsum_mul_left {α} (c : Rat) (f : α → Rat) : ∀ l : List α,
    (l.map fun x => c * f x).sum = c * (l.map f).sum
  | [] => by simp
  | x :: l => by simp only [List.map_cons, List.sum_cons, rsum_mul_left c f l, Rat.mul_add]

theorem rsum_mul_right {α} (c : Rat) (f : α → Rat) (l : List α) :
    (l.map fun x => f x * c).sum = (l.map f).sum * c := by
  rw [Rat.mul_comm, ← rsum_mul_left]; exact rsum_congr fun x _ => Rat.mul_comm _ _

theorem rsum_add {α} (f g : α → Rat) : ∀ l : List α,
    (l.map fun x => f x + g x).sum = (l.map f).sum + (l.map g).sum
  | [] => by simp [Rat.add_zero]
  | x :: l => by
    simp only [List.map_cons, List.sum_cons, rsum_add f g l]
    grind

theorem rsum_comm {α β} (f : α → β → Rat) (l₁ : List α) : ∀ l₂ : List β,
    (l₁.map fun a => (l₂.map fun b => f a b).sum).sum
      = (l₂.map fun b => (l₁.map fun a => f a b).sum).sum
  | [] => by simp [rsum_zero]
  | b :: l₂ => by
    simp only [List.map_cons, List.sum_cons]
    rw [rsum_add, rsum_comm f l₁ l₂]

theorem rsum_flatMap {α β} (g : β → Rat) (f : α → List β) : ∀ l : List α,
    ((l.flatMap f).map g).sum = (l.map fun a => ((f a).map g).sum).sum
  | [] => rfl
  | a :: l => by
    simp only [List.flatMap_cons, List.map_append, List.sum_append, List.map_cons,
      List.sum_cons, rsum_flatMap g f l]

theorem rsum_cast {α} (f : α → Int) : ∀ l : List α,
    (((l.map f).sum : Int) : Rat) = (l.map fun x => (f x : Rat)).sum
  | [] => rfl
  | x :: l => by simp only [List.map_cons, List.sum_cons, Rat.intCast_add, rsum_cast f l]

theorem rsum_ne_zero {α} {f : α → Rat} {l : List α} (h : (l.map f).sum ≠ 0) :
    ∃ x ∈ l, f x ≠ 0 := by
  apply Classical.byContradiction; intro hn
  apply h
  rw [rsum_congr (g := fun _ => 0), rsum_zero]
  intro x hx
  apply Classical.byContradiction; intro hx'
  exact hn ⟨x, hx, hx'⟩

/-- `∑_{x < N} [x = a] c = [a < N] c`. -/
theorem rsum_delta_range (a : Nat) (c : Rat) : ∀ N : Nat,
    ((List.range N).map fun x => if x = a then c else 0).sum = if a < N then c else 0
  | 0 => by simp
  | N + 1 => by
    rw [List.range_succ, List.map_append, List.sum_append, rsum_delta_range a c N]
    by_cases h : a = N
    · subst h; simp [Rat.add_zero, Rat.zero_add]
    · have : ¬ N = a := fun e => h e.symm
      by_cases h' : a < N
      · simp [h', this, show a < N + 1 by omega, Rat.add_zero]
      · simp [h', this, show ¬ a < N + 1 by omega, Rat.add_zero]

theorem rsum_range_extend (N M : Nat) (f : Nat → Rat) (hNM : N ≤ M)
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
      simp [h M (by omega) (by omega), Rat.add_zero]

/-- Reindexing multiples: `∑_{x < r N, r ∣ x} g x = ∑_{m < N} g (r m)` for `r ≥ 1`. -/
theorem rsum_multiples (r : Nat) (hr : 1 ≤ r) (g : Nat → Rat) : ∀ N : Nat,
    ((List.range (r * N)).map fun x => if x % r = 0 then g x else 0).sum
      = ((List.range N).map fun m => g (r * m)).sum
  | 0 => by simp
  | N + 1 => by
    rw [Nat.mul_succ, List.range_add, List.map_append, List.sum_append, rsum_multiples r hr g N,
      List.range_succ, List.map_append, List.sum_append]
    congr 1
    obtain ⟨r', rfl⟩ : ∃ r', r = r' + 1 := ⟨r - 1, by omega⟩
    rw [List.range_succ_eq_map, List.map_cons, List.map_cons, List.sum_cons]
    simp only [Nat.add_zero, Nat.mul_mod_right, ↓reduceIte, List.map_map, List.map_cons,
      List.map_nil, List.sum_cons, List.sum_nil, Rat.add_zero]
    rw [rsum_congr (g := fun _ => 0), rsum_zero, Rat.add_zero]
    intro j hj
    have hj := List.mem_range.mp hj
    have : (j + 1) % (r' + 1) ≠ 0 := by rw [Nat.mod_eq_of_lt (by omega)]; omega
    simp [this]

/-! ## One-dimensional relative Möbius sums -/

/-- The index range `1, …, R`. -/
def rng (R : Nat) : List Nat := (List.range R).map (· + 1)

theorem mem_rng {R x : Nat} : x ∈ rng R ↔ 1 ≤ x ∧ x ≤ R := mem_range_succ_map

theorem rsum_rng (R : Nat) (f : Nat → Rat) (h0 : f 0 = 0) :
    ((rng R).map f).sum = ((List.range (R + 1)).map f).sum := by
  rw [List.range_succ_eq_map, List.map_cons, List.sum_cons, h0, Rat.zero_add, List.map_map]
  unfold rng; rw [List.map_map]

/-- `∑_{m ∣ n} μ(m) = [n = 1]`, as a rational sum over `m ≤ n`. -/
theorem mu_sum_rat (n : Nat) (hn : 1 ≤ n) :
    ((List.range (n + 1)).map fun m => if m ≠ 0 ∧ n % m = 0 then (mu m : Rat) else 0).sum
      = if n = 1 then 1 else 0 := by
  have h := mu_divisor_sum n hn
  rw [isum_filter] at h
  have h2 := congrArg (fun z : Int => (z : Rat)) h
  simp only [rsum_cast] at h2
  rw [show (if n = 1 then (1 : Rat) else 0) = (((if n = 1 then 1 else 0 : Int)) : Rat) by
    split <;> rfl, ← h2]
  apply rsum_congr; intro m _
  by_cases hm : m = 0
  · subst hm; simp
  · by_cases hd : n % m = 0 <;> simp [hm, hd]

/-- Divisor complement: `∑_{m ∣ n} g(n/m) = ∑_{m ∣ n} g(m)` for `n ≥ 1`. -/
theorem rsum_div_compl (n : Nat) (hn : 1 ≤ n) (g : Nat → Rat) :
    ((List.range (n + 1)).map fun m => if m ≠ 0 ∧ n % m = 0 then g (n / m) else 0).sum
      = ((List.range (n + 1)).map fun m => if m ≠ 0 ∧ n % m = 0 then g m else 0).sum := by
  have key : ∀ m j : Nat, (m ≠ 0 ∧ n % m = 0 ∧ j = n / m) ↔ (j ≠ 0 ∧ n % j = 0 ∧ m = n / j) := by
    intro m j
    constructor
    · rintro ⟨hm, hmn, rfl⟩
      have hdm : m ∣ n := Nat.dvd_of_mod_eq_zero hmn
      have he : n / m * m = n := Nat.div_mul_cancel hdm
      have hj : n / m ≠ 0 := by intro h0; rw [h0, Nat.zero_mul] at he; omega
      refine ⟨hj, Nat.mod_eq_zero_of_dvd ⟨m, he.symm⟩, ?_⟩
      exact (Nat.div_eq_of_eq_mul_left (Nat.pos_of_ne_zero hj) (by rw [Nat.mul_comm]; exact he.symm)).symm
    · rintro ⟨hj, hjn, rfl⟩
      have hdj : j ∣ n := Nat.dvd_of_mod_eq_zero hjn
      have he : n / j * j = n := Nat.div_mul_cancel hdj
      have hm : n / j ≠ 0 := by intro h0; rw [h0, Nat.zero_mul] at he; omega
      refine ⟨hm, Nat.mod_eq_zero_of_dvd ⟨j, he.symm⟩, ?_⟩
      exact (Nat.div_eq_of_eq_mul_left (Nat.pos_of_ne_zero hm) (by rw [Nat.mul_comm]; exact he.symm)).symm
  have hle : ∀ m, m ≠ 0 → n / m < n + 1 := fun m _ =>
    Nat.lt_succ_of_le (Nat.div_le_self n m)
  calc ((List.range (n + 1)).map fun m => if m ≠ 0 ∧ n % m = 0 then g (n / m) else 0).sum
      = ((List.range (n + 1)).map fun m => ((List.range (n + 1)).map fun j =>
          if m ≠ 0 ∧ n % m = 0 ∧ j = n / m then g j else 0).sum).sum := by
        apply rsum_congr; intro m _
        by_cases hc : m ≠ 0 ∧ n % m = 0
        · rw [ite_eq_left hc]
          have := rsum_delta_range (n / m) (g (n / m)) (n + 1)
          rw [ite_eq_left (hle m hc.1)] at this
          rw [← this]; apply rsum_congr; intro j _
          by_cases hj : j = n / m
          · subst hj; simp [hc]
          · simp [hj]
        · rw [ite_eq_right hc, rsum_congr (g := fun _ => 0), rsum_zero]
          intro j _; rw [ite_eq_right (fun h => hc ⟨h.1, h.2.1⟩)]
    _ = ((List.range (n + 1)).map fun j => ((List.range (n + 1)).map fun m =>
          if m ≠ 0 ∧ n % m = 0 ∧ j = n / m then g j else 0).sum).sum := rsum_comm _ _ _
    _ = _ := by
        apply rsum_congr; intro j _
        rw [rsum_congr (g := fun m => if j ≠ 0 ∧ n % j = 0 ∧ m = n / j then g j else 0)
          (fun m _ => by simp only [key m j])]
        by_cases hc : j ≠ 0 ∧ n % j = 0
        · rw [ite_eq_left hc]
          have := rsum_delta_range (n / j) (g j) (n + 1)
          rw [ite_eq_left (hle j hc.1)] at this
          refine Eq.trans ?_ this; apply rsum_congr; intro m _
          by_cases hm : m = n / j
          · simp [hc, hm]
          · simp [hm]
        · rw [ite_eq_right hc, rsum_congr (g := fun _ => 0), rsum_zero]
          intro m _; rw [ite_eq_right (fun h => hc ⟨h.1, h.2.1⟩)]

/-- Common reduction: for `1 ≤ a, c ≤ R` and `c = a n`,
`∑_{x ≤ R, a ∣ x ∣ c} G(x) = ∑_{m ∣ n} G(a m)`. -/
theorem rsum_between (R a c n : Nat) (ha : a ∈ rng R) (hc : c ∈ rng R) (hn : c = a * n)
    (G : Nat → Rat) :
    ((rng R).map fun x => if x % a = 0 ∧ c % x = 0 then G x else 0).sum
      = ((List.range (n + 1)).map fun m => if m ≠ 0 ∧ n % m = 0 then G (a * m) else 0).sum := by
  obtain ⟨ha1, haR⟩ := mem_rng.mp ha
  obtain ⟨hc1, hcR⟩ := mem_rng.mp hc
  have hn1 : 1 ≤ n := by
    cases n with
    | zero => rw [Nat.mul_zero] at hn; omega
    | succ n => omega
  have hcx : ∀ x, c < x → c % x ≠ 0 := fun x hx => by rw [Nat.mod_eq_of_lt hx]; omega
  rw [rsum_rng R _ (by simp; omega),
    rsum_range_extend (c + 1) (R + 1) _ (by omega)
      (fun v hv _ => by rw [ite_eq_right (fun h => hcx v (by omega) h.2)]),
    ← rsum_range_extend (c + 1) (a * (n + 1)) _ (by rw [Nat.mul_succ]; omega)
      (fun v hv _ => by rw [ite_eq_right (fun h => hcx v (by omega) h.2)])]
  rw [rsum_congr (g := fun x => if x % a = 0 then (if c % x = 0 then G x else 0) else 0)
    (fun x _ => by by_cases h1 : x % a = 0 <;> by_cases h2 : c % x = 0 <;> simp [h1, h2])]
  rw [rsum_multiples a ha1 _ (n + 1)]
  apply rsum_congr; intro m _
  have hmod : c % (a * m) = a * (n % m) := by rw [hn, Nat.mul_mod_mul_left]
  by_cases hm : m = 0
  · subst hm
    rw [Nat.mul_zero, Nat.mod_zero]; simp; omega
  · have : (c % (a * m) = 0) ↔ (n % m = 0) := by
      rw [hmod]; constructor
      · intro h; rcases Nat.mul_eq_zero.mp h with h | h <;> omega
      · intro h; rw [h, Nat.mul_zero]
    by_cases h : n % m = 0
    · simp [hm, h, this.mpr h]
    · rw [ite_eq_right (fun e => h (this.mp e)), ite_eq_right (fun e : m ≠ 0 ∧ n % m = 0 => h e.2)]

/-- **1-d relative Möbius sum (lower form).** For `1 ≤ a, c ≤ R`:
`∑_{x ≤ R, a ∣ x ∣ c} μ(x / a) = [a = c]`. -/
theorem mob1_lower (R a c : Nat) (ha : a ∈ rng R) (hc : c ∈ rng R) :
    ((rng R).map fun x => if x % a = 0 ∧ c % x = 0 then (mu (x / a) : Rat) else 0).sum
      = if a = c then 1 else 0 := by
  have ha1 := (mem_rng.mp ha).1
  by_cases hac : c % a = 0
  · obtain ⟨n, hn⟩ := Nat.dvd_of_mod_eq_zero hac
    have hn1 : 1 ≤ n := by
      cases n with
      | zero => have := (mem_rng.mp hc).1; rw [hn, Nat.mul_zero] at this; omega
      | succ n => omega
    rw [rsum_between R a c n ha hc hn]
    rw [rsum_congr (g := fun m => if m ≠ 0 ∧ n % m = 0 then (mu m : Rat) else 0)
      (fun m _ => by rw [Nat.mul_div_cancel_left m (by omega)])]
    rw [mu_sum_rat n hn1]
    have : (n = 1) ↔ (a = c) := by
      rw [hn]; constructor
      · intro h; rw [h, Nat.mul_one]
      · intro h
        have : a * 1 = a * n := by rw [Nat.mul_one]; exact h
        exact (Nat.eq_of_mul_eq_mul_left (by omega) this).symm
    by_cases h : n = 1
    · rw [ite_eq_left h, ite_eq_left (this.mp h)]
    · rw [ite_eq_right h, ite_eq_right (fun e => h (this.mpr e))]
  · rw [ite_eq_right (fun e => hac (by rw [e]; exact Nat.mod_self c)), rsum_congr (g := fun _ => 0),
      rsum_zero]
    intro x _
    rw [ite_eq_right]
    rintro ⟨h1, h2⟩
    exact hac (Nat.mod_eq_zero_of_dvd (Nat.dvd_trans (Nat.dvd_of_mod_eq_zero h1)
      (Nat.dvd_of_mod_eq_zero h2)))

/-- **1-d relative Möbius sum (upper form).** For `1 ≤ a, c ≤ R`:
`∑_{x ≤ R, a ∣ x ∣ c} μ(c / x) = [a = c]`. -/
theorem mob1_upper (R a c : Nat) (ha : a ∈ rng R) (hc : c ∈ rng R) :
    ((rng R).map fun x => if x % a = 0 ∧ c % x = 0 then (mu (c / x) : Rat) else 0).sum
      = if a = c then 1 else 0 := by
  have ha1 := (mem_rng.mp ha).1
  by_cases hac : c % a = 0
  · obtain ⟨n, hn⟩ := Nat.dvd_of_mod_eq_zero hac
    have hn1 : 1 ≤ n := by
      cases n with
      | zero => have := (mem_rng.mp hc).1; rw [hn, Nat.mul_zero] at this; omega
      | succ n => omega
    rw [rsum_between R a c n ha hc hn]
    rw [rsum_congr (g := fun m => if m ≠ 0 ∧ n % m = 0 then (mu (n / m) : Rat) else 0)
      (fun m _ => by rw [hn, Nat.mul_div_mul_left n m (by omega)])]
    rw [rsum_div_compl n hn1 (fun m => (mu m : Rat)), mu_sum_rat n hn1]
    have : (n = 1) ↔ (a = c) := by
      rw [hn]; constructor
      · intro h; rw [h, Nat.mul_one]
      · intro h
        have : a * 1 = a * n := by rw [Nat.mul_one]; exact h
        exact (Nat.eq_of_mul_eq_mul_left (by omega) this).symm
    by_cases h : n = 1
    · rw [ite_eq_left h, ite_eq_left (this.mp h)]
    · rw [ite_eq_right h, ite_eq_right (fun e => h (this.mpr e))]
  · rw [ite_eq_right (fun e => hac (by rw [e]; exact Nat.mod_self c)), rsum_congr (g := fun _ => 0),
      rsum_zero]
    intro x _
    rw [ite_eq_right]
    rintro ⟨h1, h2⟩
    exact hac (Nat.mod_eq_zero_of_dvd (Nat.dvd_trans (Nat.dvd_of_mod_eq_zero h1)
      (Nat.dvd_of_mod_eq_zero h2)))

/-! ## Tuples: the box `{1,…,R}^k`, componentwise divisibility, tuple Möbius sums -/

/-- All `k`-tuples (as lists) with entries in `{1, …, R}`. -/
def box (R : Nat) : Nat → List (List Nat)
  | 0 => [[]]
  | k + 1 => (rng R).flatMap fun x => (box R k).map (x :: ·)

/-- Componentwise divisibility `r ∣ d` (`r_i ∣ d_i` for all `i`, same length). -/
def tdvd : List Nat → List Nat → Bool
  | [], [] => true
  | a :: r, b :: d => b % a == 0 && tdvd r d
  | _, _ => false

/-- `μ(d / r) := ∏_i μ(d_i / r_i)` (rational-valued). -/
def tmuq : List Nat → List Nat → Rat
  | a :: r, b :: d => (mu (b / a) : Rat) * tmuq r d
  | _, _ => 1

theorem box_zero (R : Nat) : box R 0 = [[]] := rfl

theorem mem_box_succ {R k : Nat} {d : List Nat} (h : d ∈ box R (k + 1)) :
    ∃ x t, d = x :: t ∧ x ∈ rng R ∧ t ∈ box R k := by
  simp only [box, List.mem_flatMap, List.mem_map] at h
  obtain ⟨x, hx, t, ht, rfl⟩ := h
  exact ⟨x, t, rfl, hx, ht⟩

theorem mem_box_entries {R : Nat} : ∀ {k : Nat} {d : List Nat}, d ∈ box R k →
    d.length = k ∧ ∀ x ∈ d, x ∈ rng R
  | 0, d, h => by
    rw [box_zero, List.mem_singleton] at h; subst h; simp
  | k + 1, d, h => by
    obtain ⟨x, t, rfl, hx, ht⟩ := mem_box_succ h
    obtain ⟨h1, h2⟩ := mem_box_entries ht
    refine ⟨by simp [h1], fun y hy => ?_⟩
    rcases List.mem_cons.mp hy with rfl | hy
    · exact hx
    · exact h2 y hy

theorem rsum_box_succ (R k : Nat) (h : List Nat → Rat) :
    ((box R (k + 1)).map h).sum
      = ((rng R).map fun x => ((box R k).map fun t => h (x :: t)).sum).sum := by
  simp only [box]; rw [rsum_flatMap]
  apply rsum_congr; intro x _; rw [List.map_map]; rfl

/-- `∑_{x ≤ R} [x = a] c = c` for `a ∈ {1,…,R}`. -/
theorem rsum_delta_rng (R a : Nat) (ha : a ∈ rng R) (c : Rat) :
    ((rng R).map fun x => if x = a then c else 0).sum = c := by
  obtain ⟨h1, h2⟩ := mem_rng.mp ha
  rw [rsum_rng R _ (by rw [ite_eq_right (by omega)]), rsum_delta_range,
    ite_eq_left (by omega)]

/-- Kronecker delta on the box: `∑_{e ∈ box} [r = e] f(e) = f(r)` for `r ∈ box`. -/
theorem rsum_delta_box (R : Nat) : ∀ (k : Nat) (f : List Nat → Rat) (r : List Nat),
    r ∈ box R k → ((box R k).map fun e => if r = e then f e else 0).sum = f r
  | 0, f, r, hr => by
    rw [box_zero, List.mem_singleton] at hr; subst hr
    simp [box_zero, Rat.add_zero]
  | k + 1, f, r, hr => by
    obtain ⟨a, r', rfl, ha, hr'⟩ := mem_box_succ hr
    rw [rsum_box_succ]
    rw [rsum_congr (g := fun x => if x = a then f (a :: r') else 0)]
    · exact rsum_delta_rng R a ha _
    intro x _
    by_cases hx : x = a
    · subst hx
      rw [ite_eq_left rfl, ← rsum_delta_box R k (fun t => f (x :: t)) r' hr']
      apply rsum_congr; intro t _
      by_cases ht : r' = t
      · subst ht; simp
      · simp [ht]
    · rw [ite_eq_right hx, rsum_congr (g := fun _ => 0), rsum_zero]
      intro t _
      rw [ite_eq_right]
      intro e; exact hx (List.cons.inj e).1.symm

/-- Product of a three-index kernel along tuples. -/
def tprod3 (g : Nat → Nat → Nat → Rat) : List Nat → List Nat → List Nat → Rat
  | a :: r, x :: d, c :: e => g a x c * tprod3 g r d e
  | _, _, _ => 1

/-- Tensorisation: if the 1-d kernel sums to `[a = c]`, so does its tuple product. -/
theorem tprod3_sum (R : Nat) (g : Nat → Nat → Nat → Rat)
    (hg : ∀ a c, a ∈ rng R → c ∈ rng R → ((rng R).map fun x => g a x c).sum
      = if a = c then 1 else 0) :
    ∀ (k : Nat) (r e : List Nat), r ∈ box R k → e ∈ box R k →
      ((box R k).map fun d => tprod3 g r d e).sum = if r = e then 1 else 0
  | 0, r, e, hr, he => by
    rw [box_zero, List.mem_singleton] at hr he; subst hr; subst he
    simp [box_zero, tprod3, Rat.add_zero]
  | k + 1, r, e, hr, he => by
    obtain ⟨a, r', rfl, ha, hr'⟩ := mem_box_succ hr
    obtain ⟨c, e', rfl, hc, he'⟩ := mem_box_succ he
    rw [rsum_box_succ]
    simp only [tprod3]
    rw [rsum_congr (g := fun x => g a x c * (if r' = e' then 1 else 0))
      (fun x _ => by rw [rsum_mul_left, tprod3_sum R g hg k r' e' hr' he']),
      rsum_mul_right, hg a c ha hc]
    by_cases h1 : a = c <;> by_cases h2 : r' = e' <;> simp [h1, h2]

/-- The 1-d kernel of the lower Möbius sum. -/
def gLow (a x c : Nat) : Rat := if x % a = 0 ∧ c % x = 0 then (mu (x / a) : Rat) else 0

/-- The 1-d kernel of the upper Möbius sum. -/
def gUp (a x c : Nat) : Rat := if x % a = 0 ∧ c % x = 0 then (mu (c / x) : Rat) else 0

theorem bridge_low : ∀ r d e : List Nat, r.length = d.length → d.length = e.length →
    (if (tdvd r d && tdvd d e) = true then tmuq r d else 0) = tprod3 gLow r d e
  | [], [], [], _, _ => by simp [tdvd, tprod3, tmuq]
  | a :: r, x :: d, c :: e, h1, h2 => by
    have ih := bridge_low r d e (by simpa using h1) (by simpa using h2)
    simp only [tdvd, tmuq, tprod3, gLow, ← ih]
    simp only [Bool.and_eq_true, beq_iff_eq]
    by_cases p1 : x % a = 0 <;> by_cases p2 : c % x = 0 <;>
      by_cases q1 : tdvd r d = true <;> by_cases q2 : tdvd d e = true <;> simp [p1, p2, q1, q2]
  | [], _ :: _, _, h1, _ => by simp at h1
  | _ :: _, [], _, h1, _ => by simp at h1
  | [], [], _ :: _, _, h2 => by simp at h2
  | _ :: _, _ :: _, [], _, h2 => by simp at h2

theorem bridge_up : ∀ r d e : List Nat, r.length = d.length → d.length = e.length →
    (if (tdvd r d && tdvd d e) = true then tmuq d e else 0) = tprod3 gUp r d e
  | [], [], [], _, _ => by simp [tdvd, tprod3, tmuq]
  | a :: r, x :: d, c :: e, h1, h2 => by
    have ih := bridge_up r d e (by simpa using h1) (by simpa using h2)
    simp only [tdvd, tmuq, tprod3, gUp, ← ih]
    simp only [Bool.and_eq_true, beq_iff_eq]
    by_cases p1 : x % a = 0 <;> by_cases p2 : c % x = 0 <;>
      by_cases q1 : tdvd r d = true <;> by_cases q2 : tdvd d e = true <;> simp [p1, p2, q1, q2]
  | [], _ :: _, _, h1, _ => by simp at h1
  | _ :: _, [], _, h1, _ => by simp at h1
  | [], [], _ :: _, _, h2 => by simp at h2
  | _ :: _, _ :: _, [], _, h2 => by simp at h2

/-- **Tuple Möbius sum (lower form).** For `r, e ∈ {1,…,R}^k`:
`∑_{d ∈ {1,…,R}^k, r ∣ d ∣ e} ∏_i μ(d_i / r_i) = [r = e]`. -/
theorem tuple_mobius_lower (R k : Nat) (r e : List Nat) (hr : r ∈ box R k) (he : e ∈ box R k) :
    ((box R k).map fun d => if (tdvd r d && tdvd d e) = true then tmuq r d else 0).sum
      = if r = e then 1 else 0 := by
  rw [← tprod3_sum R gLow (fun a c ha hc => mob1_lower R a c ha hc) k r e hr he]
  apply rsum_congr; intro d hd
  exact bridge_low r d e (by rw [(mem_box_entries hr).1, (mem_box_entries hd).1])
    (by rw [(mem_box_entries he).1, (mem_box_entries hd).1])

/-- **Tuple Möbius sum (upper form).** For `r, e ∈ {1,…,R}^k`:
`∑_{d ∈ {1,…,R}^k, r ∣ d ∣ e} ∏_i μ(e_i / d_i) = [r = e]`. -/
theorem tuple_mobius_upper (R k : Nat) (r e : List Nat) (hr : r ∈ box R k) (he : e ∈ box R k) :
    ((box R k).map fun d => if (tdvd r d && tdvd d e) = true then tmuq d e else 0).sum
      = if r = e then 1 else 0 := by
  rw [← tprod3_sum R gUp (fun a c ha hc => mob1_upper R a c ha hc) k r e hr he]
  apply rsum_congr; intro d hd
  exact bridge_up r d e (by rw [(mem_box_entries hr).1, (mem_box_entries hd).1])
    (by rw [(mem_box_entries he).1, (mem_box_entries hd).1])

/-! ## Möbius inversion over the box -/

/-- Upward divisor sum `(U f)(r) = ∑_{d ∈ {1,…,R}^k, r ∣ d} f(d)`. -/
def upSum (R k : Nat) (f : List Nat → Rat) (r : List Nat) : Rat :=
  ((box R k).map fun d => if tdvd r d = true then f d else 0).sum

/-- Möbius inverse `(M F)(r) = ∑_{d ∈ {1,…,R}^k, r ∣ d} μ(d / r) F(d)`,
`μ(d / r) = ∏_i μ(d_i / r_i)`. -/
def mobInv (R k : Nat) (F : List Nat → Rat) (r : List Nat) : Rat :=
  ((box R k).map fun d => if tdvd r d = true then tmuq r d * F d else 0).sum

theorem collapse (R k : Nat) (K : List Nat → List Nat → Rat) (f : List Nat → Rat)
    (r : List Nat) (hr : r ∈ box R k)
    (hK : ∀ e ∈ box R k, ((box R k).map fun d => K d e).sum = if r = e then 1 else 0) :
    ((box R k).map fun d => ((box R k).map fun e => K d e * f e).sum).sum = f r := by
  rw [rsum_comm, rsum_congr (g := fun e => if r = e then f e else 0)]
  · exact rsum_delta_box R k f r hr
  intro e he
  rw [rsum_mul_right, hK e he]; split <;> simp

/-- **Möbius inversion over `k`-tuples, `M ∘ U = id`.** For every `f` on `{1,…,R}^k` and every
`r ∈ {1,…,R}^k`: `∑_{r ∣ d} μ(d/r) ∑_{d ∣ e} f(e) = f(r)`. -/
theorem mobInv_upSum (R k : Nat) (f : List Nat → Rat) (r : List Nat) (hr : r ∈ box R k) :
    mobInv R k (upSum R k f) r = f r := by
  unfold mobInv upSum
  rw [← collapse R k (fun d e => if (tdvd r d && tdvd d e) = true then tmuq r d else 0) f r hr
      (fun e he => tuple_mobius_lower R k r e hr he)]
  apply rsum_congr; intro d _
  by_cases h : tdvd r d = true
  · rw [ite_eq_left h, ← rsum_mul_left]; apply rsum_congr; intro e _
    by_cases h' : tdvd d e = true <;> simp [h, h']
  · rw [ite_eq_right h]; symm
    rw [rsum_congr (g := fun _ => 0), rsum_zero]
    intro e _; simp [h]

/-- **Möbius inversion over `k`-tuples, `U ∘ M = id`.** For every `F` on `{1,…,R}^k` and every
`r ∈ {1,…,R}^k`: `∑_{r ∣ d} ∑_{d ∣ e} μ(e/d) F(e) = F(r)`. -/
theorem upSum_mobInv (R k : Nat) (F : List Nat → Rat) (r : List Nat) (hr : r ∈ box R k) :
    upSum R k (mobInv R k F) r = F r := by
  unfold mobInv upSum
  rw [← collapse R k (fun d e => if (tdvd r d && tdvd d e) = true then tmuq d e else 0) F r hr
      (fun e he => tuple_mobius_upper R k r e hr he)]
  apply rsum_congr; intro d _
  by_cases h : tdvd r d = true
  · rw [ite_eq_left h]; apply rsum_congr; intro e _
    by_cases h' : tdvd d e = true <;> simp [h, h']
  · rw [ite_eq_right h]; symm
    rw [rsum_congr (g := fun _ => 0), rsum_zero]
    intro e _; simp [h]

/-! ## Maynard's normalisation (Lemma 5.1 / eq. (5.8) shape) -/

/-- `∏_i d_i` as a rational. -/
def tN (d : List Nat) : Rat := ((d.prod : Nat) : Rat)

/-- `∏_i φ(r_i)` as a rational. -/
def tphi (r : List Nat) : Rat := (((r.map totient).prod : Nat) : Rat)

/-- `∏_i μ(r_i)` as a rational (`= μ(∏_i r_i)` when the `r_i` are pairwise coprime, as on
Maynard's support; that identity is proved in `MuTuple.lean`). -/
def tmu (r : List Nat) : Rat := (r.map fun x => (mu x : Rat)).prod

/-- Maynard's `y_r = μ(r) φ(r) ∑_{r ∣ d} λ_d / d` (all products over coordinates). -/
def maynardY (R k : Nat) (lam : List Nat → Rat) (r : List Nat) : Rat :=
  tmu r * tphi r * upSum R k (fun d => lam d / tN d) r

/-- Maynard's inverse `λ_d = μ(d) d ∑_{d ∣ r} y_r / φ(r)` (all products over coordinates). -/
def maynardLam (R k : Nat) (y : List Nat → Rat) (d : List Nat) : Rat :=
  tmu d * tN d * upSum R k (fun r => y r / tphi r) d

/-- The sign identity `μ(d) μ(r) = μ(r / d)` for all `d ∣ r ∣ e` (coordinatewise). It holds when
every `e_i` is squarefree (see `signOK_of_sqfree`). -/
def SignOK (e : List Nat) : Prop :=
  ∀ d r, tdvd d r = true → tdvd r e = true → tmu d * tmu r = tmuq d r

theorem nat_prod_pos {f : Nat → Nat} : ∀ {l : List Nat}, (∀ x ∈ l, 0 < f x) →
    0 < (l.map f).prod
  | [], _ => by simp
  | x :: l, h => by
    rw [List.map_cons, List.prod_cons]
    exact Nat.mul_pos (h x List.mem_cons_self) (nat_prod_pos fun y hy => h y (List.mem_cons_of_mem _ hy))

theorem tN_ne_zero {R k : Nat} {d : List Nat} (hd : d ∈ box R k) : tN d ≠ 0 := by
  have h : 0 < (d.map id).prod :=
    nat_prod_pos fun x hx => (mem_rng.mp ((mem_box_entries hd).2 x hx)).1
  rw [List.map_id] at h
  unfold tN; intro h0
  have : (d.prod : Rat) = ((0 : Nat) : Rat) := h0
  have := Rat.natCast_inj.mp this
  omega

theorem tphi_ne_zero {R k : Nat} {r : List Nat} (hr : r ∈ box R k) : tphi r ≠ 0 := by
  have h : 0 < (r.map totient).prod :=
    nat_prod_pos fun x hx => totient_pos x (mem_rng.mp ((mem_box_entries hr).2 x hx)).1
  unfold tphi; intro h0
  have : ((r.map totient).prod : Rat) = ((0 : Nat) : Rat) := h0
  have := Rat.natCast_inj.mp this
  omega

theorem rat_cancel1 (a b c : Rat) (hb : b ≠ 0) : a * b * c / b = a * c := by grind

theorem rat_cancel2 (t x : Rat) (ht : t ≠ 0) : t * (x / t) = x := by grind

theorem rat_div_zero (t : Rat) : (0 : Rat) / t = 0 := by grind

/-- Replacing `μ(d) μ(r)` by `μ(r/d)` inside `∑_{d ∣ r} μ(r) (U w)(r)` when the support of `w`
satisfies the sign identity. -/
theorem signed_sum (R k : Nat) (w : List Nat → Rat) (d : List Nat)
    (hS : ∀ e ∈ box R k, w e ≠ 0 → SignOK e) :
    tmu d * ((box R k).map fun r => if tdvd d r = true then tmu r * upSum R k w r else 0).sum
      = mobInv R k (upSum R k w) d := by
  unfold mobInv
  rw [← rsum_mul_left]
  apply rsum_congr; intro r _
  by_cases h : tdvd d r = true
  · rw [ite_eq_left h, ite_eq_left h]
    by_cases hU : upSum R k w r = 0
    · rw [hU]; simp
    · obtain ⟨e, he, hne⟩ := rsum_ne_zero hU
      have hre : tdvd r e = true := by
        apply Classical.byContradiction; intro hc; exact hne (by rw [ite_eq_right hc])
      have hwe : w e ≠ 0 := by rw [ite_eq_left hre] at hne; exact hne
      rw [← hS e he hwe d r h hre, Rat.mul_assoc]
  · rw [ite_eq_right h, ite_eq_right h, Rat.mul_zero]

/-- **Maynard's inversion `λ ↦ y ↦ λ` (eq. (5.8)), on the box `{1,…,R}^k`.**
If every tuple `e` in the support of `λ` satisfies the sign identity (e.g. all `e_i` squarefree),
then with `y_r = μ(r) φ(r) ∑_{r ∣ d} λ_d / d` one has `λ_d = μ(d) d ∑_{d ∣ r} y_r / φ(r)` for every
`d ∈ {1,…,R}^k`. -/
theorem maynard_lam_of_y (R k : Nat) (lam : List Nat → Rat)
    (hS : ∀ e ∈ box R k, lam e ≠ 0 → SignOK e) (d : List Nat) (hd : d ∈ box R k) :
    maynardLam R k (maynardY R k lam) d = lam d := by
  unfold maynardLam maynardY
  have h1 : upSum R k (fun r => tmu r * tphi r * upSum R k (fun d => lam d / tN d) r / tphi r) d
      = ((box R k).map fun r => if tdvd d r = true then
          tmu r * upSum R k (fun d => lam d / tN d) r else 0).sum := by
    unfold upSum
    apply rsum_congr; intro r hr
    have := tphi_ne_zero hr
    split
    · exact rat_cancel1 _ _ _ this
    · rfl
  have hS' : ∀ e ∈ box R k, lam e / tN e ≠ 0 → SignOK e := by
    intro e he hne
    apply hS e he; intro h0; apply hne; rw [h0]; exact rat_div_zero _
  rw [h1, Rat.mul_comm (tmu d), Rat.mul_assoc, signed_sum R k _ d hS',
    mobInv_upSum R k _ d hd]
  exact rat_cancel2 _ _ (tN_ne_zero hd)

/-- **Maynard's inversion `y ↦ λ ↦ y`, on the box `{1,…,R}^k`.**
If every tuple `e` in the support of `y` satisfies the sign identity (e.g. all `e_i` squarefree),
then with `λ_d = μ(d) d ∑_{d ∣ r} y_r / φ(r)` one has `y_r = μ(r) φ(r) ∑_{r ∣ d} λ_d / d` for every
`r ∈ {1,…,R}^k`. -/
theorem maynard_y_of_lam (R k : Nat) (y : List Nat → Rat)
    (hS : ∀ e ∈ box R k, y e ≠ 0 → SignOK e) (r : List Nat) (hr : r ∈ box R k) :
    maynardY R k (maynardLam R k y) r = y r := by
  unfold maynardLam maynardY
  have h1 : upSum R k (fun d => tmu d * tN d * upSum R k (fun r => y r / tphi r) d / tN d) r
      = ((box R k).map fun d => if tdvd r d = true then
          tmu d * upSum R k (fun r => y r / tphi r) d else 0).sum := by
    unfold upSum
    apply rsum_congr; intro d hd
    have := tN_ne_zero hd
    split
    · exact rat_cancel1 _ _ _ this
    · rfl
  have hS' : ∀ e ∈ box R k, y e / tphi e ≠ 0 → SignOK e := by
    intro e he hne
    apply hS e he; intro h0; apply hne; rw [h0]; exact rat_div_zero _
  rw [h1, Rat.mul_comm (tmu r), Rat.mul_assoc, signed_sum R k _ r hS',
    mobInv_upSum R k _ r hr]
  exact rat_cancel2 _ _ (tphi_ne_zero hr)

/-! ## The sign identity on squarefree entries -/

/-- The 1-d sign identity at `c`: `μ(a) μ(x) = μ(x / a)` for all `a ∣ x ∣ c`. -/
def MuSign (c : Nat) : Prop := ∀ a x, c % x = 0 → x % a = 0 → mu a * mu x = mu (x / a)

/-- The tuple sign identity follows from the 1-d one at every entry. -/
theorem signOK_of_entries : ∀ e : List Nat, (∀ c ∈ e, MuSign c) → SignOK e
  | [], _, d, r, h1, h2 => by
    cases r with
    | nil => cases d with
      | nil => simp [tmu, tmuq]
      | cons _ _ => simp [tdvd] at h1
    | cons _ _ => simp [tdvd] at h2
  | c :: e, hc, d, r, h1, h2 => by
    cases r with
    | nil => simp [tdvd] at h2
    | cons x r => cases d with
      | nil => simp [tdvd] at h1
      | cons a d =>
        simp only [tdvd, Bool.and_eq_true, beq_iff_eq] at h1 h2
        have ih := signOK_of_entries e (fun c' h => hc c' (List.mem_cons_of_mem _ h)) d r h1.2 h2.2
        have h1d := hc c List.mem_cons_self a x h2.1 h1.1
        have hq : (mu a : Rat) * (mu x : Rat) = (mu (x / a) : Rat) := by
          rw [← Rat.intCast_mul, h1d]
        simp only [tmu, tmuq, List.map_cons, List.prod_cons] at ih ⊢
        rw [← ih, ← hq]
        grind

/-- Decidable form of `MuSign c` for all `c < N` with `μ(c) ≠ 0`. -/
def muSignCheck (N : Nat) : Bool :=
  (List.range N).all fun c => mu c == 0 || (List.range (c + 1)).all fun x =>
    c % x != 0 || (List.range (x + 1)).all fun a => x % a != 0 || mu a * mu x == mu (x / a)

theorem muSign_of_check {N c : Nat} (h : muSignCheck N = true) (hc : c < N) (hmu : mu c ≠ 0)
    (hc1 : 1 ≤ c) : MuSign c := by
  intro a x hx ha
  unfold muSignCheck at h
  rw [List.all_eq_true] at h
  have := h c (List.mem_range.mpr hc)
  simp only [Bool.or_eq_true, beq_iff_eq, hmu, false_or, List.all_eq_true, List.mem_range,
    bne_iff_ne, ne_eq] at this
  have hxc : x ≤ c := by
    have hd : x ∣ c := Nat.dvd_of_mod_eq_zero hx
    exact Nat.le_of_dvd (by omega) hd
  have hx1 : x ≠ 0 := by intro h0; subst h0; rw [Nat.mod_zero] at hx; omega
  have hax : a ≤ x := Nat.le_of_dvd (by omega) (Nat.dvd_of_mod_eq_zero ha)
  rcases this x (by omega) with h' | h'
  · exact absurd hx h'
  · rcases h' a (by omega) with h'' | h''
    · exact absurd ha h''
    · exact h''

/-- `μ(a) μ(x) = μ(x/a)` for all `a ∣ x ∣ c`, every squarefree `c ≤ 30` (by `decide`). -/
theorem muSignCheck_31 : muSignCheck 31 = true := by decide

/-- Maynard's inversion `λ ↦ y ↦ λ` with the support condition stated as squarefreeness of the
entries (`μ(e_i) ≠ 0`), assuming the 1-d sign identity `MuSign c` for squarefree `c ≤ R`. -/
theorem maynard_lam_of_y_sqfree (R k : Nat) (hMu : ∀ c, 1 ≤ c → c ≤ R → mu c ≠ 0 → MuSign c)
    (lam : List Nat → Rat) (hS : ∀ e ∈ box R k, lam e ≠ 0 → ∀ c ∈ e, mu c ≠ 0)
    (d : List Nat) (hd : d ∈ box R k) :
    maynardLam R k (maynardY R k lam) d = lam d :=
  maynard_lam_of_y R k lam (fun e he hne => signOK_of_entries e fun c hc =>
    have hc' := mem_rng.mp ((mem_box_entries he).2 c hc)
    hMu c hc'.1 hc'.2 (hS e he hne c hc)) d hd

/-- Same for `y ↦ λ ↦ y`. -/
theorem maynard_y_of_lam_sqfree (R k : Nat) (hMu : ∀ c, 1 ≤ c → c ≤ R → mu c ≠ 0 → MuSign c)
    (y : List Nat → Rat) (hS : ∀ e ∈ box R k, y e ≠ 0 → ∀ c ∈ e, mu c ≠ 0)
    (r : List Nat) (hr : r ∈ box R k) :
    maynardY R k (maynardLam R k y) r = y r :=
  maynard_y_of_lam R k y (fun e he hne => signOK_of_entries e fun c hc =>
    have hc' := mem_rng.mp ((mem_box_entries he).2 c hc)
    hMu c hc'.1 hc'.2 (hS e he hne c hc)) r hr

theorem muSign_upto_30 (c : Nat) (h1 : 1 ≤ c) (h2 : c ≤ 30) (hmu : mu c ≠ 0) : MuSign c :=
  muSign_of_check muSignCheck_31 (by omega) hmu h1

/-- **Unconditional instance for `R ≤ 30`, every `k`:** if `λ` is supported on tuples with
squarefree entries in `{1,…,R}`, then `λ_d = μ(d) d ∑_{d ∣ r} y_r / φ(r)` with
`y_r = μ(r) φ(r) ∑_{r ∣ d} λ_d / d`. -/
theorem maynard_inversion_R30 (R k : Nat) (hR : R ≤ 30) (lam : List Nat → Rat)
    (hS : ∀ e ∈ box R k, lam e ≠ 0 → ∀ c ∈ e, mu c ≠ 0) (d : List Nat) (hd : d ∈ box R k) :
    maynardLam R k (maynardY R k lam) d = lam d :=
  maynard_lam_of_y_sqfree R k (fun c h1 h2 hmu => muSign_upto_30 c h1 (by omega) hmu) lam hS d hd

/-- **Unconditional instance for `R ≤ 30`, every `k`:** the converse `y ↦ λ ↦ y`. -/
theorem maynard_inversion_R30' (R k : Nat) (hR : R ≤ 30) (y : List Nat → Rat)
    (hS : ∀ e ∈ box R k, y e ≠ 0 → ∀ c ∈ e, mu c ≠ 0) (r : List Nat) (hr : r ∈ box R k) :
    maynardY R k (maynardLam R k y) r = y r :=
  maynard_y_of_lam_sqfree R k (fun c h1 h2 hmu => muSign_upto_30 c h1 (by omega) hmu) y hS r hr

/-! ## Concrete checks -/

/-- Tuple Möbius sum, `k = 2`, `R = 6`, `r = (1,2)`, `e = (6,2)` and `e = (1,2)`. -/
theorem tuple_mobius_example :
    ((box 6 2).map fun d => if (tdvd [1, 2] d && tdvd d [6, 2]) = true
        then tmuq [1, 2] d else 0).sum = 0 ∧
    ((box 6 2).map fun d => if (tdvd [1, 2] d && tdvd d [1, 2]) = true
        then tmuq [1, 2] d else 0).sum = 1 := by decide +kernel

/-- A squarefree-supported weight on `{1,…,6}²`. -/
def lamEx (d : List Nat) : Rat :=
  if d = [1, 1] then 3 else if d = [2, 3] then -1 else if d = [5, 1] then 1 / 2 else 0

/-- Round trip `λ ↦ y ↦ λ` on a concrete instance (`k = 2`, `R = 6`), at three points. -/
theorem maynard_inversion_example :
    maynardLam 6 2 (maynardY 6 2 lamEx) [1, 1] = 3 ∧
    maynardLam 6 2 (maynardY 6 2 lamEx) [2, 3] = -1 ∧
    maynardLam 6 2 (maynardY 6 2 lamEx) [2, 1] = 0 := by decide +kernel

/-- The squarefree hypothesis is needed: with `λ_{(4,1)} = 1` (and `0` elsewhere) the round trip
returns `0` at `(4,1)`, since `μ(4) = 0`. -/
theorem maynard_inversion_needs_sqfree :
    maynardLam 6 2 (maynardY 6 2 fun d => if d = [4, 1] then 1 else 0) [4, 1] = 0 := by
  decide +kernel

end MaynardInv
end TwinPrimes
