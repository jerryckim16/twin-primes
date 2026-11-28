# Fresh-context audit: Lean note v1.2 (thm:s2y and related) and main-paper sentences of 28 Nov 2026

Scope: `papers/lean-reduction/main.tex` v1.2 (subsection "The change of variables in the main term",
Theorem thm:s2y, the remark after it, abstract, Hypothesis hyp:s2, "Reproducing the checks", Appendix A item 1.2);
`paper/main.tex` Theorem thm:lean item 22, Remark rem:186-status (the "directed (outward-rounded)" sentences), and
Section sec:related ("Cards of 27 November"). No .tex file was edited. Nothing was committed. `lake` was not run.

Sources checked:
- `lean/TwinPrimes/MaynardS2Y.lean` (510 lines) and `lean/TwinPrimes/MaynardS2Mult.lean` (501 lines), read in full;
  `lean/Audit.lean`; `notes/lean-s2-y.md`, `notes/lean-s2-mult.md`.
- Maynard, arXiv:1311.4600v3. Fetched with curl into the new empty directory /tmp/claude-0/may/ and read with
  pdftotext -layout, pp. 10-13. SHA-256 dce1a7a0...d63cda9, which matches the bibitem.
- `notes/oai186-directed-check.md`, `notes/oai186-lemma11-analytic.md`.
- `notes/parity-attempts/2026-11-27-lww-{prop43,p23-27-reduction,s48-second-sum}.md` and the list of LWW audit
  files.
- `wc -l` on `lean/TwinPrimes/*.lean`, and a count of `#print axioms` lines in `Audit.lean`.

Tally: 1 error, 2 gaps, 3 overstatements, 6 slips, 2 style. The other checked parts have no finding (see the end).

## Findings

**1. error: thm:s2y(4), where the indicator sits.** The paper puts the indicator on the wrong side.
- The Lean conclusion of `maynard_S2_lam_of_y_odd` / `_W` is
  `tmu d * tphi d * upSum (y/tg) d = if d_m = 1 then λ_d else 0`. In words: ∏μφ·Σ = 1[d_m=1]·λ_d.
- The text says λ_d = 1[d_m=1]·∏μφ·Σ. For d_m ≠ 1 that asserts λ_d = 0, which is false for general λ. λ_d with
  d_m ≠ 1 is arbitrary and does not enter y^(m).
- Text: `then
  $\lambda_d=\mathbf 1[d_m=1]\prod_i\mu(d_i)\varphi(d_i)\sum_{d\mid r}y^{(m)}_r/\prod_ig(r_i)$
  for every $d$ in the box.`
- Replace with: `then
  $\prod_i\mu(d_i)\varphi(d_i)\sum_{d\mid r}y^{(m)}_r/\prod_ig(r_i)=\mathbf 1[d_m=1]\,\lambda_d$
  for every $d$ in the box (so $\lambda$ is recovered on $d_m=1$, and the right side vanishes for $d_m\ne1$).`

**2. overstatement: paper/main.tex, thm:lean item 22. This is the same issue as #1.**
- Text: `and, for odd entries, $\lambda$ is recovered from $y^{(m)}$`.
- Replace with: `and, for odd entries, $\lambda_d$ is recovered from $y^{(m)}$ for every $d$ with $d_m=1$`.

