# Route card: does LWW Prop. 5.3 accept a character twist or a thinned auxiliary prime set? (2026-11-24 (Session 51))

**Classification: conditional (for f = mu*chi, in outline); located (for Remark 1's general f).**
- (a) Twist: Prop. 5.3's proof uses the coefficient alpha only in places that a twist by a character psi mod q_0
  leaves intact, after one stated change: Prop. 2.2 is applied to chi_1*psi mod k*q_0 instead of chi_1 mod k. With the
  split of T_3 by (m, n) mod q_0, this gives the T_3 bound for mu*chi for every fixed Dirichlet character chi. It is
  conditional on [LWW] Props. 4.2 and 5.3 being correct as stated. The success criterion (a) is met in outline.
- (b) Thinning: I found no obstruction. Prop. 5.3, Lemma 4.1, Section 3's constants and Prop. 2.3 use the auxiliary
  sets only through things that survive thinning (checked line by line). Prop. 4.2's proof (pp. 18-61) was scanned
  for every use of P_i, V_i and |P_i|, NOT read line by line.
- Remark 1 (general bounded multiplicative f with BV): it reduces to (b) for arbitrary subsets P'_i ⊂ P_i, plus Type I
  for a G_g-type target, provided the pigeonhole approximation is made BEFORE Vaughan's identity. Made after it, as in
  the Session 50 sketch, the approximation error costs a power of L (Finding 4).
- **First unresolved implication:** Prop. 4.2 for subsets P'_i ⊂ P_i with V'_i >> 1 (pp. 26-47 and 53-61 not read
  line by line).
- Not in the parity paper. No parity-breaking content of our own. Twins (K = 0) untouched.

## Question
The Session 50 card (2026-11-24-lww-mu-vs-lambda.md) reduced the cases f = mu*chi (chi a fixed Dirichlet character
mod q_0) and Remark 1's "general bounded multiplicative f" to two unchecked variants of [LWW] Prop. 5.3:
- (a) Prop. 5.3 with the coefficient alpha_m = mu(m) R_Z(m) twisted by a character psi mod q_0 (the split of T_3 by
  (m, n) mod q_0), or more generally with the target sign sigma = -chi(p) depending on p's class mod q_0;
- (b) Prop. 5.3 (and the Section 4.2-5 machinery it feeds) with every auxiliary set P_{j,i} replaced by
  P_{j,i} ∩ {p ≡ a mod q_0} (pigeonhole thinning).
Does the proof of Prop. 5.3 (via Prop. 2.2, characters of modulus <= (log x)^B) go through for (a) and/or (b)?

## Criteria (written 2026-11-24 before reading the proofs)
- Success criterion (a): every step of the proof of Prop. 5.3, and of Prop. 2.2 where it is invoked, goes through
  with alpha_m = mu(m) psi(m) R_Z(m) (psi mod q_0, q_0 fixed), each change stated with page and equation; together
  with Prop. 4.2 (arbitrary coefficients, p. 18) this gives the T_3 bound for f = mu*chi.
- Success criterion (b): every step of Props. 4.2/5.3 that uses the auxiliary prime sets goes through for
  P'_{j,i} ⊂ P_{j,i} ∩ {p ≡ a mod q_0} with V'_i = sum_{P'_{j,i}} 1/p bounded below, with stated changes
  (e.g. V_i = log 2 replaced by V'_i), giving the T_3 bound with P2 at sigma fixed.
- No-go criterion: a step that uses the full set R (or full P_i) in a way the thinning/twist breaks, with page: e.g.
  a sum over all p in P_i of a quantity that needs the density or the exact value V_i = log 2 + o(1), an
  orthogonality/completeness over characters or over residue classes that the restriction destroys, or a place
  where alpha = mu R_Z is used through an identity (e.g. Möbius inversion, mu * 1 = delta, a Vaughan/Heath-Brown
  re-decomposition, zero-free region for L(s, chi) of mu specifically) that a psi-twist changes in a non-routine way.
- Cheapest decisive check: read the proof of Prop. 5.3 for every place alpha_m enters and every place P_i enters.

Outcome: success criterion (a) met (in outline, conditional on LWW). Success criterion (b) is met for Prop. 5.3 and
the other parts read; for Prop. 4.2 only by a targeted scan. No-go criterion not triggered.

## Sources read (this session)
- arXiv:2610.20242v2, fetched 24 Nov 2026 ~09:36 UTC from https://arxiv.org/pdf/2610.20242v2 into a new empty scratch
  directory (not committed). 895,874 bytes. SHA-256
  `7ac341311b4a648c32c2b23b3029e1f4a3202258b55614a33ba7e8282423d000`, which matches notes/sources-lww26.md and the
  Session 50 card. Converted with pdftotext -layout.
- Abs page https://arxiv.org/abs/2610.20242, opened 24 Nov 2026 09:36 UTC: submission history v1 (14 Oct 2026, 53 KB)
  and v2 (19 Nov 2026, 78 KB). **No v3.**
- Read line by line:
  - p. 5-6: Prop. 2.2 and proof, (2.5)-(2.11).
  - p. 7: (2.12)-(2.15).
  - p. 8-9: the V_i uses in the proof of Prop. 2.3.
  - p. 12: (3.6) and the c'_d, e_d bounds.
  - p. 15-18: Section 4.1, (4.1)-(4.14), Lemma 4.1, Prop. 4.2 statement.
  - p. 19-22: (4.19)-(4.34), the good-state conditions (4.26)-(4.27) and the measure bound (4.31).
  - p. 24-26: (4.42)-(4.50).
  - p. 47-53: Section 4.6, (4.118)-(4.135).
  - p. 61-69: Section 5.1-5.2, (5.1)-(5.30), Lemmas 5.1-5.2, Prop. 5.3 and proof.
  - p. 69-70: Section 5.3, (5.31)-(5.33).
- Scanned (text search over pp. 18-61 for every occurrence of P_i, V_i, |P_i|, "log 2", density / PNT / Siegel /
  Mertens / residue class): pp. 18-61. NOT read line by line: pp. 26-47, 53-61 (Sections 4.3-4.5, 4.7).
- Not opened: [12] (source of (2.6), "Lemma 3.9(ii)"), [11, Lemma 8], [13], [6] cited inside Lemmas 5.1-5.2.

## Notation
As in the Session 50 card. Also:
- L = log x; R_Z(n) = 1 if n has no prime factor <= Z = exp(L^{0.24}).
- alpha_m = mu(m) R_Z(m) m^{iv}, beta_n = c_V(n) R_Z(n) n^{iv} ((4.3), p. 15).
- A = {p_1...p_K : p_i in P_i}, V_i = sum_{p in P_i} 1/p.
- M_alpha(t) = M^{-1} sum_{m in I_M} alpha_m chi_1(m) m^{it} ((5.2), p. 61).
- k <= 2L^{A_0} is the major-arc denominator ((5.8), p. 64).

## Findings

### 1. Where alpha enters the proof of Prop. 5.3 (Literature reading, pp. 61-69)
The hypothesis alpha_m = mu(m) R_Z(m) (p. 63) is used in exactly four places:
- (i) **p. 64, before (5.8).** P^-(mnrs) > Z gives (abmnrs, k) = 1. Only the support of alpha (Z-sifted m) is used.
- (ii) **Lemma 5.1, (5.3), p. 61.** Montgomery–Vaughan plus the divisor bound; only |alpha_m| <= 1 is used.
- (iii) **p. 69, before (5.30).** "by Proposition 2.2, sup_{|t| <= 2XL^{B_1}} |M_alpha(t)| << L^{-A_2}". This is the
  only arithmetic use of mu. It is applied with chi_1 mod k, k <= 2L^{A_0}. The factor m^{iv}, |v| <= x^{C_0}, is
  handled on p. 69 by |t + v| << x^2 + x^{C_0}.
- (iv) **p. 66.** The r-slot: "the same argument applies to Q-tilde since alpha-tilde_r = alpha_r = mu(r) R_Z(r)". So the
  r-slot needs (i)-(iii) again, with chi_5 mod k.

The coefficient beta is arbitrary with |beta_n| <= L^C R_Z(n). The bound for the beta-side in Lemma 5.2 ((5.4)) uses
only |beta_n| <= L^C. Lemma 5.2 is uniform in any set P ⊂ [P, 2P) of primes and in any coefficients |v_p| <= 1 (p. 61-62).
No step uses Möbius inversion, an identity of mu, or a zero-free region beyond what Prop. 2.2 packages. So the
no-go criterion for (a) is not triggered.

### 2. (a) The twist: harmless after one stated change (Proved here, in outline; conditional on [LWW])
- Take alpha'_m = mu(m) R_Z(m) psi(m) m^{iv}, or alpha'_m = mu(m) R_Z(m) 1_{m ≡ u (q_0)} m^{iv}, with q_0 fixed.
  - (i) and (ii) hold unchanged: Z-sifted support, |alpha'| <= 1.
  - (iii): for large x every prime factor of q_0 is <= Z, so (m, q_0) = 1 on the support. Hence
    1_{m≡u} = phi(q_0)^{-1} sum_{psi mod q_0} psi-bar(u) psi(m), and M_{alpha'}(t) is an average of
    phi(q_0) sums of mu(m) R_Z(m) (chi_1 psi)(m) m^{i(t+v)}.
  - chi_1 psi is a character mod k q_0 <= 2 q_0 L^{A_0} <= L^{A_0 + 1}. Prop. 2.2 (p. 5) is stated for every character
    mod q <= (log x)^B with B fixed, so it applies with B = A_0 + 1. The same holds in the r-slot (iv).
  - **Stated change:** in (iii), apply Prop. 2.2 with B = A_0 + 1 to chi_1 psi instead of chi_1. Prop. 2.2's own proof
    (pp. 5-6) does not depend on q beyond q <= (log x)^B. It is inherited from (2.6) = [12, Lemma 3.9(ii)], which is
    stated "for any character chi (mod q) with q <= (log X)^{A_0}" (not opened).
- Prop. 4.2 (p. 18) needs only |alpha_m| <= L^C R_Z(m) 1_{(M,2M]} and the same for beta, so it covers alpha', beta'.
- **Assembling mu*chi, Type II.**
  - chi(mn + 2) depends only on (m mod q_0, n mod q_0). So
    T(M, N; mu chi W) = sum_{u, w mod q_0} chi(uw + 2) T_{u,w}(M, N), where T_{u,w} is LWW's (4.3) with
    alpha 1_{m≡u}, beta 1_{n≡w} and the target mu W.
  - For each (u, w), pp. 15-16 apply verbatim, since P2 holds with sigma = -1 for mu. This gives (4.5)-(4.8) with
    Q_Y^{u,w}. Lemma 4.1 holds (it uses only |alpha|, |beta| <= L^C). Prop. 4.2 holds as stated. Prop. 5.3 holds with
    the change above.
  - So T_3(mu chi W) << q_0^2 x L^{-A}.
- **Type I** for mu chi W: P3 (BV for mu in classes mod 2qr q_0) and (3.7) with mu(d) chi(d), as in Session 50
  (Finding 2, mu*chi bullet; not re-read this session).
- **Removing W** (p. 70, Prop. 2.3) is target-free apart from |f| <= 1.
- **Conclusion (conditional, in outline):** sum_{p <= x} mu(p + 2) chi(p + 2) = o(pi(x)) follows from the LWW argument
  with the stated changes, for every fixed Dirichlet character chi. This is a remark on LWW's method, not a new
  theorem; its status is that of [LWW] (Claimed).

### 3. (b) Thinning: every use of P_i found survives (Literature reading + Proved here, elementary)
Let P'_i ⊂ P_i be any subsets, V'_i = sum_{p in P'_i} 1/p, and suppose c_0 <= V'_i (< V_i < 1) with c_0 > 0 fixed.
For P'_i = P_i ∩ {p ≡ a mod q_0}, (a, q_0) = 1, Mertens in progressions gives V'_i = (log 2)/phi(q_0) + o(1)
(standard, from PNT in progressions for fixed q_0; not re-read).

Uses of the auxiliary sets, and what each needs:

| place | use | survives thinning? |
|---|---|---|
| (5.1) p. 61; (4.45) p. 25; w(a,b) <= 1 p. 26; F_I weights p. 21; sum sigma p. 24 | identities prod V_i^{-1} sum_{a in A} 1/a = 1, i.e. normalisation by the set's own V_i | yes (definition of V'_i) |
| p. 64 | P^-(ab) > exp(L^{1/10}) > k | yes (subset) |
| p. 66 | \|B_lambda(t)\| << 1 via (5.1) | yes |
| (5.27) p. 68 | \|sum_{P_i} chi_4(p) p^{i(t+xi)}/p\| <= V_i | yes (trivial) |
| p. 68 | V_1^{-1} << 1 | yes, constant c_0^{-1} |
| Lemma 5.2 p. 61 | P ⊂ [P, 2P) any set of primes, c L^{1/10} <= log P <= C_1 L^{1/5} | yes (stated uniform in P) |
| p. 17 (Lemma 4.1) | prod V_i^{-2} <<_K 1; sum over p in ∪P_i of 1/p^2 | yes, constant c_0^{-2K} |
| (4.29) p. 21; p. 45 | upper bounds \|P_i\| <= exp(2L^{a_i}) | yes (upper bounds) |
| p. 26 | 1 - w(a,b) << J^2 exp(-cL^{0.1}) via 1/(p V_i) | yes, constant c_0^{-1} |
| (4.121) p. 47 | p V_i nu_i(p) = 1 + O(R/p), s_i = 1 + O(R/p_min), Delta << e^{-L^{0.1}} | yes (normalised; p_min >= exp(L^{0.1})) |
| p. 49 | V_i < 1, choice of v_0; R(G_j), C(G_j) << 1 | yes (only V'_i < 1 used) |
| p. 50 | m(a) <<_K Y^{-1} | yes, constant c_0^{-K} |
| p. 52 (4.132) | eps_K = C (L^2)(J+1)^{-K} + ...: (J+1)^{-K} from J+1 distinct primes in each tuple, \|P'_i\| >= J+1 | yes |
| (4.135) p. 53 | "choices do not depend on the exponents a_i; those affect only the threshold for x and the implied constants" | constants now also depend on c_0 |
| Section 3, p. 12 | sum \|c'_d\|/d << 1, V_i < 1, V_i = log 2 + o(1) used only as V_i ≍ 1 | yes |
| Prop. 2.3, pp. 7-9; p. 70 | V_i ≍ 1, V_i < 1, m_j >> 1, C_{K,rho} independent of b; bK pairwise disjoint families | yes, constants depend on c_0; thinned subsets of disjoint sets stay disjoint |

- The text search found no use of the density of P_i, of PNT for the auxiliary primes, or of the interval structure of
  P_i beyond log p ≍ L^{a_i} and the upper bound on |P_i|.
- The prime-pair / P^1(F_p) machinery (pp. 18, 34-35, 43-46, 53-55) runs over p in ∪P_i as an index set, with
  products and sums normalised by nu_i or bounded via sum 1/(p+1) <= sum V_i (p. 44).
- In the thinned version, P2 for mu*chi holds exactly with the fixed sign sigma = -chi(a): (mu chi)(p v) =
  -chi(a)(mu chi)(v) for p ≡ a, p ∤ v. So route (b) treats mu*chi directly, with no split.
- **Status:** (b) holds for Prop. 5.3 and everything read line by line. For Prop. 4.2 it rests on the scan.

### 4. Remark 1 (general bounded multiplicative f): where the pigeonhole step must be placed (Proved here, elementary, outline; partly Heuristic)
- **The trap (Proved here, elementary).** Suppose one pigeonholes into sets where |f(p) - c_i| <= eps, and approximates
  f(a) by c_A = prod c_i at p. 15, i.e. inside T_3. The error is then K eps times the trivial bound for T_3, which is
  sum |alpha_m beta_n| W ~ x L^{0.52} heuristically: |beta_n| << L (p. 15), and Z-sifting gives density about
  1/log Z per variable. That is not o(x) unless eps << L^{-0.52}/K, which forces V'_i → 0. So the Session 50
  phrase "plus the K·epsilon approximation errors" understates the problem if the approximation is made inside the
  Vaughan decomposition.
- **The repair (Proved here, elementary, outline).** Approximate before Vaughan's identity. Write
  W'(N) = prod V'_i^{-1} sum_{a in A', a | N} rho^{omega'(N) - K}. For (a, N/a) = 1, f(N) = f(a) f(N/a), so
  f W' = c_A G + E + E', where:
  - G(N) = prod V'_i^{-1} sum_{a | N, (a, N/a) = 1} f(N/a) rho^{omega'(N/a)};
  - |E(N)| <= K eps W'(N);
  - E' collects the terms with (a, N/a) > 1.
  Then sum Lambda(n) E(n+2) << K eps x by Prop. 2.3 / (2.24) (the mean of W'/m' over primes). E' is negligible, as on
  pp. 15-16. G is exactly LWW's post-p.-15 target with mu(h) replaced by f(h), so its Type II sum goes through (4.6)
  using only |f(h) rho^{omega(h)}| <= 1, and then Q_Y is LWW's own, built on the P'_i.
- What remains:
  - (b) for arbitrary subsets P'_i with V'_i >= c_0(eps) > 0 (Finding 3; Prop. 4.2 scanned only).
  - Type I for the target G = G_g with g = f rho^{omega'}. The Session 40 card (2026-11-21-lww-main-term.md, Finding 1)
    shows that Type I sees only residue classes. So it needs P3 for f, i.e. BV with zero main term in classes mod q a,
    a <= x^{o(1)}. Outline, not re-checked.
  - The order of limits: K fixed (from Prop. 4.2), then eps, then b → ∞ for fixed eps, then eps → 0. This needs
    C_{K,rho} in (2.16) to depend on c_0(eps) but not on b, which is what pp. 7-10 give (outline).
- Remark 1's "f satisfying the Bombieri–Vinogradov type" must mean BV with zero main term (P3): f = 1 is bounded,
  multiplicative and equidistributed with a main term, and the conclusion fails for it. This is a reading of a hedged
  remark ("very likely applicable", "We do not pursue", p. 3), not an error in LWW.

### 5. Possible errors in LWW
- None found. All page references above check against v2. Lemma 5.2's uniformity "in xi, P, the characters and the
  coefficients" (p. 62) is what makes (b) cheap on the Prop. 5.3 side. Its proof uses [11, Lemma 8] (not opened),
  which depends on the set only through P and the coefficient bound.
- Presumed own error first. The most likely place I could be wrong is Prop. 4.2, pp. 26-47 and 53-61. A step there
  could use a lower bound on the count of primes in a short subinterval of P_i (for example, to place enough primes
  dividing a lattice coordinate). The scan found no such step, but the scan is not a reading.

## First unresolved implication
Prop. 4.2 (Q_Y - Q_Y^maj << XYL^{-A}) for auxiliary sets P'_i ⊂ P_i with V'_i >= c_0 > 0, constants depending on c_0.
- For mu*chi this is not needed: route (a) uses Prop. 4.2 as stated.
- It is needed for Remark 1 via Finding 4, together with Type I for G_g (Session 40 outline).

## What this does NOT show
- Nothing about the correctness of LWW. Every conclusion here is conditional on Props. 4.2 and 5.3 (and on Section 3
  and Prop. 2.3) being correct; they are Claimed, not verified.
- No result for lambda chi, or for f with f(p) not nearly constant on sets of positive 1/p-mass in each P_i.
  Pigeonhole always provides such sets, but only with the repair of Finding 4.
- Nothing about twins (K = 0): Lambda(n + 2) has no P2 at all (sources-lww26.md, "Distance to twin primes").
- No parity-breaking content of our own. mu*chi is a parity-type target exactly like mu (P2 with sigma = -chi(a)), so
  this extends a claimed parity-breaking argument formally. It does not move the parity-sensitive implication
  "P2 ⟹ T_3 small" (Session 50) anywhere new.

## Not checked
- Prop. 4.2's proof, pp. 26-47 and 53-61, line by line (only scanned for uses of P_i and V_i).
- [12] Lemma 3.9(ii), [11] Lemma 8, [13] Corollary 3, [6] Thms. 8.4 and 8.13 (cited inside Prop. 2.2 and Lemmas 5.1-5.2).
- Section 3 for mu*chi and for thinned sets beyond p. 12's constants (relies on the Session 50 reading).
- Mertens in progressions for the thinned mass (standard, not re-read).
- Type I for G_g with general f (Session 40 outline only).
- No numerical toy check was run: nothing in the question is visible at toy scale (Prop. 2.2-type savings need
  characters mod L^{A_0} and lengths x^delta).
- No fresh-context audit.

## Scripts
None. No Lean.
