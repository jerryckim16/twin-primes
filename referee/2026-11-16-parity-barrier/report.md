# Referee report: "The parity barrier and twin primes" (v0.9 draft, 15 Nov 2026)

Fresh-context adversarial referee (helper agent), 16 Nov 2026 (Session 25). Its write to this file was refused (subagent
policy), so the coordinator saved its report here verbatim in substance. Check scripts: `checks/c1.py` (constants),
`checks/k2.py` (k = 2 test), `checks/bip.py` (criterion (c)). The manuscript compiled to 30 pp., with no undefined
references and no overfull boxes.

## 1. Summary and recommendation
A survey with checks: the Polymath8b parity heuristic, Tao's two-point log-Chowla, FI asymptotic sieve with a^2+b^4 and
x^3+2y^3, Bombieri/Ford, Sawin-Shusterman. Own results: twisted Type I inputs for log-averaged weights (bounded level;
(log x)^{c0} conditional on TT25); a window form of Tao's convex-hull criterion; the GEH ceilings (sharp 2 at k = 2, a
certified eps-window at k = 3). No fatal mathematical error. The problems are framing, labelling, stale text and length.
Recommendation: minor revision. Acceptable as a survey once 2-3 and 5 below are fixed and the paper is cut by about a third.

## 2. Mathematical errors and gaps (most severe first)
1. "H_m < H(2m+1)" (abstract, l.455) reads as a proved inequality (for m = 1, H_1 < 6). Cor. cor:six only shows that pattern
   weights block a proof of H_m <= g exactly when g < H(2m+1). "Exact reach" overstates for m >= 2. Fix: say that.
2. Prop. bomb-twin (l.1532) assumes Bombieri's conclusion applies to a_n = Lambda(n+2) with g(2) = 0, but Bombieri's
   conditions were not read. The abstract drops that condition. Also, part (3) is no better than the classical
   Selberg-sieve bound under EH: cite that instead.
3. l.1270-1277 contradict open question 3. They say the fixed-residue literature beyond x^{1/2} is unread, while OQ3
   cites Maynard and Lichtman as read.
4. Prop. tao-weight-logc, l.313-314: "as kappa < 1" holds only because TT25 lets c be "sufficiently small absolute"
   (TT25 p.24); say so. The (log R+1)^8 and R^{2+o(1)} factors are absorbed into o(1) exponents only because
   R <= (log x)^{c0}; state this (same for (log R+1)^{17} in Cor. maynard-logc). The rest of the proof checks.
5. Remark ss-transfer, bullet 1: the needed o(x) is stronger than o(x log x) by exactly a factor log x, not "more than".
6. Remark k3-eps: the extrapolated sigma_3(1/8) ~ 1.976 does not exceed the rigorous lower bound 1.97619. The eps = 1/4
   values are still rising, so "max about 2.003" and the window (0.19, 0.31) may be too low (Heuristic; minor).
7. l.627-631: a hand scaling/LP-rationality argument sits under a Lean-checked label.
Checked and correct: Prop. bipartite (incl. (2)=>(1); LP test of (c) on 400 random tuples: 0 mismatches); Cor. six; Thm k2
(non-symmetric step-function eigenproblems gave 2.000000 for n = 8-20, eps in 0.1-0.75); Lemma dual (1)-(3);
Prop. overlap; the clean columns; Prop. unc-ceiling (needs eps >= 1/4); Cor. k3-linear; Prop./Cor. ceil (46, 392, 2965,
22007; c(5), 4.152, 4.091, 2.159); Props fi-twin, B-parity(3), ss-split, bomb-twin; the -(1+2 gamma_0)x term; the
Remark 8.1 weight (nonzero for H = 3, identically zero for H in {4,6,8,12}, n < 20100); Remark pm65 against PM8b pp. 44-45.

## 3. Labelling
- The labels paragraph defines only 4 of the 7 labels.
- Thm k3-window(2) rests on Prop. unc-ceiling, so it should be "Proved here + Computed".
- Remark ss-transfer contains our own unlabelled claims.
- Prop. bomb-twin is called "folklore" with no reference. Prop. ss-split says "compare MV17", but MV17 was not opened.
- Unlocated literature: H_1 <= 246 (PM8b Thm 1.4(i), p.2); H_1 <= 6 under GEH (Thm 1.4(xii), p.3); the exact formula for
  M_{2,eps} (PM8b pp.45-46); BV, Brun-Titchmarsh and Mertens without citations; H(3..9) (compare OEIS A008407).
- Bombieri's theorem is known via Ford only: mark it "Literature (secondary)".

## 4. Literature spot-checks (all matched)
- PM8b arXiv:1407.4897v4: Thm 1.4 (i), (vii), (xii), (xiii); the sec. 8 opening (p.68); Remark 8.1 (p.70, product over
  0 <= i <= i' <= H); Thm 3.14 (p.16); Prop. 6.5 (p.44).
- Tao16 arXiv:1509.05422v4: Thm 1.2 (p.2); the parity quotes (pp.3, 5); Remark 1.4 "in principle effective".
- FI98 arXiv:math/9811186v1: the hypotheses on pp.1041-1044; Thm 2 (p.1059); the quotes on pp.1045-1046.
- TT25 arXiv:2512.01739v2, Thm 3.1 (p.24): consistent with kappa = c/4 and L = (log X)^{1/4}.

## 5. Padding
- Prop. tao-weight: a two-line corollary of Tao's Thm 1.2, superseded by tao-weight-logc; make it a remark.
- Cor. maynard-logc: a routine variant; a remark of about 5 lines.
- Prop. B-parity (1)-(2): one-liners. Prop. fi-twin: shorten.
- Prop. bomb-twin and Prop. ss-split: about 5 lines each.
- Prop. ceil: merge it with Cor. consistent.
- sec. 4.4 (Lemma dual, Prop. overlap, clean columns, orth-relax): cut to one paragraph plus orth-relax.
- Prop. k3-step: duplicates Thm k3-window(1) at eps = 1/4; delete.
- Remark pm65: move to a footnote.
- The FI98b / HB01 / SS19 / MR16 digests (about 4 pp.): halve.
- Merge Remarks k3-eps and k3-window.
- Worth keeping: Thm k2; unc-ceiling with k3-window and k3-linear; criterion (c) with Cor. six; the Remark 8.1
  correction; the Debouzy constant.

## 6. Readability
- Abstract: about 171 words, but it is a dense list.
- History in the main text: l.66, 229-231, 330 (a version tag), 453, 699, 820, 993, 1138, 1618.
- Stale material: the "Plan for later versions"; open question 5 still listed; the changelog puts 0.9 before 0.8.
- Section 4 is about a third of the body. MR16 is misplaced. GEH, EH and DHL are used before they are defined.
- Notation clashes: lambda (Liouville / lambda_d), omega, Omega, eps, Delta, kappa, c, H, D, M. At least rename lambda_d,
  the pattern Omega and the region D.
- All cross-references resolve.

## Response (Session 25, coordinator), applied in v0.10
- Applied: 2.1 (abstract and sec:bip wording), 2.2 (abstract states the condition), 2.3 (stale lines replaced by a pointer
  to OQ3), all history items of sec. 6 in the main text except l.1618 (Debouzy remark, kept as a statement of what was
  checked), the labels paragraph (all 7 labels), the changelog order, and the "Plan for later versions".
- Deferred to the weekly review (16 Nov, Monday run), since they are restructuring decisions: the cuts of sec. 5 (incl.
  deleting Prop. k3-step, which is cross-referenced), the notation renames, items 2.4-2.7, the sec. 3 labelling items
  other than the labels paragraph, and moving MR16.
