# Route card: odd-order Chowla inputs and the parity class (Session 38, 20 Nov 2026)

**Classification: located (proved for the model class; elementary; possibly folklore in substance).**
Not in the parity paper (v1.0 frozen). No parity-breaking content.

## Question
Besides the two-point case (Tao 2016), the parity-sensitive correlation estimates for the Liouville
function that are proved for every configuration of a given type are the **odd-order** cases of the
logarithmically averaged Chowla conjecture (Tao–Teräväinen; see Sources). Suppose a sieve argument could use them *along the sieve
weights* (this is open: the theorem is unweighted and log-averaged). Would that remove the parity
obstruction of the Liouville-pattern class (parity paper, Section `sec:bip`) for any target, in
particular twin primes?

- Success criterion: a target of twin / bounded-gap type that is blocked by fair pattern weights but
  not by pattern weights whose odd-order coefficients all vanish.
- No-go criterion: every such target is still blocked by a weight with vanishing odd coefficients.

## Model
Pattern weights Psi >= 0 on {+-1}^k killing a target family E (parity paper, `sec:bip`). In the
Möbius-randomness heuristic used there, sum_n nu(n) omega(n) prod_{i in S} lambda(n+h_i) is about
hat Psi(S) sum_n nu(n), i.e. hat Psi(S)/hat Psi(empty) times the fake-weighted sum sum nu omega. (The
same heuristic predicts that all Chowla correlations vanish for the true lambda; the fake world is only
required to match the inputs the argument may use.) So a fake weight passes the test "odd-order Chowla
along the weights" iff hat Psi(S) = 0 for every odd |S|. Scope: only lambda-only correlations with
f = 1 are modelled; Lambda-twisted odd inputs sum nu Lambda(n+h_i) chi_S(lambda) (i not in S) would
constrain hat Psi(S) - hat Psi(S u {i}), involving even coefficients, and are not provided by
Tao–Teräväinen. Hypergraphs are taken without singleton or empty edges (with a singleton edge neither
class blocks).
Classes: C1 = fair (all |S| = 1 vanish; Tao's class, `prop:bipartite`); C3 = fair and all |S| = 3
vanish; Codd = all odd |S| vanish. Codd is contained in C3, which is contained in C1.

## Results
1. **Lemma (Proved here, elementary).** Psi has hat Psi(S) = 0 for all odd |S| iff Psi(s) = Psi(-s)
   for all s (expand Psi(-s) in characters). Such Psi is automatically fair. A non-negative
   symmetric Psi killing E exists iff some E-free set I has E-free complement (take
   delta_s + delta_{-s}; conversely s and -s both lie in the support). So for a hypergraph target
   H = ([k], E): **Codd blocks iff chi(H) <= 2** (2-colourable, "property B"), while
   **C1 blocks iff chi_f(H) <= 2** (fractional chromatic number; this is condition (3) of
   `prop:bipartite`, since the E-free sets are the independent sets, which form a down-set).
2. **Corollary (Proved here).** For the target families of the parity paper and of the linear route
   cards the two classes agree: every blocked target also has an antipodal blocking pair (not always
   the measure used there): graphs (bipartite <=> 2-colourable <=> chi_f <= 2; odd cycles have
   chi_f > 2), DHL[k, m+1] with k <= 2m (a split into two classes of size <= m; the paper's measure in
   (b) is not symmetric, but such a split exists), the window targets of `prop:bipartite`(c) (odd /
   even indices), the almost-prime tuples of the Session 37 card (a pattern with between r+1-k and
   2k-r-1 minus signs and its negative), the Chen halves (weights 1 - s1 s2 and 1 + s1 s2 are even),
   and the linear E2 cards of Sessions 32-33 (any signed graph: fair-blocked <=> bipartite <=>
   antipodal pair, by averaging sum_e a_e(x_i + x_j) <= -2 on an odd cycle; this also closes the
   necessity gap of the Session 32 card, which was checked only for n <= 4). For the Session 36
   polynomial systems with odd events the blocking measures (uniform on an affine F_2-subspace) are
   not antipodal; the 60 certified systems nonetheless all have antipodal free pairs (checked by the
   auditor), but agreement for that card's general proposition is open (an abstract Fano-shaped
   system satisfies its hypotheses without an antipodal pair; realisability unknown).
   **In particular, within the class, the twin-prime obstruction 1 - lambda(n)lambda(n+2) is an even
   function of the signs: no odd-order input, at any level, removes it; for twins the parity
   information sits entirely in the even (two-point) correlation.**
3. **Fano target (Computed, exact; the finite facts Lean-checked).** k = 7, E = the 7 lines of the
   Fano plane ("all three numbers of some line are prime"). C1 blocks: mass 1/8 on the all-plus
   pattern and on each of the 7 patterns whose minus set is the complement of a line (marginals
   (7/8)(4/7) = 1/2; complements of lines contain no line since two lines always meet). Codd does not
   block: the Fano plane is not 2-colourable (all 128 colourings). Already **C3 restricted to the
   seven line triples** (the larger class in which only the singleton and the 7 line coefficients
   must vanish) does not block: on every line-free pattern,
   (1/2) sum_i s_i + (1/2) sum_L prod_{i in L} s_i >= 1, so a measure on line-free patterns with all
   singleton and line coefficients zero cannot exist. Lean: `fano_not_two_colourable`,
   `fano_fair_weight`, `fano_line_certificate`, `fanoLines_pairwise_meet` in
   lean/TwinPrimes/Fano.lean (decide; axioms propext, plus Classical.choice and Quot.sound for one).
