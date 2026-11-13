# Audit D: Song–Yue §4.4 (Type III), pp. 24–29: Proposition 4.6 and Lemma 4.7

Auditor: one subagent working alone (self-review, not an independent second derivation).
Sources: `04-TypeIII.txt`, `01-defs-4.1.txt`, `05-HeathBrown.txt`, and PDF pages 24–29, rendered to `img/p-24..29.png`
and checked against the text extraction. No internet access was used.
Polymath8a [D.14a] was NOT available as text. Every statement below about its exact content comes from memory and is labelled that way.

## 0. Claim cards

**Prop 4.6.** Fix 0<σ<1 and v≥0. Let α be a coefficient sequence at scale M≥1, and let ψ1, ψ2, ψ3 be smooth at scales Ni (Def 3.8).
Assume M N1N2N3 ≍ X, X^{1/5} ≪ Ni ≪ X^{2/5}, and NiNj ≫ X^{3/5}.
Then for f = α∗ψ1∗ψ2∗ψ3, Σ_{q∈Q182(X;σ), q squarefree} τ(q)^v |Δfull(f;a,q)| ≪ X(log X)^{-C1}, uniformly in (a,P(X))=1.
No Siegel–Walfisz (SW) assumption is made on α.

**Lemma 4.7.** Every squarefree q∈Q182 with q ≥ X^{1/2-ζ} has a divisor s0 with X^{343/1000} ≤ s0 ≤ X^{1899/5000} and S X^{-η3} < s0 < S,
where S = X^{143/375}. For every b|q, d = q/b = rs with (r,s)=1 and S/(bX^{η3}) < s < S.

**Routing (Prop 4.11, case 3).** Three atoms with 0.2002 ≤ ui ≤ 0.3999 and pair sums ≥ 0.6001 must satisfy the hypotheses (45).

## 1. Nature of the argument

This is a **re-derivation** of the Type III argument of Polymath8a §7 (the "Deligne" branch). It is not an invocation of a Polymath8a Type III theorem.
Dense divisibility is replaced by one fixed divisor window (Lemma 4.7), as in [Sta26, Lemma 7], which I could not check.
The only black boxes are:
- (BB1) the bilinear Bombieri–Vinogradov theorem for convolutions, with one SW factor [D.14a Thm 2.9 (memory)];
- (BB2) Deligne's bound |Kl3(t;d)| ≤ 3^{ω(d)} for squarefree d and unit t;
- (BB3) the complete-sum / correlation estimate for products of two Kl3 sums [D.14a Lemma 6.25, Cor 6.26]. It rests on Deligne–Katz.

So the line-by-line audit applies, and it was carried out.

## 2. Dependency graph

```
Prop4.6 ── small q ≤ X^{1/2}(logX)^{-K}: BB1 (SW factor = ψ1 at scale N1 ≥ X^{1/5}; other factor at scale ≥ X^{3/5})
        ── large q, intervals I(Q):
             averaging identity (fixed c_q, E_a over units mod P(X))           [internal, verified]
             Poisson + frequency truncation + Taylor in (q-Q)/Q              [internal sketch; standard]
             zero frequencies are independent of the residue (main quantity M_c) [internal, verified]
             CRT split F = (mod-b factor) × Kl3(aB*ℓ/(b^3 m); d)              [internal, verified numerically]
             mod-b factor ≤ b1♭b2♭b3♭/b^2, independent of t, d, m             [internal, verified numerically]
             Lemma 4.7 factorization d = rs                                  [internal, proved]
             Cauchy–Schwarz in (s,ℓ) → T1 T2                                 [internal, verified]
             correlation bound (49)                                          [BB3; gcd factor misstated, see §4]
             diagonal (50), off-diagonal (51)                                [internal, verified symbolically]
             Euler product over b_i                                          [internal, verified]
             exponents (52) → three margins                                  [exact arithmetic, verified]
        ── weights τ^v: progression divisor bound (Shiu-type) + Cauchy–Schwarz [standard]
```

## 3. Obligation matrix

Categories: (a) verified; (b) verified modulo a black box whose hypotheses were checked; (c) exposition gap an expert could fill; (d) genuine gap or error; (e) could not check.

