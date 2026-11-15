# Second independent evaluation of the outer loss bounds of [14], group O_{5/2}

Program: `code/oai186_loss_outer2.py` (per component: `python3 code/oai186_loss_outer2.py --comp P2 --out
code/cap6/loss_outer2/part_P2.json`; `--selftest` for the brute-force check of the moment algorithm, `--ihcheck` for the
end-to-end I_H check). Results: `code/cap6/loss_outer2/part_*.json`, logs `runs/loss_outer2_*.log`.
Source [14] = OpenAI, short_gaps_numerics.pdf (code/third_party/openai186/), read with `pdftotext -layout` and page
images (pp. 12-16 rendered and read for (2.1)-(2.21)).

**Status: Checked numerically (re-computation from the PDF's formulas), not a proof.** The quantities are the raw
bounds R_G (2.17) and V_G (2.21) of Table 2.2, reported as A = ceil(10^18 R/I_H^-), B = ceil(10^18 V/I_H^-),
I_H^- = 23685317816e-24.

## 1. Independence statement

- Not opened (before the numbers below were final): code/oai186_loss_outer.py, oai186_loss_inner.py,
  oai186_loss_I2old.py, oai186_check2.py, third_party/openai186/prime_gap_186_certificate.py, code/cap6/loss_* .
- Nothing is imported from the repository. Shared with other code: only the transcription notes
  (notes/sources-186-*.md, used as a reading aid and re-checked against the PDF), Table 1.1 coefficients (copied from
  the PDF text), and Table 2.2 (code/oai186_tables_2_1_to_2_6.json) for the comparison. code/oai186_support_data.py
  was only RUN as a cross-check: our own ladder (1.13)-(1.16) gives the same xi_G = xi_{n,38}, U_G = S + e/2 and
  b_G = a_{n,24} (exact rational equality). code/oai186_J.py was read but not used; the cap rows (2.13) are
  implemented here by a different method (prefix sums, below).
- Arithmetic stack: Python ints + GMP (gmpy2) for exact integer polynomial products by Kronecker substitution,
  numpy for limb handling, mpmath (320 bits plus an outward margin) for logs/exps; no python-flint / Arb / FLINT.

## 2. Algorithms (different from [14]'s set-partition expansion)

- **Moments.** A coordinate is the series G = sum_roles mark(role) sum_j K^role_j X^j exp(sum_e z_e t_j^e); then
  M_{d,eta} = alpha! [z^alpha] G^d. Because [z^alpha]G = P_{w(alpha)}[K]/alpha! depends only on the weight,
  G^d = sum_k binom(d,k) P_0^{d-k} N^k (N = G - P_0 nilpotent in the truncated ring: z-monomials closed under the 53
  signatures sigma u tau, marks x^2 = y^2 = 0 for P_j, y^2 = 0 for L_j, y^4 = 0 for H) is expanded symbolically
  with exact rationals, giving integer coefficients on numeric monomials P_0^m prod P_w[role]. Checked by brute
  force over all cells and role placements of tiny grids (d = 3, 4; all three rings): exact agreement; the
  extracted coefficients reproduce (1.43) (40 P^39 C + 1560 P^38 A B) and [y^3]Q^40 = 40 F0^39 F3 + 1560 F0^38 F1 F2
  + 9880 F0^37 F1^3. P-type components need 758 (R) + 1267 (V) numeric monomials, H 1145 + 1984.
- **Products.** Exact integer polynomial products (Kronecker, 480-bit slots, GMP), coefficientwise floor at
  2^-192, with a rigorous running deficit bound e(XY) <= e(X) S(Y) + e(Y) S(X) + 1 (units 2^-192, S = coefficient
  sums). All contractions are exact integer dot products; R uses Q_eta(r) as exact integers (scale (10^10 DX^6)^2).
- **Cap rows (2.13)** by prefix sums: x_{r+a}^d = sum_i binom(d,i) x_r^{d-i} (ah)^i, so every v_{s,tau}(r) is a
  combination of windowed sums of a^i g_a d_s(a) t_a^e (exact integers apart from the 2^-200 rounding of g d t^e).
  Checked against direct mpmath summation at r = 0, 50000, 95000, 97000 for tau = (), (2), (3,3): 20 digits agree.
- **Kernels** directly from (2.1), (2.2), (2.4)-(2.9) with directed fixed-point integer arithmetic (2^-224 for the
  Dickman recurrences, ceil for every upper array).
- **End-to-end check of the moment engine**: I_H by (2.12) with the same engine (cap arrays with midpoint cell
  averages of (2.2)): 2.368531785333e-14, inside Lemma 2.5's [2.3685317816e-14, 2.3685317890e-14] and equal to our
  earlier programs' 2.36853178533e-14 (runs/loss_outer2_ihcheck.log, 202 s).

## 3. Readings of ambiguous points (all stated; none was tuned to the table)

R1. (2.1): the +1/(2M^3) term sits in the UPPER recurrence (only monotone-consistent placement; the acceptance test
    "ordered, nonincreasing" passes for every cap used).
R2. (2.9): \overline d_j(c), \underline d_j(c) are the Lemma 2.2 POINT enclosures at grid point j, caps rounded
    b^+ = h ceil(b/h), r_+^+ = h ceil(r_+/h), r_-^- = h floor(r_-/h) ("upward caps in upper grids, downward in
    lower"); NOT the cell averages d_c(j) of Sec. 2.2 (those are used only in the cap rows (2.13)).
R3. chi_G of (1.25): r in [floor(b_G/h) - d_G + 1, min(n - 1, floor(t_G/h))] = [95599, 98263] for O_{5/2}
    (b_G = a_{n,24}, t_G = 98303h); this coincides with the third outer row of (1.5). W = 1 except for low bins.
R4. (2.16), (2.20): the erased coordinate uses the same marked arrays with profile power 0 (w^(0) = 1, Z_0 = 1);
    [*](C(r) M_39(r)) is the sum over the complementary placements (1.44): for P_j
    C_P M^{xy} + C_A M^{y} + C_B M^{x} + C_C M^{1}; for H sum_i C_{F_i} M^{(3-i)}; for L_j C_P M^{y} + C_D M^{1};
    C_role(r) = sum_a chi_G(r+a) W(r+a) K^(0),role_a.
R5. Lemma 2.4: the fraction lambda(t_j^+) multiplies the A array and lambda(min{t_j^+, (m t_j^+ - U)/(m-1)}) the C
    array, for both profile powers (upper bounds, lower bound of Lambda in the denominator); Lambda = log(b/a)
    (upper bound) is the external factor in R and V.
R6. (2.8): D_0 = h sum_j \overline d_j(Lh) X^j with the delay recurrence at L = 19660 (no renewal branch, no tilt);
    the "fixed array" is ceil(w^(e)_j [X^j]F_a/h).
R7. (2.18): P(0, z_G) = {3} for O_{5/2} (z_G = c_3 = 46580h; the strict inequality excludes l = 1, 2), so
    v^(3) = v_1 + v_2 + v_3 is the only marginal.
R8. (2.13) cap rows use the cell averages d_{c_s}(a) = A_a(c_s)/h; we take the MIDPOINT of the (2.2) enclosure and
    report separately the effect of the enclosure width ("B up" = mid + width bound + truncation bound).
R9. Low bins: slope theta = ceil(7/u_j) with u_j in absolute length units; L_{<=l} = total of fragments <= l;
    (1.26) with c_t = a_t, V_t = A_t, mu_t = 2 for orders 1-2 and 5/2 for order 3, eligible rows = O_{5/2} rows and
    the absorbed O_2 rows with xi_t < u. Result: c_G(u) = b_G exactly for L12..L22 and c_G(u) > b_G for L1..L11,
    i.e. exactly the "11 + 11" split of Lemma 1.6. J = floor((N-1)/L) for L19..L22, so the omitted sum in T-hat
    vanishes. Delay branch (L >= 64). W(r) uses d_G = 40, also at the full index r + a in C(r).

## 4. Results (O_{5/2}, all 17 requested components)

A ours = ceil(10^18 R_up / I_H^-), where R_up = R + rigorous truncation bound (the source arrays are fixed upper arrays,
so R has no other enclosure width; R_up - R < 2e-31 relative to I_H, i.e. A ours = A from the midpoint up to the
last unit for P/H and within 8 units for L). B ours (mid) uses the midpoint of (2.2) in the cap rows; B ours (up)
adds the bound for the (2.2) width (crude: |kappa| sums, max |x| per shell) and the truncation bound (crude scalar
bound, dominant for H and L). Ratios are ours/table. seconds = wall time of the component (2 processes in parallel
on 4 cores shared with another job); peak RSS from getrusage.

| component | A ours | A table | ratio | B ours (mid) | B ours (up) | B table | ratio (mid) | seconds | peak RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P1 | 57148020006662 | 57148020076132 | 0.9999999988 | 15810035582373 | 15810035606553 | 15810035599715 | 0.9999999989 | 711 | 1208 |
| P2 | 69886316414622 | 69886316496332 | 0.9999999988 | 18805329943009 | 18805329971042 | 18805329967080 | 0.9999999987 | 699 | 1203 |
| P3 | 69366993021785 | 69366993102523 | 0.9999999988 | 18409874196632 | 18409874224155 | 18409874222209 | 0.9999999986 | 691 | 1210 |
| P4 | 62684550937132 | 62684551010344 | 0.9999999988 | 16455348493177 | 16455348518092 | 16455348517458 | 0.9999999985 | 678 | 1202 |
| P5 | 53862830737854 | 53862830801099 | 0.9999999988 | 13997130855541 | 13997130877129 | 13997130877252 | 0.9999999984 | 690 | 1189 |
| P6 | 44981354979339 | 44981355032435 | 0.9999999988 | 11577030522536 | 11577030540819 | 11577030541299 | 0.9999999984 | 675 | 1199 |
| P7 | 36911787897540 | 36911787941323 | 0.9999999988 | 9411611487796 | 9411611503106 | 9411611503675 | 0.9999999983 | 673 | 1198 |
| P8 | 29975466509295 | 29975466544992 | 0.9999999988 | 7572139357469 | 7572139370258 | 7572139370727 | 0.9999999982 | 692 | 1199 |
| P9 | 50573740899536 | 50573740961589 | 0.9999999988 | 12808689146054 | 12808689169341 | 12808689167903 | 0.9999999983 | 675 | 1192 |
| P10 | 32438336606922 | 32438336646873 | 0.9999999988 | 8046407125288 | 8046407142165 | 8046407139897 | 0.9999999982 | 681 | 1190 |
| P11 | 20308616056552 | 20308616081603 | 0.9999999988 | 4920425444300 | 4920425457333 | 4920425453752 | 0.9999999981 | 669 | 1187 |
| P12 | 12358345905914 | 12358345921158 | 0.9999999988 | 2916712116124 | 2916712127087 | 2916712121993 | 0.9999999980 | 647 | 1175 |
| H | 15056954287477 | 15056954296612 | 0.9999999994 | 2833062482791 | 2833063171905 | 2833062492447 | 0.9999999966 | 1064 | 1312 |
| L22 | 28197429938221 | 28197429960534 | 0.9999999992 | 5897287423908 | 5897289973911 | 5897287451435 | 0.9999999953 | 383 | 1075 |
| L21 | 14498518458000 | 14498518468563 | 0.9999999993 | 2872865664767 | 2872868606460 | 2872865686933 | 0.9999999923 | 375 | 1076 |
| L20 | 19352692634780 | 19352692647427 | 0.9999999993 | 3611707911673 | 3611711490052 | 3611707956032 | 0.9999999877 | 388 | 1076 |
| L19 | 3006707962473 | 3006707964277 | 0.9999999994 | 529135125550 | 529138087105 | 529135146833 | 0.9999999598 | 337 | 1085 |

Total: 17 components, 10728 s of component wall time (about 1 h 40 min elapsed with two workers), plus 202 s for
the I_H check. About 2300 GMP products per P component (3600 for H, 670 for L), ~0.35 s each.

### Discrepancy analysis

- **Every A and B is reproduced to 1e-9 - 5e-8 relative; no table entry is exceeded by more than that, and the
  table B lies inside our [B mid, B up] for P1-P4, P9-P12, H and all four L bins.** For P5-P8 the table B exceeds
  our B up by 123-569 units (<= 6e-11 relative), inside the systematic offset described next.
- **Systematic offset ~1.2e-9.** Our A is below the table by a nearly constant 1.17e-9 to 1.22e-9 relative for all
  12 rank-two bins (B mid: 1.1e-9 to 2.0e-9), 6e-10 for H, 6e-10 to 8e-10 for L19-L22 (A). It does not track
  Lambda (which varies by 20% across the bins), so it is not in the logarithmic factor. It is consistent with the
  table using upper arrays inflated by a common relative ~3e-11 per retained coordinate (40 x 2.9e-11 = 1.17e-9),
  e.g. an upper enclosure of w^(2) = g^2/Z with relative radius ~3e-11: Lemma 2.5's own I_H interval
  [23685317816, 23685317890] has relative half-width 1.56e-9 = 40 x 3.9e-11, and our I_H (2.368531785333e-14)
  sits at its centre, so [14]'s production apparently carries such a Z/w radius. This is our hypothesis; it
  cannot be confirmed without [14]'s archive. Either way it is an upward (safe) inflation of their bounds, and
  irrelevant at the 1e-6 level of Table 2.7.
- B for the low bins: the table exceeds our midpoint by 4.7e-9 (L22) to 4.0e-8 (L19), well inside our crude
  (2.2)-width bound (B up - B mid = 4e-7 to 5.6e-6 relative there).
- Development note (not a discrepancy): the first P2 run had a coding bug in the R contraction (R = 0; tuple
  unpacking in the incidence filter); fixed, P2 rerun; the faulty run is kept as runs/loss_outer2_P2_firstrun_Rbug.*
  (its V was already correct and equal to the final one).

## 5. Comparison with program 1 (code/cap6/loss_outer/part_O52_*.json), made only after section 4 was final

Program 1 reports A, B as decimals (its midpoint, before the ceiling).

| component | A ours | A prog1 | ours/prog1 - 1 | B ours (mid) | B prog1 | ours/prog1 - 1 |
|---|---|---|---|---|---|---|
| P1 | 57148020006662 | 57148020006661.08 | 1.6e-14 | 15810035582373 | 15810035582359.42 | 8.6e-13 |
| P2 | 69886316414622 | 69886316414621.18 | 1.2e-14 | 18805329943009 | 18805329942993.12 | 8.4e-13 |
| P3 | 69366993021785 | 69366993021784.77 | 3.3e-15 | 18409874196632 | 18409874196616.54 | 8.4e-13 |
| P4 | 62684550937132 | 62684550937131.55 | 7.3e-15 | 16455348493177 | 16455348493162.85 | 8.6e-13 |
| P5 | 53862830737854 | 53862830737853.84 | 3.1e-15 | 13997130855541 | 13997130855528.63 | 8.8e-13 |
| P6 | 44981354979339 | 44981354979338.02 | 2.2e-14 | 11577030522536 | 11577030522525.00 | 9.5e-13 |
| P7 | 36911787897540 | 36911787897539.98 | 4.4e-16 | 9411611487796 | 9411611487786.45 | 1.0e-12 |
| P8 | 29975466509295 | 29975466509294.95 | 1.8e-15 | 7572139357469 | 7572139357461.01 | 1.1e-12 |
| P9 | 50573740899536 | 50573740899535.05 | 1.9e-14 | 12808689146054 | 12808689146040.73 | 1.0e-12 |
| P10 | 32438336606922 | 32438336606921.20 | 2.5e-14 | 8046407125288 | 8046407125278.96 | 1.1e-12 |
| P11 | 20308616056552 | 20308616056551.73 | 1.4e-14 | 4920425444300 | 4920425444294.38 | 1.1e-12 |
| P12 | 12358345905914 | 12358345905913.73 | 2.2e-14 | 2916712116124 | 2916712116119.82 | 1.4e-12 |
| H | 15056954287477 | 15056954287476.73 | 1.8e-14 | 2833062482791 | 2833062482789.10 | 6.7e-13 |
| L22 | 28197429938221 | 28197429938216.30 | 1.7e-13 | 5897287423908 | 5897287425471.41 | -2.7e-10 |
| L21 | 14498518458000 | 14498518457995.57 | 3.1e-13 | 2872865664767 | 2872865667076.72 | -8.0e-10 |
| L20 | 19352692634780 | 19352692634775.88 | 2.1e-13 | 3611707911673 | 3611707917092.39 | -1.5e-09 |
| L19 | 3006707962473 | 3006707962469.35 | 1.2e-12 | 529135125550 | 529135124379.25 | 2.2e-09 |

- A agrees with program 1 to the ceiling unit for all P and H (relative differences <= 2.5e-14, i.e. our integer is
  the ceiling of program 1's decimal), and to <= 1.2e-12 for the low bins (where the exp/W enclosures differ).
  Two independent algorithms (set partitions + python-flint vs. symbolic z-series + GMP Kronecker) therefore give
  the same R_G to ~13-14 digits.
- B agrees to 7e-13 - 1.4e-12 for P and H: the difference is the cap-row (2.13) treatment of the (2.2) enclosure
  (we use its midpoint), far inside both programs' stated widths. For L19-L22 B differs by 3e-10 to 2.2e-9, also
  inside our (2.2)-width bound for those bins.
- Both programs fall short of Table 2.2 by the same ~1.2e-9 offset, so the offset is a property of [14]'s
  production, not of either re-evaluation.
- Program 1's recorded runtimes: 2000-5700 s per P component; this program: 650-710 s.

## 6. Files

- code/oai186_loss_outer2.py (program; docstring lists formulas, readings, sharing).
- code/cap6/loss_outer2/part_{P1..P12,H,L19..L22}.json (results), runs/loss_outer2_*.log (logs),
  runs/loss_outer2_queue.sh (the run schedule), runs/loss_outer2_cache/ (31 MB pickle of the cap rows v^(3);
  regenerable in ~15 s, need not be committed).
