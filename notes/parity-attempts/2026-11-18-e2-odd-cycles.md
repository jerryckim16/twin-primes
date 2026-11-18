# Route card: E2 pairs at a fixed difference d through odd cycles of linear forms (18 Nov 2026, Session 33)

Bounded attempt (about 1 hour). Nothing here bears on the twin prime conjecture, which stays OPEN. The parity paper is
frozen at v1.0; this card is NOT in the paper.

## Question (open item (a) of the E2 card, 2026-11-18-e2-consistency-test.md)
GGPY-b (arXiv:0803.2636v1, pp. 5-6) ask whether there is "any theoretical obstacle" to infinitely many pairs of E2 numbers
with a fixed difference d. The E2 card showed that in the linear-forms-with-multipliers model the PM8b-type parity class
blocks a target exactly when the graph of forms is bipartite (sufficiency proved, necessity checked for <= 4 forms). It
found an unblocked triangle for 12 | d and left open whether odd cycles of >= 5 forms realise d = 2.

## Model (as in the E2 card, sec. E(ii))
- Forms L_i(m) = a_i m + b_i with gcd(a_i, b_i) = 1, and the whole system admissible.
- An edge is a polynomial identity c L_i + s d = c' L_j with s = +-1 and c, c' in {1} u primes (Omega(c) <= 1 is forced:
  c L must be E2).
- On the edge event, x = c L_i(m) and x + s d = c' L_j(m) are both E2. A multiplier 1 needs L to be E2 (lambda = +1); a
  prime multiplier needs L to be a prime other than c (lambda = -1).
- The target is the union of the edge events. Weights in the class are fair, non-negative functions of
  (lambda(L_i(m)))_i. "Blocked" means: (1/2, ..., 1/2) lies in the hull of the target-free sign patterns, i.e. the
  fair version, condition (1) <=> (3) of Prop. prop:bipartite (parity paper, sec. bip). That proposition is stated for
  prime-only (monotone) targets; its proof of (1) <=> (3) carries over word for word to sign-pair targets, while the
  random-deletion step (2) => (1) does not and is not used here. Fairness itself is the heuristic of the E2 card,
  transferred from shifts to forms with different slopes and to E2 detectors; it is a model assumption, not a theorem.

## Success / no-go criteria (fixed before work)
- Success: an admissible odd cycle realising d = 2 with an exact Farkas certificate of non-blocking. That would remove the
  class obstruction for E2 pairs at distance 2.
- No-go: a proof that every admissible system for d = 2 is bipartite, so that every system is blocked.

## Result
**Proposition (Proved here; elementary; possibly folklore).** In this model:
- If 4 does not divide d, the edge graph of every admissible system is bipartite, and the target is blocked.
- If 4 divides d, there is an admissible system whose target is not blocked.

