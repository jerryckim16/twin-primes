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

