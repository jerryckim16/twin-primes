# Audit: code/oai186_loss_inner.py, code/oai186_loss_outer.py vs short_gaps_numerics.pdf

Method: read both programs (plus `oai186_check2.py:marginals`, `oai186_support_data.py`) against `pdftotext -layout`
of the PDF. Pages 9, 12-14 and 16 were also checked as rendered images (bars, subscripts, lists). Did NOT read the
authors' script. Light checks only: both `--schedule` runs; an exact-rational toy check of the T_e identity and of the
Eulerian carry formula; a float simulation of the (2.1) acceptance test for every low bin (well under a minute).

## Discrepancies

None found. Items marked "source ambiguous" below give the reading the code takes and how much it could matter.

## Item by item

**(a) Clipping (1.26)** — agrees with the source. PDF p.5 (1.21), p.6 (1.22)-(1.26), p.9 Sec. 1.5.2, p.10 Lemma 1.6.
inner 88-102 (c_t=b_t, V_t=C_t), outer 79-92 (c_t=a_t, V_t=A_t); eligible = rows with xi_t < u (u = bin end u0, not u+);
absorbed rows = I_2^old rows o12-23, I_2^new rows n12-23, all O_2 rows o/n 0-23; mu = 5/2 only for r_t = 3; max with b_G;
lower index floor(c_G/h) - d_G + 1 (inner 388, outer 412). Reading: c_t = the radial core of the predicate in (1.21),
consistent with the shell boundaries (1.18) and U_G (1.23). By (1.17) every retained row is nonterminal, so V_t is
constant per order (S+e, S+e/2, T+e, T+e/2) and only the core reading affects the numbers. Schedule vs Lemma 1.6: the
order-5/2 counts are 22+7+11 = 40 and the low-bin total is 61. The "below every absorbed activation" counts are
11 / 2 / 5 (O5/2 L1-11, I5/2old L1-2, I5/2new L1-5). On the remaining 11 / 5 / 6 bins the order-three minimum equals b_G.
Every bin is nonempty. The rows per group are 17 / 35 / 7 / 10 / 11 / 17 = 97, the same as the tables.
Note: clipping is also active in O_2 L1 and L2 (lower index 94919 and 93607), not only in the 5/2 groups.
Cosmetic: inner line 101 (the `order3_min_is_bG` diagnostic) uses 3/2 for the order-two groups too. It is a
diagnostic only and does not affect the numbers.

**(b) Slopes** — agrees with the source (p.9). ceil(7/u_j) with u_j = upper endpoint; 120 at (G1 = O_2, L3) (outer 62, 99);
ceil(9/u_j) in all of G6 = I_{5/2}^new (inner 77, 110).

**(c) Lists U_1..U_6, T_1..T_6** — agrees with the source (p.9, checked on the image). outer 61, 66-68; inner 64-77;
q0 = U/(m+1) and bins (q0 + t_{j-1}(z-q0), q0 + t_j(z-q0)] (inner 113-117, outer 102-106). The (1.23)/(1.24) data
xi_G, U_G, b_G, t_G, z_G, p_G also agree, and p_G is re-derived by an assert.

**(d) Delay vs renewal** — agrees with the source (p.12). M = L = floor(l0/h), delay only if L >= 64 and accept() passes
(inner 233-259, 392-403; outer 234-256, 416-422). Recurrence (2.1): lower uses delayed uppers, upper uses delayed lowers
+ 1/(2M^3), with clipping to [0,1]. Tests: ordered, in [0,1], both sequences nonincreasing, on 0 <= j < N.
Renewal (2.3): R_j = 1 for j <= M, sliding sum initialised to M, and window bookkeeping are correct. Nonpositive
values are rejected. The constant 1e-40 is used only after the first R_j whose upper bound is <= the lower bound of 1e-40.
Source ambiguous (immaterial): the j-range of the test (N, n or R1+1) is not stated. My float simulation shows every
failing bin failing at j <= 85834, below every R1+1, and the accepted bins (L >= 11704) never failing, so the range
does not change any branch. The 1e-40 floor is optional in the source ("may"). It can only increase the kernel, and
its weight is below about 1e-40 of the main term. Predicted branches: delay only for L >= 11704 (I2old L4-5, I5/2old L6-7,
I2new L4-6, I5/2new L9-11, O2 L5-10, O5/2 L19-22); renewal elsewhere. This was a float simulation, not the code's own run.

