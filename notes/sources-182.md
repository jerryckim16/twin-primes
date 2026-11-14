# Rung 182 (k = 39): source notes

Source: GPT-6 Astra (OpenAI), prompted by Romyar Sharifi, "A fixed-profile proof for prime gaps of at most 182",
dated 18 September 2026 (first version 4 September 2026). It is the first paper in the PDF bundle
https://www.math.ucla.edu/~sharifi/AI/prime_gaps_182_expository_bundle.pdf.

How the file was obtained (14 Nov 2026):
- WebFetch of the PDF failed with "maxContentLength size of 10485760 exceeded". The file is 16 MB, so this is a tool
  size limit, not a host block.
- I downloaded it with plain `curl` (HTTP 200, application/pdf, 17271479 bytes) into a new empty directory,
  /tmp/claude-0/-home-user-twin-primes/c2b439a5-665d-5729-82d7-77e5d84fc327/scratchpad/src182/bundle.pdf
  (SHA-256 5362e977880af92a73a79b411a9c66daf0b93af4ec0ed6bec320090386f4b881).
- I read it with `pdftotext -layout`, and with `-raw` to cross-check the knot vector. Nothing was executed.

PDF metadata:
- Title "Prime gaps at most 182: manuscripts and conditional formalization".
- Subject "Published inputs and conditional formalization; 18 September 2026".
- Author "GPT-6 Astra (OpenAI), prompted by Romyar Sharifi".
- 132 pp. CreationDate 4 Oct 2026.

The bundle contains three papers:
- **[M] Main paper:** PDF pp. 1-52, printed pp. 1-52.
- **[10] "Incidence operators and intervals containing many primes":** PDF pp. 53-88.
- **[11] "Kloosterman correlations with finitely many exceptional Fourier frequencies":** PDF pp. 89-132.

In this note, "p." is the printed page of [M] and equation numbers are those of [M], unless stated otherwise.

Directory https://www.math.ucla.edu/~sharifi/AI/ (WebFetch, 14 Nov 2026) lists only the parent directory and
`prime_gaps_182_expository_bundle.pdf` (last modified 2026-10-04 09:45, size 16M). It has **no companion files
there**: no certificates, code or data. The digital supplement is said to be elsewhere (Sec. 8 below).

**Status of everything below: Claimed (read from source).** Garbled extraction is marked "[reading]". "Mine:" marks my
own arithmetic or interpretation. Nothing here is a new result.

---------------------------------------------------------------------------------------------------------------
## 1. What is claimed

- Thm 1.2 (p. 5), verbatim: "One has DHL[39, 2]. Consequently H1 <= 182." Def 1.1: DHL[k,2] = "every admissible set
  of k distinct integer shifts has infinitely many translates containing at least two primes."
- **k = 39** (p. 5: "reduces the tuple size from 40 in [17, Theorem 1.1] to 39").
- The tuple comes from the MIT prime gaps table [16], Sec. 12, p. 42. It has 39 entries and diameter 182:
  {0,6,14,20,24,26,30,36,42,44,50,54,62,66,72,80,84,86,92,96,104,110,114,120,126,132,134,140,146,150,152,156,
   162,164,170,174,176,180,182}.
  Omitted residues are given for p <= 37:
  2:1, 3:1, 5:3, 7:4, 11:1, 13:12, 17:5, 19:2, 23:10, 29:3, 31:12, 37:1.
- Headline numbers (abstract and p. 5):
  - Q: "surplus greater than 0.0002766919371".
  - Q: "all corrections needed to restore the arithmetic support cost at most 0.000211478178".
  - Q: "The remaining surplus exceeds 0.000065213759".
  - Q: "The profile is described by 726 rational coefficients."

## 2. Analytic input (Sec. 3, pp. 11-18; Sec. 4)

