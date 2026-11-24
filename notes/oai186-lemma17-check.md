# Rung 186: check of Lemma 1.7 of [14] (feasible logarithmic mass of the rank-two bins)

Source [14]: OpenAI, "Numerical certificate for prime gaps at most 186", dated 30 August 2026,
`code/third_party/openai186/short_gaps_numerics.pdf`, read with `pdftotext -layout` (extract kept in the scratch
directory only, not committed). Page numbers are the printed page numbers (the number at the foot of each page).

Script: `code/oai186_lemma17_check.py`, output `code/oai186_lemma17_check.out`. All decisions use exact
`fractions.Fraction` and integers. **36 checks, 0 failures**, about 7.0 s wall and 30 MB peak RSS
(`ru_maxrss`; `/usr/bin/time` is not installed in this environment).

**Verdict: verified as stated, under the readings fixed in §5.** No repair is needed. Lemma 1.7 is a short
measure-theoretic step, not a numerical table, so the proof was checked in two ways. Each of its inequalities
was checked by hand (§3). Every finite claim it rests on was checked by computation, over all cases (§4): the 30
rank-two bins, all 30 × 98264 (bin, physical cell) pairs, the ring identities (1.43)/(1.44) for d = 2..40, and
a positive lower bound for L. One reading is forced. "Physical cell" must mean the cell of the owner
coordinate's total **including** q. Under the residual-total reading the lemma is false, and §4 [6] gives an
explicit O_2 counterexample. Three facts that the PDF does not state:
(i) d(q) = (U−q)/m on every bin, so omitting p_G and ξ loses nothing;
(ii) "the second fraction may also be capped by the first" never changes a value on this schedule;
(iii) the fractions are sharp, meaning each is the exact q-projection of the feasible set, so nothing is lost
beyond the cell rounding.

## 1. Definitions (with page references)

- p. 1. Fragment configurations X; inclusive prefix; empty maximum = 0. p. 4, (1.12):
  H_{m,ξ}(X) = max_{p∈X, p>ξ} (Σ_{f∈X, f≥p} f + (m−1)p), m ∈ {2, 5/2}.
- p. 2, (1.3). N = 98304, h = S/N, n = N − 40 = 98264, physical cells C_j = [jh, (j+1)h).
  Upper endpoint t_j^+ = (j+1)h (the same notation is used in (2.9), p. 14).
- pp. 5-6, (1.23)-(1.24). Group parameters (d, m, ξ, U, z, p_G) for O_2, O_{5/2}, I_2^old, I_{5/2}^old,
  I_2^new, I_{5/2}^new. These are taken from `code/oai186_support_data.py`, which re-derives them from (1.13)-(1.20);
  all_ok = True.
- p. 9, Sec. 1.5.1. Rank-two bins: q0 := U_G/(m_G+1). Consecutive t_{j−1}, t_j of T_1..T_6 give
  (q0 + t_{j−1}(z_G − q0), q0 + t_j(z_G − q0)]. These are the "largest-fragment intervals (q−, q+]" of Lemma 1.7.
- p. 10, Sec. 1.5.3. (1.39): rank-two condition q > U/(m+1), p > d(q) := max{p_G, ξ, (U−q)/m}, q ≤ z.
  (1.40): the one-largest Palm density Σ_j ∫ (A_j Π A_i − B_j Π B_i) dq/q. (1.41): a positive upper bound.
  (1.42): Q = P + xA + yB + xyC in R≥0[x,y]/(x², y²). P is the ordinary measure, A the coordinate holding the
  largest fragment, B the coordinate holding a secondary fragment in a different coordinate, and C both in one
  coordinate. (1.43): [xy]Q^d = d P^{d−1}C + d(d−1)P^{d−2}AB. (1.44): the erased-coordinate split.
- **p. 11, Lemma 1.7** and its proof. (1.45) defines the function written here as Lf (script-L in the PDF):
  Lf(v) = 0 for v ≤ q−, log(v/q−) for q− < v < q+, and L := log(q+/q−) for v ≥ q+. (1.46) gives the fractions
  Lf(t+)/L (applied to the owner array A) and Lf((m t+ − U)/(m−1))/L (applied to the same-coordinate array C).
- p. 11, Lemma 2.1: the rational log series bounds, used here for my own enclosure of L.
- p. 14, (2.9) and Lemma 2.4: the implemented version. It has the indicators 1_{t+>a} and 1_{t+>a+r+}, and
  λ(min{t+, (m t+ − U)/(m−1)}). Λ is "charged once". p. 15-16, (2.17), (2.19), (2.21): Λ appears exactly once
  in R_G, β_G and V_G.

## 2. Statement in my notation

