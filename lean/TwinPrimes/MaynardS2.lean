import TwinPrimes.MaynardHpw
import TwinPrimes.Basic

/-!
# Finite part of Maynard's `S₂^{(m)}` (Lemma 5.2 before any asymptotics)

Maynard (2015, Sect. 5, Lemma 5.2) evaluates, for a fixed index `m`,

  `S₂^{(m)} = ∑_{N₀ ≤ n < N, n ≡ v₀ (W)} 1[n + h_m prime] · (∑_{dᵢ ∣ n + hᵢ ∀ i} λ_{d₁,…,d_k})²`

(he takes `N₀ = N`, upper end `2N`). The first, purely algebraic, steps are: expand the square
and swap the sums; observe that if `d_m ∣ n + h_m` with `n + h_m` prime and `d_m < n + h_m`
then `d_m = 1` (Maynard: `λ` is supported on `∏ dᵢ < R ≤ N`), so only pairs `(d, e)` with
`d_m = e_m = 1` survive; for them the `m`-th divisibility condition is empty, and the remaining
conditions `[dᵢ, eᵢ] ∣ n + hᵢ` (`i ≠ m`) together with `n ≡ v₀ (W)` cut out a single residue
class modulo `q = W ∏_{i≠m} [dᵢ, eᵢ]`, so the inner count is a count of primes `n + h_m` in an
arithmetic progression (the quantity to which Bombieri–Vinogradov is then applied).

This file checks exactly these finite steps (core Lean, list sums over `ℤ`/`ℕ`, conventions of
`MaynardS1.lean`: `tupleDvd`, `mSieveSum`, support `Dk : List (List Nat)`, weights
`lam : List Nat → Int`). Primality enters only through an abstract Boolean indicator
`pr : Nat → Bool` with the soundness hypothesis `∀ p, pr p = true → IsPrime p` (`IsPrime` of
`Basic.lean`); the `m`-th coordinate of a tuple is `ds.getD m 1`, of the shifts `hs.getD m 0`.

* `maynard_S2_expand_W`: the exact expansion (no hypotheses)
  `S₂^{(m)} = ∑_{d,e ∈ Dk} λ_d λ_e #{N₀ ≤ n < N : n ≡ v₀ (W), pr(n+h_m), dᵢ,eᵢ ∣ n+hᵢ ∀ i}`;
* `prime_shift_coord_eq_one`, `count_zero_of_coord_ne_one`: a pair with `d_m ≠ 1` has count `0`
  if every `d ∈ Dk` has `d_m < N₀ + h_m`;
* `maynard_S2_support`: hence `S₂^{(m)}` equals the same double sum over `d, e ∈ Dk` with
  `d_m = e_m = 1` only;
* `maynard_S2_reduced`: for those pairs the `m`-th condition is dropped:
  `S₂^{(m)} = ∑_{d,e ∈ Dk, d_m = e_m = 1} λ_d λ_e
      #{N₀ ≤ n < N : n ≡ v₀ (W), pr(n+h_m), [dᵢ,eᵢ] ∣ n+hᵢ ∀ i ≠ m}`
  (the `(k−1)`-tuples are `List.eraseIdx _ m`);
* `maynard_S2_count_residue`: for such a pair with entries positive, coprime to `W`, and the
  `[dᵢ,eᵢ]` (`i ≠ m`) pairwise coprime, the inner count is
  `#{N₀ ≤ n < N : n ≡ r (mod W ∏_{i≠m} [dᵢ,eᵢ]), pr(n + h_m)}` for one residue `r`;
* `maynard_S2_example`: all hypotheses are satisfiable (`k = 2`, a concrete prime test).

NOT formalised (stays outside): the asymptotic evaluation of the AP prime counts
(`≈ X_N / φ(q)`), the Bombieri–Vinogradov input and the resulting error term, the condition
that `r + h_m` is coprime to `q` (Maynard's `(n + h_m, q) = 1` remark; a class with
`gcd(r + h_m, q) > 1` contains at most one prime), the change of variables to `y^{(m)}_r`
and the passage to the integral `J_k^{(m)}`.
-/

namespace TwinPrimes
namespace MaynardS2

/-! ## Coordinates of `tupleDvd` -/

