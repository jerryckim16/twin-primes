# Route card: Type II sums from Gowers norms (Green-Sawhney) and twin primes (19 Nov 2026, Session 34)

Bounded attempt (about 1.5 hours). Nothing here bears on the twin prime conjecture, which stays OPEN. The parity paper is
frozen at v1.0; this card is NOT in the paper.

## Why this mechanism (new for the project)
Earlier cards treated Gowers norms only as a global smallness condition that is blind to shift-2 correlations
(2026-11-17-gowers-infinite-complexity.md), and Type II sums only through classical bilinear structure (FI98, HB01;
2026-11-14 card). Green and Sawhney (GS) combine the two in a new way: they break parity for primes of the form
x^2 + n y^2 with x, y prime by proving the Type II estimates themselves from Gowers-norm smallness of the coordinate
weights. The question is whether this hybrid can carry a twin condition.

## Source (Literature; read in this run)
B. Green, M. Sawhney, *Primes of the form p^2 + nq^2*, arXiv:2410.04189v3 (6 Jun 2026; "accepted in Acta Math." is
taken from the arXiv listing, not the PDF), 59 pp., SHA-256 741b8ebc72b401e912f99a14b74572de4047921194f6c176715a5d6f14635e4f (PDF not kept).
Read: Section 1 (pp. 1-7), Prop. 3.4 (statement), Section 4 with Props. 4.1-4.5 and the proof of Prop. 4.1 (pp. 18-23),
the remark in Appendix B on the size of k. Not read: Sections 3, 5-8 in detail (the sieve of Prop. 3.4 is used only as GS state it).
What we use, as stated there:
- Prop. 4.1 (Sec. 4.1; Thm 1.1 is its smoothed form): for n = 0 or 4 mod 6,
  sum_{x^2+ny^2 <= X} Lam'(x) Lam'(y) 1[x^2+ny^2 prime] = pi kappa_n X/(sqrt(n) log X) + O(X (log log X)^2/(log X)^2),
  kappa_n as in (1.1) (frequency l = 0).
- The sum is a sum of w(p) over prime ideals p, with w in "product form" f (x) f'(y) (p. 3, (1.3); (2.2)).
- Prop. 4.2 (Type I) and Prop. 4.3 (Type II, levels delta^{-C} << L <= X^{3/8}): if the Type I (resp. Type II, any
  1-bounded alpha, beta) sum is >= delta X, then BOTH ||f||_{U^k[X^{1/2}]} and ||f'||_{U^k[X^{1/2}]} are
  >= (delta/((|l|+1) log X))^{O(1)} (k = 3 for Type I; k very large for Type II).
