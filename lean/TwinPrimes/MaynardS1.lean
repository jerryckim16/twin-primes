import TwinPrimes.Counting

/-!
# Finite part of the `k`-dimensional Maynard sum `S₁`

Maynard (2015, Sect. 5) uses `k`-dimensional weights `λ_{d₁,…,d_k}` and the sum

  `S₁ = ∑_{n < N, n ≡ v₀ (W)} (∑_{dᵢ ∣ n + hᵢ ∀ i} λ_{d₁,…,d_k})²`.

This file checks the purely finite, combinatorial part of its evaluation in core Lean
(no reals, no Mathlib, list-based sums; it reuses the helpers of `Counting.lean`).
A divisor tuple is a `ds : List Nat`, the shifts are `hs : List Nat` (index `i` runs over
`ds.zip hs`), the support is a finite list `Dk : List (List Nat)` and the weights are
`lam : List Nat → Int`.

Formalised:
* `tupleDvd`, `mSieveSum`: the condition `∀ i, dsᵢ ∣ n + hᵢ` and the weight
  `∑_{ds ∈ Dk, dsᵢ ∣ n+hᵢ} λ_ds`;
* `maynard_S1_expand` (all `n < N`) and `maynard_S1_expand_W` (`n ≡ v₀ (W)`): the exact
  expansion `S₁ = ∑_{ds,es ∈ Dk} λ_ds λ_es · #{n < N : [n ≡ v₀ (W)], ∀ i, dsᵢ ∣ n+hᵢ ∧ esᵢ ∣ n+hᵢ}`
  (no coprimality, positivity or length hypotheses);
* `tupleDvd_lcm`: for tuples of length `k`, the two conditions are `lcm(dsᵢ, esᵢ) ∣ n + hᵢ`;
* `crt_tuple_residue`, `crt_tuple_count_bounds`: CRT for `k` pairwise coprime moduli `Lᵢ`
  coprime to `W` — the conditions `n ≡ v₀ (W)`, `Lᵢ ∣ n + hᵢ` form a single residue class mod
  `W ∏ Lᵢ`, so the count is `N / (W ∏ Lᵢ)` up to an error `< 1` (division-free);
* `maynard_S1_error`: if the entries of all tuples are positive and coprime to `W`, and for all
  `ds, es ∈ Dk` the `lcm(dsᵢ, esᵢ)` are pairwise coprime across `i`, then for any common
  multiple `M` of the `∏ᵢ lcm(dsᵢ, esᵢ)`,
  `|W M · S₁ − N ∑_{ds,es} λ_ds λ_es (M / ∏ᵢ lcm(dsᵢ,esᵢ))| ≤ W M ∑_{ds,es} |λ_ds λ_es|`,
  i.e. `|S₁ − (N/W) ∑ λ_ds λ_es / ∏ᵢ lcm(dsᵢ,esᵢ)| ≤ ∑ |λ_ds λ_es|`.
  (`W = 1`, `v₀ = 0` gives the unrestricted version.)

Formalised elsewhere: the change of variables `λ ↦ y_r` (Maynard's Lemma 5.1 / Möbius
inversion over tuples) in `MaynardInv.lean`, and the diagonalisation of the main-term quadratic
form `∑ λ_d λ_e / ∏ lcm(dᵢ,eᵢ) = ∑_u y_u² / φ(u)` in `MaynardDiag.lean`.
NOT formalised here: the
asymptotic evaluation of `(N/W) ∑ λ_ds λ_es / ∏ lcm(dsᵢ,esᵢ)` in terms of the smooth function
`F`, the size bound on the error sum `∑ |λ_ds λ_es|`, and the treatment of pairs whose
`lcm`s are not pairwise coprime (Maynard shows their count vanishes, since a common prime
`p ∣ dsᵢ, esⱼ` with `i ≠ j` would divide `hᵢ − hⱼ`, hence `W`; here pairwise coprimality is
simply assumed for all pairs in `Dk × Dk`).
-/

namespace TwinPrimes

