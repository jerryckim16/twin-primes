# Audit: parity-barrier v0.13, Section `subsec:gowers` (and the end of Remark `rem:mr16-transfer`)

File audited: `papers/parity-barrier/main.tex`, lines 355-447 (Remark `rem:mr16-transfer`,
the `subsec:gowers` Literature paragraph, Proposition `prop:gowers-blind` and its proof, and Remark `rem:gowers`).
Sources checked: `/tmp/claude-0/src/{math_0606088,0807.1736,1509.05422,1605.04628}.txt`.
Checks: `/tmp/claude-0/audit/check.py` (exact expectation over all sign choices, d = 1, 2 with
N = 4d..4d+6, L = 2..5, both f_+ and f_-; analytic expectation for d = 3, N = 12..14, L in {2,3,4,7}),
`/tmp/claude-0/audit/localU1.py` (local U^1 and local Fourier norms of the block functions).

Verdict on the Proposition: **correct as stated, including every constant.** The errors are in
Remark `rem:gowers` (one false claim about the block functions, one misattribution of the k = 2 mechanism)
and in some page references.

---

## Errors

**E1. Remark `rem:gowers`: "The block functions above have local U^1 norm about 1 on intervals shorter than L, so they are not counterexamples there." This is false.**
- For f_+, inside a block f(n) = eps_{(b, n mod 2)}, so on a short interval the average is about (eps_{b,0}+eps_{b,1})/2. That is 0 for half the blocks and +-1 for the other half. The mean local U^1 norm is about 1/2, not 1. Measured at N = 32768, L = 64: 0.485, 0.477 and 0.462 for H = 8, 16, 32.
- For f_-, f(n) = (-1)^{floor(n/2)} eps_{(b, n mod 2)}, and its sum over any interval is O(1). So **f_- is locally U^1-uniform**: the mean local U^1 norm is 0.014 for H = 8, 16 and 32. Yet its shift-2 correlation is about -1. So f_- *is* a counterexample to "local U^1 uniformity alone controls the shift-2 correlation". This does not contradict Tao, because his argument also uses multiplicativity and more than U^1 (see E2).
- What does keep the block functions out of Tao's regime is local *Fourier* (local U^2) structure. Both functions correlate with e(n/4) or with a constant on every short interval. The mean local sup_alpha |avg f e(alpha n)| is 0.98 for f_+ and 0.72 for f_- at H = 8, and 0.90 and 0.66 at H = 32.
- **Fix:** replace the sentence with: "On intervals shorter than L the block functions are far from locally Fourier-uniform: f_+ has local U^1 norm about 1/2 on average, and f_- has local U^1 norm O(1/H) but correlates with e(n/4) on every block. So f_- is locally U^1-uniform with shift-2 correlation near -1. Local U^1 uniformity alone does not give the two-point case, and Tao's argument also uses multiplicativity (see below)." This strengthens the remark's own point.

**E2. Remark `rem:gowers`: "the k-point case needs only U^{k-1} [Tao16b, Thm 1.8, Remark 3.4, pp. 5, 18]; for k = 2 the needed U^1 statement comes from Matomaki-Radziwill [Tao16b, p. 4]." This misstates the sources.**
- Remark 3.4 (p. 18) is stated only for "a specific choice of k >= 3". The Section 3 argument of Tao16b explicitly excludes k = 2: "we may assume k > 2, since the k <= 2 case was already established in [54]" (p. 11, [54] = Tao16). The U^{k-1} bound also needs k > 2: "using our assumption k > 2" (p. 18).
- p. 4 of Tao16b says only that the d = 1 case of Conjecture 1.6 (local U^1) follows from [44] = MR16. It does not say this U^1 statement is what gives the k = 2 Chowla case.
- In Tao16 the k = 2 case is proved with the circle method and the MRT15 estimate for short sums of λ(n)e(αn) ("modulated", Tao16 abstract and p. 4). That is a local Fourier-type input with the sup over α outside the average (cf. Tao16b p. 5: "A variant of the s = 1 case of Conjecture 1.7, in which the supremum ... is placed outside the summation in n, ... was established in [46]"). E1 shows that U^1 alone cannot suffice.
- **Fix:** "For k >= 3 the k-point case needs only local U^{k-1} [Tao16b, Remark 3.4, p. 18]. The case k = 2 was proved earlier [Tao16, Theorem 1.2], with the MRT15 bound for short sums of λ(n)e(αn) (which rests on MR16 [Tao16, p. 4]) as the uniformity input. The local U^1 case of Conjecture 1.6 follows from MR16 [Tao16b, p. 4]."

