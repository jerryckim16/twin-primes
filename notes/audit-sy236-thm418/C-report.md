# Audit C: Song–Yue §4.3 "The IIb distribution estimate" (pp. 20–24)

Self-review by one agent. No independent second derivation was run. Sources: `03-IIb.txt`, `02-IIa.txt`, `01-defs-4.1.txt`, `05-HeathBrown.txt` (invocation only), and PDF pages 20–23 rendered to `img/` to check formulas (`(40)` has a complex conjugate on the second Φ, which pdftotext drops).
Scripts: `check_exponents.py` (output in `check_exponents.out`) and `sim_lemma45.py` (output in `sim_lemma45.out`).
**I had no access to Polymath8a [D.14a].** Everything said here about its Theorem 2.9, Lemma 1.3, Lemma 5.2/Cor. 5.3 and Corollary 4.16 comes from memory or from reconstructing the statement, and is marked as such.

## Claim card
Prop. 4.4. Fix σ∈(0,1) and v≥0. Let α, β be coefficient sequences (Def. 3.7) at scales M and N, with MN≍X and X^{7997/20000} ≤ N ≤ X^{11/25}. Assume **β (the shorter factor) is Siegel–Walfisz** (Def. 3.9). Then Σ_{d∈Q182(X;σ), d squarefree} τ(d)^v |Δ_full(α∗β;a,d)| ≪ X(log X)^{-C}, uniformly in (a,P(X))=1 and over families with common constants. No smoothness is assumed on either factor, and no SW is assumed on α.
Lemma 4.5 (combinatorial). Let γ*≤γ≤11/25. Every nonexceptional squarefree d∈Q182 with d ≥ X^{1/2-ζ} has r|d and u|q=d/r inside the windows (37). r contains every prime ≤ D0 that divides d. q is X^δ-smooth and has no prime ≤ D0.

## Verdict
**Proved modulo cited black boxes.** I found no genuine error in §4.3. The proof depends on:
- Polymath8a Corollary 4.16 (second bound);
- bilinear Bombieri–Vinogradov [D.14a, Thm 2.9];
- the standard divisor and progression bounds;
- the §4.2 dispersion set-up, which §4.3 reuses. I checked that each reused step carries over under the IIb hypotheses, but I did not re-audit §4.2 itself.

## Dependency graph
- (36) ← small moduli d ≤ X^{1/2}(log)^{-K} [bilinear BV, D.14a Thm 2.9]
- (36) ← exceptional moduli [divisor moments + progression divisor bound, D.14a L1.3, L5.2, C5.3]
- (36) ← the remaining moduli, through Lemma 4.5 and then the dispersion of §4.2:
  - Δ2 [BV in modulus r, with SW of β·1_{(n,q)=1}]
  - Δ1:
    - diagonal [progression divisor bound, RQ² ≤ X^{0.63036}]
    - h=0: cancellation when q0=1; when q0>D0, the (n,ℓ) count
    - h≠0 ← (44) ← (43) ← A1·A2:
      - (40) [D.14a Cor 4.16, 2nd bound]
      - (41) [elementary]
      - E1, E2, E3 [exact exponents]
- τ^v weights: Cauchy–Schwarz + progression divisor bound.

## Obligation matrix
Categories: (a) verified, (b) verified modulo a cited black box whose hypotheses were checked, (c) exposition gap an expert could fill, (d) genuine gap or error, (e) could not check.