/-- The `m`-th coordinate of a divisibility tuple: `tupleDvd hs n ds` gives `ds_m ∣ n + h_m`. -/
theorem tupleDvd_coord : ∀ (ds hs : List Nat) (m n : Nat), tupleDvd hs n ds = true →
    m < ds.length → m < hs.length → ds.getD m 1 ∣ n + hs.getD m 0
  | [], _, _, _, _, h, _ => by simp at h
  | _ :: _, [], _, _, _, _, h => by simp at h
  | d :: ds, h :: hs, 0, n, ht, _, _ => by
    simp only [tupleDvd, List.zip_cons_cons, List.all_cons, Bool.and_eq_true, beq_iff_eq] at ht
    exact Nat.dvd_of_mod_eq_zero ht.1
  | d :: ds, h :: hs, m + 1, n, ht, h1, h2 => by
    simp only [tupleDvd, List.zip_cons_cons, List.all_cons, Bool.and_eq_true] at ht
    exact tupleDvd_coord ds hs m n ht.2 (by simpa using h1) (by simpa using h2)

/-- If the `m`-th entry is `1`, the `m`-th condition is vacuous: `tupleDvd` equals the
`tupleDvd` of the tuples with the `m`-th coordinate erased. -/
theorem tupleDvd_eraseIdx : ∀ (ds hs : List Nat) (m n : Nat), ds.getD m 1 = 1 →
    m < ds.length → m < hs.length →
    tupleDvd hs n ds = tupleDvd (hs.eraseIdx m) n (ds.eraseIdx m)
  | [], _, _, _, _, h, _ => by simp at h
  | _ :: _, [], _, _, _, _, h => by simp at h
  | d :: ds, h :: hs, 0, n, h1, _, _ => by
    simp only [List.getD_cons_zero] at h1
    subst h1
    simp [tupleDvd, Nat.mod_one]
  | d :: ds, h :: hs, m + 1, n, h1, h2, h3 => by
    simp only [List.getD_cons_succ] at h1
    have ih := tupleDvd_eraseIdx ds hs m n h1 (by simpa using h2) (by simpa using h3)
    simp only [List.eraseIdx_cons_succ, tupleDvd, List.zip_cons_cons, List.all_cons] at ih ⊢
    rw [ih]

/-! ## Only `d_m = 1` survives -/

/-- If `d ∣ p` with `p` prime and `d < p`, then `d = 1`. -/
theorem prime_shift_coord_eq_one {d p : Nat} (hp : IsPrime p) (hd : d ∣ p) (hlt : d < p) :
    d = 1 := by
  rcases hp.2 d hd with h | h
  · exact h
  · omega

/-- The predicate counted in `S₂^{(m)}`, for one pair `(ds, es)`. -/
abbrev s2Pred (hs : List Nat) (W v0 N0 m : Nat) (pr : Nat → Bool) (ds es : List Nat) (n : Nat) :
    Bool :=
  decide (N0 ≤ n) && n % W == v0 && pr (n + hs.getD m 0) && tupleDvd hs n ds && tupleDvd hs n es

/-- A pair with `ds_m ≠ 1` (and `ds_m < N₀ + h_m`) contributes nothing: `n + h_m ≥ N₀ + h_m`
is prime and divisible by `ds_m`, so `ds_m = 1`. -/
theorem count_zero_of_coord_ne_one (hs ds es : List Nat) (W v0 N0 N m : Nat) (pr : Nat → Bool)
    (hpr : ∀ p, pr p = true → IsPrime p) (hm : m < hs.length) (hlen : ds.length = hs.length)
    (hsmall : ds.getD m 1 < N0 + hs.getD m 0) (hne : ds.getD m 1 ≠ 1) :
    (List.range N).countP (s2Pred hs W v0 N0 m pr ds es) = 0 := by
  rw [List.countP_eq_zero]
  intro n _ hn
  simp only [s2Pred, Bool.and_eq_true, decide_eq_true_eq] at hn
  obtain ⟨⟨⟨⟨h0, _⟩, hp⟩, hd⟩, _⟩ := hn
  have hdv := tupleDvd_coord ds hs m n hd (by omega) hm
  exact hne (prime_shift_coord_eq_one (hpr _ hp) hdv (by omega))

