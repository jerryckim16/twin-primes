# Audit of parity paper v0.7, subsection `subsec:dual` ("A dual formula, and what changes at k=3")

Referee: fresh-context adversarial audit, 15 Nov 2026. Scope: `papers/parity-barrier/main.tex`, from
`\subsection{A dual formula...}\label{subsec:dual}` to `\section{The asymptotic sieve`, plus open question 6 and changelog 0.7.
Section `sec:ceil` and Theorem `thm:k2` were read for notation. The paper was not edited and nothing was committed.
(While I worked, main.tex was changed outside this subsection by commit 975df58, which adds the Tao14b attribution. The
subsection itself did not change. It now starts at line 868.)

**Verdict.** No ERROR in the mathematics. The lemma, the k=2 identification, the overlap proposition, the clean-column
geometry and all three certificates are correct, and every printed fraction was reproduced. There is one numerical ERROR
in Remark rem:k3-eps: the claimed agreement of the two extrapolation models is wrong for two of the three columns. There
are a few GAPs, each closed by one line, and several WORDING items, mostly about scoping the "orthogonal family" claims.

## Re-runs (from /home/user/twin-primes, at most 2 cores)

| command | result | matches paper |
|---|---|---|
| `k3_orth_relax_cert.py 1 8 32` | 13523319026150757/6316738844612720 = 2.140870370 (52 s) | yes (> 2.1408) |
| `k3_orth_relax_verify.py .../orth_relax_1_8_n32.json` | 0 violations, ratio equals cert: True | yes |
| `k3_orth_relax_cert.py 1 4 32` | 39699868771187709/19218050037559040 = 2.065759465 (48 s) | yes (> 2.0657) |
| `k3_orth_relax_verify.py .../orth_relax_1_4_n32.json` | 0 violations, equals cert: True | yes |
| `k3_arrangement_verify.py k3_arrangement_cert.json` | I = 241672427/6144000000, J = 2578076273/32768000000, J/I-2 = 711155/3866758832, 0 violations | yes |
| `k3_extrapolate.py k3_thm314_dual.out` | see item 6 | table yes, "agree to 2e-4" no |

The cert script rewrites `code/parity/data/*.json`. After the re-run git shows them unchanged, so the run is
reproducible. Note that `code/parity/k3_thm314_dual.out` has two uncommitted lines (eps=0.05 disj n=40, eps=0.15 full
n=20). The paper does not use them.

## 1. Lemma lem:dual

- Boundedness: fibres have length c-|u| <= c, so (int F dt_i)^2 <= c int F^2 dt_i and ||PF||^2 <= kc||F||^2. Correct.
  The formula for P^* follows from Fubini and is correct.
- (1): Correct. The pairing is integrable because F and v are both in L^2. The truncated sign function is a valid
  test function. (Simpler: psi = f_j itself is admissible, since f_j is in L^2 and the fibres are bounded.) K = W^perp =
  intersection of the V_j^perp. Correct.
- (2): S = ||P Pi_K||^2 = ||Pi_K P^*||^2 and ||Pi_K g|| = dist(g, W). Correct.
  - **WORDING.** "the projection v(f)=Pi_W P^*f gives the exact value" sits right after "any rule f -> v(f) in
    V_1+...+V_k". But Pi_W P^*f lies in W, the closure, and a sum of closed subspaces need not be closed. Fix: "any
    rule f -> v(f) in W (for instance in V_1+...+V_k) ...".
- (3): Correct.
  - **Are the V_j closed?** Yes. V_j is the range of the orthogonal projection E_j (fibre mean on Z_j), and Z_j depends
    only on t_{-j}. The clean-column V'_j are also closed: they are the range of 1_{clean}(t_{-j}) E_j.
  - **Is closedness needed?** Not for (1) or (2), because W is defined as a closure. It is needed in (3), for E'_j to be
    an orthogonal projection and for the finite orthogonal sum to be closed. It is also needed where (3) is applied
    with V'_j = V_j at k=2.
  - **GAP (one line).** The text after the lemma uses closedness of V_j at k=2 and closedness of the clean V'_j at k=3,
    but never states it. Fix: add "V_j is closed, being the range of the fibre-mean projection E_j; likewise V'_j".

## 2. Phi = (I-E_1-E_2)P^*f at k=2

Checked region by region with (PF)_1 = g(y), (PF)_2 = f(x), so P^*(PF) = f(x)1[x<=a] + g(y)1[y<=a]. Z_1 = {y>B} is
exactly U_1, because y > B forces x <= 2-y < a. Likewise Z_2 = U_2.
- On S: Phi = f+g. Correct.
- On T_1: Phi = f. Correct, since E_1 and E_2 vanish there.
- On U_1: P^*f = f(x), and E_1 subtracts its mean over the whole fibre [0,2-y], which lies in U_1. So Phi = f - fbar(y).
  Correct.
