# Re-check of Stadlmann (arXiv:2608.31126) and Charton et al. (bgp212.pdf) against sources-enlarged-supports.md §2–§3

Compiled 2026-11-12 from the primary PDFs:
- Stadlmann, arXiv:2608.31126v1 (31 Aug 2026), 34 pp. Fetched with WebFetch and extracted with `pdftotext -layout` (plus a raw `pdftotext` pass for garbled fractions).
- Charton, Hong, Lau, Ono, Remy, Siu, Swaminathan, Thorner, Xie, "A New Bound for Small Gaps Between Primes", primegaps.axiommath.ai/bgp212.pdf (46 pp., PDF created 3 Sep 2026). Fetched and extracted the same way.

The quotes below are copied from the text extraction. Display fractions often come out flattened: for example "1/2" can appear as "12" or "21", and "∑" can be lost. Where I rebuilt a fraction, I say so and mark it **RECONSTRUCTED**. Anything I could not read reliably is marked **UNSURE**.

Status key: CONFIRMED / DIFFERENT / NOT FOUND.

---------------------------------------------------------------------------------------------
## (a) Stadlmann, Definition 1 (§2.1, p. 3): $T_k(\delta,A,B,\varepsilon)$ — **CONFIRMED**

Quote (Def. 1, p. 3):
> "Definition 1 (Simplex subset). Let k ∈ N, δ > 0 and ε > 0. Let n ∈ N and A = (A0 , A1 , . . . , An ) with −ε = A0 < · · · < An < 1/2 − ε. Let B be a n × ⌊1/δ⌋ matrix with (j, m)th entry equal Bj,m . Matrix B must satisfy that for any m ≥ 1, δ < Bj,m ≤ Bj,m+1 ≤ Bj,m + δ."

> "Tk (δ, A, B, ε) = ⋃_{j=1}^n { (t1 , . . . , tk ) ∈ [0, 1]^k : Σ_{i=1}^k ti ∈ [Aj−1 + ε, Aj + ε) and Σ_{i∈I} ti ≤ Bj,|I| for I = {i : ti > δ} }."

(The "1/2" and "1/δ" were flattened in the extraction. The sum and union signs are restored from the layout.)

- Band condition: the interval is half-open, $[A_{j-1}+\varepsilon, A_j+\varepsilon)$. CONFIRMED.
- Cap condition: $\sum_{i\in I}t_i\le B_{j,|I|}$ with $I=\{i:t_i>\delta\}$. CONFIRMED.
- Constraints: $-\varepsilon=A_0<\dots<A_n<\tfrac12-\varepsilon$ and $\delta<B_{j,m}\le B_{j,m+1}\le B_{j,m}+\delta$. CONFIRMED.
- Def. 1 does not define $B_{j,0}$. Charton et al. add $B_{j,0}=0$ (see (e)).
- Remark after Def. 1 (p. 3): "this condition implies that also Σ_{i∈I′} ti ≤ Bj,|I′| for any I′ ⊆ I."
- §6.1 (p. 33) restates the same definition verbatim.

## (b) Stadlmann, Definition 5 and Proposition 1 (pp. 4–5) — **CONFIRMED**, with nuances

Quote (Def. 5, p. 4):
> "Definition 5 (Key integrals). Let Tk (δ, A, B, ε) be as given in Definition 1. Let F be a symmetric, square-integrable function supported on Tk (δ, A, B, ε). Then define"

- $I(F;\delta,A,B,\varepsilon)=\int\cdots\int_{T_k(\delta,A,B,\varepsilon)}F(t_1,\dots,t_k)^2\,dt_1\dots dt_k$. The domain is $T_k$ itself. CONFIRMED.
- $J(F;\delta,A,B,\varepsilon)=\sum_{m=1}^n\sum_{m'=1}^n\int\cdots\int F(t_1,\dots,t_{k-1},t_k)F(t_1,\dots,t_{k-1},t_k')\,dt_1\dots dt_{k-1}dt_kdt_k'$, over the region
  > "t1 +···+tk−1 ≤ max{Am −ε, Am′ −ε} / t1 +···+tk−1 +tk ∈ [Am−1 +ε, Am +ε] / t1 +···+tk−1 +t′k ∈ [Am′−1 +ε, Am′ +ε]"

  CONFIRMED.
  - The band intervals inside $J$ are written **closed**, $[\cdot,\cdot]$, while Def. 1 uses half-open intervals. This only changes sets of measure zero.
