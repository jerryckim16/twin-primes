# Lean: the finite S2 expansion (Maynard, Lemma 5.2, algebraic part)

File: `lean/TwinPrimes/MaynardS2.lean` (339 lines, namespace `TwinPrimes.MaynardS2`). It is added to
`lean/TwinPrimes.lean`, and its 16 declarations are added to `lean/Audit.lean`. Core Lean 4.35.0, no Mathlib.
No `sorry`, no `native_decide`, no new axioms. One evaluation check uses `decide +kernel`, which is kernel
reduction and adds no axiom.

## Conventions

These follow `MaynardS1.lean`:
- `tupleDvd hs n ds` means `∀ i, ds_i ∣ n + h_i`, with the index running over `ds.zip hs`.
- `mSieveSum Dk hs lam n = ∑_{ds ∈ Dk, tupleDvd} lam ds`.
- The support `Dk` is a `List (List Nat)` and the weights are `lam : List Nat → Int`.
- The m-th coordinate is `ds.getD m 1` for a tuple and `hs.getD m 0` for the shifts.

Primality is an abstract Boolean `pr : Nat → Bool`. Its only hypothesis is soundness,
`∀ p, pr p = true → IsPrime p` (`IsPrime` from `Basic.lean`). The n-range is `N0 ≤ n < N`; Maynard's is
`N ≤ n < 2N`. The predicate that gets counted is

```lean
abbrev s2Pred (hs : List Nat) (W v0 N0 m : Nat) (pr : Nat → Bool) (ds es : List Nat) (n : Nat) : Bool :=
  decide (N0 ≤ n) && n % W == v0 && pr (n + hs.getD m 0) && tupleDvd hs n ds && tupleDvd hs n es
```

## Main statements (copied)

```lean
theorem maynard_S2_expand_W (Dk : List (List Nat)) (hs : List Nat) (lam : List Nat → Int)
    (W v0 N0 N m : Nat) (pr : Nat → Bool) :
    ((List.range N).map fun n =>
        if N0 ≤ n ∧ n % W = v0 ∧ pr (n + hs.getD m 0) = true then
          mSieveSum Dk hs lam n * mSieveSum Dk hs lam n else 0).sum
      = (Dk.map fun ds => (Dk.map fun es =>
          lam ds * lam es *
            (((List.range N).countP (s2Pred hs W v0 N0 m pr ds es) : Nat) : Int)).sum).sum

theorem count_zero_of_coord_ne_one (hs ds es : List Nat) (W v0 N0 N m : Nat) (pr : Nat → Bool)
    (hpr : ∀ p, pr p = true → IsPrime p) (hm : m < hs.length) (hlen : ds.length = hs.length)
    (hsmall : ds.getD m 1 < N0 + hs.getD m 0) (hne : ds.getD m 1 ≠ 1) :
    (List.range N).countP (s2Pred hs W v0 N0 m pr ds es) = 0
-- (and the symmetric count_zero_of_coord_ne_one' for es)

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
              (((List.range N).countP (s2Pred hs W v0 N0 m pr ds es) : Nat) : Int)).sum).sum

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
                  (List.zipWith Nat.lcm (ds.eraseIdx m) (es.eraseIdx m)) : Nat) : Int)).sum).sum

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
            (es.eraseIdx m)).prod) == r && pr (n + hs.getD m 0)
```

Helper lemmas:
- `tupleDvd_coord`: the m-th coordinate divides `n + h_m`.
- `tupleDvd_eraseIdx`: if `d_m = 1`, the m-th condition can be dropped.
- `prime_shift_coord_eq_one`: if `d ∣ p`, `p` is prime and `d < p`, then `d = 1`.
- `isum_zero_of`, `isum_filter_of_zero`, `mem_eraseIdx_mem`.

Non-vacuity checks:
- `primeB` is trial division, and `primeB_sound : ∀ p, primeB p = true → IsPrime p` is proved for all `p`.
- `maynard_S2_example` instantiates `maynard_S2_reduced` with every hypothesis discharged. The instance is
  `Dk = {(1,1),(3,1),(1,5)}`, `h = (0,2)`, `W = 2`, `v0 = 1`, `m = 0`, `N0 = 10` and every `N`.
- `ex_filter` shows that `(3,1)` really is removed.
- `maynard_S2_example_eval` evaluates both sides of the support identity at `N = 40` (`decide +kernel`).

## Correspondence with Maynard's Lemma 5.2 (arXiv:1311.4600)

Maynard's sum is S2^(m) = ∑_{N≤n<2N, n≡v0 (W)} 1_P(n+h_m) (∑_{d_i|n+h_i} λ_d)^2.

**Covered (exact, finite):**
1. Expanding the square and swapping the sums (`maynard_S2_expand_W`). This needs no hypotheses.
2. Only pairs with d_m = e_m = 1 survive (`maynard_S2_support`). Maynard's reason is that λ is supported on
   ∏ d_i < R and R < N, so d_m < n + h_m. Here that reason is the explicit hypothesis `hsmall`
   (d_m < N0 + h_m for every d ∈ Dk). The hypothesis must hold for every tuple in `Dk`; the conclusion's
   filter does the restricting.
