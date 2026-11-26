# Rung 186: independent second check of the finite contractions (2.17), (2.19), (2.21)

Source: OpenAI, "Numerical certificate for prime gaps at most 186" (30 Aug 2026),
`code/third_party/openai186/short_gaps_numerics.pdf`. I read it with `pdftotext -layout` into a scratch directory.
Page numbers are the printed ones. Sec. 2.2 is on pp. 14-16, the losses (1.30) and (1.32) are on p. 8, and
Remark 2.7 is on p. 21.

Program: `code/oai186_contractions_check2.py`. Run it with `/usr/bin/python3`. It uses fractions and sympy 1.14.
Output: `code/oai186_contractions_check2.out`.

**1999 checks, 0 failures. 284 negative-control runs (22 kinds), all caught. Runtime 88 s, peak RSS 64 MB.**

I wrote the program before I opened the first program (`code/oai186_contractions_check.py`), its output or its
note. I read the authors' script only for the coefficient matrix (checked against Table 1.1 of the PDF) and for
how the source forms are organised (lines 1821-2125).

## 1. What is checked, in my words

The claim is in Remark 2.7. The forms (2.17), (2.19) and (2.21) majorise the "physical source integrals". I read
those integrals as follows. All are divided by (hZ)^40, as in Sec. 1.1.

- **Outer, root square (2.17).** Σ_i ∫_{B_G} h_i |F|² dν^40. Here B_G is the source-failure event, h_i <= 1 is
  the face multiplier (1.31), and F is the step trial including the outer mask 1_{H_O}. This is the c_j-part of
  E_O in (1.32).
- **Outer, face square (2.21).** Σ_i ∫_{B_G} h_i(Y) |V_i(Y)|² dν^40(Y ⊕_i X). The event lives on all 40
  coordinates, and V_i = E_i F is the true erased marginal. This is the 1/c_j-part of (1.32).
- **Inner (2.19).** Σ_i ∫_{B_G} |V_i(Y)|² dν^39(Y), with B_G a failure event on the face. This is the
  per-component piece of β_old and β_new in (1.30).

The hypothesis I take as given (it is a separate lemma) is that the event measure is majorised by the arrays. On
each cell the event mass is at most Λ · χ_G(r) W(r) · [∗] Π_k (h a_{j_k}). Here a_j is the ring-valued coordinate
density, [∗] is the coefficient of (2.16), and r is the index sum in the event's own dimension. The arrays of the
paper are K^(e)_j = g_j^e a_j / Z_e, with Z_2 = Z and Z_0 = 1.

The claim is: physical <= printed form. The only lossy steps allowed are:
- h_i <= 1, summed over 40 faces;
- h_i <= w(r);
- |V|² <= Σ_{l∈P} |v^(l)|²;
- dropping the outer fragment caps from F in R_G.

## 2. Method

The toy model has D = 2, 3 or 4 coordinates in place of 40, and n = 4 to 6 cells.

- **Coordinate states.** Each coordinate state is a pair (cell j, fragment level λ), with a random positive mass
  ν(j, λ). Levels play the role of the largest fragment of the coordinate. F and V_i depend on a configuration only
  through its cells and its largest fragment, so this reduction loses nothing.
- **Shells and caps.** There are three outer shells by index sum, with caps c1 = 5 > c2 = 4 > c3 = 2 and c4 = 0.
  The shell cap arrays are d_c(a) = ν(cell a, λ <= c)/h. This gives the nested restriction ν|{max <= c} = ν_c
  exactly.
- **Trial data.** The trial uses the true signatures (1.6) and degrees 0-6. In 5 instances the coefficients are
  the real 77 coefficients. In the other 5 they are random rationals. Each instance also has random profile values
  g_j, random rational h, Z = Σ g_j², random 0/1 χ, random positive W, w and Λ, and random nonnegative ring arrays.
  The rings are L (mod y², [y]), P (mod x², y², [xy]) and H (mod y⁴, [y³]).
- **Physical side (brute force).** F is evaluated on every state tuple from midpoints: Π g · Σ c_{σ,d} (Σt − 9/10)^d
  P_σ(t), times the outer cap indicator. V_i(Y) = Σ_X ν(X) F(Y ⊕_i X) is computed over every state X and every
  face position i. The event measure μ is built on state tuples with cell totals equal to the bound (tight) or to a
  random fraction of it, spread over random level vectors in the support. The support is (u,v] for β and (0,z] for
  R and V. The face multipliers are 1 (tight) or random in [0,1] for R, and w(r_Y) (tight) or random in [0, w(r_Y)]
  for V.
