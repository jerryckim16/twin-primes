# Lane 1 (mathematics of Sections 1-3) -- fresh-context referee, 18 Nov 2026

Saved by the coordinator from the helper's final report (in substance). No false mathematical statement found; checked line by
line: prop:tao-weight-logc (kappa = c/4, c_0 = c/16, dyadic decomposition, rho(e) <= 2 tau(e), the (log R)^6 and (log R)^15 sums,
main-term density), Remark cor:maynard-logc (c/32), prop:bipartite (1)-(3), (a)-(c), cor:six, thm:pintz-maynard (q < W R^2 <=
N^{theta-delta}, tau_{3k} count, exponent 2k + (9k^2 - A)/2), cor:pintz12 (1)-(4). Scripts confirm H(3..9) = 6, 8, 12, 16, 20,
26, 30; admissibility of {0,2,8,12}, {0,2,6,8,12}, {0,4,6,10,12,16}; the Remark 8.1 weight (zero for H in {4,6,8,12}, n < 20000;
non-zero for H = 3; odd-position version non-zero for many n); 1/M_k = 0.721535, 0.607519, 0.542295. All nine Lean names exist.
Errors: E1 intro framing stated as fact; E2 rem:chen uses "kills" outside its definition, and "1 + s1 s2 kills 'n+2 a product
of exactly two primes'" is false as written (it kills "n prime and n+2 = p1 p2"); E3 "only case" should be "only case known".
Gaps: G1 Pintz proof: classes not coprime to q (restore the reduction via lambda(gm) = lambda(g) lambda(m)); G2 existence of F
with theta sum J / I > 1; G3 Remark 8.1 weights depend on n mod 6 (restore "class by class"); G4 rem:pintz-parity: fairness at r
sentence dropped, admissibility of H u {r} not needed; G5 Pintz "r != 0".
Labels: intro Heuristic; theta > 0.5126 Heuristic; H_2 bounds Literature; interpretive parts of rem:pintz-parity Heuristic;
rem:marg Proved here, rem:meta Heuristic; Lean theorem concludes total mass 0 (non-negativity step Proved here).
Minor: GEH twist "(though its main term changes)"; b_i in Remark prop:tao-weight; Tao14b read through a text extract; dropped
caveats (TT25 proposition only for w_R and shift 2; uniformity for q <= x^theta Open; k = 1 void).
