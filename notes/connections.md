# Connections between the project's results (keep honest; update each run)

The twin prime conjecture is open. Nothing below is a step that is known to lead to it.

## Bound work (main paper, verification note)
- Session 27: the verification note is frozen as v1.0 (per-number account of one-program / two-program / probabilistic results).
- Depends on: the 2026 preprints' analytic inputs (equidistribution estimates; NOT verified by us) and their reductions.
- Feeds into: the reproduced conditional bounds (240, 236; 212 / 186 / 182 variational parts). These are statements about
  DHL[k,2] for k around 39-50, i.e. far from k = 2 (twin primes) and, by the parity barrier, unable to reach below 6 even under GEH.
- Missing for anything bigger: the analytic inputs themselves; and nothing in this line can touch parity.

## Parity-barrier paper (papers/parity-barrier)
- Prop. prop:bipartite / Cor. cor:six: within Liouville-pattern weights, the obstruction blocks exactly H_m < H(2m+1)
  (core = Tao's 2014 blog post "A general parity problem obstruction"; ours: the window form and H_m < H(2m+1)). Depends
  only on the PM8b heuristic framework (the heuristic part is that this class captures what sieves can see).
  Feeds into: a sharp statement of the barrier; the H_m line (the parity limit of this class for H_2 is 12, far below the
  known 270 (EH) / 252 (GEH)); the open question whether weights outside the class block DHL[5,3].
- Prop. prop:tao-weight: confirms the obstruction's input in a weak regime. Prop. prop:tao-weight-logc (Session 19): the same at
  level (log x)^{c0}, conditional on Tao–Teräväinen arXiv:2512.01739v2 Thm 3.1 (unrefereed). Depends on: that preprint, MRT (1.12).
  Feeds into: nothing that lowers a bound; it sharpens how far the obstruction's input is a theorem. Missing to reach the sieve
  level x^theta: (3.4)-type cancellation for moduli far beyond powers of log x (no source). Even then it would only confirm the
  obstruction. Session 19 exploration: extra Liouville coordinates cannot enlarge the weight class (dead end).
- Props. prop:fi-twin, prop:B-parity, Remark rem:fi-transfer: what the asymptotic sieve would need for Lambda(n+2); the bilinear
  estimate is exactly the parity-sensitive missing piece; FI's a^2+b^4 shows which structure made it provable there.
- Prop. prop:ss-split, Remark rem:ss-transfer (bonus run, 15 Nov): written over Z, Sawin-Shusterman's split leaves
  T_D, a mu-Lambda correlation. Unconditionally, twin primes ~ 2C_2 x iff T_D(x) = o(x). A related equivalence is Murty-Vatwani
  Thm 1.1, as quoted (conditional, different quantity). Depends on: BV, or EH for larger D. Feeds into: a sharp statement of what F_q[T] has and Z lacks
  (SS Lemma 3.2: mu on a line is a character). It is a reformulation and gives no progress. Cor. cor:maynard-logc extends
  prop:tao-weight-logc to two-variable weights and, like it, is conditional on TT25.
- Open question 3 answered from the literature: (R_3) at x^{2/3+} is a second hypothesis, logically independent of (B).
  No fixed-residue all-moduli absolute-value level beyond 1/2 is known.
- Sec. sec:ceil (Session 21): Prop. prop:ceil / Cor. cor:ceil: PM8b's three GEH criteria have ratio <= k^2 log k/(k-1)^2, so they
  cannot give DHL[k,3] for k <= 45 (parity blocks only k <= 4); Thm thm:k2: at k = 2 the Thm 3.14 ratio is <= 2 with equality;
  Cor. cor:consistent: criteria and parity class agree on every blocked case. Depends on: PM8b Cor 6.4 and the statements of
  Thms 3.8/3.12/3.14 only. Feeds into: the H_m line (any H_2 <= 12-type result needs a new criterion, not a better F; relevant to
  notes/hm-programme.md); open question 6 (exact k = 3 supremum, heuristically about 2.003 at eps = 1/4). It is a statement about
  the method, not about primes, and is no step toward twin primes.
- Subsec. subsec:mr16 (Session 21): Matomaki-Radziwill read in the source; needs multiplicativity of a single function, so it says
  nothing about lambda(n)lambda(n+2) or Lambda(n+2) directly (Remark rem:mr16-transfer, our reading).
- Missing for twin primes: a bilinear (Type II) estimate for Lambda(n+2)-type sequences, an integer substitute for T_D,
  or any non-sieve input. Not in sight.

### Session 25 addition: the Siegel-zero world (paper sec:siegel)
- Depends on: Tao-Teraeväinen arXiv:2109.06291v2 Cor. 3.6 (read), elementary counting; Heath-Brown 1983 only as quoted.
- Feeds into: the meta-remark rem:meta (the obstruction's hypothesis is Chowla IN PROGRESSIONS; in a Siegel world with few
  small split primes its per-modulus form fails while two-point Chowla holds; the averaged form is not shown to fail);
  open question 8 (a per-modulus unweighted input would constrain Siegel characters; open question 1 as stated is different).
- Missing for anything bigger: control of the small split primes of a Siegel character; and in any case Siegel zeros are
  conjectured not to exist, so this route says nothing about twin primes in the actual world.

### Session 27 addition: Chen's theorem as a consistency test (paper rem:chen)
- Depends on: Prop. bipartite's class of pattern weights; Lean lemmas chen_* (lean/TwinPrimes/Parity.lean); Tao 2007, Tao 2015
  (Supplement 5), Pintz 2010 (notes/sources-chen-parity.md).
- Feeds into: nothing new; it checks that the criterion does not "block" a theorem (Chen), and predicts correctly that each
  parity half (p+2 prime; p+2 exactly two primes) is out of reach of sieve methods alone.
- Missing for anything bigger: the same as before (a parity-breaking input for Lambda(n)Lambda(n+2)). The exploration of this
  run shows the only twists sieve weights cannot see among z^Omega are z = +-1 (Selberg-Delange, 1/Gamma(z) = 0 only at
  non-positive integers), so there is no "mod 3" analogue of the barrier to exploit or to fear.

### Session 28 addition: Gowers norms and infinite complexity (paper subsec:gowers)
- Depends on: Green-Tao, Linear equations in primes (arXiv:math/0606088v2: complexity, generalised von Neumann, Thm 7.2);
  Green-Tao 2012 (MN(s), also for lambda); Tao arXiv:1605.04628 (local Gowers norms, Thm 1.8, Remark 3.4); Tao arXiv:1509.05422.
  Own: Prop. gowers-blind (random block functions; proof audited, notes/audit-parity-v013.md); code/parity/gowers_twin_blocks.py.
- Feeds into: a second, separate barrier next to parity: global Gowers uniformity (all that the finite-complexity theory uses)
  is compatible with any shift-2 correlation and with "fake primes" without twins. Twin primes need information beyond global
  Gowers norms, just as they need information beyond Type I sums.
- Missing for anything bigger: Tao's localisation for lambda (an equivalence of open conjectures; only k = 2 is proved, via
  MRT15) relies on multiplicativity at small primes and on local uniformity at scales H -> infinity slowly; for Lambda neither is available (Lambda - 1 is not locally uniform below
  scale log X). Nothing here moves toward twin primes.

