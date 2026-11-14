# Rung 186: the positive loss bound L^+ of [14] (transcription for an independent evaluator)

Source [14]: OpenAI, "Numerical certificate for prime gaps at most 186" (short_gaps_numerics.pdf, 23 pp., dated
30 August 2026). The PDF was supplied by Jerry Kim on 14 Nov 2026; it is NOT committed (copyright) and will not be
available to later sessions. Every displayed formula below was transcribed from the rendered page images (Read
tool, and 200-220 dpi crops for pp. 6 and 14), cross-checked against `pdftotext -layout`. "p." = printed page
number (= PDF page); equation numbers are those of [14].

**Status of everything below: Claimed (read from source).** This is a transcription, not our derivation.
Where the image itself leaves something open I write "[reading: ...]". My own remarks are marked "[note: ...]".

Companion notes (not repeated here): notes/sources-186-forms.md (Sec. 1.1-1.3 of [14]: nu_c, F, masks (1.5),
Table 1.1, (2.10)-(2.15)); code/oai186_support_data.py (source rows, (1.13)-(1.24), Lemma 1.1);
code/oai186_tables_2_1_to_2_6.json (Tables 2.1-2.6, the 97 component bounds and 52 Young parameters).

ASCII conventions: \overline{d}_j / \underline{d}_j = upper / lower enclosure; \uparrow(...) / \downarrow(...) =
outward (upward / downward) dyadic rounding at 160-bit real-ball precision; \mathscr{H}_0 etc. are the
script-letter domains (H_O outer, H_0 base, H_1 enlarged, H_f full); \mathscr{L}_old, \mathscr{L}_1 the actual inner
domains; [v]_+ := max(v,0); 1_{E} indicator; sans-serif P, A, B, C, B_theta, M_theta written \mathsf{...}.

---------------------------------------------------------------------------------------------------------------
## 0. Needed context from Sec. 1.3 (pp. 5-6), for convenience only (already in code/oai186_support_data.py)

- Groups, in order G1..G6: O_2, O_{5/2}, I_2^old, I_{5/2}^old, I_2^new, I_{5/2}^new. Dimensions d_G (p. 5):
  40, 40, 39, 39, 39, 39. m_G = the subscript (2 or 5/2). Parameters (d, m, xi, U, z, p_G) from (1.23)-(1.24);
  p_G = h \lfloor U_G/(2 m_G h) \rfloor.
- (1.25), p. 6: intersect the appropriate rows of (1.5) with
      \lfloor b_G/h \rfloor - d_G + 1 <= j <= \lfloor t_G/h \rfloor,      d_G in {39, 40}.
- (1.26), p. 6 (image checked): for a low bin ending at u, include every originating row (also those of the
  preceding order-two group when m_G = 5/2); with c_t, V_t the row's radial core and threshold, mu_t = 2 for source
  orders one and two, mu_t = 5/2 for order three,
      c_G(u) := max{ b_G , min_{t : xi_t < u} max{ c_t , V_t - (mu_t - 1) u } }.
  "An empty eligible set gives an empty event; otherwise retain j >= \lfloor c_G(u)/h \rfloor - d_G + 1. In
  particular, an absorbed row keeps its own order in this formula."
- Inclusive obstruction (p. 1): H_{phi,xi}(X) := max( { \sum_{q in X, q >= p} q + phi(p) : p in X, p > xi } U {0} ),
  M_xi(X) := max({p in X : p > xi} U {0}).
  [reading: "H_2", "H_{5/2}" are H_{phi,xi} with phi(p) = (m-1)p? The paper does not restate this in Sec. 1.5;
  it is the reading consistent with (1.36), see Sec. 2 below.]
- Grid: N = 98304, h = S/N, n = N - 40 = 98264, C_j = [jh,(j+1)h) (see forms note).

---------------------------------------------------------------------------------------------------------------
## 1. Sec. 1.4 from (1.30): inner charges, h_i, E_O, Proposition 1.3 (p. 8)

Context (p. 8, (1.27)-(1.29)): kappa_def = 1/50000, m_0 = 49999/50000, K_ex = 17/50, lambda = 1/125;
a_h := m_0^2 - m_0 lambda = 2479900401/2500000000, b_h := (1 - m_0/lambda) kappa_def K_ex = -843183/1000000000,
d_0 := 1 - a_h - b_h = 44415113/5000000000; J_{lambda,H} = J_0 + (a_h + b_h) J_+ + b_h J_t; quotient rho_* J/I_H.

"Charge the failures of the actual inner domains separately:"
      \beta_old := \sum_i \int_{\mathscr{H}_0 \ \mathscr{L}_old} |V_i|^2 d\nu^{39},
      \beta_new := \sum_i \int_{\mathscr{H}_1 \ \mathscr{L}_1}  |V_i|^2 d\nu^{39}.                         (1.30)
"Their coefficients are d_0 and d_0 + a_h = 1 - b_h = 1000843183/10^9, respectively. On a retained face put"
      h_i(Y) := 1                          if Y in \mathscr{H}_0,
                max{|a_h + b_h|, |b_h|}    if Y in \mathscr{H}_1 \ \mathscr{H}_0,                           (1.31)
                |b_h|                      if Y notin \mathscr{H}_1.
"If {\mathscr{B}_j} is a positive cover of the bad outer set and c_j > 0, Young's inequality gives the
nonnegative loss"
      \mathcal{E}_O := \sum_{i,j} \int_{\mathscr{B}_j} h_i(Y) ( c_j |F(Y \oplus_i X_i)|^2 + |V_i(Y)|^2 / c_j ) d\nu^{40}.   (1.32)
