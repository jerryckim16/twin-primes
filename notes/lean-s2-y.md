# Lean: the S2 change of variables y^(m) (Maynard, Lemma 5.2, eqs. (5.21)–(5.24), (5.26); algebraic/finite part only)

File: `lean/TwinPrimes/MaynardS2Y.lean` (510 lines, namespace `TwinPrimes.MaynardS2Y`, imports
`MaynardS1Diag`). It is added to `lean/TwinPrimes.lean`; its 33 declarations are added to `lean/Audit.lean`.
Core Lean 4.35.0, no Mathlib, no `sorry`, no `native_decide`, no new axioms. Finite checks use
`decide +kernel`. The conventions are those of `MaynardInv.lean` / `MaynardDiag.lean`:
- the box `box R k = {1..R}^k`;
- `tdvd` (coordinatewise divisibility) and `upSum R k f r = ∑_{r ∣ d} f d`;
- `tmu r = ∏ μ(r_i)` and `tphi r = ∏ φ(r_i)`;
- the m-th coordinate is `d.getD m 1`;
- all values are rationals.

Source read: arXiv:1311.4600v3, pp. 11–13, (5.18)–(5.27) and Lemma 5.3.

## Definitions

```lean
def gM (x : Nat) : Rat :=
  ((rng x).map fun v => if x % v = 0 then (mu (x / v) : Rat) * (totient v : Rat) else 0).sum
def tg (u : List Nat) : Rat := (u.map gM).prod
def tphiGcd (d e : List Nat) : Rat := ((((List.zipWith Nat.gcd d e).map totient).prod : Nat) : Rat)
def tphiLcm (d e : List Nat) : Rat := ((((List.zipWith Nat.lcm d e).map totient).prod : Nat) : Rat)
def fS2 (m : Nat) (lam : List Nat → Rat) (d : List Nat) : Rat :=
  if d.getD m 1 = 1 then lam d / tphi d else 0
def yS2 (R k m : Nat) (lam : List Nat → Rat) (r : List Nat) : Rat :=
  tmu r * tg r * upSum R k (fS2 m lam) r
def s2Form (R k m : Nat) (lam : List Nat → Rat) : Rat :=
  (((box R k).filter fun d => d.getD m 1 == 1).map fun d =>
    (((box R k).filter fun e => e.getD m 1 == 1).map fun e =>
      lam d * lam e * tphiGcd d e / (tphi d * tphi e)).sum).sum
```

`yS2` is exactly Maynard's (5.23), y^(m)_r = ∏ μ(r_i) g(r_i) ∑_{r|d, d_m=1} λ_d / ∏ φ(d_i), with the sum over
the box. **g:** Maynard's g is totally multiplicative with g(p) = p − 2. Here g is defined as `gM = μ ∗ φ`,
which needs no factorisation. This file proves g(p) = p − 2 for every prime p (`gM_prime`). It does **not**
prove that `gM` is multiplicative. So agreement with Maynard's g is proved on primes only, and checked by
`decide` on a few squarefree values (`gM 15 = 3`). Both functions satisfy ∑_{u|n} g(u) = φ(n) on squarefree
n, and Möbius inversion determines g on squarefree n from that relation. The identity used below is that
divisor-sum relation, not total multiplicativity.

## Main statements (copied)

