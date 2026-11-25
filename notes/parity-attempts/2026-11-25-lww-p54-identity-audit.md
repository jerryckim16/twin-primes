# Audit: route card 2026-11-25-lww-p54-identity.md (LWW Section 4.7, pp. 53-54, M_R operator identity)

Fresh-context adversarial audit, 2026-11-25. I read pp. 18-20 ((4.19)-(4.23), (4.32)), p. 7 ((2.12)), pp. 35-39,
42 and 47-55 of arXiv:2610.20242v2 (scratch pdftotext). I read the card and the whole script. I did not re-run the
script. I ran one small check of my own (single-prime model, reading L below), not committed.

**Verdict: the classification holds with fixes.** I re-derived the identity under R1 and found no sign, b'_p,
kappa_p, gap/append, distinctness or l! error. The fixes concern how R1 is justified and how strongly the result
is stated.

## Findings

**F1 (overstatement): (4.122) does not force R1.** The card (header, T2, Classification) says R1 is "the only
reading consistent with (4.122)". But (4.122) and the two sentences after it (p. 48, last lines) only track the
theta and V_i factors. The sentence "a pair appended by G_j contributes -eta'_j V_i" even drops the nu_i(p_a) that
the G_j weight contains. So these lines say nothing about where the measure goes.
- The literal reading L: the p. 48 weights are the kernels a(s,t), and the p. 49 convention
  T f(s) = sum_t a(s,t) f(t) m(t) multiplies by the full m(t) at every step. L is equally consistent with (4.122).
- Under L the identity fails. A prime held in the tuple over |A_p| indices picks up nu_i^{|A_p|-kappa_p} extra
  factors, so the ratio to M_R depends on the path. My check: p = 3, A = {0,1}, {0,1,2} give extra factors 12/17 and
  144/289 against the R1 value.
- The p. 54 sentence ("nu_i(p) V_i^{-(kappa_p-1)}") is the claim under test, so it cannot be used to fix the reading.
- Better evidence for R1, which the card does not cite:
  - The p. 49 row/column factors exp(v0 eta'_j V_i s_i q_j/theta + ...) contain s_i = sum nu_i exactly once per
    appended pair, and no tuple or m measure. That is exact only if the p. 48 weights are a(s,t)m(t).
  - ||b||^2 = prod s_i^{J+1} (p. 54) puts the tuple measure on the left state of <.,.>.
- Fix: replace "forced by (4.122)" with "supported by the p. 49 Schur-test bookkeeping and ||b||^2; the text is
  ambiguous". "Terse, not wrong" stays fair, because R1 is the natural reading of "the weight is", but it is an
  interpretive choice.

**F2 (gap): R1 is not stated precisely.** "Each entry carries nu_i exactly once, when introduced" leaves out the
1/k_i! in the m_i measure (p. 47). Precise R1:
- The p. 48 weights are the transition weights a(s,t)m(t).
- <f,g> = sum_s f(s) g(s) m(s), with m taken at the leftmost state only.
- Then 1/k_i! never enters the identity, because b has empty m at both ends. A mixed reading (nu once, but 1/k'! from
  m(t) at each step) also breaks the identity.
- Fix: state R1 this way and note that the m-measure factorials matter only for adjoints and norms (p. 49).

**F3 (gap, minor): D1's "everything else is common" leans on facts the card does not cite.**
- The rho^{-K(J+1)} cancellation and sum_p kappa_p = J+1+2R both need two things: tuple entries pairwise distinct
  (p_{i,j} != p_{i,h} in (4.90), p. 35) and the sets P_i pairwise disjoint ((2.12), p. 7). Otherwise omega_ell(z_j)
  counts fewer than K(J+1) tuple primes. Both hold, so the derivation is correct.
- The 1/((J+1)!)^{2K} (pi, sigma) factor of (4.100) is called "common" because O_j "keeps the permutations in
  (4.32)" (p. 48). The card never quotes that factor, and the toy cannot test it (it uses unordered 2-sets on both
  sides).