"Positive majorants of event indicators may be used in this formula."

"Work in L^2(\mathscr{H}_O, \nu^{40}), extending functions by zero outside the outer cap. With E_i^* the
Hilbert-space adjoint of E_i, the true face operator is"
      \mathcal{B} := \sum_i E_i^* ( d_0 R_{0,i} + a_h R_{1,i} + b_h ) E_i.
"The negative term acts on the unrestricted face." (R_{a,i}, H_{a,i}: multiplication by 1_{\mathscr{L}_a},
1_{\mathscr{H}_a} on face i, p. 5.)

**Proposition 1.3** (Signed quadratic-form restoration). For the operator \mathcal{B} defined above,
      \rho_* <P_O F, \mathcal{B} P_O F> - ||P_O F||_2^2 >= \rho_* ( J_{\lambda,H} - d_0 \beta_old - (1 - b_h)\beta_new
                                                          - \mathcal{E}_O ) - I_H.                         (1.33)
Proof (summary of p. 8): cap minus true face operator is \sum_i E_i^*(d_0(H_{0,i} - R_{0,i}) + a_h(H_{1,i} -
R_{1,i}))E_i >= 0, bounded at F by the losses (1.30). Apply [8, Prop. 4.6] and [8, (4.33)]. Discarded outer-norm
coefficient 1 - 4 rho_* |b_h| = 2497786653900013/2500000000000000 > 0. "No commutation of a face operator with
P_O is used."

[note: (2.29) p. 18 states L^+ >= d_0 beta_old + (1 - b_h) beta_new + E_O, so L^+ is exactly what replaces those
three terms in (1.33).]

---------------------------------------------------------------------------------------------------------------
## 2. Sec. 1.5: a positive cover of the support failures (pp. 9-11)

Suppress the row index in A_t, C_t, L_t for a retained order-three row. Allocation functions (p. 9):
      \phi_D(p) := min(3p/2, L),     \phi_E(p) := 3p - \phi_D(p),     L := 23C/40.                          (1.34)

**Lemma 1.4.** After the bounds for the largest fragment and opposite root have been imposed, every retained
order-three failure is a nonlargest H_{5/2} failure at the corresponding threshold.
Proof (p. 9): Lemma 1.1 gives max(A,C) <= 7L/3. Below 2L/3 both allocation functions equal 3p/2. Above 2L/3 a
nonlargest witness has inclusive prefix >= 2p; the two nonlinear obstructions and the balanced obstruction are
>= 2p + L, 5p - L, 7p/2, all > 7L/3. So the predicates fail together. The imposed caps exclude a largest witness.

"The rank-one comparisons of Lemma 1.1 and Lemma 1.4 reduce all failures to"
      O_2,  O_{5/2},  I_2^old,  I_{5/2}^old,  I_2^new,  I_{5/2}^new.                                       (1.35)
Activation, threshold, cap, radial interval, splitting point and every originating source row: (1.22)-(1.24).
"For a group G write its parameters as (d, m, xi, U, z, p_G)."

### 2.1 Witness intervals (1.5.1, p. 9)
Groups (G_1..G_6) in the order of (1.35); in each list xi = xi_G, p = p_G. Put
      a_j := (6/5)^j / 20   (0 <= j <= 9),   and || concatenates lists.
Complete low-bin boundaries:
      U_1 := (xi, 3xi/2, a_0) || (a_j)_{j=4}^{8} || ((a_8 + a_9)/2, a_9, p),
      U_2 := (2^j xi)_{j=0}^{8} || (1/100, 3/200, 9/400, 27/800) || (a_j)_{j=0}^{7} || ((a_7 + p)/2, p),
      U_3 := (xi, a_0, a_4, a_6, a_8, p),
      U_4 := (xi, 2xi, 1/100, 27/800, a_3, a_5, a_6, p),
      U_5 := (xi, a_1, a_4, a_5, a_7, a_8, p),
      U_6 := (2^j xi)_{j in {0,1,4,6,8}} || (9/400, a_1, a_3, a_5, a_6, a_7, p).
"Consecutive endpoints u_{j-1}, u_j define L_j, with slope \lceil 7/u_j \rceil, except for slope 120 at (G_1, L_3)
and slope \lceil 9/u_j \rceil throughout G_6."
[note: interval counts 10, 22, 5, 7, 6, 11 = 61 low intervals (Lemma 1.6); 10 and 22 match L1..L10 of Table 2.1
and L1..L22 of Table 2.2. Bins are (u_{j-1}, u_j]. "slope" = theta in (1.37).]

Rank-two bins: q_0 := U_G/(m_G + 1). Consecutive t_{j-1}, t_j define (q_0 + t_{j-1}(z_G - q_0), q_0 + t_j(z_G - q_0)]:
      T_1 := (j/6)_{j=0}^{6},                 T_2 := (j/16)_{j=0}^{8} || (5/8, 3/4, 7/8, 1),
      T_3 := (0, 1),                          T_4 := (0, 1/2, 1),
      T_5 := (0, 1/6, 1/2, 2/3, 1),           T_6 := (0, 1/8, 3/8, 1/2, 3/4, 1).
"Each group also has its single third-factorial component above p_G."
[note: 6+12+1+2+4+5 = 30 rank-two bins; 61 + 30 + 6 = 97 components; outer 17 + 35 = 52, inner 45.]

### 2.2 Low witnesses (1.5.2, pp. 9-10)
"A low witness in row t implies both s > c_t and s > V_t - (mu_t - 1)u, proving (1.26)."
If a witness belongs to a low bin (\ell, u], then
      L_{<=\ell} < s + (m - 1)u - U.                                                                        (1.36)
