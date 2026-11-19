# E2 pairs at distance 2 through polynomial parametrisations (Chen-type multipliers, several variables)

Session 36 (11:34 AM CT slot of 19 Nov 2026). Bounded attempt (about 1.5 hours). Nothing here bears on the twin prime
conjecture, which stays OPEN. The parity paper is frozen at v1.0; this card is NOT in the paper.

## Question
The Session 33 card (2026-11-18-e2-odd-cycles.md) proved, in the linear-forms-with-constant-multipliers model, that for
4 not dividing d every admissible system is bipartite and hence blocked (no-go for E2 pairs n, n+2). It listed as
NOT covered: multipliers depending on m (Chen-type x = p L(m) with p varying), forms in several variables, and nonlinear
parametrisations (first unresolved implication: x = L1 L2 with both factors prime). Does the no-go survive these?

## Success / no-go criteria (fixed before work)
- Success (for the E2 problem): an admissible polynomial system for d = 2 whose target is not blocked, with an exact
  Farkas certificate.
- No-go: a proof that every admissible polynomial system for d = 2 is blocked, or a proof for a precisely described
  subclass together with the exact description of what remains.

## Model
- Vertices: primitive irreducible polynomials P_v in Z[m_1, ..., m_r] (any number of variables, any degree), normalised
  with positive leading coefficient. A Chen-type multiplier x = u L(m) is the product of the two vertices u and L(m).
- An event is a polynomial identity c * prod_{v in A} P_v + s d = c' * prod_{v in B} P_v (A, B multisets of vertices,
  s = +-1, c, c' in {1} u primes) in which each side has an E2 shape:
  - c = 1, |A| = 1: the vertex must be E2 (required lambda = +1);
  - c prime, |A| = 1: the vertex must be prime (required lambda = -1);
  - c = 1, |A| = 2: both vertices prime (required lambda = -1 each).
  These are necessary sign conditions; blocking for this larger target implies blocking for the real one.
- The system is admissible: in particular there is a point m0 at which every vertex is odd.
- Weights in the class: fair, non-negative functions of (lambda(P_v(m)))_v; "blocked" means (1/2, ..., 1/2) is in the
  hull of target-free sign patterns, exactly as in the Session 33 card. Fairness for nonlinear vertices is a Chowla-type
  model assumption (heuristic), as fairness for linear forms already was.

## Result
**Proposition (Proved here; elementary; possibly folklore).** Let 4 not divide d. For an admissible polynomial system
put g_v = content of the top-degree homogeneous part of P_v and
- d = 2 mod 4: eps_v = chi_4(P_v(m0)) * f(g_v), with f(n) = lambda(n) chi_4(odd part of n) (completely multiplicative);
- d odd: eps_v = f'(g_v), with f'(n) = lambda(n) (-1)^{v2(n)}.