/-- Generic square expansion of a filtered sieve sum. -/
theorem msq_expand_gen {α} (D : List α) (P : α → Nat → Bool) (f : α → Int)
    (g : Nat → Bool) (N : Nat) :
    ((List.range N).map fun n => if g n = true then
        (D.map fun a => if P a n = true then f a else 0).sum
          * (D.map fun a => if P a n = true then f a else 0).sum else 0).sum
      = (D.map fun a => (D.map fun b =>
          f a * f b * (((List.range N).countP fun n => g n && P a n && P b n : Nat) : Int)).sum).sum := by
  have h1 : ∀ n, (if g n = true then
        (D.map fun a => if P a n = true then f a else 0).sum
          * (D.map fun a => if P a n = true then f a else 0).sum else 0)
      = (D.map fun a => (D.map fun b =>
          if (g n && P a n && P b n) = true then f a * f b else 0).sum).sum := by
    intro n
    cases hg : g n
    · simp only [Bool.false_and, Bool.false_eq_true, ite_false]
      rw [isum_congr (fun d _ => isum_zero D)]
      exact (isum_zero D).symm
    · simp only [ite_true, Bool.true_and]
      rw [isum_sq]
      apply isum_congr; intro a _; apply isum_congr; intro b _
      cases P a n <;> cases P b n <;> simp
  rw [isum_congr (fun n _ => h1 n), isum_comm]
  apply isum_congr; intro a _
  rw [isum_comm]
  apply isum_congr; intro b _
  exact isum_ite_count (fun n => g n && P a n && P b n) _ _


/-- `ds` divides the shifted tuple at `n`: `∀ i, ds_i ∣ n + h_i` (as `(n + h_i) % ds_i = 0`),
the index running over `ds.zip hs`. -/
def tupleDvd (hs : List Nat) (n : Nat) (ds : List Nat) : Bool :=
  (ds.zip hs).all fun p => (n + p.2) % p.1 == 0

/-- The `k`-dimensional sieve weight `∑_{ds ∈ Dk, ds_i ∣ n + h_i ∀ i} λ_{ds}`. -/
def mSieveSum (Dk : List (List Nat)) (hs : List Nat) (lam : List Nat → Int) (n : Nat) : Int :=
  (Dk.map fun ds => if tupleDvd hs n ds = true then lam ds else 0).sum

/-- Exact expansion of the `k`-dimensional `S₁` (no coprimality needed):
`∑_{n<N} (∑_{ds_i ∣ n+h_i} λ_ds)² = ∑_{ds,es ∈ Dk} λ_ds λ_es · #{n < N : ∀ i, ds_i ∣ n+h_i ∧ es_i ∣ n+h_i}`. -/
theorem maynard_S1_expand (Dk : List (List Nat)) (hs : List Nat) (lam : List Nat → Int) (N : Nat) :
    ((List.range N).map fun n => mSieveSum Dk hs lam n * mSieveSum Dk hs lam n).sum
      = (Dk.map fun ds => (Dk.map fun es =>
          lam ds * lam es * (((List.range N).countP fun n =>
            tupleDvd hs n ds && tupleDvd hs n es : Nat) : Int)).sum).sum := by
  have := msq_expand_gen Dk (fun ds n => tupleDvd hs n ds) lam (fun _ => true) N
  simp only [ite_true, Bool.true_and] at this
  exact this

/-- The same expansion restricted to `n ≡ v₀ (mod W)`:
`∑_{n<N, n%W=v₀} (∑_{ds_i ∣ n+h_i} λ_ds)² = ∑_{ds,es} λ_ds λ_es · #{n < N : n%W = v₀, ∀ i, ds_i ∣ n+h_i ∧ es_i ∣ n+h_i}`. -/
theorem maynard_S1_expand_W (Dk : List (List Nat)) (hs : List Nat) (lam : List Nat → Int)
    (W v0 N : Nat) :
    ((List.range N).map fun n =>
        if n % W = v0 then mSieveSum Dk hs lam n * mSieveSum Dk hs lam n else 0).sum
      = (Dk.map fun ds => (Dk.map fun es =>
          lam ds * lam es * (((List.range N).countP fun n =>
            n % W == v0 && tupleDvd hs n ds && tupleDvd hs n es : Nat) : Int)).sum).sum := by
  rw [← msq_expand_gen Dk (fun ds n => tupleDvd hs n ds) lam (fun n => n % W == v0) N]
  apply isum_congr; intro n _
  simp only [beq_iff_eq]
  rfl

