# Route card: does the k = 2 variance argument extend to k = 3? (dual formula, orthogonal relaxation)

Date: 15 Nov 2026, Session 22 (back-to-back bonus run 1 of 3). Programme: parity-barrier, part 2 (attempts).
Follows: 2026-11-15-geh-ceilings-k2.md (Thm thm:k2: at k = 2 the PM8b Theorem 3.14 ratio is <= 2, with equality),
and open question 6 of the parity paper (exact k = 3 supremum).

## Question
Polymath8b's Theorem 3.14 criterion (GEH, vanishing marginal condition) gives DHL[3,2], hence H1 <= 6, because at
k = 3 its ratio exceeds 2 (PM8b Thm 3.15). At k = 2 the ratio is at most 2 (our Thm thm:k2), proved by a variance
argument. Does that argument extend to k = 3 and give a sharp ceiling there, and what decides whether the k = 3 ratio
is above or below the parity value 2?

## Success / no-go criteria (fixed before computing)
- Success: a proved ceiling for the k = 3 ratio strictly below c(3) = 2.472 (Prop. prop:ceil) at some eps, by a
  generalisation of the k = 2 argument.
- No-go: an exact certificate that the structure the k = 2 proof uses (orthogonal constraint spaces, fibre means)
  cannot give any ceiling below 2 at k = 3, for some eps where the true supremum is (heuristically) below 2.

## What was done
1. Dual formula (Lemma lem:dual, proved here, standard Hilbert-space duality): S_k(eps) = sup_f dist(P^* f, W)^2/|f|^2,
   W the closed span of the constraint spaces V_j = {psi(t_{-j}) 1_{Z_j}}. Every explicit v(f) in W gives a ceiling; the
   projection gives the exact value. The proof of Thm thm:k2 is exactly this with the exact projection: at k = 2 the
   cylinders Z_1, Z_2 are disjoint, so Pi_W = E_1 + E_2 (fibre means), and Phi in that proof equals Pi_K P^* f.
2. Overlap (Prop. prop:overlap, proved here): for k >= 3 and 0 < eps < 1/(k-1), any two cylinders Z_i, Z_j overlap in
   positive measure (points with one large coordinate t_m in (1+eps, k/(k-1)), m not i, j), so V_i and V_j are not
   orthogonal and Pi_W is not a sum of fibre means. This is exactly the step of the k = 2 proof that does not transfer.
3. Orthogonal relaxation: keep only the "clean" columns (fibres meeting no other cylinder; at k = 3 these are
   min(t_l, t_m) >= 1/2 - eps). The relaxed class is larger, its V'_j are orthogonal, and its supremum S'_3(eps) is an
   upper bound for S_3(eps) that the k = 2 method could in principle evaluate. Exact certificates
   (code/parity/k3_orth_relax_cert.py, integer null space with python-flint, exact rational ratio):
   S'_3(1/8) >= 13523319026150757/6316738844612720 > 2.1408 (n = 32), S'_3(1/4) > 2.0657 (n = 32).
4. Heuristic (code/parity/k3_thm314_dual.py, floating point, cubes fully inside D, extrapolated in 1/n): the full class
   S_3(eps): see the table in the paper (Remark rem:k3-eps) and code/parity/k3_thm314_dual.out.

## Classification
No-go for the direct extension (Computed + Heuristic): at eps = 1/8 the relaxed supremum is certified > 2.14 while the
true supremum is heuristically about 1.98 < 2. So whether the k = 3 criterion exceeds the parity value is decided by the
overlap constraints (points where two marginal conditions act at once), which the k = 2 argument never meets.
The success criterion was NOT met (no ceiling below c(3) proved).
First unresolved implication: a rigorous upper bound for |Pi_K P^*| at k = 3 that uses the overlapping constraints,
e.g. by alternating projections (von Neumann) with an explicit rate, or a finite-element dual with error control.
No parity-breaking content: this is about the variational shadow of the obstruction, not about primes.

## Sources
Polymath8b, arXiv:1407.4897v4, Thms 3.14, 3.15 (pp. 15-16), Sec. 7.4 (pp. 62-68) (opened in Session 21, same hash as
in notes/parity-programme.md). Nothing new opened this session.
