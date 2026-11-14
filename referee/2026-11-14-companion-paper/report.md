# Referee report: companion paper v0.12

**Manuscript:** `paper/main.tex`, "Toward the twin prime conjecture: certificates, limits of the sieve, and a working programme", version 0.12 of 13 November 2026, as on `main` after PR #20. Snapshot in this directory.

**Note on a later branch:** Session 14's branch (not yet merged) adds a remark on the Song–Yue audit. It may resolve FC1 below; this report reviews v0.12 as merged.

# Summary

The paper has three parts:
1. **Reproductions** of the Maynard–Polymath sieve constants with exact certificates, and Lean-checked admissible tuples (§§1–3).
2. **Results of its own:**
   - rigidity of the pigeonhole step (§4);
   - floors for the $\varepsilon$-enlarged simplex by dual weights, including a certified floor for $k\le29$ (§5);
   - a floor for one-band hybrid supports;
   - one-sided Bonferroni certificates.
3. **Exact recomputation of the variational step** of the 2026 claims 240, 236 and 212, with ball-arithmetic ceilings, and the first sub-step on rung 186 (§6). It ends with a programme (§7).

**Coverage:**
- **Five isolated passes:**
  - P1: correctness and adversarial, §§1–4;
  - P2: correctness and adversarial, §5;
  - P3: correctness and adversarial, §6 lines 1–368;
  - P4: correctness and adversarial, §6 lines 369–849;
  - P5: claims, notation and exposition, whole paper.
- **What the passes checked:**
  - **Proofs re-derived:** Lemma egf; the rigidity propositions; Lemma dual, Prop eps-first and the floor inequality; Props caps and exact; the Bonferroni proposition.
  - **Certificates rerun:**
    - the $k=29$ floor certificate (857 intervals);
    - `verify_cert.py` on three certificates;
    - both dual ceilings (337 and 495 pieces);
    - the hybrid-floor certificates;
    - the small-$k$ and $k=12$ two-program tests.
  - **Two programs compared:** exact equality checked at $k=49$, $k=45$ and $k=48$.
  - **Song–Yue identities:** recomputed.
  - **Lean names and tuples:** every cited Lean theorem exists, and all 65 tuples are admissible.
- **The coordinator independently re-checked:**
  - the dual-weight remark (FC3), by rerunning the code;
  - two certified bounds (FC10);
  - the $V_{21}=\mathcal B_{21}$ source note (FC4);
  - the $g\ge L-\tau$ margins (FC6).
- **Not done:**
  - Lean build and axiom audit;
  - the degree-25/27 rebuilds and long exact runs;
  - external literature (no internet in the passes);
  - `cw_sample` at $(50,1/25)$, which timed out.
- **Models:** host defaults; no model preference was given.

**Headline:** no result in the paper is wrong in a way that changes a bound or a certified inequality. Every two-program claim, every certificate the passes reran, and every number in the abstract checks out. There is **one genuine mathematical error, in a negative remark** (FC3): a dual weight the paper dismisses was not tested in the range where it does best. Beyond that, the concerns are four:
- an unstated hypothesis (FC6);
- certified bounds printed rounded *up* (FC10);
- a few overclaims (FC5, FC7, FC8);
- a label system that is not applied as defined (FC9).

The paper also needs substantial reorganisation (FC12).

# Main mathematical concerns

None of critical or major severity.

# Other mathematical concerns

**FC3 (moderate, 0.85): the remark "a weight that did not work" is wrong.**
- *What the paper says:* the weight $\psi_m=(\beta/n)(a-S_A+nt_m)$ "cannot give less than $4.178$" at $(50,1/25)$, which is worse than the scaling bound $4.1515$. It says this supersedes an earlier $4.146$.
- *Why it is wrong:* `code/dual_eps.py` scans only $a\ge L+0.01=1.05$, and its optimum sits at that edge. The weight is admissible for every $a>\tau$.
- *Rerun of the same fibre code:*

  | $a$ | 1.03 | **1.037** | 1.04 | 1.05 |
  |---|---|---|---|---|
  | bound | 4.16437 | **4.14633** (binding fibre $r=10$) | 4.15020 | 4.17821 |

- *Consequence:* the test gives about $4.1463$, below the scaling bound, and it reproduces the earlier "superseded" value. Since this is only a lower bound for what the weight achieves, whether it beats scaling is **open**, not ruled out.
- *Fix:* withdraw the remark, or restate it with the corrected range and its status as open.

**FC6 (moderate, 0.85): an unstated hypothesis in Proposition `prop:exact`.**
- *The problem:* the region list in the proposition, and `capped_exact.py`, use $g\ge L-\tau$, but the statement does not assume it. Only `capped_check.py` asserts it.
- *Why no result is affected:* every parameter set satisfies it. Stadlmann and Kintali have $L-\tau=0.06$ against $g=0.112$ and $0.0728$; Charton et al. have $0.064$ against $0.0656$, a narrow margin.
- *Fix:* state the hypothesis, and add the assertion to `capped_exact.py`.

