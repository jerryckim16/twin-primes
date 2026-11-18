# Lane 2 (Section 4: ceilings, k = 2, k = 3) -- fresh-context referee, 18 Nov 2026

Saved by the coordinator from the helper's final report (in substance). Re-derived and correct: prop:ceil (scaling exponents;
thresholds 46/392/2965/22007 by an own mpmath run; c(3) = 2.4719, c(2) = 2.7726; the printed ceilings 4.1515, 4.0907, 2.1589);
thm:k2 (regions, f-bar trick, all three bounds, extremal F_eps); the dual paragraph (Phi = Pi_K P^*(g,f); clean columns
disjoint); prop:unc-ceiling (Schur test; eps >= 1/4 used exactly where stated); cor:k3-linear (scaling; 2.16832, 2.05693,
2194/4999). Certificates re-run: k3_unc_verify.py on the 439/1000 file (5135 boxes) and the 9/20 file pass; k3_arrangement_verify.py
on eps = 1/4 gives 2 + 711155/3866758832 exactly; stored ratios for 2/9 and 7/24 and the orth-relax ratios match.
Errors: (1) M_{51,1/50} has eps = 1/(k-1), the endpoint of Theorem 3.12(ii) as stated; (2) the footnote on PM8b Prop. 6.5 lost
"off the fibres used"; (3) lower bounds 1.9982 and 1.9952 are rounded up (file: 1.998162, 1.995151): truncate.
Gaps: footnote's corrected bound needs its one-line argument; rem:k3-window's mu* = kappa_3(1-eps) only for eps in [1/4, 1/2);
thm:k3-window(2) second clause superseded by the corollary; cor:k3-linear: state C = 3/2 + s mu and the range; orth-relax at
eps = 1/4 says nothing (only eps = 1/8 shows the loss, against a heuristic estimate).
Labels: footnote; rem:ceil-locates and rem:k2 headers; exact lower bounds need their file and "Computed"; "about 6e-8" needs a
source. Minor: Phi names two objects; 2/9 certificate uses denominator 100; K as complement of the closure; "2/theta >= 2" -> "> 2".