Fix a group G and a rank-two bin (q−, q+]. Take a configuration whose largest fragment is q ∈ (q−, q+] and whose
second-largest fragment p is an H_{m,ξ} witness at U. Let the coordinate holding q have total t in the physical
cell C_j, and put t+ = (j+1)h. Then q < t+. If p lies in the same coordinate, then also q < v2 :=
(m t+ − U)/(m−1). So ∫ 1[feasible] dq/q over (q−, q+] is ≤ Lf(t+) (owner) and ≤ Lf(min(t+, v2)) (same coordinate).
The other factors are bounded uniformly over the bin and the Palm measure is linear in the owner/same factor. So
the bound "L × sup of the product" may be replaced by "L × sup × fraction" on the A or C array, with L charged once.

## 3. The proof, line by line (checked by reading; the finite parts also by computation)

1. "A largest fragment requires q < t+." The coordinate total is the sum of its fragments, all ≥ 0, so q ≤ t, and
   t < t+ because the cell is half-open. Correct. The script checks it end to end ([6]) and checks that it is
   sharp ([4]).
2. "If the second fragment is on the same coordinate, then t+ > q + (U − q)/m." Here t ≥ q + p and
   p > d(q) ≥ (U−q)/m. The second inequality is (1.39): p is the second-largest fragment and a witness, so the
   inclusive prefix is q + p (plus ties) and q + p + (m−1)p > U. Correct, with strict inequality.
3. "Whence q < (m t+ − U)/(m − 1)." Multiply by m > 0 and use m − 1 > 0. Correct. The script checks the
   boundary identity v2 + (U−v2)/m = t+ exactly on all 45 882 partial same-coordinate pairs, and it checks the
   monotonicity of q + r(q) (slope 1 − 1/m > 0).
4. "Integrating dq/q over these feasible parts gives the two fractions." For every real v,
   ∫_{(q−,q+] ∩ (−∞,v)} dq/q = Lf(v). The three cases v ≤ q−, q− < v < q+ and v ≥ q+ are exactly (1.45), which
   is continuous at q± ([3]). Both constraints together give Lf(min(t+, v2)) = min(Lf(t+), Lf(v2)), since Lf is
   nondecreasing. That is the permitted cap. Correct.
5. "The other factors have been bounded over the whole original interval." If every factor is bounded uniformly over q ∈ (q−, q+],
   the integrand is ≤ (product of the bounds) · 1_F(q), so its dq/q-integral is ≤ (product of the bounds) ·
   Lf(cutoff). This needs every factor to be nonnegative, which holds
   for (1.41) and (2.9). Correct by reading. That the bounds of (2.9) really hold uniformly is Lemma 2.4, which is
   **not** checked here.
6. "Each monomial in (1.43) contains exactly one factor carrying the largest fragment." Checked by exact
   expansion for d = 2..40. Every monomial of [xy]Q^d has deg_A + deg_C = 1 (and deg_B + deg_C = 1). So
   fractions are never multiplied together, and every monomial receives one. The same holds for the four
   placements of (1.44), checked for a generic retained factor and for R = Q^39, which reproduces (1.43) at d = 40.
7. "A positive lower bound for L is used in the denominator." q+/q− ∈ (1, 1.5]. The Lemma 2.1 lower series (40
   terms) gives L ≥ 0.0314 > 0 on all 30 bins (the minimum is at O_{5/2} P8), with enclosure width < 10^-40.

## 4. Results

| # | Item | Result |
|---|------|--------|
| 0 | Support data all_ok; h; 0 < ξ < p_G ≤ z < U; max(p_G, ξ) ≤ U/(m+1) (printed claim of 1.5.3); z + m p_G ≤ U; q0 < z | 6 PASS |
| 1 | 30 bins (6, 12, 1, 2, 4, 5); T lists strictly increase from 0 to 1; U/(m+1) ≤ q− < q+ ≤ z < U (the hypotheses of Lemma 2.4); q+/q− ∈ (1, 2] | 4 PASS |
| 2 | d(q) = (U−q)/m on (q0, z] for every group (min slack r(z) − p_G = 1.9·10^-7); r(q0) = q0; q + r(q) is increasing, with the exact boundary identity | 3 PASS |
| 3 | L > 0 by a rational lower bound; width < 10^-40; continuity of (1.45) | 3 PASS |
| 4 | All 30 × 98264 pairs, in integer arithmetic. Owner fraction 0/partial/1 counts 1 029 126 / 84 185 / 1 834 609; same-coordinate 1 819 755 / 45 882 / 1 082 283 (per-bin table in the .out). Zero sets equal the Lemma 2.4 indicators 1_{t+>a} and 1_{t+>a+r+}. Exact boundary identity on every partial same cell. **Sharpness**: an explicit feasible (q, p, t) below the cutoff on every partial cell, with p > p_G, ξ. **The cap is redundant**: Lf(v2) ≤ Lf(t+) on every pair. Each bin meets all three classes | 7 PASS |
| 5 | (1.43) for d = 2..40; one largest-fragment carrier per monomial; (1.44) generic; one carrier per placement; (1.44)∘Q^39 = (1.43) at d = 40 | 5 PASS |
| 6 | End-to-end from (1.12): 23 996 exact rank-two failing configurations over all 6 groups (15 597 same-coordinate, 6000 boundary with p = (U−q)/m + 10^-30). All have a unique bin and lie in the feasible part, 0 lost. Negative controls: using jh instead of t+ loses 9976; dividing by m instead of m−1 in v2 loses 15 437. Reading R1 counterexample (below) | 3 PASS |
| 7 | Authors' script (comparison only): the same 30 rank-two tasks and (U, m). From the source text: `owner_feasible_mass_fractions` is (1.46) with the cap; the zero tests in `kernels` match [4]; `mass = log(hi/lo).upper()` is applied once as `multiplier` | 5 PASS |