- Fix: cite (4.90) and (2.12), quote the full (4.100) prefactor, and add one line on why the count of (pi, sigma)
  per ordered tuple pair (J!^K) is the same on both sides.

**F4 (slip): page references.** (4.90), the S_ell definition with 2 ∤ z_1, g~z in Omega' and distinctness, starts on
p. 35, not p. 36. The card's reading list omits p. 35. The quote of (4.100) omits the 1/((J+1)!)^{2K} prefactor and the
pi, sigma sum. The other quotes check out against the source with correct pages: (4.93), (4.101), (4.111),
(4.118)-(4.122), b'_p, nu_i, q_j, eta'_j and the G_j/O_j rules.

**F5 (slip, LWW): the sentence after (4.122) is imprecise.** "A pair appended by G_j contributes -eta'_j V_i"
should read -eta'_j V_i nu_i(p_a). This is harmless, but the card cites the sentence as support for R1 when it
should flag it. Fix: say so in T2.

**F6 (overstatement): what the toy (d) shows.**
- The toy is **not circular**. mr_side is built only from rho-powers (q_j^{1[l=[z_j]]} over all j, including tuple
  indices), V^{-(2+2R)}, rho^{-4R}, the ell-average and the rule "new not in T". It contains no nu or b'_p. op_side
  enumerates G_j/O_j directly. Equality is therefore a real test.
- But op_side *encodes* R1: nu only at z_0 and at fresh or appended selections, plain listed weights otherwise. So
  (d) tests the combinatorics given R1, not R1 itself.
- It also has K = 1, so the independence across groups (subsets S, sets I) is untested. Tuples are sets, so the
  permutation factors are untested.
- The "no distinctness" control changes two things at once (it also truncates l <= 2) and is run on 6 cases only.
  It shows sensitivity, not which rule matters.
- Fix: say "(d) checks the bookkeeping under R1", and add a reading-L control, which should fail.

**F7 (overstatement): "holds as printed".** The identity holds as printed only once a reading the text does not
state is supplied. The geometric and permutation factors (F3) are argued, not checked. Fix: "Proved under R1 (R1 is
textually supported, not stated); the per-prime algebra D2-D5 is proved unconditionally."

## Checked and correct (no finding)
- D1 rho-powers: the tuple primes give prod_j q_j^{K(J+1)} = rho^{2RK(J+1)}, which cancels the 2R kernel factors
  rho^{-K(J+1)}. The leftover is (4.137).
- V-powers: V_i^{-(J+1)} from <.,.>_ell times V_i^{-1} per step equals prod_p V_i^{-kappa_p}, because each step
  opens exactly one interval (p'_{i,sigma(J+1)} is not in the current tuple, (4.100)).
- D2: the min/max grouping, the sign + and the average 1 - sum_a x_a, which gives b'_p. D3: both telescoping
  identities.
- D4 theta balance: O_{j-1}'s h_t and O_j's h_s around G_j give q_j, -eta'_j, or a single theta for an append.
  Pairs appended or moved by O_j are counted correctly. The boundaries balance because m is empty at both ends.
- Prefix: fresh nu_i, or append at G_h then 1/V_i via the I option with [z_h]_p = [z_a]_p. This gives nu_i times
  the prefix product.
- Gap: append is forced and discard is excluded by distinctness. Each gap index gives (1 - x_j), and moving the pair
  back gives 1/V_i with the line check.
- Suffix: discard or append, then removal by G_h, h > c.
- The ratio is 1/b'_p for every p, including untouched primes, since V_i nu_i(p) = 1/((p+1) b'_p) exactly (4.120).
- D5 token argument: each prime is selected once and is located in {tuple, m, gone}. The I option cannot reuse the
  departing prime or a pair appended in the same operation. The l! orderings of the distinct primes appended in one
  G_j, each with weight 1/l!, are each followed by equal continuation weights.
- Script (a)-(c) implement the stated formulas faithfully. In (c) the target is computed independently of the model.