**(e) hat T_e** — agrees with the source (p.13). Sum_r q_r R_{r+e+1} = (exp Q - X^{e+1} exp(XQ))/(1-X) holds, since
R_k = (1-X^k)/(1-X) and Sum q_r X^r = exp(XQ). An exact toy check (N=40, L=3, K=11) confirms it for e = 0, 1.
E_r = Eu(r, .)/r! (recursion (2.5) and the carry formula of Lemma 2.3 were checked for r <= 9). The prefix uses E and
the tail T_e - prefix uses R (inner 287-315, outer 280-308). J = min(32, floor((N-1)/L)). The tail is omitted only when
rmax = floor((nn-1)/L) <= J, where it vanishes mod X^nn. Truncating mod X^{R1+1} instead of X^N is harmless because
all series start at degree 0.

**(f) chi_G and W** — agrees with the source, with one point where the source is ambiguous. R0 = floor(b_G/h) - d + 1,
R1 = min(floor(t_G/h), last face row), with d_G = 39 inner (80) and 40 outer (71). W = exp(theta(rh - U_G + (m-1)h ceil(u0/h) + d_G h))
on the full index (inner 422-423, outer 438-439; inside C(r) at r+a). PDF p.6 (1.25), p.10 (1.38), p.16.
Source ambiguous: "intersect the appropriate rows of (1.5)". The code takes the union of the domain's face rows
(base for old, enlarged for new, outer for O). For O_2, I_2^old and I_2^new this keeps 39-40 indices of the next
(smaller-cap) row: R1 = 95638 / 87233 / 87288 versus row ends 95598 / 87194 / 87249. The kernels still use z_G,
which is an upper bound there. The I_2^old agreement to 5e-10 supports this reading for that group, and the same
code path serves O_2 and I_2^new. In the 5/2 groups the two readings coincide.

**(g) P-sets, w(r), prefactors** — agrees with the source (p.16). (2.18) gives {2,3} for O_2 and {3} for every other
group; the inner rank-two P(q-, q+) is also {3} because q+ <= z_G < c_3 (inner 205-208, outer 199-200).
w(r) is tested on (r+39)h against T0 and T1 (outer 202-204). Prefactors: beta = 40hLambda/Z (inner 377);
R = 40Lambda, V = 40h^2Lambda/Z (outer 397-398). Lambda = log(b/a) for rank-two components and 1 otherwise.

**(h) Rank-two (2.9), Lemma 2.4, factorial (2.8)** — agrees with the source (p.13-14, checked on the image).
The P, A, B, C arrays (inner 427-456, outer 444-477) have the right caps (b+ and r_+^+ rounded up, r_-^- rounded down),
the right indices (s_j^-, s_j^+, j+1 in B), the indicators t+ > a and t+ > a + r+, and beta_j = 0 for jh < b. The fractions
lambda(t+) and lambda(min{t+, (mt+ - U)/(m-1)}) are applied to A and C only. In (2.8) (inner 457-477, outer 478-499):
L = p_G/h, K = z_G/h, d-bar(Lh) with no tilt, b <= floor((N-1-aL)/L), E_{a+b+1}, 1/a! once, ring mod y^4, [y^3].
The h of D_theta and D_0 cancels against /h.

**(i) Outer V form** — agrees with the source (p.15-16). C(r) is the reversed correlation of chi_G W (full index,
zero below the clip) with K^(0) = the unweighted arrays (outer 375-380, 437, 471, 494). H uses
Sum_mono C[tgt - mono](r) [X^r][mono] M_39 over all ring monomials, with M_39 from the profile-two arrays and
falling(39, .) (outer 323-373). The pairing is with the w-weighted v^(l), summed over P(0, z_G). The R form uses
Q_eta with M_40. Marginals (2.13) (check2 240-266): chi_s(r+a), p_sigma(r+a), g_a d_cs(a) t_a^{e(A)}, labelled subsets.

## Not checked
- Arb numerical behaviour of the series exp at degree ~9.8e4.
- The ring/moment code beyond reading it (set partitions, falling factorials, prefix-cache deletion: a wrongly deleted
  prefix would only be recomputed).
- `oai186_tables_2_1_to_2_6.json` against the PDF tables.
- The ladder recurrence beyond its own asserts.
- The code's own branch outcomes. The predictions in (d) come from a float simulation.
- The other readings recorded in the notes: L_{<=l} as the total of fragments <= l, and H_2 / H_{5/2} as phi(p) = (m-1)p.
  Both are consistent with (1.36)-(1.38) and Lemma 2.3 but are not restated in Sec. 1.5.
