# Rung 186: the cap forms I_H and J_{lambda,H} of [14] (transcription for an independent evaluator)

Source [14]: OpenAI, "Numerical certificate for prime gaps at most 186", short_gaps_numerics.pdf, 23 pp., dated
30 August 2026 (PDF CreationDate 1 Sep 2026). Fetched 13 Nov 2026 with WebFetch from
https://raw.githubusercontent.com/openai/PrimeGaps186/main/short_gaps_numerics.pdf (218865 bytes), copied to
/tmp/claude-0/oai186/dl.DUI6/, read with `pdftotext -layout` (and `-raw` to cross-check Table 1.1). Nothing from the
repository was executed. "p." = printed page number of [14]; equation numbers are those of [14].

**Status of everything below: Claimed (read from [14]).** Displayed formulas are transcribed from the pdftotext
output; where the extraction is garbled, my reading is marked "[reading]" and the doubt is stated. Notation
in ASCII: rho_D = Dickman function, gamma = Euler's constant, L(.) = probability law.

---------------------------------------------------------------------------------------------------------------
## 1. Fragment configurations, nu_c, Dickman convention (Sec. 1, p. 1)

- For c > 0, Pi_c = Poisson process on (0, c] with intensity dv/v, and (p. 1, unnumbered display)
      nu_c := e^gamma c L(Pi_c),        nubar_c(dt) := rho_D(t/c) dt.
  nubar_c is the total-size pushforward of nu_c ([14] cites Arratia-Barbour-Tavare (2.4)-(2.6)).
  Hence the total mass of nu_c is e^gamma c = int_0^inf rho_D(t/c) dt; e^gamma never has to be evaluated separately
  in the cap forms (they only use the cell masses of rho_D(t/c) dt).
- For 0 < b <= c: P(no points in (b,c]) = b/c, so nu_c restricted to {max X <= b} equals nu_b. nu := nu_zeta,
  zeta the ambient cap of (1.13): zeta := 19037/(100000 rho). Smaller caps are restrictions of the same measure.
- A fragment configuration is a multiset X with total |X| := sum_{p in X} p. For Y = (X_j)_{j != i}, Y (+)_i X
  inserts X in coordinate i. Erased-coordinate operator (p. 1):
      E_i F(Y) := int F(Y (+)_i X) d nu(X).
- Dickman convention (p. 2, Sec. 1.1; p. 12): "a coordinate total under a largest-fragment cap c has density
  rho_D(t/c) dt. Totals exceeding c are allowed." D_c(t) := rho_D(t/c) for t >= 0, 0 for t < 0, with
  D_c'(t) = -D_c(t-c)/t (rho_D(u) = 1 on [0,1]). Cell mass A_j(c) := int_{C_j} D_c(t) dt; d_c(j) := A_j(c)/h
  (p. 14). "The normalized fragment law requires no further conditioning on the cap" (p. 12).
- Caps apply to each fragment, not to coordinate totals (p. 5). On the grid the fragment cap is rounded down to
  a multiple of h: cap = h floor(z/h) (1.19); the z/h column of (1.5) gives these integers.
- Rigorous enclosures of d_c(j) for c = M h: Lemma 2.2, recurrence (2.1) and cell bound (2.2) (p. 12):
      dlow_{j+1} := max{0, down( dlow_j - dup_{j-M}/(2j) - dup_{j+1-M}/(2(j+1)) )},
      dup_{j+1}  := min{1, up( dup_j - dlow_{j-M}/(2j) - dlow_{j+1-M}/(2(j+1)) + 1/(2M^3) )}   (j >= M),
  initialised dlow_j = dup_j = 1 for 0 <= j <= M [reading: which bar is upper/lower is lost in extraction; the
  above is the only monotone-consistent assignment]. For j < M, A_j(c) = h; for j >= M
      max{0, down( (h/2)(dlow_j + dlow_{j+1}) - h^3/(12 c^2) )} <= A_j(c) <= up( (h/2)(dup_j + dup_{j+1}) ),   (2.2)
  intersected with [0, h]. For an unaligned cap use c^- = h floor(c/h) (lower) and c^+ = h ceil(c/h) (upper).
  (The renewal majorant (2.3) is used only for the small source-loss caps, not for I_H, J.)