**FC10 (minor, 0.95): certified lower bounds are printed rounded up.**
- *Example:* the certificates give $M_{50,1/25}\ge4.00124659\ldots$ and $\ge4.00430625\ldots$ (coordinator: `code/cert_M50e25_D25e.json`, `…D27e.json`). Theorem `thm:Meps` prints $4.0012466$ and $4.0043063$.
- *Other instances:* $M_{49,15/506}\ge3.9685535$ against the certified $3.96855349\ldots$; the lower end $3.98555$ of the Lemma 9.1 optimum interval (attained value $3.9855478$); entries in Table `tab:eps`, the $\varepsilon$ $k=3$ table and the $\theta$ table.
- *Effect:* no conclusion about 4 changes, but a printed lower bound must not exceed what is certified.
- *Fix:* truncate.

**FC4 (moderate, 0.85): the paper both asserts and disclaims $V_{21}=\mathcal B_{21}$.**
- *The problem:* §6 asserts at lines 55–58 that our 846-dimensional space is Charton et al.'s $\mathcal B_{21}$, and says at lines 478–483 that this was never checked. The project's notes quote their definition (`notes/sources-enlarged-supports.md` l.251), which is exactly $V_{21}$.
- *Fix:* keep the assertion (Literature) and delete the disclaimer. The Lemma 9.1 ceiling then applies to the authors' own space.

**FC5 (moderate, 0.9): the 212 overreach in the Programme and in `status.json`.**
- *Overreach:* both say the draft's $4.00438$ "must belong" to the Table 3 caps; the body is more careful.
- *Missing labels:* the $3.99$ ceiling's label omits three things:
  - it rests on one program's Gram weights;
  - it was checked by a randomised (Schwartz–Zippel) test;
  - it was certified once at $3.99$.
- *Not archived:* the exact weights used were loaded from a pickle outside the repository.
- *Fix:* match the body's wording, complete the label, and commit the weights or a regeneration command.

**FC7 (moderate, 0.85): "Corollary `cor:578` is the best that the plain simplex gives with BV" is unsupported.**
- *The problem:* the cited upper bound only excludes $k\le50$, so $k=51,52,53$ remain open. The paper itself says "$k\ge51$" elsewhere.
- *Fix:* qualify the sentence.

**FC8 (moderate, 0.8): the abstract overstates the evidence from Proposition `prop:family`.**
- *Overstatement:* the abstract presents numerical evidence that the $k\le29$ floor is near the limit of all $(t_m,S)$-weights. But in the relevant regime, $(30,1/4)$, the paper draws no conclusion.
- *Weak supporting claim (confidence 0.55):* the discretisation is neither a restriction nor a relaxation of the family. Even at $(50,1/25)$, "no such weight goes much below 4.14" is therefore heuristic.
- *Fix:* label both as heuristic.

**FC9 (moderate, 0.85): the label system is not applied as defined.**
- *Wrong labels:*
  - "Literature" is used for unrefereed 2026 preprints, which should be Claimed or "Literature (preprint)";
  - "Computed" is used for floating-point output, including a solver called "exact" that is the floating-point Clarabel, with "Solution may be inaccurate" warnings in the logs;
  - Proposition `prop:adjoint` is labelled "Proved here" but describes program internals, with no proof.
- *Missing labels:* Corollaries `cor:578` and `cor:246` and Lemma `lem:egf` have none, though the abstract promises every statement carries one.
- *Lean overstated:*
  - the "Lean-checked" counting facts are integer-unit arithmetic over lists of natural numbers, not the real statements used;
  - `kintali_extra_le_three` covers the cap-violation pieces, not the Corr₂ pieces it is cited for.
- *Fix:* apply the definitions as written, add the missing labels, and describe the Lean lemmas accurately.

**FC1 (moderate, 0.8): the remark on [Sta26, Lemma 5] says "the bounds 240 and 236 depend on this input".**
- *The problem:* the paper's own route to 236 goes through Song–Yue's Theorem 4.18, and the audit in `notes/audit-sy236-thm418/` found no swapped-factor step there. It found a different, repairable error, in their eq. (49), which comes from Polymath8a Lemma 6.25. The verification note fixed the corresponding sentence in v0.2.
- *Fix:* update the remark; Session 14's branch may already do so.

**FC2 (moderate, 0.75): the caveats on 240 and 236 name only the equidistribution input.**
- *The problem:* the reduction theorems ([Sta26, Prop. 1]; [SY26, Thm 4.33, §§4.12–4.14]) are also unverified. If the audit is folded in, these could silently drop out of the caveat.
- *Fix:* name them.

**FC11 (minor): numerical and provenance slips.** These were found by the passes and are listed in `reconciliation.json`; each is small.
- *Quoted values:*
  - $M_{50,1/25}\ge4.0012$ is quoted where the cited theorem gives $4.0043$;
  - "372,450" Dickman cells should be 363,450, and the maximal width is $8.35\times10^{-10}$;
  - the $j=3$ pieces took 47% of the time, not "most";
  - the stopped run had finished 153 pieces, not 138.
