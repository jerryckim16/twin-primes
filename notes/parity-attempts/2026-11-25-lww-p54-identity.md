# Route card: the M_R operator identity of LWW Section 4.7, pp. 53-54 (2026-11-25, Session 54)

**Classification: proved under reading R1 (R1 is supported by the text but not stated in it; audited, fixes applied).**
The per-prime algebra D2-D5 is proved unconditionally; the full identity
M_R(u,v,r) = prod_p b'_p * <b, G_0 O_0 G_1 ... O_{2R-1} G_{2R} b>_distinct holds under R1. I derived each step
(Proved here) and checked (a), (b), the per-prime operator factor (c), and a global toy operator model (d) exactly
in rational arithmetic (Computed). No sign, missing term, b'_p, V_i or distinctness error was found.
- The reading (R1 below, stated precisely after the audit): the weights listed on p. 48 are a(s,t)m(t), and the
  measure m (including nu_i and the 1/k_i! of the auxiliary tuples) is taken at the leftmost state of <.,.> only;
  so each prime-tuple entry and each auxiliary pair carries nu_i exactly once, when it is introduced, and the
  factorials never enter the identity. p. 48 states the operator weights descriptively and does not spell out how the
  kernels of G_j, O_j are normalised against the measure m(t). Audit F1: (4.122) does NOT force R1 (it tracks only
  theta and V_i); the literal reading L (p. 48 weights = kernels, p. 49 multiplies by m(t) at every step) fits
  (4.122) equally well and breaks the identity (path-dependent extra factors, e.g. 12/17 and 144/289 for p = 3,
  A_p = {0,1}, {0,1,2}). The evidence for R1 is p. 49: the row/column factors contain s_i once per appended pair,
  and ||b||^2 = prod s_i^{J+1} puts the measure on the left state. A mixed reading (nu once, factorials at every
  step) also breaks it.
- This checks one internal identity of the proof of Prop. 4.6 (feeding Prop. 4.2, p. 18). It is a correctness check
  of a step, not of Prop. 4.2. The estimates after p. 54 ((4.138)-(4.147)) are not checked here.

## Source
arXiv:2610.20242v2 PDF, scratch copy (not committed), SHA-256
`7ac341311b4a648c32c2b23b3029e1f4a3202258b55614a33ba7e8282423d000` (re-verified this session). pdftotext -layout. PDF
page = printed page.

## Criteria (written before the derivation)
- Success: every step from the definition of M_R ((4.93)) to the displayed identity on p. 54 is either derived in
  full here or verified by an exact finite check. Every terse place is made explicit.
- No-go / finding: a step false as printed (sign, missing term, wrong normalisation such as b'_p, an overcount from
  distinctness, a miscounted V_i), with a counterexample from an exact computation.

Outcome: success criterion met, with the reading R1. No-go not triggered.

## Question
Previous card (2026-11-25-lww-prop42-thinning.md, "Possible issues"): "Multiplication over p proves the identity
below" (p. 54) is the least explicit step of Section 4.7 and was not re-derived. Is it correct?

