import TwinPrimes.MaynardS1Diag

/-!
# Maynard's `S₂` change of variables `λ ↦ y^{(m)}` and the diagonal form (finite, exact)

Maynard, *Small gaps between primes* (arXiv:1311.4600v3), proof of Lemma 5.2, eqs. (5.21)–(5.24),
(5.26). For squarefree `d, e` Maynard writes (5.21)
`1/φ([d,e]) = (1/(φ(d)φ(e))) ∑_{u ∣ d, u ∣ e} g(u)`, `g` totally multiplicative, `g(p) = p − 2`,
and puts (5.23) `y^{(m)}_r = ∏ᵢ μ(rᵢ) g(rᵢ) ∑_{r ∣ d, d_m = 1} λ_d / ∏ᵢ φ(dᵢ)`; the main term
of `S₂^{(m)}` then becomes `∑_u (y^{(m)}_u)² / ∏ᵢ g(uᵢ)` (first term of (5.26)).

This file proves the finite algebra on the box `{1,…,R}^k` (conventions of `MaynardInv` /
`MaynardDiag`), over `ℚ`:

* `gM`: `g := μ ∗ φ`, i.e. `g(x) = ∑_{v ∣ x} μ(x/v) φ(v)`. `gM_prime`: `g(p) = p − 2` for every
  prime `p` (so `gM` agrees with Maynard's `g` on primes; multiplicativity of `gM`, hence
  agreement on all squarefree arguments, is NOT proved here). `gM_divisor_sum`:
  `∑_{x ∣ c} g(x) = φ(c)` for every `c ≥ 1` (Möbius inversion; no squarefreeness needed).
* `tphiGcd_eq_sum`: `∏ᵢ φ(gcd(dᵢ,eᵢ)) = ∑_{u ∣ d, u ∣ e} ∏ᵢ g(uᵢ)` on the box (tensorised).
* `quad_diag`: a generic diagonalisation lemma (any kernel of the form `∑_{u ∣ d, u ∣ e} c(u)`).
* `maynard_S2_diag_g`: for ALL `λ`,
  `∑_{d,e ∈ box, d_m = e_m = 1} λ_d λ_e ∏ᵢ φ(gcd(dᵢ,eᵢ)) / (∏φ(dᵢ) ∏φ(eᵢ))
     = ∑_u ∏ᵢ g(uᵢ) · (∑_{u ∣ d, d_m = 1} λ_d / ∏φ(dᵢ))²`.
* `maynard_S2_diag_y`: for `λ` supported on tuples with squarefree entries, the same form equals
  `∑_u (y^{(m)}_u)² / ∏ᵢ g(uᵢ)` with `y^{(m)} = yS2` (Lean's `x / 0 = 0` makes the terms with
  `g(u) = 0` vanish on both sides; no hypothesis on `g ≠ 0`).
* `yS2_eq_zero`: `y^{(m)}_r = 0` unless `r_m = 1` (the remark after (5.23));
  `maynard_S2_diag_y_restrict`: the `u`-sum may be restricted to `u_m = 1`.
* `maynard_S2_diag_lcm`: (5.21) form. If `φ([a,b]) φ((a,b)) = φ(a) φ(b)` for squarefree
  `a, b ≤ R` (hypothesis `hphi`), the form above equals
  `∑_{d_m = e_m = 1} λ_d λ_e / ∏ᵢ φ([dᵢ,eᵢ])`. `phi_lcm_gcd_upto_12` checks `hphi` for
  `R ≤ 12` (`decide`), giving `maynard_S2_diag_lcm_R12` unconditionally there.
* `maynard_S2_lam_of_y`: the inversion of (5.23):
  `[d_m = 1] λ_d = μ(d) φ(d) ∑_{d ∣ r} y^{(m)}_r / g(r)` on the box, for squarefree-supported `λ`,
  provided `∑_{r ∣ d, d_m = 1} λ_d/φ(d) = 0` whenever `g(r) = 0` (`hg`).

NOT covered: the pairwise-coprimality restriction `Σ'` of (5.18) and the `s_{i,j}` variables of
(5.22)/(5.24) (our sums run over all pairs of the box with `d_m = e_m = 1`, the restriction is
not imposed); the bounds (5.25)–(5.27); Lemma 5.3; multiplicativity of `φ` or `g`.
-/

namespace TwinPrimes
namespace MaynardS2Y

open Gauss SelbergOpt MaynardInv MuMult MaynardDiag

/-! ## The function `g = μ ∗ φ` -/

/-- `g(x) = ∑_{v ∣ x} μ(x/v) φ(v)` (Dirichlet convolution `μ ∗ φ`), as a rational. -/
def gM (x : Nat) : Rat :=
  ((rng x).map fun v => if x % v = 0 then (mu (x / v) : Rat) * (totient v : Rat) else 0).sum

