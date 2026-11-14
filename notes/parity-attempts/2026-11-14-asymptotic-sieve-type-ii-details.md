# Asymptotic sieve, Type II hypothesis (B), and twin primes: sources and derivation

Companion to the route card
[2026-11-14-asymptotic-sieve-type-ii-for-twin-primes.md](2026-11-14-asymptotic-sieve-type-ii-for-twin-primes.md).
Checked 2026-11-14. The twin prime conjecture is open. Nothing here proves it or
moves toward it; the aim is to find exactly where this route stops.

## 1. Sources actually opened

| ID | Source | Version / locator | SHA-256 of the file read | What was checked |
|---|---|---|---|---|
| FI98 | J. Friedlander, H. Iwaniec, "Asymptotic sieve for primes", Ann. of Math. 148 (1998) 1041–1065 | arXiv:math/9811186v1 (1 Nov 1998), whose header says it is the Annals version with journal page numbers. https://arxiv.org/pdf/math/9811186 | `d39f5249…953d1f` | (1.1)–(1.17), Theorem 1, §2 remarks, §9 Theorem 2, §10 Theorem 3. The exponents in (R), (B), (R₃) and (B*) were read from rendered page images (pp. 1043, 1059, 1063), not from the text extraction. |
| PM8b | D.H.J. Polymath, "Variants of the Selberg sieve, and bounded intervals containing many primes" | arXiv:1407.4897v4 (22 Dec 2014), 80 pp. | `4085a675…4086a7` | Claim 2.2 (EH[ϑ]), Theorem 2.3 (BV), Claim 2.6 (GEH[ϑ]), §8 "The parity problem" (pp. 68–71 of 80) |
| Tao07 | T. Tao, "Open question: the parity problem in sieve theory", blog post | https://terrytao.wordpress.com/2007/06/05/open-question-the-parity-problem-in-sieve-theory/ (fetched HTML, post body only) | `3ade5d1f…8c6567` | statement of the parity problem; paragraph on Friedlander–Iwaniec |
| Li21 | J.D. Lichtman, "Averages of the Möbius function on shifted primes" | arXiv:2009.08969v2 (20 Oct 2021) | `7f7421c3…a4456` | abstract and §1 (the folklore conjecture; Theorem 1.1 holds only on average over shifts) |

The project has no literature cache: there is no `/.research-cache/` rule in
`.gitignore`, and I was not authorised to create one. So no PDF was retained;
only the hashes above are recorded.

**Sources not opened:**
- E. Bombieri, "The asymptotic sieve" (1976). Not attempted. I know of no open copy, and I did not try to get around a paywall.
- Friedlander–Iwaniec, *Opera de Cribro* (AMS Colloquium Publ. 57, 2010). Not attempted, because it is paywalled. The book's form of the asymptotic sieve (its chapter on the asymptotic sieve) is **not** checked here.
- The Granville and Iwaniec surveys. Not attempted because of the time bound.
- Brun–Titchmarsh and Bombieri–Vinogradov in their original sources. I did not open these. BV is used only in the form PM8b Theorem 2.3 states it, and Brun–Titchmarsh is used as a standard upper bound. Both are marked *standard, not re-verified* below.

## 2. Exact hypotheses and conclusion (FI98)

Short quotations, with locators in FI98 journal pagination. The notation is FI's.

- Setup, p. 1041: A = (a_n), a_n ≥ 0, S(x) = Σ_{n≤x} a_n Λ(n) (1.2), A(x) = Σ_{n≤x} a_n (1.3), and
  (1.4) "A(x) ≫ A(√x)(log x)²".
- p. 1042: A_d(x) = Σ_{n≤x, n≡0 (d)} a_n (1.5).
  (1.6) "A_d(x) ≪ d⁻¹τ(d)⁸A(x) uniformly in d ⩽ x^{1/3}".
  (1.7) A_d(x) = g(d)A(x) + r_d(x), where g is multiplicative.
  (1.8) "0 ⩽ g(p) < 1, g(p) ≪ p⁻¹".
  (1.9) Σ_{p≤y} g(p) = log log y + c + O((log y)⁻¹⁰).
- p. 1043, Type I:
  "(R) Σ_{d⩽D} μ²(d)|r_d(t)| ⩽ A(x)(log x)^{−2^{22}} for all t ⩽ x with some D = D(x) such that (R1) x^{2/3} < D(x) < x."