### Session 29 addition: averaging over the shift (paper subsec:mrt17)
- Depends on: MRT17 Thm 1.3 (arXiv:1707.01315v3), MRT15 (abstract), MRT17b (abstract); the folklore window identity.
- Feeds into: a precise map of what is known on average over shifts: the Liouville model of parity is solved for any H -> infinity;
  Lambda Lambda only for H >= X^{8/33+eps}; below that the limit is short-interval distribution of primes, not parity.
- Missing for anything bigger: a prescribed shift. No averaged statement with an unidentified exceptional set reaches h = 2, and
  the fixed-window second moment needs relative precision o(1/log X). Nothing here moves toward twin primes.

## Bound work, rung 182 (Session 19)
- All four ingredients of the 182 cap quotient (I, J0, J+, tail T) now by two programs; q_H - 1 >= mu-. Missing before 182 could
  even be considered reproduced: the restoration losses (197 source integrals, partly underspecified), and the analytic inputs.

- Bonus run (15 Nov): the mass deficit kappa_true of the 182 minorant was recomputed by two independent methods (58 digits);
  the printed bracket and kappa-bar <= kappa_cvx hold. This checks one constant; the restoration losses are still unchecked.
- Session 21: the printed arithmetic of the restoration step (8.3), Sec. 10 totals, (10.2)-(10.3), Secs. 3.7, 13.3 re-done exactly
  (86 checks pass, code/sharifi182_arith.py). The 197 component integrals are not printed, so they cannot be checked from the bundle.

