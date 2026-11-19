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
B. Green, M. Sawhney, *Primes of the form p^2 + nq^2*, arXiv:2410.04189v3 (6 Jun 2026; accepted in Acta Math. per the
arXiv comment), 59 pp., SHA-256 741b8ebc72b401e912f99a14b74572de4047921194f6c176715a5d6f14635e4f (PDF not kept).
Read: Section 1 (pp. 1-7), Section 4.2-4.4 with Props. 4.1-4.4 and the proof of Prop. 4.1 (pp. 17-23), the remark in
Appendix B on the size of k. Not read: Sections 3, 5-8 in detail (the sieve of Prop. 3.4 is used only as GS state it).
What we use, as stated there:
- Thm 1.1 / Prop. 4.1: for n = 0 or 4 mod 6,
  sum_{x^2+ny^2 <= X} Lam'(x) Lam'(y) 1[x^2+ny^2 prime] = pi kappa_n X/(sqrt(n) log X) + O(X (log log X)^2/(log X)^2),
  kappa_n as in (1.1) (frequency l = 0).
- The sum is a sum of w(p) over prime ideals p, with w in "product form" f (x) f'(y) (p. 3, (1.3); (2.2)).
- Prop. 4.2 (Type I) and Prop. 4.3 (Type II, levels delta^{-C} << L <= X^{3/8}): if the Type I (resp. Type II, any
  1-bounded alpha, beta) sum is >= delta X, then BOTH ||f||_{U^k[X^{1/2}]} and ||f'||_{U^k[X^{1/2}]} are
  >= (delta/((|l|+1) log X))^{O(1)} (k = 3 for Type I; k very large for Type II).
- Proof of Prop. 4.1 (p. 22, (4.22)-(4.23)): w = w1 + w2 + w3 with f1 = Lam', f1' = f2 = Lam' - Lam_Cramer,
  f2' = f3 = f3' = Lam_Cramer. For w1 only f1' is Gowers-small, and that suffices (contrapositive of Props. 4.2-4.3
  plus Prop. 4.4, Leng's bound ||(Lam' - Lam_Cramer) 1_[N]||_{U^k} << (log X)^{-A}). The sieve (Prop. 3.4) needs
  |f_j|, |f_j'| <= Lam_Cramer + Lam'.
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
Every placement fails, for one of three reasons.
1. **Twin condition inside one coordinate (circular).** Put f(x) = Lam'(x) Lam'(x+2) - F(x) for any model F. GS's
   inputs require ||f 1_[N]||_{U^k[N]} small. By the nesting (4.14), ||g||_{U^1} << ||g||_{U^k}, and
   ||g||_{U^1[N]} is |E_{x<=N} g(x)| up to normalisation. So the input already contains
   sum_{x<=N} Lam'(x) Lam'(x+2) = sum_{x<=N} F(x) + o(N (log N)^2), the twin asymptotic in the form fixed by F.
   Circular. (The same holds for any fixed shift h in place of 2.)
2. **Twin condition in the outer detector (no bilinear structure).** For two outer detectors 1[N(gamma) prime]
   1[N(gamma + 2) prime] (Gaussian twin primes, or twin norms) the factorisation gamma = ab gives no factorisation of
   gamma + 2, so lambda(N(ab)) lambda(N(ab + 2)) is not of the form alpha_a beta_b. GS's Type II mechanism needs w in
   product form on ideals; the twin weight is not. This is the (B)-type input of FI98 (card 2026-11-14), not new.
3. **Twin condition between an inner and an outer detector (impossible by degree).** The prime-detected quantities are
   x, y (inner) and Q(x, y) = x^2 + n y^2 (outer). A fixed difference 2 between Q and a coordinate, Q(x, y) - x = 2
   (or with y, signs, or affine images ax + by + c), holds only on a conic, i.e. on a one-dimensional set where the
   GS averaging over (x, y) is not available; it is never an identity, since Q has degree 2. Between two inner
   coordinates, x' = x + 2 identically means one coordinate, i.e. case 1.

Positive by-product (consistent, not new): since only one factor must be Gowers-small, GS's argument carries an
ARBITRARY bounded weight f on x along (subject to the majorant |f| <= (log X)^{O(1)} (Lam_Cramer + Lam') needed by
Prop. 3.4, which we have not checked in detail). So a twin condition on x can be carried along, but not produced:
sum f(x) Lam'(y) 1[Q prime] = sum f(x) Lam_Cramer(y) 1[Q prime] + small, and with f(x) = Lam'(x) Lam'(x+2) the
right-hand side still counts twin primes x (weighted by a Cramer-model count in y). We state this only as a reading of
GS's proof structure ((4.22)-(4.24)); we have not verified that Prop. 3.4 applies to such f.

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
