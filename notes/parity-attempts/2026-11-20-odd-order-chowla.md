# Route card: odd-order Chowla inputs and the parity class (Session 38, 20 Nov 2026)

**Classification: located (proved for the model class; elementary; possibly folklore in substance).**
Not in the parity paper (v1.0 frozen). No parity-breaking content.

## Question
The only parity-sensitive correlation estimates for the Liouville function that are proved for every
configuration of a given type are the **odd-order** cases of the logarithmically averaged Chowla
conjecture (Tao–Teräväinen; see Sources). Suppose a sieve argument could use them *along the sieve
weights* (this is open: the theorem is unweighted and log-averaged). Would that remove the parity
obstruction of the Liouville-pattern class (parity paper, Section `sec:bip`) for any target, in
particular twin primes?

- Success criterion: a target of twin / bounded-gap type that is blocked by fair pattern weights but
  not by pattern weights whose odd-order coefficients all vanish.
- No-go criterion: every such target is still blocked by a weight with vanishing odd coefficients.

## Model
Pattern weights Psi >= 0 on {+-1}^k killing a target family E (parity paper, `sec:bip`). In the
Möbius-randomness heuristic used there, the sieve-weighted sum of prod_{i in S} lambda(n+h_i) under the
fake weight is about hat Psi(S) / hat Psi(empty) times the unweighted sieve sum. So a fake weight
passes the test "odd-order Chowla along the weights" iff hat Psi(S) = 0 for every odd |S|.
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
2. **Corollary (Proved here).** For every target treated in the parity paper and in the route cards
   the two classes agree, because the blocking measures used there are 2-colourings:
   graphs (bipartite <=> 2-colourable <=> chi_f <= 2, odd cycles have chi_f > 2), DHL[k, m+1] with
   k <= 2m (two classes of sizes <= m), the window targets of `prop:bipartite`(c) (odd / even
   indices), the almost-prime tuples of the Session 37 card (a pattern with between r+1-k and 2k-r-1
   minus signs and its negative), the Chen halves (weights 1 - s1 s2 and 1 + s1 s2 are even), the E2
   cards (bipartite signed graphs have antipodal target-free pairs, as code/parity/e2_cycle_cert.py
   already records). **In particular the twin-prime obstruction 1 - lambda(n)lambda(n+2) is an
   even function of the signs: no odd-order input, at any level, removes it; for twins the parity
   information sits entirely in the even (two-point) correlation.**
3. **Fano target (Computed, exact; the finite facts Lean-checked).** k = 7, E = the 7 lines of the
   Fano plane ("all three numbers of some line are prime"). C1 blocks: mass 1/8 on the all-plus
   pattern and on each of the 7 patterns whose minus set is the complement of a line (marginals
   (7/8)(4/7) = 1/2; complements of lines contain no line since two lines always meet). Codd does not
   block: the Fano plane is not 2-colourable (all 128 colourings). Already **C3 restricted to the
   seven line triples** does not block: on every line-free pattern,
   (1/2) sum_i s_i + (1/2) sum_L prod_{i in L} s_i >= 1, so a measure on line-free patterns with all
   singleton and line coefficients zero cannot exist. Lean: `fano_not_two_colourable`,
   `fano_fair_weight`, `fano_line_certificate`, `fanoLines_pairwise_meet` in
   lean/TwinPrimes/Fano.lean (decide; axioms propext, plus Classical.choice and Quot.sound for one).
4. **Minimality (Computed, exact certificates).** No hypergraph on k <= 5 vertices separates C1 from
   Codd; on k = 6 vertices one does, e.g. E = {45, 015, 025, 034, 124, 135, 235} with the fair
   measure 1/4 on each of the minus sets 035, 125, 134, 024 and no 2-colouring.
   Proof of the reduction: if E has no E-free set with E-free complement, the up-set G of sets
   containing an edge meets every complementary pair; a minimal such sub-up-set G' is a maximal
   intersecting family (if M is a minimal set of G' with M^c in G', removing M keeps an up-set with
   the covering property). For self-dual G', the free family of G' is {A^c : A in G'}, so C1-blocking
   for E implies (1/2,...,1/2) in conv G', i.e. tau*(G') >= 2 (LP duality for up-sets). The script
   enumerates all self-dual monotone Boolean functions on k <= 6 variables (1, 2, 4, 12, 81, 2646:
   OEIS A001206) and certifies tau* < 2 for k <= 5 by exact fractional transversals (max tau* = 1,
   1, 3/2, 5/3, 9/5).

## Classification and first unresolved implication
Located. Odd-order Chowla, even transported to sieve weights at level x^theta (open), cannot help
with any gap or twin target of the class; the first targets where it matters are non-2-colourable
hypergraphs with chi_f <= 2 (>= 6 positions; e.g. Fano, or three primes in arithmetic progression
among n + 210 i, i < 9, see the exploration of this session). The twin obstruction needs the
two-point (even) input, which is the open problem. Possibly folklore in substance (Tao14b's graph
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

## Audit
See the section "Fresh-context audit" below (added after the helper's report).