/-! ## CRT for `k` pairwise coprime moduli -/

theorem beq_lcm (d e m : Nat) : (m % d == 0 && m % e == 0) = (m % Nat.lcm d e == 0) := by
  have hl := @lcm_dvd_iff d e m
  rw [Nat.dvd_iff_mod_eq_zero, Nat.dvd_iff_mod_eq_zero, Nat.dvd_iff_mod_eq_zero] at hl
  apply Bool.eq_iff_iff.mpr
  simp only [Bool.and_eq_true, beq_iff_eq]
  exact hl.symm

/-- For tuples of the same length as `hs`, the pair of divisibility conditions is the single
condition for the tuple of `lcm`s. -/
theorem tupleDvd_lcm : ∀ (hs ds es : List Nat) (n : Nat), ds.length = hs.length →
    es.length = hs.length →
    (tupleDvd hs n ds && tupleDvd hs n es) = tupleDvd hs n (List.zipWith Nat.lcm ds es)
  | [], [], [], _, _, _ => rfl
  | h :: hs, d :: ds, e :: es, n, h1, h2 => by
    have ih := tupleDvd_lcm hs ds es n (by simpa using h1) (by simpa using h2)
    unfold tupleDvd at ih ⊢
    simp only [List.zip_cons_cons, List.zipWith_cons_cons, List.all_cons]
    rw [← ih]
    have hb : ((n + h) % d == 0 && (n + h) % e == 0) = ((n + h) % Nat.lcm d e == 0) := by
      exact beq_lcm d e (n + h)
    rw [← hb]
    generalize ((n + h) % d == 0) = A
    generalize ((n + h) % e == 0) = B
    generalize ((ds.zip hs).all fun p => (n + p.2) % p.1 == 0) = X
    generalize ((es.zip hs).all fun p => (n + p.2) % p.1 == 0) = Y
    cases A <;> cases B <;> cases X <;> cases Y <;> rfl
  | [], _ :: _, _, _, h1, _ => by simp at h1
  | [], [], _ :: _, _, _, h2 => by simp at h2
  | _ :: _, [], _, _, h1, _ => by simp at h1
  | _ :: _, _ :: _, [], _, _, h2 => by simp at h2

theorem coprime_prod_of_forall {x : Nat} : ∀ {L : List Nat}, (∀ y ∈ L, Nat.Coprime x y) →
    Nat.Coprime x L.prod
  | [], _ => by simp [Nat.Coprime]
  | y :: L, h => by
    rw [List.prod_cons]
    exact Nat.Coprime.mul_right (h y List.mem_cons_self)
      (coprime_prod_of_forall fun z hz => h z (List.mem_cons_of_mem _ hz))

/-- CRT for `k` moduli: if the entries of `L` are positive, pairwise coprime and coprime to `W`,
`v₀ < W` and `L` has the length of `hs`, then `n ≡ v₀ (W)` and `L_i ∣ n + h_i` for all `i` cut out a
single residue class modulo `W · ∏ L_i`. -/
theorem crt_tuple_residue {W v0 : Nat} (hv : v0 < W) : ∀ (L hs : List Nat),
    L.length = hs.length → (∀ x ∈ L, 0 < x) → (∀ x ∈ L, Nat.gcd x W = 1) →
    L.Pairwise Nat.Coprime →
    ∃ r, r < W * L.prod ∧ ∀ n, (n % W = v0 ∧ tupleDvd hs n L = true) ↔ n % (W * L.prod) = r
  | [], [], _, _, _, _ => ⟨v0, by simp; exact hv, fun n => by simp [tupleDvd]⟩
  | x :: L, h :: hs, hlen, hpos, hW, hpw => by
    obtain ⟨r', hr', hiff⟩ := crt_tuple_residue hv L hs (by simpa using hlen)
      (fun y hy => hpos y (List.mem_cons_of_mem _ hy))
      (fun y hy => hW y (List.mem_cons_of_mem _ hy)) (List.pairwise_cons.mp hpw).2
    have hx : 0 < x := hpos x List.mem_cons_self
    have hc : Nat.gcd x (W * L.prod) = 1 :=
      Nat.Coprime.mul_right (hW x List.mem_cons_self)
        (coprime_prod_of_forall (List.pairwise_cons.mp hpw).1)
    obtain ⟨r, hr, hiff2⟩ := crt_residue h hr' hx hc
    have hm : W * (x :: L).prod = W * L.prod * x := by
      rw [List.prod_cons, Nat.mul_comm x, Nat.mul_assoc]
    refine ⟨r, hm ▸ hr, fun n => ?_⟩
    rw [hm, ← hiff2, ← hiff]
    simp only [tupleDvd, List.zip_cons_cons, List.all_cons, Bool.and_eq_true, beq_iff_eq]
    constructor
    · rintro ⟨a, b, c⟩; exact ⟨⟨a, c⟩, b⟩
    · rintro ⟨⟨a, c⟩, b⟩; exact ⟨a, b, c⟩
  | [], _ :: _, hlen, _, _, _ => by simp at hlen
  | _ :: _, [], hlen, _, _, _ => by simp at hlen