**Proof.**
1. **Gauge.** On an edge e between i and j, with required signs sigma_i^e, sigma_j^e, we have c a_i = c' a_j, so
   Omega(c) + Omega(c') = Omega(a_i) + Omega(a_j) mod 2. Hence sigma_i^e sigma_j^e = tau_i tau_j with
   tau_i = (-1)^{Omega(|a_i|)}, for every edge on the pair (i, j), whatever its multipliers. (Loops cannot occur: an
   identity c L + s d = c' L forces d = 0.)
2. **Bipartite implies blocked.** If the graph is bipartite with colouring col, put
   eps_i = tau_i (-1)^{col_i}. Then eps_i eps_j = -sigma_i^e sigma_j^e on every edge e, so neither eps nor -eps meets an
   edge's sign pair. Their midpoint is (1/2, ..., 1/2), so the target is blocked. This holds for any number of forms; it
   upgrades the E2 card's "sufficiency" to all systems with multipliers.
3. **Parity reduction (admissibility mod 2).** Fix m0 with every L_i(m0) odd. Evaluating an edge at m0 gives
   c L_i(m0) + s d = c' L_j(m0).
   - If d is odd, exactly one of c, c' is even, so it equals 2. On every edge one slope is twice the other up to an odd
     factor: v2(a_j) = v2(a_i) +- 1. Then col(i) = v2(a_i) mod 2 is a 2-colouring.
   - If d = 2 mod 4: if c were even, c' would be even too, so c = c' = 2 and L_j - L_i = s d/2 is odd. Then L_i(m0) and
     L_j(m0) have opposite parity, a contradiction. So all multipliers are odd.
4. **2-adic colouring (all multipliers odd, any d).** Let o_i be the odd part of a_i.
   Put col(i) = bit number v2(d) of b_i o_i^{-1} mod 2^{v2(d)+1}. Along an edge,
   b_j o_j^{-1} = b_i o_i^{-1} + s d/(c o_i) as 2-adic integers. The added term has valuation exactly v2(d), so the lower
   bits are unchanged and bit v2(d) flips. So the graph is bipartite. This proves the first part.
5. **4 | d.** The template T(d) for 3 not dividing d has the forms m, m+d/2, 3m+d, 3m+2d, 3m+5d/2 and the edges
   - 3 L1 + d = L3 (m prime, 3m+d E2);
   - L3 + d = L4 (both E2);
   - 2 L1 + d = 2 L2 (m, m+d/2 both prime);
   - 3 L2 + d = L5 (m+d/2 prime, 3m+5d/2 E2);
   - 2 L5 - d = 2 L4 (3m+5d/2, 3m+2d both prime).

   This is a 5-cycle. It is admissible:
   - mod 2: m odd works because 4 | d;
   - mod 3: m = 2 mod 3 works for d = 4 (in general m not 0 and m not -d/2 mod 3);
   - mod 5: the forms vanish only at m = 0, -d/2, -2d, d (L5 = 3m + 5d/2 vanishes at m = 0, the class of L1), so one
     class is free; if 5 | d they vanish only at m = 0;
   - primes p >= 7: automatic for five forms with gcd(a, b) = 1.

   An exact Farkas vector w = (1, 1, -3, -2, 0) (on the indicators of lambda = -1) gives max over target-free patterns
   -2 < -3/2 = w.(1/2, ...). So the target is unblocked. For 12 | d the E2 card's triangle m, m+d/2, m+d works. QED.

## Checks (two programs)
- code/parity/e2_odd_cycles.py [d maxlen A0 mults] (seconds; output .out): meet-in-the-middle search for odd cycles of
  length <= 5 through starts a0 <= 8, multipliers {1, 2, 3, 5, 7, 11, 13}.
  - No admissible odd cycle for d in {1, 2, 3, 5, 6, 7, 10}.
  - Admissible 5-cycles for d in {4, 8, 16, 20}; 3- and 5-cycles for d in {12, 24}.
  - With odd multipliers there is no odd cycle at all, and an assertion verifies that the 2-adic bit flips on every edge
    met (about 1e5 edges per d).
  - Sanity: the E2 card's triangle is found for d = 12.
- code/parity/e2_cycle_cert.py (independent; exact; 0.3 s; output .out):
  - verifies the template's identities and admissibility for all 200 values d <= 1200 with 4 | d, 3 not dividing d;
  - verifies the Farkas certificates (5-cycle; triangle), and that the 5-cycle has no antipodal pair of target-free
    patterns;
  - checks the bipartite construction of step 2 on 2000 random signed bipartite graphs.
- The certificate of the 5-cycle was also checked by hand: every target-free pattern has w-value <= -2.
- The file e2_odd_cycles.out concatenates the runs for d in {1, 2, 3, 4, 6, 8, 12}, each with multipliers
  {1, 2, 3, 5, 7, 11, 13} and then with the odd multipliers only (for the colouring check); the runs for d in
  {5, 7, 10, 16, 20, 24} quoted above were made with the same command and not saved.
- Fresh-context adversarial audit (helper agent, Session 33): no errors; three gaps (scope of Prop. prop:bipartite for
  sign-pair targets; list of uncovered parametrisations; fairness as a model assumption) and minor notation issues,
  all fixed in this card. The bipartite test of e2_cycle_cert.py was extended with parallel edges on the same pair.

**Sharpening (Proved here, from steps 3-4).** For 4 | d, every odd cycle contains an edge 2 L_i + s d = 2 L_j, that
is, the event "L_i(m), L_j(m) both prime at distance d/2". Reason: an edge with exactly one even multiplier is
impossible for even d (at m0 one side is even and the other odd), so without (2, 2)-edges all multipliers are odd and
step 4 makes the graph bipartite.

## Honest reading
- "Unblocked" is not "provable", and for 4 | d it says almost nothing.
  - For d = 4, x = 2p, x + 4 = 2q with p, q twin primes is already an E2 pair at distance 4. The template's edge
    2 L1 + 4 = 2 L2 IS the twin-prime event.
  - More generally, by the sharpening above every unblocked system contains a prime-pair event at distance d/2, a
    de Polignac case at least as hard as the target itself would suggest.
  - The class does not see this, because it treats every edge event as possible.
- Heuristic (not computed exactly): with fair weights the edge-wise first-moment bound sum_e (1_i + 1_j - 1) has
  expectation <= 0. A proof would need an inequality with negative coefficients, as in the Farkas vector: upper bounds for
  P(lambda(L3) = -1) and lower bounds for P(L1 prime) near the parity value 1/2. Known detection ratios (GGPY E2 ratio
  ~ 0.28 per form at k = 5, B = 4; Maynard prime ratio ~ 0.1 per form) are far below that.
- The new content is the negative half: **for d not divisible by 4 (in particular d = 2: n, n+2 both E2), no
  GGPY-type change of linear coordinates with multipliers can evade the PM8b-type parity obstruction.** This answers, in
  this model, the part of GGPY-b's question that concerns this obstruction, and closes open item (a) of the E2 card. The
  obstruction is 2-adic: it is a parity-of-the-gap phenomenon, invisible for 4 | d only because the multiplier 2 turns
  odd prime gaps into E2 gaps.

## Classification
**Proved (located), model-restricted.** No-go for d = 2 in the linear model with multipliers. Unblocked but empty
parametrisations for 4 | d.

Not covered by the no-go: multipliers depending on m (x = p L(m) with p varying, as in Chen-type set-ups),
forms in several variables, and nonlinear parametrisations. First unresolved implication: nonlinear parametrisations, e.g. x = L1 L2 with both factors prime, as in
m(m+3) + 2 = (m+1)(m+2). These give hyperedge targets that the model above does not cover. See the exploration of this
session (notes/explorations.md): every quadratic identity L1 L2 + 2 = L3 L4 found (118, a <= 6, |b| <= 24), alone or
in pairs (74), is blocked; dead end in that range.

## Literature check (scope)
- GGPY-a, GGPY-b and GGPY-c (as read for the E2 card; GGPY-b pp. 5-6 is the question).
- Two web searches (18 Nov): no source found that treats fixed-difference E2 pairs through reparametrisations, or a 2-adic
  obstruction. One low-authority page notes that even semiprimes at distance 4 are equivalent to twin primes (the
  observation in "Honest reading").
- Not searched: MathSciNet; the papers citing GGPY-b. Label: possibly folklore.

## Not to repeat
- Odd cycles with odd multipliers: impossible for every d (2-adic colouring).
- Searching for d = 2 in larger multiplier or slope ranges: pointless, the proof covers all of them.