## 2. The trial function F (Sec. 1.1-1.2, pp. 1-3)

Parameters (1.1)-(1.2), p. 1-2: k = 40, S = 2742997/2624989, rho* = 2624989/10^7, T0 = 2499106033/2624989000,
T1 = 2510000/2624989, rho = 262499/10^6; rho* S = 2742997/10^7, rho* T0 = 2499106033/10^10, rho* T1 = 251/1000.

Grid (1.3), p. 2:
      N := 98304,  h := S/N,  n := N - 40 = 98264,  C_j := [jh, (j+1)h),  t°_j := (j + 1/2) h.
Shell rule (1.4): a d-coordinate cell with index sum r is in radial shell (u, v] iff u < (r+d)h <= v, 0 <= r < n
(i.e. the FULL upper endpoint (r+d)h of the cell's total is used).

Cap domains (1.5), p. 2. j = sum of coordinate indices (inclusive ranges a:b), z/h = per-fragment cap in units h:

| domain           | j-range         | z/h   |
|------------------|-----------------|-------|
| outer H_O (d=40) | 0 : 89196       | 68225 |
|                  | 89197 : 95598   | 49152 |
|                  | 95599 : 98263   | 46580 |
| base H_0 (d=39)  | 0 : 84930       | 68225 |
|                  | 84931 : 87194   | 44781 |
|                  | 87195 : 89524   | 35265 |
| enlarged H_1 (d=39) | 0 : 85161    | 68225 |
|                  | 85162 : 87249   | 44976 |
|                  | 87250 : 89914   | 35419 |
| full H_f (d=39)  | 0 : 98263       | 68225 |

H_0 subset H_1 subset H_f (p. 2). Continuous origin of these masks: (1.18)-(1.19), p. 5 (not needed for the
evaluator if the integer masks are taken as given). Largest retained totals S_box = 98303h, T0_box = 89563h,
T1_box = 89953h (p. 5).

Signatures and power sums (p. 2): t = (t_i), t_i = |X_i|, s := sum_i t_i, P_j(t) := sum_i t_i^j,
P_sigma := prod_{j in sigma} P_j, P_() := 1. Ordered signature list (1.6):
      S := ( (), (2), (3), (4), (5), (6), (2,2), (2,3), (2,4), (3,3), (2,2,2) ).
Radial degrees 0 <= d <= 6. Profile (1.7):
      g(t) := (21/200)/(1 + t/100) + (179/200)/(1 + (907/5) t).
Continuous trial (1.8):
      Ftilde(X) := 1_{H_O}(X) prod_{i=1}^{40} g(t_i) sum_{sigma in S} sum_{d=0}^{6} c_{sigma,d} (s - 9/10)^d P_sigma(t).
Coefficients (1.11): c_{sigma,d} := 10^-10 C_{sigma,d}, C from Table 1.1 (section 4 below). 11 x 7 = 77.
"Rational midpoint step function" (p. 2, verbatim): "The trial used below is the step function F obtained from
Ftilde on the grid (1.3). On each cell, evaluate the profile and polynomial at the rational midpoint, using
(r + 20)h - 9/10 as the radial argument. All face forms use the same outer trial and unrestricted face."
So on a 40-cell with indices (j_1..j_40), r = sum j_i: F = 1_{H_O} prod g(t°_{j_i}) sum c_{sigma,d} x_r^d
P_sigma(t°), x_r := (r+20)h - 9/10 (also p. 14). All values rational.

Normalisation (p. 2): Z := sum_{j<n} g(t°_j)^2 > 0; every quadratic form (norms, pairings, losses) is divided by
(hZ)^40, with the same notation kept. V_i := E_i F, and (1.9)-(1.10), p. 3:
      I_H := ||F||_2^2,   J_0 := sum_i int_{H_0} |V_i|^2 dnu^39,   J_+ := sum_i int_{H_1 \ H_0} |V_i|^2 dnu^39,
      J_t := sum_i int_{H_f \ H_1} |V_i|^2 dnu^39.
"In the square of V_i, the two integrated coordinates are independent copies conditional on the same retained
fragment configuration." Hybrid combination (1.27)-(1.29), p. 8: kappa_def = 1/50000, m0 = 49999/50000,
K_ex = 17/50, lambda = 1/125, a_h = m0^2 - m0 lambda = 2479900401/2500000000,
b_h = (1 - m0/lambda) kappa_def K_ex = -843183/10^9, d0 = 1 - a_h - b_h = 44415113/5000000000, and
      J_{lambda,H} = J_0 + (a_h + b_h) J_+ + b_h J_t.                                                   (1.29)
Quotient: rho* J_{lambda,H} / I_H.

## 3. Finite contractions for I_H and J (Sec. 2.2, pp. 14-15; precision Sec. 2.3, pp. 16-17)

Notation (p. 14): t_j := (j+1/2)h, x_r := (r+20)h - 9/10, p_sigma(r) := sum_{d=0}^{6} c_{sigma,d} x_r^d,
d_c(j) := A_j(c)/h. All radial polynomials reduced mod X^n. sigma ⊔ tau = sorted concatenation.
For a nonnegative coordinate array K (2.10):
      P_e[K](X) := sum_{j<n} K_j t_j^e X^j,
      M_{d,sigma}[K](X) := sum_{pi in Part(sigma)} (d)_{|pi|} P_0[K]^{d-|pi|} prod_{B in pi} P_{sum_{v in B} v}[K].
[reading: the extracted text shows "P_P v [K]" with "v in B" beneath; I read the subscript as e = sum of the
entries of block B.] (d)_r = falling factorial; equal entries of sigma are distinct labels for set partitions;
the empty signature gives P_0[K]^d.
Cap moments (p. 15): K_j(c) := g_j^2 d_c(j)/Z, M^c_{d,sigma} := M_{d,sigma}[K(c)], and (2.11)
      Q_eta(r) := sum_{sigma,tau in S, sigma ⊔ tau = eta} p_sigma(r) p_tau(r)   (ordered pairs).
With c_s, s = 1,2,3, the decreasing outer caps (68225h, 49152h, 46580h) and chi_s their radial masks in (1.5):
      I_H = sum_{s=1}^{3} sum_{r<n} chi_s(r) sum_eta Q_eta(r) [X^r] M^{c_s}_{40,eta}.                     (2.12)
"Each signed square uses one coherent cap measure."

Erased marginal, affine rows (2.13), p. 15 (A = labelled subset of positions of sigma, e(A) := sum_{j in A} sigma_j):
      v_{s,tau}(r) := sum_{sigma in S, 0<=d<=6, A subset {1..|sigma|}, sigma\A = tau} c_{sigma,d}
                      sum_{a=0}^{n-1-r} chi_s(r+a) x_{r+a}^d g_a d_{c_s}(a) t_a^{e(A)}
(from P_j(t, t_a) = P_j(t) + t_a^j). v^(l)_tau := sum_{s<=l} v_{s,tau}, c_4 := 0. "When the largest shared fragment
lies in (c_{l+1}, c_l], the actual marginal is v^(l); form this signed sum before squaring." Note the erased
coordinate carries g^1 (not g^2) and no 1/Z. Pairing (2.14):
      S(v, M; A) := sum_{r<n} A(r) sum_{tau,upsilon} v_tau(r) v_upsilon(r) M_{tau ⊔ upsilon}(r).
Layers (p. 15, verbatim in substance): "List all distinct positive cap values increasingly as b_1 < ... < b_t,
put M^{b_0} := 0, and set Delta M^a := M^{b_a}_{39,.} - M^{b_{a-1}}_{39,.}. These are positive layer measures. Let
l(a) := #{s : c_s >= b_a}, and let chi_{0,a}, chi_{1,a}, chi_{f,a} be the three face masks in layer a." Then (2.15):
      J_0 = (40h/Z) sum_{a: l(a)>0} S(v^(l(a)), Delta M^a; chi_{0,a}),
      J_+ = (40h/Z) sum_{a: l(a)>0} S(v^(l(a)), Delta M^a; chi_{1,a} - chi_{0,a}),
      J_t = (40h/Z) sum_{a: l(a)>0} S(v^(l(a)), Delta M^a; chi_{f,a} - chi_{1,a}).
"Nestedness makes these masks nonnegative. Enclose each layer difference from both sides and intersect with the
interval from zero to its cumulative upper bound."
UNCLEAR in [14]: (i) which cap values enter b_1 < ... < b_t (presumably the union of the outer caps
{46580, 49152, 68225}h and the face caps {35265, 35419, 44781, 44976, 68225}h, but not stated); (ii) the exact
definition of the "face mask in layer a" (presumably chi_{0,a}(r) = 1 iff r is in a base row of (1.5) whose cap
is >= b_a, similarly for enlarged/full); the M^{b}_{39} in a layer use K(b) built with the same g_j^2/Z.
These two points must be fixed by our own derivation (or by reading their script, which would not be independent).

What is convolved, and precision (pp. 11, 16-17): all objects are 1-D arrays indexed by the cell index (length
n = 98264), products are polynomial products mod X^n (powers P_0^{40-k}, P_0^{39-k} times products of P_e). The
correlation in (2.13) uses (2.24): sum_{r=j}^{n-1} I_r K_{r-j} = [X^{n-1-j}] (sum_r I_{n-1-r} X^r) K(X).
Coordinate enclosures (g, Z, d_c via (2.1)-(2.2)) at 160-bit Arb balls; positive polynomial products as
integer polynomials with binary scale Q = 2^b and floor/ceil rounding (2.22)-(2.23), b = 224 for cap moments
(b = 192 for source moments); final signed reductions in binary64 with the gamma_r error bound (2.26) (p. 17).
Production: python-flint 0.9.0 / FLINT 3.6.0 with a signed-FFT bug fix (FLINT PR 2790). [14] p. 21: "The
independent exact replay checks identities, coverage, and rational arithmetic from those records; it does not
recompute their integrals."

## 4. Table 1.1 (p. 3): C_{sigma,d}, d = 0..6, c_{sigma,d} = 10^-10 C_{sigma,d}

Fully legible; extracted by `pdftotext -layout` and `-raw`, the two agree; 77 integers parsed mechanically
(order as in (1.6)):

```json
[
 {"sigma": [],        "C": [10000000000, -264598476112, 834262268474, -3540575351215, 5377491111325, 116705356572254, 121730820431102]},
 {"sigma": [2],       "C": [71070047507, 7222861788586, -48747932657986, 290976672545723, -1136422724027134, -2058910631434711, 1375878942948547]},
 {"sigma": [3],       "C": [6457252424873, -61201446212885, 28811649792090, -2058803084231281, 9970156747759406, 38278849934023144, 34806920812932737]},
 {"sigma": [4],       "C": [-16779263512274, 128033707910825, 169290603857215, 7359669931312727, -35090795379920588, -120997133235510923, -141527585901304670]},
 {"sigma": [5],       "C": [28114161526671, -276375633435566, -690482702304933, -15120456749385986, 47650276584638031, 372137534144492224, 2191913505882230103]},
 {"sigma": [6],       "C": [-21150553032771, 379875924448266, -929062247569514, -13967219843969236, 168416050564605519, -248058724714138769, -4161797957833172083]},
 {"sigma": [2, 2],    "C": [-19004216224617, 136674974139652, -183344485344333, 1114879023072977, 1119583327002910, -47568062965320963, 2537631525616777]},
 {"sigma": [2, 3],    "C": [31171802814567, -97428388152051, 526635309233054, 1222047580792220, 15846796161434448, -165623953461271580, -2358019996221938729]},
 {"sigma": [2, 4],    "C": [-53602626608739, 329397902441121, 1613505134333316, 13893066541430270, -126262434123562668, 239934302929501943, -1506861482386002243]},
 {"sigma": [3, 3],    "C": [27653330903418, -290549334488305, -1847330641348475, 28351866831729468, -61505472221886320, -424266003419714347, 2585236507449911535]},
 {"sigma": [2, 2, 2], "C": [12374547113901, -244168600145684, 1603694896120437, -21603130476787649, -30285492734943698, 381987976419637874, 3605516061450295448]}
]
```

## 5. Lemma 2.5 and L^+ (pp. 18, 21)

Lemma 2.5 (Finite evaluation), p. 21:
      23685317816 * 10^-24 <= I_H <= 23685317890 * 10^-24,    J_{lambda,H} >= 90248755123 * 10^-24,     (2.33)
      L^+/I_H <= 696075110/10^12 < 697/10^6,    rho* J_{lambda,H}/I_H > 500103/500000.                  (2.34)
(Normalised by (hZ)^40.) Proof: evaluate (2.12), (2.15) with directed rounding; "the lower numerator uses lower
endpoints for J_0, J_+ and the upper endpoint for J_t" (since a_h + b_h > 0, b_h < 0).
L^+ (p. 18): outer component loss E_j := c_j R_j + V_j/c_j (2.27) with R_j, V_j the forms (2.17), (2.21); inner
components use (2.19) times d0 = 44415113/5000000000 (old) or 1 - b_h = 1000843183/10^9 (new) (2.28).
"Let L^+ be the sum of all these 97 component bounds"; then L^+ >= d0 beta_old + (1 - b_h) beta_new + E_O (2.29).
Tables 2.1-2.6 (pp. 18-20) list them; Table 2.7 group totals (10^12 L^+/I_H^-): O_2 38927522, O_5/2 622829241,
I2old 55254, I5/2old 435544, I2new 1405159, I5/2new 32422390; total 696075110.

## 6. Cost of an independent re-evaluation of I_H and J (my estimate, not from [14])

- No 40-dimensional cell enumeration: by symmetry everything is 1-D arrays of length n = 98264 (radial index r).
- Signatures: |{sigma ⊔ tau}| = 53 distinct eta (max length 6), 692 set partitions in total; block sums e in
  {0, 2, ..., 12} (11 nonzero values). Sub-signatures tau after erasure: the same 11 as S.
- I_H: 3 caps x 12 arrays P_e; for each cap the distinct monomials P_0^{40-k} prod P_e (k <= 6): of order 10^2
  length-98264 polynomial products per cap, then a length-n dot product with Q_eta. J: the same for M_39 over
  the (~6-8, see unclear point (i)) layer caps, plus the rows v_{s,tau}: per (sigma, d, A, s) one length-n
  correlation (2.24) -- roughly 11 signatures x 7 degrees x <=8 subsets x 3 shells ~ 10^3 FFT correlations
  (fewer after merging by tau and e(A)).
- Precision: entries of C reach 3.6e18 (c ~ 3.6e8) with heavy cancellation; [14] needed 224-bit fixed point.
  Exact rationals are not possible because d_c(j) (Dickman cell masses) are transcendental; an interval
  evaluator (own Dickman enclosure per (2.1)-(2.2), or an independent high-precision rho_D) is required.
  Size: a few thousand big-integer polynomial products of length ~10^5 with ~250-500-bit coefficients;
  minutes to hours on a workstation with an FFT/FLINT-class multiplier; impractical with Python Fractions.
- Main obstacles: (a) layer/face-mask definitions in (2.15) are underspecified (Sec. 3 above); (b) avoiding
  python-flint/FLINT (their stack) for independence requires another fast big-integer polynomial multiplier;
  (c) the extraction of (2.1) loses the over/under bars (reading given above).

---------------------------------------------------------------------------------------------------------------
## Session 13 (13 Nov 2026): first independent check -- Dickman cell masses (Section 1 above)
- code/oai186_dickman_cells.py: closed forms of rho_D on [0,3] (log and Li2; self-tested against quadrature and
  the delay equation) give d_j = A_j(c)/h = M (Phi((j+1)/M) - Phi(j/M)) for the seven grid caps M = z/h of (1.5)
  (68225, 49152, 46580, 44781, 35265, 44976, 35419), all cells j = M .. 98263. 40-digit floating point, not
  interval arithmetic. Output code/oai186_dickman_cells.json.
- Every grid value rho(j/M) lies in the transcribed recurrence enclosure (2.1) and every cell mass lies in the cell
  enclosure (2.2): 0 violations over 372,450 cells; smallest cell slack 5e-16, largest enclosure width 8.3e-10
  (units of h).
- The "[reading]" doubt (which bar is upper/lower) is IMMATERIAL here: the swapped assignment also contains the true
  values (M = 35265, 650 sampled points, 0 violations), because the two recurrences differ by far less than the
  margin 1/(2M^3). So this check confirms the transcription is consistent, not which reading [14] intends.
- Next sub-step: one 1-D contraction for a single signature (sigma = (), d = 0) on one cap domain, with an exact or
  interval evaluator written independently of [14]'s code.