Consequently, for the positive rational slope theta, its event is covered by the positive Palm sum
      \sum_{p in X \cap (\ell,u]} exp( \theta { s + (m-1)u - U - L_{<=\ell} } ).                           (1.37)
"Lemma 2.3 supplies every small-fragment completion and every possible number of remaining large fragments."
[reading: L_{<=\ell} is not defined in Sec. 1.5; I read it as the total size of all fragments <= \ell (over all
coordinates of the root), s the root total. This is the only reading consistent with Lemma 2.3, where small
fragments (<= \ell) carry the tilt e^{-theta t} and fragments in (\ell, z] are untilted, and with (1.38), which
supplies e^{theta s}.]

**Lemma 1.5** (Full-radius factorization), p. 10. If u^+ = h \lceil u/h \rceil, the residual radial factor is
      W_r = exp( \theta { rh - U + (m - 1)u^+ + dh } ).                                                     (1.38)
For an erased coordinate of index v, use W_{r+v} before summing over that coordinate.
Proof: \prod_i e^{\theta(j_i h - U/d)} = e^{\theta(rh - U)} plus the full-cell correction (the "+dh": each of d
coordinates has total < (j_i+1)h). On an erased-coordinate term the full index is r + v, giving exactly (2.20).

**Lemma 1.6** (Containment of the low-witness intervals), p. 10. The radial restrictions in (1.26), applied to the
displayed 61 low intervals, retain every source failure assigned to those intervals.
Proof (p. 10, substance): for an eligible originating row of effective order mu, a witness below u implies s > c_t
and s > V_t - (mu - 1)u; minimum over all eligible rows (incl. absorbed order-two rows) gives (1.26); the outward
full-cell test retains every cell meeting the event. Direct check stated: "Of the 40 order-5/2 low intervals, the
first 11, 2, 5 in the outer, old-inner, and new-inner groups, respectively, end below every absorbed order-two
activation. On the remaining 11, 5, 6 intervals the order-three minimum is the group's original lower radial
boundary." Each of the 61 intervals is nonempty on this grid.
[note: 11+11 = 22 (O_{5/2}), 2+5 = 7 (I_{5/2}^old), 5+6 = 11 (I_{5/2}^new): consistent with U_2, U_4, U_6.]

### 2.3 Rank-two witnesses (1.5.3, p. 10)
"If the second-largest witness exceeds p_G, let q be the largest fragment. A necessary rank-two condition is"
      q > U/(m+1),     p > d(q) := max{ p_G, xi, (U - q)/m },     q <= z.                                   (1.39)
The six groups have max(p_G, xi) <= U/(m+1), so d(q) < q on this range. Omitting p_G, xi from the maximum enlarges
the event and gives the positive kernels of Lemma 2.4. At fixed coordinate totals write A_i := D_q(t_i),
B_i := D_{d(q)}(t_i), shifting t_j to t_j - q when coordinate j contains the largest fragment, where
D_c(t) := \rho_D(t/c) for t >= 0. Terms with t_j < q vanish. The one-largest Palm density is
      \sum_j \int ( A_j \prod_{i != j} A_i - B_j \prod_{i != j} B_i ) dq/q.                                (1.40)
All its differences are nonnegative. A positive upper bound for the integrand belonging to j:
      (A_j - B_j) \prod_{i != j} A_i + B_j \sum_{i != j} (A_i - B_i) \prod_{v != i,j} A_v.                  (1.41)
Let P = ordinary measure, A = measure for the coordinate containing the largest fragment, B = that for a secondary
fragment in a different coordinate, C = that for both fragments in the same coordinate. Put
      Q := P + xA + yB + xyC      in R_{>=0}[x,y]/(x^2, y^2).                                               (1.42)
The two marks occupy one coordinate or two ordered distinct coordinates, so
      [xy] Q^d = d P^{d-1} C + d(d-1) P^{d-2} A B.                                                          (1.43)
On separating an erased coordinate, the four placements are
      C_e P_r + P_e (xy)_r + A_e y_r + B_e x_r.                                                             (1.44)
[reading: subscripts e = erased coordinate, r = the product over the remaining (retained) coordinates; (xy)_r,
y_r, x_r = the corresponding coefficients of Q^{d} over retained coordinates.]

**Lemma 1.7** (Feasible logarithmic mass), p. 11. In a largest-fragment interval (q_-, q_+], put
L := log(q_+/q_-) and
      \mathscr{L}(v) := 0              if v <= q_-,
                        log(v/q_-)     if q_- < v < q_+,                                                    (1.45)
                        L              if v >= q_+.
For a physical cell with upper endpoint t^+, its largest-fragment coordinate and same-coordinate measures may be
multiplied, respectively, by outward upper bounds for
      \mathscr{L}(t^+) / L ,      \mathscr{L}( (m t^+ - U)/(m - 1) ) / L.                                   (1.46)
The second fraction may also be capped by the first. Charge the common factor L once.
Proof: a largest fragment needs q < t^+; same coordinate also needs t^+ > q + (U-q)/m, i.e. q < (mt^+ - U)/(m-1).
Integrate dq/q over the feasible parts. Each monomial of (1.43) has exactly one factor carrying the largest
fragment, so its fraction is applied once. Use a positive lower bound for L in the denominator.

### 2.4 Higher ranks (1.5.4, p. 11)
Every remaining witness above p_G has at least three fragments above p_G, hence
1_{N_{>p_G} >= 3} <= binom(N_{>p_G}, 3). The identity
      binom(\sum_i N_i, 3) = \sum_i binom(N_i, 3) + \sum_{i != j} binom(N_i, 2) N_j + \sum_{i<j<\ell} N_i N_j N_\ell   (1.47)
