# Programme (1): bounds for H_m, m >= 2 — scoping note

Date 2026-11-15. H_m = liminf (p_{n+m} - p_n), the shortest interval that contains m+1 primes
infinitely often. All quotes were taken from pdftotext copies of the sources, fetched on this date and
read as untrusted data. Page numbers are the printed page numbers unless "PDF p." is written.
Labels follow the project's convention: **Literature** (quoted), **Computed** (by this project), **Explored**
(heuristic, not certified).

## 1. Known values (Literature)

| | unconditional | under EH | under GEH |
|---|---|---|---|
| H_2 | **396 504** (Stadlmann 2023); PM8b 398 130 | 270 | 252 |
| H_3 | **24 407 016** (Stadlmann 2023); PM8b 24 797 814 | 52 116 | — |
| H_4 | **1 391 051 532** (Stadlmann 2023); PM8b 1 431 556 072 | 474 266 | — |
| H_5 | **77 510 685 234** (Stadlmann 2023); PM8b 80 550 202 480 | 4 137 854 | — |
| H_m asymptotic | **≪ exp(3.8075 m)** (Stadlmann 2023); claimed ≪ exp(3.7877 m) (GPT-6/Sharifi 2026, not verified) | ≪ m e^{2m} (PM8b) | — |

**Polymath8b**, arXiv:1407.4897v4, Theorem 1.4 (pp. 2–3), verbatim apart from the symbols:
> Theorem 1.4 Unconditionally, we have the following bounds: (i) H1 ≤ 246. (ii) H2 ≤ 398 130.
> (iii) H3 ≤ 24 797 814. (iv) H4 ≤ 1 431 556 072. (v) H5 ≤ 80 550 202 480. (vi) Hm ≤ Cm exp((4 − 28/157)m)
> for all m ≥ 1 and an absolute (and effective) constant C. Assume the Elliott-Halberstam conjecture EH[ϑ]
> for all 0 < ϑ < 1. Then we have the following improvements: (vii) H2 ≤ 270. (viii) H3 ≤ 52 116.
> (ix) H4 ≤ 474 266. (x) H5 ≤ 4 137 854. (xi) Hm ≤ Cme^{2m} for all m ≥ 1 [...]. Finally, assume the
> generalized Elliott-Halberstam conjecture GEH[ϑ] [...]. Then (xii) H1 ≤ 6. (xiii) H2 ≤ 252.

Theorem 3.2 (p. 8) gives the underlying DHL claims: "(ii) DHL[35 410, 3]. (iii) DHL[1 649 821, 4].
(iv) DHL[75 845 707, 5]. (v) DHL[3 473 955 908, 6]. [...] (vii) DHL[54, 3]. (viii) DHL[5511, 4].
(ix) DHL[41 588, 5]. (x) DHL[309 661, 6]. [...] (xiii) DHL[51, 3]." Theorem 3.3 (pp. 8–9) gives the tuple
diameters: "(ii) H(35 410) ≤ 398 130", "(ix) H(41 588) ≤ 474 266", "(vii) H(54) = 270", "(xiii) H(51) = 252".
Table 1 (p. 9): parts (ii)–(vi) use "Theorems 2.5, 3.10, 3.11", which is the MPZ input of Polymath8a. They do
**not** use Bombieri–Vinogradov alone.

**Stadlmann**, "On primes in arithmetic progressions and bounded gaps between many primes", arXiv:2309.00425v3
(22 Feb 2025; cited in the 2026 preprints as published in Adv. Math.). Abstract (p. 1): "lim inf (p_{n+m} − p_n) =
O(exp(3.8075m))". Theorem 2 (p. 2): "The quantity Hm = lim inf n→∞ (pn+m − pn) satisfies Hm ≪ exp(3.8075m)."
Corollary 1 (p. 2):
> H2 ≤ H(35265) ≤ 396504, H3 ≤ H(1624545) ≤ 24407016, H4 ≤ H(73807570) ≤ 1391051532,
> H5 ≤ H(3340375663) ≤ 77510685234.

Proof of Corollary 1 (§2.1.4, p. 9): "we use Theorem 6.7 of [14] with (k, c log(k), T log(k)) = (35265, 0.99479,
0.85213) for m = 2, [...] to deduce that M_k^{[δ/(1/4+ω)]} > m/(1/4+ω) holds for [...] (ω, δ) = (0.00556625,
0.0207987) for (m, k) = (2, 35265) [...]. Each of these choices of ω and δ satisfies 80ω + 80δ/3 < 1, so that
MPZ[ω, δ] holds." Corollary 2 (p. 8): "Let ω > 0 and δ > 0 with 80ω + 80δ/3 < 1. Then MPZ[ω, δ] holds." Her
asymptotic proof (p. 9) also gives "Hm ≪ exp(3.81m)" without Harman's sieve.