/-- CRT counting for `k` moduli, division-free: with `P = ∏ L_i` and
`c = #{n < N : n ≡ v₀ (W), L_i ∣ n + h_i ∀ i}`, `N < W P (c + 1)` and `W P c < N + W P`. -/
theorem crt_tuple_count_bounds {W v0 : Nat} (hv : v0 < W) (L hs : List Nat)
    (hlen : L.length = hs.length) (hpos : ∀ x ∈ L, 0 < x) (hW : ∀ x ∈ L, Nat.gcd x W = 1)
    (hpw : L.Pairwise Nat.Coprime) (N : Nat) :
    N < W * L.prod * ((List.range N).countP (fun n => n % W == v0 && tupleDvd hs n L) + 1) ∧
    W * L.prod * (List.range N).countP (fun n => n % W == v0 && tupleDvd hs n L)
      < N + W * L.prod := by
  obtain ⟨r, hr, hiff⟩ := crt_tuple_residue hv L hs hlen hpos hW hpw
  have heq : (List.range N).countP (fun n => n % W == v0 && tupleDvd hs n L)
      = countRes (W * L.prod) r N := by
    unfold countRes
    congr 1
    funext n
    rw [Bool.eq_iff_iff]
    simp only [Bool.and_eq_true, beq_iff_eq]
    exact hiff n
  rw [heq]
  have hP : 0 < W * L.prod := by omega
  obtain ⟨b1, b2⟩ := countRes_bounds hP hr N
  rw [Nat.mul_add, Nat.mul_one]
  omega

