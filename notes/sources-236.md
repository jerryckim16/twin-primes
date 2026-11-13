# Source notes: the two 2026 preprints claiming $H_1\le236$ ($k=48$)

Compiled 2026-11-12. Nothing here is a new result.
- **Q:** marks a verbatim (or near-verbatim, from `pdftotext`) quote from the source.
- **Mine:** marks my own reading, rescaling or arithmetic. Check it before citing.
- "not found" means I looked and the source does not say it, or I could not open the source.

Format and notation follow `notes/sources-enlarged-supports.md` §2 (Stadlmann arXiv:2608.31126). The target format is
`code/to_ucoords.py`: $k$, $L$, $\tau$, $g$, caps $C_m$, basis, coeffs, in Polymath scaling $u=4t$, threshold $kJ/I>4$.

---------------------------------------------------------------------------------------------
## 1. Z. Song, S. Yue, "Bounded Gaps Between Primes: An Upper Bound of 236", IACR ePrint 2026/1893

### Status: full text NOT obtained
What I tried:
1. WebFetch of `https://eprint.iacr.org/2026/1893` worked for the abstract page only.
2. `curl -L https://eprint.iacr.org/2026/1893.pdf` into `/tmp/claude-0/src236/song/` returned a Cloudflare "Just a moment..."
   HTML challenge page, not a PDF. The file was not opened further.
3. WebFetch of `https://eprint.iacr.org/2026/1893.pdf` returned HTTP 403.
4. WebFetch of `https://eprint.iacr.org/archive/versions/2026/1893` returned HTTP 403.
5. WebSearch found no arXiv copy, no GitHub repository and no other mirror.

I did not try to get around the block.

### What is known (from the ePrint abstract page and the IACR news item 29506)
- Authors: Zhao Song and Song Yue. Song Yue's affiliation is listed as Northeastern University.
- Dates: received 2026-09-04, approved 2026-09-09. Category Foundations, "Preprint.", licence CC BY-NC 4.0.
- Only one history entry is shown.
- Abstract (summarised; the fetch tool would not reproduce it in full):
  - It reviews Zhang, then Maynard's 600, Polymath's 246 and Stadlmann's 240.
  - It ends **Q:** "In this paper, we prove $H\_1\leq236$."
- A WebSearch summary (secondary, NOT verified against the paper) says the authors "reduce the number of shifts from 49 to
  48". That would mean $k=48$, consistent with $H(48)=236$.

### Everything else: **not found**
The paper's content could not be read, so none of the following is known:
- the criterion;
- the support and its parameters ($\varepsilon$, $A$, $\delta$, caps);
- the level-of-distribution parameters and the equidistribution input;
- the test function and its basis;
- the claimed ratio;
- its relation to Stadlmann or Charton et al.;
- any errata.

No later version, critique or code repository was found. MathWorld's bounded-gaps table (checked 2026-11-12, "as of Sep. 7,
2026") does not list Song–Yue.

---------------------------------------------------------------------------------------------
## 2. S. Kintali, "Improved Bounded Gaps Between Primes", preprint dated September 1, 2026
- PDF: `https://shivakintali.github.io/papers/Prime-Gaps.pdf` (11 pp.). Downloaded to `/tmp/claude-0/src236/kintali/k.pdf` and read
  with `pdftotext` only.
- It is not on arXiv as far as I found.
- Homepage entry: **Q:** "Improved Bounded Gaps Between Primes. H1 <= 236." **Q:** "Sep 1, 2026: Building upon Julia Stadlmann's ideas,
  I proved H1 <= 236 using AI."
- AI-use statement, p. 1: Claude, ChatGPT and two open-weight models were used. **Q:** "The code was written by Codex and verified by the
  author."

### 2(a) Main claim (p. 1, Thm 1; proof §7, p. 10)
- **Q:** "Theorem 1 (Main theorem). H1 ≤ 236."
- The paper certifies three premises:
  - **Q:** "1. a legal one-band D182 support for k = 48, with Stadlmann's Type-IIc range empty;"
  - **Q:** "2. an exact rational variational certificate 48J(F)/I(F) = 1.000774701187468444763475111497864 . . . > 1;"
  - **Q:** "3. an explicit admissible 48-tuple of diameter 236."