- **Printed side.** The printed side applies the source's formulas:
  - (2.10) by set partitions with falling factorials, ring-valued, mod X^n;
  - (2.11) by ordered pairs;
  - (2.13) by labelled subsets, with the full index r+a;
  - (2.14);
  - (2.17), (2.19) with P(u,v), and (2.20)-(2.21) with P(0,z).

### Checks

| Check | Count | Result |
|---|---|---|
| (2.10) ring-valued M_{d,η} = brute sum over cells, each d = 1..D, all 53 η = σ⊔τ | 1590 | all equal |
| (2.13) pointwise: V_i(Y) = h Π g Σ_τ v^(l)_τ(r) P_τ(Y) for every Y and face i, with l the branch of max(Y), and V = 0 above c1 | 10 instances | all equal |
| R tight (h_i = 1, μ = bound, no cap indicator): exact identity | 10 | equal |
| R random (with cap indicator, random h_i, random μ): physical <= R_G | 20 | holds |
| β tight per branch l (all levels in one branch): physical = single-l term of (2.19) | 13 | equal |
| β random: physical <= β_G | 20 | holds |
| β on (0, 3/2] with the correct P = {3} | 9 | equal |
| V tight per branch l (h_i = w): physical = single-l term of (2.21) | 21 | equal |
| V random: physical <= V_G | 20 | holds |
| sympy: (2.10) symbolic for d <= 3 and all 53 η | 159 | identity |
| sympy: [xy] (1.43), [y], [y³] closed forms for d <= 7 | 21 | identity |
| sympy: the four placements (1.44) | 1 | identity |
| sympy: affine expansion behind (2.13), per σ | 11 | identity |
| sympy: (2.24) and (2.20) as a correlation | 12 | identity |
| (2.18) on grids (toy caps and real caps, including all boundary values), against an independent point test | 56 | agree |
| Real data, see below | 26 | pass |

### Real-data checks (exact)

- ρ* = 2624989/10^7, and T0 and T1 match (1.1).
- The H0 and H1 mask ends 89524 and 89914 are exactly the last r with (r+39)h <= T0 and (r+39)h <= T1, so w(r) >=
  h_i.
- The values of a_h and b_h are confirmed, and 0 <= |b_h| <= max{|a_h+b_h|, |b_h|} <= 1.
- P(0, z_G) = {2,3} for O2 (z = c2 exactly, so branch 1 is excluded by the strict inequality), and {3} for O5/2 and
  all inner groups.
- All 12 inner rank-two bins of Sec. 1.5.1 lie in (0, c1] and have P(q−, q+) = {3}.

### Negative controls (all caught on every instance where they change the value)

| Control | Caught / run |
|---|---|
| R_G without the factor D (40): identity | 10/10 |
| R_G without the factor D (40): inequality also fails | 10/10 |
| Profile power 1 in place of 2, in R / β / V | 10/10, 13/13, 21/21 |
| [x] in place of [xy] (P ring), in R / β / V | 4/4, 4/4, 9/9 |
| P with c4 = 3/2 ≠ 0: physical > printed (inequality fails) | 9/9 |
| P with c4 = 3/2 ≠ 0: the grid differs from the definition | 1/1 |
| d^{\|π\|} in place of (d)_{\|π\|}, in R / β / V | 10/10, 13/13, 21/21 |
| Unordered pairs in Q (R) or in S (β, V) | 10/10, 13/13, 21/21 |
| x_r in place of x_{r+a} in (2.13), for β / V | 12/12, 21/21 |
| Single shell v_l in place of the prefix v^(l) (β, l >= 2) | 9/9 |
| W(r) in place of W(r+a) in C(r) | 21/21 |
| K^(2) on the erased coordinate | 21/21 |
| h in place of h² in V_G | 21/21 |

Two control runs were vacuous: the altered formula gave the same value as the correct one on that instance (a shell
with no surviving cells). They are listed and not counted.

## 3. How this differs from a direct transcription

- The physical side never uses the printed formulas. It sums F² and |V_i|² over all state tuples, computes V_i by
  summing over the erased state at every face position, and uses the true outer cap indicator per configuration.
- Inequalities are tested with non-extremal data (random h_i, random μ below the bound, cap indicator present).
  Identities are tested with extremal data.
