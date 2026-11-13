# Audit E — Song–Yue §4.6–4.7, Theorem 4.18, and the link to §4.13–4.14 (self-review, read-only)

(Report delivered by the auditor as its final message; saved here verbatim in substance by the coordinator.)

**Verdict:** Theorem 4.18 is proved as written, conditional on the statements of Props 4.2, 4.4, 4.6, Lemmas 4.8 and 4.10, and Prop 4.11 (§4.5 and the other auditors). No level-(d) gap or error found in scope. The sieve uses exactly what Theorem 4.18 provides. The constants are ineffective (through Siegel–Walfisz in Lemma 4.8), which does not affect H1 ≤ 236.

## Items
- (a) Lemma 4.12 (τ_k in a short interval): maximal-factor count correct.
- (a) Lemma 4.13 envelope bounds: |f| ≤ g, support in [2^-41 X, 2^41 X], g ≪ τ_20 log X.
- (b) Lemma 4.13 Eq. (58): reuses Prop 4.11's grouping with the same u_i; all atoms of g smooth; SW for w_L and w_L log n elementary; hypotheses of 4.2/4.4/4.6/4.10 re-checked. (c) proof is a sketch.
- (a/b) Prop 4.14: (60)–(61) hold incl. r = ⌈2^{v+1}⌉ (checked on PDF); (62) holds at endpoints and Y = X (case analysis + numeric); Fourier convention/inversion right, interchange justified; tail exponent Bcut+2−2r (sympy); low frequencies use Prop 4.11 with T = Bcut+2; (65) right, K2 independent of Bcut; constants chosen in valid order (Bcut > C+K2+Kv, then D, then r), no circularity; sup over Y legitimately outside the q-sum. (c) ‖W^(r)‖_1 ≪ h^{-r} stated without proof (trivially true, even h^{1−r}).
- (a) Sharp cutoff restoration complete: before §4.6 the only sharp cutoff is n ≤ Z inside the μ_Z atoms (covered by Lemma 4.8); the product cutoff (X,Y] enters only in Prop 4.14.
- (a) Prop 4.15: Heath–Brown identity re-derived, numerically checked for K = 2, 3, 4; O((log X)^20) blocks; saving C+21 per block leaves C+1; Q182(X;σ) and Z fixed as Y varies.
- (a) Lemma 4.16: 2^ω root bound (brute force q < 400); cube-and-higher count right; 253/500 + 1/3 = 1259/1500 < 1.
- (a) Prop 4.17: partial-summation identity exact (numeric to 1e−10); bound uniform in t.
- (a) Theorem 4.18 and Eq. (26): lower endpoint costs O(X^{0.506}).
- (a) Sieve link: Lemma 4.28 needs only (26) with σ = σ0/2 (Cauchy–Schwarz and random-assignment steps correct). Lemma 4.30: moduli in Q182(X;σ0/2), squarefree; residues CRT products of local sets of ≤ 47 nonzero classes (fixed at p | W); multiplicities ≤ τ^8, total weight τ^14; (c) assignment of small factors to e vs e' implicit. Prop 4.31: interval shift costs X^{0.506+o(1)}; coprime average matches the main-term denominator; same moduli family, level, coefficient and residues as Theorem 4.18.
- (a) Numbers: 37 exact rational inequalities checked, all hold (incl. §4.13 constants and L+U = 253/500).

## Defects
None at level (d). Exposition gaps (c1)–(c3) above. Lemma 4.28 is redundant (Theorem 4.18 already supplies divisor weights).

## Remaining obligations (outside scope)
Props 4.2, 4.4, 4.6 (the whole beyond-1/2 level); Lemma 4.8 (uniform SW for twisted μ_Z atoms); §4.5 coverage (Lemma 4.9, Prop 4.11); Selberg main term ([D14b] Lemma 4.1); Prop 4.21 (finite certificate — independently reproduced by this project).

Files: exact_checks.py/.out (ALL PASS), sanity_checks.py/.out, img/ (rendered pages 33–38).