The paper says the new estimates are proved in the two companions bundled with it. Q (p. 5): "the analytic results in the
companions are substantive parts of the proof".
- **New Type II, "incidence" estimate.** [10, Thm 2.1, Cor 9.3]; [M] (3.1), p. 12.
  - It applies to alpha_M * beta_N with N = x^gamma and theta = 1/2 + 2 omega, under the conditions
        12w + 6d < gamma < 1/2 - 2w,   2gamma + 4w + 2d < 1,   gamma > 16w + 7d,   5gamma > 3/2 + 40w + 16d.
  - [reading] In [M] the fractions are garbled ("12 - 2w", "5γ > 32 + ..."). I took the values from [10] (2.3), PDF
    p. 54, which prints 1/2 and 3/2 cleanly. The abstract of [10] gives the same final condition as
    gamma > 3/10 + 8w + (16/5)d.
  - The proof uses an incidence-operator bound inside Stadlmann's dispersion square, with rank-four hyper-Kloosterman
    eigenvalues.
- **New Type III estimate.** [11, Thm 1.1]; [M] (3.2)-(3.3).
  - It applies to alpha * psi1 * psi2 * psi3, with x^{2s} << N_i << x^{1/2-s}, N_iN_j >> x^{1/2+s} and 0 < s < 1/6.
    The conditions are
        sigma > 1/30 + (56/15) w + (4/15) d,   108w + 2d > 1
    (fractions confirmed from [11] (1.2), PDF p. 90).
  - The moduli are squarefree and singly densely divisible.
  - The new local input is the "finite-exceptional Fourier estimate" [11, Prop 3.1] for a four-cycle of rank-three
    Kloosterman correlations.
- **Old ladder.** It uses genuine primes and cites [17] = OpenAI 186, Cor 2.19, with (3.4), p. 12:
      108w + 30d < 1 (order 1),   280w + 80d < 3 (order 2),   240w + 80d < 3 (order 3).
  - Orders 1-2 use Polymath8a, Thm 2.8(i),(ii),(iv),(v).
  - Order 3 uses Stadlmann's bilinear estimate [21, Prop 1], extended to triply densely divisible moduli in
    [17, Prop 2.18, App. A.4], together with Polymath8a Type III and Heath-Brown.
- **Parameters fixed in (3.5), p. 12:** a = .41361, I0 = .34941, c = .41364, tau = 10^-10.
  - New order-three Type II band: a - tau <= gamma <= .45.
  - Lower-order Type II conditions:
        54w + 15d + 5 sigma_m < 1 (order 1),   56w + 16d + 4 sigma_m < 1 (order 2),   sigma_m = 1/2 - a + tau;
    also 68w + 14d < 1.
  - Type III choice: sigma = 1/2 - c - tau, with w-bar = max(w, .01) "when necessary".
- **Sharp five-prime minorant (Sec. 4, pp. 18-23), new here.** Built from the Harman/Baker-Irving decomposition in
  [10, Thm 11.1].
  - (4.1): rho_x(n) = 1_P(n) - b_x(n), where b_x = 24 * 1_{S5(a;x)} and S5 is the set of products of five distinct
    primes with every pair product < x^a. Also lambda = 1 - 2a = .17278.
  - The mass deficit kappa_true is the 4-dimensional integral (4.2), with
        .000093307088324061 < kappa_true < .000093307088324062.
    It is certified by exact rational moment series on 3 simplices, (4.5)-(4.11).
  - Upper bound used, (4.3): kappa-bar = 46653544162031/500000000000000000.
  - Lean uses instead kappa_cvx = 11696/125000000 (Sec. 13.3).
- **Exceptional-square upper bound (Sec. 5), proved here.**
  - Hinge weight w_t(s) = (12/5)(s-t)_+/(2/5 - t) with t = .38, plus an auxiliary Selberg sieve with root-dependent
    radius.
  - (5.2): z_j(q) = min{lambda - eps0, (1-s_j)/2 - q - eps0}, eps0 = 10^-4.
  - Step kernel (5.6): 1024 pair bins on [2 lambda, a]; retained-sum blocks of 768 fine indices; 21-term alternating
    log series; numerators rounded up to multiples of 10^-25.
  - (5.7): 0 <= K <= 2.194.
- **Proved here, Sec. 6:** the signed hybrid inequality (Prop 6.1), the support restoration (Thm 8.1) and the
  coverage by seven source families (Sec. 9).
- **Cited from [17] (OpenAI 186):** the fragment-measure realization, the pairing identities, Props 3.5/3.7, Lemma 3.8
  and Lemmas 4.1-4.3.