## What was read (this session, line by line)
- pp. 35-36: (4.90) S_ell (starts p. 35; tuples have distinct entries), T_{1,ell}, K_{1,ell} (with rho^{(omega_ell(z)+omega_ell(z'))/2 - K(J+1)}), (4.91), (4.92),
  **(4.93)** M_R = prod_{p in ∪P_i} (p+1)^{-1} sum_ell <u_{z0}, (A A*)^R u_{z0}>_ell, with
  <f1,f2>_ell = prod_i V_i^{-(J+1)} sum_{S_ell}.
- p. 7: (2.12), the sets P_i are disjoint (needed in D1; audit F3).
- p. 38: (4.99), **(4.100)** a_ell (prefactor 1/((J+1)!)^{2K}, quoted after the audit and taken as common to both
  sides, not checked; factor prod_i 1/V_i per step; p'_{i,sigma(J+1)} not in the current tuple),
  **(4.101)** the path sum over (z_j, p^(j)), z_0 = z_{2R} = (1,0)^T; p. 39: (4.102); p. 42: **(4.111)** F(ell).
- p. 45: the main term reproduces the summands of (4.101) (context only).
- p. 47: (4.118) Z_0, (4.119) O, **q_0 = q_{2R} = sqrt(rho), q_j = rho, eta'_j = 1 - q_j**, **(4.120)**
  b'_p = 1 - sum_{j=0}^{2R} eta'_j/(p+1), nu_i(p) = 1/(V_i (p+1) b'_p), (4.121); m_i (ordered k_i-tuples of
  pairs (p, ell), repeats allowed); X_i, lambda_i(p, ell) = nu_i(p); measure weights (prime tuple prod nu_i,
  m_i: prod lambda_i / k_i!).
- p. 48: definition of G_j (remove matching pairs: -eta'_j/theta each; retained matching: q_j/theta^2; append l
  ordered pairs (p_a, [z]_{p_a}): (1/l!) prod (-eta'_j V_i/theta) nu_i(p_a)) and of O_j (shared entries with
  [z]_p = [z']_p for p | D; subsets S; departing entry appended to m_i or discarded; unshared entry from m_i
  (factor 1/V_i, only pairs present before the operation) or summed with nu_i; damping theta^{h_s+h_t});
  **(4.122)** theta (q_j/theta^2) theta = q_j.
- p. 49: kernel convention T f(s) = sum_t a(s,t) f(t) m(t); factorial identities for adjoints.
- p. 50: (4.128) z = B_D k. It is used only in the arc estimate (4.133)-(4.134), p. 53, not in the identity.
- **pp. 53-54**: Proposition 4.6, (4.136), A_p, (4.137), the two expansions, the distinctness convention, the
  kappa_p factors, the l! remark, the definition of b and the identity. p. 55 (E_mem) as context only.
- [z]_p is the line of z in P^1(F_p) (Section 4.4, (4.84) context; not re-read this session).

## Derivation (Proved here unless labelled)
**D1. Per-prime form of M_R.** Insert (4.100) into (4.101) and (4.93). For a fixed path (z_j, tuples p^(j), fixed
permutations) everything except the rho-powers, the 1/V_i factors and the line indicators is common to both sides.
- rho-powers: prod_{j<2R} rho^{(omega(z_j)+omega(z_{j+1}))/2} gives z_j the exponent 1/2 at j = 0, 2R and 1
  otherwise, i.e. prod_p prod_j q_j^{1[ell_p = [z_j]_p]}. The K(J+1) tuple primes at each z_j satisfy the indicator,
  so they contribute prod_j q_j^{K(J+1)} = rho^{2RK(J+1)}. This cancels the 2R kernel factors rho^{-K(J+1)}. What is
  left is prod_{j in A_p} 1[ell = [z_j]_p] prod_{j not in A_p} (1 - eta'_j 1[ell = [z_j]_p]). Averaged with
  1/(p+1) over ell, this is (4.137).
- V-powers: V_i^{-(J+1)} from <.,.>_ell and V_i^{-1} per step from (4.100). Each entry of a prime into a tuple
  costs 1/V_i. A prime p in P_i whose occupancy set A_p has kappa_p maximal intervals pays V_i^{-kappa_p}, and
  sum_{p in P_i} kappa_p = J+1+2R. So M_R = sum over paths of [common factors] * prod_p V_i^{-kappa_p} (4.137)_p.
- The text writes "gives the factor (4.137)" and leaves the rho-cancellation implicit. It is correct.

**D2. A_p = empty (p. 53-54).** Put x_j = eta'_j 1[ell = [z_j]_p]. Expand prod_j (1 - x_j) as
sum_S (-1)^{|S|} x^S. S = empty gives 1. |S| = 1 gives -x_a. For |S| >= 2 with min a and max c, the middle indices
sum to x_a x_c prod_{a<j<c} (1 - x_j). Averaging over ell: (1/(p+1)) sum_ell (1 - sum_a x_a) = b'_p, and x_a x_c
forces ell = [z_a]_p = [z_c]_p. This gives the printed display exactly, with the sign + in front of the double sum.

**D3. Prefix/suffix identities (p. 54).** These are telescoping sums.
prod_{h<=j<a} (1-x_j) - prod_{h<j<a} (1-x_j) = -x_h prod_{h<j<a} (1-x_j). Summed over h < a this gives the prefix
identity. The suffix identity is the mirror image. Both are as printed.

**D4. Operator side, one prime (reading R1).** Fix p in P_i and A_p. Under distinctness p is *selected* exactly
once: in a tuple at z_0, as a nu_i-summed entry in some O_j, or as a pair appended by some G_h. Its life is a word
in {fresh, in tuple, in m_i with line ell, gone}. Weights:
- Theta: a matching pair at internal j contributes theta (O_{j-1}, h_t) times q_j/theta^2 or -eta'_j/theta (G_j)
  times theta (O_j, h_s), i.e. q_j or -eta'_j. Appending at G_a gives (-eta'_a V_i/theta) theta. This is (4.122).
  Boundary terms balance only because b forces m empty at both ends. This is "empty initial and final auxiliary
  tuples leave no unmatched theta-factors". I checked it with theta = 9/10 and 2/3 in (d).
- A_p empty: either p is never selected (1), or it is appended at G_a and removed at G_c, c > a. Weight
  nu_i V_i eta'_a eta'_c 1[[z_a] = [z_c]] prod_{a<j<c} (1 - x_j), with retained-but-not-matching steps giving 1.
  Since V_i nu_i(p) = 1/((p+1) b'_p) **by definition (4.120)** (not an approximation), this is D2's right side divided
  by b'_p.
- A_p nonempty, a = min, c = max. Inside an interval the shared-entry rule [z]_p = [z']_p fixes one line ell_0.
  - Prefix before a: either p enters fresh (nu_i, or the measure at z_0) or comes from a pair appended at G_h
    (h < a) and moved in by O_{a-1} (1/V_i), giving -eta'_h V_i nu_i prod_{h<j<a}(1-x_j) / V_i. The sum is
    nu_i prod_{j<a} (1 - x_j(ell_0)) by D3.
  - Gaps between intervals: the departing entry must be appended to m_i (S option). Discarding it would force a
    second independent selection, which is excluded. It is retained ((1 - x_j) at each gap index) and moved back in
    (1/V_i, line must equal [z_{a'}]_p).
  - Suffix after c: discard (1) or append and later remove by G_h (-eta'_h), giving prod_{j>c} (1 - x_j) by D3.
  - Total: nu_i V_i^{-(kappa_p - 1)} 1[[z_j]_p const on A_p] prod_{j not in A_p} (1 - x_j(ell_0))
    = V_i^{-kappa_p} (4.137) / b'_p. Both "first in a tuple" and "first in G_j" give V_i^{-kappa_p}/((p+1)b'_p), as
    printed.
- Ratio operator/M_R = 1/b'_p for every p in ∪P_i, including untouched primes. Multiplying over p gives the
  identity.

**D5. Distinctness and l!.** Distinctness is a per-prime constraint ("selected at most once"), so the operator sum
factorises over p exactly as M_R does. The tuple paths correspond bijectively:
- M_R requires the new entry p'_i not to be in the current tuple ((4.100)).
- On the operator side this is "a pair appended during this operation cannot supply p'_i" (p. 48) together with
  distinctness.
An unordered set of l distinct appended pairs arises from l! ordered tuples, each with weight 1/l!. There is no
overcount and no missing term.

**Terse points made explicit**
- (T1) The rho-cancellation in D1. p. 53 says only "gives the factor".
- (T2) Reading R1: p. 48 lists weights "of" G_j, O_j (including nu_i(p_a) for appended pairs and nu_i for fresh
  entries). With the kernel convention of p. 49 (T f(s) = sum_t a(s,t) f(t) m(t)), the measure m(t) on p', m' must
  be divided out of the kernels for retained entries and retained pairs. Otherwise retained entries would pick up
  nu_i at every step. This is not stated. Under R1 the identity holds; under the literal reading L it fails, and L is
  also consistent with (4.122) (audit F1, correcting the draft, which said R1 was forced by (4.122) and the p. 54
  kappa_p sentence; that sentence is the claim under test). R1 is the reading supported by p. 49 (see above), so
  "terse, not wrong" is kept, but R1 is an interpretive choice.
- (T6, slip in LWW, audit F5) p. 48: "a pair appended by G_j contributes -eta'_j V_i" omits the factor nu_i(p_a)
  contained in the G_j weight. Harmless.
- (T3) The S-option bookkeeping in the gaps (append is forced, discard is excluded) is stated on p. 54 only as "the
  pair for p must remain in m_i".
- (T4) "For A_p = empty we recover (4.137) divided by b'_p" means the A_p = empty display of p. 54 equals
  [(1/(p+1)) sum_ell prod_j (1 - x_j)] / b'_p. This follows from D2.
- (T5) The removal option at G_{2R} matters: the A_p = empty terms with c = 2R and the suffix terms with h = 2R
  carry -eta'_{2R} = -(1 - sqrt(rho)). They are needed and they are present.

## Computation (Computed)
`code/parity/lww_p54_identity_check.py`, output `code/parity/lww_p54_identity_check.out`. Run with
`/usr/bin/python3 -I`, fractions.Fraction, exact.
- (a) The A_p = empty identity: 300 random cases, p in {2,3,5,7}, R in {1,2,3}, random lines in {0..p}, random
  rational eta'_j (not tied to rho). 0 failures.
- (b) Prefix/suffix identities: 300 random cases each. 0 failures.
- (c) Single-prime state-machine model of G_j/O_j (R1 weights, theta-damping, rules of p. 48), for random A_p,
  lines, eta'_j, V, theta. The model output equals V^{-kappa_p} (4.137)/b'_p in all ~400 cases.
- (d) Global toy model, K = 1, J + 1 = 2, P_1 in {{2,3,5}, {2,3,5,7}}, R in {1,2}, z_{2R} = z_0. Two sides:
  - LHS: built from (4.100)/(4.101)/(4.111): rho^{-K(J+1)} per kernel, q_j from rho, V^{-1} per entry, the 1/(p+1)
    line average.
  - RHS: a literal enumeration of G_0 O_0 ... G_{2R} on states (tuple, ordered m, selected set), with ordered
    appends weighted 1/l!.
  - Not modelled: the geometric factors, which are common to both sides.
  - Results: 13 cases (6 with {2,3,5}, R=1; 4 with {2,3,5}, R=2; 3 with {2,3,5,7}, R=1,1,2), all with nonzero M_R
    (e.g. 3125000/47258883). In every case LHS = prod b'_p * RHS exactly, for both theta = 9/10 and 2/3.
  - Negative controls (both make the comparison fail, so the toy is sensitive to the rules):
    - dropping distinctness (6 cases, R = 1, at most 2 appends per G_j): unequal in all 6;
    - letting a pair appended in O_j supply p'_i in the same O_j: unequal in all 13.
  - Runtime: about 30 s when re-run by the coordinator (output identical; the helper reported ~15 min, probably
    including development runs).
  - Limits (audit F6): not circular (the LHS uses no nu or b'_p), but the RHS builds R1 in, so (d) checks the
    bookkeeping under R1, not R1 itself; K = 1, so independence across groups is untested; tuples are sets, so the
    permutation factors are untested; the no-distinctness control changes two things at once and has 6 cases. A
    reading-L control (which should fail) was not added; the auditor's hand computation for p = 3 shows it fails.
- Degenerate parameters with b'_p = 0 (e.g. p = 3, R = 2, sqrt(rho) = 1/3) are skipped. LWW has b'_p > 0 for large x
  ((4.121)).

## Classification
**Proved under R1** (R1 is supported by the p. 49 kernel factors and ||b||^2, but not stated in LWW; the literal
reading L breaks the identity). The per-prime algebra D2-D5 is proved unconditionally. No error in LWW found
beyond the harmless slip T6.

## Audit (fresh-context adversarial, 2026-11-25)
notes/parity-attempts/2026-11-25-lww-p54-identity-audit.md: verdict "holds with fixes"; D1-D5 re-derived, no
sign, b'_p, kappa_p, gap/append, distinctness or l! error. Findings: F1 overstatement (R1 not forced by (4.122)),
F2 gap (R1 imprecise about 1/k_i!), F3 gap (D1 needs distinct tuple entries and disjoint P_i; permutation
prefactor unchecked), F4 slip (pages), F5 slip in LWW, F6 overstatement (what toy (d) shows), F7 overstatement
("holds as printed"). All applied above.

## First unresolved implication
None inside pp. 53-54. Next in line: the bounds that use the identity, i.e. E_mem and (4.138)-(4.147), pp. 55-58.
Robustness under thinning was checked in the previous card, correctness was not. [17] (the source of the G_j/O_j
construction) is unread.

## What this does NOT show
- Not that Prop. 4.6 or Prop. 4.2 is correct. Only this identity was checked. LWW remains Claimed, unrefereed.
- Not the norm bounds (4.125)-(4.135) or the estimates after p. 54.
- The toy (d) has K = 1, J = 1, at most 4 primes, R <= 2, random lines rather than lines of actual lattice
  vectors, and no geometric kernel. Faithfulness to the general case rests on the per-prime factorisation D4/D5
  (Proved here), not on the toy.
- Nothing about twins (K = 0) and no parity-breaking content.
- Not opened: [17], [4], [19]; Section 4.4 definition of [z]_p not re-read this session.
