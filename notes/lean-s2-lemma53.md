# Lean: Maynard's Lemma 5.3, exact part (y^(m) in terms of y; eqs. (5.28)–(5.30), (5.32))

File: `lean/TwinPrimes/MaynardS2Lemma53.lean` (520 lines, namespace `TwinPrimes.MaynardS2Lemma53`, imports
`MaynardS2Mult`). It is added to `lean/TwinPrimes.lean`, and its 36 declarations are added to
`lean/Audit.lean`. Core Lean 4.35.0, no Mathlib, no `sorry`, no `native_decide`, no new axioms. Finite checks
use `decide +kernel`.

The conventions are those of `MaynardInv.lean` / `MaynardS2Y.lean` (see `notes/lean-s2-y.md`):
- the box `box R k = {1..R}^k`;
- `tdvd` and `upSum`;
- `tmu r = ∏ μ(r_i)`, `tphi r = ∏ φ(r_i)`, `tN d = ∏ d_i`;
- `gM = μ ∗ φ` and `tg u = ∏ g(u_i)`;
- the m-th coordinate is `r.getD m 1`, and `a.set m 1` is a with a_m replaced by 1.

Source read: arXiv:1311.4600v3:
- p. 11: (5.7) and (5.8), the change of variables λ ↔ y;
- p. 12: (5.21)–(5.23), the definition of y^(m);
- p. 13: Lemma 5.3 and its proof, (5.28)–(5.32).

## Objects

- **λ from y.** `λ = MaynardInv.maynardLam R k y`, with `λ_d = tmu d · tN d · ∑_{d ∣ a} y_a / tphi a`. This
  is (5.8) in the form λ_d = μ(d) d ∑_{d|a} y_a/φ(a). Maynard prints λ_d / ∏ μ(d_i) d_i, which is the same
  thing because μ(d_i) = ±1 on the support.
- **y^(m).** `y^(m) = MaynardS2Y.yS2 R k m λ`, with
  `y^(m)_r = tmu r · tg r · ∑_{r ∣ d, d_m = 1} λ_d / tphi d`. This is exactly (5.23).

## Definitions (new)

```lean
def hq (x : Nat) : Rat := (mu x : Rat) * (x : Rat) / (totient x : Rat)          -- μ(x) x / φ(x)
def relSum (r a : Nat) : Rat := dvs a (fun x => if x % r = 0 then hq x else 0)   -- ∑_{r|x|a} h(x)
def cofAll : List Nat → List Nat → Rat                                          -- ∏ μ(a_i) r_i / φ(a_i)
  | x :: r, c :: a => (mu c : Rat) * (x : Rat) / (totient c : Rat) * cofAll r a
  | _, _ => 1
def tw (r : List Nat) : Rat :=                                                  -- ∏ g(r_i) r_i / φ(r_i)²
  (r.map fun x => gM x * (x : Rat) / ((totient x : Rat) * (totient x : Rat))).prod
```

Maynard's product ∏_{i≠m} μ(a_i) r_i/φ(a_i) in (5.30) is `cofAll r (a.set m 1)`. When r_m = 1, the m-th
factor becomes μ(1)·1/φ(1) = 1.

## Main statements (copied)

```lean
theorem relSum_eq (a : Nat) : 1 ≤ a → Sqf a → ∀ r, r ∣ a →
    relSum r a = (mu a : Rat) * (r : Rat) / (totient a : Rat)

theorem tupleSum_eq (R : Nat) : ∀ (k : Nat) (r a : List Nat), r ∈ box R k → a ∈ box R k →
    (∀ c ∈ a, Sqf c) →
    ((box R k).map fun d => if (tdvd r d && tdvd d a) = true then
        tmu d * tN d / tphi d else 0).sum
      = if tdvd r a = true then cofAll r a else 0

theorem maynard_lemma53_exact (R k m : Nat) (y : List Nat → Rat)
    (hsq : ∀ a ∈ box R k, y a ≠ 0 → ∀ x ∈ a, mu x ≠ 0)
    (r : List Nat) (hr : r ∈ box R k) (hrm : r.getD m 1 = 1) :
    yS2 R k m (maynardLam R k y) r
      = tmu r * tg r * ((box R k).map fun a =>
          if tdvd r a = true then y a / tphi a * cofAll r (a.set m 1) else 0).sum

theorem maynard_lemma53_split (R k m : Nat) (y : List Nat → Rat)
    (hsq : ∀ a ∈ box R k, y a ≠ 0 → ∀ x ∈ a, mu x ≠ 0)
    (r : List Nat) (hr : r ∈ box R k) (hrm : r.getD m 1 = 1) (hm : m < k)
    (hrsq : ∀ x ∈ r, mu x ≠ 0) :
    yS2 R k m (maynardLam R k y) r
      = tw r * ((rng R).map fun t => y (r.set m t) / (totient t : Rat)).sum
        + tmu r * tg r * ((box R k).map fun a =>
            if tdvd r a = true ∧ a.set m 1 ≠ r then y a / tphi a * cofAll r (a.set m 1)
            else 0).sum
```