- $K(F)$ has the same double sum and the same three-line region, except that the first line is "t1 +···+tk−1 > max{Am −ε, Am′ −ε}". Its integrand is "F (t1 , . . . , tk )^2 dt1 . . . dtk".
  - So the condition on $t_k'$ appears in $K$'s domain, but $t_k'$ is not integrated. This is a quirk of the paper as printed; Charton et al. Def. 4.6 copies it identically.
  - This resolves the old note's UNSURE about $K$: the transcription in the old note was correct.

Quote (Prop. 1, p. 5):
> "(1) Prime minorant: −c2 ≤ ρ(n; x) ≤ 1P (n) for all large x and n ∈ [x, 2x]. (2) ρ has equidistribution properties for moduli corresponding to Tk (δ, A, B, ε). (See Definition 3.) (3) If ρ(n; x) ≠ 0, then all prime factors of n exceed x^β , for some β > max{Bj,1 : 1 ≤ j ≤ n}. (4) The sum of ρ(n; x) over [x, 2x] satisfies Σ_{n∈[x,2x]} ρ(n; x) = (1 − c1 + o(1)) x/log(x)."

> "Suppose there exists a symmetric, square-integrable function F supported on Tk (δ, A, B, ε) with (2.1) [k(1 − c1 )J(F ; δ, A, B, ε) − kc2 K(F ; δ, A, B, ε)] / I(F ; δ, A, B, ε) > 1. Then H1 = lim inf n→∞ (pn+1 −pn ) ≤ H(k), where H(k) is the diameter of the shortest admissible k-tuple."

- (2.1) is the ratio "> 1". It is equivalent to $k(1-c_1)J-kc_2K>I$ because $I>0$. CONFIRMED.
- Requirements on $F$: **symmetric, square-integrable, supported on $T_k$**. Nothing else is required: no smoothness, and no extra vanishing on the marginal domain. §5.1 applies this to $F=\sum c_lG_l$, and I read this as implicitly restricted to $T_k$, since $M_1$ integrates over $T_k$ and the $M_2$ domain constraints enforce the bands. **UNSURE** whether the paper ever says "$F=1_{T_k}\cdot\sum c_lG_l$" explicitly; I did not find that wording.
- **$n=1$ reduction (my derivation, not stated in the paper):**
  - With $n=1$, $A_0=-\varepsilon$, so the band is $[0,A_1+\varepsilon]$.
  - Both band conditions in $J$ are then implied by the support of $F$ (up to measure zero).
  - Hence $J(F)=\int_{t_1+\dots+t_{k-1}\le A_1-\varepsilon}\big(\int F\,dt_k\big)^2\,dt_1\cdots dt_{k-1}$, with the $t_i$ effectively in $[0,1]$ because of the support of $F$.
  - **CONFIRMED (by derivation).**
  - Note that only the sum $t_1+\dots+t_{k-1}$ is restricted in the outer domain. The $B$-caps on the base variables come only from the support of $F$; the paper does not impose them separately.
- Symmetry is only needed to use a single $J$ in place of $\sum_i J_i$. The paper's $M_2$ (§5.1, p. 31) is written with a general index $i$ in the domain lines ("t1 +···+ti−1 +ti+1 +···+tk ≤ max{...}"), but its integrand uses $t_k, t_k'$. This is a typographical inconsistency in the source.

## (c) Stadlmann's final parameters (§6.2, "Proof of Theorem 1", p. 34) — **CONFIRMED** except the degree, which is **inconsistent within the paper**

Quote (p. 34):
> "We choose ε = 0.0075 and A = (−ε, 0.253) and δ = 0.028. Furthermore, we take B = (B1,1 , . . . , B1,⌊1/δ⌋ ) with B1,1 = B1,2 = 0.15 and B1,m = 0.17 for m ≥ 3. Next we choose ξ1 = 0.38 and ξ2 = ξ3 = 0.4."

> "this proposition tells us to use ρ(n; x) = 1P (n), which means c1 = c2 = 0. We compute the relevant matrices M1 and M2 for k = 49 and are able to obtain a vector c with c M2 c^T / c M1 c^T > 1. Therefore Proposition 1 tells us that H1 ≤ 240."