is realized by the factorial kernels in (2.8), with the factorial divisor included once. Low and rank-two
partitions and one factorial term per group cover every offending rank; all lists increase strictly between the
required endpoints; together with (1.26) and Lemma 1.6 no witness interval is omitted, including events absorbed
from lower-order rows.

---------------------------------------------------------------------------------------------------------------
## 3. Sec. 2.1: coordinate kernels (pp. 11-14)

Setup (p. 11): C_j = [jh,(j+1)h), g_j := g((j + 1/2)h), Z_0 := 1, Z_2 := Z := \sum_{j<n} g_j^2, and
      w_j^{(e)} := g_j^e / Z_e,   e in {0, 2}.
"All polynomials here are reduced modulo X^N; only j < n enter the final arrays. Arrows denote outward dyadic
extraction at 160-bit real-ball precision. For a source upper bound, its positive coordinate measures are fixed
before a signed square is expanded; the cap forms retain two-sided enclosures. Indeed 0 <= mu <= mu^+ implies
\int |P|^2 d\mu <= \int |P|^2 d\mu^+, even when P has signed coefficients."
Lemma 2.1 (p. 11-12): log via 0 <= log y - 2\sum_{r=0}^{M-1} v^{2r+1}/(2r+1) <= 2v^{2M+1}/((2M+1)(1-v^2)),
v = (y-1)/(y+1) <= 1/3, 1 <= y <= 2; exp via 0 <= e^v - \sum_{r=0}^{M} v^r/r! <= v^{M+1}/((M+1)!{1 - v/(M+2)}),
v = |x|/2^b in [0,1/2], square back, invert if x<0; refine to relative width <= 2^{-164}.

Lemma 2.2 (p. 12; already in forms note, re-read from the image to settle the bar placement): for c = Mh,
\underline{d}_j = \overline{d}_j = 1 for 0 <= j <= M, and for j >= M
      \underline{d}_{j+1} := max{ 0, \downarrow( \underline{d}_j - \overline{d}_{j-M}/(2j) - \overline{d}_{j+1-M}/(2(j+1)) ) },
      \overline{d}_{j+1}  := min{ 1, \uparrow( \overline{d}_j - \underline{d}_{j-M}/(2j) - \underline{d}_{j+1-M}/(2(j+1)) + 1/(2M^3) ) }.   (2.1)
Then \underline{d}_j <= D_c(jh) <= \overline{d}_j (point values at grid points). Cell masses: A_j(c) = h for j < M;
for j >= M, max{0, \downarrow(h/2 (\underline{d}_j + \underline{d}_{j+1}) - h^3/(12c^2))} <= A_j(c)
<= \uparrow(h/2 (\overline{d}_j + \overline{d}_{j+1})) (2.2), intersectable with [0,h]. Unaligned cap: c^- := h\lfloor c/h \rfloor
below, c^+ := h\lceil c/h \rceil above (D_c increases with c). Cap arrays enclose w_j^{(e)} A_j(c)/h; the erased
marginal uses g_j A_j(c)/h.

### 3.1 Renewal majorant (p. 12)
"For small caps use the positive renewal majorant"
      R_j := 1   (j <= M),      R_j := (1/j) \sum_{a=j-M}^{j-1} R_a   (j > M),      M >= 2.                  (2.3)
"The identity u\rho_D(u) = \int_{max(0,u-1)}^{u} \rho_D(v) dv and a left Riemann sum give R_j >= \rho_D(j/M). The exact
rational R_j is carried in a two-sided interval: initialize the sliding sum to [M, M], divide outwards by j, then add
the new interval and subtract the departing one. Reject a nonpositive lower endpoint. Only once its upper bound is
at most a lower bound for 10^{-40} may the majorant be set to the constant 10^{-40} thereafter; monotonicity
justifies this tail. For low kernels choose the delay recurrence when M >= 64 and its acceptance tests pass, and
otherwise the renewal recurrence. Write d^\star_j(Mh) for the chosen exact majorant and I_j(Mh) for its enclosure.
In the delay branch these are \overline{d}_j and its singleton interval; in the renewal branch the full two-sided
intervals must remain through the products below."
[note: d^\star_j majorizes the POINT value D_{Mh}(jh) = rho_D(j/M), not the cell mass.]

### 3.2 Low-bin kernels (pp. 12-13)
For a low bin (\ell_0, u_0] and hard cap z_0, put L := \lfloor \ell_0/h \rfloor, H := \lceil u_0/h \rceil,
K := \lceil z_0/h \rceil, (\ell, u, z) := (Lh, Hh, Kh); the data satisfy 2 <= L < H <= K <= N. For its rational
slope theta > 0 define
      Q(X) := \sum_{a=L}^{K-1} X^a / a,     M(X) := \sum_{a=L}^{H-1} X^a / a,
      D_\theta(X) := h \sum_{j<N} d^\star_j(\ell) e^{-\theta j h} X^j.                                      (2.4)
"The enclosure of D_theta uses the complete intervals I_j(\ell), not their upper endpoints."
Eulerian polynomials: E_r(X) := (r!)^{-1} \sum_{a=0}^{r-1} Eu(r,a) X^a and R_r(X) := 1 + X + ... + X^{r-1}, where
      Eu(1,0) = 1,     Eu(r,a) = (a+1) Eu(r-1,a) + (r-a) Eu(r-1,a-1),                                       (2.5)
