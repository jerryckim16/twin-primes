import TwinPrimes.MaynardS2Mult

/-!
# Maynard's Lemma 5.3, exact part: `y^{(m)}` in terms of `y` ((5.28)–(5.30), (5.32))

Source: Maynard, *Small gaps between primes*, arXiv:1311.4600v3, p. 13, Lemma 5.3 and its proof.
Objects (conventions of `MaynardInv`, `MaynardS2Y`): the box `{1,…,R}^k`, `tdvd`, `upSum`, `tmu`,
`tphi`, `tN`, `g = gM = μ ∗ φ`, `tg`.
* `λ = maynardLam R k y`, i.e. (5.8): `λ_d = ∏μ(dᵢ) ∏dᵢ ∑_{d ∣ a} y_a / ∏φ(aᵢ)`;
* `y^{(m)} = yS2 R k m λ`, i.e. (5.23).

Proved:
* `relSum_eq` / `oneSum_eq`: `∑_{r ∣ x ∣ a} μ(x) x / φ(x) = μ(a) r / φ(a)` for squarefree `a`
  (the evaluation of the `d`-sum between (5.29) and (5.30)); `tupleSum_eq`: its tuple version.
* `maynard_lemma53_exact` (= (5.30)): for `y` supported on tuples with squarefree entries and every
  `r` in the box with `r_m = 1`,
  `y^{(m)}_r = ∏μ(rᵢ)g(rᵢ) ∑_{r ∣ a} y_a / ∏φ(aᵢ) · ∏_{i ≠ m} μ(aᵢ) rᵢ / φ(aᵢ)`.
* `maynard_lemma53_split` (= (5.32) with the error term written out exactly): the terms with
  `a_j = r_j` for all `j ≠ m` give `∏ g(rᵢ) rᵢ / φ(rᵢ)² · ∑_{a_m ≤ R} y_{r[m ↦ a_m]} / φ(a_m)`;
  the rest is an explicit sum `E`.

NOT covered: the bound (5.31) on `E` (it uses `(a_j, W) = 1 ⇒ a_j = r_j` or `a_j > D₀ r_j` and
analytic estimates), `g(p)p/φ(p)² = 1 + O(p⁻²)`, and the final `O(y_max φ(W) log R / (W D₀))`.
-/

namespace TwinPrimes
namespace MaynardS2Lemma53

open Gauss SelbergOpt MaynardInv MuMult MaynardDiag MaynardS2Y MaynardS2Mult

/-! ## One dimension: `∑_{r ∣ x ∣ a} μ(x) x / φ(x) = μ(a) r / φ(a)` for squarefree `a` -/

/-- `h(x) = μ(x) x / φ(x)`. -/
def hq (x : Nat) : Rat := (mu x : Rat) * (x : Rat) / (totient x : Rat)

/-- The relative divisor sum `∑_{x ∣ a, r ∣ x} h(x)`. -/
def relSum (r a : Nat) : Rat := dvs a (fun x => if x % r = 0 then hq x else 0)

theorem totient_ne_zero_rat (x : Nat) (hx : 1 ≤ x) : (totient x : Rat) ≠ 0 := by
  have := totient_pos x hx
  intro h0
  have : ((totient x : Nat) : Rat) = ((0 : Nat) : Rat) := h0
  have := Rat.natCast_inj.mp this
  omega

theorem natCast_sub_one_ne_zero (p : Nat) (hp : 2 ≤ p) : (p : Rat) - 1 ≠ 0 := by
  obtain ⟨q, rfl⟩ : ∃ q, p = q + 2 := ⟨p - 2, by omega⟩
  rw [Rat.natCast_add]
  have : (0 : Rat) ≤ (q : Rat) := Rat.natCast_nonneg
  have h2 : ((2 : Nat) : Rat) = 2 := rfl
  rw [h2]
  grind

/-- `h(p e) = -(p/(p-1)) h(e)` for `p` prime, `p ∤ e`, `e ≥ 1`. -/
theorem hq_prime_mul (p e : Nat) (hp : IsPrime p) (he : 1 ≤ e) (hpe : ¬ p ∣ e) :
    hq (p * e) = -((p : Rat) / ((p : Rat) - 1)) * hq e := by
  have hp2 := hp.1
  unfold hq
  rw [mu_prime_mul p hp e he hpe, totient_mul_of_not_dvd p e hp hpe, Rat.natCast_mul,
    Rat.natCast_mul, natCast_sub_one p (by omega), Rat.intCast_neg]
  have h1 := totient_ne_zero_rat e he
  have h2 := natCast_sub_one_ne_zero p hp2
  grind

