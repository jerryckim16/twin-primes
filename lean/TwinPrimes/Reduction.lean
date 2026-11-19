import TwinPrimes.Basic
import TwinPrimes.Tuples

/-!
# The elementary skeleton of "ratio > 4 ⇒ bounded gaps" (programme 4, first step)

Maynard–Tao sieves prove `DHL[k,2]` by exhibiting, for every admissible `k`-tuple `H` and
every `N`, non-negative weights `w(n)` on a finite range of `n ≥ N` with

  `∑ w(n) < ∑ w(n) · #{h ∈ H : n + h prime}`.                                   (*)

This file checks, in core Lean, the two elementary steps around (*):

* `exists_of_wsum_lt` / `dhl_of_sieveInequality`: (*) for all `H`, `N` gives `DHL k`
  (pigeonhole: some `n` with `w(n) > 0` has at least two primes among `n + H`);
* `sieveInequality_of_ratio`: a ratio bound `S₂ / S₁ ≥ p / q > 1` gives (*);
* `theta_of_ratio_gt_four`: if the variational ratio is `p / q > 4`, there is a level
  `θ = a / b < 1/2` with `θ · (p / q) / 2 > 1`, the numerical form of Maynard's criterion
  `θ M_k / 2 > 1` at levels below the Bombieri–Vinogradov exponent `1/2`.

* `eventually_lt_of_asymptotics` / `sieveInequality_of_asymptotics` (Session 34): the
  limit step in abstract form -- two-sided asymptotics `S₁ ≤ (1+1/m)(a/a')B`,
  `S₂ ≥ (m/(m+1))(c/c')B` for every `m`, with `a/a' < c/c'`, give (*) eventually
  (explicit choice `m = 2ac' + 2`; all in `Nat`, no reals).

NOT formalised (and never assumed as an axiom): the analytic asymptotics
`S₁ ~ I_k(F) · B N`, `S₂ ~ (θ/2) J_k(F) · B N` that connect (*) to the variational ratio,
and the distribution estimates they rest on.  Those appear only as the hypothesis
`SieveInequality k`.
-/

namespace TwinPrimes

/-- Weighted sum `∑_{n ∈ ns} w n * f n` over a finite list. -/
def wsum (w f : Nat → Nat) : List Nat → Nat
  | [] => 0
  | n :: ns => w n * f n + wsum w f ns

/-- Pigeonhole: if `m · ∑ w < ∑ w f`, some `n` in the list has `w n > 0` and `f n > m`. -/
theorem exists_of_wsum_lt (w f : Nat → Nat) (m : Nat) :
    ∀ ns : List Nat, m * wsum w (fun _ => 1) ns < wsum w f ns →
      ∃ n, n ∈ ns ∧ m < f n ∧ 0 < w n
  | [], h => by simp [wsum] at h
  | n :: ns, h => by
    simp only [wsum, Nat.mul_one, Nat.mul_add] at h
    by_cases hn : m < f n ∧ 0 < w n
    · exact ⟨n, List.mem_cons_self, hn.1, hn.2⟩
    · have hle : w n * f n ≤ m * w n := by
        by_cases hw : w n = 0
        · simp [hw]
        · have hf : f n ≤ m := by omega
          rw [Nat.mul_comm m]
          exact Nat.mul_le_mul_left _ hf
      obtain ⟨n', hn', h1, h2⟩ := exists_of_wsum_lt w f m ns (by omega)
      exact ⟨n', List.mem_cons_of_mem _ hn', h1, h2⟩

/-- Number of `h ∈ H` with `n + h` prime (classical decidability of `IsPrime`). -/
noncomputable def primeCount (H : List Nat) (n : Nat) : Nat :=
  H.countP (fun h => @decide (IsPrime (n + h)) (Classical.propDecidable _))

