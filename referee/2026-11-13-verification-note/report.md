# Referee report: verification note v0.1 (draft)

**Manuscript:** `papers/verification-note/main.tex`, version 0.1 of 13 November 2026, as on `main` after PR #14. Source SHA-256: `a2841e73818b3a7bdcd52ea0635a642553c1a04838fe33d81029320dd5ed0bc0`.

# Summary

The note recomputes, in exact rational arithmetic, the *variational step* of three 2026 claims on $H_1$:

- Stadlmann's $240$ ($k=49$);
- Kintali's and Song–Yue's $236$ ($k=48$);
- Charton et al.'s $212$ ($k=45$).

It reports the following:

- capped ratios above $4$ for 240, and for 212 with the caps of Table 3 (two independent programs each);
- an exact integer match with Song–Yue's reference values $I_{\mathrm{ref}}$ and $J_{\mathrm{ref}}$ (the capped numerator by one program so far);
- a ball-arithmetic ceiling below $3.99$ for the 212 draft's Lemma 9.1 caps, inside one 846-dimensional space.

It explicitly does not verify the analytic (equidistribution) inputs.

**Coverage.**

- All eight prepared units (front matter, six sections, bibliography) were reviewed in five lanes by two isolated passes.
  - *Correctness and adversarial pass:*
    - rederived Lemma `lem:egf` and Proposition `prop:fibre`;
    - checked every stated number against the stored result files on `main` and on the Session 12 branch;
    - reran `songyue_compare.py` exactly;
    - checked the cap inequalities and the admissible tuples in Python.
  - *Claims, notation and exposition pass:* reviewed the text only.
- The coordinator re-checked the important quotes and claims against `main.tex` and the companion paper.
- **Not done:**
  - Lean was not run;
  - no long computation was rerun (`capped_check`, `capped_exact`, the Gram/ceiling pipeline);
  - no external literature was consulted.
- No model preference was given, so both passes and the reconciliation ran on host defaults.

**Headline:** every number in the note reproduces from the stored files, and no defect undermines a main result. The concerns are about how evidence is stated (normalisation, one-program vs two-program labels, overreach from a space-restricted ceiling) and one hypothesis stated too broadly.

# Main mathematical concerns

None of critical or major severity. The central computations check out:

- the two-program agreements for 240 (both items) and for 212 with the Table 3 caps;
- the 655- and 715-digit equalities with Song–Yue's integers (rerun);
- Kintali's printed values;
- the cap inequalities for all four cap sets (the tightest is Table 3: $324/5000\le328/5000$);
- the fibre proposition for $m\ge1$.

# Other mathematical concerns

**FC1 (moderate, confidence 0.9): two normalisations are mixed in Theorem `thm:sy` and the results table.**
- *The mix:* item (3) states $48J_T/I_0=1.000664921591\ldots>2001/2000$, which is Song–Yue's $t$-scaling with threshold $1$. The same item then gives $48J_T/I_T=4.0030988\ldots$ and $48J_0/I_0=4.0036348\ldots$, which are in the Polymath scaling with threshold $4$.
- *Consequence:* read in one normalisation, these values imply $I_T/I_0\approx0.25$, whereas the files give $0.99989$.
- *The table:* it is headed "Ratios in the Polymath scaling, where the threshold is $4$", but prints $1.00066$.
- *The integer identities:* those in items (1)–(2) hold in Song–Yue's $t$-coordinates (the factor $10^{192}=10^{4\cdot48}$ shows this). With the note's own Section 2 definitions ($u=4t$) they would be off by powers of $4$.
- *Fix:* state the coordinate system for $I_0$ and $J_T$ in Theorem `thm:sy`. Give all three ratios in one scaling, with the other in parentheses. Fix the table row.

**FC3 (moderate, 0.92): the 3.99 ceiling was certified once, not twice.**
- *Note:* "The certificate was obtained twice, at $5000$ and $6500$ bits with different block splits."
- *Companion paper and logs:*
  - the 5000-bit run certified only $\sigma=4$ (and $\sigma=3.985$ failed);
  - $\sigma=3.99$ was certified only in the 6500-bit run;
  - both runs used the same saved weights.
- *Fix:* say that $\sigma=4$ was certified twice and $\sigma=3.99$ once, both from one set of weights.

