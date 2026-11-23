# Route card: the Kátai / Bourgain–Sarnak–Ziegler criterion for λ along shifted primes (23 Nov 2026, Session 46)

**Classification: refuted as a route in the criterion's classical form (bounded prime range): its hypothesis, for the
normalised weight, needs right-order Hardy–Littlewood asymptotics for binary pairs of forms p₁m − 2, p₂m − 2 (most
pairs p₁ ≠ p₂ in a dyadic-type range P_j with p ≳ τ^{−3/2}), each individually open, so the reduction runs in the
wrong direction. Located in the growing-range form: the first unresolved
implication is an averaged second moment over a polylog-size DILATION family (Finding 5), for which we know no result.
Elementary; possibly folklore; finite-X data only. Fresh-context adversarial audit: 2 errors, 2 gaps, 4 slips, all
fixed below (see the end).**
Not in the parity paper (v1.0.1 frozen). No progress on twin primes and no way around parity.

Mechanism (genuinely new for this programme: no earlier card uses an orthogonality criterion of Kátai type). The
target Σ_{p ≤ x} λ(p + 2) = o(π(x)) is a "Chowla along primes" statement of the kind Lü–Wang–Wu claim for μ
(notes/sources-lww26.md). Kátai's criterion and its quantitative form by Bourgain–Sarnak–Ziegler prove
Σ ν(n) F(n) = o(N) for EVERY bounded multiplicative ν from a hypothesis on F alone (correlations F(p₁m) F(p₂m)), with no
Type I / Type II input on ν. Question: does it give the target with F(n) = Λ(n − 2)?

## Source (Literature, read)
Bourgain, Sarnak, Ziegler, "Disjointness of Moebius from horocycle flows", arXiv:1110.0992v1 (PDF SHA-256
dee51b51d4d7957737547807feec308d5eae9352a7d2c26568da3f2974c8c44a; not committed), Theorem 2 and Section 2 (proof:
covering of [1, N] by sets S_j of integers with a unique prime factor in P_j = primes in [(1+α)^j, (1+α)^{j+1}],
j₀ ≤ j ≤ j₁ bounded in terms of τ; then multiplicativity and Cauchy's inequality). Theorem 2 as stated: F : N → C with
|F| ≤ 1, ν multiplicative with |ν| ≤ 1, τ > 0 small; if for all primes p₁ ≠ p₂ ≤ e^{1/τ},
|Σ_{m ≤ M} F(p₁m) conj F(p₂m)| ≤ τ M for M large, then |Σ_{n ≤ N} ν(n) F(n)| ≤ 2 √(τ log 1/τ) N for N large. Note 2 there
allows a small exceptional set of pairs, and p. 13 adds: "One can certainly allow a finite number of exceptions
(independent of N) in Theorem 2, in fact the proof only involves the condition for primes p ≥ D0 which gets large as τ
gets small" (D₀ = (1 + α)^{j₀}, j₀ = α^{−1} log(1/α)^3, so p ≳ τ^{−3/2} up to logarithms; only pairs in the same
P_j are used). (Kátai 1986 and Daboussi–Delange are cited through BSZ and the search
results; not opened.)
Literature check (search scope: one web search, 23 Nov, for Kátai/BSZ applied to shifted primes or sparse sequences):
found Bergelson–Kułaga-Przymus–Lemańczyk–Richter arXiv:1705.07322 (a generalisation of the criterion) and applications
to automatic / q-semimultiplicative sequences; nothing on F = indicator of shifted primes. Not exhaustive.

## Criteria (fixed before the computation)
- Success: the criterion's hypothesis for a normalised mean-zero version of F(n) = Λ(n − 2) reduces to known inputs
  (Bombieri–Vinogradov, Siegel–Walfisz, or a known averaged Hardy–Littlewood theorem).
- No-go: the hypothesis implies, for some fixed pair (p₁, p₂), an individual binary prime-pair statement (beyond sieve
  methods by the parity phenomenon).

## Findings
Setting: F(n) = log(n − 2) if n − 2 is prime, else 0 (so Σ_{n ≤ x} F(n) ~ x); target T(x) = Σ_{n ≤ x} λ(n) F(n), and
T(x) = o(x) ⇔ Σ_{p ≤ x} λ(p + 2) = o(π(x)) (partial summation).