- On the rest ({x>a, y>a}, outside Z_1 and Z_2): Phi = 0. Correct.

The identity is correct.
- **WORDING.** The lemma's f is the pair (f_1,f_2) = PF, which is (g,f) in the proof of thm:k2. Fix: write
  "(I-E_1-E_2)P^*(PF), where (PF)_1 = g, (PF)_2 = f in the notation of that proof".
- **WORDING.** "so that proof computes the dual expression exactly; this is why it is sharp" overstates. The exact
  projection makes sharpness possible. Sharpness itself comes from the two inequalities (2uv <= u^2+v^2, and the mean
  minimising the squared deviation) being equalities at constant f, which F_eps realises. Fix: "...exactly, so no
  constraint is lost; the remaining two inequalities are equalities for constant f, which is why it is sharp."

## 3. Proposition prop:overlap

The set {B < t_m < c, sum_{l != m} t_l < c - t_m, t >= 0} lies in D, has non-empty interior because B < c, and lies
in Z_i cap Z_j because |t_{-i}|, |t_{-j}| >= t_m > B. Correct.
- **WORDING.** The last two sentences are muddled ("With psi=1 on a bounded region, the inner product ... restricted to
  it is that region's volume"). Fix: "Hence 1_{Z_i} in V_i and 1_{Z_j} in V_j (psi = 1; D is bounded) have
  <1_{Z_i},1_{Z_j}> = |Z_i cap Z_j| > 0."
- **GAP.** "...so Pi_K is not I - sum_j E_j" is true but not argued. Fix (one line): if sum_j E_j = Pi_W, then for
  v in V_i, ||v||^2 >= <Pi_W v, v> = ||v||^2 + sum_{j != i} ||E_j v||^2. So E_j v = 0 for all j != i, that is V_i is
  orthogonal to V_j, a contradiction.

## 4. Clean columns at k=3

- In direction j at u = (t_l,t_m), the fibre is [0, c - t_l - t_m]. It meets Z_l (where t_j + t_m > B) in positive
  length iff c - t_l > B, i.e. t_l < 1/2 - eps. So the fibre is clean iff min(u) >= 1/2 - eps. The boundary case is
  consistent with ">=". Correct.
- Disjointness: supp V'_j is the cylinder over the clean u-set in direction j. On it, t_j + t_m <= c - t_l <= B, so it
  is disjoint from Z_l, which contains supp V'_l (and likewise from Z_m). So the supports are pairwise disjoint.
  Correct.
- **GAP (one line).** The text asserts disjointness without this sentence. Add it.
- **WORDING.** Add "in a set of positive length" to "meets Z_l or Z_m".

## 5. Certificates

**k3_orth_relax_cert.py / verify.py (Prop prop:orth-relax).**
- Cubes are used only if they lie fully inside D: (sum c + 3)h <= 3/2.
- F is constant on cubes, so each marginal is constant on each column square.
- A column is constrained iff (j+l+2)h > B and min(j,l)h >= 1/2 - eps. This is exactly the set of column squares that
  meet the clean set {|u| > B, min u >= 1/2-eps} in positive measure. It uses only that 1/2-eps is a multiple of h,
  which the alignment assertion guarantees: (lo, a, B) times n must be integers. For eps = 1/8 and 1/4 at n = 32 they
  are. So the F lies in K' = intersection of (V'_j)^perp. Alignment of B is not even needed, since the test is exact
  either way.
- J is summed only over squares with (j+l+2)h <= a, i.e. fully inside {|u| <= a}. The integrand is >= 0, so this is a
  lower bound. Correct.
- Symmetry gives 3 J_1. The verifier recomputes all three directions independently anyway.
- I = h^3 sum x^2 and J = h^4 sum (column sums)^2 are correct.
- Exactness rests only on integer arithmetic of the final integer vector. The floating eigenvector is merely a
  candidate. Correct.

**k3_arrangement_verify.py (Prop prop:k3-step).** I checked the geometry myself.
- Cells: a sign vector over a hyperplane arrangement is convex, hence a single cell. So the label (cube, pair bits,
  level) is faithful, and the canonical label over permutations gives a symmetric F.
- Fibre integrals: they are exact. Along the fibre, breakpoints sit at x_1 = m, m-u_2, m-u_3 and m-u_2-u_3, and the
  end 3n/2 - u_2 - u_3 = 12 - u_2 - u_3 is itself of the last form, since L = 12 is an integer. Values are taken at
  segment midpoints.