- The branch structure (which prefix v^(l) applies) comes from the levels of the brute-force states. It is not
  assumed.
- The ring algebra enters the physical side only as the form of the hypothesis, [∗] Π a. Its meaning as placements
  is checked separately by sympy: (1.43), (1.44), and the [y] and [y³] closed forms.

## 4. Verdict

**Computed with script + Proved here, by reading: verified as stated, within the scope of §6.**

In the toy model, (2.17), (2.19) and (2.21) are exact finite rewritings of the physical integrals in the tight
case, and they are upper bounds in general. The only lossy steps are the listed ones.

The dimension-dependent factors are proved by reading. Here is the bookkeeping for D = 40:
- (hZ)^{-40} · h² · h^39 · Z^39 = h/Z gives 40h/Z in (2.19), with 40 faces and equal terms by symmetry.
- One extra h from the erased-coordinate cell mass gives 40h²/Z in (2.21).
- R_G has no h/Z factor, because all 40 coordinates carry K^(2).
- In D = 40, the radial argument (r + D/2)h − 9/10 is (r+20)h − 9/10.

The P-set step is also proved by reading. If max(Y) ∈ (u, v] ∩ (c_{l+1}, c_l], then l ∈ P(u, v), the allowed
shells are exactly s <= l, and V_i = v^(l)-form. If max(Y) > c1, then V_i = 0. So |V|² <= Σ_{l∈P} |v^(l)|².

## 5. Where my formulation differs from the source

1. D <= 4 in place of 40, with small n. The factor 40 becomes D, and (r+20)h becomes (r + D/2)h.
2. The source does not write out the "physical source integrals" of Remark 2.7 as formulas. I took them as in §1,
   with the external factor Λ inside the majorisation hypothesis.
3. The majorisation hypothesis is cellwise, in densities: event mass <= Λ χ W [∗] Π (h a_j). The source's arrays
   K already contain g^e/Z_e. I separate the two.
4. χ_G and W are arbitrary 0/1 and positive functions of the event's own index sum. The exponential form of W,
   Lemma 1.5 and the "< 700" claim are not used. W is evaluated at the 40-index for R, at r+a for V, and at the
   39-index for β, as in the source.
5. The face multipliers are modelled as arbitrary functions with h_i <= 1 (for R) or h_i <= w(r_Y) (for V). That
   w(r) >= h_i on the real masks is checked separately on the real data.
6. Fragments are reduced to the largest fragment per coordinate (the level). This is exact for F and V.

## 6. Not covered

- The majorisation lemmas: 2.3, 2.4, (2.8) and 1.7.
- The Dickman and Eulerian arrays, and the real-size evaluation of the 97 components.
- The directed arithmetic of Sec. 2.3: fixed-point and binary64 reductions, and (2.26).
- The cap forms (2.12) and (2.15), the Young step (2.27) and the tables.
- D = 40 itself; the toy runs go up to D = 4. The D-dependence is proved by reading, not computed.

## 7. Comparison with the first program (read only after the above was finished)

The first program is `code/oai186_contractions_check.py`, with its output and `notes/oai186-contractions-check.md`.

- **Verdicts agree.** Both programs pass with 0 failures, and all negative controls are caught. The first program
  reports 127 checks (100 positive and 27 negative), 172 s.
- The two programs read the physical integrals the same way: the same targets in (1.30) and (1.32), the same
  hypothesis, and the same three lossy steps.
- **Real data agree:**
  - P(0, z_G) = {2,3} for O2 and {3} otherwise;
  - inner rank-two P = {3};
  - the w thresholds at 89524 and 89914;
  - the values of a_h and b_h.
- **Differences in method:**
  - The first program models the event as an explicit sum over role placements. Mine uses the ring product, and I
    check the ring ↔ placement link by sympy.
  - The first program also ran literal d = 40 on n = 5, with face symmetry assumed. Mine stays at D <= 4 but sums
    every face explicitly.
  - Mine adds per-state fragment levels, so the branch l and the cap indicator are derived rather than set. It also
    adds random sub-extremal h_i and μ for the inequalities, and a c4 ≠ 0 control that breaks the inequality.
- **Discrepancies:** none. My reading of the authors' code (lines 1821-2125) also matches. One small point in their
  code: for the last shell without a largest-range, `affine_prefixes` tests `current >= 0` where (2.18) has the
  strict `0 < min(v, c3)`. These give the same set because c3 > 0 and z_G > 0.