## H_m programme (scoped, not started as a paper; notes/hm-programme.md)
- PM8b Thm 6.7 lower bound reproduced (code/hm/pm8b_mk_lower.py): k = 35410 (MPZ) and 41588 (BV only) match.
- Possible gain from 2026 inputs depends on an admissible (varpi, delta) region nobody has made explicit; modest at best.

- (Session 22) Lemma lem:dual / Prop. prop:overlap / Prop. prop:orth-relax / Prop. prop:k3-step (parity paper v0.7): the
  supremum of PM8b's Thm 3.14 ratio as a projection norm. Depends on nothing analytic (pure variational problem). Feeds into:
  open question 6 (exact k = 3 value; is S_3(eps) > 2 only on an interval of eps?), and the honest statement that H_1 <= 6
  under GEH has little room (Heuristic: sup about 2.003 at eps = 1/4). Missing for anything bigger: everything; this is about
  the variational shadow of the parity obstruction, not about primes.
- (Session 23) Prop. prop:unc-ceiling / Thm. thm:k3-window / Cor. cor:k3-linear (parity paper v0.8): rigorous brackets for
  sigma_3(eps): > 2 at 2/9, 1/4, 7/24; < 2 for eps >= 0.439. Depends on nothing analytic. Feeds into: open question 6; an
  honest statement of how robust "H1 <= 6 under GEH" is within PM8b's Theorem 3.14 (it works only in a narrow eps-window,
  heuristically (0.19, 0.31)). Missing for anything bigger: as before, this is the variational shadow, not primes.
- (Session 24) Section sec:bomb (parity paper v0.9): Prop. prop:bomb-twin (under EH, via Bombieri's theorem as quoted by Ford:
  twin primes <=> the (Lambda*Lambda)-weighted count of p-2 = p1 p2; folklore), Remarks rem:ford-twin, rem:debouzy.
  Depends on: Bombieri's theorem (originals not opened; Ford's quotation) and EH (open). Feeds into: thread 3 of the parity
  paper, the sharpest sourced form of "EH alone does not suffice"; together with Prop. prop:fi-twin it brackets the problem:
  (R) at level > 2/3 plus (B) suffices (FI98 Thm 2); level alone fixes only the prime + P2 total. Missing: any proof of a
  parity-sensitive input for Lambda(n+2) -- (B), Hooley's averaged condition (open question 7), or even Moebius on the
  single shift p-2. Nothing here moves the project closer to twin primes; it locates the gap more precisely.
- (Session 26) Thm. thm:pintz-maynard / Cor. cor:pintz12 / Remark rem:pintz-parity (parity paper v0.11): Pintz's dichotomy
  with Maynard weights; some even 0 < |d| <= 12 has lambda(p+d) = -1 for infinitely many primes (Pintz: 16). Depends on:
  Maynard 2015 Prop. 4.1 (Literature), BV for lambda (Pintz Lemma 3, quoting Vaughan's method), M_5 > 2 (Computed, two
  programs). Feeds into: the parity paper's thesis that the bipartite criterion predicts which parity-sensitive statements
  are reachable (complete graph: reachable; star: blocked). Missing for anything bigger: a single prescribed shift (d = 2)
  is a star target and is blocked; a k = 4 version needs level 0.5423 for primes and lambda (known: 0.525 for smooth moduli).
  This is a sidestep of parity, not a break, and not a step toward twin primes.

