# Rung 186: second, independent check of Lemma 1.7 of [14]

Source [14]: OpenAI, "Numerical certificate for prime gaps at most 186", 30 Aug 2026,
`code/third_party/openai186/short_gaps_numerics.pdf` (read with `pdftotext -layout`; printed pages 9-10 rendered as
images for the T-lists and (1.39)-(1.44)). Page numbers are the printed ones.

Script: `code/oai186_lemma17_check2.py`, output `code/oai186_lemma17_check2.out`. Every decision is exact
(`fractions.Fraction` / int, sympy for the algebra). Logarithms are enclosed with python-flint 0.9.0 arb balls at 160
bits, and the enclosures are turned into exact rational outward bounds. No repository code or data is used.
**22,295,188 checks, 0 failures, 88 s, peak RSS 93 MB.** Sections 1-5 and the .out were final before I opened the
first program's note.

**Verdict: verified as stated.** The lemma is a short measure-theoretic statement. Its two inequalities, the capping
remark and the "charge L once" claim are all confirmed. The finite data it is applied to (30 rank-two bins x 98,304
cells) satisfies every hypothesis, and all the fractions are rigorously in [0, 1] with valid outward bounds.

## 1. Statement and definitions used

- p. 11, Lemma 1.7: in a largest-fragment interval (q-, q+], L := log(q+/q-), and the clipped log (1.45) is
  L(v) = 0 (v <= q-), log(v/q-) (q- < v < q+), L (v >= q+). For a physical cell with upper endpoint t+, the
  largest-fragment coordinate and same-coordinate measures may be multiplied by outward upper bounds for
  L(t+)/L and L((m t+ - U)/(m-1))/L (1.46). "The second fraction may also be capped by the first. Charge the common
  factor L once." The proof says: q < t+, and q < (m t+ - U)/(m-1) because t+ > q + (U-q)/m; integrate dq/q; each
  monomial of (1.43) carries exactly one largest-fragment factor; a positive lower bound for L goes in the denominator.
- p. 10, (1.39): the rank-two condition q > U/(m+1), p > d(q) = max{p_G, xi, (U-q)/m}, q <= z. (1.42)-(1.44): the
  marking ring Q = P + xA + yB + xyC mod (x^2, y^2), [xy]Q^d = dP^{d-1}C + d(d-1)P^{d-2}AB, and the erased-coordinate
  split C_e P_r + P_e (xy)_r + A_e y_r + B_e x_r.
- p. 9: the bins (q0 + t_{j-1}(z_G - q0), q0 + t_j(z_G - q0)] with q0 = U_G/(m_G+1), and T1..T6 (6, 12, 1, 2, 4, 5 bins,
  30 in all). (1.23)-(1.24): U_G, m_G, z_G, p_G, xi_G.
- p. 14, Lemma 2.4 (the place where the lemma is used): lambda(v) = min{1, max{0, log(v/a)/Lambda}}. The fractions are
  lambda(t+) and lambda(min{t+, (m t+ - U)/(m-1)}), with indicators 1{t+ > a} and 1{t+ > a + r+}, r+ = (U-a)/m, in (2.9).

## 2. Readings I had to fix

1. The cell's coordinate total t satisfies t < t+ = (j+1)h (cells C_j = [jh, (j+1)h), (1.3)).
2. "Same-coordinate" means that the coordinate holding the largest fragment q also holds the second fragment p, with
   (U-q)/m < p <= q. The lemma keeps only (U-q)/m from d(q). Omitting p_G and xi enlarges the event, which is allowed.
3. q- = a, q+ = b are the bin endpoints from the T-lists with the aligned cap z_G = (z_G/h)h of (1.24). Lambda in
   Lemma 2.4 is this L.

## 3. Method, and why it is independent

- **Part A/B (data and hypotheses).** Recompute xi_G, U_G, m_G, z_G and p_G (p_G against floor(U/(2mh))). Build the
  30 bins and check, exactly, that they tile (q0, z_G], that U/(m+1) <= a < b <= z < U, that max(p_G, xi) <= U/(m+1)
  (so d(q) < q), and that r(a) = (U-a)/m <= a. Check L > 0 rigorously from an arb enclosure.
