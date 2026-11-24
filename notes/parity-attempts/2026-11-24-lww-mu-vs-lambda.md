# Route card: what the Lü–Wang–Wu argument needs from mu, versus lambda, mu*chi and fake targets (2026-11-24 (Session 50))

**Classification: located.** On the target side I found no gap, in outline. The first unresolved implication is
"P2 ⟹ T_3 small", meaning the step at p. 15 plus (4.6) combined with [LWW] Props. 4.2 and 5.3. That is the same
place the Session 39-40 cards found, but it is now pinned down, heuristically, by an explicit fake target that
satisfies every other property (it satisfies P3 only heuristically). Not in the parity paper (v1.1). No parity-breaking content of our own. Twins (K = 0) untouched.

## Question
Lü–Wang–Wu, arXiv:2610.20242v2 (CLAIMED, not verified), Remark 1 (p. 3): their approach is "very likely applicable to
general bounded multiplicative function f, with f satisfying the Bombieri–Vinogradov type, such as the Liouville
function". The question has three parts:
- Which properties of mu as the TARGET (mu at n + 2) do Sections 2-3 use, together with the target uses in 4.1 and 5.3?
- Does the argument as written apply to lambda, to mu*chi (chi a real character), and to fake targets?
- Where exactly must parity be broken?

- Success criterion: a list P1..Pn of target properties with equation and page numbers, and a verdict for lambda,
  mu*chi and a model g. The model g must violate one Pj and have sum_p g(p+2) not o(pi(x)), which locates where the
  argument has to work. Alternatively, a proof that no such model exists inside the class.
- No-go criterion: some g that satisfies all the Pj and has sum_{p<=x} g(p+2) >> pi(x), known or easy to show. That
  would mean a probable gap needing expert review. Before claiming it, presume a misreading and re-read.
- Cheapest decisive check: read Section 3 and pp. 15-16 for every use of the target. Then test the candidate models
  numerically against P1-P3 at toy scale.

## Sources read (this session)
arXiv:2610.20242v2, fetched 24 Nov 2026 from https://arxiv.org/pdf/2610.20242v2 into a fresh scratch directory
(not committed). 895,874 bytes, 75 pp. SHA-256 `7ac341311b4a648c32c2b23b3029e1f4a3202258b55614a33ba7e8282423d000`,
which matches the full hash recorded in notes/sources-lww26.md (Session 48). Read with pdftotext -layout:
- pp. 1-4: Section 1, Theorems 1-2, Remarks 1-4.
- pp. 4-10: Section 2: Prop. 2.1 (2.2)-(2.4); Prop. 2.2 (2.5)-(2.11); Section 2.3 (2.12)-(2.15); Prop. 2.3 (2.16)-(2.25).
- pp. 10-14: Section 3 in full, (3.1)-(3.10).
- pp. 15-18: (4.1)-(4.14), Lemma 4.1, Prop. 4.2.
- p. 63: statement of Prop. 5.3.
- pp. 69-70: Section 5.3, (5.31)-(5.33), and the removal of W.
- A full-text search for every occurrence of the target (mu(h), mu(mn+2), mu(p+2), F(n)) in the whole file.
  Sections 4.2-5.2 contain none; this agrees with the Session 39-40 audits.
Earlier cards that this one builds on: 2026-11-20-lww-orbit-test.md and 2026-11-21-lww-main-term.md.

## Notation
- L = log x and Z = exp(L^{0.24}) (Prop. 2.1).
- R = R(x) is the set of primes in (exp(L^{1/10}), exp(2 L^{1/5})]. Every auxiliary set P_{j,i} of (2.12) and of
  Section 5.3 is a disjoint subset of R, with sum_{p in P_{j,i}} 1/p = log 2 + o(1). By Mertens,
  sum_{p in R} 1/p = 0.1 log L + log 2 + o(1), which tends to infinity.
- A target is the function g in sum_{x<n<=2x} Lambda(n) g(n+2) W(n+2).
- The coefficient mu(d) R_Z(d) of Vaughan's identity belongs to the PRIME variable, not to the target. Prop. 2.2
  (pp. 5-6) and Prop. 5.3 (p. 63) are about that coefficient only.

