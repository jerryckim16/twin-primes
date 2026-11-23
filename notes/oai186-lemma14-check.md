# Rung 186: check of Lemma 1.4 of [14] (and the ingredient max(A,C) <= 7L/3 of Lemma 1.1)

Source [14]: OpenAI, "Numerical certificate for prime gaps at most 186", dated 30 August 2026. The PDF IS in the repo:
`code/third_party/openai186/short_gaps_numerics.pdf`. This contradicts the remark in notes/sources-186-loss.md that it
"is NOT committed". I read it with `pdftotext -layout`. Every lemma and definition used below is in this one file.
Nothing else was needed. Page numbers are the printed page numbers.

Script: `code/oai186_lemma14_check.py`, output `code/oai186_lemma14_check.out`. It uses exact `fractions.Fraction`
throughout, runs 81 checks with 0 failures, and takes about 17 s. Sympy is not installed. All the inequalities
involved are linear and homogeneous in (p, L), so each is proved exactly by checking its slope and its value at
the breakpoint p = 2L/3 (section [2] of the script).

**Verdict: verified as stated.** The printed proof leaves one step implicit, the largest-witness exclusion ("The
imposed caps exclude a largest witness"). That step is correct. It rests on Lemma 1.1's A_t <= 11C_t/10 and on the
running-minimum caps (1.18), not only on max(A,C) <= 7L/3. Below I state it in full and check it exactly. I found
no error, and no step needs repair.

## 1. Definitions (with page references)

- p. 1. M_xi(X) := max({p in X : p > xi} u {0}). The inclusive obstruction is
  H_{phi,xi}(X) := max({ sum_{q in X, q >= p} q + phi(p) : p in X, p > xi } u {0}). "Equal fragment sizes remain in
  the inclusive prefix."
- p. 4, (1.12). H_{m,xi} is H_{phi,xi} with phi(p) = (m-1)p, for m in {2, 5/2}. So H_{5/2} (the "balanced
  obstruction") has phi(p) = 3p/2.
- p. 4, (1.13)-(1.16). g0, e = g0/rho, S, T0, T1, zeta. The ladders omega_{nu,t} and delta_{nu,t}. The quantities
  B_{nu,t} = (1/2 + 2 omega_{t-1})/rho and xi_{nu,t} = delta/rho. Then a = B - T_nu, b = B - S,
  eta = (xi + S + T_nu - B)/2 in order three (r_t = 3, t >= 24), A = a + eta and C = b + eta.
  L_{nu,t} := 23 C_{nu,t}/40, phi_D(u) := min(3u/2, L), phi_E(u) := 3u - phi_D(u).
- p. 4, (1.17). For nonterminal rows (A, C) = (S + e/2, T_nu + e/2) in order three. These are the "thresholds".
- p. 5, (1.20). The retained rows are T_o = {(o,t): t <= 27} and T_n = {(n,t): t <= 38}. The order-three retained
  rows are (o, 24..27) and (n, 24..38), 19 rows. All of them are nonterminal.
- p. 5, (1.21). These are the order-three predicates on a root of total s:
  - O_t = {s <= a_t} u {H_{phi_D,xi_t} <= A_t, phi_E(M_{xi_t}) <= C_t} (outer).
  - I_t = {s <= b_t} u {H_{phi_E,xi_t} <= C_t, phi_D(M_{xi_t}) <= A_t} (inner).

  A "failure" is the complement. The "two nonlinear obstructions" are H_{phi_D} and H_{phi_E}.
- p. 5, (1.18). These are the caps, one per fragment:
  - outer: z = S + e/2 - 23(T1 + e/2)/40 on (a_{n,24}, S];
  - base: z = 63(T0 + e/2)/160 on (b_{o,24}, T0];
  - enlarged: z = 63(T1 + e/2)/160 on (b_{n,24}, T1].

  Grid masks (1.5) and (1.19) round each cap down to 46580h, 35265h and 35419h.
- p. 6-7, Lemma 1.1 and its proof. In order three, eta = xi - e/2 > 0, A + C = B + xi, A >= C > L and
  A <= 11C/10 < 161C/120 = 7L/3. "The bounds for the largest fragment and opposite root are therefore A_t - L_t
  and 63C_t/160". The caps are their running minimum.
- p. 5-6, (1.22)-(1.24). These give the six groups, their source rows and their parameters (m, xi_G, U_G, (b_G, t_G],
  z_G, p_G).
- p. 9, (1.34). Lemma 1.4 and (1.35).

Reading. I take "nonlargest witness" to mean a p in X, p > xi, such that some other element q of X has q >= p.
Two equal largest fragments therefore both count as nonlargest; their prefix is 2p. Ties have nu-measure zero (the
Poisson intensity dv/v is continuous), so the convention does not affect any integral. I take "the bounds for the
largest fragment and opposite root" to be the fragment caps of (1.18) on the order-three shells. In the outer
case they control both the term of the largest fragment in H_{phi_D} and the opposite-root conjunct
phi_E(M_xi) <= C.

## 2. Statement in my notation

Let t be a retained order-three row, with (A, C, L, xi) = (A_t, C_t, 23C_t/40, xi_t). Let X be a root (the fragment
multiset of the 40-coordinate outer configuration, or of the 39-coordinate face) with total s, and with every
fragment at most the cap z(s) of (1.18) on its face.

- **Outer.** If s > a_t and (H_{phi_D,xi}(X) > A or phi_E(M_xi(X)) > C), then there is a nonlargest p in X,
  p > xi, with sum_{q >= p} q + 3p/2 > A = S + e/2.
- **Inner.** If s > b_t and (H_{phi_E,xi}(X) > C or phi_D(M_xi(X)) > A), then there is a nonlargest p in X,
  p > xi, with sum_{q >= p} q + 3p/2 > C = T_nu + e/2.

Then by (1.22)-(1.24) the event lies in the group O_{5/2}, I_{5/2}^old or I_{5/2}^new respectively, because
xi_G <= xi_t, U_G = threshold and b_G <= core.

## 3. Step-by-step check

| # | Step | Status | Exact check (script section) |
|---|------|--------|------------------------------|
| 1 | Lemma 1.1: max(A,C) <= 7L/3 | **verified** | [1]. (1.17) holds exactly for all 19 rows, and no retained row is terminal. A >= C > L > 0. The largest A/C is 1.0975913 (old rows; new rows 1.0928) <= 11/10 < 161/120 = 7·23/(3·40). The smallest slack 7L/3 - A is 0.2324. |
| 2 | "Below 2L/3 both allocation functions equal 3p/2" | **verified** (read "below" as p <= 2L/3) | [2]. phi_D(p) = 3p/2 iff 3p/2 <= L iff p <= 2L/3, and then phi_E = 3p - 3p/2 = 3p/2. At p = 2L/3, phi_D = L = 3p/2. For p > 2L/3: phi_D = L < 3p/2 < phi_E = 3p - L. Also checked on an exact grid p/L in [0,2] with step 1/1500. So for p <= 2L/3 the phi-term at p is the H_{5/2}-term at p, for both predicates. |
| 3 | A nonlargest witness has prefix >= 2p | **verified** | The prefix contains p and a distinct q >= p. |
| 4 | For p > 2L/3: terms >= 2p+L, 5p-L, 7p/2 | **verified** | phi_D = L, phi_E = 3p - L, plus the prefix bound >= 2p. |
| 5 | ... all > 7L/3 | **verified**, sharp | [2]. The differences are 2(p - 2L/3), 5(p - 2L/3) and (7/2)(p - 2L/3). Each is > 0 iff p > 2L/3, and each is 0 at p = 2L/3, where step 2 applies instead. |
| 6 | "Thus the predicates fail together" | **verified** | By steps 1, 2 and 5, at every nonlargest witness: phi-term > threshold iff 3p/2-term > threshold, for threshold A (outer, phi_D) and C (inner, phi_E), since both are <= 7L/3. Only the direction phi-failure => H_{5/2}-failure is needed. [5]: 0 mismatches in 152,000 random or adversarial exact configurations. |
| 7 | "The imposed caps exclude a largest witness" | **verified** (implicit in the proof; supplied here) | [3]. Take M unique largest, with its own term M + phi(M). **Outer:** for M <= 2L/3, 5M/2 <= 115C/120 < A and 3M/2 <= L < C hold automatically. For M > 2L/3 we need M <= A - L (for H_{phi_D}) and M <= (C+L)/3 = 21C/40 (for the opposite-root conjunct phi_E(M_xi) <= C). A - L <= 21C/40 is equivalent to A <= 11C/10, which is Lemma 1.1. The cap z = S + e/2 - 23(T1+e/2)/40 equals A_n - L_n exactly. It is <= A_o - L_o <= 21C_o/40 for the old rows (slack 4.7e-3). **Inner:** phi_D(M) <= L < C <= A holds automatically. For M <= 2L/3 = 23C/60 < 2C/5 we have 5M/2 < C. For M > 2L/3 we need 4M - L <= C, i.e. M <= 63C/160, which is exactly the base and enlarged caps. At equality the term is exactly C, which is not a failure because the predicate is non-strict, and the grid caps are strictly smaller anyway. **Region:** a_t >= a_{n,24} for all 19 rows (a_{o,24} - a_{n,24} = 3.6e-3) and b_t >= b_{nu,24}. The capped mask rows begin at j0 = floor(l/h) - d + 1 (95599, 87195, 87250), and every cell below j0 has totals < l. So the cap holds wherever a row can fail. The inner new predicate is also imposed on the base face, but it is charged in beta_new over H1 \ L1, which contains H0 \ L1 since H0 <= H1 index by index (checked). Negative controls: raising any cap by 1e-12 above its sharp value produces a single-fragment failure that has no nonlargest witness. |
| 8 | Group containment: (1.35) is the right target | **verified** | [4]. For every own row: xi_G = min xi_t, U_G = threshold (S + e/2, T0 + e/2, T1 + e/2) and b_G = min core. The face's largest total <= t_G. The absorbed order-two rows (needed for (1.35), not for Lemma 1.4) have xi_t >= xi_G and V_t = S+e, T+e >= U_G, so their H_2 failure is an H_{5/2} failure (3p/2 > p). The 5/2-shell caps also exclude a largest H_2 witness (2z <= threshold). The H_2 groups end where the 5/2 groups begin. |

## 4. Code consistency, task (c)

- **Upstream `prime_gap_186_certificate.py`.** It imports python-flint at top level, and flint is not installed,
  so the script pulls the group-construction code (`_ladder`, `_shells`, `_cells`, `_event_cells`, `_group`,
  `build_inputs`, `source_clipped_group`) out with `ast` and executes it unchanged. It builds exactly the six groups
  of (1.35), in order. Their order, activation, threshold, radial interval, hard cap, split and source rows agree
  exactly with (1.22)-(1.24). `nonlargest=True` is asserted for each, and order-three rows carry
  `owner_plateau = 23C/40 = L_t`.
- **Our evaluators.** The script extracts `group_data` and `clip_lower` from `oai186_loss_outer.py` (O_2, O_{5/2})
  and `oai186_loss_inner.py` (four inner groups) the same way and calls them. Their output matches (1.22)-(1.24),
  including the own and absorbed rows.
- **Clipping.** A difference worth noting: upstream's 5/2 groups list only the order-three rows in `source_rows`.
  It does not include the absorbed order-two rows that the text of (1.26) says to include, and our code does
  include them. The clipped lower boundary c_G(u) is nevertheless identical at all 61 low-bin ends (32 outer,
  29 inner), so this has no effect on the cover.
- **Scope of this check.** The Lemma 1.4 reduction never enters the loss code as a formula. It is only the
  justification for using H_{5/2} with (U_G, xi_G) = (min threshold, min activation). The code is consistent
  with it.

## 5. Not covered here

- Lemmas 1.5-1.7, 2.3 and 2.4: whether the low, rank-two and factorial forms majorise the "nonlargest H_{5/2}
  failure" events, and whether the cover by rank is complete.
- The analytic part of Lemma 1.1 (the distribution inequalities of [8]).
- The restoration step (Proposition 1.3).

The random test in [5] is a sanity check. The proof is the algebra in rows 1-7.