- Proof of Prop. 4.1 (p. 22, (4.22)-(4.23)): w = w1 + w2 + w3 with f1 = Lam', f1' = f2 = Lam' - Lam_Cramer,
  f2' = f3 = f3' = Lam_Cramer. For w1 only f1' is Gowers-small, and that suffices (contrapositive of Props. 4.2-4.3
  plus Prop. 4.4: ||(Lam' - Lam_Cramer) 1_[X^{1/2}]||_{U^k[X^{1/2}]}^{2^k} <<_A (log X)^{-A}, which combines Leng's
  bound (4.17), Tao-Teraeviainen (4.18) and Siegel's theorem, hence is ineffective). They take delta = (log X)^{-12}
  and rescale functions bounded by log X. The sieve (Prop. 3.4) needs the POINTWISE bound
  |f_j|, |f_j'| <= Lam_Cramer + Lam' (constant 1) and gives sum_p w(p) << X (log log X)^2/(log X)^2. The main term
  (Prop. 4.5) is evaluated only for Lam_Cramer x Lam_Cramer.
- p. 3: "for parity reasons one cannot hope to show that there are infinitely many primes of the form x^2 + y^2 with both
  x and y prime" short of x^2 + 4. Here "parity" is parity mod 2 (x, y odd forces x^2 + y^2 even), a local obstruction,
  not the Liouville parity problem.

## The mechanism in the project's language
Two kinds of prime detector occur.
- OUTER: 1[N(a) prime] for an ideal a of Q(sqrt(-n)). Its Type II structure comes from N(ab) = N(a) N(b): the
  parity-twisted weight lambda(N(ab)) = lambda(N a) lambda(N b) is absorbed into alpha, beta, so the fair weight
  1 + lambda(N(gamma)) is inconsistent with a Type II input at the GS levels. This is the classical way to break parity
  (same as FI98, HB01).
- INNER: f(x), f'(y), arbitrary weights of the two coordinates; GS need only that ONE of them minus a model is
  Gowers-small. This is the new part.

## Success / no-go criteria (fixed before work)
- Success: a placement of a fixed-shift twin condition (two prime detectors whose arguments differ by 2 identically, on an
  infinite family) into the GS framework such that the needed inputs are known unconditionally, or a reduction of a
  twin-type statement to an input strictly weaker than the twin asymptotic.
- No-go: every placement is either circular (needs the twin asymptotic or more as input) or not of GS form.

## Result (Proved here; elementary; possibly folklore)
Every placement fails, in one of four ways.
1. **Twin condition inside one coordinate (circular).** Put f(x) = Lam'(x) Lam'(x+2) - F(x) for a model F, rescaled
   by (log X)^{-2} to be 1-bounded. At GS's precision (delta = (log X)^{-12}, contradicted through Prop. 4.4 with A
   large) the input needed is ||f/(log X)^2||_{U^k[N]} <= (log N)^{-A'}. The U^1 average is controlled by U^2: in GS's
   normalisation ||g||_{U^1[N]} = |sum g|/N, and |sum g|/N << ||g||_{U^2[N]} for g supported on [+-O(N)] (zero Fourier
   coefficient, or Cauchy-Schwarz); then (4.14) (which starts at U^2) gives U^2 << U^k. So the input already contains
   sum_{x<=N} Lam'(x) Lam'(x+2) = sum_{x<=N} F(x) + O_A(N (log N)^{-A}), the twin asymptotic with a power-of-log error
   (qualitative smallness o(1) would already give an o(N) error, i.e. the twin asymptotic). Circular. The same holds for
   any fixed shift h.
2. **Twin condition in the outer detector (no bilinear structure available).** For two outer detectors
   1[N(gamma) prime] 1[N(gamma + 2) prime] (Gaussian twin primes, twin norms), the factorisation gamma = ab gives no
   factorisation of gamma + 2, and no way is known to write lambda(N(ab)) lambda(N(ab + 2)) as alpha_a beta_b. GS's
   Type II mechanism needs w in product form on ideals; the twin weight is not known to be of any such form. This is
   the (B)-type input of FI98 (card 2026-11-14), not new.
3. **Twin condition on a curve (no two-dimensional averaging).** The prime-detected quantities are x, y (inner) and
   Q(x, y) = x^2 + n y^2 (outer). A fixed difference 2 between Q and a coordinate (Q(x, y) - x = 2, or with y, signs,
   affine images) holds only on a conic, and y = x + 2 between the two coordinates only on a line. On such
   one-dimensional sets the weight is not of product form and the GS averaging over (x, y) is not available (the
   fixed-y degeneration is Landau's x^2 + 4 problem, GS p. 3). A difference that is NOT fixed is harmless: GS remark that
   "x and y - 1 prime" should be within reach (p. 2), an independent shift of one coordinate.
4. **Twin weight carried but not evaluated.** Taking the twin weight as the non-small factor, f(x) = Lam'(x) Lam'(x+2)
   and f' = Lam' - Lam_Cramer, is of GS form and not circular, but fails twice: (i) f violates the pointwise majorant
   |f| <= Lam_Cramer + Lam' of Prop. 3.4 by a factor about log X, and after rescaling the GS error term
   X (log log X)^2/log X exceeds the expected size X/log X of the twin-weighted sum by (log log X)^2; (ii) even with a
   better error term, the remaining sum sum f(x) Lam_Cramer(y) 1[Q prime] still counts twin primes x, and Prop. 4.5
   evaluates only Lam_Cramer x Lam_Cramer. So the twin condition can at best be carried along, not produced, and at GS's
   stated precision not even carried. (Heuristic numerics for the carried form: exploration of this run,
   code/explore/gs_twin_carry.py.)

**Classification: located (literature + elementary observations; folklore in substance).** First unresolved
implication: a Type II (bilinear) structure for n -> lambda(n) lambda(n+2), or Gowers-uniformity of
Lam(x) Lam(x+2) - model, which by item 1 already contains the twin asymptotic. The GS mechanism breaks parity for one
multiplicative (norm-form) detector, with additive (Gowers) control of the coordinates; twin primes offer neither a
second multiplicative structure nor a finite-complexity additive one. No parity-breaking content for twin primes.

## Computation (Computed, numerical sanity check only)
code/parity/gs_norm_form_check.py [X] [PKAPPA] (/usr/bin/python3 -I; < 1 min at X = 1e9, ~0.7 GB), output
code/parity/gs_norm_form_check.out. It checks that we read the constant and normalisation of Prop. 4.1 (n = 4, l = 0)
correctly: kappa_4 ~ 2.21344 (partial products to 1e6, 1e7, 1e8 agree to 4e-5), FI's c = pi kappa_4/8 ~ 0.86922, and
the ratio of the sum to (pi kappa_4/2) int_2^X dt/log t is 0.944, 0.969, 0.982 at X = 1e7, 1e8, 1e9 (to X/log X:
1.012, 1.029, 1.035; the error term is (log log X)^2/log X relative). Consistent with the theorem; not decisive for
anything above, which is a proof.

## Not done / sources
- GS's forthcoming paper on Gaussian-prime corners (cited as [16] in GS, p. 3) would be an average over a shift d (as in
  MRT, card 2026-11-17); not opened, not cited further.
- Merikoski's alternative argument via the multiplicative large sieve (remark after Prop. 4.2) not opened.
- Literature check: GS read as above; one web search (see the log). Possibly folklore; we claim nothing new about GS.

## Audit (fresh-context adversarial helper; mathbox not available)
Checked every attribution against the pdftotext of GS v3 and re-ran the script (independently recomputed FI's c from the
Conjecture 1.2 product to 1e7: 0.869223 vs pi kappa_4/8 = 0.869217). Found 3 errors in the first draft, all fixed above:
item 1 was stated at a strength that is trivially true (now at GS's power-of-log precision); (4.14) starts at U^2 (the
U^1 step is now argued directly); the "positive by-product" misstated Prop. 3.4's majorant (constant 1, pointwise) and
ignored that GS's error term is too weak for weights of twin density (now item 4). Gaps fixed: the fourth placement,
the line y = x + 2, the attribution of Prop. 4.4, "not known to be" in item 2; section and page references corrected.