out-of-range indices zero. Put q_r := Q^r / r! and J := min(32, \lfloor (N-1)/L \rfloor). For e = 0, 1:
      T_e := \sum_{r>=0} q_r R_{r+e+1} = ( exp Q - X^{e+1} exp(XQ) ) / (1 - X)     (mod X^N),
      \hat{T}_e := \sum_{r=0}^{J} q_r E_{r+e+1} + \uparrow( T_e - \sum_{r=0}^{J} q_r R_{r+e+1} ).
[note: in the closed form exp(XQ) means exp(X*Q(X)), i.e. sum_r q_r X^r; checked against
R_{r+e+1} = (1 - X^{r+e+1})/(1-X).]
"The positive omitted sum is enclosed by subtracting the enclosed prefix from an upper enclosure of T_e; a negative
upper endpoint is rejected. It vanishes if J = \lfloor (N-1)/L \rfloor." Physical-mass polynomials:
      \mathsf{B}_\theta := D_\theta \hat{T}_0,                                                              (2.6)
      \mathsf{M}_\theta := D_\theta M \hat{T}_1.                                                            (2.7)

**Lemma 2.3** (Eulerian cell kernels), p. 13. The coefficients of B_theta, M_theta majorize, respectively, the
physical-cell masses of
      (e^{-\theta t} D_\ell(t) dt) * exp_*( 1_{(\ell,z]}(v) dv/v ),
      1_{(\ell,u]}(v) dv/v * (e^{-\theta t} D_\ell(t) dt) * exp_*( 1_{(\ell,z]}(v) dv/v ).
No small-fragment mass or high-fragment count is omitted.
Proof (p. 13): [7, Thm. 5.2] gives on totals \bar\nu_z = \bar\nu_\ell * exp_*(1_{(\ell,z]} dv/v) (the void factor
\ell/z cancels the normalization change); reduced Mecke marking [7, Thm. 4.5] adds the designated factor. On C_a,
dv/v <= density 1/(ah), mass 1/a; on C_j the tilted low density <= d^\star_j(\ell) e^{-\theta j h}. For r uniform
fractional cell coordinates, carry mass (1/r!) \sum_{b=0}^{a+1} (-1)^b binom(r+1,b) (a+1-b)^r = [X^a] E_r. Carry is
E_{r+1}, or E_{r+2} with a designated fragment; 0 <= E_r <= R_r coefficientwise bounds the omitted terms; terms with
rL >= N vanish.

"Fix the upward endpoints of w_j^{(e)} [X^j] B_theta / h and w_j^{(e)} [X^j] M_theta / h as the ordinary and
designated arrays. Apply (1.38) at the full index before erasure."

### 3.3 Third-factorial kernels (p. 13)
For the third-factorial bound above p_G, take L := \lfloor p_G/h \rfloor, K := \lceil z_0/h \rceil, form Q as above
and set D_0 := h \sum_{j<N} \overline{d}_j(Lh) X^j. For a = 0, 1, 2, 3,
      \mathcal{F}_a := D_0 (Q^a / a!) \sum_{b=0}^{\lfloor (N-1-aL)/L \rfloor} (Q^b / b!) E_{a+b+1}     (mod X^N),   (2.8)
empty sums zero. The fixed array is \uparrow( w_j^{(e)} [X^j] \mathcal{F}_a / h ). Reduced factorial Palm marking
and the same carry calculation show it bounds the cell measure weighted by binom(N_{>p_G}, a). The factor 1/a! is
charged once. Extracting total degree three includes every higher rank and all placements.
[reading: here D_0 uses \overline{d}_j (delay recurrence), not d^\star_j; no tilt (theta = 0). Whether the renewal
branch may be used when L < 64 is not said for D_0.]

### 3.4 Rank-two (largest-fragment) arrays (p. 14, image checked at 220 dpi)
For a largest-fragment bin (a, b], assume U/(m+1) <= a < b <= z_0 < U, m in {2, 5/2}. Drop the splitting and
activation cutoffs, and put
      r(q) := (U - q)/m <= q,     r_- := (U - b)/m,     r_+ := (U - a)/m,
      s_j^- := max(0, j - \lceil b/h \rceil),     s_j^+ := max(0, j + 1 - \lfloor a/h \rfloor).
Let t_j^+ := (j+1)h, \hat{w}_j^{(e)} := \uparrow w_j^{(e)}, and \beta_j = 0 for jh < b,
\beta_j = \underline{d}_{s_j^+}(r_-^-) otherwise. "With upward caps in upper grids and downward caps in lower grids, set"
      \mathsf{P}_j^{(e)} := \uparrow( \hat{w}_j^{(e)} \overline{d}_j(b^+) ),
      \mathsf{A}_j^{(e)} := 1_{t_j^+ > a} \uparrow( \hat{w}_j^{(e)} \overline{d}_{s_j^-}(r_+^+) ),
      \mathsf{B}_j^{(e)} := \uparrow( \hat{w}_j^{(e)} [ \overline{d}_j(b^+) - \underline{d}_{j+1}(r_-^-) ]_+ ),         (2.9)
      \mathsf{C}_j^{(e)} := 1_{t_j^+ > a + r_+} \uparrow( \hat{w}_j^{(e)} [ \overline{d}_{s_j^-}(b^+) - \beta_j ]_+ ).
"Here [v]_+ := max(v,0), and differences are enclosed upward before clipping."
[reading: b^+, r_+^+ = caps rounded up to the grid (h\lceil.\rceil), r_-^- = rounded down (h\lfloor.\rfloor), per the
c^+/c^- rule of p. 12; \overline{d}_j(c), \underline{d}_j(c) = the Lemma 2.2 enclosures of the point value D_c(jh)
at cap c. NOTE the clash with Sec. 2.2's d_c(j) := A_j(c)/h (cell average): (2.9) uses the subscripted point
enclosures. Note also the asymmetry: P and A use index j (left endpoint), B's subtracted term uses j+1 (right
endpoint), beta_j uses s_j^+.]