- **$k=48$, $H=236$.** The tuple is given in Lemma 6, §7, p. 9:
  `{0,6,8,14,18,24,26,48,50,54,56,60,66,68,74,78,80,84,90,96,98,104,110,116,120,126,134,138,144,150,158,164,168,176,180,186,188,194,200,204,206,210,216,224,228,230,234,236}`.
  - Omitted residues $a_p$ for $p\le47$: 2:1, 3:1, 5:2, 7:2, 11:9, 13:10, 17:4, 19:13, 23:13, 29:15, 31:1, 37:7, 41:10, 43:2, 47:5.
  - Prop 7 also claims $H(48)=236$ by exhaustive search. The paper says this is not needed for the bound.

### 2(b) Criterion (p. 2)
- It is Stadlmann's Prop. 1 with $c_1=c_2=0$ and one band.
- **Q:** "In the prime-indicator specialization c1 = c2 = 0, and for the one-band support used here, the positivity criterion is exactly
  $kJ(F)/I(F) > 1$, $I(F)=\int_{\mathbb R^k_{\ge0}} F(t)^2dt$, and $J(F)=\int_{x\in\mathbb R^{k-1}_{\ge0},\ |x|_1\le A_1-\varepsilon}\big(\int_0^\infty F(x,t)\,dt\big)^2dx$."
- **Q:** "The integrands are extended by zero outside the support."
- The criterion is applied in Stadlmann's scaling ($t=\log_x d$, quarter scale), with threshold 1.

### 2(c) Support "D182" (§2, pp. 2–3)
- **Q:** "$\varepsilon = 3/400$, $A = 253/1000$, $U = A+\varepsilon = 521/2000$, $L = A-\varepsilon = 491/2000$"
  - **Note:** the paper's "L" is the *marginal base cutoff*, not our support $L$.
- **Q:** "$\delta = 91/5000 = 0.0182$, $B_0 := 0$, $B_m = 1899/10000 = 0.1899$ $(1 \le m \le 54)$. Here $54=\lfloor1/\delta\rfloor$. In
  Stadlmann's band notation this is n = 1, A0 = −ε, and A1 = A."
- **Q:** "$T = \{ t\in\mathbb R^{48}_{\ge0} : |t|_1 < U,\ R_\delta(t) := \sum_{i:t_i>\delta} t_i \le B_{\#\{i:t_i>\delta\}}\}$."
  - So the cap is **uniform in $m$**.
  - The paper notes $B_0=0$ as a "zero-group convention" filling a gap in Stadlmann's Def. 1 (p. 4).
- Stadlmann's monotonicity conditions (p. 4): **Q:** "δ < Bm, and Bm ≤ Bm+1 ≤ Bm + δ whenever both columns are defined. The first
  inequality has margin 1717/10000".
- Fibre geometry for $J$ (§6, eq. (6.1)), with $S=|x|_1$, $r=\#\{i:x_i>\delta\}$, $R=\sum_{x_i>\delta}x_i$ and $H=U-S$:
  - **Q:** "If R ≤ Br, the allowed endpoint of the last-coordinate fiber is h(x) = min{H, max{δ, Br+1 − R}}."
  - **Q:** "If R > Br, the base is illegal and the capped marginal is zero."
  - **Q:** "r ≤ 10".

**Mine: translation to `to_ucoords.py` format** ($u=4t$, threshold 4):

| quantity | value |
|---|---|
| $k$ | 48 |
| $L=4U$ | $521/500=1.042$ |
| $\tau=4(A-\varepsilon)$ | $491/500=0.982$ |
| $g=4\delta$ | $91/1250=0.0728$ |
| $C_m=4B_m$ | $1899/2500=0.7596$ for every $m\ge1$, so caps = {"1": 1899/2500, "2": 1899/2500, "3+": 1899/2500} |

- $L$ and $\tau$ are **identical to Stadlmann's** §6.2 choice.
- The differences from Stadlmann are:
  - $k$ is 48 instead of 49;
  - $\delta$ is 0.0182 instead of 0.028;
  - the cap is a single 0.1899 instead of 0.15/0.15/0.17.
- In Polymath scale Stadlmann's caps are 0.6/0.6/0.68 with $g=0.112$. Kintali's support is a smaller $g$ with a larger, uniform cap.
- The format fits directly. The coordinate threshold uses strict $t_i>\delta$.
- §4 (p. 7) says **Q:** "the cap removes 0.000109694616131920316502022095467 . . . of the denominator energy" (i.e. $I/I_0=0.99989\ldots$).

