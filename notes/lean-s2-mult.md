# Lean: multiplicativity of φ and g = μ ∗ φ; the S2 theorems without `hphi` / `hg`

File: `lean/TwinPrimes/MaynardS2Mult.lean` (501 lines, namespace `TwinPrimes.MaynardS2Mult`, imports
`MaynardS2Y`). It is added to `lean/TwinPrimes.lean`, and its 29 declarations are added to `lean/Audit.lean`.
Core Lean 4.35.0, no Mathlib, no `sorry`, no `native_decide`, no new axioms. The conventions are those of
`MaynardS2Y.lean` (see `notes/lean-s2-y.md`):
- `totient` is the counting definition from `Selberg.lean`;
- `gM` is μ ∗ φ;
- `IsPrime`/`Sqf` come from `MuMult.lean`;
- the box `{1..R}^k` and `tdvd`/`upSum` come from `MaynardInv.lean`.

Purpose: `MaynardS2Y` left two arithmetic hypotheses open.
- **`hphi`**, in `maynard_S2_diag_lcm`, was φ([a,b])φ((a,b)) = φ(a)φ(b) for squarefree a, b ≤ R. It was
  checked only for R ≤ 12, by `decide`.
- **`hg`**, in `maynard_S2_lam_of_y`, was "∏ g(r_i) = 0 ⇒ ∑_{r|d, d_m=1} λ_d/φ(d) = 0".

This file proves `hphi` for **all** a, b, with no side conditions. It replaces `hg` by Maynard's own support
condition, entries coprime to W with 2 ∣ W (that is, odd entries), and derives `hg` from it.

## Proof routes (no CRT bijection, no Mathlib)

- **φ at a prime factor.** For p prime and every x, φ(p x) = p φ(x) if p ∣ x and φ(p x) = (p − 1) φ(x) if
  p ∤ x. The proof counts residues:
  - #{k < j n : gcd(k+1, n) = 1} = j φ(n), by periodicity;
  - when p ∤ n, the residues coprime to n that are divisible by p are k + 1 = p(j+1) with j < n.
    `Gauss.cnt_mul` counts them, and there are φ(n) of them.