/-- The symmetric statement for `es_m ≠ 1`. -/
theorem count_zero_of_coord_ne_one' (hs ds es : List Nat) (W v0 N0 N m : Nat) (pr : Nat → Bool)
    (hpr : ∀ p, pr p = true → IsPrime p) (hm : m < hs.length) (hlen : es.length = hs.length)
    (hsmall : es.getD m 1 < N0 + hs.getD m 0) (hne : es.getD m 1 ≠ 1) :
    (List.range N).countP (s2Pred hs W v0 N0 m pr ds es) = 0 := by
  rw [List.countP_eq_zero]
  intro n _ hn
  simp only [s2Pred, Bool.and_eq_true, decide_eq_true_eq] at hn
  obtain ⟨⟨⟨⟨h0, _⟩, hp⟩, _⟩, he⟩ := hn
  have hdv := tupleDvd_coord es hs m n he (by omega) hm
  exact hne (prime_shift_coord_eq_one (hpr _ hp) hdv (by omega))

/-! ## The expansion and the support reduction -/

/-- **Exact expansion of `S₂^{(m)}`** (no hypotheses):
`∑_{N₀ ≤ n < N, n ≡ v₀ (W), pr(n+h_m)} (∑_{dᵢ ∣ n+hᵢ} λ_d)²
  = ∑_{d,e ∈ Dk} λ_d λ_e · #{n < N : N₀ ≤ n, n ≡ v₀ (W), pr(n+h_m), dᵢ,eᵢ ∣ n+hᵢ ∀ i}`. -/
theorem maynard_S2_expand_W (Dk : List (List Nat)) (hs : List Nat) (lam : List Nat → Int)
    (W v0 N0 N m : Nat) (pr : Nat → Bool) :
    ((List.range N).map fun n =>
        if N0 ≤ n ∧ n % W = v0 ∧ pr (n + hs.getD m 0) = true then
          mSieveSum Dk hs lam n * mSieveSum Dk hs lam n else 0).sum
      = (Dk.map fun ds => (Dk.map fun es =>
          lam ds * lam es *
            (((List.range N).countP (s2Pred hs W v0 N0 m pr ds es) : Nat) : Int)).sum).sum := by
  rw [← msq_expand_gen Dk (fun ds n => tupleDvd hs n ds) lam
    (fun n => decide (N0 ≤ n) && n % W == v0 && pr (n + hs.getD m 0)) N]
  apply isum_congr; intro n _
  simp only [Bool.and_eq_true, decide_eq_true_eq, beq_iff_eq, and_assoc]
  rfl

theorem isum_zero_of {β} {f : β → Int} {l : List β} (h : ∀ x ∈ l, f x = 0) :
    (l.map f).sum = 0 := by
  rw [isum_congr h]; exact isum_zero l

theorem isum_filter_of_zero {α} (p : α → Bool) (f : α → Int) : ∀ l : List α,
    (∀ x ∈ l, p x = false → f x = 0) → ((l.filter p).map f).sum = (l.map f).sum
  | [], _ => rfl
  | x :: l, h => by
    have ih := isum_filter_of_zero p f l (fun y hy => h y (List.mem_cons_of_mem _ hy))
    cases hx : p x
    · rw [List.filter_cons_of_neg (by simp [hx]), ih, List.map_cons, List.sum_cons,
        h x List.mem_cons_self hx, Int.zero_add]
    · rw [List.filter_cons_of_pos hx, List.map_cons, List.sum_cons, ih, List.map_cons,
        List.sum_cons]

