/-!
# Twin primes and bounded gaps: definitions and the combinatorial half

Core Lean 4 only (no Mathlib), so this file compiles with a bare toolchain.

Nothing here proves the twin prime conjecture.  What is machine-checked:

* `twin_iff`            : the twin prime conjecture is `BoundedGaps 2`;
* `admissible_of_check` : a finite computation certifies admissibility;
* `NarrowTuple.boundedGaps` : `DHL k` plus an admissible `k`-tuple inside
  `[0, D]` gives infinitely many prime pairs at distance at most `D`.

The analytic statement `DHL k` is a *hypothesis* throughout, never an axiom.
-/

namespace TwinPrimes

/-- Primality, stated from scratch. -/
def IsPrime (n : Nat) : Prop := 2 ≤ n ∧ ∀ d : Nat, d ∣ n → d = 1 ∨ d = n

/-- The twin prime conjecture: twin primes beyond every bound. -/
def TwinPrimeConjecture : Prop :=
  ∀ N : Nat, ∃ p, N ≤ p ∧ IsPrime p ∧ IsPrime (p + 2)

/-- Infinitely many pairs of distinct primes at distance at most `B`.
For `B ≥ 2` this is equivalent to `liminf (p_{n+1} - p_n) ≤ B`. -/
def BoundedGaps (B : Nat) : Prop :=
  ∀ N : Nat, ∃ p q, N ≤ p ∧ p < q ∧ q ≤ p + B ∧ IsPrime p ∧ IsPrime q

theorem BoundedGaps.mono {B B' : Nat} (h : B ≤ B') (hB : BoundedGaps B) :
    BoundedGaps B' := by
  intro N
  obtain ⟨p, q, hN, hpq, hq, hp, hq'⟩ := hB N
  exact ⟨p, q, hN, hpq, by omega, hp, hq'⟩

theorem IsPrime.odd_of_three_le {p : Nat} (hp : IsPrime p) (h3 : 3 ≤ p) :
    p % 2 = 1 := by
  rcases Nat.mod_two_eq_zero_or_one p with h | h
  · have hd : 2 ∣ p := Nat.dvd_of_mod_eq_zero h
    rcases hp.2 2 hd with h' | h' <;> omega
  · exact h

/-- The twin prime conjecture is exactly the case `B = 2` of bounded gaps. -/
theorem twin_iff : TwinPrimeConjecture ↔ BoundedGaps 2 := by
  constructor
  · intro h N
    obtain ⟨p, hN, hp, hp2⟩ := h N
    exact ⟨p, p + 2, hN, by omega, by omega, hp, hp2⟩
  · intro h N
    obtain ⟨p, q, hN, hpq, hq, hp, hq'⟩ := h (N + 3)
    have hpo := hp.odd_of_three_le (by omega)
    have hqo := hq'.odd_of_three_le (by omega)
    have hqp : q = p + 2 := by omega
    subst hqp
    exact ⟨p, by omega, hp, hq'⟩

/-! ## Admissible tuples -/

/-- `H` is admissible: it misses a residue class modulo every prime. -/
def Admissible (H : List Nat) : Prop :=
  ∀ p : Nat, IsPrime p → ∃ r, r < p ∧ ∀ h ∈ H, h % p ≠ r

/-- Does `H` miss some residue class modulo `m`? -/
def missesClass (H : List Nat) (m : Nat) : Bool :=
  (List.range m).any fun r => H.all fun h => h % m != r

/-- Finite certificate: `H` misses a class modulo every `m` with
`2 ≤ m ≤ H.length`.  Larger moduli are handled by pigeonhole. -/
def admissibleCheck (H : List Nat) : Bool :=
  (List.range (H.length + 1)).all fun m => decide (m < 2) || missesClass H m

/-- Pigeonhole: a list shorter than `n` misses some number below `n`. -/
theorem exists_not_mem_of_length_lt :
    ∀ (n : Nat) (L : List Nat), L.length < n → ∃ r, r < n ∧ r ∉ L := by
  intro n
  induction n with
  | zero => intro L h; omega
  | succ n ih =>
    intro L hL
    by_cases hn : n ∈ L
    · have hlt : (L.filter (fun x => x != n)).length < L.length := by
        apply List.length_filter_lt_length_iff_exists.mpr
        exact ⟨n, hn, by simp⟩
      obtain ⟨r, hr, hrL⟩ := ih (L.filter (fun x => x != n)) (by omega)
      refine ⟨r, by omega, ?_⟩
      intro hmem
      apply hrL
      rw [List.mem_filter]
      refine ⟨hmem, ?_⟩
      have : r ≠ n := by omega
      simpa using this
    · exact ⟨n, by omega, hn⟩