**Lemma 2.4** (Whole-bin Palm envelopes), p. 14. These arrays bound the ordinary, largest-fragment coordinate,
distinct-secondary, and same-coordinate coordinates, respectively. Put \Lambda := log(b/a), and let
\lambda(v) := min{1, max{0, log(v/a)/\Lambda}} for v > 0, \lambda(v) := 0 for v <= 0. Multiply the arrays for the
largest fragment and for coincident marks by outward upper bounds on the respective fractions
      \lambda(t_j^+),        \lambda( min{ t_j^+, (m t_j^+ - U)/(m-1) } ),
respectively. The external factor \Lambda is charged once.
Proof (p. 14): off the largest-fragment coordinate A = D_q(t), B = D_{r(q)}(t); on it A = D_q(t-q), B = D_{r(q)}(t-q),
t >= q. Differences positive since r(q) <= q; product difference splits as in (1.41). Monotonicity in cap and
nonnegative total, r_- <= r(q) <= r_+ and t - q >= max(0, jh - b) give the upper endpoints. For jh >= b also
t - q <= t_j^+ - a, giving the lower endpoint in the same-coordinate difference. A largest-fragment cell is empty if
t_j^+ <= a; a same-coordinate cell if t_j^+ <= a + r_+ (q + r(q) increases). Fractions as in Lemma 1.7; positive
lower bound for Lambda in the denominator, clip at one, second fraction may be bounded by the first.

---------------------------------------------------------------------------------------------------------------
## 4. Sec. 2.2 from (2.16): the loss forms (pp. 15-16)

Background (2.10)-(2.15) (P_e[K], M_{d,sigma}[K], Q_eta, I_H, v_{s,tau}, v^(l), S(v,M;A), J_0/J_+/J_t): see
notes/sources-186-forms.md Sec. 3. Note t_j := (j+1/2)h, radial polynomials mod X^n.

"For a source component, take the ordinary and marked arrays from Sec. 2.1. Use profile power two on retained
coordinates and zero on an additional erased coordinate. The marking rings and extracted coefficients are"
      component | coordinate polynomial                          | coefficient
      L_j       | P + yD               (mod y^2)                 | [y]
      P_j       | P + xA + yB + xyC    (mod x^2, y^2)            | [xy]                                    (2.16)
      H         | F_0 + yF_1 + y^2 F_2 + y^3 F_3   (mod y^4)     | [y^3]
"The entries denote coordinate arrays. Write [*] for the selected coefficient, [X^r *] := [X^r][*], K^{(2)}, K^{(0)}
for the profile choices, and M_{d,eta} := M_{d,eta}[K^{(2)}]. All coordinate placements, including coincident
marks, remain. The external factor is Lambda := log(q_+/q_-) for a rank-two bin and Lambda := 1 otherwise."
[note: L_j = low bin j (P = ordinary array from B_theta, D = designated array from M_theta); P_j = rank-two bin j
(arrays (2.9)); H = third-factorial component (arrays from F_0..F_3). K^{(e)} = the array built with w^{(e)}.]

p. 16: "Let chi_G indicate the full-cell intervals in (1.25), clipped by (1.26) for a low bin. Its radial weight is
      W(r) := exp( \theta { rh - U_G + (m_G - 1)u^+ + d_G h } ),   u^+ := h\lceil u/h \rceil;
otherwise put W := 1. Only indices with chi_G = 1 are evaluated, and their exponent is less than 700. For an outer
low component, select the dyadic upper array once and use it in both source forms. For an inner low component,
keep the same two-sided enclosure of the exact weight in every signed term. The root-square bound is"
      R_G := 40 \Lambda \sum_{r<n} \chi_G(r) W(r) \sum_\eta Q_\eta(r) [X^r *] M_{40,\eta}.                   (2.17)
"The factor 40 bounds the sum of the absolute face multipliers, each at most one. Using the largest group cap and
discarding further outer cap restrictions only increases this integral of a square."

For (u, v] \subseteq (0, c_1]:
      \mathcal{P}(u,v) := { l in {1,2,3} : max(u, c_{l+1}) < min(v, c_l) }.                                (2.18)
(c_1 > c_2 > c_3 the outer caps 68225h, 49152h, 46580h; c_4 := 0.) "The actual signed marginal is one of these
prefixes. Use \mathcal{P} := \mathcal{P}(q_-, q_+) for an inner rank-two component and \mathcal{P} := \mathcal{P}(0, z_G)
otherwise. The sum of their complete squares therefore gives"
      \beta_G := (40 h \Lambda / Z) \sum_{l in \mathcal{P}} \mathcal{S}( v^{(l)}, ([X^r *] M_{39,\eta})_{\eta,r} ; \chi_G W )   (2.19)
as a positive inner bound. For an outer component, form in the marking ring
      C(r) := \sum_{a=0}^{n-1-r} \chi_G(r+a) W(r+a) K_a^{(0)},      H_\eta(r) := [*]( C(r) [X^r] M_{39,\eta} ).   (2.20)
"The event and radial weight remain at the full index r + a; the erased coordinate carries no extra profile factor.
This product contains all four rank-two placements and all factorial degrees of the erased coordinate." With the
radial upper bound
      w(r) := 1                          if (r+39)h <= T_0,
              max{|a_h + b_h|, |b_h|}    if T_0 < (r+39)h <= T_1,
              |b_h|                      if (r+39)h > T_1,
