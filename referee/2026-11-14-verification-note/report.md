# Referee report: verification note v0.4 (draft)

**Manuscript:** `papers/verification-note/main.tex`, version 0.4 of 13 November 2026, as on `main` after PR #20. Snapshot in this directory (`manifest.json`, `full-source.tex`, `sections/`).

**Earlier review:** the 13 November run on v0.1 (`referee/2026-11-13-verification-note/`). This is a fresh review of the whole of v0.4. Nothing was reused from the earlier run beyond a check, made after each pass had finished, of which earlier findings are resolved.

# Summary

The note recomputes, in exact rational arithmetic, the variational step of three 2026 claims on $H_1$:
- Stadlmann's 240 ($k=49$);
- Kintali's and Song–Yue's 236 ($k=48$);
- Charton et al.'s 212 ($k=45$).

It reports the following:
- capped ratios above 4, each by two independent programs: 240, the 236 witness (and our own $k=48$ function) and 212 with the Table 3 caps;
- exact integer equality with Song–Yue's two reference values;
- a ball-arithmetic ceiling below $3.99$ for the 212 draft's Lemma 9.1 caps, in the 846-dimensional space $V_{21}$.

**Coverage:**
- All nine units were reviewed in five lanes by two isolated passes:
  - V1, correctness and adversarial;
  - V2, claims, notation and exposition.