- p. 1043, bilinear, verbatim up to typesetting:
  "(B) Σ_m | Σ_{N<n⩽2N, mn⩽x} γ(n)μ(mn)a_{mn} | ⩽ A(x)(log x)^{−2^{22}} for every N with (B1) Δ⁻¹√D < N < δ⁻¹√x for some δ = δ(x) ⩾ 2 and Δ = Δ(x) ⩾ 2, and where the coefficients are given by (B2) γ(n) = γ(n,C) = Σ_{d|n, d⩽C} μ(d)."
  p. 1044: "This is required for every C with (B3) 1 ⩽ C ⩽ xD⁻¹."
- p. 1044: (1.16) "a_n = 0 if μ(n) = 0".
  **Theorem 1:** "Assuming the above hypotheses, we have (1.17) Σ_{p⩽x} a_p log p = HA(x){1 + O(log δ(x)/log Δ(x))}", where H = Π_p (1−g(p))(1−1/p)⁻¹ (1.14).
- p. 1059, §9, Theorem 2 drops (1.16). It uses (9.1) "0 ⩽ g(p²) ⩽ g(p), g(p²) ≪ p⁻²" and (9.2) "Σ_{n⩽x} a_n² ⩽ x^{−2/3}A(x)²". In place of (R) it uses
  "(R₃) Σ³_{d<DL²} |r_d(t)| ⩽ A(x)L⁻² where L = (log x)^{2^{24}}", where Σ³ means a sum over cubefree d.
  "Theorem 2. Assume the following hypotheses: (1.4), (1.6), (1.8), (1.9), (B), (B1), (B2), (B3), (9.1), (9.2), (R₃) and (R1). Then (1.17) holds true for A = (a_n)."
- p. 1063, §10, Theorem 3: in Theorem 2, (B) may be replaced by (B*). In (B*), the inner sum runs only over n with no prime factor p < P, where 2 ⩽ P ⩽ Δ^{1/(2^{35} log log x)}, and the bound is A(x)(log x)^{−2^{26}}.

**What (B) does *not* contain.** (B) has no general α_m ⊗ β_n and no Siegel–Walfisz hypothesis. The inner coefficient is the specific Möbius-type weight γ(n,C)μ(mn), and the absolute value is taken outside the inner sum. That is the same as allowing arbitrary bounded α_m. FI say (p. 1045): "the source of cancellation in the bilinear form in (B) comes from the sign changes of the Möbius function μ(mn) in the inner sum". The Siegel–Walfisz-type β condition the task asked about belongs to GEH (PM8b Claim 2.6, (7)), not to FI's (B).

**Sharpness remarks by FI (p. 1045):**
- "our stipulation of the lower bound restriction N > Δ⁻¹√D in (B1) is essential; indeed by narrowing this slightly to N > √D we would not be able to break the parity problem."
- "our hypothesis (B) can be realistic only if D is somewhat larger than x^{2/3+ε}."
- Selberg's sequence a_n = ½(1+λ(n)) "satisfies (R) with D = x^{1−ε} but fails to satisfy (B)."

