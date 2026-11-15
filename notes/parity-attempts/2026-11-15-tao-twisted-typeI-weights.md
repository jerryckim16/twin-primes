# Is the twisted Type I input of the parity obstruction a theorem? (Tao's two-point theorem along sieve weights)

- **Date:** 2026-11-15 (Session 17). Kind: attempt (locate the barrier; model problem).
- **Target:** PM8b §8's obstruction assumes, heuristically, that Liouville-twisted Type I sums such as
  sum_{n = a (q)} lambda(n)lambda(n+2) are negligible. Can this input be proved, in some averaged form, for the actual weights a
  twin-prime sieve uses, w(n) = (sum_{d | n(n+2), d <= R} lambda_d)^2? If so, in what regime, and what is the first missing step?
- **Success criterion:** a proved statement sum_{n<=x} w(n)lambda(n)lambda(n+2)/n = o(sum w(n)/n) for a non-trivial class of sieve
  weights, with the regime (level R) stated exactly. **No-go criterion:** the needed uniformity is shown to be equivalent to, or to
  imply, a known open problem, or the cited theorem does not apply.
- **Cheapest decisive check:** read Tao16 Thm 1.2 (arXiv:1509.05422) and check the parameters (a_1 = a_2 = q, b_1 = c, b_2 = c+2).
- **Outcome: proved, restricted regime.** Paper Prop. prop:tao-weight (Proved here, possibly folklore): for every periodic w,
  sum_{n<=x} w(n)lambda(n)lambda(n+2)/n = o(log x); for Selberg-type weights of fixed level R (or R(x) -> infinity slowly enough),
  both parity classes lambda(n)lambda(n+2) = +-1 carry half the log-weighted mass. Proof: split into residue classes, n = qm + c,
  Tao16 Thm 1.2 with a_1 b_2 - a_2 b_1 = 2q != 0.
- **What this is and is not:** it CONFIRMS the input of the parity obstruction (the weight cannot distinguish the two parity classes)
  in the log-averaged, bounded-level regime. It gives no lower bound for twin primes and does not break parity.
- **First unresolved implication:** uniformity of Tao16 Thm 1.2 in the modulus q up to x^theta (even on average over q). Tao16
  Remark 1.4 and footnote 2: the dependence on (a_i, b_i) is effective in principle but expected to be very poor (A roughly
  triple-exponential in 1/eps; decay (log log log x)^{-c}), so the slow-growth regime is all the theorem gives.
- **Numerics (Heuristic):** code/explore/parity_weighted_liouville.py, runs/explore_parity_weighted.log: at X = 1e8, theta = 1/4,
  B/A = 4.3e-5, twin pairs carry 4.7% of the weight, all in the "+" class.
- **Disposition:** closed (proved in the weak regime; the strong regime is Open and would only confirm the obstruction).
- **Continuations:** (a) uniform-in-modulus two-point log Chowla on average over q <= x^theta (Open; search literature: none found in
  one search, 15 Nov); (b) DONE in the same run: the proposition is stated for any two distinct shifts h != h', so the PM8b weight (1-lambda(n)lambda(n+2))(1-lambda(n+2)lambda(n+6)) = 1 - ll(0,2) - ll(2,6) + ll(0,6), which involves only two-point products, is covered in the same weak regime (f = 1, log-averaged, fixed modulus). f = Lambda or alpha*beta is NOT covered.
- **Review:** adversarial fresh-context audit (Session 17): correct with fixable gaps (diagonal choice of R(x) made explicit; Tao's Remark 1.4 says 'in principle effective'); all fixes applied in paper v0.1. Literature-check: one web search, no prior statement found (possibly folklore).