```lean
theorem gM_prime (p : Nat) (hp : MuMult.IsPrime p) : gM p = (p : Rat) - 2

theorem gM_divisor_sum (R c : Nat) (hc : c ∈ rng R) :
    ((rng R).map fun x => if c % x = 0 then gM x else 0).sum = (totient c : Rat)

theorem tphiGcd_eq_sum (R : Nat) : ∀ (k : Nat) (d e : List Nat), d ∈ box R k → e ∈ box R k →
    tphiGcd d e = ((box R k).map fun u =>
      if (tdvd u d && tdvd u e) = true then tg u else 0).sum

theorem maynard_S2_diag_g (R k m : Nat) (lam : List Nat → Rat) :
    s2Form R k m lam
      = ((box R k).map fun u => tg u * (upSum R k (fS2 m lam) u * upSum R k (fS2 m lam) u)).sum

theorem yS2_eq_zero (R k m : Nat) (lam : List Nat → Rat) (r : List Nat)
    (hr : r.getD m 1 ≠ 1) : yS2 R k m lam r = 0

theorem maynard_S2_diag_y (R k m : Nat) (lam : List Nat → Rat)
    (hsq : ∀ d ∈ box R k, lam d ≠ 0 → ∀ x ∈ d, mu x ≠ 0) :
    s2Form R k m lam
      = ((box R k).map fun u => yS2 R k m lam u * yS2 R k m lam u / tg u).sum

theorem maynard_S2_diag_lcm (R k m : Nat) (lam : List Nat → Rat)
    (hphi : ∀ a b, a ∈ rng R → b ∈ rng R → mu a ≠ 0 → mu b ≠ 0 →
      totient (Nat.lcm a b) * totient (Nat.gcd a b) = totient a * totient b)
    (hsq : ∀ d ∈ box R k, lam d ≠ 0 → ∀ x ∈ d, mu x ≠ 0) :
    (((box R k).filter fun d => d.getD m 1 == 1).map fun d =>
      (((box R k).filter fun e => e.getD m 1 == 1).map fun e =>
        lam d * lam e / tphiLcm d e).sum).sum
      = ((box R k).map fun u => yS2 R k m lam u * yS2 R k m lam u / tg u).sum

theorem maynard_S2_diag_lcm_R12 (R k m : Nat) (hR : R ≤ 12) (lam : List Nat → Rat)
    (hsq : ∀ d ∈ box R k, lam d ≠ 0 → ∀ x ∈ d, mu x ≠ 0) :
    -- same conclusion as maynard_S2_diag_lcm

theorem maynard_S2_lam_of_y (R k m : Nat) (lam : List Nat → Rat)
    (hsq : ∀ d ∈ box R k, lam d ≠ 0 → ∀ x ∈ d, mu x ≠ 0)
    (hg : ∀ r ∈ box R k, tg r = 0 → upSum R k (fS2 m lam) r = 0)
    (d : List Nat) (hd : d ∈ box R k) :
    tmu d * tphi d * upSum R k (fun r => yS2 R k m lam r / tg r) d
      = if d.getD m 1 = 1 then lam d else 0
```

Also in the file:
- `maynard_S2_diag_y_restrict`: the u-sum may be restricted to u_m = 1.
- `quad_diag`: the generic diagonalisation, for any kernel K(d,e) = ∑_{u|d,u|e} c(u).
- `phi_gcd_sum_rat`: one coordinate of `tphiGcd_eq_sum`.
- `gM_range`, `totient_prime` (φ(p) = p − 1), `totient_one`, `tdvd_getD`, `natprod_phi_lcm_gcd`.
- `phi_lcm_gcd_upto_12`: φ([a,b])φ((a,b)) = φ(a)φ(b) for a, b ≤ 12, by `decide +kernel`.

## Correspondence with Maynard

| Lean | Maynard |
|---|---|
| `gM_divisor_sum`, `phi_gcd_sum_rat`, `tphiGcd_eq_sum` | (5.21) in the form φ((d,e)) = ∑_{u∣d,e} g(u). The 1/φ([d,e]) form is reached via `hphi` below |
| `yS2` | definition (5.23) |
| `yS2_eq_zero` | "y^(m)_r = 0 unless r_m = 1" (just after (5.23)) |
| `maynard_S2_diag_y` / `_restrict` | the identity behind the main term of (5.24) and the first term of (5.26): ∑ λ_d λ_e / ∏ φ([d_i,e_i]) = ∑_u (y^(m)_u)² / ∏ g(u_i) |
| `maynard_S2_diag_lcm` | the same identity, written with 1/∏ φ([d_i,e_i]) as in (5.18)/(5.22) |
| `maynard_S2_lam_of_y` | inversion of (5.23) (Maynard uses it implicitly: λ is determined by y^(m) on d_m = 1) |