theorem dvs_one (F : Nat → Rat) : dvs 1 F = F 1 := by
  unfold dvs; simp [rng, Rat.add_zero]

theorem dvs_congr (n : Nat) (F G : Nat → Rat) (h : ∀ v, 1 ≤ v → v ∣ n → F v = G v) :
    dvs n F = dvs n G := by
  unfold dvs; apply rsum_congr; intro v hv
  by_cases hd : n % v = 0
  · rw [ite_eq_left hd, ite_eq_left hd]
    exact h v (mem_rng.mp hv).1 (Nat.dvd_of_mod_eq_zero hd)
  · rw [ite_eq_right hd, ite_eq_right hd]

theorem dvs_mul_left (n : Nat) (c : Rat) (F : Nat → Rat) :
    dvs n (fun v => c * F v) = c * dvs n F := by
  unfold dvs; rw [← rsum_mul_left]; apply rsum_congr; intro v _
  by_cases hd : n % v = 0
  · rw [ite_eq_left hd, ite_eq_left hd]
  · rw [ite_eq_right hd, ite_eq_right hd, Rat.mul_zero]

theorem dvs_zero (n : Nat) : dvs n (fun _ => 0) = 0 := by
  unfold dvs; rw [rsum_congr (g := fun _ => 0), rsum_zero]
  intro v _; split <;> rfl