/-- `φ(p) = p − 1` for a prime `p`. -/
theorem totient_prime (p : Nat) (hp : MuMult.IsPrime p) : totient p = p - 1 := by
  obtain ⟨h2, hd⟩ := hp
  unfold totient
  obtain ⟨q, rfl⟩ : ∃ q, p = q + 1 := ⟨p - 1, by omega⟩
  rw [List.range_succ, List.filter_append, List.length_append]
  have h1 : (List.range q).filter (fun k => Nat.gcd (k + 1) (q + 1) == 1) = List.range q := by
    rw [List.filter_eq_self]
    intro k hk
    have hk := List.mem_range.mp hk
    simp only [beq_iff_eq]
    rcases hd _ (Nat.gcd_dvd_right (k + 1) (q + 1)) with h | h
    · exact h
    · exfalso
      have hdv : q + 1 ∣ k + 1 := h ▸ Nat.gcd_dvd_left (k + 1) (q + 1)
      have := Nat.le_of_dvd (by omega) hdv
      omega
  have h3 : [q].filter (fun k => Nat.gcd (k + 1) (q + 1) == 1) = [] := by
    have : (Nat.gcd (q + 1) (q + 1) == 1) = false := by rw [Nat.gcd_self]; simp; omega
    simp only [List.filter_cons, List.filter_nil, this]; rfl
  rw [h1, h3, List.length_range]; simp

theorem totient_one : totient 1 = 1 := by decide