Also in the file:
- `oneSum_eq` / `oneSum_zero`: the 1-d sum taken over x ∈ {1..R}, in the cases r ∣ a and r ∤ a;
- `hq_prime_mul`: h(p e) = −(p/(p−1)) h(e) for p ∤ e;
- `dvs_one`, `dvs_congr`, `dvs_mul_left`, `dvs_zero`;
- `tdvd_set_iff`: (d ∣ a ∧ d_m = 1) ↔ d ∣ a[m↦1];
- `tdvd_set_of`, `tdvd_set_self`, `tdvd_refl`, `set_mem_box`, `set_set_one`;
- `tphi_set`: φ(r[m↦t]) = φ(t) φ(r) if r_m = 1;
- `rsum_set_eq`: the box tuples with a[m↦1] = r are exactly r[m↦t], t ≤ R;
- `coef_eq_tw`: ∏ μ(r_i) g(r_i) · cofAll r r / ∏ φ(r_i) = ∏ g(r_i) r_i/φ(r_i)², for squarefree entries;
- `sqf_one`, `one_mod_eq`, `totient_ne_zero_rat`, `natCast_sub_one_ne_zero`, `hqTuple_cons`.

**Proof route.** `relSum_eq` uses strong induction on a. Write a = p a' with p prime (p ∤ a' since a is
squarefree), and split the divisors of p a' using `MaynardS2Mult.dvs_prime_mul`.
- If p ∤ r, then ∑ = (1 − p/(p−1)) ∑_{r|x|a'} = −1/(p−1) · μ(a') r/φ(a').
- If p | r, the divisors of a' contribute nothing, and ∑ = −p/(p−1) · μ(a') (r/p)/φ(a').

In both cases the result is μ(p a') r / φ(p a'). The proof uses μ(p e) = −μ(e) (`mu_prime_mul`) and
φ(p e) = (p−1)φ(e) (`totient_mul_of_not_dvd`).

`tupleSum_eq` tensorises this over the coordinates. The condition d_m = 1 is absorbed by replacing a with
a[m↦1] (`tdvd_set_iff`). With that, `maynard_lemma53_exact` is a single swap of the d and a sums.

## Correspondence with Maynard

| Lean | Maynard (arXiv v3) |
|---|---|
| `maynardLam` (existing) | (5.8), p. 11 |
| `yS2` (existing) | (5.23), p. 12 |
| unfolding `yS2 (maynardLam y)` | (5.28), p. 13 |
| `rsum_comm` step in `maynard_lemma53_exact` | (5.29): swap of the d and a sums |
| `relSum_eq`, `tupleSum_eq` | "evaluate the sum over d₁,…,d_k explicitly" (between (5.29) and (5.30)) |
| `maynard_lemma53_exact` | (5.30), exactly |
| `maynard_lemma53_split`, first term | main term of (5.32): ∏ g(r_i) r_i/φ(r_i)² · ∑_{a_m} y_{r_1,…,a_m,…,r_k}/φ(a_m) |
| `maynard_lemma53_split`, second term | the a_j ≠ r_j (j ≠ m) terms that (5.31) bounds; here an explicit exact sum |

**How the statement and hypotheses differ from Maynard's**

1. **The exact identity is (5.30), not the Lemma 5.3 formula.**
   - The formula y^(m)_r = ∏ μ(r_i)g(r_i) · ∑_{a_m} y/φ(a_m) is not an exact identity.
   - Exactly, the sum runs over all a with r ∣ a, weighted by ∏_{i≠m} μ(a_i) r_i/φ(a_i).
   - Restricting to a_j = r_j for j ≠ m gives the coefficient ∏ g(r_i) r_i/φ(r_i)². It is not ∏ μ(r_i)g(r_i),
     and it is not 1.
   - Lemma 5.3 as printed has coefficient 1 and an O(·) term. It comes from two approximations, neither of
     which is formalised:
     - the bound (5.31) on the a_j ≠ r_j terms;
     - g(p)p/φ(p)² = 1 + O(p⁻²) with p > D₀.
2. **Box instead of Maynard's support.**
   - All sums are over {1..R}^k.
   - Maynard's support is: ∏ r_i < R, ∏ r_i squarefree, (∏ r_i, W) = 1. It lies inside the box, and y
     vanishes outside it.
   - The box is closed under coordinatewise divisors, so the d-sum and the a-sum in (5.28)–(5.30) are taken
     exactly. No truncation error arises.
   - The main-term sum over a_m runs over a_m ≤ R. The support of y cuts it down to Maynard's range
     ((a_m, W) = 1, a_m ∏_{i≠m} r_i < R) automatically.
3. **Squarefree support.**
   - `hsq` asks only that every entry of a tuple in supp y is squarefree.
   - It does not ask that the entries be pairwise coprime, that the product be squarefree, or that the entries
     be coprime to W. Everything here is coordinatewise, and μ(r) means ∏ μ(r_i).
   - Maynard's support condition implies `hsq`.
   - W plays no role in the exact identity. In Maynard it only enters the estimate (5.31): (a_j, W) = 1 forces
     a_j = r_j or a_j > D₀ r_j.
4. **r_m = 1** (`hrm`) is Maynard's hypothesis. For r_m ≠ 1, y^(m)_r = 0 (`MaynardS2Y.yS2_eq_zero`).
   - The exact identity needs no squarefreeness of r. If r is not squarefree, both sides carry the factor
     ∏ μ(r_i) = 0.
   - The split form uses `hrsq` and `m < k` only to rewrite the main coefficient as ∏ g(r_i) r_i/φ(r_i)², and
     to reindex a = r[m↦a_m].

## NOT covered

- The bound (5.31) on the error part E. It needs (a_j, W) = 1 ⇒ a_j > D₀ r_j, sums of μ²/φ², and log R
  bounds.
- g(p)p/φ(p)² = 1 + O(p⁻²), and the replacement of ∏ g(r_i) r_i/φ(r_i)² by 1 + O(D₀⁻¹).
- The final O(y_max φ(W) log R / (W D₀)) of Lemma 5.3. Anything analytic.
- The use of Lemma 5.3 in §6 (substituting the smooth choice (6.3) of y).

## Non-vacuity

- `yEx` on {1..6}² has support (1,3) ↦ 2, (5,3) ↦ 1, (2,3) ↦ −1, (1,6) ↦ 1/2, (3,1) ↦ 1. All entries are
  squarefree (`ex_hsq`, decide).
- `maynard_lemma53_exact_example` and `maynard_lemma53_split_example` are the theorems at r = (1,3), m = 0,
  with every hypothesis discharged (`ex_hsq`, `ex_r`, `rfl`, `decide`).
- `ex_values` (`decide +kernel`):
  - y^(0)_{(1,3)} = 9/16;
  - the (5.32) main term is (3/4)(2 − 1 + 1/4) = 15/16;
  - the error part is −3/8, coming from a = (1,6). So the split is not trivial: the main term alone is not
    exact;
  - y^(1)_{(3,1)} = 3/4;
  - `cofAll (1,3) (1,6)` = μ(6)·3/φ(6) = 3/2.

## Build / audit

`lake build`: `Build completed successfully (29 jobs).` (previously 28). `lake env lean Audit.lean`:
337 lines (previously 301, +36).

| axioms | before | after |
|---|---|---|
| `[propext, Classical.choice, Quot.sound]` | 172 | 204 |
| `[propext, Quot.sound]` | 75 | 78 |
| `[propext]` | 21 | 22 |
| none | 33 | 33 |

No `sorryAx` and no other axiom appears. `grep` finds no `sorry`, `native_decide` or `axiom` in the new file.
