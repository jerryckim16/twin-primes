# Audit of Song–Yue §4.2 ("The IIa distribution estimate"), pp. 15–20

Scope: Proposition 4.2, Lemma 4.3, and the proof of Proposition 4.2. The formulas were checked against
rendered PDF pages 15–19 (`img/p-15.png` … `img/p-19.png`), not only against the pdftotext extraction.
This is a self-review by one agent, not an independent second audit.

## Claim card

**Prop 4.2.** Fix 0<σ<1 and v≥0. Let α, β be coefficient sequences (Def 3.7) at scales M, N with MN≍X and
X^{11/25} ≤ N ≤ X^{1/2}, and let β (the *shorter* factor) be Siegel–Walfisz (Def 3.9, including the
auxiliary coprimality parameter r). Then for every fixed C, uniformly in (a,P(X))=1 and in the
coefficient families with common constants,
  Σ_{d∈Q182(X;σ), d squarefree} τ(d)^v |Δ_full(α*β; a, d)| ≪ X (log X)^{-C}.
No smoothness of α or β is assumed. No dense divisibility is assumed. Moduli satisfy d ≤ X^{(1-σ)253/500}.

**Lemma 4.3.** Let η2=1821/10^5, τ0=1/(5·10^5), D0=exp((log X)^{1/3}), γ=log_X N, and fix 0<ζ<τ0/100. Every
squarefree d∈Q182 with d≥X^{1/2-ζ} that is not exceptional (Π_{p|d,p≤D0} p ≤ exp((log X)^{2/3})) factors as d=qr, where
X^{γ-η2+2τ0} ≤ r < X^{γ-3τ0}, r contains every prime factor of d that is ≤D0, and q is X^δ-smooth with all prime factors >D0.

## Verdict

**Conditional on named inputs (no defect found).** Every internal step and every exponent inequality checks
out. Each cited input is used within its hypotheses, as far as those hypotheses can be checked from memory.
The named inputs are:
 (I1) the bilinear Bombieri–Vinogradov theorem (Polymath8a "Theorem 2.9"; Bombieri–Friedlander–Iwaniec/Motohashi);
 (I2) the Pólya–Vinogradov completion bound with Weil/Bombieri bounds for complete sums of
      e_{d1}(c1/n)e_{d2}(c2/(n+l)) with squarefree moduli (cited as Polymath8a "Corollary 4.16, second bound");
 (I3) the divisor bound in arithmetic progressions with τ(q)^{O(1)} loss, for q ≤ x^{1-ε} (Polymath8a "Lemma 1.3(iii)").
No local copy of Polymath8a (arXiv:1402.0811) was available and the internet was not used, so the exact theorem
numbers and statement wording are **from memory and unverified** (category e for the labels). The
mathematical content of I1–I3 is classical, and the paper's use of it is correct.

## Dependency graph

Prop 4.2
├─ small moduli d ≤ X^{1/2}(log X)^{-K_C}: I1 directly (all d, sup over a) ................ (b)
├─ exceptional moduli: ω(d) > (log X)^{1/3} ⇒ Markov + divisor moments + I3 + Cauchy–Schwarz ... (a)/(b: I3)
├─ Lemma 4.3 (combinatorial) ............................................................. (a)
├─ dyadic split q≍Q, r≍R, (28) ............................................................ (a) exact
├─ Δ = Δ1 + Δ2 (identity φ(qr)=φ(q)φ(r)) .................................................... (a)
├─ Δ2: SW of β·1_{(·,q)=1} uniformly in q (mass of (n,q)>1 is ≪ N D0^{-1} log^{O(1)}) ⇒ I1 mod r ...... (b)
└─ Δ1: average over b2 mod P(X) → linearise → Cauchy–Schwarz → S ≪ MN²R^{-1}(log X)^{-C}
   ├─ diagonal ℓ=0: I3 at modulus r[q1,q2] ≤ X^{0.59021}; ratio R/N ≤ X^{-3τ0} .......... (b: I3)
   ├─ h=0, q0=1: exact cancellation of the four correlations (same c_{q,r}, b-independent) ....... (a)
   ├─ h=0, q0>1: q0>D0; congruence count in (n,ℓ) .............................................. (a)
   └─ h≠0: (29) ⇐ Cauchy–Schwarz → (30) [I2] + (31) [elementary] → (32) → (33)–(35) [exact] ....... (b: I2)
Divisor weight τ(d)^v: I3 + Cauchy–Schwarz ................................................. (a)

## Obligation matrix

