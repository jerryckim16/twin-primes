# Referee pass before freezing the parity paper as v1.0 (18 Nov 2026, Session 32)

Five fresh-context adversarial referees (helper agents; mathbox:referee is not available in this environment), one lane each:
- lane1-sections1-3.md: mathematics of Sections 1-3 (Type I input, criterion, Chen test, Remark 8.1, Pintz dichotomy);
- lane2-section4.md: Section 4 (ceilings, k = 2 theorem, k = 3 window), with the certificates re-run;
- lane3-sections5-7.md: Sections 5-7 and the numerical section, with identity (*) re-tested numerically;
- lane4-literature.md: literature fidelity, 11 arXiv sources downloaded and checked against printed pages;
- lane5-framing-labels.md: framing, labels, notation, readability, caveats lost in the condensation.
A sixth helper checked afterwards that the fixes introduced no new error (see the log entry of Session 32).

Outcome: no false mathematical statement and no literature mismatch of substance. Found: 2 statements wrong as written
(rem:chen "1 + s1 s2 kills 'n+2 = p1 p2'" -> "n prime and n+2 = p1 p2"; the hybrid-average range "H = o(log X)" ->
"H <= (c log X)^{1/(1+delta)}"), two exact lower bounds rounded up instead of truncated (1.9982 -> 1.9981, 1.9952 -> 1.9951),
and a set of hypotheses and caveats lost in the condensation from v0.16 (Delta condition for (B); "w fixed" in the Siegel
section; r != 0 in Pintz; non-coprime classes in the Pintz proof; class-by-class reading of the Remark 8.1 weight; fairness at r;
V(2) by the PNT; 4 | L; footnote argument for PM8b Prop. 6.5), plus framing, label and notation items.

Response: all items applied in v1.0 (see the lane files for the list), except the following, judged cosmetic: label keys
named prop:/cor: on remarks and sec: on subsections, the bibliography key Cit26, and journal page numbers for MR16, GT10, GT12
(not opened). Lane 4's unverified locations are listed in lane4-literature.md; they were read in earlier sessions (see
notes/sources-*.md) and are not re-verified here.