| # | Item | Status |
|---|---|---|
| 1 | Statement: quantifiers, ranges, coefficient hypotheses. SW is on β, the shorter factor at scale N. α is arbitrary and is removed by Cauchy–Schwarz against a smooth majorant ψ_M. Range [X^{γ*}, X^{11/25}] overlaps IIa at 11/25. | (a) |
| 2 | Lemma 4.5, r-window: start G0 ≤ X^{2B+o(1)} is below the target because γ*−η2+2τ0−2B = 461/250000 > 0 (exact). Greedy overshoot < δ and η2−δ = 1/100000 = 5τ0 (exact), so r < X^{γ−3τ0}. Primes outside G0 are primes of ee', so they are ≤ X^δ and q has no primes ≤ D0. | (a) |
| 3 | Lemma 4.5, u-window: target a_{11/25}−η2+2τ0 = 17897/500000 > 0. q exceeds the target by 2ω+η2+τ0−ζ (6053/250000 − ζ). Window width is exactly δ. Edge cases: at γ=γ* and γ=11/25 the margins are strict (exact). Exceptional moduli and d < X^{1/2−ζ} are excluded and handled elsewhere. | (a) |
| 4 | Lemma 4.5 stress test: 4918 random D182-type moduli in exact log-space arithmetic, with γ ∈ {γ*, 11/25, random}, adversarial prime orders and all smooth primes of size δ. 0 failures. This is a sanity check, not the proof. | (a) |
| 5 | (38): every exponent was recomputed exactly (15759/25000, −27549/100000; 2A = 1/2+2ω). Minor: R ≪ NX^{−3τ0} actually holds, which is stronger than stated. | (a) |
| 6 | Common-divisor removal (39): q1 = u1·w1 coprime, U1 ≫ q0^{-1}X^{aγ−η2}, U1 ≤ X^{aγ−3τ0}. There is one factorization per (q,r), so no multiplicity. | (a) |
| 7 | Cauchy–Schwarz with (u1, q2, n) outside: A1 ≪ X^{o(1)} zNU1Q/q0² (needs Q ≪ N). The coefficients c_{h,u1,v1,q2} contain the selection indicator, the chosen factorization and the Poisson coefficient, and do not depend on n. | (a) |
| 8 | (40): moduli d'1 = r·q0·u1·[v1,v2] and d'2 = q2 are squarefree and coprime, with coprimality enforced by the nonzero coefficients. The phase coefficient mod p\|r is a(h1v2−h2v1)/(n·q0·u1·q2·v1·v2), so it is a unit multiple of h1v2−h2v1 (checked from Φ). The zero conventions match: (n, d'1) = (n+ℓr, q2) = 1. Mean-term ratios are ≤ (c,r)/r. | (b) |
| 9 | Use of Cor 4.16, second bound, without dense divisibility. Any d is d-densely divisible, so taking y = d is legitimate. I reconstructed the second bound from Weil bounds plus completion; the local factor where c≡0 gives only O(1) at nonzero frequencies, so the gcd terms stay harmless. If a length or size condition is required, N/q0 ≤ d/q0 holds as well, since d ≥ X^{1/2−ζ} > N. | (b), from memory |
| 10 | Applying Cor 4.16 "on each class mod q0". This needs n = c + q0·m: the q0-phase is constant, modulus d/q0, and the weight becomes a shifted smooth weight at scale N/q0. This is not spelled out in the paper. As I remember it, Polymath allows "shifted smooth" sequences, which would cover this. The same gap is in IIa. | (c) |
| 11 | (41): b≠0 contributes ≪ HV·τ(r)·X^{o(1)}·HV. b=0 contributes R·X^{o(1)}·HV, because h1v2 ≠ 0 means there is no divisor bound at 0. | (a) |
| 12 | (42), its normalization, the two forms of E1/E2, and the prefactor of (43): symbolic identities, all verified with sympy (difference 0). | (a) |
| 13 | E1, E2, E3 bounds. LP worst case over the admissible (R, Q, U1, q0): E1 exponent = (1+24ω+7η2−3γ)/2 − (7/2)·log q0, which is −1/25000 at γ*. E2 exponent = 8ω+3η2−γ, which is −16061/50000. E3 exponent = −τ0 exactly. All three are monotone as claimed. With κ = τ0/8 and ζ < τ0/1000, every term gives ex/2 + ζ + κ < 0 (exact). (44) follows. | (a) |
| 14 | Reused §4.2 steps under the IIb hypotheses: <br>• BV for small d needs N, M ≥ X^ε. <br>• Exceptional moduli do not depend on N. <br>• Δ2 uses BV in r with R ≪ X^{11/25−τ0}. <br>• The SW restriction needs primes of q > D0 and N/p ≥ X^{0.38}. <br>• Diagonal: RQ² ≤ X^{15759/25000} < X^{1−ε} and R/N ≤ X^{−τ0}. <br>• h=0: q0>1 implies q0>D0. <br>• Nonzero frequencies use (44) with the same normalization M·q0/(RQ²). | (b) |
| 15 | Swapped-factor pitfall (Remark 4.23): it does not occur. β is SW and is the factor kept inside the dispersion. α needs nothing. The only use of SW is BV in Δ2, which needs it on one factor. The Heath–Brown invocation (Prop. 4.11) proves SW for both grouped factors and puts the smaller one in the β slot. | (a) |
| 16 | Divisor weights τ^v. | (b) (same as IIa) |
| 17 | Pointers to Polymath §5.6, (5.38)–(5.42), Prop. 5.13 and [Sta26, Lemma 4]. Not load-bearing. | (e) |

## Defects found
None of type (d). Minor exposition points:
- item 10;
- the exact hypothesis list of Cor 4.16 is never quoted (the "polynomial length condition" is not named);
- Poisson coefficients are O(1) rather than ≤ 1 (trivial);
- (38) understates R ≪ NX^{−3τ0} (harmless).

## Remaining obligations
1. Check [D.14a, Cor 4.16] verbatim against the use in item 9:
   - squarefree, coprime moduli;
   - the dense-divisibility parameter y, which may be taken equal to d;
   - the form of the mean term (gcd ratios);
   - shifted smooth weights, or a congruence restriction mod q0;
   - the exact length or size hypothesis.
2. Check [D.14a, Thm 2.9]: both scales ≥ X^ε, SW on one factor, and constants uniform over families.
3. Check [D.14a, Lemma 1.3, Lemma 5.2, Cor. 5.3] (divisor bounds in progressions).
4. Audit §4.2 itself: the Δ1 averaging over b2, the four-correlation cancellation at h=0, q0=1, and the (n,ℓ) count. §4.3 imports these unchanged.

Strongest safe statement: Prop. 4.4 holds as stated, provided items 1–4 above are confirmed.