- **Part C (exhaustive exact feasibility, all 2,949,120 bin x cell pairs).** For each cell the feasible q-sets are
  derived directly from the constraints, not from (1.46):
  - largest fragment in the coordinate: q in (a, b] with q < t+;
  - same coordinate: q in (a, b] such that some p satisfies (U-q)/m < p <= q and q + p < t+. The affine slack
    g(q) = (t+ - q) - (U-q)/m is shown strictly decreasing, its exact root is found, and the set is (a, min(b, root)).

  These are compared with the clipped arguments clip(t+) and clip((m t+ - U)/(m-1)) of (1.46). The script also
  checks the (2.9) indicators (t+ > a iff L(t+) > 0; t+ > a + r+ iff L(w) > 0), and that
  lambda(min{t+, w}) = min of the two fractions (the capping remark and Lemma 2.4's form agree). It checks
  t+ <= U ⇒ w <= t+, and t+ > U ⇒ both fractions equal 1, so capping never loses mass.
- **Part D (rigorous enclosures).** On every cell where a fraction lies strictly inside (0, 1) (84,185 first and
  45,882 second fractions, 130,067 cells), arb gives log(v/a)/L. The script checks 0 < f < 1 and f2 <= f1
  rigorously. It forms the exact rational outward bound upper(log)/lower(L), using a positive rational lower bound
  for L, and checks that it dominates the ball. None of these bounds exceeds 1, and the widest one is 1.8e-46 above
  the lower endpoint. On 333 sampled (cell, fraction) pairs, the logarithmic mass is cross-checked two other ways.
  (i) Rigorous arb quadrature (`acb.integral`) of dq/q over the exact feasible interval must overlap the closed form.
  (ii) Exact rational Riemann brackets (64 panels, monotone 1/q) must contain the arb log.
- **Part E (algebra).** sympy expands (P + xA + yB + xyC)^d in R[x,y]/(x^2,y^2) for d = 1..40. It confirms (1.43)
  and that every monomial of [xy]Q^d has degree exactly 1 in {A, C} (one largest-fragment factor) and exactly 1 in
  {B, C}. It confirms (1.44) for r in {1, 2, 3, 38, 39}, with every monomial carrying exactly one of A, C, A_e, C_e.
  It also checks symbolically that t+ > q + (U-q)/m is equivalent to q < (m t+ - U)/(m-1) (positive factor), for
  m = 2 and m = 5/2, and that q + r(q) increases.

## 4. Findings

- 30 bins (6, 12, 1, 2, 4, 5). All hypotheses hold. L ranges from 0.0314 (O_{5/2} bin 8) to 0.4054 (I^old_2, one bin).
- Cell classes over all bins: first fraction 0 on 1,029,126 cells, 1 on 1,835,809, strictly inside on 84,185. The
  second fraction is 0 on 1,819,755, 1 on 1,083,483, strictly inside on 45,882.
- No disagreement between the directly derived feasible sets and (1.46) on any cell. The capping remark is exact.
  For t+ <= U the second argument is <= t+. For t+ > U both fractions are 1, since b <= z < U.
- "Charge L once": confirmed. Every monomial in (1.43)/(1.44) has exactly one largest-fragment factor (A or C, or
  A_e or C_e on the erased coordinate), so each Palm term gets exactly one fraction, and the external factor
  Lambda = L appears once.

## 5. Caveats

- I check the lemma and its instantiation on the certificate's bins and grid. I do not recompute the Dickman-based
  arrays P, A, B, C of (2.9) themselves. Their sup-over-bin bounds ("the other factors have been bounded over the whole
  original interval") are Lemma 2.4's job. I check only the monotonicity facts used there: r(q) <= q on the bins, and
  that q + r(q) increases.
- The fractions are applied to cell measures, which are integrals over t in the cell. Using t+ (the cell's sup) gives
  an upper bound for every t in the cell, because both fractions are nondecreasing in t+. That monotonicity is evident
  from the formula and implied by the exhaustive check.

## 6. Comparison with the first program (written after sections 1-5 and the .out were final)

First program: `code/oai186_lemma17_check.py`, `code/oai186_lemma17_check.out`, `notes/oai186-lemma17-check.md`. It
reports 36 checks, 0 failures, about 7 s and 41 MB. Its checks are one per claim; mine are per cell, so the counts
are not comparable.

- **Verdict: agree.** Both say "verified as stated", with no repair needed.
- **30 bins (6, 12, 1, 2, 4, 5) and their hypotheses: agree.** L > 0 with the same minimum, 0.0314 at O_{5/2} bin 8.
- **Cell classes: agree, after one bookkeeping difference.** The first program runs over j < n = 98264. My script
  runs over j < N = 98304. The zero and partial counts are identical: owner 1,029,126 / 84,185 and same-coordinate
  1,819,755 / 45,882, with 130,067 partial cells. The "one" counts differ by exactly 1,200 = 30 bins x 40 extra cells
  (1,835,809 vs 1,834,609 and 1,083,483 vs 1,082,283). Every extra cell has both fractions equal to 1. Not a
  disagreement. Since only j < n enter the final arrays (p. 12), the first program's range is the one that matters.
- **Cap redundant: agree.** Both find v2 <= t+ iff t+ <= U, and both fractions equal 1 when t+ > U. Cells with
  t+ > U occur only for the inner groups (the first note states this explicitly; my check covers it implicitly).
- **(1.43)/(1.44): agree.** One largest-fragment factor per monomial. They check d = 2..40 and a generic R, and
  also (1.44) with Q^39 against (1.43) at d = 40. I check d = 1..40 and r in {1, 2, 3, 38, 39}.
- **A reading the first note makes explicit and mine left implicit.** The first note's R1 is that the physical
  cell is the cell of the owner coordinate's total including q. It gives a counterexample under the
  residual-total reading. My script uses the including-q reading: the constraint is q <= t < t+ in Part C. My
  note's reading 1 states t < t+, but I did not flag that the other reading exists or that it would make the
  lemma false. I agree with their analysis on reading. I did not re-run their counterexample.
- **Extras on each side.** The first program adds the end-to-end rank-two configurations from (1.12): 23,996
  configurations, plus negative controls and sharpness witnesses with p > p_G, xi. It also notes d(q) =
  (U-q)/m on every bin (min slack 1.9e-7). Mine adds rigorous arb enclosures of every partial fraction, with
  rational outward bounds (none > 1, width <= 1.8e-46). It also adds two independent cross-checks of the log
  mass on sampled cells: arb quadrature and exact Riemann brackets.
- **No bug of my own found** on comparison. No disagreement in substance.