/-- **The 1-d sum of (5.29)→(5.30):** for squarefree `a ≥ 1` and `r ∣ a`,
`∑_{x ∣ a, r ∣ x} μ(x) x / φ(x) = μ(a) r / φ(a)`. -/
theorem relSum_eq (a : Nat) : 1 ≤ a → Sqf a → ∀ r, r ∣ a →
    relSum r a = (mu a : Rat) * (r : Rat) / (totient a : Rat) := by
  induction a using Nat.strongRecOn with
  | ind a ih =>
  intro ha hs r hr
  rcases Nat.lt_or_ge a 2 with h2 | h2
  · have : a = 1 := by omega
    subst this
    have : r = 1 := Nat.dvd_one.mp hr
    subst this
    unfold relSum; rw [dvs_one]; decide +kernel
  · obtain ⟨p, hp, a', rfl⟩ := exists_prime_dvd _ h2
    have hp2 := hp.1
    have ha' : 1 ≤ a' := by
      rcases Nat.eq_zero_or_pos a' with h | h
      · subst h; omega
      · exact h
    have hlt : a' < p * a' := by
      have := Nat.mul_le_mul_right a' hp2; omega
    have hpa' : ¬ p ∣ a' := fun h => hs p hp (Nat.mul_dvd_mul_left p h)
    have hs' : Sqf a' := sqf_of_dvd hs (Nat.dvd_mul_left a' p)
    have hphi := totient_ne_zero_rat a' ha'
    have hp1 := natCast_sub_one_ne_zero p hp2
    have hmu : (mu (p * a') : Rat) = -(mu a' : Rat) := by
      rw [mu_prime_mul p hp a' ha' hpa', Rat.intCast_neg]
    have htot : ((totient (p * a') : Nat) : Rat) = ((p : Rat) - 1) * (totient a' : Rat) := by
      rw [totient_mul_of_not_dvd p a' hp hpa', Rat.natCast_mul, natCast_sub_one p (by omega)]
    unfold relSum
    rw [dvs_prime_mul p a' hp ha' hpa', hmu, htot]
    by_cases hpr : p ∣ r
    · obtain ⟨r', rfl⟩ := hpr
      have hr' : r' ∣ a' := Nat.dvd_of_mul_dvd_mul_left (by omega) hr
      have e1 : dvs a' (fun x => if x % (p * r') = 0 then hq x else 0) = 0 := by
        refine (dvs_congr a' _ (fun _ => 0) ?_).trans (dvs_zero a'); intro v _ hv
        rw [ite_eq_right]; intro h
        exact hpa' (Nat.dvd_trans (Nat.dvd_trans (Nat.dvd_mul_right p r')
          (Nat.dvd_of_mod_eq_zero h)) hv)
      have e2 : dvs a' (fun e => if (p * e) % (p * r') = 0 then hq (p * e) else 0)
          = -((p : Rat) / ((p : Rat) - 1)) * relSum r' a' := by
        unfold relSum; rw [← dvs_mul_left]; apply dvs_congr; intro v hv1 hv
        rw [Nat.mul_mod_mul_left]
        by_cases h : v % r' = 0
        · rw [h, Nat.mul_zero, ite_eq_left rfl, ite_eq_left rfl,
            hq_prime_mul p v hp hv1 (fun h' => hpa' (Nat.dvd_trans h' hv))]
        · have : p * (v % r') ≠ 0 := Nat.mul_ne_zero (by omega) h
          rw [ite_eq_right this, ite_eq_right h, Rat.mul_zero]
      rw [e1, e2, ih a' hlt ha' hs' r' hr', Rat.natCast_mul]
      grind
    · have hr' : r ∣ a' := euclid hp hpr hr
      have e2 : dvs a' (fun e => if (p * e) % r = 0 then hq (p * e) else 0)
          = -((p : Rat) / ((p : Rat) - 1)) * relSum r a' := by
        unfold relSum; rw [← dvs_mul_left]; apply dvs_congr; intro v hv1 hv
        have hiff : (p * v) % r = 0 ↔ v % r = 0 := by
          rw [← Nat.dvd_iff_mod_eq_zero, ← Nat.dvd_iff_mod_eq_zero]
          exact ⟨euclid hp hpr, fun h' => Nat.dvd_trans h' (Nat.dvd_mul_left v p)⟩
        by_cases h : v % r = 0
        · rw [ite_eq_left (hiff.mpr h), ite_eq_left h,
            hq_prime_mul p v hp hv1 (fun h' => hpa' (Nat.dvd_trans h' hv))]
        · rw [ite_eq_right (fun e => h (hiff.mp e)), ite_eq_right h, Rat.mul_zero]
      have e1 := ih a' hlt ha' hs' r hr'
      unfold relSum at e1
      rw [e2, e1]
      unfold relSum
      rw [e1]
      grind


/-- The same sum over `x ∈ {1,…,R}` (the form that appears coordinatewise in the box). -/
theorem oneSum_eq (R r a : Nat) (ha : a ∈ rng R) (hs : Sqf a) (hr : r ∣ a) :
    ((rng R).map fun x => if x % r = 0 ∧ a % x = 0 then hq x else 0).sum
      = (mu a : Rat) * (r : Rat) / (totient a : Rat) := by
  obtain ⟨h1, h2⟩ := mem_rng.mp ha
  have h0 : (if 0 % r = 0 ∧ a % 0 = 0 then hq 0 else 0) = 0 := by
    rw [ite_eq_right]; intro h; rw [Nat.mod_zero] at h; omega
  have e : relSum r a = ((rng a).map fun x => if x % r = 0 ∧ a % x = 0 then hq x else 0).sum := by
    unfold relSum dvs
    apply rsum_congr; intro v _
    by_cases ha' : a % v = 0 <;> by_cases hv : v % r = 0 <;> simp [ha', hv]
  rw [← relSum_eq a h1 hs r hr, e, rsum_rng R _ h0, rsum_rng a _ h0,
    rsum_range_extend (a + 1) (R + 1) _ (by omega)]
  intro v hv _
  rw [ite_eq_right]; intro h
  rw [Nat.mod_eq_of_lt (show a < v by omega)] at h; omega

theorem oneSum_zero (R r a : Nat) (hr : ¬ a % r = 0) :
    ((rng R).map fun x => if x % r = 0 ∧ a % x = 0 then hq x else 0).sum = 0 := by
  rw [rsum_congr (g := fun _ => 0), rsum_zero]
  intro x _
  rw [ite_eq_right]; intro h
  exact hr (Nat.mod_eq_zero_of_dvd (Nat.dvd_trans (Nat.dvd_of_mod_eq_zero h.1)
    (Nat.dvd_of_mod_eq_zero h.2)))

/-! ## Tuples -/

/-- `∏ᵢ μ(aᵢ) rᵢ / φ(aᵢ)` (all coordinates). Lemma 5.3 uses it at `a` with `a_m` replaced by `1`,
which removes the `m`-th factor (it becomes `μ(1)·r_m/φ(1) = r_m = 1`). -/
def cofAll : List Nat → List Nat → Rat
  | x :: r, c :: a => (mu c : Rat) * (x : Rat) / (totient c : Rat) * cofAll r a
  | _, _ => 1

theorem hqTuple_cons (y : Nat) (d : List Nat) :
    tmu (y :: d) * tN (y :: d) / tphi (y :: d) = hq y * (tmu d * tN d / tphi d) := by
  unfold tmu tN tphi hq
  simp only [List.map_cons, List.prod_cons, Rat.natCast_mul]
  grind

/-- **Tuple version of the `d`-sum in (5.29):** for `r, a` in the box with `a` having squarefree
entries, `∑_{r ∣ d ∣ a} ∏ᵢ μ(dᵢ) dᵢ / φ(dᵢ) = [r ∣ a] ∏ᵢ μ(aᵢ) rᵢ / φ(aᵢ)`. -/
theorem tupleSum_eq (R : Nat) : ∀ (k : Nat) (r a : List Nat), r ∈ box R k → a ∈ box R k →
    (∀ c ∈ a, Sqf c) →
    ((box R k).map fun d => if (tdvd r d && tdvd d a) = true then
        tmu d * tN d / tphi d else 0).sum
      = if tdvd r a = true then cofAll r a else 0
  | 0, r, a, hr, ha, _ => by
    rw [box_zero, List.mem_singleton] at hr ha; subst hr; subst ha
    simp [box_zero, tdvd, cofAll, tmu, tN, tphi, Rat.add_zero]; decide +kernel
  | k + 1, r, a, hr, ha, hs => by
    obtain ⟨x, r', rfl, hx, hr'⟩ := mem_box_succ hr
    obtain ⟨c, a', rfl, hc, ha'⟩ := mem_box_succ ha
    have ih := tupleSum_eq R k r' a' hr' ha' (fun c' h => hs c' (List.mem_cons_of_mem _ h))
    rw [rsum_box_succ]
    rw [rsum_congr (g := fun y => (if y % x = 0 ∧ c % y = 0 then hq y else 0) *
        ((box R k).map fun d => if (tdvd r' d && tdvd d a') = true then
          tmu d * tN d / tphi d else 0).sum)]
    · rw [rsum_mul_right, ih]
      simp only [tdvd, Bool.and_eq_true, beq_iff_eq]
      by_cases hcx : c % x = 0
      · rw [oneSum_eq R x c hc (hs c List.mem_cons_self) (Nat.dvd_of_mod_eq_zero hcx)]
        by_cases ht : tdvd r' a' = true
        · rw [ite_eq_left ht, ite_eq_left ⟨hcx, ht⟩]; rfl
        · rw [ite_eq_right ht, ite_eq_right (fun h => ht h.2), Rat.mul_zero]
      · rw [oneSum_zero R x c hcx, Rat.zero_mul, ite_eq_right (fun h => hcx h.1)]
    · intro y _
      rw [← rsum_mul_left]; apply rsum_congr; intro d _
      simp only [tdvd]
      by_cases h1 : y % x = 0 <;> by_cases h2 : c % y = 0 <;>
        by_cases h3 : tdvd r' d = true <;> by_cases h4 : tdvd d a' = true <;>
        simp [h1, h2, h3, h4, hqTuple_cons]

/-! ## Replacing `a_m` by `1` -/

theorem one_mod_eq (x : Nat) : 1 % x = 0 ↔ x = 1 := by
  rcases x with _ | _ | x
  · simp
  · simp
  · rw [Nat.mod_eq_of_lt (by omega)]; omega

/-- `d ∣ a` and `d_m = 1` iff `d ∣ a[m ↦ 1]`. -/
theorem tdvd_set_iff : ∀ (d a : List Nat) (m : Nat),
    (tdvd d a = true ∧ d.getD m 1 = 1) ↔ tdvd d (a.set m 1) = true
  | [], [], _ => by simp [tdvd]
  | x :: d, c :: a, 0 => by
    simp only [tdvd, List.set_cons_zero, List.getD_cons_zero, Bool.and_eq_true, beq_iff_eq,
      one_mod_eq]
    constructor
    · rintro ⟨⟨_, h⟩, rfl⟩; exact ⟨rfl, h⟩
    · rintro ⟨rfl, h⟩; exact ⟨⟨Nat.mod_one _, h⟩, rfl⟩
  | x :: d, c :: a, m + 1 => by
    simp only [tdvd, List.set_cons_succ, List.getD_cons_succ, Bool.and_eq_true, beq_iff_eq]
    rw [← tdvd_set_iff d a m]
    constructor
    · rintro ⟨⟨h1, h2⟩, h3⟩; exact ⟨h1, h2, h3⟩
    · rintro ⟨h1, h2, h3⟩; exact ⟨⟨h1, h2⟩, h3⟩
  | [], _ :: _, m => by cases m <;> simp [tdvd]
  | _ :: _, [], m => by simp [tdvd]

/-- If `r_m = 1` then `r ∣ a[m ↦ 1]` iff `r ∣ a`. -/
theorem tdvd_set_of : ∀ (r a : List Nat) (m : Nat), r.getD m 1 = 1 →
    tdvd r (a.set m 1) = tdvd r a
  | [], [], _, _ => by simp
  | x :: r, c :: a, 0, h => by
    simp only [List.getD_cons_zero] at h; subst h
    simp [tdvd, List.set_cons_zero, Nat.mod_one]
  | x :: r, c :: a, m + 1, h => by
    simp only [List.getD_cons_succ] at h
    simp only [tdvd, List.set_cons_succ, tdvd_set_of r a m h]
  | [], _ :: _, m, _ => by cases m <;> simp [tdvd]
  | _ :: _, [], m, _ => by simp [tdvd]

theorem set_mem_box (R : Nat) : ∀ (k : Nat) (a : List Nat) (m : Nat), a ∈ box R k →
    a.set m 1 ∈ box R k
  | 0, a, m, ha => by
    rw [box_zero, List.mem_singleton] at ha; subst ha; simp [box_zero]
  | k + 1, a, m, ha => by
    obtain ⟨c, a', rfl, hc, ha'⟩ := mem_box_succ ha
    have h1 : 1 ∈ rng R := mem_rng.mpr ⟨Nat.le_refl 1, Nat.le_trans (mem_rng.mp hc).1 (mem_rng.mp hc).2⟩
    cases m with
    | zero =>
      rw [List.set_cons_zero]
      simp only [box, List.mem_flatMap, List.mem_map]; exact ⟨1, h1, a', ha', rfl⟩
    | succ m =>
      rw [List.set_cons_succ]
      simp only [box, List.mem_flatMap, List.mem_map]
      exact ⟨c, hc, a'.set m 1, set_mem_box R k a' m ha', rfl⟩

theorem sqf_one : Sqf 1 := by
  intro p hp h
  have := Nat.le_of_dvd (by omega) h
  have := hp.1
  have : 4 ≤ p * p := Nat.mul_le_mul this this
  omega

/-! ## Lemma 5.3, exact part (5.28)–(5.30) -/

/-- **Maynard (5.28)–(5.30), exact.** Let `y` be supported on tuples with squarefree entries,
`λ = maynardLam y` (i.e. (5.8): `λ_d = μ(d) d ∑_{d ∣ a} y_a / φ(a)`), and `y^{(m)} = yS2 λ`
((5.23)). Then for every `r` in the box with `r_m = 1`,
`y^{(m)}_r = ∏ᵢ μ(rᵢ) g(rᵢ) · ∑_{r ∣ a} y_a / ∏ᵢ φ(aᵢ) · ∏_{i ≠ m} μ(aᵢ) rᵢ / φ(aᵢ)`. -/
theorem maynard_lemma53_exact (R k m : Nat) (y : List Nat → Rat)
    (hsq : ∀ a ∈ box R k, y a ≠ 0 → ∀ x ∈ a, mu x ≠ 0)
    (r : List Nat) (hr : r ∈ box R k) (hrm : r.getD m 1 = 1) :
    yS2 R k m (maynardLam R k y) r
      = tmu r * tg r * ((box R k).map fun a =>
          if tdvd r a = true then y a / tphi a * cofAll r (a.set m 1) else 0).sum := by
  unfold yS2
  congr 1
  unfold upSum
  rw [rsum_congr (g := fun d => ((box R k).map fun a =>
      (if (tdvd r d && tdvd d (a.set m 1)) = true then tmu d * tN d / tphi d else 0)
        * (y a / tphi a)).sum)]
  · rw [rsum_comm]
    apply rsum_congr; intro a ha
    rw [rsum_mul_right]
    by_cases hy : y a = 0
    · rw [hy, rat_div_zero, Rat.mul_zero]; split <;> simp
    · have hs : ∀ c ∈ a.set m 1, Sqf c := by
        intro c hc
        rcases List.mem_or_eq_of_mem_set hc with hc | rfl
        · exact sqf_of_mu c (mem_rng.mp ((mem_box_entries ha).2 c hc)).1 (hsq a ha hy c hc)
        · exact sqf_one
      rw [tupleSum_eq R k r (a.set m 1) hr (set_mem_box R k a m ha) hs, tdvd_set_of r a m hrm]
      split
      · grind
      · simp
  · intro d _
    by_cases hrd : tdvd r d = true
    · rw [ite_eq_left hrd]
      unfold fS2
      by_cases hdm : d.getD m 1 = 1
      · rw [ite_eq_left hdm]
        unfold maynardLam upSum
        rw [show ∀ (A S B : Rat), A * S / B = (A / B) * S from fun A S B => by grind,
          ← rsum_mul_left]
        apply rsum_congr; intro a _
        have hiff : tdvd d (a.set m 1) = tdvd d a := by
          apply Bool.eq_iff_iff.mpr; rw [← tdvd_set_iff]; exact ⟨fun h => h.1, fun h => ⟨h, hdm⟩⟩
        rw [hiff]
        by_cases hda : tdvd d a = true
        · simp [hrd, hda]
        · simp [hrd, hda]
      · rw [ite_eq_right hdm, rsum_congr (g := fun _ => 0), rsum_zero]
        intro a _
        have : tdvd d (a.set m 1) = false := by
          apply Bool.eq_false_iff.mpr; intro h; exact hdm ((tdvd_set_iff d a m).mpr h).2
        simp [this]
    · rw [ite_eq_right hrd, rsum_congr (g := fun _ => 0), rsum_zero]
      intro a _; simp [hrd]

/-! ## The main term of (5.32): `a_j = r_j` for all `j ≠ m` -/

theorem tdvd_refl : ∀ a : List Nat, tdvd a a = true
  | [] => rfl
  | x :: a => by simp [tdvd, Nat.mod_self, tdvd_refl a]

theorem tdvd_set_self : ∀ (a : List Nat) (m : Nat), tdvd (a.set m 1) a = true
  | [], _ => rfl
  | x :: a, 0 => by simp [tdvd, Nat.mod_one, tdvd_refl a]
  | x :: a, m + 1 => by simp [tdvd, Nat.mod_self, tdvd_set_self a m]

theorem set_set_one : ∀ (r : List Nat) (m t : Nat), r.getD m 1 = 1 → (r.set m t).set m 1 = r
  | [], _, _, _ => rfl
  | x :: r, 0, t, h => by simp at h; subst h; simp
  | x :: r, m + 1, t, h => by
    simp only [List.getD_cons_succ] at h
    simp [set_set_one r m t h]

theorem natprod_phi_set : ∀ (r : List Nat) (m t : Nat), r.getD m 1 = 1 → m < r.length →
    ((r.set m t).map totient).prod = totient t * (r.map totient).prod
  | [], _, _, _, h => by simp at h
  | x :: r, 0, t, h, _ => by
    simp at h; subst h; simp [totient_one]
  | x :: r, m + 1, t, h, hm => by
    simp only [List.getD_cons_succ] at h
    simp only [List.length_cons] at hm
    simp only [List.set_cons_succ, List.map_cons, List.prod_cons,
      natprod_phi_set r m t h (by omega)]
    exact Nat.mul_left_comm _ _ _

theorem tphi_set (r : List Nat) (m t : Nat) (h : r.getD m 1 = 1) (hm : m < r.length) :
    tphi (r.set m t) = (totient t : Rat) * tphi r := by
  unfold tphi; rw [natprod_phi_set r m t h hm, Rat.natCast_mul]

/-- Reindexing: tuples `a` of the box with `a[m ↦ 1] = r` are exactly `r[m ↦ t]`, `t ∈ {1,…,R}`. -/
theorem rsum_set_eq (R : Nat) : ∀ (k m : Nat) (r : List Nat) (F : List Nat → Rat),
    r ∈ box R k → m < k → r.getD m 1 = 1 →
    ((box R k).map fun a => if a.set m 1 = r then F a else 0).sum
      = ((rng R).map fun t => F (r.set m t)).sum
  | 0, _, _, _, _, hm, _ => absurd hm (Nat.not_lt_zero _)
  | k + 1, 0, r, F, hr, _, hrm => by
    obtain ⟨x, r', rfl, _, hr'⟩ := mem_box_succ hr
    simp only [List.getD_cons_zero] at hrm; subst hrm
    rw [rsum_box_succ]; apply rsum_congr; intro c _
    show _ = F (c :: r')
    rw [← rsum_delta_box R k (fun a' => F (c :: a')) r' hr']
    apply rsum_congr; intro a' _
    simp only [List.set_cons_zero, List.cons.injEq, true_and]
    by_cases h : a' = r'
    · subst h; simp
    · rw [ite_eq_right h, ite_eq_right (fun e => h e.symm)]
  | k + 1, m + 1, r, F, hr, hm, hrm => by
    obtain ⟨x, r', rfl, hx, hr'⟩ := mem_box_succ hr
    simp only [List.getD_cons_succ] at hrm
    have ih := rsum_set_eq R k m r' (fun a' => F (x :: a')) hr' (by omega) hrm
    rw [rsum_box_succ]
    rw [rsum_congr (g := fun c => if c = x then
        ((box R k).map fun a' => if a'.set m 1 = r' then F (x :: a') else 0).sum else 0)]
    · rw [rsum_delta_rng R x hx, ih]
      apply rsum_congr; intro t _; rfl
    · intro c _
      by_cases hc : c = x
      · subst hc; rw [ite_eq_left rfl]; apply rsum_congr; intro a' _
        simp only [List.set_cons_succ, List.cons.injEq, true_and]
      · rw [ite_eq_right hc, rsum_congr (g := fun _ => 0), rsum_zero]
        intro a' _
        simp only [List.set_cons_succ, List.cons.injEq]
        rw [ite_eq_right (fun e => hc e.1)]

/-- `∏ᵢ g(rᵢ) rᵢ / φ(rᵢ)²`, the coefficient in (5.32). -/
def tw (r : List Nat) : Rat :=
  (r.map fun x => gM x * (x : Rat) / ((totient x : Rat) * (totient x : Rat))).prod

theorem coef_eq_tw : ∀ r : List Nat, (∀ x ∈ r, 1 ≤ x ∧ mu x ≠ 0) →
    tmu r * tg r * cofAll r r / tphi r = tw r
  | [], _ => by simp [tmu, tg, cofAll, tphi, tw]; decide +kernel
  | x :: r, h => by
    have ih := coef_eq_tw r (fun z hz => h z (List.mem_cons_of_mem _ hz))
    obtain ⟨h1, h2⟩ := h x List.mem_cons_self
    have hmu : (mu x : Rat) * (mu x : Rat) = 1 := by
      rw [← Rat.intCast_mul, mu_mul_self_sqf x h1 (sqf_of_mu x h1 h2)]; rfl
    have hphi := totient_ne_zero_rat x h1
    have htw : tw (x :: r)
        = gM x * (x : Rat) / ((totient x : Rat) * (totient x : Rat)) * tw r := by
      simp [tw]
    rw [htw, ← ih]
    unfold tmu tg tphi
    simp only [List.map_cons, List.prod_cons, cofAll, Rat.natCast_mul]
    generalize (r.map fun x => (mu x : Rat)).prod = A
    generalize (r.map gM).prod = B
    generalize cofAll r r = C
    generalize (((r.map totient).prod : Nat) : Rat) = D
    grind

/-- **Maynard (5.32), exact form.** Under the hypotheses of `maynard_lemma53_exact`, with
`m < k` and `r` having squarefree entries, split the `a`-sum of (5.30) into the terms with
`a_j = r_j` for all `j ≠ m` (that is, `a[m ↦ 1] = r`) and the rest:
`y^{(m)}_r = ∏ᵢ g(rᵢ) rᵢ / φ(rᵢ)² · ∑_{a_m ≤ R} y_{r[m ↦ a_m]} / φ(a_m) + ∏ᵢ μ(rᵢ)g(rᵢ) · E`,
where `E` is the sum of the (5.30) terms with some `a_j ≠ r_j`, `j ≠ m` (Maynard bounds `E` in
(5.31)). -/
theorem maynard_lemma53_split (R k m : Nat) (y : List Nat → Rat)
    (hsq : ∀ a ∈ box R k, y a ≠ 0 → ∀ x ∈ a, mu x ≠ 0)
    (r : List Nat) (hr : r ∈ box R k) (hrm : r.getD m 1 = 1) (hm : m < k)
    (hrsq : ∀ x ∈ r, mu x ≠ 0) :
    yS2 R k m (maynardLam R k y) r
      = tw r * ((rng R).map fun t => y (r.set m t) / (totient t : Rat)).sum
        + tmu r * tg r * ((box R k).map fun a =>
            if tdvd r a = true ∧ a.set m 1 ≠ r then y a / tphi a * cofAll r (a.set m 1)
            else 0).sum := by
  have hlen := (mem_box_entries hr).1
  have hphi := tphi_ne_zero hr
  rw [maynard_lemma53_exact R k m y hsq r hr hrm,
    rsum_congr (g := fun a => (if a.set m 1 = r then y a / tphi a * cofAll r r else 0) +
      (if tdvd r a = true ∧ a.set m 1 ≠ r then y a / tphi a * cofAll r (a.set m 1) else 0)),
    rsum_add, Rat.mul_add,
    rsum_set_eq R k m r _ hr hm hrm,
    ← coef_eq_tw r (fun x hx => ⟨(mem_rng.mp ((mem_box_entries hr).2 x hx)).1, hrsq x hx⟩)]
  · congr 1
    rw [← rsum_mul_left, ← rsum_mul_left]; apply rsum_congr; intro t _
    rw [tphi_set r m t hrm (by omega)]
    have := tphi_ne_zero hr
    grind
  · intro a _
    by_cases he : a.set m 1 = r
    · have hd : tdvd r a = true := he ▸ tdvd_set_self a m
      rw [ite_eq_left hd, ite_eq_left he, ite_eq_right (fun h => h.2 he), he, Rat.add_zero]
    · rw [ite_eq_right he, Rat.zero_add]
      by_cases hd : tdvd r a = true
      · rw [ite_eq_left hd, ite_eq_left ⟨hd, he⟩]
      · rw [ite_eq_right hd, ite_eq_right (fun h => hd h.1)]

/-! ## Non-vacuity -/

/-- A weight on `{1,…,6}²` supported on tuples with squarefree entries, including `(1,6)`,
which contributes to the error part `E` at `r = (1,3)`, `m = 0`. -/
def yEx (a : List Nat) : Rat :=
  if a = [1, 3] then 2 else if a = [5, 3] then 1 else if a = [2, 3] then -1
  else if a = [1, 6] then 1 / 2 else if a = [3, 1] then 1 else 0

theorem ex_hsq : ∀ a ∈ box 6 2, yEx a ≠ 0 → ∀ x ∈ a, mu x ≠ 0 := by decide +kernel

theorem ex_r : [1, 3] ∈ box 6 2 := by decide +kernel

/-- `maynard_lemma53_exact` at `yEx`, `r = (1,3)`, `m = 0`, every hypothesis discharged. -/
theorem maynard_lemma53_exact_example :
    yS2 6 2 0 (maynardLam 6 2 yEx) [1, 3]
      = tmu [1, 3] * tg [1, 3] * ((box 6 2).map fun a =>
          if tdvd [1, 3] a = true then yEx a / tphi a * cofAll [1, 3] (a.set 0 1) else 0).sum :=
  maynard_lemma53_exact 6 2 0 yEx ex_hsq [1, 3] ex_r rfl

/-- `maynard_lemma53_split` at the same instance. -/
theorem maynard_lemma53_split_example :
    yS2 6 2 0 (maynardLam 6 2 yEx) [1, 3]
      = tw [1, 3] * ((rng 6).map fun t => yEx ([1, 3].set 0 t) / (totient t : Rat)).sum
        + tmu [1, 3] * tg [1, 3] * ((box 6 2).map fun a =>
            if tdvd [1, 3] a = true ∧ a.set 0 1 ≠ [1, 3] then
              yEx a / tphi a * cofAll [1, 3] (a.set 0 1) else 0).sum :=
  maynard_lemma53_split 6 2 0 yEx ex_hsq [1, 3] ex_r rfl (by decide) (by decide +kernel)

/-- The values: `y^{(0)}_{(1,3)} = 9/16`; the main term of (5.32) is `(3/4)·(2 − 1 + 1/4) = 15/16`;
the error part is `−3/8` (from `a = (1,6)`), so the split is not trivial. Also
`y^{(1)}_{(3,1)} = 3/4`, and `cofAll (1,3) (1,6) = μ(6)·3/φ(6) = 3/2`. -/
theorem ex_values :
    yS2 6 2 0 (maynardLam 6 2 yEx) [1, 3] = 9 / 16 ∧
    tw [1, 3] * ((rng 6).map fun t => yEx ([1, 3].set 0 t) / (totient t : Rat)).sum = 15 / 16 ∧
    tmu [1, 3] * tg [1, 3] * ((box 6 2).map fun a =>
        if tdvd [1, 3] a = true ∧ a.set 0 1 ≠ [1, 3] then
          yEx a / tphi a * cofAll [1, 3] (a.set 0 1) else 0).sum = -3 / 8 ∧
    yS2 6 2 1 (maynardLam 6 2 yEx) [3, 1] = 3 / 4 ∧
    cofAll [1, 3] ([1, 6].set 0 1) = 3 / 2 := by
  decide +kernel

end MaynardS2Lemma53
end TwinPrimes