- Song-Yue, Kintali and Charton et al. [3] are cited for the dispersion targets ([3, Lemma 5.6, Sec. 6.4]) and history.
  Stadlmann 2026 [22] is cited for the mixed-support idea and for Lemma 6.

## 3. Sieve support

- The support is **not a simplex.** It uses the 186-style framework: Poisson "fragment configurations" with
  nu_zeta = e^{gamma_E} zeta Law(Pi_zeta) ((2.1), p. 7), Dickman total law rho_D(t/zeta) dt ((2.3)) and erasure
  operators E_i ((2.6)).
- Arithmetic domains are predicates on the pooled fragments (Sec. 3.5): tail obstructions
  H_{phi,xi} = max_{u>xi}(sum_{v>=u} v + phi(u)) (3.7), with order 1/2/3 rows (3.8)-(3.11).
  - Order-three allocation: phi_D(u) = min(3u/2, L), phi_E = 3u - phi_D.
  - Plateaux:
        Lambda_old = clip((3A_r - C_r)/4; 3max/7, 3min/5),   Lambda_new = (23/40) C_r.
  - Counts: 43 old and 55 new retained rows (p. 16); 638 scalar source inequalities and 31 order-three extraction
    witnesses (p. 16).
  - **The full row tables are NOT in the PDF**; they are in the digital supplement. Only rows 13 and 14 of the new
    ladder are given, (3.15)-(3.16):
        b13 = 37058221276498005595947498293/40868109574262446536646110000,
        b14 = 260700046797786617627841743303/286076767019837125756522770000,   xi_j = U_n - b_j,
        U_n = T1 + eps_r/rho, eps_r = 10^-7.
  - Self source: w_s = 21/5000, d_s = 2279/100000, xi_s = 22790/262499, c_s = B0 - T1.
  - Subtraction source (3.17): S_C = B0 - b14 - eps_r/rho*, sigma0 = .100001, and w_C, d_C as displayed.
    rho* S_C ~ .2607860319243.
- Four domains (3.12), p. 15:
      O = H_O ∩ O_old ∩ O_new,   L0 = H_0 ∩ L_old ∩ L_new,   L1 = H_1 ∩ L_new,   C = H_C ∩ C14raw,
  with L0 ⊂ L1 ⊂ C.
- Scales (7.1), p. 29:
      k = 39,  N = 393216,  n0 = N - k = 393177,
      S = 1379373467/1312494500,  h = S/N = 1379373467/516093837312000,
      rho* = 2624989/10^7 < rho = 262499/10^6.
      T1 = 1262625033/1312494500 (p. 16),  B0 = 1/(2 rho).
  - T0 is given only via rho* T0 = .2491228441011 (p. 29). I found no exact rational for T0.
  - Physical radii: rho* S = .2758746934, rho* T1 = .2525250066, 2 rho* S = .5517493868 < 1.
  - Ambient cutoff zeta = .17277/rho.
- Cap domains (Sec. 7.2 table, p. 30). r = sum of cell indices (inclusive range); bound M0 <= c h, where M0 is the largest
  fragment over all coordinates:

  | domain       | d  | r range          | c      |
  |--------------|----|------------------|--------|
  | H_O          | 39 | 0 : 352697       | 246256 |
  |              |    | 352698 : 376449  | 196608 |
  |              |    | 376450 : 393176  | 186253 |
  | H_0          | 38 | 0 : 334253       | 246256 |
  |              |    | 334254 : 343163  | 177542 |
  |              |    | 343164 : 355047  | 140306 |
  | H_1          | 38 | 0 : 336274       | 246256 |
  |              |    | 336275 : 343169  | 179967 |
  |              |    | 343170 : 359896  | 141724 |
  | H_C          | 38 | 0 : 352698       | 246256 |
  |              |    | 352699 : 371671  | 186491 |

  - Cell convention, p. 29: j_i = floor(|X_i|/h), t°_i = (j_i + 1/2)h, s° = (r + d/2)h, s+ = (r + d)h. The profile uses
    midpoints; Q: "its support tests use the actual fragments and the whole-cell upper total."
  - Mine: these domains have exactly 4x the cell count of 186 (N = 98304 there). 246256h = 0.6581729 is just below
    zeta = 0.6581739.