3. For the surviving pairs the m-th condition is empty. The rest combine to [d_i, e_i] | n + h_i for i ≠ m
   (`maynard_S2_reduced`). The result is an exact identity with no coprimality hypotheses.
4. CRT (`maynard_S2_count_residue`): for a pair whose [d_i, e_i] (i ≠ m) are pairwise coprime and coprime
   to W, the inner count is a count of n in [N0, N) in a single class mod q = W ∏_{i≠m}[d_i, e_i] with
   pr(n + h_m). That count is the prime-in-AP count X to which Bombieri–Vinogradov is applied.
   - The pairwise-coprimality hypothesis `hpw` is assumed per pair here.
   - For S1, the bad pairs are handled in `MaynardHpw.lean` (`count_zero_of_not_pairwise`). That
     argument has not been re-run for S2 in this file. It would transfer verbatim, because the S2 count
     is bounded by the S1 count.

**Not covered (stays outside):**
- The asymptotics: #{primes in the class} = X_N/φ(q) + error. This is also where the discarded classes
  come in: they have gcd(r + h_m, q) > 1 and contain at most one prime.
- The Bombieri–Vinogradov input and the bound O(y_max^2 N/(log N)^A) on the summed errors.
- The main-term quadratic form ∑ λ_d λ_e / φ(∏[d_i, e_i]). Its change of variables to y^(m)_r
  (Maynard (5.8) and Lemma 5.3) is the analogue of `MaynardDiag.lean`, with φ in place of the identity
  and the m-th coordinate fixed at 1. It is NOT done here.
- The passage to the integral J_k^(m)(F).

## Build / audit output

| | before (unchanged tree) | after |
|---|---|---|
| `lake build` | `Build completed successfully (24 jobs).` | `Build completed successfully (25 jobs).` |
| `lake env lean Audit.lean` lines | 209 | 225 (+16) |
| `[propext, Classical.choice, Quot.sound]` | 116 | 123 |
| `[propext, Quot.sound]` | 54 | 59 |
| `[propext]` | 11 | 15 |
| no axioms | 28 | 28 |

No `sorryAx` and no other axiom appears.

The new file's entries:

```
'TwinPrimes.MaynardS2.tupleDvd_coord' depends on axioms: [propext, Quot.sound]
'TwinPrimes.MaynardS2.tupleDvd_eraseIdx' depends on axioms: [propext, Classical.choice, Quot.sound]
'TwinPrimes.MaynardS2.prime_shift_coord_eq_one' depends on axioms: [propext, Quot.sound]
'TwinPrimes.MaynardS2.count_zero_of_coord_ne_one' depends on axioms: [propext, Classical.choice, Quot.sound]
'TwinPrimes.MaynardS2.count_zero_of_coord_ne_one'' depends on axioms: [propext, Classical.choice, Quot.sound]
'TwinPrimes.MaynardS2.maynard_S2_expand_W' depends on axioms: [propext, Quot.sound]
'TwinPrimes.MaynardS2.isum_zero_of' depends on axioms: [propext, Quot.sound]
'TwinPrimes.MaynardS2.isum_filter_of_zero' depends on axioms: [propext]
'TwinPrimes.MaynardS2.maynard_S2_support' depends on axioms: [propext, Classical.choice, Quot.sound]
'TwinPrimes.MaynardS2.maynard_S2_reduced' depends on axioms: [propext, Classical.choice, Quot.sound]
'TwinPrimes.MaynardS2.mem_eraseIdx_mem' depends on axioms: [propext]
'TwinPrimes.MaynardS2.maynard_S2_count_residue' depends on axioms: [propext, Classical.choice, Quot.sound]
'TwinPrimes.MaynardS2.primeB_sound' depends on axioms: [propext, Quot.sound]
'TwinPrimes.MaynardS2.maynard_S2_example' depends on axioms: [propext, Classical.choice, Quot.sound]
'TwinPrimes.MaynardS2.ex_filter' depends on axioms: [propext]
'TwinPrimes.MaynardS2.maynard_S2_example_eval' depends on axioms: [propext]
```

The library now has 22 files and 6076 lines in `lean/TwinPrimes/`.

## Not done / caveats

- **Bad pairs.** There is no S2 analogue of `maynard_S1_error_W` or `maynard_S1_diag_W` that drops the bad
  pairs (non-coprime [d_i, e_i]) inside S2. The CRT step assumes `hpw` per pair.
- **No division-free error bound.** There is no |q · count − (N − N0)/…| bound for S2, because the count
  of primes in an AP has no elementary finite estimate. That is exactly the BV input.
- **Coordinate convention.** The m-th coordinate uses `getD`, with defaults 1 and 0. Under the length
  hypotheses the defaults are never used.
- **Range.** The range is `[N0, N)`; Maynard's [N, 2N) is the case N0 = N, N ↦ 2N. The bound hypothesis
  then reads d_m < N + h_m.