/-- **`g(p) = p − 2`** for every prime `p` (Maynard's `g` on primes). -/
theorem gM_prime (p : Nat) (hp : MuMult.IsPrime p) : gM p = (p : Rat) - 2 := by
  have hp2 := hp.1
  have hmu := mu_prime p hp
  have hphi := totient_prime p hp
  obtain ⟨q, rfl⟩ : ∃ q, p = q + 1 := ⟨p - 1, by omega⟩
  unfold gM rng
  rw [List.range_succ, List.map_append, List.map_append, List.sum_append]
  have h1 : (((List.range q).map (· + 1)).map fun v =>
      if (q + 1) % v = 0 then (mu ((q + 1) / v) : Rat) * (totient v : Rat) else 0).sum
      = ((rng q).map fun v => if v = 1 then (mu (q + 1) : Rat) * (totient 1 : Rat) else 0).sum := by
    apply rsum_congr; intro v hv
    have hv' := mem_rng.mp hv
    by_cases h : v = 1
    · subst h; rw [ite_eq_left (Nat.mod_one _), ite_eq_left rfl, Nat.div_one]
    · rw [ite_eq_right h, ite_eq_right]
      intro hm
      rcases hp.2 v (Nat.dvd_of_mod_eq_zero hm) with h' | h'
      · exact h h'
      · omega
  rw [h1, rsum_delta_rng q 1 (mem_rng.mpr ⟨by omega, by omega⟩)]
  simp only [List.map_cons, List.map_nil, List.sum_cons, List.sum_nil, Nat.mod_self,
    ↓reduceIte, Nat.div_self (show 0 < q + 1 by omega), mu_one, totient_one, hmu, hphi]
  have : q + 1 - 1 = q := by omega
  rw [this]
  simp only [Rat.natCast_add]
  grind

/-- For `1 ≤ x ≤ R` the defining sum of `g(x)` may be taken over `v ≤ R`. -/
theorem gM_range (R x : Nat) (hx : x ∈ rng R) :
    gM x = ((rng R).map fun v =>
      if x % v = 0 then (mu (x / v) : Rat) * (totient v : Rat) else 0).sum := by
  obtain ⟨h1, h2⟩ := mem_rng.mp hx
  unfold gM
  rw [rsum_rng x _ (by rw [ite_eq_right]; intro h; rw [Nat.mod_zero] at h; omega),
    rsum_rng R _ (by rw [ite_eq_right]; intro h; rw [Nat.mod_zero] at h; omega),
    rsum_range_extend (x + 1) (R + 1) _ (by omega) (fun v hv _ => by
      rw [ite_eq_right]; intro h; rw [Nat.mod_eq_of_lt (by omega)] at h; omega)]

/-- **`∑_{x ∣ c} g(x) = φ(c)`** for `1 ≤ c ≤ R` (sum over `x ≤ R`). -/
theorem gM_divisor_sum (R c : Nat) (hc : c ∈ rng R) :
    ((rng R).map fun x => if c % x = 0 then gM x else 0).sum = (totient c : Rat) := by
  calc ((rng R).map fun x => if c % x = 0 then gM x else 0).sum
      = ((rng R).map fun x => ((rng R).map fun v =>
          (if x % v = 0 ∧ c % x = 0 then (mu (x / v) : Rat) else 0) * (totient v : Rat)).sum).sum := by
        apply rsum_congr; intro x hx
        rw [gM_range R x hx]
        by_cases hcx : c % x = 0
        · rw [ite_eq_left hcx]; apply rsum_congr; intro v _
          by_cases hxv : x % v = 0 <;> simp [hxv, hcx]
        · rw [ite_eq_right hcx, rsum_congr (g := fun _ => 0), rsum_zero]
          intro v _; simp [hcx]
    _ = ((rng R).map fun v => ((rng R).map fun x =>
          (if x % v = 0 ∧ c % x = 0 then (mu (x / v) : Rat) else 0) * (totient v : Rat)).sum).sum :=
        rsum_comm _ _ _
    _ = ((rng R).map fun v => if v = c then (totient c : Rat) else 0).sum := by
        apply rsum_congr; intro v hv
        rw [rsum_mul_right, mob1_lower R v c hv hc]
        by_cases h : v = c
        · subst h; simp
        · simp [h]
    _ = (totient c : Rat) := rsum_delta_rng R c hc _

/-- One coordinate of (5.21): `φ(gcd(a,b)) = ∑_{x ≤ R, x ∣ a, x ∣ b} g(x)` for `1 ≤ a ≤ R`. -/
theorem phi_gcd_sum_rat (R a b : Nat) (ha : a ∈ rng R) :
    ((totient (Nat.gcd a b) : Nat) : Rat)
      = ((rng R).map fun x => if (a % x == 0 && b % x == 0) = true then gM x else 0).sum := by
  obtain ⟨h1, h2⟩ := mem_rng.mp ha
  have hg1 : 0 < Nat.gcd a b := Nat.gcd_pos_of_pos_left _ (by omega)
  have hgR : Nat.gcd a b ≤ R := Nat.le_trans (Nat.gcd_le_left _ (by omega)) h2
  rw [← gM_divisor_sum R (Nat.gcd a b) (mem_rng.mpr ⟨hg1, hgR⟩)]
  apply rsum_congr; intro x _
  have key : ((a % x == 0 && b % x == 0) = true) ↔ (Nat.gcd a b % x = 0) := by
    simp only [Bool.and_eq_true, beq_iff_eq, ← Nat.dvd_iff_mod_eq_zero]
    exact Nat.dvd_gcd_iff.symm
  by_cases h : Nat.gcd a b % x = 0
  · rw [ite_eq_left h, ite_eq_left (key.mpr h)]
  · rw [ite_eq_right h, ite_eq_right (fun e => h (key.mp e))]

/-! ## Tuples -/

/-- `∏ᵢ g(uᵢ)`. -/
def tg (u : List Nat) : Rat := (u.map gM).prod

/-- `∏ᵢ φ(gcd(dᵢ, eᵢ))` as a rational. -/
def tphiGcd (d e : List Nat) : Rat := ((((List.zipWith Nat.gcd d e).map totient).prod : Nat) : Rat)

/-- `∏ᵢ φ(lcm(dᵢ, eᵢ))` as a rational (Maynard's `∏ᵢ φ([dᵢ, eᵢ])`). -/
def tphiLcm (d e : List Nat) : Rat := ((((List.zipWith Nat.lcm d e).map totient).prod : Nat) : Rat)

/-- **Tensorised (5.21) numerator.** For `d, e ∈ {1,…,R}^k`,
`∏ᵢ φ(gcd(dᵢ,eᵢ)) = ∑_{u ∈ {1,…,R}^k, u ∣ d, u ∣ e} ∏ᵢ g(uᵢ)`. -/
theorem tphiGcd_eq_sum (R : Nat) : ∀ (k : Nat) (d e : List Nat), d ∈ box R k → e ∈ box R k →
    tphiGcd d e = ((box R k).map fun u =>
      if (tdvd u d && tdvd u e) = true then tg u else 0).sum
  | 0, d, e, hd, he => by
    rw [box_zero, List.mem_singleton] at hd he; subst hd; subst he
    simp [box_zero, tphiGcd, tdvd, tg, Rat.add_zero]
  | k + 1, d, e, hd, he => by
    obtain ⟨a, d', rfl, ha, hd'⟩ := mem_box_succ hd
    obtain ⟨b, e', rfl, _, he'⟩ := mem_box_succ he
    rw [rsum_box_succ]
    have hsplit : tphiGcd (a :: d') (b :: e')
        = ((totient (Nat.gcd a b) : Nat) : Rat) * tphiGcd d' e' := by
      simp only [tphiGcd, List.zipWith_cons_cons, List.map_cons, List.prod_cons, Rat.natCast_mul]
    rw [hsplit, phi_gcd_sum_rat R a b ha, ← rsum_mul_right]
    apply rsum_congr; intro x _
    rw [tphiGcd_eq_sum R k d' e' hd' he', ← rsum_mul_left]
    apply rsum_congr; intro t _
    simp only [tdvd, tg, List.map_cons, List.prod_cons]
    cases a % x == 0 <;> cases b % x == 0 <;> cases tdvd t d' <;> cases tdvd t e' <;>
      simp [Rat.mul_zero, Rat.zero_mul]

/-- **Generic diagonalisation.** If `K(d,e) = ∑_{u ∣ d, u ∣ e} c(u)` on the box, then for all `w`,
`∑_{d,e} w_d w_e K(d,e) = ∑_u c(u) (∑_{u ∣ d} w_d)²`. -/
theorem quad_diag (R k : Nat) (c : List Nat → Rat) (K : List Nat → List Nat → Rat)
    (hK : ∀ d ∈ box R k, ∀ e ∈ box R k, K d e = ((box R k).map fun u =>
      if (tdvd u d && tdvd u e) = true then c u else 0).sum)
    (w : List Nat → Rat) :
    ((box R k).map fun d => ((box R k).map fun e => w d * w e * K d e).sum).sum
      = ((box R k).map fun u => c u * (upSum R k w u * upSum R k w u)).sum := by
  generalize hB : box R k = B at hK
  let x : List Nat → List Nat → Rat := fun u d => if tdvd u d = true then w d else 0
  have hA : ∀ d ∈ B, ∀ e ∈ B, w d * w e * K d e
      = (B.map fun u => c u * (x u d * x u e)).sum := by
    intro d hd e he
    rw [hK d hd e he, ← rsum_mul_left]
    apply rsum_congr; intro u _
    simp only [x]
    cases tdvd u d <;> cases tdvd u e <;> simp <;> grind
  calc (B.map fun d => (B.map fun e => w d * w e * K d e).sum).sum
      = (B.map fun d => (B.map fun e =>
          (B.map fun u => c u * (x u d * x u e)).sum).sum).sum := by
        apply rsum_congr; intro d hd; apply rsum_congr; intro e he; exact hA d hd e he
    _ = (B.map fun d => (B.map fun u =>
          (B.map fun e => c u * (x u d * x u e)).sum).sum).sum := by
        apply rsum_congr; intro d _
        exact rsum_comm (fun e u => c u * (x u d * x u e)) B B
    _ = (B.map fun u => (B.map fun d =>
          (B.map fun e => c u * (x u d * x u e)).sum).sum).sum :=
        rsum_comm (fun d u => (B.map fun e => c u * (x u d * x u e)).sum) B B
    _ = (B.map fun u => c u * (upSum R k w u * upSum R k w u)).sum := by
        apply rsum_congr; intro u _
        unfold upSum; rw [hB]
        change _ = c u * ((B.map (x u)).sum * (B.map (x u)).sum)
        rw [← rsum_mul_right, ← rsum_mul_left]
        apply rsum_congr; intro d _
        rw [← rsum_mul_left, ← rsum_mul_left]

/-! ## Maynard's `y^{(m)}` (5.23) and the diagonal form (5.24)/(5.26) -/

/-- The weight `[d_m = 1] λ_d / ∏ᵢ φ(dᵢ)`. -/
def fS2 (m : Nat) (lam : List Nat → Rat) (d : List Nat) : Rat :=
  if d.getD m 1 = 1 then lam d / tphi d else 0

/-- Maynard's (5.23): `y^{(m)}_r = ∏ᵢ μ(rᵢ) g(rᵢ) · ∑_{r ∣ d, d_m = 1} λ_d / ∏ᵢ φ(dᵢ)`
(sum over the box `{1,…,R}^k`). -/
def yS2 (R k m : Nat) (lam : List Nat → Rat) (r : List Nat) : Rat :=
  tmu r * tg r * upSum R k (fS2 m lam) r

/-- The `S₂` main-term quadratic form in the `φ(gcd)` normalisation of (5.21). -/
def s2Form (R k m : Nat) (lam : List Nat → Rat) : Rat :=
  (((box R k).filter fun d => d.getD m 1 == 1).map fun d =>
    (((box R k).filter fun e => e.getD m 1 == 1).map fun e =>
      lam d * lam e * tphiGcd d e / (tphi d * tphi e)).sum).sum

/-- **Diagonalisation of the `S₂` form, `g`-version.** For every `λ` on the box:
`∑_{d_m = e_m = 1} λ_d λ_e ∏φ(gcd(dᵢ,eᵢ)) / (φ(d) φ(e)) = ∑_u ∏ᵢ g(uᵢ) (∑_{u ∣ d, d_m = 1} λ_d/φ(d))²`. -/
theorem maynard_S2_diag_g (R k m : Nat) (lam : List Nat → Rat) :
    s2Form R k m lam
      = ((box R k).map fun u => tg u * (upSum R k (fS2 m lam) u * upSum R k (fS2 m lam) u)).sum := by
  rw [← quad_diag R k tg tphiGcd (fun d hd e he => tphiGcd_eq_sum R k d e hd he) (fS2 m lam)]
  unfold s2Form
  rw [← MaynardS1Diag.rsum_filter_of_zero (fun d => d.getD m 1 == 1) _ (box R k)
    (fun d _ hP => by
      have : fS2 m lam d = 0 := by
        unfold fS2; rw [ite_eq_right]; intro h; rw [h] at hP; simp at hP
      rw [rsum_congr (g := fun _ => 0), rsum_zero]
      intro e _; rw [this]; simp)]
  apply rsum_congr; intro d hd
  have hd1 : d.getD m 1 = 1 := by simpa using (List.mem_filter.mp hd).2
  rw [← MaynardS1Diag.rsum_filter_of_zero (fun e => e.getD m 1 == 1) _ (box R k)
    (fun e _ hP => by
      have : fS2 m lam e = 0 := by
        unfold fS2; rw [ite_eq_right]; intro h; rw [h] at hP; simp at hP
      rw [this]; simp)]
  apply rsum_congr; intro e he
  have he1 : e.getD m 1 = 1 := by simpa using (List.mem_filter.mp he).2
  unfold fS2
  rw [ite_eq_left hd1, ite_eq_left he1]
  grind

theorem tdvd_getD : ∀ (r d : List Nat) (m : Nat), tdvd r d = true →
    d.getD m 1 % r.getD m 1 = 0
  | [], [], _, _ => by simp
  | a :: r, b :: d, 0, h => by
    simp only [tdvd, Bool.and_eq_true, beq_iff_eq] at h; simpa using h.1
  | a :: r, b :: d, m + 1, h => by
    simp only [tdvd, Bool.and_eq_true, beq_iff_eq] at h; simpa using tdvd_getD r d m h.2
  | [], _ :: _, _, h => by simp [tdvd] at h
  | _ :: _, [], _, h => by simp [tdvd] at h

/-- **`y^{(m)}_r = 0` unless `r_m = 1`** (remark after (5.23)). -/
theorem yS2_eq_zero (R k m : Nat) (lam : List Nat → Rat) (r : List Nat)
    (hr : r.getD m 1 ≠ 1) : yS2 R k m lam r = 0 := by
  have : upSum R k (fS2 m lam) r = 0 := by
    unfold upSum
    rw [rsum_congr (g := fun _ => 0), rsum_zero]
    intro d _
    by_cases h : tdvd r d = true
    · rw [ite_eq_left h]
      unfold fS2
      rw [ite_eq_right]
      intro hd
      have h1 := tdvd_getD r d m h
      rw [hd] at h1
      generalize r.getD m 1 = x at h1 hr
      rcases x with _ | _ | x
      · simp at h1
      · exact hr rfl
      · rw [Nat.mod_eq_of_lt (by omega)] at h1; omega
    · rw [ite_eq_right h]
  unfold yS2; rw [this, Rat.mul_zero]

/-- **Maynard's (5.24)/(5.26) main term, exact.** If `λ` is supported on tuples with squarefree
entries, then
`∑_{d_m = e_m = 1} λ_d λ_e ∏φ(gcd(dᵢ,eᵢ)) / (φ(d) φ(e)) = ∑_u (y^{(m)}_u)² / ∏ᵢ g(uᵢ)`. -/
theorem maynard_S2_diag_y (R k m : Nat) (lam : List Nat → Rat)
    (hsq : ∀ d ∈ box R k, lam d ≠ 0 → ∀ x ∈ d, mu x ≠ 0) :
    s2Form R k m lam
      = ((box R k).map fun u => yS2 R k m lam u * yS2 R k m lam u / tg u).sum := by
  rw [maynard_S2_diag_g]
  apply rsum_congr; intro u _
  have hs : tmu u * tmu u = 1 ∨ upSum R k (fS2 m lam) u = 0 := by
    apply Classical.byCases (p := ∃ d ∈ box R k, tdvd u d = true ∧ fS2 m lam d ≠ 0)
    · rintro ⟨d, hd, hud, hl⟩
      left
      have hl' : lam d ≠ 0 := by
        intro h0; apply hl; unfold fS2; simp [h0, rat_div_zero]
      apply tmu_sq_of_tdvd u d hud
      intro y hy
      have hy1 := (mem_rng.mp ((mem_box_entries hd).2 y hy)).1
      exact ⟨hy1, sqf_of_mu y hy1 (hsq d hd hl' y hy)⟩
    · intro hn
      right
      unfold upSum
      rw [rsum_congr (g := fun _ => 0), rsum_zero]
      intro d hd
      by_cases hud : tdvd u d = true
      · have : fS2 m lam d = 0 := Classical.byContradiction fun hl => hn ⟨d, hd, hud, hl⟩
        simp [hud, this]
      · simp [hud]
  unfold yS2
  generalize upSum R k (fS2 m lam) u = U at hs ⊢
  by_cases hg : tg u = 0
  · rw [hg]; simp [Rat.mul_zero, Rat.zero_mul, rat_div_zero]
  · rcases hs with h | h
    · have : tmu u * tg u * U * (tmu u * tg u * U) / tg u
          = (tmu u * tmu u) * (tg u * (U * U)) := by grind
      rw [this, h, Rat.one_mul]
    · subst h; simp [Rat.mul_zero, rat_div_zero]

/-- The `u`-sum in `maynard_S2_diag_y` may be restricted to `u_m = 1`. -/
theorem maynard_S2_diag_y_restrict (R k m : Nat) (lam : List Nat → Rat)
    (hsq : ∀ d ∈ box R k, lam d ≠ 0 → ∀ x ∈ d, mu x ≠ 0) :
    s2Form R k m lam
      = (((box R k).filter fun u => u.getD m 1 == 1).map fun u =>
          yS2 R k m lam u * yS2 R k m lam u / tg u).sum := by
  rw [maynard_S2_diag_y R k m lam hsq, MaynardS1Diag.rsum_filter_of_zero]
  intro u _ hP
  have : u.getD m 1 ≠ 1 := by intro h; rw [h] at hP; simp at hP
  rw [yS2_eq_zero R k m lam u this]; simp [rat_div_zero]

/-! ## The `1/φ([d,e])` form (5.21) -/

theorem natprod_phi_lcm_gcd (R : Nat)
    (hphi : ∀ a b, a ∈ rng R → b ∈ rng R → mu a ≠ 0 → mu b ≠ 0 →
      totient (Nat.lcm a b) * totient (Nat.gcd a b) = totient a * totient b) :
    ∀ d e : List Nat, d.length = e.length → (∀ x ∈ d, x ∈ rng R ∧ mu x ≠ 0) →
      (∀ x ∈ e, x ∈ rng R ∧ mu x ≠ 0) →
      ((List.zipWith Nat.lcm d e).map totient).prod * ((List.zipWith Nat.gcd d e).map totient).prod
        = (d.map totient).prod * (e.map totient).prod
  | [], [], _, _, _ => rfl
  | a :: d, b :: e, hl, hd, he => by
    simp only [List.zipWith_cons_cons, List.map_cons, List.prod_cons]
    have ih := natprod_phi_lcm_gcd R hphi d e (by simpa using hl)
      (fun x hx => hd x (List.mem_cons_of_mem _ hx)) (fun x hx => he x (List.mem_cons_of_mem _ hx))
    have ha := hd a List.mem_cons_self
    have hb := he b List.mem_cons_self
    have h1 := hphi a b ha.1 hb.1 ha.2 hb.2
    calc totient (Nat.lcm a b) * ((List.zipWith Nat.lcm d e).map totient).prod *
          (totient (Nat.gcd a b) * ((List.zipWith Nat.gcd d e).map totient).prod)
        = (totient (Nat.lcm a b) * totient (Nat.gcd a b)) *
            (((List.zipWith Nat.lcm d e).map totient).prod *
              ((List.zipWith Nat.gcd d e).map totient).prod) := by ac_rfl
      _ = (totient a * totient b) * ((d.map totient).prod * (e.map totient).prod) := by rw [h1, ih]
      _ = totient a * (d.map totient).prod * (totient b * (e.map totient).prod) := by ac_rfl
  | [], _ :: _, hl, _, _ => by simp at hl
  | _ :: _, [], hl, _, _ => by simp at hl

/-- **(5.21)-form of the diagonalisation.** If `φ([a,b]) φ((a,b)) = φ(a) φ(b)` for squarefree
`a, b ≤ R` and `λ` is supported on tuples with squarefree entries, then
`∑_{d_m = e_m = 1} λ_d λ_e / ∏ᵢ φ([dᵢ,eᵢ]) = ∑_u (y^{(m)}_u)² / ∏ᵢ g(uᵢ)`. -/
theorem maynard_S2_diag_lcm (R k m : Nat) (lam : List Nat → Rat)
    (hphi : ∀ a b, a ∈ rng R → b ∈ rng R → mu a ≠ 0 → mu b ≠ 0 →
      totient (Nat.lcm a b) * totient (Nat.gcd a b) = totient a * totient b)
    (hsq : ∀ d ∈ box R k, lam d ≠ 0 → ∀ x ∈ d, mu x ≠ 0) :
    (((box R k).filter fun d => d.getD m 1 == 1).map fun d =>
      (((box R k).filter fun e => e.getD m 1 == 1).map fun e =>
        lam d * lam e / tphiLcm d e).sum).sum
      = ((box R k).map fun u => yS2 R k m lam u * yS2 R k m lam u / tg u).sum := by
  rw [← maynard_S2_diag_y R k m lam hsq]
  unfold s2Form
  apply rsum_congr; intro d hd
  apply rsum_congr; intro e he
  have hdB := (List.mem_filter.mp hd).1
  have heB := (List.mem_filter.mp he).1
  by_cases h0 : lam d * lam e = 0
  · rw [h0]; simp [rat_div_zero]
  · have hld : lam d ≠ 0 := fun h => h0 (by rw [h, Rat.zero_mul])
    have hle : lam e ≠ 0 := fun h => h0 (by rw [h, Rat.mul_zero])
    have hN := natprod_phi_lcm_gcd R hphi d e
      (by rw [(mem_box_entries hdB).1, (mem_box_entries heB).1])
      (fun x hx => ⟨(mem_box_entries hdB).2 x hx, hsq d hdB hld x hx⟩)
      (fun x hx => ⟨(mem_box_entries heB).2 x hx, hsq e heB hle x hx⟩)
    have hQ : tphiLcm d e * tphiGcd d e = tphi d * tphi e := by
      unfold tphiLcm tphiGcd tphi
      rw [← Rat.natCast_mul, ← Rat.natCast_mul, hN]
    have hpd := tphi_ne_zero hdB
    have hpe := tphi_ne_zero heB
    have hL : tphiLcm d e ≠ 0 := by
      intro h; rw [h, Rat.zero_mul] at hQ
      rcases Rat.mul_eq_zero.mp hQ.symm with h' | h' <;> contradiction
    have hG : tphiGcd d e ≠ 0 := by
      intro h; rw [h, Rat.mul_zero] at hQ
      rcases Rat.mul_eq_zero.mp hQ.symm with h' | h' <;> contradiction
    rw [← hQ]
    grind

set_option maxRecDepth 100000 in
/-- `φ([a,b]) φ((a,b)) = φ(a) φ(b)` for all `1 ≤ a, b ≤ 12` (kernel `decide`). -/
theorem phi_lcm_gcd_upto_12 : ∀ a, a < 13 → ∀ b, b < 13 →
    totient (Nat.lcm a b) * totient (Nat.gcd a b) = totient a * totient b := by
  decide +kernel

/-- **(5.21)-form, unconditional for `R ≤ 12`.** -/
theorem maynard_S2_diag_lcm_R12 (R k m : Nat) (hR : R ≤ 12) (lam : List Nat → Rat)
    (hsq : ∀ d ∈ box R k, lam d ≠ 0 → ∀ x ∈ d, mu x ≠ 0) :
    (((box R k).filter fun d => d.getD m 1 == 1).map fun d =>
      (((box R k).filter fun e => e.getD m 1 == 1).map fun e =>
        lam d * lam e / tphiLcm d e).sum).sum
      = ((box R k).map fun u => yS2 R k m lam u * yS2 R k m lam u / tg u).sum :=
  maynard_S2_diag_lcm R k m lam (fun a b ha hb _ _ =>
    phi_lcm_gcd_upto_12 a (by have := (mem_rng.mp ha).2; omega)
      b (by have := (mem_rng.mp hb).2; omega)) hsq

/-! ## Inversion of (5.23) -/

/-- **Inversion of Maynard's (5.23).** For `λ` supported on tuples with squarefree entries, and
assuming `∑_{r ∣ d, d_m = 1} λ_d/φ(d) = 0` whenever `∏ g(rᵢ) = 0` (`hg`; on Maynard's support,
odd entries, this is automatic once `g(r) ≠ 0` for odd squarefree `r`), for every `d` in the box:
`μ(d) φ(d) ∑_{d ∣ r} y^{(m)}_r / g(r) = [d_m = 1] λ_d`. -/
theorem maynard_S2_lam_of_y (R k m : Nat) (lam : List Nat → Rat)
    (hsq : ∀ d ∈ box R k, lam d ≠ 0 → ∀ x ∈ d, mu x ≠ 0)
    (hg : ∀ r ∈ box R k, tg r = 0 → upSum R k (fS2 m lam) r = 0)
    (d : List Nat) (hd : d ∈ box R k) :
    tmu d * tphi d * upSum R k (fun r => yS2 R k m lam r / tg r) d
      = if d.getD m 1 = 1 then lam d else 0 := by
  have h1 : upSum R k (fun r => yS2 R k m lam r / tg r) d
      = ((box R k).map fun r => if tdvd d r = true then
          tmu r * upSum R k (fS2 m lam) r else 0).sum := by
    unfold upSum
    apply rsum_congr; intro r hr
    split
    · unfold yS2
      by_cases h0 : tg r = 0
      · have := hg r hr h0
        unfold upSum at this
        rw [this]; dsimp only; rw [h0]; simp [Rat.mul_zero, rat_div_zero]
      · exact rat_cancel1 _ _ _ h0
    · rfl
  have hS' : ∀ e ∈ box R k, fS2 m lam e ≠ 0 → SignOK e := by
    intro e he hne
    have hl : lam e ≠ 0 := by intro h0; apply hne; unfold fS2; simp [h0, rat_div_zero]
    apply signOK_of_entries e
    intro c hc
    exact muSign_of_sqfree c (mem_rng.mp ((mem_box_entries he).2 c hc)).1 (hsq e he hl c hc)
  rw [h1, Rat.mul_comm (tmu d), Rat.mul_assoc, signed_sum R k _ d hS',
    mobInv_upSum R k _ d hd]
  unfold fS2
  split
  · exact rat_cancel2 _ _ (tphi_ne_zero hd)
  · rw [Rat.mul_zero]

/-! ## Checks -/

/-- `g(1) = 1`, `g(2) = 0`, `g(3) = 1`, `g(5) = 3`, `g(15) = 3 = g(3) g(5)`, `g(4) = 1 ≠ g(2)²`
(`gM = μ ∗ φ` is not totally multiplicative; only squarefree arguments matter). -/
theorem gM_values : gM 1 = 1 ∧ gM 2 = 0 ∧ gM 3 = 1 ∧ gM 5 = 3 ∧ gM 15 = 3 ∧ gM 4 = 1 := by
  decide +kernel

/-- Example weights on `{1,2,3}²`: `λ(1,1) = 2`, `λ(1,3) = -1`, `λ = 0` otherwise. -/
def lamEx (d : List Nat) : Rat := if d = [1, 1] then 2 else if d = [1, 3] then -1 else 0

theorem ex_hsq : ∀ d ∈ box 3 2, lamEx d ≠ 0 → ∀ x ∈ d, mu x ≠ 0 := by decide +kernel

theorem ex_hg : ∀ r ∈ box 3 2, tg r = 0 → upSum 3 2 (fS2 0 lamEx) r = 0 := by decide +kernel

/-- Both sides of `maynard_S2_diag_y` for `lamEx` (`R = 3`, `k = 2`, `m = 0`) equal `5/2`. -/
theorem maynard_S2_diag_example :
    s2Form 3 2 0 lamEx = 5 / 2 ∧
      ((box 3 2).map fun u => yS2 3 2 0 lamEx u * yS2 3 2 0 lamEx u / tg u).sum = 5 / 2 := by
  decide +kernel

/-- `maynard_S2_diag_lcm_R12` with all hypotheses discharged, for `lamEx`. -/
theorem maynard_S2_diag_lcm_example :
    (((box 3 2).filter fun d => d.getD 0 1 == 1).map fun d =>
      (((box 3 2).filter fun e => e.getD 0 1 == 1).map fun e =>
        lamEx d * lamEx e / tphiLcm d e).sum).sum
      = ((box 3 2).map fun u => yS2 3 2 0 lamEx u * yS2 3 2 0 lamEx u / tg u).sum :=
  maynard_S2_diag_lcm_R12 3 2 0 (by decide) lamEx ex_hsq

/-- `maynard_S2_lam_of_y` with all hypotheses discharged, for `lamEx`. -/
theorem maynard_S2_lam_of_y_example (d : List Nat) (hd : d ∈ box 3 2) :
    tmu d * tphi d * upSum 3 2 (fun r => yS2 3 2 0 lamEx r / tg r) d
      = if d.getD 0 1 = 1 then lamEx d else 0 :=
  maynard_S2_lam_of_y 3 2 0 lamEx ex_hsq ex_hg d hd

/-- `y^{(0)}_{(1,3)} = μ(3) g(3) λ(1,3)/φ(3) = 1/2` and `y^{(0)}_{(3,1)} = 0` (since `r_0 ≠ 1`). -/
theorem ex_y_values : yS2 3 2 0 lamEx [1, 3] = 1 / 2 ∧ yS2 3 2 0 lamEx [3, 1] = 0 := by
  decide +kernel

end MaynardS2Y
end TwinPrimes
