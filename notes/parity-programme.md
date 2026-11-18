# Parity-barrier programme: plan and sources (Phase B, top priority)

Paper: `papers/parity-barrier/main.tex` ("The parity barrier and twin primes: what is known and what is missing").
Attempts: `notes/parity-attempts/` (one route card per run, index in its README).
The twin prime conjecture is open. Nothing in this programme claims to prove it or to break parity for it.

## Sources read (file hashes of the copies read; PDFs not kept)
| key | source | version | SHA-256 | read where / when |
|---|---|---|---|---|
| FI98 | Friedlander–Iwaniec, Asymptotic sieve for primes, Ann. Math. 148 (1998) | arXiv:math/9811186v1 | d39f5249d9003a8a7ce121c93e785dcffa2dfb5ccc9e728820a705826d953d1f | pp. 1041-1046 (hypotheses, Thm 1, Selberg example, twin primes remark), §9 Thm 2, §10 Thm 3; 14 Nov (coordinator) and 15 Nov (Session 17) |
| PM8b | Polymath, Variants of the Selberg sieve... | arXiv:1407.4897v4 | 4085a675d4716db2b22e672d083d4e38262b88b37b8d05b06bcdceb7cb4086a7 | §8 pp. 68-71 (of 80), re-read 15 Nov |
| Tao16 | Tao, The logarithmically averaged Chowla and Elliott conjectures for two-point correlations | arXiv:1509.05422 (current version) | 467329ae414b669808555fddf131be3bc07025777ae3af8ccdea6e98db6722e9 | Thm 1.2, Thm 1.3, Cor 1.5, Remarks 1.4, 1.6, pp. 2-6; 15 Nov |
| Tao07 | Tao, blog "Open question: the parity problem in sieve theory" (2007) | HTML | (14 Nov, see attempt details) | quoted in the 14 Nov route card only; re-read before use in the paper |
| FI98b | Friedlander–Iwaniec, The polynomial X^2+Y^4 captures its primes, Ann. Math. 148 (1998) 945-1040 | arXiv:math/9811185v1 | 7c1ef7c50fe5ac405560c0bf56baea5fd6c014bdc6fc5d248727b96f66cdb07a | Thm 1, Prop 2.1, 3.5, 4.1, (5.2), Lemma 17.1, Prop 17.2, pp. 945-1017 (helper, notes/sources-fi-x2y4.md; key quotes re-checked by the coordinator); 15 Nov (Session 18) |
| PM8b (again) | §8 incl. Remark 8.1 (p. 70), Thm 1.4 (pp. 2-3) | arXiv:1407.4897v4 | same hash | 15 Nov (Session 18) |
| TT25 | Tao–Teräväinen, Quantitative correlations and some problems on prime factors of consecutive integers (preprint) | arXiv:2512.01739v2 | see notes/sources-chowla-quantitative.md | Thm 3.1, Remarks 3.2, pp. 24-25 (re-checked by the coordinator) |
| HR, Pil, Guo, Hughes | Helfgott–Radziwiłł 2103.06853v2; Pilatte 2310.19357v3; Guo 2608.23500; Hughes 2609.28526 | arXiv | notes/sources-chowla-quantitative.md | helper reading only (statements, uniformity ranges); not used in the paper yet |
| TT25 (again) | Thm 3.1, Remarks 3.2, §1.6, §3.2 opening (pp. 9-10, 24-27) | arXiv:2512.01739v2 | ce10e83b10c6544e1dbff037a5e4efa0e387892e0fc596ae09dce76025d7b41e | Session 19 (helper + independent auditor, same hash) |
| MRT15 | Matomäki–Radziwiłł–Tao, An averaged form of Chowla's conjecture, ANT 9 (2015) | arXiv:1503.05121v3 | 8a2633b1594615fe0c340bbca01ad059be5bd66d3495bd028e7e9d2264f1e688 | eq. (1.12), Thm 1.6 (pp. 5-6); Session 19 |
| HB01 | Heath-Brown, Primes represented by x^3+2y^3, Acta Math. 186 (2001) 1-84 | journal scan supplied by Jerry | 96ffd7eb27e724d1ddecd6c738e7261c739c329f02fb222a9c964d0046ec10ae | pp. 2-10, 17-21, 52, 66-69, 72-73, 78-79; Session 19 follow-up (secondary notes by Maynard, X. Li also in notes/sources-hb-x3-2y3.md) |
| MR16 | Matomäki–Radziwiłł, Multiplicative functions in short intervals, Ann. Math. 183 (2016) | arXiv:1501.04585v4 | ec546fdf256b3b3b26b161886c5bab5efb372978ab430c0032e55919f5329277 | Thm 1, Cor 1-6, pp. 1-19, 21-24, 29-31, 36-38 (helper; Thm 1 and Cor 2 re-checked by the coordinator); Session 21 (notes/sources-mr16.md) |
| PM8b (again) | Thms 3.8, 3.12-3.15 (pp. 13-16), Cor 6.4, Prop 6.5, Remark 6.6, M_{2,eps} (pp. 44-46), Sec. 7.4 (pp. 62-68) | arXiv:1407.4897v4 | same hash | Session 21 (coordinator) |
| Li21 | Lichtman, Averages of the Möbius function on shifted primes | arXiv:2009.08969v2 | (14 Nov) | abstract, §1 |