4. **Minimality (Computed, exact certificates).** No hypergraph on k <= 5 vertices separates C1 from
   Codd; on k = 6 vertices one does, e.g. E = {45, 015, 025, 034, 124, 135, 235} with the fair
   measure 1/4 on each of the minus sets 035, 125, 134, 024 and no 2-colouring.
   Proof of the reduction: if E has no E-free set with E-free complement, the up-set G of sets
   containing an edge meets every complementary pair; take a minimal such sub-up-set G'. (a) If some
   A and A^c are both in G', take M minimal in G' with M subset of A; then M^c contains A^c, so M^c is
   in G', and removing M keeps an up-set with the covering property, a contradiction. So G' contains
   exactly one set of each complementary pair. (b) G' is intersecting: if A, B in G' are disjoint then
   A^c contains B, so A^c is in G' too. Hence G' is maximal intersecting (self-dual). Its free family
   is {A^c : A in G'} and contains the E-free sets, so C1-blocking for E implies (1/2,...,1/2) in
   conv G', i.e. tau*(G') >= 2 (LP duality; for an up-set, conv G is its dominant intersected with the
   cube). Conversely any self-dual G' with tau* >= 2 gives a separating E (its minimal sets), so k = 6
   is exactly the minimum. The script
   enumerates all self-dual monotone Boolean functions on k <= 6 variables (1, 2, 4, 12, 81, 2646:
   OEIS A001206) and certifies tau* < 2 for k <= 5 by exact fractional transversals (max tau* = 1,
   1, 3/2, 5/3, 9/5).

## Classification and first unresolved implication
Located. Odd-order Chowla, even transported to sieve weights at level x^theta (open), cannot help
with any gap or twin target of the class (the dichotomy here is odd versus even inputs along the
weights, not proved versus open); the first targets where it matters are non-2-colourable
hypergraphs with chi_f <= 2 (>= 6 positions; e.g. Fano, or three primes in arithmetic progression
among n + 210 i, i < 9, see the exploration of this session). The twin obstruction is removed
only by the two-point (even) input along the sieve weights. Unweighted and log-averaged, that input is
Tao's theorem (2016); along the weights it is open, exactly as for the odd orders. Possibly folklore in substance (Tao14b's graph
criterion already reduces twins to an even pattern); the chi versus chi_f formulation and the
minimality statement were not found in a short search (one web search; TT18 and TT17 read; Tao14b only as summarised in the parity paper, `rem:tao14b`).

## Sources read
- T. Tao, J. Teräväinen, "The structure of logarithmically averaged correlations of multiplicative
  functions, with applications to the Chowla and Elliott conjectures", arXiv:1708.02610v2 (SHA-256
  232bdb1a...a276ad), Theorem 1.1(i) p. 4 (odd order cases), Corollary 1.8 and (8), Remark 1.9 p. 8.
- T. Tao, J. Teräväinen, "Odd order cases of the logarithmically averaged Chowla conjecture",
  arXiv:1710.02112v1 (SHA-256 232dc299...369748), abstract and Section 1.
- Parity paper v1.0, `sec:bip` (definitions, `prop:bipartite`, `rem:tao14b`, `rem:marg`).

## Scripts
- code/parity/odd_chowla_class.py (/usr/bin/python3 -I; 7 s; output .out).
- lean/TwinPrimes/Fano.lean (in Audit.lean).

## Fresh-context audit (helper agent, independent scripts, 20 Nov 2026)
- Verified independently: all Fano facts and the inequality (tight: minimum exactly 2); no separation on
  k <= 5 by brute force over all down-sets (Dedekind numbers 3, 6, 20, 168, 7581) with exact Farkas
  certificates; the self-dual counts and tau* maxima; the k = 6 example; almost-prime ranges for k <= 10;
  3-APs in [9]; signed-graph E2 targets (k <= 4 exhaustive, 3000 random on k = 5, 6); the 60 certified
  Session 36 systems all have antipodal free pairs; Lean file compiles with the stated axioms. (Also:
  the class with singletons and the 28 non-line triples zero does block Fano.)
- Errors fixed: (E1) the framing said the two-point input is open; two-point log-averaged Chowla is a
  theorem (Tao 2016), only its use along sieve weights is open; (E2) the Corollary overstated the E2
  case for the Session 36 polynomial systems (now restricted, with the open point stated).
- Gaps fixed: DHL measure not symmetric (an antipodal pair exists anyway); the minimality reduction
  (two missing steps added); model scope (f = 1 only); singleton-edge convention; the ratio in the model
  paragraph. Not checked by the auditor: page numbers and hashes of TT18/TT17 (PDFs not in the repo).