**FI on twin primes (p. 1046), verbatim:** "we certainly expect that the sieve given here is quite capable of settling, for instance, the twin prime problem. The stumbling block is that in this case we have no idea how to prove that the relevant sequence satifies the condition (B). Even proving (R) to such a high level is currently beyond reach." ("satifies" is the source's typo.)

## 3. Specialisation to a_n = Λ(n+2)

Take a_n = Λ(n+2). Then S(x) = Σ_{n≤x} Λ(n)Λ(n+2), and (1.17) reads Σ_{p≤x} Λ(p+2) log p.

**Type I data.** For odd d, the residue 2 is coprime to d, so A_d(t) = ψ(t+2; d, 2) + O(log² x). For even d, Λ(n+2) ≠ 0 with n even forces n+2 = 2^j, so A_d(t) = O(log² x). Hence:
- g(2^j) = 0 and g(p^j) = 1/φ(p^j) for odd p.
- (1.8) holds, since g(2) = 0 and g(3) = ½ < 1.
- (1.9) holds by Mertens and the prime number theorem.
- (9.1) holds, since g(p²) = 1/(p(p−1)).
- (1.4) holds, since A(x) ~ x.
- (9.2) holds, since Σ a_n² ~ x log x ≤ x^{4/3}.
- (1.6) follows from Brun–Titchmarsh, since d/φ(d) ≤ 2^{ω(d)} ≤ τ(d). Brun–Titchmarsh is standard and was not re-verified here.

The squarefree support condition (1.16) fails for this sequence. So we use Theorem 2, which does not need it.

**Main term.** H = Π_p (1−g(p))(1−1/p)⁻¹ = 2·Π_{p≥3} p(p−2)/(p−1)² = 2C₂. So (1.17) would give Σ_{p≤x} Λ(p+2) log p = 2C₂·x·(1 + O(log δ/log Δ)). This is exactly the Hardy–Littlewood twin-prime asymptotic. The theorem therefore has the right shape, and **(R₃)+(B) for this sequence would imply the twin prime conjecture**. This is a direct reading of FI Theorem 2 with g as above. The verification of (1.4)–(1.9), (9.1) and (9.2) is mine; I label it *proved here, modulo Brun–Titchmarsh*.

**Required Type I, (R₃).** For all t ≤ x:
  Σ_{d<DL², d odd, cubefree} |ψ(t+2; d, 2) − ψ(t+2)/φ(d)| ≪ x(log x)^{−2^{25}}, with D > x^{2/3}.
This is a fixed-residue Elliott–Halberstam bound at level x^{2/3+}, with absolute values. PM8b p. 6, Claim 2.2 defines EH[ϑ] as Σ_{q≤Q} sup_a |Δ(Λ1_{[x,2x]}; a (q))| ≪ x log^{−A}x for Q ⪅ x^ϑ. PM8b Theorem 2.3 says: "The following classical result of Bombieri and Vinogradov remains the best partial result of the form EH[ϑ]: … EH[ϑ] holds for every fixed 0 < ϑ < 1/2." So BV gives (R₃) only for D = x^{1/2−ε}, and (R1) fails: it needs D > x^{2/3}. The Type I hypothesis is **not known**. Its gap is the exponent jump from 1/2 to 2/3. I did not check post-2014 progress for absolute-value, fixed-residue sums; that is a continuation.

**Required Type II, (B) specialised.** For every N with Δ⁻¹√D < N < δ⁻¹√x and every 1 ≤ C ≤ x/D:

  (B-twin)  Σ_{m} | Σ_{N<n≤2N, mn≤x} γ(n,C) μ(mn) Λ(mn+2) | ≤ A(x)(log x)^{−2^{22}},  where A(x) = Σ_{n≤x} Λ(n+2) ~ x.

Here μ(mn) ≠ 0 forces (m,n) = 1 and m, n squarefree. With D = x^{2/3+} and Δ = x^η, the range is N ∈ (x^{1/3+η'}, x^{1/2}(log x)^{−α}), so m ∈ (x^{1/2}, x^{2/3}). This is the Type II range.

## 4. Analysis of (B-twin) (proved here unless labelled)

**(a) Exact parity reformulation (proved).** For squarefree k, μ(k) = λ(k). So, with C = 1 (γ ≡ 1),
  Σ_m |Σ_n μ(mn)Λ(mn+2)| = Σ_m |Σ_n μ²(mn) λ(mn) Λ(mn+2)|.
So (B-twin) at C = 1 is a bilinear Chowla-type estimate for the function k ↦ λ(k)Λ(k+2).

**(b) The parity twin sequence fails (B) identically (proved).** Let a⁺_k = Λ(k+2)(1+λ(k))/2. For squarefree k, μ(k)a⁺_k = Λ(k+2)·1_{μ(k)=+1} ≥ 0. So with C = 1 the (B) sum for a⁺ equals its trivial bound Σ_{mn≤x, n~N} μ²(mn)a⁺_{mn}: there is no cancellation at all.

PM8b's parity heuristic (§8, p. 70) is that "all the bounds that are believed to hold for (142), (143) should also hold … for (144), (145)". These are the linear, Type I-type discrepancies, so the heuristic predicts a⁺ satisfies the same Type I axioms as 2a⁺ ≈ Λ(·+2). The size of the trivial bound for a⁺ (≍ x) is also heuristic: it needs a positive proportion of primes q with λ(q−2) = +1 and with q−2 having a divisor in (N, 2N]. I did not prove that.

**(c) Specialisation α ≡ 1 (proved).** From Σ_m|S_m| ≥ |Σ_m S_m|, (B-twin) at C = 1 implies
  | Σ_{k≤x} μ(k) Λ(k+2) c_N(k) | ≤ A(x)(log x)^{−2^{22}},  where c_N(k) = #{n | k : N < n ≤ 2N}.
Up to prime powers, this is Σ_{q prime} μ(q−2) c_N(q−2) log q: a divisor-weighted form of Möbius at shifted primes. Li21 abstract: "It is a folklore conjecture that the Möbius function exhibits cancellation on shifted primes; that is, Σ_{p⩽X} μ(p+h) = o(π(X)) as X → ∞ for any fixed shift h > 0." Li21 proves it only "on average for shifts h ⩽ H, provided log H/log log X → ∞" (Theorem 1.1).

This does **not** show that (B-twin) implies the unweighted conjecture, because c_N is not constant. Nor is any equivalence claimed. The status of the weighted fixed-shift sum is: no unconditional result was found in the sources opened.

**(d) Cauchy–Schwarz in m.** Write β_n = γ(n,C)μ(n) with |β_n| ≤ τ(n), and S_m = μ(m)Σ_{n~N, (n,m)=1, mn≤x} β_n Λ(mn+2). Then

  (Σ_m |S_m|)² ≤ (x/N) · Σ_{n₁,n₂~N} β_{n₁}β_{n₂} Σ_{m ≤ x/max(n₁,n₂), (m,n₁n₂)=1} μ²(m) Λ(mn₁+2) Λ(mn₂+2).

- **Diagonal n₁ = n₂.** Brun–Titchmarsh gives Σ_{m≤x/n}Λ(mn+2)² ≪ (x/φ(n))log x. So the diagonal is ≪ x(log x)^{O(1)}, and its contribution (x/N)·x(log x)^{O(1)} is acceptable once N ≥ (log x)^{2^{23}+O(1)}. That holds throughout (B1).
- **Off-diagonal.** What is missing is
  (OD)  | Σ_{n₁≠n₂~N} β_{n₁}β_{n₂} Σ_m μ²(m)Λ(mn₁+2)Λ(mn₂+2) | ≤ N·x·(log x)^{−2^{23}}.
  For each fixed pair, the inner sum counts prime pairs on the two linear forms n₁m+2 and n₂m+2. These satisfy n₂(n₁m+2) − n₁(n₂m+2) = 2(n₂−n₁), so each pair is a binary "twin-type" problem. The trivial size of (OD) is ≍ N·x. The only available source of cancellation is the Möbius weights β_{n₁}β_{n₂}.
- **Parity at the correlation level (proved).** Repeat (d) with a⁺ in place of Λ(·+2) and C = 1. For squarefree mn_i, λ(mn_i) = μ(m)μ(n_i), so a⁺(mn_i) ≠ 0 forces μ(n_i) = μ(m). Then β_{n₁}β_{n₂} = μ(n₁)μ(n₂) = 1 on every non-zero term: (OD) is a sum of non-negative terms. So any proof of (OD) for Λ(·+2) must use information that separates Λ(k+2) from Λ(k+2)(1±λ(k))/2 along pairs (mn₁, mn₂). In other words, it needs a parity-sensitive binary correlation of λ restricted to shifted primes. Cauchy–Schwarz moves the parity problem into the correlation sum; it does not remove it.

**(e) What the literature says about (B)-type estimates for twins.**
- FI98, p. 1046 (quoted in §2): "no idea how to prove that the relevant sequence satifies the condition (B)."
- PM8b §8, pp. 70–71, verbatim: "if one were able to obtain non-trivial bounds for "bilinear" expressions such as Σ_{x≤n≤2x} f(n)Λ(n+2) = ΣΣ_{d,m} α(d)β(m)1_{[x,2x]}(dm)Λ(dm+2) for functions f = α ⋆ β of the form in Claim 2.6, then (by a modification of the proof of Proposition 2.7) one would very likely obtain non-trivial bounds on Σ Λ(n)Λ(n+2) which would soon lead to a proof of the twin prime conjecture. Unfortunately, we do not know of any plausible way to control such bilinear expressions. (Note however that there are some other situations in which bilinear sieve axioms may be established, for instance in the argument of Friedlander and Iwaniec [21] establishing an infinitude of primes of the form a² + b⁴.)"
- PM8b §8, p. 69: the parity argument shows "sieve-theoretic methods … from obtaining any bound on H₁ that is stronger than H₁ ≤ 6, even on the assumption of … GEH[ϑ]", and "The same arguments of course also prohibit a sieve-theoretic proof of the twin prime conjecture … the simpler weight ω(n) = 1 − λ(n)λ(n+2) … essentially due to Selberg".
- Tao07, paragraph "Despite this parity problem…": Friedlander–Iwaniec's argument has "a (non-smooth) error term which has the form of a bilinear sum, which captures correlation with the Liouville function. The main difficulty is to control this bilinear error term", which for a²+b⁴ "reduces to understanding some correlations between the Möbius function and the Jacobi symbol". Also: "These methods all seem to require that the form be representable as a norm over some number field". Twin primes n(n+2) have no such norm structure. That last point is a heuristic comparison only.

**Consequence for the route (source-backed).** (B-twin) is the very estimate FI98 (1998) and PM8b (2014) identify as the stumbling block. Under the parity heuristic of PM8b §8, (B-twin) cannot follow from any family of linear (Type I / GEH-type) equidistribution axioms. GEH alone is not enough either: PM8b shows that sieve methods under GEH stop at H₁ ≤ 6.

## 5. Heuristic numerical illustration

**Label: Heuristic.** This proves nothing about (B). The required saving (log x)^{−2^{22}} cannot be observed at any computable x.

A condensed copy of the script is below: the same computation, with the docstring, timing lines and output formatting removed. The original (SHA-256 `03b628d0…9cbd9cc`) was run from the scratchpad with Python 3.13.18 and numpy 2.5.3, took 4.1 s, and used seed 20261114 for the random-sign baseline. It computes B(N) = Σ_m|Σ_{N<n≤2N, mn≤x} μ(mn)a_{mn}| (C = 1) and T(N), the same sum with absolute values inside. Output at x = 2·10⁶:

```
       N      seq      B/T   rand/T   B/A(x)
      77     twin   0.3988   0.4146   0.0862
     160     twin   0.2701   0.2904   0.0613
     331     twin   0.1933   0.2089   0.0423
     684     twin   0.1308   0.1384   0.0294
    1223     twin   0.0954   0.1087   0.0213
 (all N)  selberg   1.0000                      (exact identity, §4(b) analogue)
 (all N)  twinpar   1.0000                      (exact identity, §4(b))
```

Here twin means a = Λ(·+2), selberg means a = (1+λ)/2, and twinpar means a = Λ(·+2)(1+λ)/2. rand/T uses random signs with the same magnitudes. At this tiny x, the twin sequence's inner sums cancel at the random-sign rate. The parity-twisted sequences show no cancellation, and that is an algebraic identity, not a numerical finding. The only thing this discriminates is that no small-x parity bias is visible in the inner sums. It says nothing at the scale the theorem needs.

```python
import numpy as np, sys, time
x = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
M = x + 3
spf = np.zeros(M, dtype=np.int64)
for p in range(2, int(M**0.5) + 1):
    if spf[p] == 0:
        idx = np.arange(p*p, M, p); sel = spf[idx] == 0; spf[idx[sel]] = p
isprime = (spf == 0); isprime[:2] = False; spf[isprime] = np.arange(M)[isprime]
mu = np.zeros(M, dtype=np.int64); Om = np.zeros(M, dtype=np.int64); mu[1] = 1
for k in range(2, M):
    p = spf[k]; q = k // p; Om[k] = Om[q] + 1; mu[k] = 0 if q % p == 0 else -mu[q]
lam = np.where(Om % 2 == 0, 1, -1); lam[0] = 0
Lam = np.zeros(M)
for p in np.nonzero(isprime)[0]:
    pk = p
    while pk < M: Lam[pk] = np.log(p); pk *= p
k = np.arange(M)
seqs = {'twin': np.where(k + 2 < M, np.concatenate([Lam[2:], [0, 0]]), 0.0),
        'selberg': (1 + lam) / 2.0}
seqs['twinpar'] = seqs['twin'] * (1 + lam) / 2.0
rng = np.random.default_rng(20261114)
for N in [int(x**e) for e in (0.30, 0.35, 0.40, 0.45, 0.49)]:
    for name, a in seqs.items():
        A = a[1:x+1].sum(); B = T = R = 0.0
        for m in range(1, x // (N + 1) + 1):
            hi = min(2 * N, x // m)
            if hi <= N: break
            n = np.arange(N + 1, hi + 1); v = mu[m * n] * a[m * n]
            B += abs(v.sum()); T += np.abs(v).sum()
            R += abs((np.abs(v) * rng.choice([-1, 1], size=v.size)).sum())
        print(N, name, B/T, R/T, B/A)
```