- **Could a breakpoint reorder inside a triangle? No.** Two breakpoints coincide, or a breakpoint hits the end, only on
  u_2 in Z, u_3 in Z, u_2+u_3 in Z or u_2-u_3 in Z. In the unit square [p,p+1]x[q,q+1], the only such lines through the
  interior are the two diagonals u_2+u_3 = p+q+1 and u_2-u_3 = p-q. So the four triangles are exactly the cells of the
  2D arrangement. On each open triangle the breakpoint order and the segment labels are fixed. Segment lengths are
  differences of affine functions, so f_1 and g are affine there (f_1^2 is quadratic).
- Because of this, three non-collinear interior values determine the affine piece. The extrapolation
  v_i = 2P_i - (sum P)/3 for barycentric (2/3, 1/6, 1/6) is correct. The two extra affinity checks are only sanity
  checks; correctness rests on the geometric argument.
- The marginal check uses three interior points per triangle with min sum >= Bn = 10. That is exactly {u_2+u_3 >= 10},
  a union of triangles because 10 is an integer, and it shows f_1 = 0 on each such triangle. Sufficient.
- J region: max sum <= an = 6, a union of triangles, so J is exact here, not merely a lower bound.
- The quadrature formulas are exact: integral of f^2 = |T|/6 (sum f_i^2 + sum_{i<j} f_i f_j), integral of g =
  |T| x mean, and |T| = 1/4.
- I covers all of D. The cert has 515 labels, all coefficients have denominator dividing 1000, and the verifier
  imports nothing from the first program.
- Printed values 2.00019 ... 2.00255 for n = 8 ... 24 match the best rounded ratios in `k3_arrangement_exact.out`.
  6e-8 matches the 5.77e-8 in notes/explorations.md, Session 21.

- **WORDING (verifier description).** "checks that both are affine on the triangles" overstates. It spot-checks at two
  points. Fix: "both are affine on the triangles cut out by ... because on each open triangle the order of the fibre
  breakpoints is fixed (the breakpoints m, m-u_2, m-u_3, m-u_2-u_3 coincide only on these lines); the program
  spot-checks this at two further interior points".
- **WORDING (scaling).** In "u_j=m, u_2±u_3=m" and "u_j=m and u_2+u_3=m", u is the scaled variable 8t_{-1} with m in Z,
  and j in {2,3} after fixing fibre direction 1. None of this is said. Fix: "in the scaled coordinates u = 8(t_2,t_3)
  of the fibre in direction 1, the lines u_j = m (j = 2,3), u_2 ± u_3 = m, m in Z".

## 6. Remark rem:k3-eps

The table matches the three-point model L - c/n - d/n^2 (n = 24, 32, 40) rounded to 3 decimals.

| eps | full | clean only | none |
|---|---|---|---|
| 1/8 | 1.97648 | 2.18098 | 2.27251 |
| 1/4 | 2.00300 | 2.10543 | 2.16760 |
| 3/8 | 1.98982 | 2.01746 | 2.05635 |

- **ERROR (numerical).** "Extrapolating from n=32,40 (models L-c/n and L-c/n-d/n^2 agree to 2·10^{-4})".
  - The two models agree to <= 1.4e-4 only in the "all conditions" column.
  - In the other columns they differ by 5.2e-4 (1/8 clean, 1/8 none), 5.5e-4 (1/4 clean), 7.3e-4 (1/4 none),
    4.8e-4 (3/8 clean) and 8.6e-4 (3/8 none).
  - Also, the quadratic model uses n = 24, 32, 40, not just n = 32, 40.
  - Fix: "Extrapolating (model L-c/n from n=32,40 and L-c/n-d/n^2 from n=24,32,40; the two agree to 2·10^{-4} in the
    first column and to 10^{-3} in the others; table: the second model)".
  - The 1/n behaviour itself is well supported. Successive differences in the full column at eps = 1/4 are in ratio
    1 : 0.499 : 0.298, against 1 : 0.5 : 0.3 predicted.
- **WORDING.** "the arrangement values above agree with the extrapolated 2.003". The arrangement values are lower
  bounds, increasing to 2.00255 at n = 24, and a 1/n^2 fit of n = 20, 24 gives about 2.0029. Fix: "are consistent
  with (below and increasing towards)".
- **WORDING (first conclusion).** "exceeds the parity value 2 only for eps in a window around 1/4, and then by about
  0.15%".
  - This rests on three sampled eps, plus eps = 0.05 in the .out file (extrapolated 1.936, but from two points only).
  - Nothing above 3/8 was sampled, and the 3/8 margin is 0.010.
  - The values are extrapolations of grid lower bounds, and density of the grid class in K is not proved.
  - Fix: "among the sampled eps (1/8, 1/4, 3/8) only eps = 1/4 gives an extrapolated value above 2, and there by about
    0.15%; this suggests a window around 1/4". Optionally add the eps = 0.05 row (full 1.936, clean 2.235, two-point
    extrapolations).