```json
{
  "status": "Claimed (read from source), [M] (7.1), Sec. 7.2, (3.5), (6.8), (4.3)",
  "k": 39, "N": 393216, "n0": 393177,
  "S": "1379373467/1312494500", "h": "1379373467/516093837312000",
  "rho_star": "2624989/10000000", "rho": "262499/1000000",
  "T1": "1262625033/1312494500", "rho_star_T0_decimal": ".2491228441011",
  "zeta": ".17277/rho",
  "caps_HO":  [[0,352697,246256],[352698,376449,196608],[376450,393176,186253]],
  "caps_H0":  [[0,334253,246256],[334254,343163,177542],[343164,355047,140306]],
  "caps_H1":  [[0,336274,246256],[336275,343169,179967],[343170,359896,141724]],
  "caps_HC":  [[0,352698,246256],[352699,371671,186491]],
  "component_caps_over_h": [141720, 177528, 246256],
  "a": ".41361", "I0": ".34941", "c": ".41364", "tau": "1e-10",
  "ell": "6308693370963335/576460752303423488",
  "kappa_bar": "46653544162031/500000000000000000",
  "hinge_t": ".38", "eps0": "1e-4", "K_upper": "2.194", "t_young": "11/10"
}
```

## 4. The test function (Sec. 7.3-7.5, pp. 30-32)

- One-coordinate factor (7.2), the same as 186 [18, (1.7)]:
      g(t) = (21/200)/(1 + t/100) + (179/200)/(1 + (907/5) t).
- Eleven signatures, in the order of the coefficient table (p. 30; this is a different order from 186):
      ∅, (2), (3), (4), (2,2), (5), (2,3), (6), (2,4), (3,3), (2,2,2).
  - P_j = sum_i (t°_i)^j and P_sigma = prod P_j. These are products of power sums, so diagonal terms are kept.
- Radial part: **22 cubic B-splines** B_{d,3}(s°), 0 <= d <= 21, using Cox-de Boor with right-continuous knots.
  - The knot vector has 26 entries (confirmed with -raw):
        (3/20)x4, 1/4, 7/20, 9/20, 11/20, 13/20, 3/4, 33/40, 7/8, 37/40, u1 x4, 49/50, u2 x4, S x4,
        u1 = 324809441462533/344528493755500,
        u2 = 16262888471886818524688913778251703267/16161921199408696007503616565983946000.
  - Mine: u1 ~ 0.942765, u2 ~ 1.006247 and S ~ 1.050956, so the knots are increasing. The fourfold internal knots allow
    jumps, and the spline argument is uncentered s°.
- Profile (7.3), with component caps A = {141720h, 177528h, 246256h}:
      F(X) = 1_{H_O}(X) prod_{i=1}^{39} g(t°_i) * sum_{c in A} 1_{M0(X) <= c} sum_sigma sum_{d=0}^{21}
             c_{c,sigma,d} B_{d,3}(s°) P_sigma(t°).
  - Coefficient count: 3 x 11 x 22 = 726.
  - Q: "The exported coefficients already include the angular scaling ... without an additional power of 39."
  - Q: "The three cap components ... are added before every square."
- **The coefficients are NOT printed in the PDF.** Q (p. 31): "The complete rational table is supplied as digital
  data; Appendix B identifies it unambiguously."
  - In the repo, Lean literal: formal/TrialData182.lean. JSON: inputs/source_certificates/; "the full profile is given
    by the three independent_components arrays. The top-level vector is a constructor seed" (p. 46).
  - Trial-file SHA-256 (p. 46, split over two lines in extraction):
    3ebae41700a7839f2d7a7b3fe068b11ed364a7542aab110173bbcdbd66645952.
  - Mine: the component caps 141720 and 177528 are not the same as the H_0/H_1 caps.
- Normalization (Sec. 7.5): g_j = g((j + 1/2)h), Z = sum_{j<n0} g_j^2, and every form is divided by
  𝒩 = (hZ)^39.
  - Cell masses: w_c(j) = int_{jh}^{(j+1)h} rho_D(t/c) dt.
  - Face prefactor 39h/Z.