| # | Obligation | Status |
|---|---|---|
| 1 | Statement typing: scales, quantifiers, "M ≥ 1", uniformity in a and in coefficients | (a) |
| 2 | N ≫ X^{9/10} and M ≪ X^{1/10} from the pair products | (a) |
| 3 | Lemma 4.7: existence of s0 in the window | (a), proof in §5 |
| 4 | Lemma 4.7: s = s0/(s0,b) divides d, (r,s)=1, S/(bX^{η3}) < s < S | (a) |
| 5 | Exact constants: s3=143/375; 343/1000+δ=903/2500<2B; 1/1500; 23/15000; 473/3000 | (a), `exponents.py` |
| 6 | Small moduli via BB1: hypotheses (SW for smooth ψ1 including the coprimality twist; polynomial scales) | (b), memory of BB1's exact scale conditions |
| 7 | Coverage: q ≤ X^{(1-σ)253/500} < X^{1/2+2ω}, with overlap X^{1/2-ζ} < X^{1/2}(log X)^{-K} | (a) |
| 8 | Averaging identity Σ\|Δ\| = S_c(a0) − E_a S_c(a) ≤ 2E (q \| P(X) because q is squarefree and < X) | (a) |
| 9 | Poisson, truncation \|h_i\| ≤ X^{ζ/2}H_i, Taylor separation (gain X^{-ζ/2} per order) | (c): only sketched, but correct |
| 10 | Zero-frequency terms are independent of t (Ramanujan sums) | (a) |
| 11 | CRT split; Kl3 argument aB*ℓ/(b^3 m); mod-b factor ≤ ∏b_i♭/b^2 and independent of t, d, m | (a), numerical check |
| 12 | Collecting ℓ = ℓ1ℓ2ℓ3 costs O(τ3(\|ℓ\|)); H_b = X^{3ζ/2}Q^3/(B*N); implicit (ℓ,b)=1 (dropping it only enlarges the bound) | (a)/(c) |
| 13 | Cauchy–Schwarz in (s,ℓ) with weights 1/s and s; T1 ≪ X^{o(1)}H_b; smooth majorant of the ℓ-interval | (a) |
| 14 | (49): correlation bound for modulus s[r1,r2] | (b) for the shape (H/L+1)L^{1/2}·∏_{bad p}p^{1/2}. **The bad-prime factor at p\|g is misstated**: (d-minor), repairable, see §4 |
| 15 | Completion with the mask (ℓ, s r1 r2)=1, and the "Lemma 6.25 when the length condition fails" remark | (c)/(e): depends on the exact form of BB3 |
| 16 | Diagonal D=0: divisor-bound count; (50) | (a), sympy |
| 17 | Σ_{s≍Z0} gcd(D,s)^{1/2} ≪ X^{o(1)}Z0 for D≠0; m-sum ≪ X^{o(1)}(M^2 + M g^{1/2}) | (a); the m-sum also holds for the corrected gcd |
| 18 | (51): t- and g-sums, including the endpoints min(1, (g/L0)^{1/2}) ≤ (g/L0)^{1/2} | (a), sympy |
| 19 | T bound from T1(T2,0 + T2,≠0); weakening the denominators to bB*^{1/2} | (a), sympy |
| 20 | Euler product Σ ∏b_i♭/(b^3 B*^{1/2}): factor 1 + O(p^{-3/2}) | (a), closed form vs brute force |
| 21 | (52) and the three exponents 1−1/3000, 1−137/3000, 1−71/2400 (each decreasing in ν = log_X N, so the worst case is ν = 9/10) | (a), exact |
| 22 | τ(q)^v weights via the progression divisor bound and Cauchy–Schwarz | (c): needs a Shiu-type bound uniform in a huge integer a. Standard |
| 23 | Routed range (Lemma 4.9 case 3 → (45)), including P ∈ [X/2^20, 2^21 X], smoothness of the atoms, no μ_Z atom, M ≥ 1 | (a) |
| 24 | Citation pointers ([D.14a] §7.2 eqs (7.11)–(7.15), Lemmas 6.25, 7.3, 7.4, 7.5, Cor 6.26; [Sta26, Lemma 7]) | (e): not available offline |

## 4. Demonstrated defect: the gcd factor in (49), p. 27

Write r_i = g t_i. Twisted multiplicativity gives Kl3(t; rs) = Kl3(t s̄^3; r) Kl3(t r̄^3; s); this was checked numerically.
So for p | g, the p-components of the two Kl3 factors in U have arguments c ℓ m̄_i (r_i s/p)^{-3}.
These coincide, which is the case where the local correlation is about p instead of O(1), exactly when

    m1 t1^3 ≡ m2 t2^3 (mod p),

not when m1 ≡ m2 (mod p).

Numerical check (`kl3_check.py`, with p = 7, t1 = 2, t2 = 3, s = 1):
- pairs with m1 = m2 give the small value 0.194;
- pairs with m1 t1^3 ≡ m2 t2^3 (mod 7) and m1 ≢ m2 give the large value 0.973.

At p = 31 and p = 61, the local correlation is about p (29.97 and 59.98) for equal arguments and about 1 otherwise.

Consequently, (49) as printed, with gcd(g, m1−m2)^{1/2}, is false in general. It can fail by a factor up to about g^{1/2}, which is not X^{o(1)}.
The p|s factor gcd(D,s) with D = m1 r1^3 − m2 r2^3 is correct; the check gave a large value exactly when D ≡ 0 (mod 11).

**Repair.** Replace gcd(g, m1−m2) by gcd(g, m1t1^3 − m2t2^3). Since (t1, g) = 1:

    Σ_{m1,m2≍M} gcd(g, m1t1^3 − m2t2^3)^{1/2} ≤ Σ_{e|g} e^{1/2} M(M/e+1) ≪ X^{o(1)}(M^2 + M g^{1/2}).