## Findings

### 1. The target properties used (Literature reading, page by page)
The target enters in exactly the following places.

- **P1 (boundedness)**, |g| <= 1, or |g| <= L^C with the losses of the Session 40 card. Used at:
  - (2.2), p. 4;
  - the truncation of R_Z(k) in (3.3)-(3.4) and of W in (3.5)-(3.6), pp. 11-12, where only sums of |target| over
    progressions are bounded;
  - (3.9) and the da > x^{1/20} range, p. 14;
  - the smoothing error O(x L^{2-B}) on p. 15;
  - the removal of the terms with (a, h) > 1, pp. 15-16;
  - the Cauchy–Schwarz step (4.6), p. 16, which uses only |mu(h) rho^{omega(h)}| <= 1;
  - the prime-power remark after (5.31), p. 69;
  - the removal of W on p. 70, by Cauchy–Schwarz with Prop. 2.3.
- **P2 (sign-multiplicativity at the auxiliary primes).** For p in R and p ∤ v, g(p v) = sigma g(v), with sigma
  fixed (sigma = -1 for mu). In the form used for mu, g also vanishes when p^2 | n for some p in R. It is used twice:
  - p. 15: mu(ah) = (-1)^K mu(h) for a in A with (a, h) = 1. This turns the target into a function of h = (mn+2)/a,
    and (4.6) then discards it. The sign must be the SAME for every a in A. Q_Y in (4.7) carries no coefficient on
    a or b except eta(a/Y) eta(b/Y) and prod V_i^{-2}, and Prop. 4.2 (p. 18) is stated only for that Q_Y.
  - p. 13, (3.7): mu(dv) = mu(d) mu(v) 1_{(v,d)=1} = mu(d) sum_{a | v, p|a ⇒ p|d} mu(v/a), for d composed of
    primes of R. This turns the condition d | qk + 2 into a reduced class modulo 2qr. (3.9) uses that the primes of
    d exceed exp(L^{0.1}).
  - Proved here (elementary): the identity g(v) 1_{(v,d)=1} = sum_{a | v, a | d^∞} g(v/a) follows from P2 in the
    mu form, by checking v = p^j v' for j = 1, 2, 3, ... For lambda, (3.7) is not needed at all, because
    lambda(dv) = lambda(d) lambda(v) holds without any coprimality condition.
  - Multiplicativity at primes outside R is NEVER used.
- **P3 (Bombieri–Vinogradov with ZERO main term).** This is (3.1), p. 10, cited from [16, Prop. 3]: reduced classes,
  max over z <= Y_0. It is applied on p. 13 only to moduli 2qr <= x^{2/5+o(1)} <= Y_0^{1/2} L^{-B}, with
  Y_0 = (2x+2)/(da) >= 2 x^{19/20}. So the level actually used is 2/5 + o(1), as in the Session 40 card. T_1
  follows by partial summation (p. 14).
- **Not used for the target:** Prop. 2.2, Prop. 2.3 (which is about W and primes only), Props. 4.2 and 5.3, and all of
  Sections 4.2-5.2. Section 6 (Theorem 2, mu^2) was not examined.

### 2. Verdicts
- **lambda (Proved here in outline; conditional on Props. 4.2 and 5.3 like everything else).**
  - P1 holds.
  - P2 holds in a stronger form: lambda(ah) = (-1)^K lambda(h) for every h. The (a, h) > 1 removal and the
    identity in (3.7) become unnecessary.
  - P3 follows from (3.1), so the theorem cited is for mu but transfers. Write lambda(n) = sum_{d^2 | n} mu(n/d^2).
    The class condition forces (d, m) = 1. For d <= L^{A+1}, use (3.1) at length y/d^2 with B replaced by
    B + A + 1. For d > L^{A+1}, the trivial bound gives sum_m (y/(d^2 m) + 1) summed over d, which is
    << y L^{-A} + Q y^{1/2} << y L^{-A}.
  - So the argument applies to lambda after two routine changes, not verbatim. This supports Remark 1 for lambda.
    By the Session 26 card, sum_p lambda(p+2) = o(pi(x)) would settle the single-prescribed-d case blocked in the
    Liouville-pattern class. That case is claimed, not proved.
