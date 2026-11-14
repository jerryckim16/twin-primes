# Asymptotic sieve Type II hypothesis for twin primes

- **Date:** 2026-11-14
- **Kind:** attempt (source-dependent implication and obstruction location)
- **Target:** Can the Friedlander–Iwaniec asymptotic sieve, which breaks parity given a Type I hypothesis (R) and a bilinear hypothesis (B), be applied to a_n = Λ(n+2)? If not, which estimate is missing, and what is it equivalent to or at least as hard as?
- **Hypotheses and types:**
  - The sequence is a_n = Λ(n+2) ≥ 0 for n ≤ x. It is not supported on squarefree n, so FI98 Theorem 2 (§9) applies, not Theorem 1.
  - The density is g(p^j) = 1/φ(p^j) for odd p and g(2^j) = 0, with A(x) ~ x.
  - FI's (B) is Σ_m |Σ_{N<n≤2N, mn≤x} γ(n,C)μ(mn)a_{mn}| ≤ A(x)(log x)^{−2^{22}}, for every N with Δ⁻¹√D < N < δ⁻¹√x and every 1 ≤ C ≤ x/D, where γ(n,C) = Σ_{d|n, d≤C} μ(d).
  - (B) has no Siegel–Walfisz hypothesis and no general β. The inner weight is Möbius-specific.
- **Active conventions:** FI98 notation (journal pagination); λ is the Liouville function.
- **Current dependency/evidence status:** The twin prime conjecture is open. This attempt claims no progress toward it.
- **Nearest prior attempt and first failure:** None in this project; this is the first record under `notes/parity-attempts/`. In the literature: FI98 p. 1046, and PM8b §8 pp. 70–71.
- **Route:**
  1. Extract FI98's hypotheses exactly.
  2. Specialise them to a_n = Λ(n+2) and check each one.
  3. Analyse (B) by rewriting it with λ, specialising α_m ≡ 1, and applying Cauchy–Schwarz in m with a parity test of the resulting correlation sum.
- **Mechanism and distinctness from prior routes:** The project's other work uses Maynard–Tao sieves, which only use linear (Type I / GEH) inputs and stop at H₁ ≤ 6 (PM8b §8). This route uses the one known sieve framework with a bilinear axiom.
- **Changed input, if reopening a failed route:** N/A
- **Success criterion:** Name an unconditional source, or a proof, for both (R₃) at level D > x^{2/3} and (B) for Λ(n+2). This is presumed impossible with current knowledge, because it would prove the twin prime conjecture.
- **Failure/no-go criterion:** The missing estimate is pinned to a precise inequality, and that inequality is shown to be parity-sensitive or documented as open.
- **Cheapest decisive check:** Read FI98 p. 1046 and PM8b §8. Then compute (B) for the parity-twisted sequence Λ(n+2)(1+λ(n))/2.
- **Attempt outcome:** Conditional implication, with the gap located.
  - FI98 Theorem 2, applied with the checked density data, gives Σ_{p≤x} Λ(p+2) log p ~ 2C₂x (the Hardy–Littlewood twin-prime asymptotic), **conditional on** two inputs that are not known:
    - (R₃): fixed-residue Elliott–Halberstam with absolute values at level x^{2/3+}. Bombieri–Vinogradov gives only level x^{1/2}.
    - (B-twin): Σ_m |Σ_{N<n≤2N, mn≤x} γ(n,C)μ(mn)Λ(mn+2)| ≤ x(log x)^{−2^{22}} for x^{1/3+} < N < x^{1/2}(log x)^{−α} and 1 ≤ C ≤ x/D.
  - Proved here:
    - (i) With C = 1, (B-twin) is exactly a bilinear sum of λ(k)Λ(k+2), because μ = λ on squarefree numbers.
    - (ii) For a⁺ = Λ(·+2)(1+λ)/2, every term μ(mn)a⁺_{mn} is ≥ 0, so (B) has no cancellation at all.
    - (iii) Taking α ≡ 1, (B-twin) implies a divisor-weighted Möbius-at-shifted-primes bound, |Σ_k μ(k)Λ(k+2)c_N(k)| ≪ x(log x)^{−2^{22}}. The unweighted fixed-shift version is a folklore open conjecture (Li21).
    - (iv) After Cauchy–Schwarz in m, the diagonal is harmless. The missing piece is the off-diagonal correlation bound (OD): Σ_{n₁≠n₂} β_{n₁}β_{n₂} Σ_m μ²(m)Λ(mn₁+2)Λ(mn₂+2) ≪ Nx(log x)^{−2^{23}}, with β_n = γ(n,C)μ(n). For a⁺, this sum has only non-negative terms. So Cauchy–Schwarz moves the parity problem into (OD) but does not remove it.