Why the cap is redundant: v2 ≤ t+ iff t+ ≤ U. If t+ > U, then t+ > U > z ≥ q+ and v2 > t+, so both fractions
are 1. Cells with t+ > U_G do occur, but only for the four inner groups (nh = 1.04453 > U_G ≈ 0.952-0.956).

## 5. Ambiguities and the readings taken

1. **R1, "physical cell with upper endpoint t+"**: the cell C_j of the owner coordinate's total t, **including** q.
   This is what (2.9) does: A_j is indexed by the physical j with residual index s_j^− = max(0, j − ⌈b/h⌉), and
   the authors' `kernels` does the same. The other reading, t+ = the upper end of the residual (t − q) cell,
   makes the lemma **false**. Counterexample: O_2, q = 0.36 ∈ P1 = (0.34832, 0.37735], alone in its coordinate,
   and p = 0.35 in another coordinate. Here p > (U−q)/2 = 0.34248, p > p_G and H_2 = 1.06 > U = 1.04496, so this
   is a genuine rank-two failure. The residual total is 0, so t+ = h and Lf(h)/L = 0, which would drop it
   (script [6], last check).
2. **R2, "second-largest witness"** (1.5.3): a witness p that is the second-largest fragment, so its inclusive
   prefix is q + p. That is the only reading under which (1.39) is the necessary condition. On O_{5/2} m z > U, so
   the largest fragment can also be an H_{5/2} witness there. That has no bearing on this lemma, which concerns
   the component built on p.
3. **R3, "outward upper bounds for the fractions" / "charge L once"**: (upper bound of Lf(v)) / (lower bound of L),
   with one factor L, given by an upper bound, per rank-two component. This is consistent with (2.17), (2.19),
   (2.21) and with the code (`multiplier = source.mass`). The product is ≥ the true Lf(v) because
   L_up · Lf_up / L_low ≥ Lf.
4. **R4, the q-measure is dq/q** with the cell laws D_c(t) = ρ_D(t/c), the normalized Poisson-Palm intensity of
   the largest fragment. This is taken from (1.40) and p. 1 and is **not** re-derived.
5. Lemma 1.7 does not say "clip at one". Lemma 2.4 does. Clipping is not needed for validity.
6. Different readings and the verdict: only R1 changes it, from true to false. R2-R4 are the only readings under
   which the surrounding text ((1.39), (2.9), (2.17)-(2.21)) is consistent.

## 6. Not checked

- Lemma 2.4, i.e. that the arrays of (2.9) bound the q-dependent factors uniformly over each bin. This includes
  the Dickman cap rounding and the residual shifts. Lemma 1.7 assumes it ("the other factors have been bounded").
- (1.40) as the Palm density (the normalization and the dq/q intensity), and (1.41) as an upper bound. (1.41) was
  checked by reading only: telescoping with 0 ≤ B_i ≤ A_i.
- The arb evaluation in the authors' code. python-flint is not installed here, so the script injects a
  placeholder `flint` module only to load the Fraction-level schedule and read the source text. No arb routine
  runs. (Side effect of this environment: `code/oai186_lemma16_check.py` now records 1 FAIL ("authors' script
  importable"), because it imports the module without that placeholder. Its committed .out predates this.)
- Lemma 2.1 itself. Its standard atanh series bound is used for my enclosure of L. The positivity of L also
  follows from 2v > 0.
- The random test in [6] is a sanity check. The proof is §3 plus the exhaustive [4]/[5].

## 7. Commands

```
pdftotext -layout code/third_party/openai186/short_gaps_numerics.pdf <scratch>/n.txt   # not committed
/usr/bin/python3 code/oai186_lemma17_check.py > code/oai186_lemma17_check.out           # 36 checks, 0 failures
bash -c 'time /usr/bin/python3 code/oai186_lemma17_check.py > /dev/null'               # ~7.0 s wall; RSS 30 MB (in-script)
```