| Item | Status |
|---|---|
| $k=49$ | CONFIRMED |
| $\varepsilon=0.0075$ | CONFIRMED |
| $A=(-\varepsilon,0.253)$, so $n=1$ | CONFIRMED |
| $\delta=0.028$ | CONFIRMED |
| $B_{1,1}=B_{1,2}=0.15$, $B_{1,m}=0.17$ for $m\ge3$ | CONFIRMED |
| $\xi=(0.38,0.4,0.4)$ | CONFIRMED |
| $c_1=c_2=0$ | CONFIRMED |

**Degree $D=19$: DIFFERENT / internally inconsistent.**
- §5.1 (p. 31): "In particular, H1 ≤ 246 was obtained by optimization over basis B27 . To obtain H1 ≤ 240, we work with the smaller basis B19, which indicates that our method gives quite a large improvement."
- Introduction (p. 1): "while Polymath [5] used symmetric polynomials of degree ≤ 27 to achieve H1 ≤ 246, we only needed polynomials of degree ≤ 21 to get H1 ≤ 240."
- §1.1 (p. 2): "we will use the same kind of basis to prove H1 ≤ 240, but with the stricter condition 2a + b ≤ 21."
- §1.1 (p. 2): "it can still take days to compute all necessary matrix entries for symmetric polynomials of degree 2a + b ≤ 21."
- So the paper says 21 three times (abstract area and §1.1) and 19 once (§5.1). The old note's "D=19" follows §5.1 only. **UNSURE which is correct.**

Basis definition (§5.1, p. 31):
> "BD = { p(t1 , . . . , tk )^2 (1 − t1 − · · · − tk )^b : p(t1 , . . . , tk ) symmetric polynomial, deg(p) = a, 2a + b ≤ D }."

- The factor is $(1-\sum t_i)$, not $(A_1+\varepsilon-\sum t_i)$. CONFIRMED as printed.

**Numerical ratio: NOT FOUND.** Only "c M2 c^T / c M1 c^T > 1" is stated (p. 34 and §6.1).

**Basis dimension: NOT FOUND.**

Additional observations:
- §6 opens with "To conclude the proof of H1 ≤ 246", which is a typo for 240.
- Thm 1 reads "H1 ... satisfies Hm ≤ 240", a misprint the old note already recorded.
- §6.2, verbatim: "the upper bound on the sum over I1 in each of the conditions (A), (B), (C) and (E) is greater than 0.34. Since B1,m + B1,m′ ≤ 0.34 ... In condition (D) we are done if we have {1, . . . , m + m′ } = I1 ∪ I2 with bounds Σ_{i∈I1} yi ≤ 0.32 and Σ_{i∈I2} yi ≤ 0.07."

## (d) Stadlmann: $\omega$ in terms of $A_j$; conditions in Lemmas 3–7; Prop. 3