**FC5 (moderate, 0.8): the hypothesis of Proposition `prop:fibre` is stated too broadly.**
- *Problem:* "If $C_{m+1}\le C_m+g$ for all $m$" fails at $m=0$ for every listed cap set when $C_0=0$, the convention $B_0=0$ of Song–Yue. Also, $C_0$ is never defined. Taken literally, the proposition applies to none of the supports.
- *Why the conclusion survives:* the proof is correct for $m\ge1$. When $m(u')=0$, $u'$ is always admissible.
- *Fix:* set $C_0=0$ and require the inequality for $m\ge1$ only.

**FC6 (minor, 0.85): the Lean attributions say more than the Lean statements prove.**
- "$m\le10$ … for Kintali" bounds the large coordinates of points *in the support*. The correction pieces include non-admissible bases with $m$ up to about $14$; the 126-piece count is right.
- The cap inequalities are Lean-checked only for the Table 3 caps, not for the Lemma 9.1 caps.
- *Fix:* name the Lean theorems and state what each one bounds.

**FC7 (minor, 0.85).** "Smaller than those of Table 3 for every $m\ge4$" should read **every $m\ge1$**: $0.62<0.6216$, $0.62<0.6352$, $0.68<0.70$, and so on. The same slip is in the companion paper.

**FC8 (minor, 0.9).** Rounded values are printed with an ellipsis, so the last digit is wrong:
- $1.000664921591\ldots$ should be $1.0006649215907\ldots$;
- $4.0026596864\ldots$ should be $4.00265968636\ldots$.

Either truncate, or drop the ellipsis and write "≈".

# Exposition and organization

**FC11 (moderate): no dictionary between normalisations.** The sources work in $t$ with threshold $1$ (and Song–Yue with $2001/2000$). The note works in $u=4t$ with threshold $4$. A short paragraph mapping $(A,\varepsilon,\delta,B_m)\mapsto(L,\tau,g,C_m)$ and threshold $1\mapsto4$, at the start of Section 2, would prevent FC1. The one-band form of $J_T$ is labelled Literature but is the note's own reduction; say so.

**FC12 (moderate): three load-bearing steps get one sentence each, with no pointer.** These are the two-radial-variable reduction of the corrections, the method of the second evaluator, and the "dual-weight" ceiling $4.14$. Add a pointer to the relevant sections of the companion paper, or a short appendix.

**FC10 (moderate, notation).**
- *Overloaded symbols:* $U$ is both Song–Yue's radius $521/2000$ and the fibre endpoint. $s$, $t$ and $I$ each have two meanings.
- *Inconsistent names:* the cap-free functionals are written $I,J$ in one place and $I_0,J_0$ in another.
- *Undefined:* the space $V$ and "degree", which Proposition `prop:ceiling` depends on, are never defined. The counts $707/846/1041$ fit "products of $(L-P_1)^a$ and even power sums of total degree $\le D$".

# Claim and scope assessment

**FC2 (moderate, 0.9): evidence levels are stated inconsistently.**
- *The note's own standard:* the Method defines "certified" as two programs agreeing.
- *Where the one-program qualifier is missing:*
  - the label of Theorem `thm:sy`;
  - its row in "Results in brief";
  - the 236 corollary.
  The qualifier appears only in the status paragraph.
- *The corollary overstates:* it says both preprints' criteria hold "for the published witness and for an independent test function". For the independent function, only $kJ_T/I_T>4$ was computed, not Song–Yue's $48J/I_0>2001/2000$.
- *Wrong program:* "agrees with it on the cap-free part" refers to `capped_check.py`, which has no cap-free term. The recorded agreement is between `capped_exact.py` and `songyue_I0/J0.py`, to about 11 digits.
- *Missing provenance:* the $4.14$ ceiling for $k=49$ has no program or method attribution.

**FC4 (moderate, 0.85): overreach from a ceiling restricted to one space.**
- *What the proposition proves:* Proposition `prop:ceiling` bounds the ratio only for $P$ in the 846-dimensional space $V$.
- *What the text says:* the final remark says a change of caps "moves the best attainable ratio below $4$". The text after the proposition says the authors' $4.00438$ "must belong to the caps of Table 3", while admitting their space was checked only by dimension. It also guesses that the Lemma 9.1 values "appear to be left over from an earlier choice".
- *Fix:* say "best ratio in $V$", "is consistent with Table 3", and drop the drafting conjecture, or attribute it to a cited passage of the draft.

**FC13 (minor).**
- The title says "the 2026 bounds"; "the 2026 claimed bounds" is more accurate.
- "All four bounds" counts 236 twice.
- "To every printed digit" (Kintali) should give the digit count and say which normalisation Kintali uses.

# Questions for the authors

1. **(FC9, conditional.)** The companion paper records that Kintali's analytic input is Stadlmann's Proposition 3. If so, does the possible gap in [Sta26, Lemma 5] (Remark `rem:lemma5`) also bear on Kintali's 236, while Song–Yue claim to avoid it through a different route? The note's Introduction says each preprint brings "new equidistribution estimates". Please check Kintali's text and state which 236 argument the remark affects.
2. Is the space of [Cha26, Thm 11.1] the same as $V$, not just of the same dimension? This decides whether FC4 can be strengthened.

# Suggested revisions

1. Fix the normalisation in Theorem `thm:sy` and the results table, and state its coordinates (FC1, with the dictionary of FC11).
2. Add the one-program qualifier everywhere it applies. Restrict the corollary's claim for the independent function. Correct the attribution of the cap-free agreement. Give provenance for $4.14$ (FC2).
3. Correct "certified twice" (FC3).
4. Restrict the overreaching statements to $V$, and drop the drafting conjecture (FC4).
5. Define $C_0=0$ and restrict the fibre hypothesis to $m\ge1$ (FC5).
6. Make the Lean attributions precise (FC6). Fix $m\ge4\to m\ge1$ (FC7) and the ellipses (FC8).
7. Define $V$ and "degree", and split the overloaded symbols (FC10). Add pointers for the compressed steps (FC12).
8. Answer Question 1 and adjust Remark `rem:lemma5` accordingly.
9. Minor framing (FC13).

# Overall assessment

- **Core contribution:** the note is careful and honest about its scope, and its core contribution checks out. Every reported number reproduces from the stored data, the two-program agreements are real, and the exact integer match with Song–Yue's reference values holds.
- **Before sharing:** none of the issues found threatens a result. Several, though, overstate the evidence or mix conventions in ways an expert reader would catch quickly, notably FC1–FC4. They should be fixed before the note is shown to anyone outside the project.
- **Second program:** the one-program status of the 236 capped numerator should stay prominent until `capped_exact.py` finishes.
- **Limits of this review:** it did not run Lean or the long computations, and did not consult the external papers. It does not certify the analytic inputs, the novelty of the work, or correctness beyond what was checked.