| # | Item | Status | Category |
|---|---|---|---|
| 1 | Statement typing: scales, ranges, SW on the shorter factor β, no smoothness, d ≤ X^{253/500} | passed | (a) |
| 2 | Lemma 4.3: G=∏f_i∏f'_i ≤ X^{2(1-σ)B}. f_i need not be prime or rough, which is harmless because all of G goes into r | passed | (a) |
| 3 | Lemma 4.3: adjoining primes ≤ D0 costs ≤ exp((log X)^{2/3}) = X^{o(1)} (nonexceptional) | passed | (a) |
| 4 | Lemma 4.3: start below target, 11/25−η2+2τ0−2B = 20997/500000 > 0 (exact) | passed | (a) |
| 5 | Lemma 4.3: overshoot, −η2+2τ0+δ = −3τ0 (exact), with strict "<" correct | passed | (a) |
| 6 | Lemma 4.3: target < log_X d, since γ−η2+2τ0 ≤ 1/2−η2+2τ0 < 1/2−ζ | passed | (a) |
| 7 | Lemma 4.3: q is X^δ-smooth with primes > D0 (q ⊂ ee', d squarefree). Edge cases m=m'=0 (G=1), γ=1/2, primes of size exactly X^δ all pass. Toy simulation: 708 cases, 0 failures | passed | (a) |
| 8 | Coverage: X^{1/2-ζ} < X^{1/2}(log X)^{-K_C}, so BV plus Lemma 4.3 cover every modulus | passed | (a) |
| 9 | Exceptional moduli: ω(d) > (log X)^{1/3} ⇒ count ≪_A D(log X)^{-A}. Pointwise |Δ| ≪ (X/D)τ(d)^{O(1)}log^{O(1)} needs I3 with d ≤ X^{0.506} ≤ X^{1-ε} | passed | (b) |
| 10 | (28): R≫X^{γ−η2}, R≪NX^{−τ0}, QR≪X^{253/500}, RQ²≪X^{59021/100000}, Q/N≪X^{−35579/100000} (exact at γ=11/25, monotone) | passed | (a) |
| 11 | C0 is supported on ≤ gcd(b1−b2,q0) classes, which is nonzero only if that gcd divides ℓ, so ≤ z | passed | (a) |
| 12 | Poisson/CRT: modulus rq0q1q2 (squarefree, pairwise coprime), phase Φ, H = c_H X^ζ RQ²/(q0M) ≥ X^ζ D/M, tail negligible | passed | (a) |
| 13 | First Cauchy–Schwarz factor ≤ X^{o(1)}Nz/q0 (uses q0≪Q≪N) | passed | (a) |
| 14 | (30) completion term: on a class mod q0 the q0-components are constant, the remaining modulus is ≤ R(Q/q0)^4, and the bound is d'^{1/2+o(1)}. Degenerate local factors (p | k, both coefficients ≡0) average out over k | passed (I2) | (b); citation label (e) |
| 15 | (30) mean term: at p|r only d1 carries p, Ramanujan sum gives p−1 or −1, product ≤ gcd(h1s1s2−h2q1q2, r). Other primes are bounded trivially by p, giving N·gcd/(q0 r) | passed | (a) |
| 16 | (31) determinant count, including the retained b=0 term | passed | (a) |
| 17 | (32): recomputed. The true q0-powers are q0^{-7}, q0^{-6}, q0^{-4} vs the paper's q0^{-4}, so discarding them is favourable | passed | (a) |
| 18 | (33) 1+12ω+7η2/2−5γ/2 ≤ −53/200000; (34) 8ω+3η2−γ ≤ −36137/100000; (35) 2γ−1−τ0 ≤ −1/500000. Exact, with monotonicity checked | passed | (a) |
| 19 | κ=τ0/4 and ζ<τ0/100: worst margins −207/781250 and −49/25000000, both < −τ0/2 | passed | (a) |
| 20 | Δ2: SW of β1_{(·,q)=1} uniform in q (not by direct appeal to Def 3.9, which would cost τ(q)^{K}, but by the D0-mass bound). BV in modulus r ≤ X^{1/2−3τ0}. Σ1/φ(q) ≪ log X | passed | (b) |
| 21 | Δ1: averaging b2 over units mod P(X) reproduces the 1/φ(q)-average, then Cauchy–Schwarz with (RM)^{1/2} | passed | (a) |
| 22 | Diagonal: X^{1+o(1)} vs MN²/R = XN/R ≥ X^{1+3τ0} | passed | (b: I3) |
| 23 | h=0, q0=1 cancellation: coefficients frozen, coprimality conditions independent of the unit residues | passed | (a) |
| 24 | h=0, q0>1: ≪ log^{O(1)}(MN + MN²/(RD0)) recomputed | passed | (a) |
| 25 | h≠0 total ≪ X^{−κ}MN²R^{−1}log² recomputed | passed | (a) |
| 26 | τ(d)^v weights via Cauchy–Schwarz | passed | (a) |
| 27 | Uniformity in a and in the coefficient families (Polymath8a convention: implied constants depend only on fixed data) | passed | (c) |
| 28 | Exact Polymath8a labels: Thm 2.9, Cor 4.16 ("second bound"), Prop 5.10, Lemma 1.3(ii)–(iii), Lemma 5.2, Cor 5.3, §§5.3–5.4 | not checkable offline | (e) |

## Decisive checks and commands

* `python3 exponents.py`: every numerical claim in §4.2 recomputed in exact rationals (Fraction/sympy). All PASS.
  Sensitivity: term (33) is the tightest. Its zero point is γ = 219947/500000 = 0.439894 against the endpoint
  0.44. Equivalently, the largest admissible QR exponent at γ=11/25 is 607253/1200000 ≈ 0.5060442, against 0.506. The
  margins are small but exact and positive. (33)–(34) are exactly Stadlmann's Lemma 3 conditions
  24ω+7δ−5γ<−2 and 8ω+3δ−γ<0 with δ→η2 (cross-checked against `notes/stadlmann-recheck-s5.md` in the project).
* `python3 completesums.py`: brute force over primes 3≤p<42 and all (c,c1,c2,l,k) of the local complete sums
  behind (30). The Ramanujan-sum identity holds exactly. The non-degenerate sums satisfy |S| ≤ 4√p (max ratio 3.245).
  This is a sanity check of I2's local input, not a proof.
* `python3 lemma43_sim.py`: toy log-scale simulation of the greedy construction of Lemma 4.3. 0 failures.

## Comments on cited results (from memory of Polymath8a; unverified wording)

* **Bilinear BV (I1).** As I recall it: α, β coefficient sequences at scales M, N ≫ x^ε (or similar), NM≍x, β SW.
  Then Σ_{q≤x^{1/2}log^{−B}x} sup_{a∈(Z/q)^×} |Δ(α*β;a(q))| ≪ x log^{−A}x. Hypotheses met: N ≥ X^{0.44} and M ≫ X^{1/2}.
  β is SW. Moduli r ≤ X^{1/2−3τ0}. sup over a gives uniformity in the CRT assignment. For Δ2 the sequences
  α1_{(·,q)=1}, β1_{(·,q)=1} are coefficient sequences with uniform constants. The paper proves SW for the second
  one correctly, uniformly in q.
* **Completion (I2).** The bound actually used in (30) is the √modulus completion bound plus a mean term. The
  q-van der Corput bound is not used. If Polymath8a's Cor 4.16 states its √q bound under a y-dense-divisibility
  hypothesis whose right-hand side is free of y, then "take y = the modulus" (every q is q-densely divisible) is
  right. If instead the corollary's *second* bound is the van der Corput one (N^{1/2}q^{1/6}y^{1/6}+…), the label
  "second bound" is wrong, but the bound used remains the classical one and the conclusion is unaffected. I could
  not determine the ordering from memory, so this is (e) for the label and (b) for the mathematics. Polynomial
  length: N/q0 ≤ X^{1/2} and modulus ≥ X^{0.42}.
* **Divisor bound in APs (I3).** It is used at moduli ≤ X^{0.59021} (diagonal) and ≤ X^{0.506} (pointwise |Δ|). Both are ≤ X^{1−ε}.
* **Dense divisibility.** It is never needed. Lemma 4.3 replaces Polymath8a's use of x^δ-dense divisibility in
  Type II (finding r ∈ [x^{−δ−ε}N, x^{−ε}N]) by an explicit greedy factor. This works because all rough factors
  (≤ X^{2B} = X^{0.3798}) fit below the target X^{γ−η2+2τ0} ≥ X^{0.4218}. That is the one D182-specific input, and it is verified.
  Smoothness of q (X^δ) is used only to ensure N/p ≥ X^{0.42} in the SW-restriction argument.

## Exposition gaps (category c)

* c1. The k≠0 completion terms with degenerate local factors (p|k and both phase coefficients ≡0 mod p) need the
  standard gcd-averaging over k. This is hidden inside the citation to Cor 4.16, and it is routine.
* c2. Uniformity of BV over the q-indexed family relies on Polymath8a's fixed-constants convention. It is stated
  but not spelled out.
* c3. "Lemma 5.2 and Corollary 5.3" of Polymath8a are cited for the exceptional-moduli bound. The elementary argument
  given in the text is self-contained regardless.
* c4. The relabelling N := min(N0, X^{1/2}) in Prop 4.11 (outside scope) changes the support constants by a fixed
  factor. Prop 4.2's proof tolerates this, since γ ≤ 1/2 + O(1/log X) only changes R/M by O(1).

## Demonstrated defects (category d)

None found in §4.2.

## Remaining obligations

1. Check the exact statements and numbering in Polymath8a (arXiv:1402.0811 / ANT 2014): Theorem 2.9 (BV hypotheses
   on N, M; sup over a), Corollary 4.16 (which bound is "second"; its hypotheses: squarefree moduli, dense
   divisibility parameter, length condition, shifts l1,l2 allowed), Proposition 5.10, Lemma 1.3(iii) (τ(q)^{O(1)}
   form and modulus range), and Lemma 5.2/Corollary 5.3.
2. Check [Sta26, Lemma 3] against its source text for the statement wording. Its conditions are already confirmed in the project notes.
3. Downstream (outside scope): the callers (Prop 4.11, Lemma 4.13) must supply SW for the *scale-N (shorter)*
   factor. Prop 4.11 states that both grouped factors are SW, which suffices.

## Strongest safe statement

Prop 4.2 holds as stated, given I1–I3 in their classical forms. No dense-divisibility hypothesis is needed, and the
numerical margins are positive in exact arithmetic.