- Appendix B also mentions "12 shells". The main text does not define them. [Not found; presumably the radial
  shells/spans of the certificate.]

## 5. Numerical criterion and certification

- Criterion, Cor 6.2 (p. 29): rho* 𝒥(U) > I(U) for U = PF = 1_O F, where (6.7)
      𝒥(U) = J0(U) + (1 - ell) J+(U) - d_h E_{C^c}(U),   d_h = kappa-bar (1/ell - 1),
  - J0 = sum_i ||1_{L0} E_i U||^2 and J+ = sum_i ||1_{L1\L0} E_i U||^2.
  - E^tail_i = int_{C^c} K |E_i U|^2 dnu^{38}, from Prop 6.1, (6.5).
  - (6.8): ell = 6308693370963335/576460752303423488 (Mine: ~0.010944).
  - Mine: in Polymath terms this is a "ratio > 1" criterion in rho* units, as in 186, not the Maynard kJ/I > 4.
- Cap quotient (7.4): q_H = rho* (J0,H + (1-ell)J+,H - d_h E_{H_C^c}) / I(F).
- Enclosures:
  - (7.5): I-/+ = 9900316613656518642800593 / 9900316889124784142456785 over
    664613997892457936451903530140172288, i.e. about 1.4896341e-11.
  - (7.6): mu = q_H - 1 >= mu- = 9968877639291/36028797018963968 > .0002766919371.
- Restoration (Thm 8.1, (8.6)):
      loss = b + Gamma b/t + 2 sum sqrt(A_j M_j) + (t - gamma_op) sum A_j,   t = 11/10,
  with eps_h = kappa-bar(1/.0108 - 1) 2.194, delta_op = 4 rho* eps_h and Gamma = 4 rho*(1 + eps_h) ((8.3)).
  - It has 197 source components: 60 outer and 137 inner (Sec. 9.1 table, families G1-G6 and C).
  - Split points p_G/h: 98304, 78643, 88771, 71017, 89983, 71986, 93245.
- Sec. 10 tables (p. 40), in units of 1e-6, rounded up:
  - b = 26.702800674
  - Gamma b/t = 25.966859017
  - 2 sum sqrt(A M) = 155.342695198
  - (t - gamma_op) sum A = 3.465822296
  - (10.2): L-bar = 105739089/500000000000 = .000211478178.
  - (10.3): mu- - L-bar = 573626291549967919851/8796093022208000000000000 > .000065213759.
  - CHECKED HERE (trivial exact-rational subtraction, Python fractions): mu- - L-bar equals the displayed (10.3)
    fraction exactly. I also checked h = S/N, rho* S = .2758746934 and rho* T1 = .2525250066. No integral was checked.
- Certification method (Sec. 10.3, p. 41):
  - Arb interval arithmetic; exact rational spline pieces; Q: "exact Dickman logarithm and dilogarithm primitives on
    0 <= u <= 3" (largest Dickman argument 393177/140306 < 3).
  - Positive Poisson/Mecke majorants with exponential (Chernoff) kernels for source failures (9.1)-(9.2).
  - Directed integer recurrences (9.6).
  - Fine-grid aggregation by 48 with Bernstein / PSD Gram enclosures (9.3)-(9.5).
  - Q: "two independent scalar implementations". Q: "The fast scalar checks do not repeat those long integrations."
- Lean (Sec. 13):
  - Repo romyar1/prime-gaps-lean at commit b77bf175bdedc5123027b3fcf0abc38427975770, with Lean 4.34.0-rc2.
  - It proves the implication to DHL[39,2] and H1 <= 182 under **262 numerical integral inequalities as hypotheses**
    (5 cap, 60 outer-root, 60 outer-face and 137 inner-face), plus finite-field premises: Katz Kloosterman bounds,
    Fouvry-Kowalski-Michel, and the local Fourier proposition [11, Prop 3.1].
  - Q: "The posted endpoint does not prove the 262 integral inequalities."
  - The Lean margin uses kappa_cvx: (rho* 𝒥cvx(PF) - I(PF))/I(F) > 33/10^6 (p. 45).
  - External recomputation of 9 Sep 2026: "All 262 rational target comparisons, 14 implementation audits and four
    deliberate rejection tests passed" (p. 44).