**Baker–Irving**, "Bounded intervals containing many primes", arXiv:1505.01815v1 (Math. Z. 286 (2017)),
Theorem 1.1 (p. 1): "We have Hm ≪ exp(3.815m)." The paper gives no explicit H_2,…,H_5.

**The 2026 preprints.**
- Stadlmann, "Bounded gaps between primes", arXiv:2608.31126v1 (31 Aug 2026), p. 1: "Concrete upper bounds for
  H2, . . . , H5 are also known, see [5] and [6]. The best known upper bounds on Hm for m ≥ 2 all use
  equidistribution estimates of Zhang type." Also p. 1: "In Polymath's approach to proving upper bounds on Hm
  [5], the gains from having a larger exponent of distribution outweigh the losses from being restricted to
  xδ-smooth numbers when m ≥ 2, but not when m = 1." The paper states **no new H_m bound for m ≥ 2**; its
  Theorem 1 concerns H_1 only (the extracted text reads "satisfies Hm ≤ 240", a typo for H1).
- Kintali, "Improved Bounded Gaps Between Primes" (1 Sep 2026, shivakintali.github.io/papers/Prime-Gaps.pdf):
  no H_m statement for m ≥ 2. "Many primes" appears only in reference titles.
- Charton et al., "A New Bound for Small Gaps Between Primes" (primegaps.axiommath.ai/bgp212.pdf): it defines
  DHL[k, m] (p. 2) but states results only for H_1.
- OpenAI, "Improved short gaps between primes": it defines H_m (§1.1) but states results only for H_1.
- Song–Yue, IACR ePrint 2026/1893: **not checked**. The PDF is behind a Cloudflare challenge (HTTP 403 to curl and
  WebFetch), and notes/sources-236-song-yue.md contains no H_m statement.
- GPT-6 Astra / Sharifi bundle (18 Sep 2026, math.ucla.edu/~sharifi/AI/prime_gaps_182_expository_bundle.pdf).
  Its companion paper "Incidence operators and intervals containing many primes" (bundle PDF pp. 53–87) states in
  its Theorem 1.1 (companion p. 2, PDF p. 54): "There is an absolute constant 𝐶 such that 𝐻𝑚 ≤ 𝐶 exp(3.7877𝑚)
  (𝑚 ≥ 1)." The abstract adds: "The constant implicit in this asymptotic statement is not evaluated." §12.1
  (companion pp. 33–34) uses the transfer "[𝛼] 𝑀𝑘 > 2𝑚/(𝜗(1 − 𝜅))", with 𝜗 = 5283999/10^7 and 𝜅′ = 139/200000,
  and 2(1+𝜀_BI)/(𝜗(1−𝜅′)) = 3.7876448630… < 3.7877. **No explicit H_2,…,H_5.** This claim is not verified here.

Conclusion: the best explicit bounds are Stadlmann 2023 (unconditional) and PM8b (EH, GEH). No 2026 source
gives an explicit H_m for m ≥ 2. Song–Yue is the one 2026 source not checked.

## 2. The criterion for DHL[k, m+1] (Literature)

PM8b, Lemma 3.4 (p. 9–10), the pigeonhole criterion: if ν obeys (13) with α and (14) with β_i, and "the key
inequality (β1 + · · · + βk)/α > m. (15) Then DHL[k, m + 1] holds." Also on p. 8: "DHL[k, m + 1] implies that
Hm ≤ H(k)".

- Theorem 3.8 (p. 13): "Suppose that there is a fixed 0 < ϑ < 1 such that EH[ϑ] holds, and such that
  Mk > 2m/ϑ. Then DHL[k, m + 1] holds." Bombieri–Vinogradov gives EH[ϑ] for every ϑ < 1/2. So under BV the
  condition is **M_k > 4m**: M_k > 4 for H_1 and **M_k > 8 for H_2**. This confirms the "ratio > 8 where
  H_1 needs > 4" reading, in the R_k normalisation. In the Stadlmann-2026 / project normalisation
  (Σt_i ≤ 1/4, criterion "kJ/I > 1"), the same statement reads ">1 for H_1, >2 for H_2". Under EH the H_2
  condition is M_k > 4, i.e. the variational problem of H_1 under BV. That is why 270 = H(54), with
  M_54 > 4.00238 (Theorem 3.9(vii)).