- **Route disposition and scope:** Closed as blocked within this scope. The located estimate (B-twin) is stated as unproved and unprovable by known methods by the theorem's own authors: FI98 p. 1046, "no idea how to prove that the relevant sequence satifies the condition (B)". PM8b pp. 70–71 says the same of bilinear Λ(dm+2) sums: "we do not know of any plausible way to control such bilinear expressions". I propose no new input.
- **Continuations:**
  - Untried: check *Opera de Cribro* (2010), which is paywalled and was not opened, for a weaker form of (B), for example a different N-range or an integrated form like (∫B) on p. 1063.
  - Untried: survey results after 2014 on absolute-value, fixed-residue Bombieri–Vinogradov beyond x^{1/2}. This decides whether (R₃) is a second, independent barrier. FI98 p. 1046 (1998) says "Even proving (R) to such a high level is currently beyond reach".
  - Untried: the literature on Hardy–Littlewood for pairs of linear forms (n₁m+2, n₂m+2) averaged over coefficients n₁, n₂ ~ N with N² ≤ x. No source was opened. Under (iv), such averages cannot give (OD) without parity-sensitive input; a check would only confirm this.
  - Obstructed: proving (B-twin) from GEH or any linear axioms, by (ii) and the PM8b §8 parity heuristic.
- **Evidence label:** conditional (the implication (R₃)+(B-twin) ⇒ twin-prime asymptotic follows from FI98 Thm 2 with the verified density data). Items (i), (ii), (iii) and the Cauchy–Schwarz reduction in (iv) are proved here. The numerics are heuristic.
- **Review and freshness status:** self-reviewed; current as of 2026-11-14; not independently audited.
- **First unresolved or failed implication:** (B-twin), equivalently the off-diagonal bound (OD). Each needs cancellation of λ(k) on k ∈ (primes − 2) along multiplicative structure. (R₃) at level > x^{2/3} is a second unproved input.
- **Strongest surviving statement:** If (R₃) holds with D > x^{2/3} and (B-twin) holds in FI's range, then Σ_{p≤x} Λ(p+2) log p = 2C₂x(1 + O(log δ/log Δ)). Separately, (B-twin) at C = 1 implies the divisor-weighted shifted-prime Möbius cancellation (iii), and it fails identically for the parity-twisted sequence (ii).
- **Artifacts and commands:**
  - Details, quotations and locators: [2026-11-14-asymptotic-sieve-type-ii-details.md](2026-11-14-asymptotic-sieve-type-ii-details.md).
  - Sources were fetched with curl from arXiv (math/9811186v1, 1407.4897v4, 2009.08969v2) and the Tao 2007 blog post. pdftotext was used, and the exponents were checked against rendered page images.
  - Numerics: `python3 -I bilinear_B.py 2000000` (scratchpad; condensed copy in the details file), x = 2·10⁶, 4.1 s, seed 20261114.
- **Next unresolved question:** Is there any sequence closely tied to twin primes, for example restricting n by a norm form or adding a second variable, for which an FI-type (B) is provable? For a single linear shift n ↦ n+2, (OD) needs λ-cancellation on shifted primes, which no known method supplies.
- **Uniform route or obstruction, when evidence is bounded:** The uniform obstruction is (ii): Λ(n+2) and Λ(n+2)(1+λ(n))/2 are heuristically indistinguishable to Type I axioms (PM8b §8), but (B) separates them. So (B) itself carries the parity information.
- **What another bounded case would discriminate, if applicable:** Larger-x numerics cannot reach the (log x)^{−2^{22}} saving and would discriminate nothing new.
