# Route card: the level-1/2 barrier for bounded multiplicative functions (Green; Granville–Shao) versus the twisted Type I input

- **Date:** 2026-11-23 (Session 47). Kind: bounded parity attempt (locate; literature + elementary arguments).
- **Classification: located.** The premise "general 1-bounded multiplicative f cannot be distributed beyond level 1/2" is
  not what the sources prove (Finding 0): both papers go BEYOND 1/2 for a fixed residue class, and their counterexamples
  limit the *saving* (about one log x over all moduli, about (log x)² over prime moduli), at every level, not the
  level. What the beyond-1/2 proofs use of f is exactly
  multiplicativity at primes in a range [Y, Z) plus |f| ≤ 1 (Finding 1); λ(n)λ(n+2) fails this at the first step, and
  the formal transfer (Proved here, Finding 2) bounds the twisted Type I sum at level Q by a two-point Liouville
  problem with well-factorable weights for the dilated forms (pm+2, p'm+2) at level ≍ Q²: this route does not help.
  The large-prime obstruction of Granville–Shao transfers to the two-point class n ↦ f(n)f(n+2) (Proved here,
  conditional on the same hypothesis (1.5) that Granville–Shao assume; Finding 3). Along the twin Selberg weights at
  level R = x^θ it moves the weighted sum by a CONSTANT fraction (≍ log R/log x) of the weighted mass (corrected in the
  audit; Finding 3b, conditional on the standard GPY-type asymptotics, not reopened), so no class-wide theorem gives the
  weighted f = 1 input; whether this bears on λ is Open. For the Λ-twisted inputs the construction defeats the class
  (not λ) at every level, even q = 1 (Proved here, elementary; Finding 4).
- No parity-breaking content. Nothing here bears on a lower bound for twin primes; at best it confirms and locates the
  obstruction's input. Possibly folklore throughout. Not in the paper (v1.0 frozen).

## Mechanism (new for this programme)

The beyond-x^{1/2} theorems for bounded multiplicative functions in progressions (Green 2016/18; Granville–Shao 2017/19)
and the limits they prove, compared with the input PM8b's obstruction needs: for f ∈ {1, Λ, α⋆β},
Σ_{n ≡ a (q)} f(n+h) λ(n)λ(n+2) negligible for q ≤ x^θ on average (paper §2, steps 2–4; subsec:typeI; oq:uniform).

## Question and criteria (fixed before the work)

(i) Do the constructions that stop general 1-bounded multiplicative f say anything about λ(n)λ(n+2)? (ii) Does
Granville–Shao's fixed-residue result beyond x^{1/2} apply to λ (one point), and to the two-point quantity?
- **Success (a):** the twisted Type I input beyond level 1/2 is blocked for every multiplicative-type model, so the two
  barriers coincide in a stated sense; **or (b):** a specific structural property of λ that the beyond-1/2 results use,
  with the exact first step where λ(n)λ(n+2) fails to have it.
- **No-go:** the beyond-1/2 results need multiplicativity in n of the distributed function and λ(n)λ(n+2) fails it in a
  way no known identity repairs: classify "located" and name the first unresolved implication.
- **Outcome:** (a) fails (there is no level-1/2 barrier in the sources to coincide with; the transferred obstruction is a
  saving obstruction at every level, and along the twin Selberg weights a constant-fraction obstruction for the class at
every fixed θ > 0, Finding 3b, which again is not tied to 1/2). (b) holds in the form: the property used is multiplicativity at primes p ∈ [Y, Z)
  (not complete multiplicativity, not ±1 values, not non-pretentiousness, which enter only the main terms); first failing
  step identified. The no-go criterion is met: located.

## Sources read (Literature; opened in full text)

| key | source | version | SHA-256 of PDF | where read |
|---|---|---|---|---|
| Gr | B. Green, *A note on multiplicative functions on progressions to large moduli*, arXiv:1604.04481 | v4, 23 Apr 2018 (v1 15 Apr 2016) | a0d643d0e88b34aaace726ef09fa1fde23d1a82666e4c50ba48fa4e640670aa9 | all 17 pp.: Thm 1.1 p. 1, Cor 1.2 and remarks p. 2, §2 Prop 2.2 pp. 5–9, §3 Prop 3.1 pp. 9–15, §4 p. 16 |
| GS | A. Granville, X. Shao, *Bombieri–Vinogradov for multiplicative functions, and beyond the x^{1/2}-barrier*, arXiv:1703.06865 | v2, 18 Apr 2019 (v1 20 Mar 2017) | 3a6b74c2a6d7156e9ea95cc6496683e3906e3fb9e9f441a9756c842339cb2579 | §1 pp. 1–9 (class C p. 3, Prop 1.3 p. 5, Prop 1.4 p. 6, §1.4 and Thm 1.8 pp. 7–8); §4 opening, Thm 4.2, Prop 4.3 and proof pp. 17–23; Lemma 4.5 statement p. 24; §7 opening and Prop 7.1 pp. 41–42; §7.1 p. 47; §8.1–8.3 pp. 47–50 |

Fetched with curl (arxiv.org abs pages for versions; PDFs from arxiv.org/pdf/<id>v<k>), read with `pdftotext -layout`,
kept in the session scratchpad (src/gs/), not committed. GS §§2–3, 5–6, the proof of Prop 7.1 and §§8.4–9 were skimmed or
not read. **Identifier note:** the identifier arXiv:1609.01224 suggested for Green's note is a different paper
(Nazaroglu, "r-Tuple error functions and indefinite theta series of higher-depth"; abs page title only); Green's note is
1604.04481 (found via the arXiv API by title). Literature check: three arXiv API title/abstract searches (23 Nov) for
two-point Chowla / Liouville correlations in progressions to large moduli returned nothing on that question (two
unrelated titles, not opened). Not exhaustive.

## What the sources say (Literature)

- **Gr Thm 1.1 (p. 1).** f multiplicative, |f| ≤ 1, X^{1/3} < Q < X^{1/2+1/78−σ}, 0 < |a| < 10Q: then
  |E_{n≤X, n≡a (q)} f(n) − E_{n≤X} f(n)| ≤ ε except for at most Q ε^{−1} X^{−cσε} primes q ∈ [Q, 2Q). **Cor 1.2 (p. 2):**
  the same for μ and for λ (with E f replaced by 0, via the prime number theorem). p. 2: the restriction to prime q is
  "quite important"; the theorem "is false without some such restriction, as may be seen by taking f(n) = (−1)^n μ²(n)"
  ("pretentious"), with "E_{n⩽X} f(n) is very small". [Flag (corrected in the audit): Green's remark is wrong for
  both readings. As printed (−1)^n μ²(n) has value −1 at n = 1, so it is not multiplicative; (−1)^{n+1} μ²(n) is
  multiplicative but its mean is 2/π², not small (mean of (−1)^n μ²(n) is −2/π²). Theorem 1.1 still fails for
  (−1)^{n+1} μ²(n) with even q: Computed (N = 4·10⁶, q = 2018, 20014) class means 0.81 ≈ 8/π² (a = 1) and −0.40 ≈ −4/π²
  (a = 2) against the global 0.2026 ≈ 2/π². The function (−1)^{n+1} without μ² has mean ≈ 0 and would fit the
  remark.] p. 3: "We do not know how to establish a corresponding result with a
  being allowed to vary with q, for any Q > X^{1/2}". **§4 (p. 16):** with a(q) varying, the analogue of the bilinear form
  (4.1) can be ≫ Q² (explicit choice a(q) = p on half the primes, p' on the other half, where the CRT solution is m = 1):
  "to make progress ... one would need a different mode of argument". This is a limit of the method, not a counterexample
  function. **Remark after Prop 2.2 (p. 5):** for the open problem Σ_{n≤X} μ(n)Λ(n−1) = o(X) "the bilinear estimate is
  certainly the heart of the matter", reducing to Hardy–Littlewood counts for px+1, p'x+1 for almost all p, p' ∼ X^δ.
- **Gr Prop 2.2 (p. 5), proof p. 6.** For ANY F : N → C and multiplicative |f| ≤ 1,
  E_{n≤X} f(n)F(n) ≪ E_triv + E_sieve + E_bilinear, with E_bilinear built from Σ_{m∈I, (m,pp')=1} F(pm) conj F(p'm) only.
  The one use of f: "Using the multiplicativity of f, Σ may be rewritten as Σ_p f(p) Σ_m w(m) f(m) F(pm)" (p. 6); then
  Cauchy–Schwarz with |f(m)w(m)| ≤ 1 removes f. **§3 (pp. 12–15):** for F the fixed-a progression weight, F(pm)F(p'm)
  becomes 1_{m ≡ r(q,q') (qq')} with r(q,q') given by CRT; Poisson summation, the reciprocity relation and the
  Bettin–Chandee bound for Kloosterman fractions give cancellation over (q, q'), which is what passes level 1/2.
- **GS class C (p. 3):** |Λ_f(n)| ≤ Λ(n), "includes ... all 1-bounded completely multiplicative functions".
  **Obstructions (p. 6):** "(i) If f correlates closely with a character of small conductor; or (ii) If the values of
  f(p) with x/2 < p ≤ x conspire against equi-distribution." **Prop 1.3 (p. 5):** for any 1-bounded multiplicative g and
  Q, x/Q → ∞, changing g on almost all primes of (x/2, x] to a constant σ gives Σ_{q∼Q} |Δ(f, x; q, 1)| ≫ x/log x.
  **Prop 1.4 (p. 6), §8.3 (pp. 49–50):** assuming (1.5) (π(x; q, a) = (π(x)/φ(q))(1 + O((log x)^{−A})) for q ≤ x^{1−ε}),
  for x^{2/5} < Q < x/2 a ±1 completely multiplicative f satisfying the A-Siegel–Walfisz criterion for all A has
  Σ_{q∼Q} |Δ(f, x; q, 1)| ≫ x/log x (f(p) = −1 iff p ∈ (x/2, x] and some prime ℓ ∈ (x^{1/3}, x^{2/5}] divides p − 1).
  So Cor 1.1 (saving (log x)^{1−ε} for Q ≤ x^{1/2−δ}) is best possible up to ε, at levels BELOW 1/2 as well.
  **Thm 1.8 (p. 8):** f ∈ C, 1 ≤ |a| ≪ Q ≤ x^{20/39−δ}: Σ_{q∼Q, (a,q)=1} |Δ_k(f, x; q, a)| ≪ x/(log x)^{1−ε}, and under
  the 1-Siegel–Walfisz criterion the same for Δ. p. 8: Green's result is "more-or-less best possible (up to the log log x
  factor)". **Prop 4.3 (p. 21, proof pp. 22–23):** Green's inequality with F arbitrary; f used only in the rewriting
  Σ' = Σ_m w(m) f(m) Σ_{Y≤p<Z} f(p) F(pm) (p. 22). **§7 (p. 41):** "We will be able to do this when the residue classes
  a_q do not vary with q"; Prop 7.1 (p. 42) is the bilinear bound for the fixed-a weight.

## Findings

**0. Correcting the premise (Literature).** Neither paper proves a level-1/2 barrier for bounded multiplicative
functions. Fixed a: level 20/39 (Gr: prime moduli, almost all q, precision ε; GS: all moduli after removing
small-conductor characters, saving (log x)^{1−ε}). Varying a(q): beyond 1/2 is open and the method provably cannot do it
in general (Gr §4), but no counterexample function is given. The proved counterexamples (Gr p. 2; GS Props 1.3–1.4, §8)
are pretentious-at-small-moduli or large-prime constructions; they bound the saving at every Q in their ranges,
including Q < x^{1/2}: by about log x over all moduli (GS Prop 1.4), and by about (log x)² over prime moduli, where
Green's bound x log log x/(log x)² is near-optimal (GS p. 7–8 and §8.2: ≫ x/(log x)² for prime q ∼ Q). So success criterion (a) has nothing to coincide with.

**1. What the beyond-1/2 step uses (Literature, our reading of Gr pp. 5–15, GS pp. 21–23, 41–42).** (α) f(pm) = f(p)f(m)
for primes p ∈ [Y, Z), p ∤ m; (β) |f| ≤ 1. After that, f is gone: all of the progression arithmetic, including the
Kloosterman step that crosses 1/2, is in F and is a lattice-point count. Complete multiplicativity, the values ±1 and
non-pretentiousness are not used there; pretentiousness enters only the main terms (characters ψ_j, Siegel–Walfisz,
class C for composite moduli). **For λ (one point; answer to (ii), first half):** λ ∈ C, since −F'/F for F = ζ(2s)/ζ(s)
has coefficient (−1)^k log p at p^k, i.e. Λ_λ = λΛ (Proved here, one line), and λ satisfies Siegel–Walfisz (classical;
not re-read here). Hence GS Thm 1.8 gives Σ_{q∼Q,(a,q)=1} |Δ(λ, x; q, a)| ≪ x/(log x)^{1−ε} for fixed a and
Q ≤ x^{20/39−δ}, and Gr Cor 1.2 gives precision ε for almost all prime q < x^{1/2+1/78−σ} (Literature). This one-point
statement is not an input of the twin obstruction: the weight 1 − λ(n)λ(n+2) expands into 1 and the two-point term only
(cf. Session 38). (Heuristic aside: one-point λ along the twin Selberg weights would need the classes n ≡ 0 (d₁),
n ≡ −2 (d₂), i.e. residue classes varying with the modulus, where Gr §4 says the method stops at 1/2.)

**2. The formal transfer and where it fails (Proved here; elementary).** Let F be the GS fixed-a weight (4.2)/§7 (or any
F). GS Prop 4.3 holds for arbitrary F, so apply it with f = λ and F̃(n) := λ(n+2)F(n) (|F̃| = |F|, so T and E_sieve are
unchanged):

  Σ_{Z⁹≤n≤x} λ(n)λ(n+2)F(n) ≪ T/(Y log Y) + E_sieve + max_{P∈[Y,Z)} ( P x E_{p,p'∼P} |B(p,p')| )^{1/2},

  B(p,p') = Σ_{m ≤ min(x/p, x/p')} λ(pm+2) λ(p'm+2) F(pm) F(p'm)

(GS's E_bilinear, p. 21, with P inside the square root). This is only an upper bound. Expanding F as in GS Lemma 4.5 /
Gr (3.12), F(pm)F(p'm) is a combination of indicators 1_{m ≡ r(q,q') ([q,q'])} (CRT; for composite moduli the modulus
is [q,q'] and the pair contributes only if the two congruences are compatible mod (q,q'); for prime q ≠ q' it is qq')
and mean terms, so B is a combination, with the factorable coefficients ξ_q ξ̄_{q'}, of two-point Liouville sums
Σ_{m≤M, m≡r ([q,q'])} λ(pm+2)λ(p'm+2) for the pair of forms (pm+2, p'm+2) (determinant 2(p'−p) ≠ 0), to moduli
[q,q'] ≤ 4Q². Regimes (P ≤ Z ≤ x^ε throughout):
- Q² ≤ x^{1−ε}/P: B is a two-point problem with well-factorable weights ξ_q ξ̄_{q'} at level ≍ Q², for new (dilated)
  forms. This is weaker than the absolute-value form of the twisted input at level Q², but it is still a level-Q² problem
  for the same kind of correlation; since Prop 4.3 only gives an upper bound, the conclusion is that this route does not
  help (not that the problems are equivalent). (With Q, Y, Z bounded it is Tao16 Thm 1.2 for (pm+2, p'm+2): consistent
  with paper Remark prop:tao-weight, no gain.)
- x^{1−ε}/P < Q² ≤ x: the progressions in m ≤ M = x/P have length O(x^ε) at most; intermediate, not examined separately
  (minor, since P ≤ x^ε).
- Q > x^{1/2}: each progression contains at most one m ≤ M, and B is Σ_{q≠q'} ξ_q ξ̄_{q'} λ(p r + 2) λ(p' r + 2) 1_{r ≤ M},
  r = r(q,q'). Green's Poisson step needs the summand to be a smooth cut-off times a progression indicator; the factor
  λ(pr+2)λ(p'r+2) makes it unavailable.
Writing λ(n)λ(n+2) = λ(n(n+2)) and running Ramaré's identity on N = n(n+2) gives the same terms (p | n gives
λ(m)λ(pm+2), with λ(pm+2) not split). The failing step is the first one, (α): for g(n) = λ(n)λ(n+2),
g(pm) = −λ(m) λ(pm+2) ≠ g(p)g(m), and the leftover λ(pm+2) survives Cauchy–Schwarz. The one known identity that handles
the two-point product, λ(pn)λ(pn+2p) = λ(n)λ(n+2) (the small-prime dilation behind Tao16, as quoted in paper
subsec:typeI; Tao16 not reopened here), changes the shift instead of factoring and gives only bounded level with
log-averaging. **First unresolved implication:** "E_{p,p'∼P} |B(p,p')| = o(x/P) for every P ∈ [Y,Z), for the fixed-a weight F
with arbitrary |ξ_q| ≤ 1 (for Q slightly above x^{1/2} this is cancellation over (q,q') in
Σ_{q≠q'∼Q} ξ_q ξ̄_{q'} λ(p r(q,q') + 2) λ(p' r(q,q') + 2) 1_{r(q,q') ≤ x/p'} plus mean terms)
⟹ Σ_{q∼Q} |Σ_{n≡a (q)} λ(n)λ(n+2) − (1/q_r)Σ_{n≡a (q_s)} λ(n)λ(n+2)| = o(x)": the implication holds by Prop 4.3 with
F̃ (E_sieve and T handled as in GS, with Y, Z chosen so that they are o(x)), and its hypothesis is not known (for Q < x^{1/2} the hypothesis is the
well-factorable-weighted two-point input for (pm+2, p'm+2) at level Q²). Note also that the fixed-a conclusion is not the
varying-class input the Selberg weights need. Not addressed by any source we read.

**3. The large-prime obstruction in the two-point class (Proved here, conditional on GS (1.5); elementary).** Let
x^{2/5+ε} < Q ≤ x^{1−ε}, I = (x^{1/3}, x^{2/5}], P = {p ∈ (x/2, x] prime : ℓ | p − 2 for some prime ℓ ∈ I}, f completely
multiplicative with f(p) = −1 for p ∈ P and f(p) = 1 otherwise, g(n) = f(n)f(n+2), and
Δ₂(q) = Σ_{n≤x, q|n} g(n) − (1/q) Σ_{n≤x} g(n) (the class n ≡ 0 (q) that Selberg weights for n(n+2) use). Then
Σ_{q∼Q, q odd} |Δ₂(q)| ≫ x/log x.
Proof. For n ≤ x+2, f(n) = −1 iff n ∈ P or n = 2p with p ∈ P ∩ (x/2, x/2+1] (a composite n ≤ x+2 has no prime factor
> x/2 except in that O(1) case). If q | n ≤ x and q ≤ 2Q < x/2 then n ∉ P, so up to O(1) terms g(n) = −1 iff n+2 ∈ P,
and Σ_{q|n} g(n) = ⌊x/q⌋ − 2A(q) + O(1), A(q) = #{p ∈ P : p ≡ 2 (q)}. The total is x − 4#P + O(x/log² x) (pairs p, p ± 2
both in P: Brun). Take q odd (for even q there is no odd prime p ≡ 2 (q), A(q) = 0 and Δ₂(q) ≈ +4#P/q > 0, so the
one-sided inequality below fails there; using |Δ₂| those q would only add to the sum). If some ℓ ∈ I divides q, every
prime p ∈ (x/2, x] with p ≡ 2 (q) is in P, so under (1.5) A(q) = (1+o(1))π*(x)/φ(q) (π* counts primes in (x/2, x]),
and #P ≤ Σ_{ℓ∈I} π*(x; ℓ, 2) = (c + o(1))π*(x), c = log(6/5) (as in GS §8.3). Hence for odd such q
Δ₂(q) ≤ −(2 − 4c − o(1)) π*(x)/φ(q) + O(x/(q log² x)), and 2 − 4 log(6/5) = 1.27… > 0. Each q ≤ 2Q < x has at most two
prime factors in I (three would exceed x), so Σ_{odd q∼Q, some ℓ∈I divides q} 1/φ(q) ≥ (1/2)Σ_{ℓ∈I} Σ_{odd q∼Q, ℓ|q} 1/q
≫ Σ_{ℓ∈I} 1/ℓ ≫ 1 (Q/ℓ ≥ x^ε → ∞), and the sum is ≫ x/log x. ∎
Scope. This f is 1-pretentious on [1, x] and has nothing to do with λ; it shows only that no theorem for the class
{f(n)f(n+2) : f ±1 completely multiplicative} can save more than about log x at any level in (x^{2/5}, x^{1−ε}),
including below 1/2.

**3b. Along the twin Selberg weights the effect is a constant fraction (corrected in the audit; Proved here,
conditional on the standard GPY/Maynard k = 2 asymptotics, not reopened this session).** [The draft said "relative
1/log x, harmless, neither blocks nor helps"; that compared with Σ w ≍ x/log R, which is wrong for these
dimension-2 weights. Retracted.] Let w_R(n) = (Σ_{d|n(n+2), d≤R} y_d)² be the GPY-type twin weights
(y_d = μ(d)P(log(R/d)/log R), P a fixed polynomial vanishing to order 2 at 0), R = x^θ, 0 < θ < 1/4 fixed. Then
Σ_{n≤x} w_R(n) ~ I x/(log R)² while on primes the sieve is one-dimensional, Σ_{x/2<p≤x} w_R(p) ~ J x/(2 log x log R)
and the same for w_R(p − 2) (I, J > 0 constants from P; the prime sums use Bombieri–Vinogradov at level R² ≤ x^{1/2−ε}).
Take the simplest member: f(p) = −1 for every prime p ∈ (x/2, x], f(p) = 1 otherwise, g(n) = f(n)f(n+2). Then
g(n) = −1 exactly when one of n, n+2 is a prime in (x/2, x] (up to Brun-negligible pairs and O(1) terms), so
Σ_n w_R(n)g(n) = Σ_n w_R(n) − 2Σ_{x/2<p≤x}(w_R(p) + w_R(p−2)) + small = (1 − κ_θ + o(1)) Σ_n w_R(n),
κ_θ = (2J/I)(log R/log x) = (2J/I)θ, a positive constant; whereas the mean of g is 1 − O(1/log x). So g is not
distributed along w_R like its mean, by a constant fraction of the weighted mass, at every fixed θ > 0 (not a level-1/2
phenomenon; no ℓ-condition is needed). Consequence (for the class): no theorem valid for all ±1 completely
multiplicative f gives the weighted f = 1 twisted input along w_R, at any fixed level x^θ. For λ: the same split shows
that the prime-supported part of Σ_n w_R(n)λ(n)λ(n+2) is −Σ_p w_R(p)λ(p+2) − Σ_p w_R(p−2)λ(p−2), of potential size a
constant fraction of the weighted mass, so the f = 1 input for λ is entangled with weighted λ along shifted primes
(Heuristic reading; not an implication, since cancellation between the parts is not excluded). Whether this blocks the
f = 1 input for λ is **Open**.

**4. The Λ-twisted inputs fail for multiplicative-type models at every level (Proved here; elementary).** Let g be any
±1 completely multiplicative function and σ ∈ {±1}. Define f completely multiplicative with f(p) = g(p) for p ≤ x/2,
for p > x, and for p ∈ (x/2, x] with p+2 prime; and f(p) = σ f(p+2) for primes p ∈ (x/2, x] with p+2 composite
(well defined: p+2 ≤ x+2 composite has all prime factors ≤ (x+2)/3 < x/2, where f = g). Then
Σ_{x/2<p≤x} f(p)f(p+2) = σ(π(x) − π(x/2)) + O(x/log² x). The terms p ≤ x/2 come from g and could cancel this in
Σ_{p≤x}; choosing σ = sign of Σ_{p≤x/2} g(p)g(p+2) (or 1 if it is 0) gives |Σ_{p≤x} f(p)f(p+2)| ≥ (1 − o(1))(π(x) −
π(x/2)) ≫ x/log x, and on the dyadic range (x/2, x] either sign can be prescribed. So the input
Σ Λ(n)f(n)f(n+2) = o(x) (PM8b (144) with f = Λ, already at q = 1) is false for members of the class (it is a
statement about the class, not about λ); any proof of it for λ must use λ(p) = −1
at the large primes, and then it is Σ_p λ(p+2) = o(π(x)): one-point λ along shifted primes, the open problem that Gr
p. 5 (for μ(n)Λ(n−1)) and Session 46 reduce to Hardy–Littlewood counts for dilation pairs. Not a level question.

## Answers

(i) The constructions (GS Props 1.3, 1.4; Gr p. 2) are about choosing f, not about λ. They transfer to the two-point
class (Findings 3, 3b, 4): along the twin Selberg weights at level x^θ they move the f = 1 twisted sum by a constant
fraction of the weighted mass (Finding 3b, conditional on standard GPY-type asymptotics), so no class-wide theorem gives
the weighted f = 1 input; whether this bears on λ is Open. For the Λ twist they defeat the class at every level, which
shows that input is a property of λ at large primes and not of the class. They are not level-1/2 phenomena. (ii) Yes for λ itself, fixed a (Finding 1); for λ(n)λ(n+2) the method applies formally but returns
the same problem at level Q² (Finding 2).

## Numerics

Only the audit check of Green's p. 2 example (Computed, pure-Python sieve to N = 4·10⁶, script code/parity/green_example_check.py,
output .out; committed by the coordinator): mean of (−1)^{n+1}μ²(n) 0.20264 (2/π² = 0.20264); class means mod 2018 and 20014:
0.812, 0.815 (a = 1), −0.405, −0.400 (a = 2). Nothing else needed computing.

## Not checked

The proofs of Gr Thm 1.1, GS Thm 1.8 and Prop 7.1 (Bettin–Chandee input) were not audited; GS §§2–3, 5–6, 8.4–9
not read; Ford's theorem (used by GS §8.1) and Tao16 not opened in this session. Finding 3 uses (1.5) as GS do; an
unconditional version (Brun–Titchmarsh constants) was not attempted, and Brun–Titchmarsh alone with these ranges does not
give 2 − 4c > 0 (crude check: c becomes 2 log(4/3) ≈ 0.58), and the lower bound for A(q) at q up to x^{1−ε} needs
(1.5) anyway. Finding 3b uses the GPY/Maynard k = 2 asymptotics (main terms and the prime sum via BV) without
reopening them, and the constants I, J were not computed. Whether Green's varying-residue difficulty (Gr §4,
Green–Ruzsa) has a two-point analogue that blocks rather than merely stops methods was not examined.

## Audit (Session 47)

Fresh-context adversarial audit (coordinator relay), applied in the same session.
- **(2) Slip, fixed.** The saving limit depends on the set of moduli: about log x over all moduli (GS Prop 1.4), about
  (log x)² over prime moduli (Green's x log log x/(log x)² is near-optimal, GS pp. 7–8, §8.2). Summary and Finding 0
  updated.
- **(3) Error, fixed.** The draft said (−1)^{n+1}μ²(n) "has the stated property". It does not: its mean is 2/π², not
  small. Green's remark is wrong for both versions; Theorem 1.1 still fails for (−1)^{n+1}μ²(n) with even q (computed
  class means), and (−1)^{n+1} without μ² has mean ≈ 0. Sources section rewritten.
- **(4) Error, fixed.** In the Finding 2 display, P belongs inside the square root: E_bilinear = max_P (P x E|B|)^{1/2}.
- **(5) Gap, fixed.** The intermediate regime x^{1−ε}/P < Q² ≤ x is now listed (not examined; minor since P ≤ x^ε).
  For composite moduli the CRT modulus is [q,q'] with a compatibility condition mod (q,q'). "B is the twisted Type I
  problem itself" was an overclaim: B carries factorable weights ξ_q ξ̄_{q'}, so it is now called a well-factorable-weighted
  two-point problem at level Q². Since Prop 4.3 is only an upper bound, "circular" now reads "this route does not help".
  The first unresolved step is now stated as an implication.
- **(7) Gaps in the Finding 3 proof, fixed.** (a) n = 2p ≤ x+2 with p ∈ (x/2, x/2+1] makes "exactly" off by O(1):
  now O(1). (b) For even q, A(q) = 0 and Δ₂(q) > 0, so the one-sided bound fails: now restricted to odd q (with |Δ₂|
  even q only add). (c) The sum over ℓ uses that each q < x has at most two prime factors in I: now stated.
- **(8) Error, retracted and replaced.** "Relative 1/log x / harmless / neither blocks nor helps" was wrong: for the
  dimension-2 twin weights Σ w_R ≍ x/log² R while Σ_p w_R(p) ≍ x/(log x log R), ratio ≍ log R/log x, a constant at
  R = x^θ. Replaced in the summary, Finding 3 (new 3b) and Answers (i). The class-wide question was settled here,
  conditional on the standard GPY-type asymptotics: a member of the class misses the weighted f = 1 input by a constant
  fraction at every fixed θ > 0 (Finding 3b). Whether this bears on λ is Open.
- **(9) Slip, fixed.** In Finding 4 the p ≤ x/2 terms (from g) can cancel σ(π(x) − π(x/2)). Now σ is chosen against
  them, or either sign is prescribed on the dyadic range (x/2, x].
- **(11) Classification.** "Located" stands. "Harmless for the obstruction" withdrawn. "Fatal at every level" now
  reads "defeats the class (not λ) at every level".