### Session 30 addition: hybrid averages (paper rem:lt22)
- Depends on: LT22 (arXiv:2111.08912v3) Thm 1.2, Cor. 1.4, Props 2.1, 2.7, 3.2; an elementary modification argument.
- Feeds into: the open question on the smallest averaging range (sec. open questions) and the Ford / Murty-Vatwani remarks,
  where sum_p mu(p+h) for one fixed shift is exactly the extra condition needed.
- Honest distance: the hybrid case with mu at the averaged position is solved down to (log X)^{1+eps}; below log X both its
  inputs fail. Twin primes need Lambda at both positions at a single shift; no averaging argument of this type applies.
  Nothing here moves toward the conjecture.
- H_m side (notes/hm-programme.md section 6): Stadlmann's MPZ region is bounded by the combinatorial lemma (sigma > 1/10),
  not by the estimates; so H_2 gains from 2026 inputs could only come from hybrid supports, not from MPZ.

### Session 31 addition: Fejér averages and pair correlation (paper rem:gm)
- Depends on: the window identity (rem:mrt17); Goldston-Montgomery as stated in Goldston's notes (arXiv:math/0412313v1,
  Thm 7, (9.3)); Merikoski Main Thm 2 (arXiv:1605.04757v1); Goldston's singular-series formula as quoted in MS04 (47).
- Feeds into: open question oq:mrtcond (partly answered for the Fejér form); the parity paper's thesis that below the mean gap
  averaged statements are empty and that a fixed shift needs a different kind of input.
- Honest distance: under RH + strong pair correlation the Fejér-averaged HL holds down to c log X, but a single shift needs the
  variance at bounded K to o(N), which is equivalent to HL at h = 2 itself. Nothing here moves toward the conjecture; SPC is
  open even under GRH.

### Sessions 32-33 addition: E2 numbers (route cards only; paper v1.0 frozen)
- Depends on: the bipartite criterion (paper sec:bip, the fair version (1) <=> (3), which carries over to sign-pair
  targets); GGPY arXiv:math/0609615, 0803.2636, math/0506067 (read in Session 32).
- Result: in the linear-forms-with-multipliers model, "x, x+d both E2" is blocked in every parametrisation iff 4 does not
  divide d (2-adic colouring); for 4 | d the unblocked systems all contain a prime-pair event at distance d/2.
- Honest distance: this is about a heuristic class of weights, not about what can be proved. For n, n+2 both E2 it says that
  GGPY-type changes of coordinates cannot evade the parity obstruction; it says nothing about twin primes beyond that.

