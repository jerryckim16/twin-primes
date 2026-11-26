# Lean: bad pairs in S2 (Maynard, Lemma 5.2, algebraic/finite part only)

File: `lean/TwinPrimes/MaynardS2Hpw.lean` (233 lines, namespace `TwinPrimes.MaynardS2Hpw`, imports
`MaynardS2`). It is added to `lean/TwinPrimes.lean`; its 14 declarations are added to `lean/Audit.lean`.
Core Lean 4.35.0, no Mathlib, no `sorry`, no `native_decide`, no new axioms. Conventions (`s2Pred`,
`tupleDvd`, `mSieveSum`, `goodPair`, `ShiftsCop`, `getD m 1`) are those of `MaynardS2.lean` / `MaynardHpw.lean`.

## Main statements (copied)

```lean
theorem count_zero_of_not_good_S2 (hs ds es : List Nat) (W v0 N0 N m : Nat) (pr : Nat → Bool)
    (hd : ds.length = hs.length) (he : es.length = hs.length) (hH : ShiftsCop hs W)
    (hdW : ∀ d ∈ ds, Nat.gcd d W = 1) (heW : ∀ e ∈ es, Nat.gcd e W = 1)
    (hbad : goodPair ds es = false) :
    (List.range N).countP (s2Pred hs W v0 N0 m pr ds es) = 0

theorem count_zero_reduced_of_not_good (hs ds es : List Nat) (W v0 N0 N m : Nat)
    (pr : Nat → Bool) (hm : m < hs.length)
    (hd : ds.length = hs.length) (he : es.length = hs.length) (hH : ShiftsCop hs W)
    (hdW : ∀ d ∈ ds, Nat.gcd d W = 1) (heW : ∀ e ∈ es, Nat.gcd e W = 1)
    (hbad : goodPair (ds.eraseIdx m) (es.eraseIdx m) = false) :
    ((List.range N).countP fun n =>
      decide (N0 ≤ n) && n % W == v0 && pr (n + hs.getD m 0) &&
        tupleDvd (hs.eraseIdx m) n
          (List.zipWith Nat.lcm (ds.eraseIdx m) (es.eraseIdx m))) = 0

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
            (((List.range N).countP (s2Pred hs W v0 N0 m pr ds es) : Nat) : Int)).sum).sum

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
                  (List.zipWith Nat.lcm (ds.eraseIdx m) (es.eraseIdx m)) : Nat) : Int)).sum).sum
```

`maynard_S2_good_support` is the intermediate form. It has the same hypotheses as
`maynard_S2_good_reduced`, keeps the `s2Pred` count, and filters by `d_m = e_m = 1`, then by
`goodPair ds es`. Helper: `shiftsCop_eraseIdx` (`ShiftsCop` survives erasing a coordinate).

## Hypotheses

- `ShiftsCop hs W`: every x coprime to W is coprime to every h_i − h_j. In other words, every prime
  dividing a shift difference divides W. This is the weak form, as in `MaynardHpw`.
- `hDW` / `hdW`, `heW`: the entries are coprime to W (Maynard: λ is supported on (d, W) = 1).
- `hlen`: the tuples have length k.
- Only the reduced/support forms use `hpr`, `hm` and `hsmall`. They are the hypotheses of
  `maynard_S2_support` (pr accepts only primes, and d_m < N0 + h_m).
- Not needed: `v0 < W`, positivity of the entries, and squarefreeness. The bad-pair argument does not
  use the residue condition or primality, because the S2 count is a sub-count of the S1 count.

Argument: if n is counted, then [d_i, e_i] | n + h_i for all i. A common factor of two moduli divides
h_i − h_j, so it is coprime to itself, and therefore equals 1 (`pairwise_coprime_of_solvable`).

## Relation to Maynard Lemma 5.2

This is the algebraic/finite part only, with no analytic estimate. Maynard drops the pairs with
non-coprime [d_i, e_i] because they have no admissible n. `maynard_S2_good_reduced` therefore
expresses S2^(m) as a sum over pairs with d_m = e_m = 1 and pairwise coprime erased moduli. Those
moduli are exactly the hypothesis `hpw` of `maynard_S2_count_residue` (CRT, giving one class mod
W·∏_{i≠m}[d_i, e_i]). The per-pair `hpw` assumption noted in `lean-s2-expansion.md` is now discharged.
This file does not cover prime counts in APs, Bombieri–Vinogradov, the y^(m) change of variables, or
J_k^(m).

## Non-vacuity

The setting is `h = (0,2,6)`, `W = 6`, `v0 = 5`, `m = 0`, `N0 = 10`, with support
`{(1,1,1),(1,5,1),(1,1,5)}`.
- `ex_hH`: `ShiftsCop` holds. `ex_not_shiftsDvd`: `ShiftsDvd` fails, since 4 ∤ 6.
- `ex_bad_pair`: the pair `((1,5,1),(1,1,5))` passes the d_m = 1 filter and is bad, with moduli
  (1,5,5), both before and after erasing coordinate m.
- `ex_bad_count`: its S2 count up to 200 is 0 (`decide +kernel`).
- `ex_good_count_pos`: the good pair `((1,5,1),(1,5,1))` has a positive count.
- `ex_filter_sizes`: the filter keeps 7 of the 9 pairs.
- `maynard_S2_good_example`: an instance of `maynard_S2_good_reduced` with every hypothesis discharged.
- `maynard_S2_good_example_eval`: both sides of the good-support identity evaluated at N = 120.

## Build / audit

`lake build`: `Build completed successfully (26 jobs).` (previously 25). `lake env lean Audit.lean`:
239 lines (previously 225, +14).

| axioms | before | after |
|---|---|---|
| `[propext, Classical.choice, Quot.sound]` | 123 | 129 |
| `[propext, Quot.sound]` | 59 | 61 |
| `[propext]` | 15 | 21 |
| none | 28 | 28 |

No `sorryAx` and no other axiom appears.