## 6. Differences from 186 and from the 240/236 supports

- **Versus 186** ([17], [18]; notes/sources-186.md, notes/sources-186-forms.md):

  | item | 186 | 182 |
  |------|-----|-----|
  | k | 40 | 39 |
  | grid N | 98304 | 393216 |
  | S | 2742997/2624989 (rho* S = .2742997) | rho* S = .2758746934 |
  | rho*, rho | same | same |
  | trial | 77 coefficients, polynomial radial degree 0..6 in (s - 9/10) | 726 coefficients, 22 cubic B-splines in uncentered s° |
  | cap components | one | three independent components with M0 <= c, c in {141720, 177528, 246256}h, summed before squaring |
  | angular data | g and the 11 signatures | same g and same 11 signatures (reordered) |

  - Domains: 186 had H_O, H_0, H_1 and H_f. 182 has H_O, H_0, H_1 and H_C, where H_C is a new subtraction domain C with
    its own row-14 order-two source ("Subtracting the full available canonical face", Sec. 6.2).
  - Minorant: 186 used Stadlmann's prime minorant rho = P - b with kappa_def = 1/50000, m0 and K_ex = 17/50. 182 uses a
    new sharp five-prime minorant with explicit kappa_true ~ 9.33e-5 and a root-dependent step kernel K <= 2.194. The
    hybrid form is replaced by (6.7) with ell.
  - Analytic input: 182 adds the new incidence Type II and the new Type III estimates (companions [10], [11]) on top of
    the 186 inputs. These change the order-three rows and the new ladder (55 rows).
  - Restoration: in 182 the loss is about 2.11e-4 against a cap surplus of about 2.77e-4. In 186 it was about 6.96e-4
    of I against a surplus above 2.06e-4 (186 Lemma 4.8).
  - Mine: in 182 the restoration loss is ~76% of the cap surplus.
  - 182 has 197 components; 186 had 97.
- **Versus 240 (Stadlmann) and 236 (Song-Yue, Kintali):** those use a Lebesgue-measure capped simplex / mixed support
  with polynomial F and threshold kJ/I > 4 (or > 1 with the minorant scaling). They have no fragment measure, no
  Dickman law and no support-restoration step. 182 shares nothing numerically with them, apart from citing Stadlmann's
  estimates and dispersion targets.

## 7. What a reproduction of the variational step would need

1. **The 726 rational coefficients.** They are only in romyar1/prime-gaps-lean (formal/TrialData182.lean or
   inputs/source_certificates/, three `independent_components` arrays; trial SHA-256 above). This is not yet fetched.
   Reading data files is fine; running their scripts would not be independent.
2. An evaluator for I(F), J0,H, J+,H and E_{H_C^c} (with K) on a 393216-cell grid in 39 coordinates. This is the
   18x-26x-scaled analogue of the 186 contraction pipeline, with these extra pieces:
   - B-spline radial factors: piecewise cubic with jumps at fourfold knots. These replace polynomial powers, so the
     contraction must split at knots.
   - Three cap components, each with its own Dickman cell masses w_c(j).
   - The step kernel K from (5.2)-(5.6), with 1024 bins and 768-index blocks.
   Target: mu- = 9968877639291/2^55 (Mine: 36028797018963968 = 2^55).
3. The restoration loss: 197 source integrals.
   - **Underspecified in the PDF.** The 43 + 55 row tables (omega_prev, omega, delta, order, S, T) are not printed;
     only rows 13 and 14 are given.
   - Low-witness bin windows, Chernoff parameters beta, count prefixes R and the dyadic scale Q are not printed.
   - The exact T0 is not printed (only rho* T0 = .2491228441011).
   - The meaning of "12 shells" is not given.
   - The pairing between component caps and face caps in layers is not spelled out.
   All of these are "in the digital supplement". A cap-only check of mu- is feasible from the PDF plus the
   coefficients and T0. The full criterion needs the supplement.
4. Independent checks possible from the PDF alone: kappa_true by the simplex moment series (4.5)-(4.11) (rational
   vertices, triangulation and volumes are given), the kappa_cvx vertex bound, the tuple's admissibility, and the
   rational arithmetic of (8.3), (10.2)-(10.3) and Sec. 3.7.