theorem mem_zipWith_exists {f : Nat → Nat → Nat} {x : Nat} : ∀ {l l' : List Nat},
    x ∈ List.zipWith f l l' → ∃ a ∈ l, ∃ b ∈ l', x = f a b
  | [], _, h => by simp at h
  | _ :: _, [], h => by simp at h
  | a :: l, b :: l', h => by
    rw [List.zipWith_cons_cons, List.mem_cons] at h
    rcases h with h | h
    · exact ⟨a, List.mem_cons_self, b, List.mem_cons_self, h⟩
    · obtain ⟨a', ha, b', hb, e⟩ := mem_zipWith_exists h
      exact ⟨a', List.mem_cons_of_mem _ ha, b', List.mem_cons_of_mem _ hb, e⟩

/-- Error term of the `k`-dimensional `S₁` on `n ≡ v₀ (mod W)`, division-free.  Hypotheses:
every tuple in `Dk` has length `k = |hs|`, positive entries coprime to `W`; for all
`ds, es ∈ Dk` the moduli `lcm(ds_i, es_i)` are pairwise coprime (across `i`); and `M` is a
common multiple of all `∏_i lcm(ds_i, es_i)`.  Then
`|W M · S₁ − N · ∑_{ds,es} λ_ds λ_es (M / ∏_i lcm(ds_i,es_i))| ≤ W M · ∑_{ds,es} |λ_ds λ_es|`,
i.e. `|S₁ − (N/W) ∑ λ_ds λ_es / ∏_i lcm(ds_i, es_i)| ≤ ∑ |λ_ds λ_es|` after dividing by `W M`. -/
theorem maynard_S1_error (Dk : List (List Nat)) (hs : List Nat) (lam : List Nat → Int)
    (W v0 N M : Nat) (hv : v0 < W)
    (hlen : ∀ ds ∈ Dk, ds.length = hs.length)
    (hpos : ∀ ds ∈ Dk, ∀ d ∈ ds, 0 < d)
    (hDW : ∀ ds ∈ Dk, ∀ d ∈ ds, Nat.gcd d W = 1)
    (hpw : ∀ ds ∈ Dk, ∀ es ∈ Dk, (List.zipWith Nat.lcm ds es).Pairwise Nat.Coprime)
    (hM : ∀ ds ∈ Dk, ∀ es ∈ Dk, (List.zipWith Nat.lcm ds es).prod ∣ M) :
    (((W * M : Nat) : Int) * ((List.range N).map fun n =>
          if n % W = v0 then mSieveSum Dk hs lam n * mSieveSum Dk hs lam n else 0).sum
      - (N : Int) * (Dk.map fun ds => (Dk.map fun es =>
          lam ds * lam es * ((M / (List.zipWith Nat.lcm ds es).prod : Nat) : Int)).sum).sum).natAbs
      ≤ W * M * (Dk.map fun ds => (Dk.map fun es => (lam ds * lam es).natAbs).sum).sum := by
  rw [maynard_S1_expand_W, ← isum_mul_left, ← isum_mul_left, ← isum_sub, ← nsum_mul_left]
  refine Nat.le_trans (natAbs_isum_le _ _) (nsum_le ?_)
  intro ds hds
  rw [← isum_mul_left, ← isum_mul_left, ← isum_sub, ← nsum_mul_left]
  refine Nat.le_trans (natAbs_isum_le _ _) (nsum_le ?_)
  intro es hes
  have hlenL : (List.zipWith Nat.lcm ds es).length = hs.length := by
    rw [List.length_zipWith, hlen ds hds, hlen es hes, Nat.min_self]
  have hposL : ∀ x ∈ List.zipWith Nat.lcm ds es, 0 < x := by
    intro x hx
    obtain ⟨a, ha, b, hb, rfl⟩ := mem_zipWith_exists hx
    exact Nat.lcm_pos (hpos ds hds a ha) (hpos es hes b hb)
  have hWL : ∀ x ∈ List.zipWith Nat.lcm ds es, Nat.gcd x W = 1 := by
    intro x hx
    obtain ⟨a, ha, b, hb, rfl⟩ := mem_zipWith_exists hx
    have hab : Nat.Coprime (a * b) W := Nat.Coprime.mul_left (hDW ds hds a ha) (hDW es hes b hb)
    exact Nat.Coprime.coprime_dvd_left
      (Nat.lcm_dvd (Nat.dvd_mul_right a b) (Nat.dvd_mul_left b a)) hab
  have hcount : ((List.range N).countP fun n =>
      n % W == v0 && tupleDvd hs n ds && tupleDvd hs n es)
      = (List.range N).countP fun n => n % W == v0 && tupleDvd hs n (List.zipWith Nat.lcm ds es) := by
    congr 1; funext n
    rw [Bool.and_assoc, tupleDvd_lcm hs ds es n (hlen ds hds) (hlen es hes)]
  rw [hcount]
  obtain ⟨b1, b2⟩ := crt_tuple_count_bounds hv _ hs hlenL hposL hWL (hpw ds hds es hes) N
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

/-- Non-vacuity check (`k = 2`, `hs = [0, 2]`, `N = 30`): both sides of the expansion agree. -/
theorem maynard_S1_expand_example :
    let Dk := [[1, 1], [3, 1], [1, 5], [3, 5]]
    let lam : List Nat → Int := fun ds => if ds = [1, 1] then 2 else -1
    ((List.range 30).map fun n => mSieveSum Dk [0, 2] lam n * mSieveSum Dk [0, 2] lam n).sum
      = (Dk.map fun ds => (Dk.map fun es => lam ds * lam es * (((List.range 30).countP fun n =>
          tupleDvd [0, 2] n ds && tupleDvd [0, 2] n es : Nat) : Int)).sum).sum := by
  decide

end TwinPrimes