- **φ([a,b])φ((a,b)) = φ(a)φ(b).** The proof uses strong induction on a, and writes a = p a' with p prime.
  Then gcd(p a', b) is either gcd(a', b) or p·gcd(a', b), because it lies between them in divisibility and
  the quotient divides p.
  - In the first case lcm(p a', b) = p·lcm(a', b), and p ∣ lcm(a', b) ⇔ p ∣ a'.
  - In the second case the lcm is unchanged, and p ∣ gcd(a', b) ⇔ p ∣ a'.

  In both cases the factor (p or p − 1) is the same on both sides.
- **g(p n) = (p − 2) g(n)** for p ∤ n. The divisors of p n split into the divisors v of n and the
  multiples p e with e ∣ n (`dvs_prime_mul`). The first group contributes −μ(n/v)φ(v), using
  `MuMult.mu_prime_mul`. The second contributes μ(n/e)(p − 1)φ(e).

## Main statements (copied)

```lean
theorem totient_prime_mul (p x : Nat) (hp : IsPrime p) :
    totient (p * x) = (if p ∣ x then p else p - 1) * totient x

theorem totient_lcm_mul_gcd (a : Nat) : ∀ b,
    totient (Nat.lcm a b) * totient (Nat.gcd a b) = totient a * totient b

theorem totient_mul_coprime (m n : Nat) (h : Nat.Coprime m n) :
    totient (m * n) = totient m * totient n

theorem gM_prime_mul (p n : Nat) (hp : IsPrime p) (hn : 1 ≤ n) (hpn : ¬ p ∣ n) :
    gM (p * n) = ((p : Rat) - 2) * gM n

theorem gM_mul_coprime_sqf (m : Nat) : Sqf m → ∀ n, Nat.Coprime m n →
    gM (m * n) = gM m * gM n

theorem gM_pos_of_odd_sqf (n : Nat) : 1 ≤ n → Sqf n → n % 2 = 1 → 0 < gM n

theorem hg_of_odd (R k m : Nat) (lam : List Nat → Rat)
    (hsq : ∀ d ∈ box R k, lam d ≠ 0 → ∀ x ∈ d, mu x ≠ 0)
    (hodd : ∀ d ∈ box R k, lam d ≠ 0 → ∀ x ∈ d, x % 2 = 1) :
    ∀ r ∈ box R k, tg r = 0 → upSum R k (fS2 m lam) r = 0

theorem maynard_S2_diag_lcm_all (R k m : Nat) (lam : List Nat → Rat)
    (hsq : ∀ d ∈ box R k, lam d ≠ 0 → ∀ x ∈ d, mu x ≠ 0) :
    (((box R k).filter fun d => d.getD m 1 == 1).map fun d =>
      (((box R k).filter fun e => e.getD m 1 == 1).map fun e =>
        lam d * lam e / tphiLcm d e).sum).sum
      = ((box R k).map fun u => yS2 R k m lam u * yS2 R k m lam u / tg u).sum

theorem maynard_S2_lam_of_y_odd (R k m : Nat) (lam : List Nat → Rat)
    (hsq : ∀ d ∈ box R k, lam d ≠ 0 → ∀ x ∈ d, mu x ≠ 0)
    (hodd : ∀ d ∈ box R k, lam d ≠ 0 → ∀ x ∈ d, x % 2 = 1)
    (d : List Nat) (hd : d ∈ box R k) :
    tmu d * tphi d * upSum R k (fun r => yS2 R k m lam r / tg r) d
      = if d.getD m 1 = 1 then lam d else 0

theorem maynard_S2_lam_of_y_W (R k m W : Nat) (hW : 2 ∣ W) (lam : List Nat → Rat)
    (hsq : ∀ d ∈ box R k, lam d ≠ 0 → ∀ x ∈ d, mu x ≠ 0)
    (hcop : ∀ d ∈ box R k, lam d ≠ 0 → ∀ x ∈ d, Nat.Coprime x W)
    (d : List Nat) (hd : d ∈ box R k) :
    tmu d * tphi d * upSum R k (fun r => yS2 R k m lam r / tg r) d
      = if d.getD m 1 = 1 then lam d else 0
```

Also in the file:
- the counting helpers `cnt_add`, `periodic_iter`, `cnt_periodic`, `cnt_split`, `cnt_coprime_mul`;
- `totient_eq_cnt`, `totient_zero`, `totient_mul_of_dvd`, `totient_mul_of_not_dvd`;
- `dvs` (the divisor sum over `rng n`), `gM_eq_dvs`, `gM_zero`, `gM_one`, `natCast_sub_one`, `dvs_prime_mul`;
- `tg_pos_of_tdvd`: ∏ g(u_i) > 0 whenever u ∣ d coordinatewise and every entry d_i is ≥ 1, odd and
  squarefree.

## What this changes in `MaynardS2Y`

| `MaynardS2Y` | hypothesis | now |
|---|---|---|
| `maynard_S2_diag_lcm` | `hphi` (checked only for R ≤ 12) | `maynard_S2_diag_lcm_all`: only `hsq` remains, for every R, k, m |
| `maynard_S2_lam_of_y` | `hg` | `maynard_S2_lam_of_y_odd` / `_W`: `hg` replaced by "entries odd" / "entries coprime to W, 2 ∣ W" |

- The remaining hypothesis `hsq` (squarefree support) is Maynard's own assumption.
- `hodd` is also Maynard's: (d_i, W) = 1 and 2 ∣ W.
- `hg` cannot be dropped with nothing in its place, since g(2) = 0.
- With `gM_mul_coprime_sqf` and `gM_prime`, g(n) = ∏_{p|n}(p − 2) on squarefree n follows by induction.
  This means `gM` agrees with Maynard's totally multiplicative g on every squarefree argument, the only
  arguments that occur. The product formula itself is not stated as a separate theorem.

## NOT covered / what remains

- **Multiplicativity of `gM` when neither factor is squarefree.** This would be g(m n) = g(m) g(n) for all
  coprime m, n, e.g. g(9·4) = g(9) g(4). It is not proved. Only the case with m squarefree is proved.
  It is not needed: `gM` enters only at entries of squarefree tuples. The obstruction is that
  g(p n) is not a constant multiple of g(n) when p ∣ n, so the general case needs the divisor
  bijection d ∣ m n ↔ (d₁ ∣ m, d₂ ∣ n).
- Everything listed as NOT covered in `notes/lean-s2-y.md`, apart from the multiplicativity of φ and of g on
  squarefree arguments:
  - the Σ′ / s_{i,j} restriction, (5.25)–(5.27);
  - Lemma 5.3, whose exact part (5.28)–(5.30) still needs μ·id/φ multiplicativity;
  - prime counts in APs and Bombieri–Vinogradov;
  - anything analytic.

## Non-vacuity

- `ex_hodd`: `MaynardS2Y.lamEx` (support (1,1), (1,3)) has odd entries (`decide +kernel`).
- `maynard_S2_lam_of_y_odd_example`: the instance at `lamEx`. It replaces `MaynardS2Y.ex_hg`, which was
  checked by `decide`, with the general argument.
- `mult_values`: φ(36) = 12 = φ(4)φ(9), g(105) = 15 = 1·3·5, g(9) = 4. The last one shows that g is not
  ∏(p − 2) at non-squarefree arguments.

## Build / audit

`lake build`: `Build completed successfully (28 jobs).` (previously 27). `lake env lean Audit.lean`:
301 lines (previously 272, +29).

| axioms | before | after |
|---|---|---|
| `[propext, Classical.choice, Quot.sound]` | 154 | 172 |
| `[propext, Quot.sound]` | 67 | 75 |
| `[propext]` | 21 | 21 |
| none | 30 | 33 |

No `sorryAx` and no other axiom appears.
