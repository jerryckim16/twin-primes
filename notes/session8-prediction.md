# Registered prediction (Session 8, written 13 Nov 2026 01:40 UTC, before the k = 45 Lemma 9.1 optimisation finished)

Heuristic (own): optimising P on the capped support recovers only a small fraction of what the caps cost
the truncated cap-free optimiser, because the truncation is a perturbation and the Rayleigh quotient
gains from re-optimisation only to second order.
Evidence so far (k = 49, Stadlmann, degree 20, even power sums): cap-free 4.016176, truncated 4.012039
(cost 0.004137), optimised on T 4.012420 (regains 0.000381, about 9%).

Prediction for Charton et al. with the caps of their Lemma 9.1 (k = 45, degree 21, 846 coefficients):
cap-free 4.012272, truncated 3.973687 (cost 0.038585). If about 10% is regained, the optimum on T in this
space is about 3.977-3.981, still below 4; any value above 3.99 would contradict the heuristic.
