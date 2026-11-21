# Route card: Linnik's identity and the convolution-depth ladder on rough pairs (21 Nov 2026)

**Classification: located (no-go inside the paper's class; elementary, possibly folklore; computed).**
Not in the parity paper (v1.0 frozen). No progress on twin primes and no way around parity.

## Question
Linnik's identity writes Λ(n)/log n as an alternating sum of the counts d'_j(n) of ordered
factorisations into j factors ≥ 2. On z-rough n (all prime factors > z = X^{1/J}) the sum stops at
j ≤ J − 1, so the twin count on rough pairs is a finite combination of the correlations
S_{j,j'} = Σ_{n ≤ X−2} R(n)R(n+2) d'_j(n) d'_{j'}(n+2). Which S_{j,j'} are known, are they
parity-blind, how much do errors get amplified, and how does this relate to the bipartite
criterion (paper Prop. `prop:bipartite`)?

- Success criterion: some S_{j,j'} (in particular one with j = 1 or j' = 1) has a known asymptotic,
  unconditionally or under EH, and this asymptotic is not implied by parity-blind data, i.e. data
  left unchanged by the fair weights 1 + cλ(n)λ(n+2) of the paper's class.
- No-go criterion: the ladder is a change of basis inside the table of factorisation types of
  (n, n+2); every rung with a known or EH-accessible asymptotic is parity-blind, and the twin count is
  not in the span of parity-blind functionals.

## Sources read (PDFs in /tmp/claude-0/linnik/, not committed; SHA-256 of the copies read)
- Matomäki, Radziwiłł, Tao, "Correlations of the von Mangoldt and higher divisor functions I. Long
  shift ranges", arXiv:1707.01315v3 (SHA-256 e93924c5a97b7813320ca84dcbf4619a958b47781e2e7ab36f6e2fd11a9493a1),
  PDF pp. 2-7: Conjecture 1.1 (6)-(10), Remark 1.2, Section 1.1 "Prior results".
- Ford, Maynard, "On the theory of prime-producing sieves", arXiv:2407.14368v1
  (SHA-256 3ca8078509f8f9e7cf52ca943a1599a714e23c1387ae27bbd0845998d76d2301), PDF pp. 1-4 (the (I)/(II)
  setup, Selberg's example, Theorems 2.1-2.2) and pp. 19-22 (Linnik's identity, (5.1), Lemmas 5.3-5.5).

## What the sources say (Literature, opened)
1. Linnik's identity, as stated in FM p. 19 (unnumbered display before (5.1); they cite Linnik's
   book [19, 0.6.13] and Friedlander–Iwaniec §17.2, neither opened):
   Λ(n)/log n = Σ_{j≥1} (−1)^{j+1}/j · #{d_1⋯d_j = n : d_i > 1}. It holds for every n ≥ 2. Prime
   powers are not excluded: at n = p^k both sides equal 1/k. FM Lemma 5.5(b) (pp. 21-22) is a vector
   analogue: L_c(x) = 1(k = 1) when |x| < c.
2. FM p. 2: Selberg's example a_n = 1 + λ(n), b_n = 1 satisfies the Type I estimate (I) for every
   γ < 1 but has no primes, "so non-trivial Type II information is necessary to detect primes".
   Theorem 2.1 (p. 3): for every γ < 1 there is ν_0(γ) > 0 such that a Type II range of length
   ν ≤ ν_0 does not suffice either.
3. MRT p. 2: Λ "behaves similarly in many ways to the divisor functions d_k for k moderately large".
   The Linnik and Heath-Brown identities give the explicit connection.
4. MRT p. 6 (binary divisor problem). For k = l = 2 the asymptotic is known with error X^{2/3+o(1)}
   (Deshouillers–Iwaniec). For d_2(n)d_l(n+h) with l ≥ 3, power savings are known ([6], [14], [76]).
   "When k, l ≥ 3, no unconditional proof of even the weaker asymptotic … is known", although upper and
   lower bounds of the right order are. MRT p. 4 calls k = l = 3 "a notorious open problem".
   Baier–Browning–Marasingha–Zhao handle d_3d_3 for almost all h in a window of length H ≥ X^{1/3+ε}.
5. MRT pp. 6-7 (Titchmarsh). For k = 2 the asymptotic of Σ Λ(n)d_2(n+h) is due to Linnik, sharpened by
   Fouvry and Bombieri–Friedlander–Iwaniec to O_A(X log^{−A} X) and by Drappeau. "When k ≥ 3 even the
   weaker estimate … remains open; sieve theoretic methods would only give this asymptotic assuming a
   level of distribution of Λ that is greater than 1 − 1/k, which would follow from EH but is not known
   unconditionally for any k ≥ 3". So for Λd_k the stated obstruction is the **level of distribution**,
   and EH removes it for each fixed k. For d_kd_l with k, l ≥ 3 the source gives no reason. That this
   obstruction is depth or level and not parity is our reading (Heuristic, item H1 below).

## Findings
**F1 (Proved here; folklore). The rough truncation.** Put z = X^{1/J} and let R(n) = 1 when n ≥ 2 has
every prime factor > z. If R(n) = 1 and n ≤ X, then Ω(n) ≤ J − 1 (Ω ≥ J would force n > z^J = X).
Hence d'_j(n) = 0 for j ≥ J. If such an n is squarefree with Ω(n) = r, an ordered factorisation is a
surjection from the r primes onto j labelled factors, so d'_j(n) = j!·S(r, j). Linnik then reads
Σ_j (−1)^{j−1}(j−1)! S(r, j) = [r = 1]. Proof: Σ_r S(r,j) t^r/r! = (e^t − 1)^j/j!, and
log(1 + (e^t − 1)) = t; compare the coefficients of t^r/r!. Also d'_j R = g^{*j} with
g = 1_{m≥2, (m,P(z))=1}, because n is rough iff every factor of n is rough. So S_{j,j'} is the
shift-2 correlation of a j-fold and a j'-fold convolution of rough indicators. Rung j ≥ 2 is a
bilinear (Type II-shaped) sum, and rung 1 is the bare rough indicator.

**F2 (Proved here). The ladder is a change of basis in the type table.** Let N(t, t') count the pairs
(n, n+2) with R = 1 at both points, n + 2 ≤ X, and exponent signatures t, t'. Then
S_{j,j'} = Σ_{t,t'} d'_j(t) d'_{j'}(t') N(t,t'), and
T := Σ R(n)R(n+2)(Λ/log)(n)(Λ/log)(n+2) = Σ_{j,j' ≤ J−1} c_j c_{j'} S_{j,j'}, with c_j = (−1)^{j−1}/j.
The matrix d'_j(t) is triangular in (j, Ω(t)), with diagonal entries j! on squarefree types. So, up to
the non-squarefree rough types (count O(X^{1−1/J}), [audit] see below), {S_{j,j'}} carries the
information of the Ω-table of (n, n+2), which is finer than the λ-patterns of the paper's class. It is
not exact: d'_j depends on the exponent signature (d'_2(pq) = 2, d'_2(p²) = 1), so e.g. at J = 3 the
pattern sum Σ RRλλ is not in the span of the S_{j,j'}. T is the twin-prime count on (z, X], plus prime-power pairs of total
weight O(X^{1/2}), and every twin pair (p, p+2) with p > z is a rough pair. So the J = 3 ladder
T = S_{11} − (S_{12} + S_{21})/2 + S_{22}/4 already contains the whole twin problem. It is the d'-basis
form of Session 41 Finding 4, which used the λ-basis. Remark: n = p² never occurs with n + 2 rough,
because p² + 2 ≡ 0 mod 3.

**F3 (Proved here). How the paper's fair weights act on the rungs.** On two positions the fair pattern
weights are, up to scaling, Ψ = 1 + c·s_1s_2 with |c| ≤ 1. Ψ̂({1}) = Ψ̂({2}) = 0 forces this form, and
Ψ ≥ 0 iff |c| ≤ 1. For c = −1 the weight kills the single edge {1,2} (Prop. `prop:bipartite`(a): an
edge is bipartite). Reweighting gives S^Ψ_{j,j'} = S_{j,j'} + c·L_{j,j'} with
L_{j,j'} := Σ RR λ(n)λ(n+2) d'_j(n)d'_{j'}(n+2). The weight stays inside the class; only the *data*
S_{j,j'} are Ω-dependent, which is the case Remark `rem:marg` says the class does not cover as weights.
(a) Top rung: d'_{J−1}(n)R(n) ≠ 0 forces Ω(n) = J − 1, so L_{J−1,J−1} = S_{J−1,J−1}, and the twin-killing
weight (c = −1) kills S_{J−1,J−1} exactly, just as it kills T.
(b) Linear algebra: a combination of functionals that are each invariant along the orbit
{1 + cλλ} is itself invariant. T is not invariant: T^Ψ = T − L_T, and L_T = T up to the prime-square
terms. So **T is not in the span of parity-blind rungs**, and recovering it needs at least one rung
with L_{j,j'} ≠ o(S_{j,j'}), i.e. a parity-sensitive asymptotic. [audit] The asymptotic form uses the
sieve upper bound S_{j,j'} ≪_J X/log²X: if every L_{j,j'} = o(S_{j,j'}) then L_T = o(X/log²X), hence
T = o(X/log²X). No rough rung is exactly parity-blind (F4), so only this asymptotic form has content.

**F4 (Computed: `code/parity/linnik_ladder.py`, output `code/parity/linnik_ladder.out`; /usr/bin/python3 -I,
46 s, about 1 GB; created here, not committed in this run).**
- Exact checks: the Stirling identity for r ≤ 40, Linnik's identity for all 2 ≤ n ≤ 10^5 (prime powers
  included; d'_j from direct Dirichlet convolution), and d'_j = j!S(Ω, j) on all 60793 squarefree
  n ≤ 10^5, j ≤ 17. Zero failures.
- The reconstruction T = Σ c_jc_{j'}S_{j,j'} is exact (Fractions) at X = 10^7 and 10^8 for J = 3 and 4.
  At X = 10^8 there are 440288 twin pairs on rough pairs at J = 3 (440304 at J = 4; T − twins = 113.5 at J = 3).
- Twist ratios ρ_{j,j'} = L_{j,j'}/S_{j,j'} at X = 10^8:

  | J | ρ_11 | ρ_12, ρ_21 | ρ_22 | ρ_13, ρ_31 | ρ_23, ρ_32 | ρ_33 |
  |---|------|------------|------|------------|------------|------|
  | 3 | +0.078 | −0.254, −0.254 | +1 | – | – | – |
  | 4 | +0.004 | −0.028, −0.029 | +0.303 | +0.044, +0.043 | −0.543, −0.545 | +1 |

  Every rung is parity-sensitive at the computed X. [audit] That this persists at a definite rate is not
  shown: at J = 4, ρ_11 falls from 0.0071 (10^7) to 0.0037 (10^8), and the H2 heuristic gives
  ρ_11 → ((1 − log 3 + P_3)/(1 + log 3 + P_3))² ≈ 4.7·10^{−4} (P_3 ≈ 0.147). The low rungs (the rough-pair count S_11 and the
  rungs next to it) become nearly parity-blind as J grows, while the parity information moves to the
  top rungs.
- Amplification at bounded J: Σ|c_jc_{j'}S_{j,j'}|/T = 4.66 (J = 3) and 12.6 (J = 4) at X = 10^8 (4.49
  and 11.7 at 10^7). A relative error below T/Σ|ccS| (0.21, resp. 0.079) in every rung would suffice.
  At fixed J the amplification is a constant. **Precision is not the obstruction; the parity content of
  the rungs is.**
- Without roughness, depth goes up to log₂ X and the coefficient mass A(r) = Σ_j (j−1)!S(r, j) for
  Ω = r squarefree grows factorially. Computed: A(r)·(log 2)^r/(r−1)! = 1.000000 to six digits for
  r = 8, 10, 15, 20, 30, 40 (the values printed; the script prints twice this ratio under a
  label normalised by (r−1)!/(2(log 2)^r)). Proved here: Σ_r A(r)t^r/r! = Σ_j (e^t − 1)^j/j = −log(2 − e^t), which has a logarithmic
  singularity at t = log 2. Hence A(r) ~ (r−1)!/(log 2)^r by standard singularity transfer (sketch;
  possibly folklore).
- Unrestricted Titchmarsh data at X = 10^7: Σ_p log p·λ(p+2)d_k(p+2) / Σ_p log p·d_k(p+2) =
  +0.0001, +0.0008, +0.0014, +0.0022, +0.0019 for k = 2, 3, 4, 6, 8, against 0.08 to 1 for the rough rungs.

**H1 (Heuristic). Fixed-depth divisor data are parity-blind.** Unrestricted, d'_j = Σ_{i≤j}(−1)^{j−i}C(j,i)d_i
(Proved: (ζ − 1)^j expanded binomially). So unrestricted rungs are combinations of the correlations
d_i d_{i'} and Λ d_i. The twin-killing fair weight changes Σ Λ(n)d_k(n+2) into Σ Λ(n)(1 + λ(n+2))d_k(n+2),
i.e. by the λ-twisted sum. Σ λ(m)d_k(m)m^{−s} = ζ(2s)^k/ζ(s)^k has no pole at s = 1, and the computed
ratios above are of order 10^{−3}. So everything that is known (d_2d_l, Λd_2) and everything EH
would give (Λd_k for each fixed k, item 5) lies, heuristically, in the parity-blind subspace. It cannot determine T at any fixed depth ([audit] because without roughness no fixed-depth truncation of
Linnik's identity represents T; F3(b) concerns the rough rungs). To reach T one needs depth j ≍ log X with errors uniform in
j, against the factorial coefficient mass. Uniformity in the depth is where the parity problem sits on
the unrestricted side. On the rough side, depth is bounded but every rung is parity-sensitive (F4).
Either way, the barrier is the one the bipartite criterion predicts.

**H2 (Heuristic).** Assume factorisation types of n and n + 2 are asymptotically independent on rough
pairs (HL-type). For J = 3, the share of primes among x^{1/3}-rough numbers is 1/(1 + log 2) (Buchstab).
So mean λλ → ((1 − log 2)/(1 + log 2))² ≈ 0.033, against the computed 0.092 (10^7) and 0.078 (10^8),
which are decreasing. So ρ_11 stays bounded away from 0 at J = 3.

## Evaluation against the criteria
Success criterion: **not met.** The sources opened give no asymptotic for any rough rung S_{j,j'},
including S_11, the number of x^{1/J}-rough pairs. Every rough rung is parity-sensitive (F3(a), F4).
The known and EH-accessible correlations (items 4-5) are unrestricted and parity-blind (H1).
No-go criterion: **met within the class** (F2 and F3(b) proved; parity-blindness of the fixed-depth
data heuristic, H1).

## Classification and first unresolved implication
Located (no-go). The Linnik ladder is a triangular change of basis inside the Ω-table of (n, n+2).
At bounded depth (rough pairs) the amplification is a harmless constant, but every rung is
parity-sensitive. At unbounded depth (no roughness) the rungs are the d_k/Λd_k correlations, which are
parity-blind at every fixed k and whose stated k ≥ 3 obstruction is level (MRT p. 7). The parity problem
then reappears as uniformity in the depth. First unresolved implication: an asymptotic for one rough
rung with |ρ| bounded below. The cheapest is S_11 at J = 3, the count of n ≤ X with n(n+2) free of
primes ≤ X^{1/3} (ρ_11 ≈ 0.08 computed, 0.033 heuristic). We found it in none of the sources opened;
we did not search the two-dimensional sieve literature. Twin primes are untouched.

## Possible use
One sentence for a v1.1 next to Remark `rem:marg`: "Linnik's identity on X^{1/J}-rough pairs re-expresses
the twin count through J² Ω-dependent correlations. The fair weight 1 − λ(n)λ(n+2) annihilates the top
one exactly, and the fixed-depth unrestricted ones (d_kd_l, Λd_k) are parity-blind." For the weekly review.
Not audited.

## Sources not opened
None needed beyond the two above. Cited only through MRT or FM, and not opened: Linnik's book (1963),
Friedlander–Iwaniec, Opera de Cribro §17.2, Deshouillers–Iwaniec, Drappeau, Topacogullari, Fouvry,
Bombieri–Friedlander–Iwaniec, and Baier–Browning–Marasingha–Zhao. No access errors occurred.

## Audit (Session 42, fresh-context)
Re-ran `/usr/bin/python3 -I code/parity/linnik_ladder.py` (45.8 s, peak RSS 0.98 GB): output identical
to the .out apart from timings. Independent re-implementation at X = 10^6 (rough indicator from the
smallest prime factor, d'_j as g^{*j} by direct convolution, λ from Ω) agrees with the script in all
S_{j,j'} and ρ_{j,j'} for J = 3, 4. Script read: pair range 2 ≤ n ≤ X−2 correct, roughness strict
(p > z), prime powers handled by exponent signatures, d_k and λ in (iii) correct; no bugs found
(one cosmetic label, G3). Sources re-downloaded to /tmp/claude-0/audit/ (SHA-256 match the card); every
quote and page in items 1-5 checked and found accurate. Prop. `prop:bipartite`(a) and Remark
`rem:marg` cited accurately. Checked and correct: F1 (Ω ≤ J−1 by strict roughness; d'_j = j!S(r,j)
is stated only for squarefree n, as it should be: for rough non-squarefree n, d'_j is the binomial
combination of d_i, with multinomial diagonal j!/∏e_i!, and Linnik still holds, verified to 10^5);
the Stirling proof; the p² + 2 remark; the J = 3 coefficients; F3 fair form and F3(a); the generating
function −log(2 − e^t) and A(r) ~ (r−1)!/(log 2)^r (simple log singularity at log 2, others farther);
the H1 Dirichlet series; H2's 0.033; every table entry.
Errors and gaps (edits marked [audit] in the text):
- E1 (error, F2): "carries exactly the information of the Ω-table" is false when non-squarefree rough
  types occur (d'_2(pq) = 2 ≠ d'_2(p²) = 1); at J = 3 Σλλ is not in the span of the S_{j,j'}. Holds up to
  the non-squarefree types, O(X^{1−1/J}) = o(X/log²X). Sentence corrected.
- G1 (gap, F3(b)): the asymptotic form needed the sieve upper bound S ≪ X/log²X and gives only
  T = o(X/log²X); the exact form is vacuous for the rough ladder (no rung has ρ = 0). Step added.
- G2 (overclaim, F4): "parity-sensitive at a definite rate" not supported for ρ_11 at J = 4 (decreasing;
  heuristic limit ≈ 4.7·10^{−4}). Softened.
- G3 (minor, F4): "r = 8, …, 40" only sampled values; script label off by factor 2 (cosmetic, script not
  edited). Corrected.
- G4 (minor, F4): 440288 twin pairs is the J = 3 count. Clarified.
- G5 (gap, H1): "By F3(b) it cannot determine T at any fixed depth" misattributes the reason. Reworded.
- G6 (minor, Literature item 4-5): omits that BBMZ need H ≤ X^{1−ε} with O(HX^{−δ}) exceptions, and that
  Drappeau's bound needs a Siegel-zero correction term. Not edited.
- G7 (gap, Evaluation): the no-go criterion's first clause is vacuous on the rough side (no rough rung has
  a known asymptotic) and heuristic on the unrestricted side (H1); "met within the class" rests on H1, not
  only on F2/F3(b). The card already labels H1 heuristic; not edited.
Classification "located (no-go inside the paper's class)" stands, with the no-go understood as partly
heuristic (H1). The card claims no progress on twin primes, and it makes none.
