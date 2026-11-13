# Audit A — Song–Yue §4.1 and §4.5 (parameters, Heath–Brown classification, routing), plus all numerics in §§4.1–4.7

(Report delivered by the auditor as its final message; saved by the coordinator. Single-agent self-review.)

**Verdict:** no demonstrated defect in §4.1 or §4.5; every numerical inequality found in §§4.1–4.7 holds exactly. Prop 4.11 (every localized Heath–Brown block is covered) and Lemma 4.13 hold if Props 4.2, 4.4, 4.6 hold as stated; through 4.14–4.17, so does Theorem 4.18.

## Checked
- (a) §4.1 constants: U=521/2000, L=491/2000, L+U=253/500, 10δ<B<11δ, r(t)≤10, Lemma 4.1.
- (a) Heath–Brown identity (53): re-derived; exact integer checks for (K,Z) = (3,5), (4,4), (10,2).
- (a) (54), (55): at most 20 factors; O((log X)^20) blocks.
- (a) Lemma 4.8: divisor bound, location, smoothness of large atoms. (b) SW for grouped factors: inheritance identity checks; only black box is classical Siegel–Walfisz for µ (scale hypothesis met).
- (a) Lemma 4.9: proof re-checked step by step (4s−(1/2−s) = 1/2000 > 0; 2(1/2+s) > 1). 59,998 exact random/threshold vectors (≤ 9 coords) satisfy an alternative; MILP counterexample search (n ≤ 9) found nothing beyond tolerance. Five equal parts 1/5 break all three alternatives at s = 1/10, so s > 1/10 is essential.
- (a) Lemma 4.10: 3999/10000 + 253/500 = 9059/10000 < 1.
- (a, given 4.2/4.4/4.6) Routing: every case of Lemma 4.9 covered with strictly positive reserves; IIb and IIa ranges closed, meet at 11/25. Bilinear case: both groups SW, shorter in β slot. Type III: the three selected atoms have u ≥ 0.2002, hence smooth (not Möbius); α needs only a divisor bound.
- (a) Stadlmann-type factor swap: none (bilinear case, long-factor case, BV inside Type III, Lemma 4.13 envelope all keep SW in the required slot).
- (a) 72 exact numeric checks, 0 failures: (28), (32)–(35), (38), (42)–(43), IIb margins, Lemmas 4.3/4.5/4.7, Type III exponents 1−1/3000, 1−137/3000, 1−71/2400, Euler factor, (63), 1259/1500.
- (e) Locators [D.14a, Lemmas 3.1, 3.3, 3.4(iii)] not checked offline; 3.1 re-proved in the paper, 3.3 re-derived here; only 3.4(iii) relied on (classical SW).

## Exposition gaps (c)
Lemma 4.9 proof skips the trivial no-pivotal-index case; "m, m' ≤ 54" in Q182 is vacuous (m ≤ 10 forced); N := min(N0, X^{1/2}) relabelling changes support constants by ≤ 2^{10.5} (legitimate under the claimed uniformity); "at least X^{η/20}" should be "≫ X^{η/20}" in Lemma 4.8.

## Remaining obligations
Props 4.2, 4.4, 4.6 and their deep inputs ([D.14a] Thm 2.9, Cor 4.16, Prop 5.10, Lemma 6.25/Cor 6.26); classical SW for µ with a coprimality restriction; Lemma 4.30 (checked by audit E).

Files: check_numerics.py → numerics.out; check_lemma49.py → lemma49.out; check_heathbrown.py → heathbrown.out; img/.