**How the hypotheses differ from Maynard's**

1. *No coprimality restriction, no s_{i,j}.* Maynard's main term (5.18) is a sum Σ' over pairs with W and the
   [d_i,e_i] pairwise coprime. He then removes the restriction with the variables s_{i,j}, (5.22)/(5.24), and
   bounds the terms with s_{i,j} ≠ 1 in (5.25). Our `s2Form` instead runs over **all** pairs of the box with
   d_m = e_m = 1. For this unrestricted form the diagonalisation is exact: (5.24) holds with every s_{i,j} = 1
   and no error term. This mirrors what `MaynardDiag.lean` does for S1. This file does not relate the
   unrestricted form to Maynard's Σ', i.e. it does not estimate the bad pairs or the s_{i,j} terms.
2. *Squarefree support* (`hsq`) is used only to get μ(u)² = 1, and it is Maynard's assumption.
   Lean's convention x/0 = 0 makes the terms with g(u) = 0 vanish on both sides; for example g(2) = 0 for any
   u with an even entry. So `maynard_S2_diag_y` needs no hypothesis g ≠ 0. Maynard has (u,W) = 1, so u is odd.
3. *(5.21) itself.* 1/φ([d,e]) = φ((d,e)) / (φ(d)φ(e)) is equivalent to φ([a,b])φ((a,b)) = φ(a)φ(b). That is
   true for all a, b, but this file does **not** prove it in general, because multiplicativity of φ is not
   available in the project. It is the hypothesis `hphi`, needed for squarefree a, b ≤ R only, and is checked
   by `decide` for R ≤ 12 (`maynard_S2_diag_lcm_R12`).
4. *Inversion.* `hg` asks that ∑_{r|d, d_m=1} λ_d/φ(d) = 0 whenever ∏ g(r_i) = 0. On Maynard's support
   (entries coprime to W, so odd) this should follow from g(r) ≠ 0 for odd squarefree r. That fact is not
   proved here, since it needs multiplicativity of `gM`.

## NOT covered

- The step from S2 (the count, `MaynardS2*.lean`) to the form `s2Form`. That step needs prime counts in APs
  (X_N/φ(q) + E), Bombieri–Vinogradov and (5.19)–(5.20).
- The Σ' restriction and the s_{i,j} contributions (5.25), and X_N ~ N/log N (5.27).
- Lemma 5.3 (y^(m) in terms of y), including its exact part (5.28)–(5.30). That part needs φ and μ·id/φ to
  be multiplicative.
- Multiplicativity of φ and of g; the general (5.21) identity (see hypothesis 3 above).
- Anything analytic.

## Non-vacuity

- `gM_values`: g(1) = 1, g(2) = 0, g(3) = 1, g(5) = 3, g(15) = 3 = g(3)g(5), and g(4) = 1. Since g(2)² = 0 ≠ 1,
  `gM` differs from a totally multiplicative g at non-squarefree arguments; those arguments are irrelevant.
- `lamEx` on {1,2,3}², with m = 0: λ(1,1) = 2, λ(1,3) = −1, and λ = 0 elsewhere.
- `ex_hsq` and `ex_hg` hold.
- `maynard_S2_diag_example`: both sides of `maynard_S2_diag_y` evaluate to 5/2 (`decide +kernel`).
- `maynard_S2_diag_lcm_example` and `maynard_S2_lam_of_y_example` are instances with every hypothesis
  discharged.
- `ex_y_values`: y^(0)_{(1,3)} = 1/2 and y^(0)_{(3,1)} = 0.

## Build / audit

`lake build`: `Build completed successfully (27 jobs).` (previously 26). `lake env lean Audit.lean`:
272 lines (previously 239, +33).

| axioms | before | after |
|---|---|---|
| `[propext, Classical.choice, Quot.sound]` | 129 | 154 |
| `[propext, Quot.sound]` | 61 | 67 |
| `[propext]` | 21 | 21 |
| none | 28 | 30 |

No `sorryAx` and no other axiom appears.