### 2(d) Level of distribution / equidistribution (pp. 2–5)
- No new estimate is proved.
- **Q:** "No conjectural distribution hypothesis is assumed; the precise imported analytic results and five source-level corrections are
  stated below."
- The input is Stadlmann's Prop. 3, Type I/IIa/IIb/III branches, with Bombieri–Vinogradov below $x^{1/2}$.
- **Q:** "ω = (A+A)/2 − 1/4 = 3/1000". The Type IIc branch is made empty and is not used:
  - **Q:** "γlo = ξ2 − η = 0.3999999999";
  - **Q:** "γIIc,hi = 1/3 + 8ω + 7δ/3 + 3η = 0.3998000003".
  - IIb covers $\gamma$ below $\tau_{II}=2/5+24\omega/5+7\delta/5+2\eta=0.4398800002$, and IIa covers the rest.
- Minorant: **Q:** "(ξ1, ξ2, ξ3) = (19/50, 2/5, 2/5), η = 10^{−10}". This gives $\rho=1_{\mathbb P}$ and $c_1=c_2=0$.
  - **Q:** "roughness exponent is β = 1 − 2ξ2 = 1/5 > B1" (margin 101/10000).
- Global inequality margins (table, p. 4): I1 246999997/15000000000, I2 1352999993/35000000000, II0 15540001/100000000,
  II1 60999999/5000000000, II2 51499999/5000000000, III 106499999/5000000000.
  - The formula column was garbled in extraction, so I cannot confirm the expressions.
- Tuple-partition table: p. 4.
- No $\varpi$ or $\theta$ parameters appear; the level is $1/2+2\omega$ in Stadlmann's sense.
- Claimed defect in Stadlmann v1 (p. 2): **Q:** "The source also has a literal Type-IIc defect: its displayed condition permits ω0 < 0 while
  requiring a nonnegative subset sum to be at most 8ω0 < 0. The construction below neither repairs nor uses that case."
- Only two of the "five source-level corrections" are clearly identified in the text: the $B_{j,0}=0$ convention and the Type IIc
  defect. The other three were **not found** explicitly.

### 2(e) Test function (§3, pp. 5–6)
- **Q:** "The coefficient file contains 1,295 exact triples (a, α, c_{a,α}), with a ≥ 0 and a + |α| ≤ 25. It is byte-identical to the public
  AxiomMath PrimeGapsLib witness at commit 1faa7b14...b106477."
  - The full hash is in ref. [10]: `1faa7b14e82ddebc2772dfb9153922f01b106477`.
- **Q:** "$P(z)=\sum_{a,\alpha} c_{a,\alpha}\,(26/25 - |z|_1)^a\, m_\alpha(z)$". Here $m_\alpha$ is the **monomial** symmetric polynomial,
  with $\alpha$ "a partition ... of positive integers".
- **Q:** "Put z = (26/(25U))t, let PU(t) = P(z), and define F(t) = PU(t)1T(t)."
- **Q:** "The provenance and scaling audit reproduces the public k = 50 certificate."
  - **Mine:** the witness looks like the Axiom PrimeGapsLib reproduction of Polymath's $M_{50,1/25}$ certificate. The repo's README
    mentions `PrimeGapsTheory.Gap246.Endgame.Main`, and $26/25=1+\varepsilon$ with $\varepsilon=1/25$.
  - It is reused unchanged as a test function at $k=48$, rescaled to the D182 support. The coefficients were **not re-optimised**.
- Degree $\le25$, 1,295 terms. **Q:** "The 272 marginal signatures give 272 · 273/2 = 37,128 unordered products and 7,338 distinct output
  signatures."
- Whether $\alpha$ is restricted to even parts: **not found** in Kintali.
- **Mine:** in $u=4t$ coordinates, $z=26u/(25L)$ with $L=1.042$, so
  $F\propto\sum c_{a,\alpha}(26/(25L))^{a+|\alpha|}(L-|u|_1)^a m_\alpha(u)$.
  - Our evaluator basis uses products of **power sums** $P_j$, not monomial symmetric $m_\alpha$.
  - Converting $m_\alpha\to$ power-sum products is exact but $k$-dependent. It is needed before feeding this witness to
    `capped_exact.py`, or the evaluator must accept $m_\alpha$.