- Theorem 3.12 (p. 15), the ε-enlarged simplex: M_{k,ε} > 2m/ϑ, under EH[ϑ] with 1+ε < 1/ϑ, or under GEH
  with ε < 1/(k−1).
- Theorem 3.10 (p. 14), MPZ: "If M_k^{[δ/(1/4+ϖ)]} > m/(1/4+ϖ), then DHL[k, m + 1] holds", where MPZ[ϖ, δ] is
  given by Theorem 2.5 (p. 6: "MPZ[ϖ, δ] holds for every fixed ϖ, δ ≥ 0 with 600ϖ + 180δ < 7") or by Stadlmann's
  Corollary 2 (80ω + 80δ/3 < 1). For m = 2 the threshold is 2/(1/4+ϖ) ≈ 7.83 instead of 8. The price is the
  coordinate cap T = δ/(1/4+ϖ). Here δ, not ϖ, is the binding constraint.
- The explicit lower bound used for every large k is Theorem 6.7 (pp. 46–47). It takes
  g(t) = 1/(c+(k−1)t) on [0,T], with c = θ/log k, T = β/log k and τ = 1 − kμ (p. 54), and the values (θ, β)
  of Table 2 (p. 55).
- Upper bounds (Corollary 6.4, p. 44): M_k ≤ k/(k−1)·log k. (Proposition 6.5, p. 44):
  M_{k,ε} ≤ k/(k−1)·log(2k−1).

## 3. Reproduction (Computed)

Script: `code/hm/pm8b_mk_lower.py`. Output: `code/hm/pm8b_mk_lower.json`. The script implements Theorem 6.7
exactly as stated, (100)–(113), in arb ball arithmetic: python-flint 0.9, 256 bits, rigorous `acb.integral`, and
closed forms for m2, μ, σ², U and the singular part of W. θ and β are exact decimals. It runs on 1 core in about
90 s.

- **Table 2 entries reproduced.** k = 41588: M^{[T]} ≥ 8.0000014048 (published 8.000001401). k = 5511: 6.00004861.
  k = 35410: 7.82984925. k = 309661: 10.00000032. k = 1649821: 11.65752556. Hypotheses (105) and (106) hold in
  every case. Four of the published values are rounded up in the last digit, by at most 4·10^-9 (35410: ours
  7.8298492549, published 7.829849259). This changes no conclusion.
- **H_2 under BV only (Theorem 3.8 with M_k > 8).** The smallest k for which an optimised (θ, β) gives a
  certified M_k > 8 is **k = 41588** (θ = 0.978781, β = 0.943237, margin 1.4·10^-6). This **equals the source's
  k**: Table 2 / Theorem 3.9(ix), which PM8b uses for DHL[41588, 5] under EH. PM8b never states the
  BV-only consequence DHL[41588, 3], i.e. H_2 ≤ H(41588) ≤ 474 266 (Theorem 3.3(ix)). That bound is weaker than
  the MPZ result. The tuple was not constructed here.
- **H_2 unconditional, PM8b route (Theorem 3.10 with 600ϖ+180δ < 7).** The smallest certified k is
  **35410 = PM8b's k** (margin 9·10^-5 in the constraint; k = 35409 fails at the best parameters found). With
  PM8b's own (θ, β) the margin is 2.5·10^-6.
- **H_2 with Stadlmann's region (80ω+80δ/3 < 1).** Her parameters at k = 35265 are reproduced:
  ω = 0.00556625071811, δ = 0.0207986846 against her printed (0.00556625, 0.0207987), margin 6.8·10^-5. The
  optimiser also certifies **k = 35262** (θ = 0.996231, β = 0.844504), 3 below her 35265. This is a
  certified DHL[35262, 3] given her Corollary 2 and PM8b Theorem 6.7. Its value is cosmetic: H(35262) is not
  computed here, and it can be at most about 3 × 11 below 396 504.
- k_min is heuristic (Nelder–Mead plus bisection, assuming monotonicity in k). The criterion at k_min is
  rigorous given Theorem 6.7.

## 4. What a 2026-input H_2 bound would require