/-- A strictly increasing list on which a predicate holds at least twice contains `a < b`
with the predicate true at both. -/
theorem two_of_countP (p : Nat → Bool) :
    ∀ H : List Nat, H.Pairwise (· < ·) → 2 ≤ H.countP p →
      ∃ a b, a ∈ H ∧ b ∈ H ∧ a < b ∧ p a = true ∧ p b = true
  | [], _, h => by simp at h
  | x :: xs, hs, h => by
    rw [List.pairwise_cons] at hs
    rw [List.countP_cons] at h
    by_cases hx : p x = true
    · simp only [hx, ite_true] at h
      have hpos : 0 < xs.countP p := by omega
      obtain ⟨b, hb, hpb⟩ := List.countP_pos_iff.mp hpos
      exact ⟨x, b, List.mem_cons_self, List.mem_cons_of_mem _ hb, hs.1 b hb, hx,
        by simpa using hpb⟩
    · have hx' : p x = false := by simpa using hx
      simp only [hx', Bool.false_eq_true, ite_false, Nat.add_zero] at h
      obtain ⟨a, b, ha, hb, hab, hpa, hpb⟩ := two_of_countP p xs hs.2 h
      exact ⟨a, b, List.mem_cons_of_mem _ ha, List.mem_cons_of_mem _ hb, hab, hpa, hpb⟩

/-- The sieve inequality (*) for every admissible increasing `k`-tuple, beyond every `N`. -/
def SieveInequality (k : Nat) : Prop :=
  ∀ H : List Nat, H.length = k → H.Pairwise (· < ·) → Admissible H →
    ∀ N : Nat, ∃ (ns : List Nat) (w : Nat → Nat), (∀ n ∈ ns, N ≤ n) ∧
      wsum w (fun _ => 1) ns < wsum w (primeCount H) ns

/-- (*) for all tuples gives `DHL[k,2]`. -/
theorem dhl_of_sieveInequality {k : Nat} (h : SieveInequality k) : DHL k := by
  intro H hlen hsort hadm N
  obtain ⟨ns, w, hN, hlt⟩ := h H hlen hsort hadm N
  obtain ⟨n, hn, h2, _⟩ := exists_of_wsum_lt w (primeCount H) 1 ns (by simpa using hlt)
  obtain ⟨a, b, ha, hb, hab, hpa, hpb⟩ :=
    two_of_countP (fun h => @decide (IsPrime (n + h)) (Classical.propDecidable _)) H hsort h2
  exact ⟨n, hN n hn, a, b, ha, hb, hab, @of_decide_eq_true _ (Classical.propDecidable _) hpa,
    @of_decide_eq_true _ (Classical.propDecidable _) hpb⟩

/-- A ratio bound `q · S₂ ≥ p · S₁` with `q < p` and `S₁ > 0` gives (*). -/
theorem sieveInequality_of_ratio {k : Nat} (p q : Nat) (hpq : q < p)
    (h : ∀ H : List Nat, H.length = k → H.Pairwise (· < ·) → Admissible H →
      ∀ N : Nat, ∃ (ns : List Nat) (w : Nat → Nat), (∀ n ∈ ns, N ≤ n) ∧
        0 < wsum w (fun _ => 1) ns ∧
        p * wsum w (fun _ => 1) ns ≤ q * wsum w (primeCount H) ns) :
    SieveInequality k := by
  intro H hlen hsort hadm N
  obtain ⟨ns, w, hN, hpos, hle⟩ := h H hlen hsort hadm N
  refine ⟨ns, w, hN, ?_⟩
  generalize wsum w (fun _ => 1) ns = S₁ at hpos hle ⊢
  generalize wsum w (primeCount H) ns = S₂ at hle ⊢
  -- q * S₁ < p * S₁ ≤ q * S₂, hence S₁ < S₂.
  have h1 : q * S₁ < p * S₁ := Nat.mul_lt_mul_of_pos_right hpq hpos
  have h2 : q * S₁ < q * S₂ := Nat.lt_of_lt_of_le h1 hle
  exact Nat.lt_of_mul_lt_mul_left h2

/-- Ratio `p / q > 4` ⇒ a level `θ = a / b < 1/2` with `θ · (p / q) / 2 > 1`
(take `a = p + 4q`, `b = 4p`). -/
theorem theta_of_ratio_gt_four (p q : Nat) (h : 4 * q < p) :
    ∃ a b : Nat, 0 < b ∧ 2 * a < b ∧ 2 * b * q < a * p := by
  refine ⟨p + 4 * q, 4 * p, by omega, by omega, ?_⟩
  have : 4 * q * p < p * p := Nat.mul_lt_mul_of_pos_right h (by omega)
  have e1 : 2 * (4 * p) * q = 2 * (4 * q * p) := by
    rw [Nat.mul_assoc, Nat.mul_assoc, Nat.mul_comm p q, ← Nat.mul_assoc 4 q p]
  have e2 : (p + 4 * q) * p = p * p + 4 * q * p := by rw [Nat.add_mul]
  rw [e1, e2]; omega

/-- If `m·a'·S₁ ≤ (m+1)·a·B` and `m·c·B ≤ (m+1)·c'·S₂` with `(m+1)²·a·c' < m²·c·a'` and `B > 0`,
then `S₁ < S₂`. -/
theorem lt_of_two_sided (a a' c c' m S1 S2 B : Nat)
    (h1 : m * a' * S1 ≤ (m + 1) * a * B) (h2 : m * c * B ≤ (m + 1) * c' * S2)
    (hm : (m + 1) * (m + 1) * (a * c') < m * m * (c * a')) (hB : 0 < B) : S1 < S2 := by
  have k1 : (m * (m + 1) * a' * c') * S1 ≤ ((m + 1) * (m + 1) * (a * c')) * B := by
    have := Nat.mul_le_mul_left ((m + 1) * c') h1
    calc (m * (m + 1) * a' * c') * S1 = (m + 1) * c' * (m * a' * S1) := by grind
      _ ≤ (m + 1) * c' * ((m + 1) * a * B) := this
      _ = ((m + 1) * (m + 1) * (a * c')) * B := by grind
  have k2 : (m * m * (c * a')) * B ≤ (m * (m + 1) * a' * c') * S2 := by
    have := Nat.mul_le_mul_left (m * a') h2
    calc (m * m * (c * a')) * B = m * a' * (m * c * B) := by grind
      _ ≤ m * a' * ((m + 1) * c' * S2) := this
      _ = (m * (m + 1) * a' * c') * S2 := by grind
  have k3 : ((m + 1) * (m + 1) * (a * c')) * B < (m * m * (c * a')) * B :=
    Nat.mul_lt_mul_of_pos_right hm hB
  exact Nat.lt_of_mul_lt_mul_left (Nat.lt_of_le_of_lt k1 (Nat.lt_of_lt_of_le k3 k2))

/-- For `a·c' < c·a'` the choice `m = 2·a·c' + 2` satisfies the hypothesis `hm` above. -/
theorem good_m (a a' c c' : Nat) (h : a * c' < c * a') :
    (2 * (a * c') + 2 + 1) * (2 * (a * c') + 2 + 1) * (a * c') <
      (2 * (a * c') + 2) * (2 * (a * c') + 2) * (c * a') := by
  generalize a * c' = X at h ⊢
  generalize c * a' = Y at h ⊢
  have e : (2 * X + 2 + 1) * (2 * X + 2 + 1) * X < (2 * X + 2) * (2 * X + 2) * (X + 1) := by grind
  exact Nat.lt_of_lt_of_le e (Nat.mul_le_mul_left _ h)

/-- Abstract "asymptotics ⇒ eventual strict inequality": if, for every `m > 0`, eventually
`S₁(N) ≤ (1 + 1/m)·(a/a')·B(N)` and `S₂(N) ≥ (m/(m+1))·(c/c')·B(N)`, with `a/a' < c/c'` and
`B(N) > 0`, then eventually `S₁(N) < S₂(N)`. -/
theorem eventually_lt_of_asymptotics (a a' c c' : Nat) (h : a * c' < c * a')
    (S1 S2 B : Nat → Nat) (hB : ∀ N, 0 < B N)
    (hasy : ∀ m, 0 < m → ∃ N0, ∀ N, N0 ≤ N →
      m * a' * S1 N ≤ (m + 1) * a * B N ∧ m * c * B N ≤ (m + 1) * c' * S2 N) :
    ∃ N0, ∀ N, N0 ≤ N → S1 N < S2 N := by
  obtain ⟨N0, hN0⟩ := hasy (2 * (a * c') + 2) (by omega)
  exact ⟨N0, fun N hN => lt_of_two_sided a a' c c' _ (S1 N) (S2 N) (B N)
    (hN0 N hN).1 (hN0 N hN).2 (good_m a a' c c' h) (hB N)⟩

/-- The analytic asymptotics in abstract form give the sieve inequality (*): if for every
admissible increasing `k`-tuple there are weights `w_N` on lists `ns_N ⊆ [N, ∞)` whose sums
satisfy `S₁ ~ (a/a')·B`, `S₂ ~ (c/c')·B` in the two-sided form of
`eventually_lt_of_asymptotics` (only the upper bound for `S₁` and the lower bound for `S₂`
are used), with `a/a' < c/c'` (in Maynard's notation `a/a' ≥ I_k(F)` and
`c/c' ≤ (θ/2)·J_k(F)`), then `SieveInequality k`, hence `DHL k`.  The asymptotics
themselves are NOT proved here. -/
theorem sieveInequality_of_asymptotics {k : Nat} (a a' c c' : Nat) (h : a * c' < c * a')
    (hfam : ∀ H : List Nat, H.length = k → H.Pairwise (· < ·) → Admissible H →
      ∃ (ns : Nat → List Nat) (w : Nat → Nat → Nat) (B : Nat → Nat),
        (∀ N, ∀ n ∈ ns N, N ≤ n) ∧ (∀ N, 0 < B N) ∧
        ∀ m, 0 < m → ∃ N0, ∀ N, N0 ≤ N →
          m * a' * wsum (w N) (fun _ => 1) (ns N) ≤ (m + 1) * a * B N ∧
          m * c * B N ≤ (m + 1) * c' * wsum (w N) (primeCount H) (ns N)) :
    SieveInequality k := by
  intro H hlen hsort hadm N
  obtain ⟨ns, w, B, hge, hB, hasy⟩ := hfam H hlen hsort hadm
  obtain ⟨N0, hN0⟩ := eventually_lt_of_asymptotics a a' c c' h
    (fun N => wsum (w N) (fun _ => 1) (ns N)) (fun N => wsum (w N) (primeCount H) (ns N)) B hB hasy
  refine ⟨ns (max N N0), w (max N N0), fun n hn => ?_, hN0 _ (Nat.le_max_right _ _)⟩
  exact Nat.le_trans (Nat.le_max_left N N0) (hge _ n hn)

/-- End to end, combinatorial part only: (*) for `k = 50` gives gaps `≤ 246`. -/
theorem boundedGaps_246_of_sieveInequality_50 (h : SieveInequality 50) : BoundedGaps 246 :=
  boundedGaps_246_of_DHL_50 (dhl_of_sieveInequality h)

/-- End to end, combinatorial part only, from the abstract asymptotics at `k = 50`. -/
theorem boundedGaps_246_of_asymptotics_50 (a a' c c' : Nat) (h : a * c' < c * a')
    (hfam : ∀ H : List Nat, H.length = 50 → H.Pairwise (· < ·) → Admissible H →
      ∃ (ns : Nat → List Nat) (w : Nat → Nat → Nat) (B : Nat → Nat),
        (∀ N, ∀ n ∈ ns N, N ≤ n) ∧ (∀ N, 0 < B N) ∧
        ∀ m, 0 < m → ∃ N0, ∀ N, N0 ≤ N →
          m * a' * wsum (w N) (fun _ => 1) (ns N) ≤ (m + 1) * a * B N ∧
          m * c * B N ≤ (m + 1) * c' * wsum (w N) (primeCount H) (ns N)) :
    BoundedGaps 246 :=
  boundedGaps_246_of_sieveInequality_50 (sieveInequality_of_asymptotics a a' c c' h hfam)

end TwinPrimes