- **Second conclusion:** fine as heuristic.
- **WORDING (third conclusion, overgeneral).** "an upper bound of the k=2 type, which sees only an orthogonal family
  of constraints, cannot prove S_3(eps) <= 2 for any eps in the table".
  - Only one orthogonal family was computed: the symmetric clean columns.
  - Other mutually orthogonal subfamilies exist, e.g. asymmetric ones keeping all constraint columns in one direction
    and only the non-intersecting cylinders in the other two. Their relaxations could be smaller.
  - At eps = 3/8 the clean-column value is above 2 only after extrapolation; the n = 40 bound is 1.987.
  - At eps = 1/4 the statement is vacuous, since S_3(1/4) > 2 by PM8b.
  - Fix: "the relaxation that keeps only the clean-column constraints has (heuristic) supremum above 2 for every eps
    in the table, so a k=2-type bound through that relaxation cannot prove S_3(eps) <= 2 there; for eps = 1/8 this is
    certain (Proposition prop:orth-relax)."
- **WORDING.** The table header "all conditions, S_3(eps)" reads as values. Fix: "extrapolated grid value, S_3(eps)".

## 7. Overclaiming, attribution, notation

- **No overclaiming about twin primes or parity.** Prop k3-step says explicitly "This is [Theorem 3.15]; nothing new is
  proved". The abstract sentence on k=3 is accurate. DHL[3,2] => H_1 <= 6, and the use of GEH = GEH[theta] for all
  theta < 1 matches sec:ceil. Attribution to PM8b Theorems 3.14 and 3.15 matches the task context (eps < 1/(k-1),
  eps = 1/4, marginal condition, J_{i,1-eps}). I could not open PM8b to confirm that the polynomial is in §7.4; the
  project note says so.
- **WORDING (open question 6).**
  - "The orthogonal part of the constraints alone allows more than 2.14" suggests a canonical orthogonal part. Fix:
    "The clean-column constraints alone (an orthogonal subfamily) allow ...".
  - "a sharp ceiling must use the overlapping constraints" is certain only in the sense that the clean-column
    relaxation exceeds 2 at eps = 1/8. That S'_3 > S_3 is heuristic, since no upper bound below 2.14 is proved for S_3.
    Fix: "a ceiling of 2 (where it holds) cannot come from the clean-column relaxation alone".
- **WORDING (changelog 0.7).** "New Section~\ref{subsec:dual}" refers to a subsection. Use "New Subsection" or "New
  \S". The 0.7 item is otherwise accurate: 2.14, 2.06, 2 + 1.84e-4.
- **Notation clashes (WORDING).**
  - V_f, V_g (variances in the proof of thm:k2) against the subspaces V_j. Rename the variances, e.g. Var_f.
  - S (the square [0,a]^2 in thm:k2) against S_k(eps). Acceptable, but S'_3 next to S is confusing.
  - m: in DHL[k,m+1] in sec:ceil; as a coordinate index in prop:overlap ("Pick m not in {i,j}"); and as an integer
    offset in prop:k3-step. Use, say, r for the index and m in Z (stated) for offsets.
  - c is k/(k-1), c(k) is the ceiling, and "L - c/n" in rem:k3-eps uses c as a fit constant. Write "L - alpha/n".
  - u is used for t_{-j} in t-units in the lemma and for scaled coordinates in prop:k3-step (see item 5).

## Summary of findings

| # | class | location | one-line fix |
|---|---|---|---|
| 1 | ERROR | rem:k3-eps "models ... agree to 2·10^{-4}", "from n=32,40" | they agree to 2e-4 only in the first column (up to 8.6e-4 elsewhere); the quadratic model uses n = 24, 32, 40 |
| 2 | GAP | prop:overlap "Pi_K is not I - sum E_j" | add the one-line E_j v = 0 argument |
| 3 | GAP | after the lemma / clean columns | state that V_j and V'_j are closed (ranges of projections) and give the one-line disjointness argument |
| 4 | WORDING | lem:dual(2) "v(f) in V_1+...+V_k ... Pi_W P^*f" | allow v(f) in W |
| 5 | WORDING | "this is why it is sharp"; f vs (g,f) | see item 2 |
| 6 | WORDING | prop:overlap last sentences | use <1_{Z_i}, 1_{Z_j}> = vol(Z_i cap Z_j) |
| 7 | WORDING | verifier "checks that both are affine"; unscaled u, m | give the breakpoint argument and state the scaling |
| 8 | WORDING | rem:k3-eps first and third conclusions, "agree", table header | scope to the sampled eps and to the clean-column family |
| 9 | WORDING | open question 6 "orthogonal part", "must" | "clean-column constraints"; "cannot come from that relaxation" |
| 10 | WORDING | notation: V_f, S, m, c, u; changelog "Section" | rename as listed |