**3. gap: thm:s2y does not say that λ is rational.**
- All Lean statements are over `Rat`. Line 142 says this explicitly for thm:diag ("items (1)-(3) of
  Theorem thm:diag take rational ones"). thm:s2y does not say it, although Maynard's λ are real and hyp:glue names the
  real→rational passage.
- Text: `Let $\lambda$ be supported on the box $\{1,\dots,R\}^k$ with squarefree entries, and fix $m$.`
- Replace with: `Let $\lambda$ be rational-valued and supported on the box $\{1,\dots,R\}^k$ with squarefree entries,
  and fix $m$.` (In Lean, "supported" means: λ_d ≠ 0 at a box point implies squarefree entries. The sums run over the
  box only.)

**4. slip: Maynard's identity (5.21) is quoted without its condition.**
- Maynard writes it "valid for square-free d_i, e_i" (p. 11). With a totally multiplicative g it is false otherwise:
  for d = e = 4 the left side is 1/2 and the right side is 1/4.
- Text: `Maynard diagonalises it with
  $\varphi([d,e])^{-1}=\varphi(d)^{-1}\varphi(e)^{-1}\sum_{u\mid d,\,u\mid e}g(u)$,`
- Replace with: `Maynard diagonalises it with
  $\varphi([d,e])^{-1}=\varphi(d)^{-1}\varphi(e)^{-1}\sum_{u\mid d,\,u\mid e}g(u)$ (for squarefree $d,e$),`
- Optional addition: with g = μ*φ the identity holds for all d, e (`gM_divisor_sum` together with
  `totient_lcm_mul_gcd`). That is one more reason for the Lean definition.

**5. slip: the equations cited for the s_{i,j} step.**
- Maynard introduces the s_{i,j} in the text just before (5.21) and writes them in (5.22). (5.24) is the main term after
  substitution, and (5.25) is the bound for s_{i,j} ≠ 1.
- Text: `he removes the restriction with variables $s_{i,j}$ and bounds the terms with $s_{i,j}\ne1$
  \cite[(5.24)--(5.25)]{May15}`
- Replace with: `he encodes the restriction with M\"obius variables $s_{i,j}$ and bounds the terms with
  $s_{i,j}\ne1$ \cite[(5.22), (5.24)--(5.25)]{May15}`.
- "Removes" is also loose. The restriction is written as a Möbius sum, and the s ≠ 1 part is then estimated with an
  O(.../D_0) error, not removed exactly.

**6. slip: "so it agrees with Maynard's g on every squarefree argument".**
- This follows by induction from `gM_prime` and `gM_mul_coprime_sqf`. It is not a stated Lean theorem.
- The phrase "the only ones that occur" is right in effect, not literally. The u-sums of (3) and (4) run over all u in
  the box, including non-squarefree u, where g = μ*φ ≠ Maynard's g (`gM 4 = 1`, `gM 9 = 4`). Those terms vanish only
  because y^(m)_u carries the factor μ(u).
- Text: `so it agrees with Maynard's $g$ on every squarefree argument, the only ones that occur.`
- Replace with: `so (by induction, not stated as a separate Lean theorem) it agrees with Maynard's $g$ on every
  squarefree argument; at non-squarefree $u$ the two differ ($g(4)=1$ here), but those terms vanish since
  $y^{(m)}_u$ contains $\mu(u)$.`

**7. slip: the non-vacuity sentence.**
- In `MaynardS2Y.lean`, the computed 5/2 is `maynard_S2_diag_example`, for `s2Form` (the φ(gcd) form) and the y-side.
  The 1/φ([d,e]) form of (3) is linked only by `maynard_S2_diag_lcm_example`, which goes through
  `maynard_S2_diag_lcm_R12`, not through `maynard_S2_diag_lcm_all`.
- `MaynardS2Mult.lean` instantiates only `maynard_S2_lam_of_y_odd`. Neither file instantiates `_lcm_all` or `_W`.
- The claim is true by chaining. As written, it suggests a direct check of (3) as stated.
- Text: `Non-vacuity examples with every hypothesis discharged are in both files (both sides of (3) equal $5/2$
  on a two-term $\lambda$).`
- Replace with: `Non-vacuity examples are in both files: on a two-term $\lambda$ ($R=3$, $k=2$) both sides of (3)
  equal $5/2$ (computed by \tl{decide} for the $\varphi(\gcd)$ form, linked to the $1/\varphi([d,e])$ form through
  the $R\le12$ instance), and the inversion (4) is instantiated with every hypothesis discharged.`

**8. style: thm:s2y item 1.**
- `gM\_prime` is not "multiplicativity".
- Text: `\tl{gM\_mul\_coprime\_sqf}, \tl{gM\_prime}: the multiplicativity of $g$ just stated.`
- Replace with: `\tl{gM\_prime}, \tl{gM\_mul\_coprime\_sqf}: $g(p)=p-2$ and the multiplicativity of $g$ just stated.`

**9. overstatement (mild): Hypothesis hyp:s2, last sentence.**
- "Removal of the coprimality restriction" is not an exact finite step. It is Maynard's (5.25) estimate, with sums over
  s > D_0 and a D_0-loss. It is elementary, but analytic in kind: it is an inequality, not an identity. The reader
  might read it as like the rest of the note, which is exact.
- Text: `The removal of the coprimality restriction and the exact part of Lemma~5.3 are
  elementary and are the next steps of this programme.`
- Replace with: `The bound for the $s_{i,j}\ne1$ terms (an elementary estimate with a loss $1/D_0$) and the exact part
  of Lemma~5.3 are the next steps of this programme.`
- The abstract wording "the coprimality restriction in the main term of $S_2$" would read better as "the removal of the
  coprimality restriction (Maynard's $s_{i,j}$ terms) in the main term of $S_2$" (style).

**10. slip (outside the .tex): stale statements in notes/lean-s2-y.md.**
- §"How the hypotheses differ" item 3 says that φ([a,b])φ((a,b)) = φ(a)φ(b) is "not prove[d] in general, because
  multiplicativity of φ is not available in the project". Item 4 says "That fact is not proved here".
- "NOT covered" lists "Multiplicativity of φ and of g".
- All of these are now proved in `MaynardS2Mult.lean`. Each holds for that one file. A pointer would prevent a reader
  from taking them as project status.
- Proposed: append "(now proved in MaynardS2Mult.lean; see notes/lean-s2-mult.md)" to each.
- The module docstring of `MaynardS2Y.lean` is literally correct ("NOT proved here").

**11. slip: paper/main.tex sec:related, Proposition 4.3.**
- The card's classification is "proved here, relative to LWW's own definitions and the hypotheses of Prop. 4.2". It also
  proves the implication (4.54) ⟹ (4.55), not (4.55).
- Text: `Proposition~4.3 (pp.~27--30), proved relative to their definitions;`
- Replace with: `Proposition~4.3 (pp.~27--30), the implication (4.54)$\Rightarrow$(4.55), proved relative to their
  definitions and the hypotheses of Proposition~4.2;`

**12. gap: paper/main.tex sec:related, Section 4.8.**
- The s48 card is conditional on more than the inputs of Prop. 4.5(i):
  - (J1) Prop. 4.5(ii)/(4.96), checked only relative to the 4.5(i) machinery. Its "as in (i)" steps were not
    re-derived.
  - (J3) Mertens, V_i = log 2 + o(1).
  - (J4) the Prop. 4.2 hypotheses.
  - (J5) meas M_{-2}, from the p23-27 card.
  - (4.76) and the Q ↦ TQ bijection, read in source and checked numerically, not re-derived.
- Text: `Section~4.8, (4.148)--(4.157), conditional on the inputs of Proposition~4.5(i).`
- Replace with: `Section~4.8, (4.148)--(4.157), conditional on Proposition~4.5(ii) (checked only relative to the
  machinery of Proposition~4.5(i), whose inputs it inherits) and on Mertens.`

**13. overstatement: paper/main.tex sec:related, "now has a card".**
- The s48 card itself hedges: "each part of Section 4 from (4.9) to (4.157) ... appears to have been the subject of a
  card (judged from the card list, not re-audited)".
- I found no card that claims a line-by-line check of pp. 18-23 apart from (4.26)-(4.31). The p23-27 card and the
  thinning card treat (4.13)-(4.22) as definitions and (4.26)-(4.31) for set-dependence and the measure bound.
- Text: `Every part of their Section~4 from (4.9) to (4.157) now has a card.`
- Replace with: `Judged from the card list, every part of their Section~4 from (4.9) to (4.157) has now been the
  subject of a card, (4.9) itself only as a named input.`

**14. style: paper/main.tex rem:186-status, the directed-arithmetic sentence.**
- The single label \lbl{Computed} covers claims that the note settles differently:
  - claims 1-7 and 12 are "Proved by reading" or "Proved here", with exact computations alongside;
  - claims 10 and 11 are "Checked by reading only".
- Text: `(\lbl{Computed}, $31$ checks,`
- Replace with: `(\lbl{Proved here} by reading and \lbl{Computed}, $31$ checks,`
- The numbers are correct: 31 checks, 19 negative controls, (2.26) for 1 ≤ r ≤ 98264, one program written from the
  PDF, verdict "verified as stated", and (2.3) proved for every M ≥ 2.

## No finding

- **Lean names.** All eight cited names exist, with the stated content: `totient_lcm_mul_gcd` (all a, b, including 0),
  `totient_mul_coprime`, `gM_mul_coprime_sqf` (m squarefree, n arbitrary coprime), `gM_prime`, `yS2_eq_zero`
  (unconditional), `maynard_S2_diag_lcm_all`, `maynard_S2_lam_of_y_odd`, `maynard_S2_lam_of_y_W` (2 ∣ W, entries
  coprime to W). Each appears once in Audit.lean. Neither file contains sorry, native_decide or axiom.
- **thm:s2y(3).** "For every R, k, m", "all pairs of the box (not only good ones)" and "x/0 = 0" are accurate.
  - The only hypothesis is `hsq`, so no oddness is needed.
  - The LHS filters d_m = e_m = 1 over the box.
  - The RHS sums over all u in the box with y²/tg. tg can be 0, and then y = 0 too.
  - If m ≥ k, `getD` makes d_m = 1 vacuous. This is harmless.
- **Oddness remark.** It is accurate: g(2) = 0, and the hypothesis `hg` is genuinely needed. For example, take k = 1
  and λ_(2) = 1. Then y_(2) = 0, so the inversion fails at d = (2).
- **Maynard.**
  - (5.18) is the main term XN/φ(W) Σ' λλ/∏φ([d_i,e_i]) with d_m = e_m = 1.
  - g is totally multiplicative with g(p) = p − 2, in Lemma 5.2 and after (5.21).
  - (5.23) defines y^(m) exactly as printed in the note. The remark "y^(m) = 0 unless r_m = 1" follows (5.23).
  - (5.24) with every s_{i,j} = 1 is Σ μ(u)²/g(u)·(y^(m)_u)², which is what (3) gives.
  - Lemma 5.3 expresses y^(m) through y, via (5.28)-(5.30). Its exact step uses the multiplicativity of
    μ(d)d/φ(d).
  - The error term of Lemma 5.2 is O(y_max² N/(log N)^A), as hyp:s2 says.
- **Abstract, Appendix A item 1.2, hyp:glue range.** These are consistent with the theorem, apart from #9's wording.
- **Counts.**
  - 25 files and 7320 lines (`wc -l`).
  - Nine Maynard* files. Reduction + Maynard* + Mu* (MuMult, MuTuple) total 4143 lines.
  - Audit.lean has 301 `#print axioms` lines. 172 + 75 + 21 + 33 = 301 matches the table in notes/lean-s2-mult.md.
    The run itself was not reproduced.
- **186 Lemma 1.1 sentence.** 196 checks, 17 negative controls, 67 retained rows and strict margins ≥ 10⁻⁶ all match
  notes/oai186-lemma11-analytic.md. "The imported theorems themselves are not verified" matches its status line.
- **LWW p23-27 sentence.** "Conditional on the divisor bound (4.9) (a consequence of Shiu's theorem, which we have not
  read) and on Mertens" matches (I1) and (I2). The page ranges pp. 16-18 and 23-27 match.
- **LWW, other sentences.** "All cards were audited by a fresh-context helper" holds: every LWW card from 25-27 Nov has
  an audit file, and the thinning card has an in-file audit. "No error has been found" and the "next" list (pp. 15-16,
  (4.1)-(4.8), the divisor bound, then Section 5) match the s48 card.