Not opened yet: Bombieri, Le grand crible / The asymptotic sieve (1976); Opera de Cribro (paywalled); Selberg's original parity papers;
Heath-Brown x^3+2y^3 (Acta 2001); Matomäki–Radziwiłł 2016; MRT averaged Chowla;
Tao–Teräväinen; Sawin–Shusterman (arXiv:1808.04001).

## Threads and status (one bounded step per run)
1. Selberg's parity problem / PM8b obstruction: v0.1 Section 2 (Literature, re-read 15 Nov). Next: a Lean check of the finite
   combinatorial fact that omega vanishes on A_1 and on the twin set (trivial; only if it costs nothing); Bombieri's formal statement.
2. Known parity-breaking results: Tao16 Thm 1.2 (Prop. prop:tao-weight), TT25 Thm 3.1 (Prop. prop:tao-weight-logc, v0.3), FI x^2+y^4
   (v0.2). Heath-Brown x^3+2y^3: read in the source (v0.4, Session 19 follow-up). Next: Sawin–Shusterman
   (arXiv:1808.04001) and the step with no integer analogue.
3. Conditional statements: FI98 Thm 2 specialised to Lambda(n+2) (Prop. prop:fi-twin). Next: which hypotheses are known NOT to suffice
   (EH/GEH for sieve methods: PM8b §8).
4. Numerical illustrations: Selberg-weighted lambda(n)lambda(n+2) (Sec. 4, Heuristic).
5. Open questions: Sec. 5.