- **mu*chi, chi real, nonprincipal, fixed modulus.**
  - P1 and P3 hold: reduce to classes mod lcm(m, q_0).
  - (3.7) works with mu(d) chi(d).
  - P2 FAILS as the argument uses it: (mu chi)(a) = (-1)^K chi(a) varies over A. Then Q_Y would carry
    chi(a) chi(b), and Prop. 4.2 is not stated for weighted a, b. So the argument does not apply verbatim.
  - **Main heuristic repair (audit finding 6; checked against the PDF this session).** chi is periodic mod q_0,
    so chi(mn+2) depends only on (m mod q_0, n mod q_0). Split T_3 into at most q_0^2 sums. Each has coefficients
    alpha_m 1_{m≡u}, beta_n 1_{n≡w}, the constant factor chi(uw+2), and the target mu W, for which P2 holds with
    sigma = -1.
    - Prop. 4.2 (p. 18) allows arbitrary coefficients |alpha_m| <= L^C R_Z(m), |beta_n| <= L^C R_Z(n), so it covers
      these.
    - Prop. 5.3 (p. 63) assumes alpha_m = mu(m) R_Z(m) exactly. Since m is Z-sifted, (m, q_0) = 1 for large x, and
      1_{m≡u} = phi(q_0)^{-1} sum_psi psi-bar(u) psi(m). So one needs Prop. 5.3 with alpha twisted by a character
      psi mod q_0. Its proof rests on Prop. 2.2 (pp. 5-6), which is stated for characters of modulus
      q <= (log x)^B, so this is plausibly routine.
    - Status: **needs Prop. 5.3 with a twist by characters mod q_0; not checked.**
    - The Type I part is unchanged: P3 holds for mu chi, and (3.7) works with mu(d) chi(d).
  - Second heuristic repair: take every P_{j,i} inside {p in R : chi(p) = +1}. By PNT in progressions (standard,
    not re-read), that set still has 1/p-mass (0.05 + o(1)) log L, which tends to infinity, so the b → ∞ step of
    p. 70 survives with V_i = (log 2)/2 + o(1). Not checked: whether Sections 4.2-5 work for prime sets thinned by a
    congruence. They use the prime lists of (4.17) and counts of primes in P_i.
  - For a general bounded multiplicative f with BV (the wording of Remark 1), P2 is not a consequence of BV.
    - Pigeonhole the values f(p), p in R, into k arcs. This gives a subset of R of 1/p-mass at least about
      (0.1 log L)/k on which f(p) is nearly constant.
    - So the argument does not cover Remark 1 verbatim, but pigeonhole thinning reduces the question to two things:
      whether Sections 4.2-5 accept thinned prime sets, and the K·epsilon approximation errors in f(a) ≈ sigma^K.
    - Remark 1 is itself hedged ("very likely applicable", "We do not pursue"), so none of this implies an error by
      LWW.