This is exactly the bound the paper uses next. So (51), (52) and all the margins are unchanged.

Classification: an error in a displayed inequality that is local, repairable, and has no effect on the exponents. I list it as (d-minor). For the theorem it behaves like (c).
Whether [D.14a, Cor 6.26] states the correct factor cannot be checked offline.

## 5. Lemma 4.7: proof check, with edge cases

Let G = ∏fi ∏fi' (the two rough groups). By (24), each group has log_X ≤ (1−σ)B ≤ B, so G ≤ X^{2B} = X^{1899/5000}.
q/G = ee' is X^δ-smooth. Because q is squarefree, all the factors are pairwise coprime.
- **If G ≥ X^{0.343},** take s0 = G.
- **Otherwise,** multiply in primes of ee' one at a time. This is possible because q ≥ X^{1/2-ζ} > X^{0.343} for ζ < 0.157. Stop at the first product ≥ X^{0.343}.
  The previous product was < X^{0.343}, and each prime is ≤ X^δ, so s0 < X^{0.343+δ} = X^{0.3612} < X^{0.3798}.

The window: (s3−η3, s3) = (0.342333…, 0.381333…), which contains [0.343, 0.3798], with margins 1/1500 and 23/15000.
Empty rough groups (G = 1) fall into the second case. The case G ≥ X^{0.343} with an empty smooth part is covered.

**Second part.** s = s0/(s0,b) is coprime to b and divides q, so s | d. (r,s) = 1 because d is squarefree.
Also s0/b ≤ s ≤ s0, which gives (47).
A randomized log-space stress test (`lemma47_sim.py`, 2·10^5 trials) found no failure. This is illustration only; the argument above is the proof.

Verdict: **proved as written.**

## 6. Routed Type III range (case 3 of Lemma 4.9)

Here Li = P^{ui} with P ∈ [X/2^20, 2^21 X], so Li ≍ X^{ui} with absolute constants. That gives:
- Ni ≫ X^{0.2002} ≫ X^{1/5};
- Ni ≪ X^{0.3999} ≪ X^{2/5};
- NiNj ≫ X^{0.6001} ≫ X^{3/5}.

The exact reserves are 1/5000, 1/10000 and 1/10000. M is the product of the remaining Lj, so M ≥ 1, and it is the scale of a divisor-bounded convolution.
There is always at least one remaining atom, because the number of atoms 2j is even and ≥ 4.
The selected atoms are w_L·n^{it}(·log n) with |t| ≤ (log X)^T, which is smooth in the sense of Def 3.8 with (log X)^{O(1)} derivative losses.
They cannot be μ_Z atoms, because Li ≫ X^{0.2002} > 2Z.

The proof of Prop 4.6 actually uses only N ≫ X^{9/10} (the routed range gives N ≫ X^{0.90015}) and M ≍ X/N, plus N1 ≥ X^ε for BB1.

Verdict: **the routed range is inside (45).**

## 7. Consistency cross-check (from memory, so heuristic)

From (52), the admissible window for s is
- s < 1/4 + 3σ/2 − 6ϖ (from T1),
- s − η > 1/2 − 3σ + 8ϖ (from T3),

with σ = 1/10. A window exists iff η < 9σ/2 − 1/4 − 14ϖ = 79/500.
That is exactly the Polymath8a Deligne Type III condition σ > 1/18 + 28ϖ/9 + 2δ/9 as I remember it, with η playing the role of δ.
So the paper's bookkeeping matches Polymath's final constraint structurally. The paper's window (0.3423, 0.3813) lies inside the admissible region (0.224 + η, 0.382).

## 8. Verdict

**Prop 4.6 is conditional on named inputs.** Those inputs are BB1, BB2 and BB3; the hypotheses checked so far are squarefree moduli, unit arguments, smooth weights and polynomial scales. It also needs the one local correction to (49) from §4.
With that correction, every internal step was verified, including all exponent arithmetic, which is exact.

**Lemma 4.7 is proved as written.**

**The routing of case 3 is verified.**

### Remaining obligations
1. Check against the actual text of [D.14a] (arXiv:1402.0811v3):
   - the exact statements of Lemma 6.25 and Cor 6.26: their gcd factors, coprimality masks, the length condition, and normalization;
   - Theorem 2.9 (bilinear BV): its scale hypotheses.
2. Optionally check that the Taylor-separation sketch (eqs (7.11)–(7.15) of [D.14a]) matches the argument as written.
3. Check [Sta26, Lemma 7], which I did not see.

## 9. Files and commands

- `python3 exponents.py`: exact rational checks of every displayed constant, the three exponents, the routed range, and the window constraint.
- `python3 bookkeeping.py`: sympy re-derivation of (50), (51), the T bound and (52), plus the Euler factor (brute force against closed form).
- `python3 kl3_check.py`: twisted multiplicativity; the CRT mod-b factor bound and its independence of t; the bad-prime test showing the error in (49).
- `python3 lemma47_sim.py`: randomized stress test of the Lemma 4.7 construction.
- `img/p-24..29.png`: the PDF pages used to check the formulas.