**$\omega(j,j')$: CONFIRMED.**
- Prop. 3(A) (p. 27): "ω(j, j′) = (Aj + Aj′)/2 − 1/4". The fraction was flattened in the extraction; the layout is unambiguous.
- Proof of Prop. 3 (p. 27): "q ≤ x^{(1−ε0)(Aj +Aj′)} and so we will work with ωmax = (Aj + Aj′)/2 − 1/4."
- Later (p. 29): "Recalling that ωmax ≤ An − 1/4, it suffices to have ..."

**Lemma conditions (§3.2, pp. 12–13).** Each lemma is quoted as printed.

- **Lemma 3** "(Polymath Type II)": "24ω + 7δ − 5γ < −2, 8ω + 3δ − γ < 0." CONFIRMED.
- **Lemma 4** "(Polymath Type I(ii))": "24ω + 7δ − 3γ < −1, 8ω + 3δ − γ < 0." The conditions are CONFIRMED. The title is DIFFERENT from the old note's label "Type IIb": the lemma title says "Type I(ii)", while Prop. 3 calls the corresponding condition "(C) Type IIb".
- **Lemma 5** "(Baker-Irving Type I)": "3γ − 12ω − 3δ > 1 if γ ≤ 1/2, 68ω + 14δ < 1 if γ ∈ (1/2, 1/2 + 2ω + ε]." CONFIRMED.
  - **Yes, $68\omega+14\delta<1$ appears**: in Lemma 5 (p. 13), again in its proof (p. 18: "Overall we thus have the desired equidistribution properties if 68ω + 14δ < 1 and 3γ − 12ω − 3δ > 1"), and as (4.5) "68ωmax + 14δ∗(γ) < 1" in the proof of Prop. 3 (p. 28).
- **Lemma 6** "(S. Type I)": "8ω + 4δ + 2γ < 1, 32ω + 10δ − γ < 0, 48ω + 16δ − 4γ < −1." The conditions are CONFIRMED. The title is DIFFERENT from the old note's "Type IIc (Stadlmann [6])": the lemma title says "S. Type I", its moduli set is called "DIIc", and Prop. 3 calls it "(D) Type IIc condition".
- **Lemma 7** "(Polymath Type III)": "28ω + 9γ + 8δ < 4." CONFIRMED.

Further facts from §3.2:
- Note after Lemma 3: "permissible (ω, γ, δ) are defined via strict inequalities."
- All moduli sets are subsets of "[1, x^{1/2+2ω}]".

**Prop. 3 global conditions (I)–(III), p. 26.** The fractions were badly garbled in extraction. Below they are **RECONSTRUCTED** from the proof on pp. 27–29, which shows the derivations.
- (I) Type I: $\min\{\xi_1-4A_n+\tfrac23,\ \tfrac97-\tfrac{34}{7}A_n\}-2\epsilon>\delta$.
  - The proof states "the assumption ξ1 − 4An + 2/3 − 2ϵ > δ ensures that δ∗(γ) ≥ δ".
  - The second term follows from $\delta^*=\tfrac1{14}-\tfrac{68}{14}\omega_{\max}-\epsilon$ with $\omega_{\max}=A_n-\tfrac14$. This is the 68ω+14δ<1 condition expressed in $A_n$.
- (II) Type II: "19/2 − 36An − 13δ + 100ϵ ≥ 0" and $\min\{\tfrac{\xi_2}{10}-\tfrac{32A_n}{10}+\tfrac{8}{10},\ \tfrac{\xi_2}{4}+\tfrac{11}{16}-3A_n\}-2\epsilon\ge\delta$.
  - The fractions are UNSURE character-for-character.
  - The second form matches Charton et al. §9.2, which quotes "δ < ξ2/4 + 11/16 − 3A1 − 2εa".
- (III) Type III: $\tfrac{11}{8}-\tfrac72A_n-\tfrac98\xi_3-2\epsilon>\delta$.
- In these conditions, $\epsilon=10^{-10}$ ("Let ϵ = 10−10").

**Largest $\omega$ allowed by Prop. 3: NOT STATED in the paper.**
- Prop. 3 has no explicit "$\omega\le\dots$" bound. $\omega$ enters only through $\omega(j,j')\le A_n-\tfrac14$ and conditions (I)–(III) in $A_n$.
- My computation from the reconstructed conditions, with $\delta=0.028$, $\xi=(0.38,0.4,0.4)$, $\epsilon\approx0$:

| Condition | Value at $A_n=0.253$ | Bound on $A_n$ | Bound on $\omega=A_n-1/4$ |
|---|---|---|---|
| (I) first term | $0.0347>0.028$ | $<0.25467$ | $<0.0047$ |
| (I) second term (= 68ω+14δ<1) | $0.0569$ | $<0.25894$ | $<0.0089$ |
| (II) first | $9.5-9.108-0.364=0.028\ge0$ | $\le0.25378$ | $\le0.0038$ |
| (II) min, first term | $0.0304$ | $\le0.25375$ | $\le0.0038$ |
| (II) min, second term | $0.0285$ | $\le0.25317$ | **$\le0.00317$** (binding) |
| (III) | $0.0395$ | $<0.25643$ | $<0.0064$ |

- So for Stadlmann's $\delta$ and $\xi$, the largest admissible value is $A_n\approx0.25317$, i.e. $\omega_{\max}\approx0.0032$. Stadlmann uses $A_1=0.253$, so $\omega_{\max}=0.003$.
- **This is my arithmetic on RECONSTRUCTED fractions, not a statement in the paper.**
- With $\omega=0.003$, $\delta=0.028$: $68\omega+14\delta=0.204+0.392=0.596<1$. So the 68ω condition is far from binding here; the binding constraint is Type II.

**Prop. 2 (minorant, p. 21–22): CONFIRMED.**
- Quote: "2ξ1 + 3ξ2 < 2, ξ2 ≤ ξ3 , ξ1 + 9ξ2 < 4, 2ξ1 + ξ2 > 1, 17ξ2 < 7."
- $c_2$: "c2 = 24 if ξ2 > 4/10, 0 if ξ2 ≤ 4/10".
- Quote: "(Note: If ξ2 ≤ 4/10, then ρ(n; x) is simply 1P (n).)"
- Prop. 2 property (3) gives the prime-factor exponent as "x^{1−2ξ2}". At $\xi_2=0.4$ that is $x^{0.2}$, and $0.2>\max_j B_{j,1}=0.15$.

## (e) Charton et al. — **CONFIRMED**, with one correction to the basis description

**Def. 4.1 "(Stadlmann support)" (§4.1, p. 4): CONFIRMED.**
> "Let k, n ∈ N, let δ, ε > 0, and let A = (A0 , A1 , . . . , An ) satisfy −ε = A0 < · · · < An < 1/2 − ε. Let B = (Bj,m ) be an n × ⌊1/δ⌋ matrix satisfying, whenever both sides are defined, δ < Bj,m ≤ Bj,m+1 ≤ Bj,m + δ, and set Bj,0 = 0 for every j. For t = (t1 , . . . , tk ), put S(t) = Σ ti , Rδ (t) = {i : ti > δ}, Mδ (t) = Σ_{i∈Rδ(t)} ti ."

- Then $T_k=\bigcup_{j=1}^n\{t\in[0,1]^k:\ A_{j-1}+\varepsilon\le S(t)<A_j+\varepsilon,\ M_\delta(t)\le B_{j,|R_\delta(t)|}\}$. This is the same set as Stadlmann's Def. 1.
- Lemma 4.2 "(Hereditary rough-mass bound)" proves the subset property.

**Def. 4.6 (Key integrals, p. 6): CONFIRMED.** $I$, $J$ and $K$ are identical to Stadlmann's Def. 5, including the same $K$ quirk. The hypothesis on $F$ is again "symmetric, square-integrable function supported on Tk".

**Prop. 4.7 (p. 6):** this is Stadlmann's Prop. 1 with the conclusion "Then DHL[k, 2] holds", criterion (4.1) "> 1".

**Thm 4.10 (p. 14): CONFIRMED.**
> "Theorem 4.10 (Direct-prime sieve criterion). Let T be a Stadlmann support, and suppose that 1P is equidistributed for every modulus generated by T . If a nonzero symmetric F ∈ L2 (T ) satisfies kJT (F ) > IT (F ), then DHL[k, 2] holds."

**Table 3 (§9.1, p. 39), "Exact parameter datum P": CONFIRMED.**

| quantity | physical | rescaled by 4 |
|---|---|---|
| k | 45 | 45 |
| ω | 7/1000 | – |
| (A0, A1) | (−1/125, 257/1000) | – |
| εs | 1/125 | – |
| δ | 41/2500 | g = 41/625 |
| B1,m, 1 ≤ m ≤ 10 | (1/5000)(777, 794, 875, 917, 953, 983, 1016, 1042, 1063, 1081) | C(m) = 4B1,m |
| B1,m, m ≥ 11 | 1081/5000 | C(m) = 1081/1250 |
| (ξ1, ξ2, ξ3) | (19/50, 2/5, 2/5) | – |
| εa | 10^−10 | – |

- **The /5000 denominator is CONFIRMED.**
  - The extraction shows "1/5000 (777, ...)" as a stacked prefactor.
  - The $m\ge11$ entry, "1081/5000", is explicit.
  - Table 4 independently checks it: "Definition 1: B3 ≤ B2 + δ | 7/40 | 438/2500 | 1/5000". Here $875/5000=7/40$ and $(794+82)/5000=438/2500$.
  - Table 4 also has "First-rung cap wall 777/5000".
- $n=1$. $\omega=7/1000=A_1-\tfrac14$, consistent with Stadlmann's $\omega(j,j')$.
- Support as written on p. 39: "T = { t ∈ [0, ∞)^45 : Σ ti < 53/200, Σ_{ti>δ} ti ≤ B1,#{i:ti>δ} }".
- Marginal cutoff, quote: "The marginal cutoff is A1 − εs = 249/1000."
- Rescaled values (§9.3): "L = 53/50, τ = 249/250, g = 41/625, C(m) = 4B1,m". Also: "the physical threshold 1 is exactly the rescaled threshold 4."
- **Internal inconsistency in the draft, CONFIRMED.**
  - Lemma 9.1 (p. 41) says the dilation "sends the two physical rough caps to C(1) = C(2) = 31/50 and C(s) = 17/25 for s ≥ 3".
  - That corresponds to $B=0.155$ and $0.17$ with only two distinct caps, which contradicts Table 3's ten-step caps (e.g. $C(1)=4\cdot777/5000=0.6216$).
  - Lemma 9.1 looks like a leftover from an earlier parameter set.

**Basis and dimension (§11, p. 42): CONFIRMED, with a correction.**
> "We use the symmetric space of degree 21 generated by products of even power sums and powers of the remaining simplex radius."

> "if λ = (λ1 , . . . , λr ) is a partition all of whose parts are positive and even, write |λ| = λ1 + · · · + λr and Pλ = ∏_{j=1}^r Pλj , with P∅ = 1. We use the space B21 = spanQ {(L − P1 )^a Pλ : a ≥ 0, λj ∈ 2Z>0 , a + |λ| ≤ 21}."

> "After repeated monomials are identified, the displayed family has dimension 846."

- Correction to the old note: $P_\lambda$ here is a **product of power sums**, with $P_j(x)=\sum_{i=1}^{45}x_i^j$ (§9.4, p. 41). It is not Polymath's monomial-symmetric $P_\alpha$. The span condition "λ even parts, a+|λ| ≤ 21" is as the old note says.

**Certified ratio: CONFIRMED.**
- Thm 11.1 (p. 43): "the supported function F⋆ = 1_T̃ P⋆ satisfies JT (F⋆ ) / IT (F⋆ ) = 4.00438409833460131937 . . . > 4."
- The same number appears in the Introduction (p. 2) as "v^T JT v / v^T IT v".
- In §9.4 the rescaled $J_T$ includes the factor $k$: "JT (F ) = 45 ∫_T̂ ( ∫_0^{U(x̂)} F (x̂, u) du )^2 dx̂".
  - The fiber endpoint is "U(x̂) = min{L − S, max{g, C(s + 1) − ρ1}}".
  - The base is "T̂ = {x̂ : S ≤ τ, ρ1 ≤ C(s)}".
  - So the base carries the cap constraint explicitly, which is consistent with $F$ being supported on $T$.
- The certificate coefficients are not printed in the visible text. The paper says "the exact rational coefficient vector used in the certificate".

## Number of bands in the final choice
- **Stadlmann:** $n=1$. "A = (−ε, 0.253)" (p. 34); $B$ is a single row "B = (B1,1 , . . . , B1,⌊1/δ⌋ )".
- **Charton et al.:** $n=1$. "(A0 , A1 ) = (−1/125, 257/1000)"; the caps are $B_{1,m}$ only (Table 3).
- Neither paper uses more than one band in its final parameters. The general $n>1$ machinery is only stated, and Stadlmann says in §6.2 that the general results were developed "with the intend of proving better bounds on H1".

## Corrections to sources-enlarged-supports.md
1. §2(d) "D=19": the paper is inconsistent. §5.1 says B19, while the abstract area and §1.1 say degree ≤ 21 (three times).
2. §2(c) lemma labels: Lemma 4 is titled "Polymath Type I(ii)" (Prop. 3 calls it Type IIb), and Lemma 6 is titled "S. Type I" (moduli set DIIc, Prop. 3 calls it Type IIc). The inequalities are all correct.
3. §2(b) $K$ domain: confirmed as transcribed, so the UNSURE flag can be dropped.
4. §3 basis: $P_\lambda$ is a product of power sums $P_j=\sum x_i^j$, not a monomial symmetric polynomial.
5. §3 "/5000": confirmed. The Lemma 9.1 inconsistency is confirmed.
6. §2(d) $\omega_{\max}=0.003$: consistent with the paper ("ωmax ≤ An − 1/4"). By my reconstruction, the Prop. 3 Type II condition caps $A_n$ at about 0.2532 for $\delta=0.028$, $\xi_2=0.4$.