**E3. Remark `rem:gowers`: "Tao sidesteps it for λ by localising".** This is overstated. For λ, localisation proves nothing beyond k = 2. Theorem 1.8 is an equivalence between open conjectures, and Tao16b p. 4 says "the d > 1 cases remain open". The k = 2 result (Tao16) predates the localisation framework and does not go through it.
**Fix:** "Tao reformulates the problem for λ by localising: ... (Theorem 1.8, an equivalence of open conjectures). The only case proved, k = 2, is [Tao16]."

## Gaps

**G1. `rem:gowers`: "on intervals of length H << log X the function Λ-1 equals -1 at most points, so it is not locally uniform at all."** The inference is invalid as written. Λ-1 equals -1 at most points on intervals of *every* length, and it is still globally Gowers-uniform. The correct reason: for H = o(log X), most intervals [x, x+H] contain no prime, because the number of x with a prime in [x, x+H] is at most (H+1)π(2X). On those intervals the local average of Λ-1 is exactly -1 (up to prime powers), so E_x ||Λ-1||_{U^1[x,x+H]} >= 1 - O(H/log X). For H of order C log X, the Poisson-type fluctuation still keeps the local U^1 norm bounded below, but "-1 at most points" is no longer the reason. **Fix:** replace "H << log X" by "H = o(log X)" and give the reason above. Also, "at the scale it needs" has no citation. Say that the entropy-decrement scales H are taken slowly growing (Tao16 p. 4: "a scale parameter H (in some suitable range [H_-, H_+])"), and keep it labelled as our reading.

**G2. `rem:gowers`: the passage on why the route fails for Λ** should cite the direct source. Tao16 p. 5 says: the arguments "rely in an essential fashion on multiplicativity at small primes, they unfortunately do not appear to have any bearing as yet on twin prime-type sums such as (1.2)". The use of λ(p) = -1 and complete multiplicativity in the local-uniformity-to-Chowla step is at Tao16b p. 12. Citing these would turn part of the "our reading" into Literature.

**G3. `rem:gowers`: "So the global Gowers norms of λ or Λ, which is all the finite-complexity theory uses, carry no information about ..."** There are two problems.
- (a) The finite-complexity theory also uses a pseudorandom majorant. Proposition 7.1 of GT10 assumes |f_i| <= ν with ν D-pseudorandom. So "all ... uses" should read "the only arithmetic input beyond the pseudorandom majorant".
- (b) "carry no information" should read "their smallness, with any rate of the form O(L/N)^{1/2^d}, does not by itself constrain". The Proposition is about smallness, not about the norms' values.

**G4. "Gowers uniformity of every order is compatible with ..."** The Proposition fixes one d. To make it hold for all d <= D at once, apply Markov to the D norms simultaneously (factor D+1 instead of 1, or D+2 in part (2)). Either add that sentence or say "of any fixed order".

**G5. Proof, minor omissions (the claims are true; the steps are just not written).**
- (i) "the expected numerator is at most 2^{2d} L N^d" silently sums over the 2^d - 1 nonzero ω. The arithmetic is 2^d · N(2N)^{d-1} · 2L = 2^{2d} L N^d. Say "summing over ω".
- (ii) Markov's inequality needs ||f||^{2^d}_{U^d} >= 0. This holds for real f: for d = 1 it is (Σf)^2, and in general it is a sum of squares over x, h_1, ..., h_{d-1}. State it.
- (iii) The count N(2N)^{d-1}·2L uses h_j in [1-N, N-1] for j ≠ i (so negative h is covered), and 2L-1 values of h_i for given ω·h in (-L, L). Worth one clause.
- (iv) Part (1) uses one realisation for f_+ and a separate one for f_-. Fine, but say so.
- (v) In the last display of the proof, the step Σ_{n<=N-2} f(n) + Σ_{n<=N-2} f(n+2) <= 2|S| + 4 (S = Σ_{n<=N} f(n)) is where the "+8/N" comes from (4 from here plus 4 from the bad-n count). Stating it makes the constant checkable.