/-- **Only `d_m = e_m = 1` survives.** If `pr` only accepts primes, `m < k`, all tuples in `Dk`
have length `k` and `m`-th entry `< N₀ + h_m` (Maynard: entries `≤ R < N`), then
`S₂^{(m)} = ∑_{d,e ∈ Dk, d_m = e_m = 1} λ_d λ_e · #{n < N : N₀ ≤ n, n ≡ v₀ (W), pr(n+h_m),
dᵢ,eᵢ ∣ n+hᵢ ∀ i}`. -/
theorem maynard_S2_support (Dk : List (List Nat)) (hs : List Nat) (lam : List Nat → Int)
    (W v0 N0 N m : Nat) (pr : Nat → Bool)
    (hpr : ∀ p, pr p = true → IsPrime p) (hm : m < hs.length)
    (hlen : ∀ ds ∈ Dk, ds.length = hs.length)
    (hsmall : ∀ ds ∈ Dk, ds.getD m 1 < N0 + hs.getD m 0) :
    ((List.range N).map fun n =>
        if N0 ≤ n ∧ n % W = v0 ∧ pr (n + hs.getD m 0) = true then
          mSieveSum Dk hs lam n * mSieveSum Dk hs lam n else 0).sum
      = ((Dk.filter fun ds => ds.getD m 1 == 1).map fun ds =>
          ((Dk.filter fun es => es.getD m 1 == 1).map fun es =>
            lam ds * lam es *
              (((List.range N).countP (s2Pred hs W v0 N0 m pr ds es) : Nat) : Int)).sum).sum := by
  rw [maynard_S2_expand_W]
  have inner : ∀ ds ∈ Dk,
      ((Dk.filter fun es => es.getD m 1 == 1).map fun es =>
          lam ds * lam es *
            (((List.range N).countP (s2Pred hs W v0 N0 m pr ds es) : Nat) : Int)).sum
        = (Dk.map fun es => lam ds * lam es *
            (((List.range N).countP (s2Pred hs W v0 N0 m pr ds es) : Nat) : Int)).sum := by
    intro ds _
    apply isum_filter_of_zero
    intro es hes hne
    have hne' : es.getD m 1 ≠ 1 := by simpa using hne
    rw [count_zero_of_coord_ne_one' hs ds es W v0 N0 N m pr hpr hm (hlen es hes)
      (hsmall es hes) hne']
    simp
  rw [← isum_congr inner]
  symm
  apply isum_filter_of_zero
  intro ds hds hne
  have hne' : ds.getD m 1 ≠ 1 := by simpa using hne
  apply isum_zero_of
  intro es _
  rw [count_zero_of_coord_ne_one hs ds es W v0 N0 N m pr hpr hm (hlen ds hds)
    (hsmall ds hds) hne']
  simp

/-- **`S₂^{(m)}` with the `m`-th condition removed.** Under the hypotheses of
`maynard_S2_support`,
`S₂^{(m)} = ∑_{d,e ∈ Dk, d_m = e_m = 1} λ_d λ_e ·
    #{n < N : N₀ ≤ n, n ≡ v₀ (W), pr(n+h_m), [dᵢ,eᵢ] ∣ n+hᵢ ∀ i ≠ m}`,
the `(k−1)`-tuples being `List.eraseIdx _ m` and the `lcm`s taken coordinatewise. -/
theorem maynard_S2_reduced (Dk : List (List Nat)) (hs : List Nat) (lam : List Nat → Int)
    (W v0 N0 N m : Nat) (pr : Nat → Bool)
    (hpr : ∀ p, pr p = true → IsPrime p) (hm : m < hs.length)
    (hlen : ∀ ds ∈ Dk, ds.length = hs.length)
    (hsmall : ∀ ds ∈ Dk, ds.getD m 1 < N0 + hs.getD m 0) :
    ((List.range N).map fun n =>
        if N0 ≤ n ∧ n % W = v0 ∧ pr (n + hs.getD m 0) = true then
          mSieveSum Dk hs lam n * mSieveSum Dk hs lam n else 0).sum
      = ((Dk.filter fun ds => ds.getD m 1 == 1).map fun ds =>
          ((Dk.filter fun es => es.getD m 1 == 1).map fun es =>
            lam ds * lam es * (((List.range N).countP fun n =>
              decide (N0 ≤ n) && n % W == v0 && pr (n + hs.getD m 0) &&
                tupleDvd (hs.eraseIdx m) n
                  (List.zipWith Nat.lcm (ds.eraseIdx m) (es.eraseIdx m)) : Nat) : Int)).sum).sum := by
  rw [maynard_S2_support Dk hs lam W v0 N0 N m pr hpr hm hlen hsmall]
  apply isum_congr; intro ds hds
  apply isum_congr; intro es hes
  obtain ⟨hdD, hd1⟩ := List.mem_filter.mp hds
  obtain ⟨heD, he1⟩ := List.mem_filter.mp hes
  have hd1' : ds.getD m 1 = 1 := by simpa using hd1
  have he1' : es.getD m 1 = 1 := by simpa using he1
  have hld := hlen ds hdD
  have hle := hlen es heD
  congr 3
  funext n
  simp only [s2Pred, Bool.and_assoc]
  rw [tupleDvd_eraseIdx ds hs m n hd1' (by omega) hm,
    tupleDvd_eraseIdx es hs m n he1' (by omega) hm,
    tupleDvd_lcm (hs.eraseIdx m) (ds.eraseIdx m) (es.eraseIdx m) n
      (by simp [List.length_eraseIdx, hld, hm]) (by simp [List.length_eraseIdx, hle, hm])]

/-! ## The inner count is a count of primes in one residue class -/

theorem mem_eraseIdx_mem {x : Nat} : ∀ {l : List Nat} {m : Nat}, x ∈ l.eraseIdx m → x ∈ l
  | [], _, h => by simp at h
  | _ :: _, 0, h => List.mem_cons_of_mem _ (by simpa using h)
  | _ :: l, m + 1, h => by
    rw [List.eraseIdx_cons_succ, List.mem_cons] at h
    rcases h with rfl | h
    · exact List.mem_cons_self
    · exact List.mem_cons_of_mem _ (mem_eraseIdx_mem h)

/-- **Prime counts in an AP.** For one surviving pair, with entries positive and coprime to `W`
and the moduli `Lᵢ = [dᵢ, eᵢ]` (`i ≠ m`) pairwise coprime, there is a residue `r < W ∏_{i≠m} Lᵢ`
with `#{N₀ ≤ n < N : n ≡ v₀ (W), pr(n+h_m), Lᵢ ∣ n+hᵢ ∀ i ≠ m}
  = #{N₀ ≤ n < N : n ≡ r (mod W ∏_{i≠m} Lᵢ), pr(n+h_m)}`. -/
theorem maynard_S2_count_residue (hs ds es : List Nat) (W v0 N0 N m : Nat) (pr : Nat → Bool)
    (hv : v0 < W) (hm : m < hs.length)
    (hld : ds.length = hs.length) (hle : es.length = hs.length)
    (hpos : ∀ d ∈ ds ++ es, 0 < d) (hDW : ∀ d ∈ ds ++ es, Nat.gcd d W = 1)
    (hpw : (List.zipWith Nat.lcm (ds.eraseIdx m) (es.eraseIdx m)).Pairwise Nat.Coprime) :
    ∃ r, r < W * (List.zipWith Nat.lcm (ds.eraseIdx m) (es.eraseIdx m)).prod ∧
      ((List.range N).countP fun n =>
          decide (N0 ≤ n) && n % W == v0 && pr (n + hs.getD m 0) &&
            tupleDvd (hs.eraseIdx m) n (List.zipWith Nat.lcm (ds.eraseIdx m) (es.eraseIdx m)))
        = (List.range N).countP fun n =>
          decide (N0 ≤ n) && n % (W * (List.zipWith Nat.lcm (ds.eraseIdx m)
            (es.eraseIdx m)).prod) == r && pr (n + hs.getD m 0) := by
  have hlenL : (List.zipWith Nat.lcm (ds.eraseIdx m) (es.eraseIdx m)).length
      = (hs.eraseIdx m).length := by
    simp [List.length_zipWith, List.length_eraseIdx, hld, hle, hm]
  have hposL : ∀ x ∈ List.zipWith Nat.lcm (ds.eraseIdx m) (es.eraseIdx m), 0 < x := by
    intro x hx
    obtain ⟨a, ha, b, hb, rfl⟩ := mem_zipWith_exists hx
    exact Nat.lcm_pos (hpos a (List.mem_append_left _ (mem_eraseIdx_mem ha)))
      (hpos b (List.mem_append_right _ (mem_eraseIdx_mem hb)))
  have hWL : ∀ x ∈ List.zipWith Nat.lcm (ds.eraseIdx m) (es.eraseIdx m), Nat.gcd x W = 1 := by
    intro x hx
    obtain ⟨a, ha, b, hb, rfl⟩ := mem_zipWith_exists hx
    have hab : Nat.Coprime (a * b) W := Nat.Coprime.mul_left
      (hDW a (List.mem_append_left _ (mem_eraseIdx_mem ha)))
      (hDW b (List.mem_append_right _ (mem_eraseIdx_mem hb)))
    exact Nat.Coprime.coprime_dvd_left
      (Nat.lcm_dvd (Nat.dvd_mul_right a b) (Nat.dvd_mul_left b a)) hab
  obtain ⟨r, hr, hiff⟩ := crt_tuple_residue hv _ _ hlenL hposL hWL hpw
  refine ⟨r, hr, ?_⟩
  congr 1
  funext n
  have key := hiff n
  apply Bool.eq_iff_iff.mpr
  simp only [Bool.and_eq_true, decide_eq_true_eq, beq_iff_eq] at key ⊢
  constructor
  · rintro ⟨⟨⟨a, b⟩, c⟩, d⟩; exact ⟨⟨a, key.mp ⟨b, d⟩⟩, c⟩
  · rintro ⟨⟨a, b⟩, c⟩; have := key.mpr b; exact ⟨⟨⟨a, this.1⟩, c⟩, this.2⟩

/-! ## Non-vacuity -/

/-- A Boolean primality test by trial division. -/
def primeB (p : Nat) : Bool := decide (2 ≤ p) && (List.range p).all fun d => d < 2 || p % d != 0

/-- `primeB` only accepts primes. -/
theorem primeB_sound : ∀ p, primeB p = true → IsPrime p := by
  intro p hp
  simp only [primeB, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true, List.mem_range,
    Bool.or_eq_true, bne_iff_ne, ne_eq] at hp
  refine ⟨hp.1, fun d hd => ?_⟩
  have hdle : d ≤ p := Nat.le_of_dvd (by omega) hd
  have hdpos : 0 < d := Nat.pos_of_dvd_of_pos hd (by omega)
  rcases Nat.lt_or_ge d p with hlt | hge
  · rcases hp.2 d hlt with h | h
    · omega
    · exact absurd (Nat.mod_eq_zero_of_dvd hd) h
  · right; omega

/-- Support `{(1,1), (3,1), (1,5)}` (`k = 2`, `h = (0, 2)`, `W = 2`, `v₀ = 1`, `m = 0`). -/
def exDk : List (List Nat) := [[1, 1], [3, 1], [1, 5]]

def exLam (d : List Nat) : Int := if d = [1, 1] then 2 else -1

/-- All hypotheses of `maynard_S2_reduced` hold here (`N₀ = 10`, every `N`); the pairs
involving `(3,1)` drop out. -/
theorem maynard_S2_example (N : Nat) :
    ((List.range N).map fun n =>
        if 10 ≤ n ∧ n % 2 = 1 ∧ primeB (n + [0, 2].getD 0 0) = true then
          mSieveSum exDk [0, 2] exLam n * mSieveSum exDk [0, 2] exLam n else 0).sum
      = ((exDk.filter fun ds => ds.getD 0 1 == 1).map fun ds =>
          ((exDk.filter fun es => es.getD 0 1 == 1).map fun es =>
            exLam ds * exLam es * (((List.range N).countP fun n =>
              decide (10 ≤ n) && n % 2 == 1 && primeB (n + [0, 2].getD 0 0) &&
                tupleDvd ([0, 2].eraseIdx 0) n
                  (List.zipWith Nat.lcm (ds.eraseIdx 0) (es.eraseIdx 0)) : Nat) : Int)).sum).sum :=
  maynard_S2_reduced exDk [0, 2] exLam 2 1 10 N 0 primeB primeB_sound (by decide)
    (by decide) (by decide)

/-- The filtered support is `{(1,1), (1,5)}`: the tuple `(3,1)` really is removed. -/
theorem ex_filter : exDk.filter (fun ds => ds.getD 0 1 == 1) = [[1, 1], [1, 5]] := by decide

/-- Numerical sanity check at `N = 40` of `maynard_S2_support` (both sides evaluated). -/
theorem maynard_S2_example_eval :
    ((List.range 40).map fun n =>
        if 10 ≤ n ∧ n % 2 = 1 ∧ primeB (n + [0, 2].getD 0 0) = true then
          mSieveSum exDk [0, 2] exLam n * mSieveSum exDk [0, 2] exLam n else 0).sum
      = ((exDk.filter fun ds => ds.getD 0 1 == 1).map fun ds =>
          ((exDk.filter fun es => es.getD 0 1 == 1).map fun es =>
            exLam ds * exLam es * (((List.range 40).countP
              (s2Pred [0, 2] 2 1 10 0 primeB ds es) : Nat) : Int)).sum).sum := by
  decide +kernel

end MaynardS2
end TwinPrimes
