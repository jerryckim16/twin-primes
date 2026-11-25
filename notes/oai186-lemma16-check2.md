# Rung 186: second, independent check of Lemma 1.6 of [14]

Source [14]: OpenAI, "Numerical certificate for prime gaps at most 186", 30 Aug 2026,
`code/third_party/openai186/short_gaps_numerics.pdf` (read with `pdftotext -layout`; printed pages 9-10 also rendered
as images to fix the lists U1..U6 and the lemma text). Page numbers are the printed ones.

Script: `code/oai186_lemma16_check2.py`, output `code/oai186_lemma16_check2.out`. Exact `fractions.Fraction` / integer
arithmetic for every decision; no repository code or data used (every number recomputed from the PDF's formulas).
**180,016 checks, 0 failures, 3.4 s, peak RSS 20 MB.** Sections 1-5 and the .out were final before I opened the first
program's note.

**Verdict: verified as stated**, under the readings in section 2 (none of them is forced; each is the natural one, and
the alternative readings I tried give the same outcome).

## 1. Statement and definitions used

- p. 10, Lemma 1.6: "The radial restrictions in (1.26), applied to the displayed 61 low intervals, retain every source
  failure assigned to those intervals." Proof: per eligible row, a witness below u gives s > c_t and
  s > V_t - (mu_t - 1)u; minimum over eligible rows, absorbed order-two rows included, gives (1.26); "outward
  full-cell test". Direct check: of the 40 order-5/2 intervals, the first 11, 2, 5 (outer, old-inner, new-inner) "end
  below every absorbed order-two activation"; on the remaining 11, 5, 6 "the order-three minimum is the group's
  original lower radial boundary"; "Each of the 61 intervals is nonempty on this grid."
- p. 6, (1.26): c_G(u) = max{b_G, min_{t: xi_t < u} max{c_t, V_t - (mu_t - 1)u}}; retain j >= floor(c_G(u)/h) - d_G + 1;
  empty eligible set = empty event; mu_t = 2 (orders 1, 2), 5/2 (order 3); "include every originating row, also those
  of the preceding order-two group when m_G = 5/2"; (1.25) the box range floor(b_G/h) - d_G + 1 <= j <= floor(t_G/h).
- p. 4-5, (1.13)-(1.21): ladders, rows, a, b, A, C, xi; predicates O_t, I_t; p. 5-6, (1.22)-(1.24): groups, xi_G, U_G,
  b_G, t_G, z_G, p_G. p. 2, (1.3)-(1.5) grid and masks.
- p. 9, Sec. 1.5.1: a_j = (6/5)^j/20 and the six lists U1..U6 (xi = xi_G, p = p_G). Interval counts 10, 22, 5, 7, 6, 11
  (= 61; the 5/2 groups have 22 + 7 + 11 = 40). p. 9, Sec. 1.5.2 and (1.36)-(1.37).
- p. 9, Lemma 1.4 (checked separately): a retained order-three failure is a nonlargest H_{5/2} failure at the same
  threshold. Used here only to justify mu_t = 5/2 for order-three rows; Part D below also evaluates the literal
  order-three predicates.

## 2. Readings I had to fix

1. **Core and threshold.** For the outer groups c_t = a_t and V_t = A_t (failure of O_t needs s > a_t and an obstruction
   above A_t); for the inner groups c_t = b_t and V_t = C_t (I_t). Inner order-one rows never fail (I_t = whole space).
   For every originating row V_t equals U_G exactly (checked); absorbed rows keep their own (larger) V_t and mu_t = 2.
2. **Absorbed rows.** O_{5/2} absorbs all O_2 rows ((o,t),(n,t), t <= 23); I^old_{5/2} absorbs (o, 12..23);
   I^new_{5/2} absorbs (n, 12..23).
3. **"Assigned to an interval"** = the configuration has a failing witness p (p > xi_t, prefix(p) + (mu_t - 1)p > V_t)
   with p in (l, u], and its root total lies in the group's radial interval (b_G, t_G]. This matches the Palm sum
   (1.37) over p in X ∩ (l, u].
4. **Retained index set of an interval** = the group's mask row of (1.5) (the row with cap z_G) ∩ (1.25) ∩
   {j >= floor(c_G(u)/h) - d + 1}. (1.25)'s lower bound coincides with the mask row's lower end for all six groups
   (checked), and its upper bound is never binding.
5. **"End below every absorbed order-two activation"** = u <= xi_t for every absorbed row. No interval endpoint
   equals an absorbed activation (checked), so <= and < agree.
6. **"Nonempty on this grid"**: I check both readings: the retained index range is nonempty, and the Sec. 2.1
   conditions 2 <= L < H <= K <= N with L = floor(l/h), H = ceil(u/h), K = ceil(z_G/h).

## 3. Method, and why it is independent

- **Part A (data).** Recomputes the ladders, the 67 retained rows, (1.17), the six mask rows of (1.5) from
  (1.18)+(1.19), p_G = h floor(U_G/(2 m_G h)) against (1.24), xi_G = min activation of the originating rows, absorbed
  activations >= xi_G.
- **Part B ((1.26) itself).** Builds the 61 intervals from the lists (each list strictly increasing), evaluates
  c_G(u) and the retained range, and checks the direct-check counts as stated: the intervals ending below all absorbed
  activations are exactly a prefix of length 11 / 2 / 5, the rest number 11 / 5 / 6, and on those the order-three
  minimum (originating rows only) gives max(b_G, min) = b_G; hence c_G(u) = b_G there.
- **Part C (exhaustive, without (1.26)).** For each interval, every eligible row (originating and absorbed) and every
  index sum j of the group's whole mask range (192,123 (interval, cell) pairs), it decides exactly whether a failure
  with a witness in the interval can have its total in [jh, (j+d)h) ∩ (b_G, t_G] (s > c_t, s > V_t - (mu_t - 1)p for
  some admissible p <= min(u, z_G), p > max(l, xi_t)). Every such cell must be retained by (1.26). It also counts cells
  that (1.26) retains but where no failure is possible.
  **C2 (boundaries):** (i) every failure-capable row has core >= the first group's b_G, and the cells below each first
  mask row end at or below b_G, so nothing is lost below the first groups; (ii) in the cells of a 5/2 mask row whose
  totals can still be <= t_G of the preceding 2-group (straddling cells), a failure of a 2-group row is retained by
  the 5/2 interval holding its witness (20,230 cases).
- **Part D (explicit configurations, literal predicates).** For each interval and eligible row it builds concrete
  multisets of fragments on d coordinates. The witness p is at u or random in the interval, larger prefix fragments
  are in [p, z_G], and filler fragments are < h < min xi. The placements are both adversarial (each coordinate total
  just below a grid point, plus filler-only coordinates, which lower the cell index) and random. For each one it
  evaluates (1.21) literally: H_{2,xi}, H_{phiD,xi}, H_{phiE,xi}, M_xi, phi_D, phi_E with L = 23C/40. It keeps only
  real failures in the group's region (b_G < s <= t_G, mask row, fragments <= cap), checks a failing witness lies in
  the interval, and computes j = Σ floor(t_i/h). 4,136 failing configurations were tested and all were retained;
  763 candidates were skipped because they fell outside the region or did not fail.

## 4. Findings

- 61 intervals (10, 22, 5, 7, 6, 11); 40 of order 5/2. All lists strictly increasing.
- Direct check exactly as stated: ending below all absorbed activations: O_{5/2} intervals 1-11 (u <= 9/400 <
  min absorbed activation xi_{o,23} = 0.024787 < next end 27/800), I^old_{5/2} 1-2 (u <= 1/100 < xi_{o,23} < 27/800),
  I^new_{5/2} 1-5 (u <= 9/400 < xi_{n,23} = 0.028353 < next end 0.06). Order-three minimum = b_G on the remaining 11, 5, 6.
- c_G(u) > b_G (a real restriction) only on O_2 intervals 1-2 (c - b = 0.0608, 0.0469: few rows eligible since
  xi_{o,t} span is wide) and on the 5/2 intervals that end below the absorbed activations (c - b from 0.0283 down to
  0.0106). Elsewhere c_G(u) = b_G. All 2-group inner intervals are unrestricted.
- Part C: 142,683 failure-possible cells, **all retained**; and **0 cells retained without a possible failure**. So
  (1.26) with the outward floor is exactly the set of cells allowed by the necessary conditions: sound, and not
  improvable by one cell at either end.
- Part D: explicit failures reach within 0-3 cells of the retained lower end on all 61 intervals (exactly the lower
  end on 11). So the restriction is not just sound on paper but nearly attained by actual configurations.
- Nonemptiness: every retained range is nonempty (smallest: O_{5/2} interval 1, j in 98259..98263, 5 cells;
  I^new_{5/2} interval 1, 89910..89914), and 2 <= L < H <= K <= N holds for all 61.

## 5. Differences from the PDF's formulation / caveats

- The containment itself is a two-line argument; the real content is the data. I check it by an exhaustive cell
  search and by literal configurations, not only by evaluating (1.26).
- I do not check that the low, rank-two and factorial components together cover every witness (Sec. 1.5.4). That
  belongs to the cover statement, not to Lemma 1.6. I do check the two facts it needs here: xi_G is the minimum
  activation, and absorbed activations are >= xi_G, so bins starting at xi_G miss no witness.
- Order-three rows are treated through Lemma 1.4 (mu = 5/2). The literal predicates in Part D agree on all
  constructed configurations.

## 6. Comparison with the first program (written after sections 1-5 and the .out were final)

First program: `code/oai186_lemma16_check.py`, `code/oai186_lemma16_check.out`, `notes/oai186-lemma16-check.md`. It
reports 42 checks, 0 failures, about 6.5 s and 42 MB. Its 42 checks are coarse (one check per claim). My 180,016 are
per item: cells, rows and configurations. The counts are not comparable.

- **Verdict: agree.** Both say "verified as stated", with no repair needed.
- **Numbers: agree exactly.** Both find 61 intervals split 10/22/5/7/6/11, with 40 of order 5/2. The direct check
  gives 11/2/5 intervals ending below the absorbed activations, with the same separating values (0.0225 < 0.024787
  < 0.03375; 0.01 < 0.024787 < 0.03375; 0.0225 < 0.028353 < 0.06). The order-three minimum equals b_G exactly on
  the remaining 11/5/6 intervals. No ties, so "<" and "<=" agree. For nonemptiness, the smallest retained range is
  5 indices (O_{5/2} interval 1) under both mask readings. The full-cell test is exact: their (a) matches my Part C
  finding of 0 retained-but-impossible cells.
- **Readings: agree.** Both take (c_t, V_t) = (a_t, A_t) for outer groups and (b_t, C_t) for inner groups. Both take
  absorbed rows to be the preceding order-two group's rows, keeping mu = 2. Both read "assigned" through a witness
  of the failing row itself (my reading 3). The first note adds a useful point that I did not test. Under the
  looser reading "any group-level H_{m_G} witness in the bin", the sentence is false. It gives an explicit O_2
  root that bin L1 clips but bin L3 retains, so the cover is unaffected. I did not construct such roots, because
  my Part D only uses row witnesses, so I neither confirm nor contradict that example independently.
- **A structural fact noted only by the first program:** c_G(u) = max(b_G, min of the eligible cores) on all 61
  intervals, so the threshold term V_t - (mu_t - 1)u never decides. My script did not test this. After the
  comparison I checked it with a throwaway script (not part of the recorded .out), using my script's own
  functions: it holds on 61 of 61. **Agree.**
- **Different methods.** The first program uses random and boundary failing roots: 7,050 roots, 16,510 witnesses,
  and negative controls. Mine uses an exhaustive cell-by-cell search (192,123 interval-cell pairs plus 20,230
  straddling-cell cases) and 4,136 explicit configurations evaluated with the literal predicates (1.21), including
  order three. Both find 0 lost.
- **No bug of my own found** on comparison. No disagreement.