the second outer form is
      V_G := (40 h^2 \Lambda / Z) \sum_{l in \mathcal{P}(0, z_G)} \mathcal{S}( v^{(l)}, H ; w ).          (2.21)
"The factors 40h/Z and 40h^2/Z result from dividing the face square, and its additional erased-coordinate integral,
by the same (hZ)^{40}. There is no conditional-cap normalization."
[reading: in (2.20) K_a^{(0)} is the erased coordinate's marked array (in the marking ring of (2.16)) with profile
power 0, and C(r)[X^r]M_{39,eta} is a product in the marking ring (M_{39,eta} built from the 39 retained K^{(2)}
arrays) of which [*] is taken -- this realizes (1.44). The sum over a is a reversed correlation, cf. (2.24).
M_{39,eta} is then contracted against the cap affine rows v^{(l)} by (2.14) with mask w.]

Use in Sec. 2.4 (p. 18, for orientation; numbers in the JSON): outer component loss E_j := c_j R_j + V_j/c_j (2.27)
with R_j, V_j from (2.17), (2.21); inner components use (2.19) times d_0 (old) or 1 - b_h (new) (2.28);
L^+ := sum of the 97 component bounds >= d_0 beta_old + (1 - b_h) beta_new + E_O (2.29); I_H^- := 23685317816e-24;
table integers: c = q/10^6, R/I_H^- <= A/10^18, V/I_H^- <= B/10^18, cA/10^18 + B/(10^18 c) <= E/10^12 (2.30);
inner: beta_G/I_H^- <= A/10^18, kappa_G A/10^18 <= E/10^12 (2.31).

---------------------------------------------------------------------------------------------------------------
## 5. Sec. 2.3: interval evaluation (pp. 16-17), briefly

- Positive polynomials at binary scale Q = 2^b: integer polynomials A^-, A^+ with 0 <= A^-/Q <= A <= A^+/Q
  coefficientwise; truncated products
      (AB)^- = \lfloor A^- B^- / Q \rfloor,     (AB)^+ = \lceil A^+ B^+ / Q \rceil                          (2.22)
  (exact integer polynomial products; coefficientwise division). Coefficientwise upper division, deg P < r:
      \lceil P/Q \rceil = \lfloor ( P + (Q-1)(1 + X + ... + X^{r-1}) ) / Q \rfloor.                          (2.23)
  Exact zero prefixes: if A = X^{v_A}\tilde A, B = X^{v_B}\tilde B, v_A + v_B < n, apply (2.22) to \tilde A\tilde B
  mod X^{n - v_A - v_B} and restore X^{v_A+v_B}; otherwise the product mod X^n is zero.
- Reversed positive correlations:
      \sum_{r=j}^{n-1} I_r K_{r-j} = [X^{n-1-j}] ( \sum_{r=0}^{n-1} I_{n-1-r} X^r ) K(X).                   (2.24)
  Cap moments b = 224, source moments b = 192; positive coordinate endpoints fixed before any signed expansion.
- 2.3.1 Signed shell sums: in a cap layer the signed sum of allowed outer-shell marginals is squared before
  integration; for a source bound, the actual marginal is one of the finitely many sums in (2.18) and the sum of
  their complete squares is a valid upper bound. Signed shell coefficients are never replaced by absolute values.
- 2.3.2 Final reductions: binary64 (53-bit, round-to-nearest-even, gradual underflow to 2^{-1074}, no overflow),
  checked in the producing process. Dyadic endpoints converted outwards by one predecessor/successor after binary
  scaling; an integer too large is first replaced by
      v_- := \lfloor v/2^r \rfloor,    v_+ := \lceil v/2^r \rceil                                           (2.25)
  then scaled by 2^{r-b}. Enclose all four endpoint products and take the hull. With u := 2^{-53},
  \gamma_r := ru/(1-ru), s = fl(\sum_{j=1}^r x_j), t = fl(\sum_{j=1}^r |x_j|): lower endpoint = binary64 predecessor
  of fl(s - fl(\gamma_r t)), upper = successor of fl(s + fl(\gamma_r t)). Required slack
      (1-u)^2 (1 - \gamma_{r-1}) \gamma_r - \gamma_{r-1} > 0     (1 <= r <= 98264),                          (2.26)
  numerator after removing u/((1-ru)(1-(r-1)u)): 1 - (r^2+r)u + (4r^2-3r)u^2 - (2r^2-2r)u^3; for M = 98264 at least
  1 - (M^2+M)u - 3Mu^2 - 2M^2u^3 > 0.
- Production (p. 17): coordinate enclosures at 160 bits (Arb real balls), then (2.22) with 224 fractional bits for
  cap moments and 192 for source moments. Source coordinate upper endpoints fixed only after kernel constructions;
  signed marginal rows by outward real-ball arithmetic, shells summed before squaring. Reject nonfinite or reversed
  endpoints, negative positive-upper bounds, any failure of the machine hypotheses. Apply the exact Young parameters;
  round raw bounds upwards to 10^{-18} and component bounds to 10^{-12}. Index bounded by N, factorial degree by 3,
  every formal exponential truncated.

---------------------------------------------------------------------------------------------------------------
## 6. Precision / production remarks (end of Sec. 2.5, p. 21; also p. 17 and App. A, p. 23)

- p. 17: "The real-ball calculations use precision 160 and the published Arb method [4]. The recorded production
  used python-flint 0.9.0 and FLINT 3.6.0 with the published signed-FFT conversion correction [3, 6, 5]; the inputs
  and directed outputs are included in [2]."