- *Timing:* "15.5 core-hours, about 2.1 hours on four cores" is inconsistent, since 2.1 hours is only the resumed segment.
- *Wrong reasoning or explanations:*
  - the thin-bound paragraph mixes two polynomials;
  - the "second-order" model predicts a gain of about 0.033, below the 0.0386 loss, not above it;
  - the Lemma 9.1 caps are below Table 3's for every $m\ge1$, not $m\ge4$;
  - "their caps start lower" is false in every normalisation;
  - the remark "how sharp" cites Prop `capfree` on the wrong side.
- *Missing artifacts:* $M_{105}\ge4.17427$ (reproduced by P1 as $4.174272850696$), the $k=50$, $D=16$ column, two Prop `family` values, and the degree-8 `capped_exact` run have no committed files.
- *Unstated parameters:* the $k=3$ remarks do not state their shifts or $D$.
- *Stale text:* "(not done yet)" and "(Open)" in the v0.6–0.7 text.
- *Programme and status:*
  - "39→38" is not uniquely the most valuable step;
  - the Programme's one-band dual certificate cannot "locate 182";
  - a "Rules" sentence refers to a nonexistent column;
  - `status.json` has a stale Kintali entry and stale theorem numbers.

# Exposition and organization

**FC12 (moderate):**
- *Abstract:* it is a single sentence of about 45 lines, mixing a dozen results, reproductions, caveats and version history.
- *Version narration:* "version 0.6", "v0.8" and the like appear in section headings and in the mathematics, and superseded results are kept as numbered propositions. The title of §6 ("versions 0.5–0.9") is out of date.
- *Buried results:* the paper's own main results (the hybrid floor and the Bonferroni proposition) sit at the end of a half-paper §6 that interleaves four claimed bounds.
- *Programme section:* it is mostly a status recap and a reading list, and "Track B" is not a well-posed problem.
- *Notation:*
  - $I,J$ denote the capped functionals ($t$-scale), the cap-free ones ($u$-scale) and Song–Yue's numerator in successive paragraphs;
  - the scaling drifts, and one display gives the same ratio in two scalings;
  - $U,s,V,P,R,F,M,\sigma$ each carry two or three meanings in §6;
  - $n$, $M_T$, $J^{(m)}_{k,\varepsilon}$ and $C$ are undefined or defined late;
  - several by-name references point to the wrong place.

**Suggested shape for a version 1.0:**
- **§1:** the problem, and three numbers.
- **§2:** methods (exact moments, the two evaluators, Gram ceilings, Bonferroni).
- **§3:** reproductions (246, 240, 236, 212), with one table.
- **§4:** own results (rigidity, floors, the hybrid floor), each a theorem with a label.
- **§5:** open problems.
- **Appendix:** history and changelog.

# Claim and scope assessment

**What holds:**
- The three numbers are consistent across the paper, README.md, status.json and the bound history: established 246, claimed 182, reproduced 236 and 240 (conditional) and 246.
- Every mention of 236 and 240 carries a "not verified" caveat.
- Statements about the parity barrier are accurate.
- The project does not claim progress on the twin prime conjecture itself, although the title "Toward the twin prime conjecture" frames it that way (minor).

**What needs fixing:** FC1, FC2, FC5, FC7 and FC8.

# Questions for the authors

1. Re FC3: should the remark be withdrawn, or should the weight be certified properly near $a\approx1.037$? If its true value is below 4.1515, it would improve the paper's scaling bound at $(50,1/25)$.
2. Can the Lemma 9.1 Gram weights be committed, and should the second program's random-point check be completed?
3. Should the "exact convex solver" results be relabelled as floating point, or re-solved with a certified solver?

# Suggested revisions

1. Fix FC3: the weight remark, with the corrected range and open status.
2. State $g\ge L-\tau$ (FC6).
3. Truncate every certified bound (FC10).
4. Resolve $V_{21}=\mathcal B_{21}$ (FC4).
5. Complete the ceiling's label, and soften "must belong" (FC5).
6. Qualify the "best the plain simplex gives" claim (FC7) and the abstract's heuristic claims (FC8).
7. Apply the label system as defined (FC9).
8. Update the Lemma 5 remark, and name the reduction theorems as unverified (FC1, FC2).
9. Make the minor fixes in FC11.
10. Reorganise along FC12 before any outside circulation.

# Overall assessment

- **Results:** the computational core is solid. Every exact certificate and two-program agreement the passes reran holds, and the proofs re-derived are correct.
- **The one mathematical error:** it is in a negative remark (FC3). Correcting it reopens a possible improvement rather than undoing a result.
- **Remaining issues:** none threatens a stated bound. Several overstate the evidence or blur labels, and an expert would notice them: FC5, FC7, FC8 and FC9.
- **Form:** the paper reads as a lab notebook rather than a paper. For anyone outside the project, it needs the reorganisation in FC12 more than any further result.
- **Limits of this review:** it does not certify the analytic inputs, novelty, or correctness beyond what was checked; Lean was not built and no long computation was rerun.
