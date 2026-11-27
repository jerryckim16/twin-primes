# Rung 186: the analytic-input side of Lemma 1.1 of [14] (hypotheses of the imported estimates of [8])

Sources (fetched 27 Nov 2026 with curl into the new empty directory `/tmp/claude-0/oai186-l11/dl.3SAK/`, read with
`pdftotext -layout`; PDFs not committed; nothing from the authors' repository was opened or executed):
- [14] OpenAI, "Numerical certificate for prime gaps at most 186", 30 Aug 2026,
  https://raw.githubusercontent.com/openai/PrimeGaps186/main/short_gaps_numerics.pdf, 218865 bytes, 23 pp.,
  SHA-256 `79190b2ca18cb8aca0645a7bf97c1fb48e8984af4785cf18079d9b4f74c90031` (identical to
  `code/third_party/openai186/short_gaps_numerics.pdf`).
- [8] OpenAI, "Improved short gaps between primes", 30 Aug 2026,
  https://cdn.openai.com/pdf/51126fac-1b68-4128-9666-c908bcc16033/short_gaps.pdf, 369949 bytes, 39 pp.,
  SHA-256 `456f05e0a3ef589ebb0e9abcfd31f140f3c945adbf6950e00ef371a3c88b0930` (same as recorded in
  notes/oai186-restoration-threshold.md).

"p." means a printed page number. Equation numbers belong to the paper named. Inside [14], "[8]" is the main paper.
Inside [8], "[14]" is the companion, "[15]" is Polymath, "New equidistribution estimates of Zhang type" (ANT 2014),
"[16]" is Polymath, "Variants of the Selberg sieve", "[17]" is Sarajian-Weingartner, "[19]" is Stadlmann, Adv. Math.
468, "[2]" is Baker-Irving, and "[4]" is Bombieri-Friedlander-Iwaniec.

Script: `code/oai186_lemma11_check.py` (`/usr/bin/python3 -I`, exact `fractions.Fraction` only, no flint).
Output: `code/oai186_lemma11_check.out`. **112 checks, 0 failures, including 11 negative controls, all caught.
Runtime 0.10 s.** I wrote it from the two PDFs alone.

**Verdict: verified as stated, with one wording caveat (R1 in §4).** I recomputed every source row of [14] from the
printed rationals. Each one satisfies the exact hypotheses of the [8] statements that [14] invokes:
- strict hypotheses, each with margin >= 10^-6 (the paper says > 10^-8);
- the transfer guards;
- the order-three budget;
- the radius bounds, the level and density retreat, and complete band coverage;
- the cap, group and inner-square claims.

Every line of the proof of Lemma 1.1 checks out. I found no gap. What stays unchecked is the analytic number theory
inside [8] (and further back) behind these statements; §5 records where it comes from.

Status: Claimed. This verifies that the hypotheses are met. It does not verify the theorems of [8].

## 1. What Lemma 1.1 states ([14] p. 6)

> Every retained row satisfies its strict distribution inequalities, actual-LCM transfer guards, and the level and
> density retreat to rho*. The retained bands cover all mixed moduli on the physical cells, and all bounds for the
> largest fragment and opposite root hold. In order three, max(A_t, C_t) <= 7L_t/3. The six groups satisfy
> xi_G > 2h, xi_G < p_G <= z_G, and z_G + m_G p_G <= U_G. The new order-two row 12 also implies the common inner
> self-square source.

The proof runs from p. 6 to p. 7. The data come from (1.13)-(1.17) on p. 4, (1.18)-(1.24) on pp. 5-6, and (1.5) on
p. 2. The row parameters are ω (level: moduli up to x^{1/2+2ω}) and δ (density: x^δ-dense divisibility). Each row's
(ω, δ) comes from the ladder (1.15). There are two ladders: "old" (full primes P_x, eps_o = 1e-6, 29 rows) and
"new" (Stadlmann minorant ϱ, eps_n = 1e-7, 43 rows). The proof says nothing about its sigma choices or about what
Prop 2.22 requires beyond the points listed in §3.

## 2. The statements of [8] that Lemma 1.1 relies on (page, equation)

| Use in Lemma 1.1 | [8] statement | Hypotheses (exact) |
|---|---|---|
| old rows, r = 1, 2, bilinear | Prop 2.16 (p. 10) = [15, Thm 2.8(i),(ii),(iv)] | 0<ω<1/12, 0<δ<1/4+ω, 0<σ<1/2, 68ω+14δ<1; (2.11): 54ω+15δ+5σ<1 (r=1), 56ω+16δ+4σ<1 (r=2) |
| old rows, Type III | Prop 2.17 (p. 10) = [15, Thm 2.8(v)] | (2.12): 1/18+28ω/9+2δ/9 < σ < 1/2 (plus 0<ω<1/12, 0<δ<1/4+ω) |
| old rows, r = 3, bilinear | Prop 2.18 (pp. 10-11), (2.14) | 72ω+24δ<1, 48ω+16δ+4σ<1, 64ω+20δ+2σ<1 |
| old rows, assembled | Cor 2.19 (p. 11) and its proof | (2.15): 108ω+30δ<1 / 280ω+80δ<3 / 240ω+80δ<3. Proof: σ>1/10 (Heath-Brown reduction [15, Lem 2.7, 3.1]), σ>2ω, (2.12), and the bilinear inequalities with one common σ. At r=3, σ := 1/10+(3-240ω-80δ)/40 |
| new rows | Prop 2.22 (pp. 12-13) and its proof | 0<ω<1/12, 0<δ<1/4+ω; (2.24): 1/4+7ω+2δ<c*, 1/18+28ω/9+2δ/9<19/200, 1/2+2ω<b*. r=1,2: 68ω+14δ<1 and (2.11) with σ_m. r=3: (2.14) with σ_m. The proof needs σ_m+τ in place of σ_m and the three bounds of (2.24) lowered by τ, for some fixed 0<τ<=10^-10 |
| constants | (2.19) (p. 11) | a* = 0.40481, b* = 0.59519, c* = 0.33856 (exact); σ_m = 1/2 - a* |
| transfer r = 1, 2 | Lemma 4.1 (pp. 24-25), via Prop 2.4 (p. 5) | s_D <= S, s_E <= T, Q=[D,E] > R^B; (i) B+ξ >= 2T; (ii) B+ξ >= max(2S-T, 2T-S); predicates s<=a or H_{2,ξ} <= a+ξ (and the same with b) |
| transfer r = 3 | Prop 4.2 (p. 25), via Prop 2.3 (p. 4) and Lemma 2.2 | (4.6) A+C <= B+ξ; φ_D, φ_E nonnegative and nondecreasing with φ_D+φ_E = 3u (4.7); φ(0)=0 by (4.5); predicates (4.8)-(4.9); concrete φ in (4.10), L = 23C/40 |
| retreat | §4.2.4, (4.19) (p. 26) | ρ* < ρ ⇒ R^ξ < x^δ and W[D,E] <= x^{ρ*B⁺+o(1)} < x^{1/2+2ω-ε} |
| inner squares | (4.13)-(4.17), Lemma 4.3 (pp. 25-26) | Lemma 4.3 guard c+ξ >= 0; (4.15) parameters; the (4.16) margins; (4.17) |
| moduli below the first band | Prop 2.15 (BV, p. 10) and (2.26) (p. 12) | R^{B_0} = x^{ρ*/(2ρ)} < x^{1/2} |

[8] §4.2.2 (p. 25) says: "The strict distribution inequalities, lower-order transfer guards, order-three budgets and
coverage of all mixed moduli are verified in [14, Lem. 1.1]." The citations therefore run both ways. [8] proves
statements for general parameters, and [14] supplies the numbers. Neither proof assumes the other's conclusion, so
the citation is not circular.

## 3. Line-by-line check of the proof of Lemma 1.1

Script sections are in brackets. All checks are exact.

| # | Step of the proof ([14] pp. 6-7) | Status | Detail |
|---|---|---|---|
| 1 | Parameters (1.1), (1.13) are consistent with [8] (4.1), (4.11), (2.19) | verified [0] | ρ = 1/4+Ω_o = 262499/10^6, ρ* = ρ-g0, S, T0 = 2-3/1000-S, T1 as printed. σ_{m,τ} = 1/2-a*+τ. τ = 10^-10 is allowed by Prop 2.22's proof. b* = 1-a* |
| 2 | "The block formula after (1.15) gives the row counts and these rational enclosures" | verified [1] | 29 rows (12,12,5) and 43 rows (12,12,19). Only the last row of each ladder is terminal. The block formula W+(2/s)^j(v-W) reproduces every untruncated value. All six printed 10^6·ω intervals are exactly [floor(min), ceil(max)]. Note: the new ladder terminates only because Ω_n = 0.01265 < W_{n,3} = 0.0126507... (negative control: Ω_n+1e-5 never terminates) |
| 3 | Old rows r=1,2 satisfy Prop 2.16 with σ = σ0 = 0.100001, plus Type III (2.12) | verified [2] | By construction 54ω+15δ+5σ0 = 1-15eps_o (r=1) and 56ω+16δ+4σ0 = 1-16eps_o (r=2) hold identically. Least margins: (2.11) 1.5e-5 / 1.6e-5; 68ω+14δ<1 >= 0.31; (2.12) >= 0.0155; σ0 > 1/10 by 1e-6; σ0 > 2ω by >= 0.082. Cor 2.19's (2.15) also holds (margins 4e-5, 1e-4) |
| 4 | Old rows r=3: (2.14) and (2.12) with σ = 1/10+(3-240ω-80δ)/40 | verified [2] | This σ equals 1/10+2eps_o identically (the ladder sets 240ω+80δ = 3-80eps_o). (2.14) margins: 0.100024, 8e-6, 3.65e-4. (2.12) >= 5.77e-3 (row 27). σ>1/10 by 2e-6; σ>2ω; (2.15) margin 8e-5 |
| 5 | New rows: Prop 2.22 with σ_{m,τ} in (2.11) (r=1,2) and (2.14) (r=3), 68ω+14δ<1 (r=1,2), and the three bounds of (2.24) lowered by τ | verified [2] | Least margins: (2.11) 1.5e-6 / 1.6e-6 (= 15eps_n, 16eps_n); (2.14) third = 1-20eps_n exactly, so margin 2e-6; first (2.24) bound 9.69e-6 at (n,38); second 9.46e-5 at (n,38); third >= 0.0699 |
| 6 | "the Type III parameter can be chosen below 19/200 - τ" | verified [2] | This is the second (2.24) bound lowered by τ. It holds on all 39 new rows. My reading of Prop 2.22's proof: σ3 must lie in (1/18+28ω/9+2δ/9, 19/200-τ). That makes the three smooth lengths in [x^{0.19-τ}, x^{0.405+τ}] with pairwise products >= x^{0.595-τ} satisfy (2.13). Exactly this interval is checked here |
| 7 | "These comparisons are affine in ω" (so endpoint checks suffice) | true; not needed | δ = c-sω-eps is affine in ω inside a block, and σ is constant there. I checked every row exactly, so the endpoint argument is not used |
| 8 | "The least positive density is 89999/10^11, and every required strict affine margin exceeds 10^-8" | verified [2]; see R1 | The least δ over all 72 ladder rows is exactly 89999/10^11, at the terminal row (n,42), which is **not retained**. Over the retained rows the least δ is 8.8236e-6 at (n,38). The least margin over the retained rows is 1e-6 (σ0 > 1/10). The least over all 72 rows is 8.9999e-7 (δ>0 at (n,42)). Both exceed 10^-8 |
| 9 | "lower-order transfer guards reduce to S-T_ν+e >= 0 and min(2T_ν-S, 2S-T_ν)+e >= 0" | verified [3] | B+ξ = S+T_ν+e exactly on every nonterminal row (from δ-E+2ω_{t-1} = g0). So Lemma 4.1(i) B+ξ>=2T ⇔ S-T+e >= 0, and (ii) ⇔ the min. Least slack 0.0888. Also, the (1.21) thresholds a+ξ and b+ξ equal A and C, as Lemma 4.1 needs |
| 10 | "In retained order three, η = ξ-e/2 > 0, A+C = B+ξ, A >= C > L, A <= 11C/10 < 161C/120 = 7L/3" | verified [3] | A+C = B+ξ gives (4.6) with equality. (4.10)'s φ_D, φ_E are nonnegative and nondecreasing, vanish at 0, and sum to 3u. This is the part already checked in oai186-lemma14-check.md, rechecked here |
| 11 | Radius hypotheses s_D <= S, s_E <= T_ν of Lemma 4.1 and Prop 4.2 (implicit in the proof) | verified [3] | The largest retained cell upper endpoints are 98303h < S = 98304h, 89563h <= T0 (T0/h = 89563.39) and 89953h <= T1 (T1/h = 89953.81) |
| 12 | "The bounds for the largest fragment and opposite root are therefore A_t-L_t and 63C_t/160; the lower-order cap is half the threshold. Each exceeds its activation. Taking their running minimum after each core, together with ζ, gives (1.18)" | verified [5] | For the outer, base and enlarged domains I took the running minimum over the cores of the retained rows that apply (outer: both ladders with cores a_t; base: old r>=2 with cores b_t; enlarged: new r>=2). After each core it equals the printed piecewise z(s). Each cap exceeds its row's ξ. Why these caps are sufficient is Lemma 1.4's largest-witness exclusion, verified in oai186-lemma14-check.md row 7 |
| 13 | "Inward cap rounding and full upper cell endpoints give (1.5)... the terminal rows lower no cap" | verified [5] | (1.19) applied to (1.18) reproduces all nine rows of (1.5) exactly. The terminal rows are not retained |
| 14 | Boundary comparisons floor(B/h) = 187773, 188087, 188254, 188256; pair maxima 187866h, 188256h; B⁺_t = B_{t+1} | verified [4] | Retained-row rule (1.20): B_{o,27} < 187866h <= B_{o,28} and B_{n,38} < 188256h <= B_{n,39}. Coverage: the B⁺ of the last retained row is >= the pair maximum, and B is strictly increasing. Every mixed modulus Q = [D,E] <= DE < R^{S_box+T_ν,box} therefore lies below R^{B_0} or in one retained band |
| 15 | "Since ρ* < ρ, every level and density endpoint, including the initial BV band, is strictly retreated" | verified [4] | For all retained rows, ρ*B⁺ < 1/2+2ω and ρ*ξ < δ. B_0 = 1/(2ρ), so ρ*B_0 < 1/2 |
| 16 | "min ξ_t > 33·10^-6 > 22·10^-6 > 2h" | verified [4] | min ξ = 3.3614e-5 at (n,38); 2h = 2.126e-5 |
| 17 | Six-group tables and splitting guards ξ_G > 2h, ξ_G < p_G <= z_G, z_G+m_G p_G <= U_G; "later order-5/2 activation and threshold are no larger" | verified [6] | Over the source rows of (1.22), ξ_G, U_G and b_G are the minima printed in (1.23). p_G/h = floor(U_G/(2m_G h)) as in (1.24). The guards are tight for O2 (slack 0.036h), I2old (2.43h) and I2new (1.85h). Negative controls: one more cell in z_G (O2) or p_G (I2new) breaks them |
| 18 | Common inner-square source: (4.15) parameters, the prime and minorant margins, 1/2+2ω_s-2ρT1 = 55122259/13124945000, c_s+ξ_s > 0, c_s-b_{n,12} > 4/100, ξ_s-ξ_{n,12} > 5/100, C_{n,12} < c_s+ξ_s ⇒ row 12 implies S(B_BV,T1,ξ_s) | verified [7] | The prime estimate at (ω_s,δ_s,σ0) has least margin 1.6e-5 ((2.11) r=2). The minorant has least margin 0.0136. The exact value is as printed. The differences are 0.0429 and 0.0510. The implication holds because b_{n,12} < c_s, and because ξ_s > ξ_{n,12} gives H_{2,ξ_s} <= H_{2,ξ_{n,12}} (fewer witnesses) <= C_{n,12} < c_s+ξ_s. Lemma 4.3 = Lemma 4.1(ii) with S = T = T1, whose guard is exactly c+ξ >= 0. Also ρ*·2T1 = 0.502 < 1/2+2ω_s and ρ*ξ_s < δ_s |
| 19 | Remark 1.2 (base face must carry the new conditions) | not checked | Not part of Lemma 1.1 |

## 4. Where my reading differs from, or adds to, theirs

None of these is presumed to be an error.
- **R1 (wording).** "The least positive density is 89999/10^11" is the minimum over all ladder rows. It is attained at
  the terminal, non-retained row (n,42). That row's ω = Ω_n and δ < 10^-6 match Prop 2.22's "order-three example".
  Over the retained rows the minimum is 8.82e-6. Neither reading changes anything.
- **R2.** For orders 1-2, Prop 2.22 is stated with σ = σ_m. Its proof needs σ_m+τ, and [14] checks σ_{m,τ}, which is
  the stronger condition. I checked both the stated and the proof-level conditions with σ_{m,τ}.
- **R3.** For the old rows, Theorem 1.1's proof cites Cor 2.19, whose hypothesis is (2.15). [14] instead checks the
  underlying Prop 2.16/2.17/2.18 conditions with an explicit σ. I checked both. The extra conditions in Cor 2.19's
  proof (σ>1/10, σ>2ω, one common σ for the bilinear and Type III ranges) also hold. The binding one is σ0 > 1/10, by
  1e-6.
- **R4.** I read the first bound of (2.24) as (2.17) of Lemma 2.20 at σ = 1/2-(c*-τ): 4σ+28ω+8δ<1 ⇔
  1/4+7ω+2δ < c*-τ. I read the third bound as the condition b*-τ > θ = 1/2+2ω needed by (2.18). This is consistent
  with the proof's text. It is a reading, not checked further.
- **R5.** Lemma 1.1 does not mention the radius hypotheses s_D <= S, s_E <= T_ν of the transfer results. They hold on
  the grid (row 11), with 0.39h and 0.81h to spare for T0 and T1.
- **R6.** The tightest margins are of order 10^-6 (σ0 - 1/10; 15-20·eps_n in the minorant bilinear conditions; the
  first (2.24) bound at (n,38) is 9.7e-6). All are fixed positive constants, which is all the qualitative argument
  of [8] uses (§4.2.4, "fix the strict source ... margins").

## 5. Chain of imports (located, not verified)

- [14] Lemma 1.1 → [8] Prop 2.16 → [15, Thm 2.8(i),(ii),(iv)] (Polymath; the Type II part is used on doubly dense
  moduli as a subclass of singly dense).
- → [8] Prop 2.17 → [15, Thm 2.8(v)] (Type III).
- → [8] Prop 2.18 (2.14) → [19, Prop 1] (Stadlmann), extended to triply densely divisible moduli in [8] §A.4
  (Lemma A.7 and the following; pp. ~33-35). The extension is proved in [8] itself.
- → [8] Cor 2.19, proved in [8]: it combines 2.16, 2.17 and 2.18 with the Heath-Brown reduction [15, Lem 2.7]
  (combinatorics [15, Lem 3.1]), subinterval uniformity [15, Rem 3.6], and [8] Prop 2.12(iii) (proved in [8]).
- → [8] Prop 2.22, proved in [8] §A.6 by Lemma A.8 (localized coefficients and their Siegel-Walfisz property) and
  Lemma A.9 (corrected Buchstab decomposition). These rework [19, Lems 18-22, §4.8]. The proof also uses:
  - [8] Lemma 2.20, from §A.5 adapting [2, Lem 3], with (2.18) via the Type 0 argument of [15, §3];
  - Prop 2.16/2.18 (bilinear) and Prop 2.17 (Type III);
  - for (2.26): Prop 2.13 ([16, §4.5]), Prop 2.10 ([15, Lem 3.4], [16, §4.5]) and Prop 2.15 (BV [4, (1.4)];
    [15, Thm 2.9]).
- → [8] Prop 2.21 (minorant positivity and mass) → [19, Prop 2]. The bound κ_true is recomputed in [14] Lemma 2.8,
  which is not checked here.
- Transfer: [8] Lemma 4.1 → Prop 2.4 (proved in [8]; its order-two insertion step is [17, Prop 1], re-proved inline).
  [8] Prop 4.2 → Prop 2.3 (proved in [8]) → Lemma 2.2 (first part = [17, Thm 2]; second part proved in [8]).
  Dense divisibility is Definition 2.1 = [15, Def 2.1] (= [17]'s starred class), with properties from
  [15, Lem 2.10(0)-(iii)].
- Inner squares: [8] Lemma 4.3 → Lemma 4.1(ii). BV below R^{B_BV}.
- Retreat and W-adjoining: [8] (4.19) and Lemma 2.2's second part, in §4.2.4.

Reading of the proofs: I read the short proofs of Lemma 2.2, Props 2.3/2.4, Lemma 4.1, Prop 4.2 and Lemma 4.3. They
are consistent with how [14] uses them: exponentiating the log-conditions gives exactly (2.1)/(2.2), with
X = R^B, Y = R^ξ, D0 = R^S, E0 = R^T, caps R^A and R^C. This is a reading check, not a verification of
Sarajian-Weingartner's Thm 2.

## 6. Final table

| Claim of Lemma 1.1 | Status |
|---|---|
| strict distribution inequalities (old: Prop 2.16/2.17/2.18, Cor 2.19; new: Prop 2.22) on all 67 retained rows | **verified exactly** (least margin 1e-6) |
| row counts, ω enclosures, least density 89999/10^11, margins > 10^-8 | **verified** (R1: the least density is at a non-retained row) |
| actual-LCM transfer guards (Lemma 4.1), order-three budget (Prop 4.2) | **verified exactly** |
| radius hypotheses of the transfer results | **verified** (implicit in [14]) |
| level and density retreat to ρ*, initial BV band | **verified** |
| band coverage (1.20), boundary floors, pair maxima | **verified exactly** |
| caps (1.18) as running minimum, each > activation, masks (1.5) | **verified exactly** |
| max(A,C) <= 7L/3, A <= 11C/10 | **verified** (again; first in oai186-lemma14-check) |
| largest-fragment and opposite-root bounds suffice | verified earlier (oai186-lemma14-check row 7) |
| six-group guards (1.23)-(1.24) | **verified exactly** |
| new row 12 ⇒ common inner-square source, (4.16)-(4.17) | **verified exactly** |
| the analytic statements of [8] themselves (Props 2.15-2.18, 2.21, 2.22, Cor 2.19, Lemma 2.20, App. A) | **not verified** (located, §5) |

## 7. Not checked

- The truth of [8] Props 2.15-2.18, Cor 2.19, Lemma 2.20, Props 2.21-2.22 and Appendix A (§A.4 triple dense
  divisibility, §A.5, §A.6 Lemmas A.8-A.9), and the external inputs [15], [16], [17], [19], [2], [4].
- Whether the exponent ranges in Prop 2.22's proof (x^{0.19-τ}..x^{0.405+τ}, pairwise >= x^{0.595-τ}, bilinear
  x^{a*-τ}..x^{b*+τ}) are the ranges Stadlmann's decomposition actually produces (R4).
- The finite-band realization (§4.2.4, Lemma 4.4) and Prop 4.6, which consume these sources.
- [14] Lemma 2.8 (κ_true) and Remark 1.2.