## 8. Versions, errata, comments

- Title-page footnote (p. 1), verbatim in substance:
  - Q: "Original version: 4 September 2026. The 11 September 2026 version expanded citations and exposition; the stated
    results and numerical data were unchanged in that revision."
  - Q: "This edition incorporates corrections to the Type III result and adds its formal verification as a derivation
    from explicitly stated general published-theorem hypotheses."
  - Q: "Repository-publication references updated on 3 October 2026."
  - [11] carries the same footnote. [10] says it "accompanies the corrected Type III result".
- So the Type III companion was **corrected** after 11 Sep (by 18 Sep). The PDF does not say what was wrong, or whether
  the numbers (3.3) changed.
- I saw no retraction, erratum list or third-party comment. The UCLA directory has no other file.
- The repo and release (prime-gaps-external-182-verified-20260909.zip, SHA-256
  2960729efa8996538731820ce6cadc202831c8e98b2c0bdb14cfd19f33726f3b, p. 47, joined from two extracted lines, 64 hex
  chars) were not fetched.

## 9. Session 14 follow-up (14 Nov 2026): the top-level Lean file of the 182 development (pasted by Jerry Kim)
Status: **Claimed** (read only; NOT compiled here -- it needs Mathlib and the modules IncidenceRawBlockBound,
SourceIncidenceSecondary182, SourceIncidenceBilinear182 and the rest of the development, none of which we have; this
project uses core Lean without Mathlib). The `#print axioms` output was not supplied; the file's docstring says the
axiom reports are "standard-only" and "certify these conditional theorems, not their hypotheses".
- Endpoint theorems (namespace PrimeGap182), all with the same four hypotheses:
  - `primeGapLiminf_le_182_of_local_inputs : PrimeGap186.primeGapLiminf ≤ (182 : EReal)`;
  - `infinite_integer_translates182_of_local_inputs`: for H : Finset ℤ with H.card = 39 and the usual admissibility
    (for every prime p some residue a mod p misses H), {n : ℤ | 2 ≤ #{h ∈ H : (n + h).toNat prime}} is infinite,
    i.e. DHL[39,2] (negative n + h map to toNat = 0, not prime, so this is harmless);
  - `infinite_consecutive_prime_pairs182_of_local_inputs`: infinitely many primes p with a next prime q, q - p ≤ 182.
- The four hypotheses (docstring, verbatim in substance):
  1. `PhysicalSourceBounds182` -- "the 262 physical numerical inequalities" (the integral inequalities of the
     certificate; cf. Sec. 5 above: 5 cap, 60 outer-root, 60 outer-face, 137 inner-face);
  2. `PublicPrimeLocalBounds182` -- "the two established public prime-local bounds";
  3. `AllIncidenceRankFourBounds` -- "the established rank-four Kloosterman bound";
  4. `LocalFourierHypothesis C D p₀` (some C ≥ 0, D, p₀) -- "the new Type III local Fourier proposition", which the
     docstring calls "still an explicit unproved input. Its manuscript proof has not been completely formalized."
  The docstring adds: "there is no supplied global bilinear, distribution, support, or moment estimate."
- New compared with the bundle's Sec. 13 (as recorded in Sec. 5 above): the new incidence Type II estimate is now
  DERIVED in Lean from hypothesis 3 (`incidenceSecondaryFamily182_of_rank_four` via `incidenceRawBlockFamily_of_rank_four`
  and `incidenceSecondaryEstimate_of_raw`; then `trialOrderThreeBilinear182_of_rank_four`), so per this file it is no
  longer a separate input. The 182 endpoint reuses `PrimeGap186.primeGapLiminf` from the 186 development.
- What this means here: the claimed reduction is formalised conditionally on (1)-(4). (2) and (3) are described as
  established published results (we have not checked their Lean statements against the literature). (4) is new and
  unproved in Lean. (1) is the numerical part, which this project could recompute if it had the 726 trial coefficients
  (formal/TrialData182.lean, still needed: notes/sources-needed.md). We have not compiled or inspected the imported
  modules, so even the conditional theorems are Claimed here, not Lean-checked.