- p. 21: "The data archive [2] fixes the exact trial, masks, complete schedule, source code, rational endpoint
  records, and corrected runtime provenance. Its recorded production used 160-bit Arb arithmetic through
  python-flint, 224-bit cap convolutions, and 192-bit source convolutions, with the FLINT signed-FFT conversion
  correction [4, 6, 3, 5]. The independent exact replay checks identities, coverage, and rational arithmetic from
  those records; it does not recompute their integrals. A full run of the accompanying script reproduces the
  complete certificate from the exact inputs."
- Remark 2.7 (pp. 21-22): Lean input = 149 upper inequalities for the physical source integrals of Tables 2.1-2.6
  (two per each of 52 outer rows, one per each of 45 inner rows) plus the three cap bounds (2.33). "The physical
  source integrals are the quantities majorized by the computational forms (2.17), (2.19) and (2.21); these are not
  identified by definition." Lean does not yet verify the finite contractions or the Arb/FLINT production.
- References: [2] "Exact input data, production records and verification scripts for the 77-coefficient numerical
  certificate, accompanying data archive, 2026" (no URL given). [3] FLINT 3.6.0. [4] Johansson, Arb, IEEE Trans.
  Comput. 66 (2017). [5] FLINT commit 7ad753d51c82fdec115cb179b41d0e581f1cb0ec, PR 2790 ("Fix fft conversion bug
  causing rare incorrect results in fmpz_poly_mul_SS"). [6] python-flint 0.9.0, commit
  572c8a213a88c0f92feb1bdb938ce4622f4517fa. App. A: script prime_gap_186_certificate.py (Python 3.12, NumPy,
  python-flint linked to FLINT containing [5]; `--workers 4`) and PrimeGaps186.lean.

---------------------------------------------------------------------------------------------------------------
## 7. What an independent re-evaluation of L^+ needs (my summary, not from [14])

In order:
1. Grid and trial data (N, h, n, g_j, Z, w^{(e)}, c_{sigma,d}, outer caps c_1..c_3, masks (1.5)) -- already in
   forms note / support code. Group parameters (d, m, xi, U, z, p_G, b_G, t_G) and all source rows (c_t, V_t, xi_t,
   order) -- in code/oai186_support_data.py.
2. Bin schedule: the 61 low bins from U_1..U_6 with slopes theta, the 30 rank-two bins from T_1..T_6, 6 factorial
   components; radial masks chi_G from (1.25) and, for low bins, c_G(u) from (1.26) (needs every eligible row incl.
   absorbed order-two rows); weights W(r) (1.38).
3. One-coordinate kernels: Dickman point enclosures (2.1) at caps \ell, p_G-floor, b^+, r_+^+, r_-^-; renewal
   majorant (2.3) when M < 64; low-bin arrays from B_theta, M_theta (2.4)-(2.7) (Eulerian E_r, hat T_e with J <= 32);
   factorial arrays F_0..F_3 (2.8); rank-two arrays P, A, B, C (2.9) with lambda-fractions of Lemma 2.4; for e = 2
   (retained) and e = 0 (erased).
4. Marked moment rows M_{40,eta}, M_{39,eta} via (2.10) in the marking rings of (2.16), mod X^n; extract [*].
5. Cap affine rows v^{(l)} (2.13) (shared with J), P-sets (2.18), w(r).
6. R_G (2.17), V_G via C(r), H_eta (2.20)-(2.21) for the 52 outer components; beta_G (2.19) for the 45 inner ones.
7. Divide by I_H^-, compare with Table A/B columns; recombine with the table's c = q/10^6 (2.27)-(2.31) and sum to
   L^+/I_H^- <= 696075110/10^12.

Underspecified / ambiguous points:
- L_{<=\ell} in (1.36)-(1.37) is not defined in Sec. 1.5 (read as total of fragments <= \ell); likewise the meaning
  of H_2 / H_{5/2} (read as phi(p) = (m-1)p) must be taken from Sec. 1.1/the main paper [8].
- Notation clash: d_c(j) := A_j(c)/h (cell average, Sec. 2.2) vs \overline{d}_j(c) (point enclosure, (2.1), (2.9)).
  Which one the low-bin and rank-two arrays mean is decided only by the bars; the cap-rounding rule
  ("upward caps in upper grids, downward in lower") is stated in one sentence.
- Whether the slope theta for "slope \lceil 7/u_j \rceil" is in the same length units as h (u_j are absolute
  fragment sizes, from ~xi_G up to p_G, so theta is large for the first bins): not stated, but forced by W(r)'s
  exponent theta*(rh - U ...).
- Exactly which source rows enter (1.26) for each low bin ("eligible"/"absorbed" rows) needs Sec. 1.3 data; only
  the summary counts of Lemma 1.6 are given as a check.
- The precise structure of the [*]-extraction in (2.20) (product of the erased marked array with the 39-coordinate
  marked moments, realizing (1.44)), and whether K^{(0)} for an outer low component is the designated or ordinary
  array per monomial, is implied rather than written out.
- D_0 in (2.8) uses \overline{d}_j(Lh) with no renewal fallback stated for small L.
- How the inner beta_G for low and factorial components picks P(0, z_G) vs P(q_-, q_+) is stated; but the mask
  chi_G for an inner group is in terms of the base/enlarged rows of (1.5) ("appropriate rows") -- which rows, and
  whether the face mask H_0 vs H_1 difference is applied, is not spelled out.
- Archive [2] (records, schedule, code) has no URL in the PDF; Tables 2.1-2.6 give only rounded integers, so a
  re-evaluation can be compared only to those upward-rounded bounds.