### Session 34 addition: Type II from Gowers norms (Green-Sawhney; route card only)
- Depends on: Green-Sawhney arXiv:2410.04189v3 (Props. 3.4, 4.1-4.5, as stated there); Gowers-norm nesting; FI98 (B).
- Result: the GS hybrid breaks parity for ONE multiplicative (norm-form) prime detector, using additive (Gowers) control of
  the coordinates; a fixed-shift twin condition is either circular (inside a coordinate), without known bilinear structure
  (outer), on a one-dimensional set (conic/line), or carried but not produced (and too weak at GS's precision).
- Honest distance: confirms that twin primes offer neither a second multiplicative structure nor a finite-complexity additive
  one. Nothing here moves toward the conjecture.

### Session 38 addition: odd-order Chowla and a claimed mu-on-shifted-primes theorem (route card + news; paper v1.0.1 status note)
- Odd-order Chowla (Tao–Teräväinen, proved unweighted and log-averaged): even if usable along sieve weights, it removes the
  class obstruction only for non-2-colourable targets; every blocked twin or bounded-gap target is 2-colourable. Distance to
  twins: none gained; within the class the twin obstruction lives in the two-point (even) correlation along the sieve
  weights (unweighted and log-averaged, the two-point input is Tao's 2016 theorem; along the weights it is open).
- Lü–Wang–Wu (arXiv:2610.20242, Claimed): sum_p mu(p+2) = o(pi(x)). If correct, a parity-breaking binary result with a prime
  variable, via multiplicativity of mu at n+2 plus the Type II structure of Lambda(n). Distance to twins: Lambda(n+2)
  has no such multiplicativity; in prop:ss-split the twin asymptotic would still need shift -2, a full log x saving and
  uniformity over e <= x/D. Not verified here.
  Session 39: their Type II step uses the target only through boundedness and multiplicativity at auxiliary primes; if correct, the same estimate would give P^+(p+2) > p^{1-o(1)} infinitely often (EH-strength; route card 2026-11-20-lww-orbit-test.md, one gap). Twins correspond to K = 0, where the mechanism gains nothing: distance to twin primes unchanged. Session 40: the main-term gap of that implication is closed in outline (route card 2026-11-21-lww-main-term.md), so it rests only on their Prop. 4.2 and Prop. 5.3; still nothing for twins (K = 0). Session 49: now Section 6.4 of the parity paper v1.1 (audited again; the Type II statement holds for targets of the form prod V_i^{-1} sum_{a|N} g(N/a) with |g| <= L^C, not for every bounded target). Distance to twins unchanged.
- Large-q function fields (Carmon–Rudnick; Bender–Pollack, Bary-Soroker; Literature): with the degree n fixed and q -> infinity,
  two-point Chowla and twin primes over F_q[x] are theorems, through Pellet's formula (mu as a quadratic character of the
  discriminant) and Weil / Lang–Weil, in a ring whose primes all have norm >= X^{1/n}. Distance to twins over Z: the integer
  counterpart contains the Cesàro two-point Chowla conjecture and, on rough pairs, determines the twin count itself; no
  integer substitute for Pellet is known (route card 2026-11-21-large-q-pellet.md). Nothing for twins over Z.
- Sifting-dimension ladder (Session 43; route card 2026-11-22-dimension-ladder.md; Proved here conditional on EH and the
  beta-sieve theorem as quoted, Computed constants): primes p with every prime factor of p+2 = 1 mod q form a sieve problem
  of dimension (q-2)/(q-1) < 1, solved under EH for each fixed q; the lower constant -> 0 as the dimension -> 1, which is the
  twin case (f_1(2) = 0, parity). Distance to twins: unchanged; the family approaches twins only where its constant vanishes.
- Level ladder (Session 44; route card 2026-11-22-level-ladder.md; Computed thresholds, Literature levels): unconditionally,
  known levels beyond 1/2 do not give any rung kappa > 1/2 through the pure beta-sieve (rung 3 needs 0.6121, known only for
  triply well-factorable weights, which the beta_{2/3}-sieve weights are not). Distance to twins: unchanged.
- Switching on rung 3 (Session 45; route card 2026-11-22-switching-rung3.md; Computed, heuristic main terms checked
  against data): one-step Chen switching at level 1/2 does not reach kappa = 2/3; at a common level theta > 0.5692 for both
  sieves it would (no such level is known for these weights). Distance to twins: unchanged.
- Katai-BSZ orthogonality criterion (Session 46; route card 2026-11-23-katai-bsz-dilation.md; elementary, audited): for
  sum_p lambda(p+2) its necessary input is right-order Hardy-Littlewood for most dilation pairs (p1 m - 2, p2 m - 2), a
  family of twin-prime-type problems. Distance to twins: unchanged (the criterion moves the difficulty, it does not
  reduce it).
- Green / Granville-Shao level beyond 1/2 for multiplicative functions (Session 47; route card
  2026-11-23-granville-shao-level-half.md; literature + elementary, audited): no level-1/2 barrier exists there for a fixed
  residue class; the beyond-1/2 step needs multiplicativity, which lambda(n)lambda(n+2) lacks; a statement valid for all
  bounded completely multiplicative f cannot give the weighted twisted input at any fixed level. Distance to twins: unchanged.
- Merikoski's large-sieve route (Session 48; route card 2026-11-23-merikoski-large-sieve.md; literature + elementary,
  audited): the root large sieve of his Type I argument needs an anisotropic norm form and a free coordinate; n(n+2) is
  a one-point slice of the split form x^2 - y^2, Type I for d | n(n+2) is elementary anyway, and in Z x Z the twin target
  is parity-even. This route does not help; the multiplicative-large-sieve argument GS cite is unpublished. Distance to
  twins: unchanged.