Then on every event e, prod_{v in A_e + B_e} eps_v = - lambda(c_e) lambda(c'_e) (product over the multiset).
Consequently, with S = {eta in F_2^V : sum_{v in e} eta_v = 1 + Omega(c_e) + Omega(c'_e) for every e} (multiset sums
mod 2), S is nonempty, no sign vector (-1)^eta with eta in S meets any event, and **if no vertex indicator lies in the
F_2-span of the event supports (reduced mod 2), the uniform measure on S is fair and the target is blocked.** In
particular every system whose events all have an even number of vertices (all linear systems; all identities
L1 L2 + s d = L3 L4) is blocked.

**Proof.**
1. *Multipliers.* Evaluate the event at m0: c X + s d = c' Y with X, Y odd. If d = 2 mod 4 and c is even then c' is
   even, so c = c' = 2 and X + s d/2 = Y with d/2 odd: X, Y of opposite parity, contradiction; so c, c' are odd. If d
   is odd, exactly one of c, c' is even (= 2).
2. *Top parts.* c prod_A P - c' prod_B P is the constant -s d, so the top-degree homogeneous parts agree:
   c prod_A top(P_v) = c' prod_B top(P_v) (the top part of a product is the product of the top parts, Z[m] being a
   domain; the degrees agree because a nonconstant identity has equal top degree on both sides). Taking contents
   (Gauss's lemma: content is multiplicative) gives c prod_A g_v = c' prod_B g_v as positive integers.
3. *d = 2 mod 4.* Apply the completely multiplicative f: f(c) prod_A f(g_v) = f(c') prod_B f(g_v), so
   prod_{A+B} f(g_v) = f(c) f(c') = lambda(c) lambda(c') chi_4(c) chi_4(c') (c, c' odd). At m0 the two values
   x0 = c prod_A P_v(m0) and x0 + s d are odd and differ by d = 2 mod 4, so chi_4(x0 + s d) = - chi_4(x0), i.e.
   chi_4(c) prod_A chi_4(P_v(m0)) = - chi_4(c') prod_B chi_4(P_v(m0)). Multiplying,
   prod_{A+B} eps_v = - lambda(c) lambda(c').
4. *d odd.* From step 2, v2: v2(c) + sum_A v2(g_v) = v2(c') + sum_B v2(g_v), and v2(c) + v2(c') = 1 (step 1), so
   sum_{A+B} v2(g_v) is odd; and Omega(c) + Omega(c') = sum_{A+B} Omega(g_v) mod 2 (Omega is completely additive).
   Hence prod eps_v = (-1)^{sum Omega(g_v) + sum v2(g_v)} = - lambda(c) lambda(c').
5. *Required signs.* On each side the product of the required signs is lambda(c): (c = 1, one E2 vertex) +1;
   (c prime, one prime vertex) -1; (c = 1, two prime vertices) +1. So an event is met by a sign vector sigma only if
   prod_{A+B} sigma_v = lambda(c) lambda(c'). By steps 3-4, eps (i.e. eta_0 with eps = (-1)^{eta_0}) is in S, so S is
   nonempty; every sign vector from S has product - lambda(c) lambda(c') on every event and meets none.
6. *Fairness.* S is an affine subspace eta_0 + K, K = {eta : sum_{v in e} eta_v = 0 for all e}. A coordinate v is
   balanced under the uniform measure on S iff it is not constant on K, iff the indicator of v is not in K-perp, the
   span of the event supports. QED.

For linear forms this recovers the Session 33 colouring (eps_i = tau_i (-1)^{col_i} up to a global sign): with
g_i = |a_i| odd, chi_4(o_i) chi_4(o_i m0 + b_i) = chi_4(m0 + o_i b_i) and o_i b_i = b_i o_i^{-1} mod 4.

## What remains (honest scope)
- **Odd events with a forced vertex.** Events with |A| + |B| odd (one side a single vertex, the other two primes, e.g.
  x = u L(m), x + 2 = Q(u, m) irreducible: every Chen-type event is of this kind) can put a vertex indicator into the
  span. Then the uniform measure on S is not fair and the Proposition is silent. Example (by hand, and found by the
  search): m, m + 2 both E2, and x = m^2 + 2m - 2 E2 with x + 2 = m (m + 2), m and m + 2 prime. Here eta_x is forced, but
  the system is still blocked (uniform on (lambda(m), lambda(m+2)) in {(+,-), (-,+)}, lambda(x) uniform). In the search
  (below) every such system was blocked by the LP; no proof that this always happens.
- 4 | d: the identity fails (338 of 378 events at d = 4 violate it); unblocked linear systems exist (Session 33). The
  random small systems of the search did not find them (the sampling is weak; the 5-cycle template needs specific edges).
- d odd: proved above, but untested by the search (the generated families had no admissible odd-d system: they lack the
  multiplier-2 shapes; the per-event skips are inadmissibility mod 2).
- Outside the model: anything not expressible as fair weights of lambda-values of the vertices (genuine bilinear
  sieve information in the Chen variable p, switching, Type II input) is not covered. The model is a heuristic class.

## Checks (two programs)
- code/parity/e2_poly_gauge.py (sympy factorisation over Z, scipy LP; 10 min; output .out). Families: c L(m)
  (c in {1, 3, 5}), Chen-type u L(m), products L1 L2 in one variable, bilinear (a u + b) w, and u w; shifts s d for
  d in {1, 2, 3, 5, 6, 7, 10, 4, 8, 12}; about 370 events per d, of which 40 (d even) are skipped as not odd at any
  point of the box. Results for d = 2 mod 4 (d = 2, 6, 10): the product identity holds on every event and in every
  system; 195 + 200 + 215 random connected systems (up to 5 events, up to 12 vertices; 363-401 odd events among them),
  all LP-blocked; F_2-balanced in 192 / 195 / 214 cases; "balanced but unblocked" never occurs (as the Proposition
  requires); the remaining 3 / 5 / 1 are blocked but not balanced (the "forced vertex" case above).
- code/parity/e2_poly_gauge_check.py (independent: no sympy, no LP; 0.5 s; output .out): verifies 60 exact blocking
  certificates (d = 2; 196 events, 124 of them odd, Chen-type and bilinear included): each identity holds identically
  (5x5x5 integer grid; exact since every polynomial has degree <= 2 in each variable), multipliers and shapes are valid,
  every vertex is odd at m0, and the listed set S of sign vectors meets no event and is balanced in every coordinate.

## Classification
**Proved (located), model-restricted.** No-go for E2 pairs at distance 2 (and every d not divisible by 4) through any
polynomial parametrisation, in any number of variables and with Chen-type variable multipliers, whenever no vertex is
forced (all-even systems unconditionally). First unresolved implication: systems with odd events in which a vertex
indicator lies in the F_2-span of the event supports (blocked in every case found, not proved). The obstruction is again
2-adic (chi_4 of values and the 2-part and Liouville sign of top-degree contents).

## Literature check (scope)
- The GGPY papers and the question in GGPY-b (as for the Session 32/33 cards). No new search engine run beyond what the
  Session 33 card records; possibly folklore. We claim nothing about the actual E2 problem.

## Audit
See below (fresh-context adversarial helper; mathbox not available).

## Not to repeat
- Polynomial reparametrisations with constant multipliers and all-even events, for 4 not dividing d: covered by the proof.
- Chen-type x = u L(m) set-ups inside the fair-weight class: covered except for the forced-vertex case.