1. **The classical statement is trivial here (Proved here, immediate).** Theorem 2 needs |F| ≤ 1. Applied to F/log N it
   bounds |Σ λ F/log x| by 2√(τ log 1/τ) N, while trivially |Σ λ F/log x| ≤ π(N) = o(N). Any use for the target must
   work with the normalised, unbounded F (|F| ≤ log N), i.e. re-run the proof for a sparse weight.
2. **The hypothesis fails for F itself (Computed, finite X; conjecturally exact).** (1/M) Σ_{m ≤ M} F(p₁m) F(p₂m)
   tends (conjecturally, Hardy–Littlewood for the pair of forms p₁m − 2, p₂m − 2) to a positive singular-series
   constant for every admissible pair, not to 0. At X = 1e8 (M = X/max(p₁, p₂)): 3.520 for (3, 5), 3.165 (3, 7),
   2.112 (5, 7), 1.597 (11, 13), 2.817 (31, 37). So F must be replaced by a mean-zero F₀ = F − G with a model G.
3. **For F₀ the hypothesis IS the Hardy–Littlewood asymptotic (Proved here, elementary; folklore in substance).** Take
   G(n) = (W/φ(W)) 1[(n − 2, W) = 1] (W = ∏_{p ≤ w} p, the W-trick model; here w = 13). Then
   Σ λ F = Σ λ F₀ + Σ λ G, and Σ_{n ≤ x} λ(n) G(n) = o(x) is known for each fixed w (G is W-periodic; λ is completely
   multiplicative, so non-coprime classes reduce to coprime ones, and Σ λ χ = o(x) since L(s, χ) ≠ 0 on Re s = 1).
   Expanding Σ F₀(p₁m) F₀(p₂m) = Σ FF − Σ FG − Σ GF + Σ GG: the GG term is a periodic average (C_mod), and the cross
   terms are prime sums in residue classes to the fixed modulus p₁p₂W (Siegel–Walfisz). Since F(p_i m) already "sees"
   the prime p_i (p_i m − 2 is prime to p_i), Σ F(p₁m) G(p₂m) ≈ C_mod · p₁/(p₁ − 1) when p₁ > w (and ≈ C_mod when
   p₁ ≤ w). Hence, for p₁, p₂ > w,
   C₀ = C_raw − C_mod (p₁/(p₁ − 1) + p₂/(p₂ − 1) − 1)  (and C₀ = C_raw − C_mod for p₁, p₂ ≤ w).
   Data at 1e8 confirm this: (17, 19): 1.4931 − 1.3441 · 1.1181 = −0.0097 against C₀ = −0.0098; (23, 29), (31, 37) agree
   within 0.004. So |C₀| ≤ τ is the Hardy–Littlewood asymptotic Σ_{m ≤ M} Λ(p₁m − 2) Λ(p₂m − 2) = (𝔖 + O(τ)) M only
   if the model is fine enough: the truncated singular series differs from the true one by about 1/w, so one needs
   w = w(τ) → ∞ (e.g. w ≥ e^{1/τ}); each fixed w is allowed, since Σ λ G_w = o(x) for each w. With that choice,
   (1.3) for F₀ is equivalent, up to O(τ), to right-order Hardy–Littlewood for the pair. (Proved here, elementary,
   after the audit's corrections; folklore in substance.) Data at 1e8 for p₁, p₂ ≤ w = 13: C₀ = −0.063 (3, 5),
   −0.037 (5, 7), −0.034 (11, 13) (finite-X and w-truncation effects; they prove nothing).
   **No-go criterion met** (as a statement about the NECESSARY input of any BSZ-type argument for this F; the
   classical theorem itself does not apply, Finding 1): for fixed small τ the proof uses (1.3) only for pairs in the
   same P_j with p ≳ τ^{−3/2}, and Note 2 lets any finite set of pairs fail; but (1.3) must hold for all but a small
   proportion of the pairs in each P_j. So for some (indeed most) fixed pairs p₁ ≠ p₂ in that range one needs
   Σ_{m ≤ M} Λ(p₁m − 2) Λ(p₂m − 2) ≥ (𝔖(p₁, p₂) − O(τ)) M, an individual binary statement with the right constant,
   open and of twin-prime type (the parity phenomenon blocks such asymptotics for sieve methods; standard, not
   re-proved here). Caution: the forms p m − 2, p ∈ P_j, form an admissible tuple, so Maynard's theorem for linear
   forms already gives SOME pair infinitely often prime; what is out of reach is the asymptotic / right-order lower
   bound for most pairs. The criterion trades a parity-sensitive statement about λ for parity-insensitive but
   individually open Hardy–Littlewood asymptotics: the wrong direction.
4. **Sparseness forces a growing prime range (Heuristic outline; not proved).** In the Cauchy–Schwarz step,
   |Σ_{p ∈ P_j} Σ_m ν(p) ν(m) F(pm)|² ≤ M_j Σ_m |Σ_{p ∈ P_j} F(pm)|²; for unbounded F the diagonal p₁ = p₂ is
   Σ_p Σ_m F(pm)² ≈ |P_j| M_j log N (Computed: (1/M) Σ F(pm)² / log X = 1.42, 1.18, 1.10, 1.04, 1.02 for p = 3, 5, 7, 11, 13
   at 1e8, ≈ (p/(p − 1))(1 − 1/log X) to four digits), against the trivial size |P_j| M_j of the sum. So the diagonal alone costs a relative
   √(log N / |P_j|), and the method needs prime ranges with |P_j| ≫ log N, i.e. primes up to at least
   log N · log log N (we write (log N)^{1+ε}),
   with BSZ's bounded j₁ replaced by one growing with N. The covering steps (2.3)–(2.10) of BSZ would also have to be
   redone along the sparse set (upper-bound sieve on n − 2 prime); plausible for slowly growing ranges, not checked.
5. **Averaging over the pairs (first unresolved implication).** With P = (log N)^{1+ε} the hypothesis may fail for a
   small set of pairs (Note 2), so what is really needed is the averaged statement
   Σ_m |Σ_{p ∈ P_j} F₀(pm)|² = o(|P_j|² M_j), a second moment of r_j(m) = Σ_{p ∈ P_j} Λ(pm − 2) about its model over a
   polylog-size family of DILATIONS (pairs of forms p₁m − 2, p₂m − 2). The averaged Hardy–Littlewood theorems used in
   earlier cards (Matomäki–Radziwiłł–Tao, Lichtman–Teräväinen; Sessions 29, 30) average over SHIFTS h in long ranges;
   the dilation family is different and much smaller (≈ (log N)^{2+2ε} pairs, up to log log factors). Exploration
   (code/explore/dilation_second_moment.py, notes/explorations.md, Session 46): the pair-averaged C₀ over the 136 pairs
   of primes in [3, 61] shrinks as w grows, consistent with Hardy–Littlewood plus w-truncation (finite X; proves
   nothing). We know of no result giving this second
   moment (not searched beyond the scope above); whether it is itself parity-blocked is open here.

## Honest summary
The Kátai–BSZ criterion removes all Type I / Type II work on λ, but for the shifted-prime weight it moves the whole
difficulty into binary prime correlations along dilations: individually twin-prime-type (classical form: no-go), on
average an unstudied dilation second moment (growing-range form: located). Nothing here bears on twin primes beyond
that location.

Files: code/parity/katai_dilation.py [X] (/usr/bin/python3 -I; ~40 s at 1e8, ~4 GB; λ self-checked against trial
division), output code/parity/katai_dilation.out (X = 1e8; also Σ_{p ≤ 1e8} λ(p + 2) = −299, π = 5761455).

## Audit (fresh-context adversarial helper, Session 46)
1 gap (Note 2 under-quoted: the proof uses only pairs in one P_j with p ≥ D₀) — fixed. 2 error (the no-go was argued
from the fixed pair (3, 5), which may be exceptional; correct argument: most pairs in P_j need right-order HL) — fixed,
with the Maynard caution added. 3 error (the cross terms differ from the GG term when p_i > w; the stated equivalence
"(𝔖_w + o_{w→∞}(1))" with w = 13 fixed was incoherent) — replaced by the exact relation, checked against the data, and
w = w(τ) → ∞. 4 slip (C_raw − C_mod quoted instead of C₀ for p > w) — fixed. 5 gap (the classical theorem does not
apply to F₀ at all; the no-go is about the necessary input) — fixed in wording. 6, 7, 9, 12 fine (7: "Hecke" dropped).
8 slip (diagonal factor (p/(p − 1))(1 − 1/log X)) — fixed. 10 slip (header) — fixed. 11 slip (pair count up to log log
factors) — fixed. The audit's checks were re-done here on the source text (bsz.txt p. 13) and on the .out numbers.