## Literature checks

| Claim (location) | Source | Status |
|---|---|---|
| GT10 Definition 1.5, Lemma 1.6, Main Theorem, pp. 7-9 | math_0606088 pp. 7-9 | OK. Def 1.5 p. 7, Lemma 1.6 p. 8 ("finite complexity iff no two of the ψ_i are affinely dependent"), Main Theorem p. 9, conditional on GI(s) and MN(s). |
| Quotation "which counts twin primes, has infinite complexity" (p. 7) | p. 7, Examples 1 | OK, verbatim. |
| Proposition 7.1, Theorem 7.2, cited as "p. 27" | pp. 26-27 | **Page fix:** Proposition 7.1 is on **p. 26** and Theorem 7.2 on p. 27. Cite "pp. 7-9, 26-27". The bib entry says "read pp. 1-10, 27", so p. 26 was cited without being listed as read; update it. Theorem 7.2 is indeed ||Λ'_{b,W} - 1||_{U^{s+1}[N]} = o(1), conditional on GI(s) and MN(s). |
| Normalisation | GT10 App. B vs Tao16b p. 4 | Minor: the GT10 norm U^{s+1}[N] (App. B, via Z_{N'}) is not literally the Tao16b local norm used in the Proposition. The two are comparable up to constants depending on d. Add "(equivalent up to constants)". |
| MN(s) proved in GT12 (abstract; Section 6 for λ) | 0807.1736 abstract, Section 6 "The Liouville function" | OK. The abstract says it "implies the Möbius and Nilsequence conjecture MN(s) ... for every positive integer s". |
| GI(s) by GTZ, "as cited in [Tao16b, p. 2, ref. 32]" | 1605.04628 | **Page wrong.** p. 2 does not cite [32]. The proof is attributed in the abstract (p. 1), on p. 4 ("inverse conjecture for the Gowers norms, proven in [32]") and on p. 6. Ref [32] is GTZ, "An inverse theorem for the Gowers U^{s+1}[N]-norm". Change to "p. 4". |
| "For λ, global Gowers uniformity on intervals of length ≍ X is known [Tao16b, p. 4]" | p. 4 | OK: "the results in [32], [29] give the claim (1.4) when H >= X" (ω fixed). |
| Local norm definition (Prop.) [Tao16b, p. 4] | p. 4 | OK, matches exactly. |
| Thm 1.8 equivalence (p. 5) | p. 5 | OK. Conjectures 1.3-1.7 are equivalent. |
| Remark 3.4, p. 18, "k-point case needs only U^{k-1}" | p. 18 | Correct page, but the remark is **for k >= 3 only** (see E2). |
| "for k = 2 the needed U^1 statement comes from MR [Tao16b, p. 4]" | p. 4, p. 11 | **Misattribution** (E2). p. 4 gives local U^1 from MR16. The k = 2 Chowla case is from Tao16 (p. 11 of Tao16b), via MRT15. |
| "multiplicativity at small primes named in the abstract of [Tao16]" | 1509.05422 abstract | OK: "Our main tools are the multiplicativity of the Liouville function at small primes, ...". |
| `rem:mr16-transfer`: Tao16 Theorem 1.2 is the two-point result | p. 2 | OK. |
| `rem:mr16-transfer`: "by its abstract it uses the averaged short-interval result of [MRT15] rather than [MR16] itself, together with an entropy decrement argument" | abstract; p. 4 | **Partly misleading.** The abstract does name the MRT result ("averages of *modulated* multiplicative functions in short intervals"; MRT15 is ref [23] = "An averaged form of Chowla's conjecture") and the entropy decrement argument. But p. 4 adds that the MRT estimate "is based in turn on the results of Matomäki and Radziwill in [21]" (= MR16). "rather than MR16 itself" suggests independence from MR16, which is false. **Fix:** "... uses the MRT15 estimate for short sums of λ twisted by e(αn), which itself builds on [MR16] [Tao16, p. 4], together with ...". Also say "modulated". Optionally add the p. 5 quotation (G2). |
| "(Green-Tao count patterns of primes that sieve weights alone cannot)" | GT10 p. 9, pp. 67-68; GT12 pp. 2-3 | Defensible but unsourced. Suggested sources: GT10 p. 9 (enlarging Λ to almost primes gives upper bounds off by a constant factor); GT10 Remark after Theorem D.3, pp. 67-68 ("significant barriers (the 'parity problem') to reducing this multiplicative loss to something approaching 1"); GT12 pp. 2-3 (MN(s) is proved by "Vinogradov's method of Type I and Type II sums", the bilinear input that sieve axioms lack). Suggested text: "(the finite-complexity counts get past parity because MN(s) uses bilinear Type I/II information [GT12, §3]; sieve weights alone give only upper bounds off by a constant [GT10, pp. 9, 67-68])". |
| Λ - 1 not locally uniform for H << log X | none needed (elementary) | True for H = o(log X) with the corrected reasoning (G1). Mark it "our reading" or give the one-line argument. |
| Script numbers (N = 32768, L = 64: 0.209, 0.969, 0.098, -0.004) | `code/parity/gowers_twin_blocks.out` | OK, they match the output (0.2091, 0.96875, 0.0979, -0.00446). |

## Minor

- **M1.** The Proposition's bound is non-trivial only when N >> c_d L. At the script's parameters c_2 L/N = 4, so the bound on ||f||^4 is vacuous. The script itself says "crude". The remark should say the numbers are measured, not guaranteed by the Proposition. Also, the measured U^2 norm of f_+ (0.209) is about twice that of λ (0.098). Both are small, but "against" may read as "comparable". State that the ratio is roughly (L)^{1/4} ≈ 2.8 in expectation.
- **M2.** The constant c_d = 2^{2d+1}(4d)^d is correct but very loose. At d = 3, N = 12-14 the exact expectation is 0.38-0.67 against bounds of 3·10^4 to 1.3·10^5. The hypothesis N >= 4d can be weakened to N >= 2d: the denominator bound only needs floor(N/2d) >= N/4d. No change needed.
- **M3.** Edge cases verified exhaustively for small parameters (no failures):
  - d = 1, where the norm power is (Σf)^2/N^2 and E <= L/N <= 32L/N;
  - L = 2, where every n is "bad" and the bound is trivially negative;
  - L odd;
  - n indexed from 1, where block 0 has L-1 elements, which is harmless;
  - coinciding vertices (h_i = 0), handled correctly by the multiset "even count" condition;
  - negative h_i.

  The bad-n count 2N/L + 2 and the bound -(N-2) + 4N/L + 4 hold deterministically for every realisation checked.
- **M4.** The parity component of the label is not needed for (1): blocks alone give the same correlation. It is needed only so that f_- (with s(n) = (-1)^{floor(n/2)}) has s(n)s(n+2) = -1 while n and n+2 share an eps. A half-sentence on why the label has two coordinates would help the reader.
- **M5.** The W-trick parenthesis ("1+f and 1-f already make the point") is correct and does not need the Proposition: any ±1 function f with small Gowers norms works, e.g. random signs. Add "(any f with small Gowers norms, e.g. random signs)". It also needs b and b+2 both coprime to W, which is implicit.
- **M6.** "folklore in substance" is fine. Give one pointer if one exists (e.g. Tao's blog discussions of why Gowers norms do not control binary problems); otherwise leave it as is.

---

## Resolution (coordinator, Session 28)
All items checked against the sources (Tao16 pp. 4-5, Tao16b pp. 4, 11, 18, GT12 Sec. 3, GT10 pp. 9, 26, 67-68) and applied
in v0.13: E1 (f_- is locally U^1-uniform with correlation ~ -1; now used as the point), E2 (k >= 3 only for Remark 3.4; k = 2 via
Tao16 Thm 1.2 and MRT15), E3 ("reformulates"; equivalence of open conjectures), G1 (H = o(log X) with the counting argument), G2
(Tao16 p. 5 quotation), G3 (pseudorandom majorant; "does not by itself constrain"), G4 (simultaneous version for d <= D with
factor D+2), G5 (all steps written), page fixes (GT10 p. 26; Tao16b p. 4), rem:mr16-transfer (MRT15 builds on MR16), the
parenthetical sourced (GT12 Sec. 3; GT10 pp. 9, 67-68), M1, M4, M5. M2, M3, M6: no change.