## Literature-check record
- 15 Nov: one standard web search ("logarithmically averaged Chowla two-point correlation in arithmetic progressions uniform modulus
  ... sieve weights") found no source stating Prop. prop:tao-weight or a uniform-in-modulus version; hence "possibly folklore" stays.

## Session 18 (15 Nov) updates
- Thread 1: new Section sec:bip of the paper (v0.2): exact criterion for which targets a Liouville-pattern weight can block
  (Prop. prop:bipartite, Cor. cor:six); PM8b Remark 8.1 correction (subsec:rem81). Lean: lean/TwinPrimes/Parity.lean.
- Thread 2: FI a^2+b^4 done (subsec:fi-x2y4, Remark rem:fi-transfer). Next: Heath-Brown x^3+2y^3, then Sawin–Shusterman.
- Open question 1: TT25 Thm 3.1 would give level (log x)^{c0} (deduction not written; next candidate step: write and audit it,
  as a strengthening of Prop. prop:tao-weight, labelled conditional on the preprint).
- Next attempt candidates: (a) the deduction above; (b) weights outside the class (residue-class version explored: classwise
  fairness gives nothing new, global fairness is the wrong notion; see notes/explorations.md); (c) the function-field step.

## Bonus run (15 Nov, after Session 19) updates
- Sources read: SS19 arXiv:1808.04001v2 (SHA-256 5b762a0888363d2d1140bb9831a6d940586208f690b4dda3fa6e712337e0a687; notes/sources-sawin-shusterman.md);
  Li21 again (p. 1); Cantarini arXiv:2607.09110v1 (15625c8524d6a89944f085ece4dd75c8ab0d5dc4e04fd98f2ebeb531114afc9c; pp. 1-3, quoting Murty-Vatwani);
  for open question 3 (helper): Polymath8a 1402.0811v3, Maynard 2006.06572v2 / 2006.07088v1 / 2006.08250v1, Lichtman 2211.09641v1 / 2309.08522v1
  (hashes in notes/sources-oq3-level.md). Not opened: Murty-Vatwani (JNT 2017), BFI (Acta 1986); see notes/sources-needed.md.
- Thread 2: Sawin-Shusterman done (paper v0.5, Section sec:ss). Next: Matomaki-Radziwill (2016) or the original Murty-Vatwani.
- Thread 3: Prop. prop:ss-split. Open question 3 answered from the literature (no all-moduli fixed-residue absolute-value result
  beyond x^{1/2}; weighted records 17/32 bilinear and 66/107 well-factorable; none reaches 2/3).
- Open question 5 answered conditionally (Cor. cor:maynard-logc).
- Next attempt candidates: (b') weights that change the twisted main terms (open question 2); (c) an integer structure in
  which "mu restricted to a line is a character" has a substitute (we know none for n -> n+2).


## Session 21 (15 Nov, bonus run started 14:54 UTC) updates
- Thread 2: Matomäki–Radziwiłł read in the source (paper v0.6, subsec:mr16, Remark rem:mr16-transfer). Next in thread 2: MRT averaged
  Chowla in more detail only if needed; otherwise thread 2 is complete for the planned list (FI, HB, Tao, TT, MR, SS).
- Thread 1/3 and this run's attempt: new Section sec:ceil (ceilings for the PM8b GEH criteria; Thm thm:k2: k = 2 exactly at the parity
  value; Cor cor:consistent; Remark rem:pm65 on PM8b Prop 6.5). Route card notes/parity-attempts/2026-11-15-geh-ceilings-k2.md.
- Open question 2 partly answered (DHL[5,3] not by PM8b's GEH criteria); new open question 6 (exact k = 3 supremum).
- Next attempt candidates: (a) a dual certificate for the k = 3 supremum (open question 6; exploration of this run suggests about
  2.003 at eps = 1/4); (b) weights that change the twisted main terms (open question 2); (c) Murty–Vatwani in the original if it arrives.

## Session 22 (15 Nov, back-to-back bonus run 1 of 3) updates
- Attempt (route card 2026-11-15-k3-dual-orthogonal.md): dual formula for the Thm 3.14 supremum; at k = 3 the constraint
  cylinders overlap, so the k = 2 variance argument does not transfer; orthogonal relaxation certified > 2.14 at eps = 1/8 while
  the true sup is ~1.976 (Heuristic). Paper v0.7 subsec:dual. Exact step-function check of PM8b Thm 3.15 (2 + 1.8e-4, two programs).
- LITERATURE CORRECTION: the core of Prop. prop:bipartite is in Tao's blog post "A general parity problem obstruction"
  (21 Nov 2014; notes/sources-tao14b.md), found via Akeno arXiv:2508.02769v3. Credited in v0.7 (Remark rem:tao14b).
  Lesson: blog posts are part of the literature check; search terrytao.wordpress.com for every parity-type statement.
- Next attempt candidates: (a) a rigorous ceiling for S_3(eps) using the overlapping constraints (alternating projections with a
  rate; finite-element dual with error control); (b) does S_3(eps) > 2 hold on an interval? exact arrangement certificates at
  other eps (helper run in progress at the end of Session 22, see the log); (c) weights that change the twisted main terms.

## Session 23 (15 Nov, back-to-back run 2 of 3, same conversation) updates
- Attempt (route card 2026-11-15-k3-window.md): Schur-test reduction to 1D for eps >= 1/4; Theorem thm:k3-window (sigma_3 > 2 at
  2/9, 1/4, 7/24; <= 1.9999 for eps >= 0.439), Cor. cor:k3-linear (scaling). Paper v0.8 subsec:window.
- Literature: PM8b v4 re-read for this (p. 63: their partition works for eps in [1/4, 1/3], 1/4 chosen for simplifications);
  three web searches found no range-of-eps statement.
- Next: rigorous ceiling < 2 for small eps / [0.31, 0.439) needs the marginal condition (overlapping constraints).

## Session 24 (15 Nov, 11:34 AM CT slot) updates
- Sources read: Fo04 Ford, On Bombieri's asymptotic sieve, arXiv:math/0401215v1 (SHA-256 4af579dbe2af84c4539bce0ef4067a97364f68bf83ab53622a40a0baea5b86b3), pp. 1-5;
  De19 Debouzy arXiv:1907.06393v1 (0743fb64c6478419ed5e5bb8c63d7769eadac5b241c3e93c2b39e7bedc887838), pp. 1-3, 36-37 (+ audit read Lemma 2.6, (59), (61), (67));
  Li21 again (7f7421c328f01dcf18565b1840a0d9e66e9f901ee966b414c8bde5f9e49a4456), pp. 1-2, Thm 1.1; FI98 p. 1044 again (same hash).
  Not opened: Bombieri, The asymptotic sieve (1976) and Le grand crible (Asterisque 18): quoted only through Ford.
- Thread 3: new Section sec:bomb (paper v0.9): Prop. prop:bomb-twin, Remarks rem:ford-twin, rem:debouzy; open question 7.
  Thread 3 now covers: FI98 Thm 2 specialised (what suffices with (B)), PM8b sec. 8 (GEH heuristic), Bombieri/Ford (level alone).
- Next attempt candidates: (a) the k = 3 small-eps ceiling (open question 6; review to decide whether to continue);
  (b) Murty-Vatwani in the original if it arrives; (c) the Hooley-type question for twins (open question 7): is there ANY
  structured sequence of the twin type (a_n = Lambda(n+2) times a nice weight) for which the averaged condition is provable?

## Session 28 (17 Nov, 7:34 PM CT slot of 16 Nov) updates
- Sources read (SHA-256 of the copies read; PDFs not kept):
  GT10 Green-Tao, Linear equations in primes, arXiv:math/0606088v2
  (4cc772cfa6f2f9fa2af82d07b6323669c8150ac1911e83a245cc667f956500f5), pp. 1-10, 27 (Def. 1.5, Lemma 1.6, Main Theorem,
  Prop. 7.1, Thm 7.2), p. 68 (parity remark after Thm D.3);
  GT12 Green-Tao, Moebius strongly orthogonal to nilsequences, arXiv:0807.1736v4
  (1983964ece08526e3ceca872c011d1fd6d95d689670e3715bcc6c3a20749d577), abstract, Sec. 1, Sec. 6;
  Tao16 again, arXiv:1509.05422v4 (467329ae414b669808555fddf131be3bc07025777ae3af8ccdea6e98db6722e9), abstract and Sec. 1;
  Tao16b Tao, Equivalence of the log-averaged Chowla and Sarnak conjectures, arXiv:1605.04628v1
  (0ea72ada5def4f1a8abacaa02b67ac3a4f5c9efb5b804fdcac06e69505e0e99d), pp. 1-7, 18.
  Not opened: Green-Tao-Ziegler inverse theorem (quoted through Tao16b and GT12).
- Thread 2/5: new subsection subsec:gowers (paper v0.13): Prop. prop:gowers-blind, Remark rem:gowers. Route card
  notes/parity-attempts/2026-11-17-gowers-infinite-complexity.md. Weekly-review candidate (c) done; (d) MRT averaged
  Hardy-Littlewood over shifts remains.

## Session 29 (17 Nov, 3:34 AM CT slot) updates
- Sources read (SHA-256; PDFs not kept): MRT17 Matomaki-Radziwill-Tao, Correlations of the von Mangoldt and higher divisor
  functions I, arXiv:1707.01315v3 (e93924c5a97b7813320ca84dcbf4619a958b47781e2e7ab36f6e2fd11a9493a1), pp. 1-11;
  MRT17b arXiv:1712.08840 (abstract); MRT15 abstract (arXiv:1503.05121).
- Thread 2/3: new subsection subsec:mrt17 (paper v0.14), Remark rem:mrt17, one open question (conditional ranges). Route card
  notes/parity-attempts/2026-11-17-mrt-averaged-hardy-littlewood.md; audit notes/audit-parity-v014.md. All four weekly-review
  candidates (a)-(d) are now done. Cuts: FI98b and HB01 digests halved. Next attempts: from the open questions of the paper.
- Noted, not read: Lichtman-Teravainen, On the Hardy-Littlewood-Chowla conjecture on average (arXiv:2111.08912; hybrid
  Lambda(n) lambda(n+h) averaged over h, H >= (log X)^{1+eps} per a search snippet) -- a candidate source for a later run.

## Session 30 (17 Nov, 11:34 AM CT slot) updates
- Sources read (SHA-256; PDFs not kept): LT22 Lichtman-Teravainen, On the Hardy-Littlewood-Chowla conjecture on average,
  arXiv:2111.08912v3 (87410676f879ac750cc23e4e0703e073e8b8f459a3cde2d85b6a0c8468464014), read in full (16 pp.).
- Thread 2/3: Remark rem:lt22 (paper v0.15): hybrid averages stop at the mean prime gap (both inputs); Li21 citations
  updated. Route card notes/parity-attempts/2026-11-17-hybrid-averages-mean-gap.md; audit notes/audit-parity-v015.md.
- Referee items 2.6, 2.7 and three section-3 labelling items applied. Still open: notation renames; cuts (sec. num, k = 3).
- Next attempt candidates: conditional ranges for averaged HL under GRH/EH (open question); nothing else from the review list.

## Session 31 (18 Nov) updates
- Sources read: Merikoski arXiv:1605.04757v1 (SHA-256 0a719f3949793b82b7a1bd035d4e2d93e4da95325017bbb903f4284f487efd51; pp. 1-6);
  Goldston arXiv:math/0412313v1 (d4107ba6b463294ffffd409842ee6beae394dc9f80c6dc0e8fc52f9c4615473c; sections 6, 8, 9);
  Montgomery-Soundararajan arXiv:math/0409258v1 (4814387da412faf35d86f7e5d84a789cfa6743b08a6dff1e47fbc7632d7a8176; section 0,
  Thms 2-3, (16), (17), (47)); Keating-Rudnick arXiv:1204.0708v3 (54d6ae76d339aeb3c0af867288021c863bb1b4f3d6816904aac21e496dfc52dd;
  pp. 1-5, exploration only). Abstracts only: Keating-Smith 1903.07057v1, Conrey-Keating 1604.06124v2.
- Thread 3/5: Remark rem:gm (paper v0.16); open question oq:mrtcond partly answered (Fejér form under RH + SPC).
- Next attempt candidates: the almost-all form of MRT17 under GRH or EH (still not found in print); Selberg's RH mean-square
  bound (not opened) would give the Fejér form for K/log^2 N -> infinity.

## Session 32 (18 Nov 2026)
- Parity paper FROZEN as v1.0 (24 pp., from 33): weekly-review cuts and referee items of 16 Nov applied, notation renamed
  (sieve coefficients y_d; pattern functions Psi with signs s_i; k = 2 region T), averaging remarks merged into one subsection
  with two short propositions (prop:lt22, prop:gm), five-lane referee pass referee/2026-11-18-parity-barrier-v1/ (no false
  statement of substance; two wrong-as-written statements, two rounded-up bounds and several lost caveats fixed).
- Attempt: E2 numbers as a parity-even consistency test (route card 2026-11-18-e2-consistency-test.md): consistent. Sources
  GGPY arXiv:math/0609615v1 (SHA-256 411a638e...), 0803.2636v1 (7dc2b242...), math/0506067v1 (e7b065dd...).
- From now on: v1.0 changes only as errata (1.0.x); a v1.1 or short note only for an attempt that proves something not implied.