- **Fake targets: which property catches which model** (Proved here elementary or Heuristic, as marked; the toy
  numbers are in Section 3 below).
  - (a) g = 1 and g = mu^2 (P2 holds with sigma = +1) satisfy P1 and P2 and fail P3 (nonzero mean). Their
    correlations are pi(x) and A_2 pi(x) ([LWW] Section 6 claims A_2; not examined).
  - (b) g = (-1)^{omega_R(n)} satisfies P1 and P2 (sigma = -1) and fails P3. Its mean is about
    prod_R (1 - 2/l), roughly L^{-0.2}, which is far above the precision L^{-A}. Its correlation is
    prod_R (1 - 2/(l-1)), of order L^{-0.2}, so o(1). It is consistent with the claim and is no counterexample.
  - (c) **The parity model g3' (P1 and P3 hold, P2 fails, full correlation).**
    - Definition: g3'(N) = (Lambda(N-2) - Lambda^flat(N-2))/L, with the fake primes
      Lambda^flat(n) = 1_{n = p_1 p_2, x^{2/5+eps} < p_1 <= p_2} · (log n)/c(n).
      - c(n) is the smooth local density factor: the density of such semiprimes near n, relative to the primes,
        is about log(log n/((2/5+eps) log x) - 1), which equals log(3/2) for n ≍ x and eps → 0. So
        Lambda^flat(n) ≈ 1_{n = p_1 p_2, p_1 > x^{2/5+eps}} (log n)/log(3/2), up to a smooth correction.
      - The script instead uses p_1 > X_0^{0.4}, with a constant on each block of length 10^5 equal to
        (sum of Lambda over the block)/(number of such semiprimes in the block). The toy maximum weight/L on the
        window, 2.45, agrees with 1/log(3/2) ≈ 2.47.
      - These fake primes are invisible to Type I information at level 2/5.
    - Type I sums for g3' W (corrected after audit finding 1):
      - The terms q > 1 in T_1 and T_2 have N - 2 = qk with 1 < q <= x^{2/5+o(1)}. There Lambda and Lambda^flat
        both vanish, up to prime powers qk = p^j, which contribute O(x^{1/2+o(1)}).
      - The d = 1 term of T_1 (mu(1) R_Z(1) = 1, i.e. q = 1) equals sum_k R_Z(k) (log k) g3'(k+2) W(k+2). It is NOT
        identically zero. It is o(x) only if Lambda^flat matches Lambda in the reduced classes -2 mod d, d | P (the
        classes that the W-expansion sees). That is P3, which holds here only heuristically.
    - P3 in reduced classes, equidistribution of both weights: this rests on BV for primes and for products of two
      primes in ranges (standard, not re-read this session), so it is Heuristic at the level used.
    - Nevertheless sum_{x<n<=2x} Lambda(n) g3'(n+2) = sum Lambda(n)^2/L ≈ x. With W inserted the Type I sums are
      o(x), heuristically as just explained, so T_3(g3' W) ≈ x m_W. The Type II sum DOES see this target.
    - The reason (Proved here, elementary): on n = p_1 p_2 with p_1, p_2 > x^{1/5}, the Type II piece of Vaughan's
      identity equals -log n. The parity information sits in Lambda's Type II piece at the fake semiprimes.
    - g3' satisfies every target property except P2 (P3 heuristically). For g3' the Type I sums are handled
      directly, so the only place P2 is needed is p. 15. So for mu the parity-sensitive implication is exactly:
      **"P2 at all primes of R ⟹ T_3 = o(x)", that is, p. 15 + (4.6) + Props. 4.2 and 5.3.** Nothing else on the
      target side appears to carry it.
  - (d) **A non-multiplicative member of the class (P1, P2 and P3 all hold, in outline).**
    - Definition: g5'(n) = mu(n_R) v(n/n_R), where n_R is the R-part of n, v(h) = g3'(h) for h - 2 > x^{0.9}, and
      v(h) = 0 otherwise. Below x^{0.9} no fake semiprime can compensate the primes.
    - P2 holds by construction. P3 is Heuristic, as in (c).
    - Its correlation is the R-free part: sum over p with p + 2 having no prime factor in R, which is about
      prod_R (1 - 1/(l-1)) ~ (1/2)(log x)^{-0.1} of pi(x) (Mertens). The cross terms e = n_R > 1 are twin-type
      correlations (eh - 2, h - 2). By an upper-bound sieve (standard, not re-read) they are
      << x L^{0.1-1+o(1)}. This is Heuristic, and the toy numbers agree.
    - Consequences:
      - (i) Heuristic: the class defined by P1, P3 and P2 restricted to R = (exp(L^{1/10}), exp(2L^{1/5})]
        contains functions with correlation of order (log x)^{-0.1} pi(x). So no proof that uses only these
        properties of the target can beat (log x)^{-0.1}. The exponent 0.1 comes from LWW's window for the
        auxiliary primes: 1/10 < a_i < 1/5 in (2.12). This is consistent with Theorem 1 (o(1)) and with Remark 2
        ((log log x)^{-A}). The no-go criterion is NOT triggered.
      - (ii) If P2 holds only on a set S of 1/p-mass s (for example, b fixed families, s = bK log 2), the same
        construction gives correlation about e^{-s}. So the b → ∞ step of p. 70 genuinely needs P2 on sets of
        divergent mass. It is also quantitatively consistent with LWW's bound x sqrt(C_{K,rho}/b): from (2.14) and
        (2.24), W vanishes on all but a fraction 2^{-K} + o(1) of the reduced classes, so C_{K,rho} >= 2^K - 1
        (Proved here, elementary, outline), and 2^{-bK} <= sqrt((2^K - 1)/b).
  - No model with P1-P3 and correlation >> pi(x) was found. The heuristic reason: for p + 2 with a large R-part, a
    class function sees primes only through sign sums over the orbit {e h : e R-composed}, and those orbits are huge.
    If the LWW argument is correct, non-existence follows, since the argument uses only P1-P3 of the target. The
    converse does not hold. Open.

### 3. Numerical check (Computed; toy scale, an illustration, NOT a verification)
Command: `/usr/bin/python3 -I code/parity/lww_mu_vs_lambda.py 1e7 100`. Output in `code/parity/lww_mu_vs_lambda.out`;
the run took 2 min and used about 1.5 GB.

Setup:
- Window N in (5·10^6, 10^7], with R = {5, ..., 31}.
- Fake primes: semiprimes with p_1 > X_0^{0.4} = 478, block-mass-matched. Weight/L is at most 2.45 on the window
  and 4.08 for m >= X_0^{0.9}.
- Columns:
  - "corr" is sum_p f(p+2)/#p over the 316,067 primes in the window.
  - "P2" is the fraction of 2·10^5 random pairs (d, v) with f(dv) = (-1)^{omega(d)} f(v), counting only pairs
    where one side is nonzero.
    - The column tests sigma = -1 only. mu^2 (0.331) satisfies P2 with sigma = +1, which the column does not
      test, and g = 1 satisfies P2 with sigma = +1 without vanishing at p^2, like lambda.
  - S_red and S_2 are sum_{m<=100} of max over classes and z of the partial class sums, divided by the mass
    sum |f|. S_red uses the reduced classes of (3.1). S_2 uses the class N ≡ 2 (mod q) of T_1 and T_2. The noise
    baseline is |f| times random signs.
    - S_2 starts at q = 3, so it does not test the q = 1 (d = 1) term of T_1. That term needs zero mean in the
      reduced classes mod d | P, which S_red covers only for d <= 100.

| target | corr | P2 | S_red | S_2 | noise S_red / S_2 |
|---|---|---|---|---|---|
| mu | -0.0009 | 1.000 | 0.023 | 0.006 | 0.017 / 0.005 (random ±1) |
| lambda | -0.0000 | 1.000 | 0.017 | 0.005 | same |
| mu chi_{-4} | +0.0019 | 0.471 | 0.032 | 0.008 | same |
| mu^2 | +0.748 (A_2 = 0.748) | 0.331 | 4.52 | 2.07 | — |
| (-1)^{omega_R} | +0.136 (pred. 0.136) | 1.000 | 0.84 | 0.46 | — |
| g3, model sieved only to D = 30 | +0.588 | 0.015 | 0.37 | 0.22 | 0.054 / 0.002 |
| g3' (semiprime fake) | +0.981 | 0.000 | 0.037 | 0 | 0.074 / 0 |
| g5' | +0.398 (R-free part 0.3986; cross terms -0.0003; R-free fraction 0.406) | 1.000 | 0.075 | 0.0085 | 0.116 / 0.011 |

Reading:
- The numbers match Finding 2.
- One instructive failure: a target built from a sieve model at small level (g3, D = 30) is caught by S_2, the
  classes N ≡ 2 (mod q) that the Type I sums actually use. Only a model sifted to the Type I level x^{2/5}, which
  must contain semiprimes, passes. This is the parity phenomenon in target form. I first used the D = 30 model and
  wrongly expected it to pass P3; the S_2 column corrected this.
- At this size the R-free density (0.41) is far from its asymptotic (1/2) L^{-0.1}.

## First unresolved implication
"P2 for mu at every prime of R ⟹ T_3(mu W) = o(x)": the step at p. 15 with (4.6), then Prop. 4.2 for arbitrary
coefficients, then Prop. 5.3. Model (c) shows, heuristically, that P1 and P3 alone are compatible with T_3 of order
x. Model (d) shows, heuristically, that P1-P3 (with P2 on R) are compatible with correlation of order (log x)^{-0.1}. So the step must use P2, and in fact
on sets of divergent 1/p-mass.

## Not checked
- Props. 4.2 and 5.3 themselves, and Sections 4.2-5.2 beyond the text search.
- Whether those sections allow prime sets thinned by a congruence, as the mu*chi repair needs.
- Rigorous P3 for g3' and g5': this would need BV for semiprimes in ranges, and the R-sieve combined with BV. These
  are standard results that I did not re-read.
- The upper-bound sieve for the cross terms of g5'.
- Section 6.
- Whether a version newer than v2 exists: the abs page was not opened this session; the v2 PDF was fetched by its
  pinned URL.
- No audit by a fresh agent.

## Scripts
`code/parity/lww_mu_vs_lambda.py` with `.out` (numpy; toy scale). No Lean.

## Audit (fresh-context, Session 50)
The coordinator relayed a fresh-context adversarial audit with ten findings. All were accepted, and the
classification is unchanged (located).
1. **ERROR (g3' Type I).** It is not true that the Type I sums vanish identically. The q > 1 terms vanish up to
   prime powers (O(x^{1/2+o(1)})). The d = 1 term of T_1 is o(x) only by P3 (Heuristic). Fixed in Finding 2(c),
   and the S_2 limitation is now noted in Section 3.
2. **SLIP.** "P2 is used only ... on p. 15" contradicted the use in (3.7). It now reads: for g3' the Type I sums are
   handled directly, so the only place P2 is needed is p. 15.
3. **OVERSTATEMENT.** "Equivalent to the claim" is replaced by: non-existence follows if the LWW argument is
   correct; the converse does not hold; Open.
4. **OVERSTATEMENT.** The (log x)^{-0.1} ceiling is now labelled Heuristic and restricted to P1, P3 and P2 on R. The
   exponent 0.1 is attributed to LWW's window.
5. **OVERSTATEMENT.** "Pinned down" now says heuristically, because g3' has P3 only heuristically. "Nothing else
   ... can carry it" now says "appears to".
6. **GAP (mu*chi).** Added the splitting of T_3 by (m, n) mod q_0 as the main heuristic repair. I checked it against
   the PDF: Prop. 4.2 (p. 18) allows arbitrary coefficients; Prop. 5.3 (p. 63) assumes alpha = mu R_Z; Prop. 2.2
   (pp. 5-6) covers characters of modulus up to (log x)^B. Marked "needs Prop. 5.3 with a twist by characters mod
   q_0; not checked".
7. **OVERSTATEMENT (Remark 1).** Replaced by "not covered verbatim; pigeonhole thinning reduces it to the thinned-set
   question (plus K·epsilon errors)". The card notes that Remark 1 is hedged and that no error by LWW is implied.
8. **GAP.** Lambda^flat is now defined explicitly, both asymptotically and as the script implements it. The toy
   maximum 2.45 is compared with 1/log 1.5 ≈ 2.47.
9. **SLIP.** Added a note that the P2 column tests sigma = -1 only, covering mu^2 and g = 1.
10. **SLIP (script).** In the docstring, R is now {5,...,31} and the runtime is about 2 minutes. The duplicate D and
    `small` definitions are removed. A comment on the S_2 and P2 limitations was added. The script was re-run with
    /usr/bin/python3 -I; the new .out is identical to the old one apart from the removed `time` lines.