- **Checks V1 ran:**
  - re-derived Lemma egf and every case of Proposition fibre, including $C_0=0$, $m(u')=0$, non-admissible bases and the endpoints of $\theta$;
  - checked the cap conditions for all four cap sets and the dimensions $707/846/1041$;
  - confirmed exact equality of the two programs' $I_T,J_T$ wherever "two programs" is claimed, and every stated ratio;
  - reproduced both Song–Yue integers;
  - reran the $4.14$ ceiling (337 pieces);
  - checked the positive-definiteness logic and the error bounds in `capped_gram.py`, and the admissibility of the Lean tuples.
- **Checks the coordinator re-ran:**
  - the Kintali digits;
  - the abstract length;
  - the Lemma 9.1 run logs;
  - the Lean statements in `Caps.lean`;
  - the $B_{21}$ definition in the project's source notes;
  - the Song–Yue margin.
- **Not done:** Lean was not built; no long computation was rerun; no external literature was consulted.
- **Models:** no model preference was given; all passes and the reconciliation ran on host defaults.

**Headline:** no error in any result. The mathematics and every number check out against the stored certificates. The concerns are three:
- one stale remark, which contradicts the project's own later audit;
- incomplete evidence labels for the Lemma 9.1 ceiling;
- readiness for archival posting.

Several of these were introduced or left over by the v0.2–v0.4 updates.

# Main mathematical concerns

None of critical or major severity.

# Other mathematical concerns

**FC1 (moderate, 0.9): Remark `rem:lemma5` is stale.**
- *The problem:* it says the note has not checked whether Song–Yue's own analytic proof uses a step like the questioned one in [Sta26, Lemma 5]. The repository's audit (`notes/audit-sy236-thm418/`, merged before v0.4) found no such step. It also found that Song–Yue's eq. (49) is false as printed but repairable, and that the error comes from Polymath8a Lemma 6.25 / Cor. 6.26. The note mentions none of this, and Polymath8a is not in its bibliography.
- *Fix:* summarise the audit with its honest label: one AI auditor per section, not peer review. Keep the analytic input labelled Claimed.

**FC2 (moderate, 0.7): the "analytic + variational" split leaves out the reduction theorems.**
- *The problem:* each bound also rests on a reduction from the variational criterion to $\mathrm{DHL}[k,2]$: [Sta26, Prop. 1], [SY26, §§4.12–4.14] and [Cha26, Thm 4.10]. These are not verified here either. The 236 corollary names only "their equidistribution input".
- *Fix:* name three parts (equidistribution, reduction, variational step) and say which one this note checks.

**FC3 (moderate, 0.8): the Lemma 9.1 ceiling's evidence is under-labelled.**
- *Single program:* the Gram weights come from `capped_check.py` only, checked against it at one random point. The second program's evaluation of that point has not finished (`runs/exact_rand45_lemma91.log` is partial). The ceiling at $3.99$ was certified once.
- *Provenance gaps:*
  - neither run log (`runs/gram45_lemma91_D21.log`, `…_recheck.log`) records the precision or the block split;
  - the research log says 4800 bits for the first run, where the note says 5000;
  - the saved exact weights were loaded from a pickle outside the repository.
- *Where it matters:* none of this is in the abstract, the results table or the proposition's label.
- *Fix:* label the ceiling "Computed, ball arithmetic; weights from one program, randomised cross-check". Commit the weights, or a regeneration command. Fix the bit count, and log precision and split in future runs.

**FC4 (moderate, 0.65): the hedge on the 212 draft's space contradicts the project's own source notes.**
- *The problem:* the note says it has not checked that Charton et al.'s space equals $V_{21}$ "beyond its dimension". But `notes/sources-enlarged-supports.md` quotes their definition, $\mathcal B_{21}=\mathrm{span}\{(L-P_1)^aP_\lambda : \lambda \text{ with even parts}, a+|\lambda|\le21\}$, which is exactly $V_{21}$. The companion paper asserts the equality in one place and denies checking it in another.
- *Fix:* state the equality (Literature, read in the source). The ceiling then bounds every $P$ in the authors' own space, which strengthens the located inconsistency. Keep it framed as an inconsistency for the authors to resolve.

**FC5 (moderate, 0.8): Song–Yue's own criterion has a much thinner margin.**
- *The problem:* Remark "what would change the picture" quotes margins of $0.003$–$0.012$ above $4$. Against Song–Yue's own threshold $2001/2000$, the witness clears by only $1.000664921591-1.0005=1.65\times10^{-4}$, or $6.6\times10^{-4}$ in the Polymath scaling.
- *Fix:* state the margin for each criterion.

**FC6 (moderate, 0.85): the "Lean-checked" counting lemmas are integer-unit arithmetic.**
- *The problem:* `lean/TwinPrimes/Caps.lean` proves its statements for lists of natural numbers in units of $1/1000$, $1/1250$ or $1/2500$, not for real coordinates. The real statements are true by the same one-line bound ($mg<s\le L$), but Lean does not prove them.
- *Coverage gap:* `charton_extra_le_six` assumes the large set carries at least $777$ units, so it does not cover the Lemma 9.1 caps ($C_1=775/1250$).
- *Fix:* label the range facts "Proved here (elementary)", and describe the Lean lemmas as checks of the integer arithmetic.

**FC8 (minor, 0.75): the 4.14 ceiling does not use the bound $u_i\le 0.6$.**
- *The problem:* $\sup_F kJ_T/I_T\le M_{49}(L,\tau)\le4.14$ needs only $T\subset L\R_{49}$, but the text says the bound "depends only on these two facts".
- *Fix:* drop the coordinate bound from the sentence, and give the dual-weight parameters ($a=1.0417$, $s_1=1.0007$).

**FC9 (minor, 0.85): a cited file does not record what it is cited for.**
- *The problem:* the cap-free agreement behind the second program for Theorem `thm:sy` item (1) is cited to `compare2_sy236.json`, which compares only $J_T$. V1 checked that the equality holds, after the coordinate scaling.
- *Fix:* record it in the file, or cite where it was checked.

**FC10 (minor, 0.9): the match with Kintali is understated, and one digit is wrong.**
- *Understated:* the coordinator recomputed $48J_T/I_T$ exactly from `code/cap6/check_sy236.json`: $4.00309880474987377905390044599145775\ldots$. Four times Kintali's printed $1.000774701187468444763475111497864$ is $4.003098804749873779053900445991456$. So the agreement covers **all 33 printed digits**, not 12. The "12" was introduced in v0.2.
- *Wrong digit:* the value printed as $4.0030988047499\ldots$ is rounded but carries an ellipsis. It should read $4.0030988047498\ldots$.

**FC11 (minor, 0.75): the certified vectors are not identified.**
- *The problem:* "cap-free optimiser" is defined as an eigenvector, but the exact values belong to a specific rational approximation.
- *Fix:* say which certificate file holds each vector, and the rounding rule (for example, "400 significant bits").

# Exposition and organization

**FC12 (minor):**
- *Abstract:* it is 2154 characters, above arXiv's 1920 limit, and dense with digits.
- *Version history in the body:* version tags ("Second program (version 0.3)") appear in the text, and the changelog is written for internal readers.
- *Theorem `thm:sy`:* item (3) and its table cell mix two normalisations and two provenances.
- *Labels:* "Computed" is defined as exact but is also used for ball and interval results, and "conditional" is an undeclared label.
- *Notation:*
  - $J$ and $J_T$ both appear in the Song–Yue block;
  - the star notation is defined incompletely;
  - Song–Yue's own $L$ clashes with the note's $L$;
  - $P$, $s$ and $D$ each carry two meanings;
  - $|u'|$ is never defined.

**FC7 (moderate) also concerns exposition: see the next section.** The derivations that the exactness rests on are deferred to the living companion paper: the reduction of the corrections to two radial variables, and the second evaluator. A one-page appendix defining the pieces and regions would make the note self-contained.

# Claim and scope assessment

**FC7 (moderate, 0.8): not ready for archival posting.**
- *Unfrozen references:* the note links a live repository and a living paper with no frozen version. It cites the companion paper as "version 0.9", which is now 0.12, and the section numbers it gives may drift.
- *AI statement:* the AI-assistance statement and the word "independent" understate how the work was produced. Both programs, the Lean files, the text and the internal referee reports were written by AI agents under the author's direction. "Independent" means separate agent contexts without access to each other's code; the statement should say so.
- *Fix:* tag a release (ideally archived with a DOI), cite the tag or commit, expand the statement, and add the appendix above.

**What the note's claims get right:** the analytic inputs are not claimed. Every bound is presented as conditional. The 212 discussion is framed as a located inconsistency, not a refutation.

# Questions for the authors

1. Can the saved Gram weights for the Lemma 9.1 ceiling be committed, or regenerated by a single documented command? And should `capped_exact.py`'s random-point check be finished, so that the ceiling also rests on two programs?
2. Is the first ceiling run 4800 bits or 5000 bits?

# Suggested revisions

1. Update Remark `rem:lemma5` with the audit (FC1). Name the reduction theorems as unverified (FC2).
2. Complete the evidence labels and provenance for the Lemma 9.1 ceiling (FC3).
3. Replace the $V_{21}$ hedge with the source's definition (FC4).
4. State the margin against $2001/2000$ (FC5).
5. Relabel the Lean range facts (FC6).
6. Freeze references, expand the AI statement, and add the appendix (FC7).
7. Make the minor fixes FC8–FC12, including the 33-digit agreement with Kintali and the abstract length.

# Overall assessment

- **Results:** v0.4 is a careful note, and its central results check out. Every two-program claim was confirmed exact, the Song–Yue integers reproduce, and the fibre proposition is now stated and proved correctly.
- **Earlier findings:** most of the 13 November review's findings are resolved: the normalisation, the "certified twice" claim, the hypothesis $m\ge1$, the digits and the wording about the space. Two persist in part: the compressed core reduction and the overloaded $s$.
- **Remaining issues:** none threatens a result. FC1 and FC3–FC5 should be fixed before the note is shown outside the project, because each is the kind of inconsistency an expert would notice. FC7 is a prerequisite for posting.
- **Limits of this review:** it does not certify the analytic inputs, the novelty of the work, or correctness beyond what was checked.
