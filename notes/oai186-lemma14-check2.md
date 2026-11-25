# Rung 186: second, independent check of Lemma 1.4 of [14]

Source [14]: OpenAI, "Numerical certificate for prime gaps at most 186", 30 Aug 2026,
`code/third_party/openai186/short_gaps_numerics.pdf` (read with `pdftotext -layout`; page 4 also rendered as an
image to resolve (1.13)-(1.15)). Page numbers are the printed ones.

Script: `code/oai186_lemma14_check2.py`, output `code/oai186_lemma14_check2.out`. It uses exact `fractions.Fraction`
only, and no repository code or data: every number is recomputed from the PDF's formulas. Neither
`oai186_support_data.py` nor the JSON tables were used. **1,457,740 checks, 0 failures, about 70 s.**
The script and the output (this note's sections 1-5) were finished before I opened the first program's note.

**Verdict: verified as stated**, under the reading in section 2. The data hypotheses it needs (the caps (1.18) and
the masks (1.5)) are reproduced exactly from the PDF's formulas.

## 1. Statement and definitions used

- p. 9, Lemma 1.4: "After the bounds for the largest fragment and opposite root have been imposed, every retained
  order-three failure is a nonlargest H5/2 failure at the corresponding threshold." The proof cites
  "max(A, C) <= 7L/3" (Lemma 1.1, p. 6) and ends "The imposed caps exclude a largest witness."
- p. 9, (1.34): phi_D(p) = min(3p/2, L), phi_E(p) = 3p - phi_D(p), L = 23C/40 (also on p. 4 after (1.16)).
- p. 1: M_xi(X) = max({p in X: p > xi} u {0}). The inclusive obstruction is
  H_{phi,xi}(X) = max({sum_{q in X, q >= p} q + phi(p) : p in X, p > xi} u {0}).
  p. 4, (1.12): H_{m,xi} has phi(p) = (m-1)p, so H_{5/2} has phi(p) = 3p/2.
- p. 4, (1.13)-(1.16): the constants, the ladders omega, delta (iterated until the first Omega), and
  B, xi, a, b, eta, A, C. (1.17) gives the thresholds. p. 5, (1.18) caps, (1.19) grid rule, (1.20) retained rows,
  (1.21) predicates O_t and I_t. p. 2, (1.3)-(1.5): the grid and masks.
- p. 5, after (1.21): R_0 = H_0 Lold L_1 and R_1 = H_1 L_1. p. 8, (1.30): beta_old is over H0 \ Lold and beta_new
  over H1 \ L1. So new-row inner failures live on H1 (the enlarged caps) and old-row inner failures on H0 (the base
  caps). The outer predicate O_t, for old and new rows, lives on H_O.

## 2. Formalization (where I had to choose)

- "Failure" means the complement of O_t (or I_t) of (1.21) at a root of total s. It needs s > a_t (or s > b_t).
- A witness is p in X with p > xi_t. It is **nonlargest** iff the multiset {q in X : q >= p} has at least 2 elements
  (with multiplicity). So with two equal largest fragments, the witness counts as nonlargest. This matches the
  proof's "a nonlargest witness has inclusive prefix at least 2p" and the convention after (1.12).
  The PDF does not define "nonlargest" for ties. This choice is the natural one.
- "Nonlargest H5/2 failure at the corresponding threshold" means: there is a nonlargest witness p with
  prefix(p) + 3p/2 > A_t (for O_t) or > C_t (for I_t), with the same activation xi_t.
- "Bounds for the largest fragment and opposite root imposed" means that every fragment is at most the cap of the
  domain at that root: (1.18) in the continuous reading, and h*floor(z/h) from the masks (1.5) in the grid reading.
  I check both. The PDF does not say which phrase names which bound. Lemma 1.1's proof says the bounds "are
  A_t - L_t and 63C_t/160", which are the outer and inner order-three caps. My check does not depend on the naming.

## 3. Method, and why it is independent

- **Part A (data).** The script recomputes the ladders exactly and checks the printed facts it relies on: (1.1),
  the ladder lengths 29 and 43, the order counts, the retained rows (1.20), the boundary floors 187773, 188087,
  188254 and 188256 and the pair maxima, (1.17) for every retained row, eta = xi - e/2, A >= C > L > 0, and
  max(A,C) <= 7L/3 for all 19 order-three rows. It regenerates the masks from (1.18)+(1.19) and compares them with
  the printed (1.5). It checks grid inclusion H0 ⊆ H1 ⊆ Hf, and that each mask cap is at most every continuous cap
  its cells can meet.
- **Part B (proof).** A counterexample must lie in one of these regions, for each row t and each predicate:
  - (i) a unique largest witness M, with prefix M, whose phi-term exceeds the threshold, with xi < M <= cap;
  - (ii) the second conjunct fails: phi_E(M) > C (outer) or phi_D(M) > A (inner). M_xi = 0 cannot fail;
  - (iii) a nonlargest witness (variables p and P = prefix >= 2p) whose phi-term fails while its 3p/2-term does
    not.

  If all are empty, the lemma follows. I also test the converse region (H5/2 fails, phi does not) for information.
  min and max are expanded into conjunctions and disjunctions; for example, P + min(3p/2, L) > A means
  (P + 3p/2 > A and P + L > A). This gives a finite union of rational polyhedra with strict and non-strict
  inequalities. Exact Fourier-Motzkin elimination, with strictness tracking, decides each one. There is no slicing
  at p = 2L/3 and no slope argument. In total 304 regions (2 cap modes x 19 rows x 2 predicates on outer or inner
  x 4) were all found empty. The cap used for row t is the largest cap among the shells or mask rows that can carry
  a total s > core: in the grid mode, a mask row j_lo:j_hi qualifies iff (j_hi + d)h > core. FM self-tests: with an
  absurdly large cap, region (i) is nonempty.
- **Part C (brute force on the literal definitions).** For each of the 19 rows and its predicate, the script
  evaluates (1.21) exactly as written: H by its max over witnesses, M_xi, phi_D and phi_E. It does this on every
  multiset of size <= 3, and a deterministic thinning of size 4 (1,457,119 multisets in all). The values come from
  a rational grid on (xi, cap] that contains every critical value ±1e-9 (2L/3, A-L, 21C/40, 63C/160, thr/2,
  thr/3, 2thr/7, ...). For each multiset it tests "failure ⇒ nonlargest H5/2 failure". This is independent of the
  case split in Part B. It found 0 violations, and also 0 converse violations. Negative controls: one fragment
  1e-6 above A-L (outer) or 63C/160 (inner) is a failure with no nonlargest witness, so the caps are what makes
  the lemma true.

## 4. Findings

- Continuous caps: the cap slack is **exactly 0** for rows n24 (outer: z = A_n - L_n) and o24 / n24 (inner:
  z = 63C/160). The largest-witness exclusion is sharp. It holds only because the predicates are non-strict
  (term = threshold is not a failure). FM, with strict failure inequalities, confirms emptiness.
- Grid caps (46580h, 35265h, 35419h) have positive slack of at least 3.4e-6.
- The outer case also needs M <= 21C/40 for the opposite-root conjunct phi_E(M_xi) <= C. With the common outer
  cap A_n - L_n, this holds for the old rows too (C_o < C_n).
- Old order-three cores lie above the start of the outer order-three shell: a_{o,24} - a_{n,24} = 3.57e-3. On the
  grid, the last 49152-cap cell ends at 95638h < a_{o,24}. So no order-three failure meets the larger
  order-two cap. On the inner side, b_{o,24} < b_{n,24}, which is harmless because old rows use the base domain
  (whose cap starts at b_{o,24}) and new rows use H1 ⊇ H0.

## 5. Differences from the PDF's formulation

- The PDF argues with max(A,C) <= 7L/3 and the breakpoint 2L/3. I never use 7L/3 inside the proof (Part A checks
  it separately). Part B decides the same implication directly from the row data and the caps.
- The largest-witness exclusion is one sentence in the PDF. Here it is regions (i) and (ii), checked explicitly,
  including the opposite-root conjunct.
- I enlarge the nonlargest-witness region by dropping P <= s and the caps (P >= 2p only). It is still empty.
- The lemma's downstream use (containment in the groups (1.22)-(1.24): xi_G, U_G, b_G) is not checked here.

## 6. Comparison with the first program (written after section 1-5 and the .out were final)

First program: `code/oai186_lemma14_check.py` and `notes/oai186-lemma14-check.md`, 81 checks, about 17 s,
slope-plus-breakpoint proofs and random tests.

- **Verdict: agree** (verified as stated, no repair needed).
- **Largest-witness exclusion: agree.** Both identify it as the implicit step and both find it correct and sharp.
  Both find that it needs the caps (1.18): A - L for the H_phiD term and 21C/40 for the opposite-root conjunct in
  the outer case (the first note phrases the latter as A <= 11C/10), and 63C/160 for the inner case. The
  negative controls agree (1e-12 there, 1e-6 here).
- **Tie convention: agree.** Equal largest fragments count as nonlargest. The first note adds that ties are
  nu-null.
- **Region facts: agree.** a_{o,24} - a_{n,24} = 3.6e-3. New-row inner failures are charged on H1, with
  H0 ⊆ H1 index by index.
- **Extras in the first program, not in mine:** group containment (1.22)-(1.24), and consistency with the
  upstream and our loss code (task (c) there).
- **Extra in mine:** the exact continuous slack is 0 (sharp), the grid slacks are positive, the converse is also
  verified, and the masks (1.5) are re-derived from (1.18)+(1.19).
- No disagreement found.