1. **The k range is about 3·10^4, not 40–50.** By Corollary 6.4, M_k > 8 needs k/(k−1)·log k > 8, so k ≥ 2981.
   Even the ε-enlarged problem needs k ≳ 1500 (Proposition 6.5). For a support inside ρ·R_k, rescaling gives a
   ratio at most ρ·k/(k−1)·log k. The 2026 H_1 supports reach only Σt_i ≤ 1/4 + ω + ε in Stadlmann-2026
   coordinates, i.e. ρ ≈ 1 + 4(ω+ε) ≈ 1.1–1.2 in R_k units. At k = 49–50 their ratio is therefore at most
   about 4.8, far below the 8 (or ≈ 7.6) needed. **The capped k ≈ 40–50 supports and certificates of this
   project are irrelevant to H_2.** Only the *idea* transfers: combining the BV simplex with a capped Zhang
   band, as in Stadlmann 2026 §1.1.
2. **Analytic inputs.** An MPZ-type estimate MPZ[ϖ, δ], or Type I/II/III estimates for a minorant, with an
   **explicit admissible δ** (smoothness). The binding constraint is δ, since T = δ/(1/4+ϖ) caps the
   coordinates. Candidates:
   (a) Stadlmann 2023 Corollary 2. This is published and already used; it gives 35265 (35262 here).
   (b) Stadlmann 2026 Lemmas 3–7 (Song–Yue Remark 4.23 flags Lemma 5), or Song–Yue Theorem 4.18. Both are
   hybrid BV/Zhang supports; neither is verified here.
   (c) The Sharifi bundle's Type II "5γ > 3/2 + 40ω + 16δ" together with its Type III and Harman minorant
   (𝜗 = 0.5284, 𝜅 ≤ 0.000695). Not verified, and stated only for "sufficiently small" δ ≤ δ0 = 1/108.
3. **Explored (not certified; scratchpad script).** Assume the transfer M_k^{[T]} > 2m/(𝜗(1−𝜅)) = 7.5753 for
   m = 2, with T = δ/(𝜗/2) as in PM8b. Then the smallest k with the Theorem 6.7 bound above 7.5753 is about
   44 450 at T = 0.035 (δ = 1/108, worse than 35262), about 34 600 at T = 0.05, and about 27 600 at T = 0.081
   (PM8b-sized δ ≈ 0.021). Whether 2026 inputs improve H_2 at all therefore depends on how large δ their Type
   I/II/III ranges allow at ω ≈ 0.014. No source evaluates this.
4. **Variational side.** At k ≈ 3·10^4 the symmetric-polynomial Gram method used for H_1 is useless. One needs
   an analogue of Theorem 6.7, the product ansatz g(t_1)…g(t_k) with a probabilistic analysis, for a hybrid
   support: the BV simplex Σt_i ≤ 1 plus a Zhang band 1 < Σt_i ≤ 1+4ω whose coordinates are capped at T. This
   is a new (modest) piece of mathematics. Once derived, the numerics are 1-D integrals and the same order
   of cost as above. The tuple H(k) for k ≈ 3·10^4 needs the PM8b/Sutherland greedy-sieve machinery, which is
   cheap at this size.

## 5. Recommendation

Programme (1) is **feasible on 4 cores / 16 GB**. Every computation is 1-D ball-arithmetic integrals plus a
k ≈ 3·10^4 admissible-tuple search. It is worthwhile only as a modest, clearly labelled small result:
"H_2 ≤ H(k) conditional on [named 2026 estimate]", with a gain of perhaps a few per cent in k (35265 down to
around 28k–35k). The outcome hinges on an analytic parameter (the δ-range) that the 2026 sources do not make
explicit. The H_1 work (capped supports at k ≈ 40–50) does not carry over. Under EH, H_2 is literally the
problem of H_1 under BV (M_k > 4). No new input is available there, so 270/252 stand. Suggested priority: below
the parity-barrier programme. Run it as a short side project only if step (i) below shows a gain.

**First concrete computation.**
(i) For each candidate input set (Stadlmann 2023 Corollary 2; Stadlmann 2026 Lemmas 3–7; Sharifi Type II/III),
derive the feasible (ϖ, δ) region with exact rational inequalities.
(ii) Maximise over (k, θ, β, ϖ) with δ = T(1/4+ϖ), using the existing `code/hm/pm8b_mk_lower.py` with its
constraint function swapped, to get each input's k_min for m = 2 (and m = 3–5 at no extra cost).
Step (ii) for Stadlmann 2023 is already done here (k = 35262). Only if some 2026 region gives k clearly below
35262 should the hybrid-support Theorem 6.7 analogue (item 4) be derived.