/-- Soundness of the finite certificate. -/
theorem admissible_of_check {H : List Nat} (hc : admissibleCheck H = true) :
    Admissible H := by
  intro p hp
  by_cases hle : p ≤ H.length
  · have h1 := List.all_eq_true.mp hc p (List.mem_range.mpr (by omega))
    have hp2 : ¬ p < 2 := by have := hp.1; omega
    have h2 : missesClass H p = true := by simpa [hp2] using h1
    obtain ⟨r, hr, hall⟩ := List.any_eq_true.mp h2
    refine ⟨r, List.mem_range.mp hr, ?_⟩
    intro h hh
    have h3 := List.all_eq_true.mp hall h hh
    simpa using h3
  · obtain ⟨r, hr, hrL⟩ :=
      exists_not_mem_of_length_lt p (H.map (· % p)) (by simp; omega)
    refine ⟨r, hr, ?_⟩
    intro h hh heq
    exact hrL (List.mem_map.mpr ⟨h, hh, heq⟩)

/-! ## The Dickson-Hardy-Littlewood statement `DHL[k,2]` -/

/-- `DHL[k,2]`: every admissible `k`-tuple has infinitely many translates
containing at least two primes.  Open for small `k`; `DHL 2` gives twin primes. -/
def DHL (k : Nat) : Prop :=
  ∀ H : List Nat, H.length = k → H.Pairwise (· < ·) → Admissible H →
    ∀ N : Nat, ∃ n, N ≤ n ∧
      ∃ a b, a ∈ H ∧ b ∈ H ∧ a < b ∧ IsPrime (n + a) ∧ IsPrime (n + b)

/-- An admissible `k`-tuple contained in `[0, D]`, with its certificate. -/
structure NarrowTuple (k D : Nat) where
  H : List Nat
  len : H.length = k
  sorted : H.Pairwise (· < ·)
  bound : ∀ h ∈ H, h ≤ D
  check : admissibleCheck H = true

/-- Sub-tuples of admissible tuples are admissible. -/
theorem Admissible.sublist {H H' : List Nat} (hs : H.Sublist H') (h : Admissible H') :
    Admissible H := by
  intro p hp
  obtain ⟨r, hr, hall⟩ := h p hp
  exact ⟨r, hr, fun x hx => hall x (hs.subset hx)⟩

/-- `DHL[k,2]` implies `DHL[k',2]` for `k ≤ k'`: delete shifts from the tuple. -/
theorem DHL.mono {k k' : Nat} (hk : k ≤ k') (h : DHL k) : DHL k' := by
  intro H hlen hsort hadm N
  have hsub : (H.take k).Sublist H := List.take_sublist k H
  have hlen' : (H.take k).length = k := by
    rw [List.length_take]; omega
  obtain ⟨n, hn, a, b, ha, hb, hab, hpa, hpb⟩ :=
    h (H.take k) hlen' (hsort.sublist hsub) (Admissible.sublist hsub hadm) N
  exact ⟨n, hn, a, b, hsub.subset ha, hsub.subset hb, hab, hpa, hpb⟩

/-- The combinatorial half of every bounded-gaps theorem. -/
theorem NarrowTuple.boundedGaps {k D : Nat} (T : NarrowTuple k D)
    (hDHL : DHL k) : BoundedGaps D := by
  intro N
  obtain ⟨n, hn, a, b, _, hb, hab, hpa, hpb⟩ :=
    hDHL T.H T.len T.sorted (admissible_of_check T.check) N
  have hbD := T.bound b hb
  exact ⟨n + a, n + b, by omega, by omega, by omega, hpa, hpb⟩

/-! ## Why the target is 2 (session 4) -/

/-- `2` is prime. -/
theorem isPrime_two : IsPrime 2 := by
  refine ⟨by decide, fun d hd => ?_⟩
  have hle : d ≤ 2 := Nat.le_of_dvd (by decide) hd
  have hpos : 0 < d := Nat.pos_of_dvd_of_pos hd (by decide)
  omega

/-- Gaps of size `1` occur only once (`2, 3`): `BoundedGaps 1` is false, so `2` is the
smallest bound that can hold, and the twin prime conjecture is the strongest statement
of this form. -/
theorem not_boundedGaps_one : ¬ BoundedGaps 1 := by
  intro h
  obtain ⟨p, q, hN, hpq, hq, hp, hq'⟩ := h 3
  have h1 := hp.odd_of_three_le (by omega)
  have h2 := hq'.odd_of_three_le (by omega)
  omega

/-- A pair `{0, d}` is admissible exactly when `d` is even. -/
theorem admissible_pair_iff (d : Nat) : Admissible [0, d] ↔ d % 2 = 0 := by
  constructor
  · intro h
    obtain ⟨r, hr, hall⟩ := h 2 isPrime_two
    have h0 := hall 0 (by simp)
    have hd := hall d (by simp)
    simp at h0
    omega
  · intro hd p hp
    by_cases h2 : p = 2
    · subst h2
      exact ⟨1, by decide, by intro x hx; simp at hx; rcases hx with rfl | rfl <;> omega⟩
    · have hp3 : 3 ≤ p := by have := hp.1; omega
      by_cases h1 : d % p = 1
      · exact ⟨2, by omega, by
          intro x hx; simp at hx; rcases hx with rfl | rfl
          · simp
          · omega⟩
      · exact ⟨1, by omega, by
          intro x hx; simp at hx; rcases hx with rfl | rfl
          · simp
          · exact h1⟩

end TwinPrimes