### 2(f) Claimed values
| quantity | value | reference |
|---|---|---|
| Cap-free $q_0=48J_0/I_0$ (support $\lvert t\rvert<U$, base $\le0.2455$) | $1.000908704175987505707537332488725\ldots$ | p. 6 |
| $I/I_0$ | $0.999890305383868079683497977904532\ldots$ | Prop 4 |
| $J/J_0$ | $0.999756438739933773404567680738685\ldots$ | Prop 5 |
| **Final $48J(F)/I(F)$** | $N/D=1.000774701187468444763475111497864\ldots$ | Prop 5 |

- In Polymath scale the final ratio is $4.0031\ldots$ against threshold 4 (Mine: $\times4$).
- Exact $N$ and $D$ are not printed; they are said to be in the repo artifacts.
- **Q:** "The combined capped-J artifact has SHA-256 07267dbc5c6c26aa95444d70aed77f62132fe4b7eb516e11b33496b4c8d5459d".
- §5 (p. 7) records a failed Cauchy–Schwarz lower bound of $0.9628\ldots$. The paper says it is not used in the proof.
- Lemma 3 (p. 6) argues that the cap-face discontinuities are harmless (approximation, citing Lemma 1 of Stadlmann).

### 2(g) Relation to Stadlmann / Charton et al.
- It is explicitly an extension of Stadlmann v1 ("computer-assisted extension of Stadlmann's recent GPY/Maynard–Tao framework").
- It uses the same one-band Def. 1 support, Prop. 1 criterion and Prop. 3 equidistribution. The changes are listed in 2(c), plus
  the parameter choice that empties Type IIc.
- On Stadlmann's numerics, Kintali says (p. 2): **Q:** "Version 1 does not supply the final matrices, rational vector, quotient, or code,
  so that numerical claim is not reproducible from the arXiv bundle alone."
- Charton et al. (212) is not cited. The only Axiom link is the reused PrimeGapsLib witness (ref. [10]).

### 2(h) Repository, versions, critiques, oddities
- Code and data: **Q:** "The required files are file are in the directory comutation/ in the public github repository
  github.com/shivakintali/Prime-Gaps". The directory is actually `computation/`.
  - WebFetch of the GitHub page shows 2 commits, no README and no description.
  - Files include `run_D182_uniform.sh`, `compute_one_band_capped_I.py`, `compute_one_band_capped_J_correction.py`,
    `combine_capped_{I,J}.py`, `capped_I_d182.{0..7,complete}.json`, `capped_Jcorr_d182.{0..7,complete}.json`,
    `general_simplex_U2605_L2455.json`, `allsmall_J_enlarged.json` and `exact_axiom_general_simplex.py`.
  - `gh api` access to the repo was refused in this session, so the files were not read.
- Section numbering jumps from §7 to §10 (no §8–9) in the PDF I read. The PDF's front matter shows no version number.
- MathWorld (as of Sep 7, 2026) lists "236, Sep. 1, 2026, Kintali (2026)" with **Q (paraphrased by fetch tool):** "The author checked the
  exact-arithmetic programs. Analytic inputs are imported from the literature."
  - MathWorld reports no independent verification.
- Published critique: **not found**. Later version: **not found**. The homepage shows only the Sep 1 entry.

---------------------------------------------------------------------------------------------
## 3. Side-by-side (Polymath scale $u=4t$, threshold 4) — Mine
| source | k | L | tau | g | caps $C_m$ | test fn | claimed ratio |
|---|---|---|---|---|---|---|---|
| Stadlmann §6.2 | 49 | 1.042 | 0.982 | 0.112 | 0.6, 0.6, 0.68 ($m\ge3$) | $\mathcal B_{19}$, not published | ">4", no value |
| Kintali D182 | 48 | 521/500 | 491/500 | 91/1250 | 1899/2500 for all $m$ | Axiom $k{=}50$ witness, 1295 terms, deg $\le25$, $m_\alpha$ basis | $4\times1.0007747\ldots$ |
| Song–Yue | 48 (per search snippet only) | not found | not found | not found | not found | not found | not found |

**Sources:**
- https://shivakintali.github.io/papers/Prime-Gaps.pdf
- https://shivakintali.github.io/
- https://github.com/shivakintali/Prime-Gaps
- https://github.com/AxiomMath/PrimeGapsLib
- https://eprint.iacr.org/2026/1893
- https://iacr.org/news/item/29506
- https://mathworld.wolfram.com/BoundedGapsBetweenPrimes.html
