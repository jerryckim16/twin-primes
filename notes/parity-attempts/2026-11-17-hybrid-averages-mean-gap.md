# Route card: hybrid averages and the mean prime gap (Lichtman–Teräväinen)

Date: 2026-11-17 (Session 30, 11:34 AM CT slot). mathbox not available; bounded attempt run by hand, audit by a
fresh-context helper (findings below, all applied).

## Question
Lichtman–Teräväinen (LT22, arXiv:2111.08912v3, read in full, SHA-256 87410676...68464014) prove
sum_{p<=X} mu(p+h) = o(pi(X)) for all but o(H) shifts h <= H once H >= (log X)^{1+eps} (Cor. 1.4; also for lambda).
This is the parity model case on average, at a scale enormously shorter than the X^{8/33} of MRT17 for
Lambda(n)Lambda(n+h). What does the hybrid trick buy toward a fixed shift, and where exactly does it stop?

## Success / no-go criteria
- Success: a precise statement of the scale below which LT's inputs cannot work, from BOTH sides (the input on mu and the
  input on Lambda), or a mechanism that reaches H = O(1).
- No-go: if LT already state such a barrier for the mu side (they state the Lambda-side sharpness, Remark 2.8, only).

## What was done
1. Read the proof: Prop. 3.2 (Fourier identity + Hölder) uses only (i) |f| <= 1 and the sieve bound (4.1)-(4.2) for
   n+h not in S, (ii) hypothesis H_2(X,H,eta) for f = mu 1_S 1_[0,X] with eta << H^{-delta} (Prop. 2.1, from MRT15),
   (iii) moment bounds for g (Prop. 2.7), needing H >= (log X)^{p/(p-2)}; diagonal terms show (iii) fails for H = o(log X).
2. Proved (elementary, folklore in substance): with mu' = 1 on U = P + [1,H] (P = primes <= X - H), mu' = mu elsewhere,
   mu' satisfies (i) verbatim and (ii) with eta' <= 2 eta + (216+o(1)) H / log X, but
   sum_{h<=H} sum_{n<=X} mu'(n+h) Lambda(n) >= (1+o(1)) H X. So the mu-side input is consistent with total conspiracy
   along primes whenever H^{1+delta} <= c log X, in particular for H = o(log X).
3. At bounded H, H_2 cannot hold with eta -> 0 (average over alpha: eta >= 2 H^{-1} X^{-1} sum |f|^2).
4. Script code/parity/hybrid_shifted_primes.py (X = 2e7, 2 min): discrete analogues of both bounds asserted for
   H = 2,...,64 (powers of 2); max_{h<=64} |sum lambda(p+h)|/pi(X) = 0.0025 (h = 42), 0.0018 at h = 2.

## Classification
**Located (literature + elementary lemma; folklore in substance).** Both inputs of the hybrid method break down at the
mean prime gap log X; the fixed-shift parity model (k = l = 1) stays open, and twin primes are not a hybrid case
(Lambda at both positions). First unresolved implication: any input on mu at scales H = o(log X) must be pointwise
along the primes, i.e. a genuinely prime-correlated statement — the parity problem itself.

## Audit (fresh-context helper, applied)
8 items: the quoted script maximum was wrong (0.0018 at h = 2 was only the max over h <= 8; true 0.0025 at h = 42);
inequality (a) omitted primes in (X-H, X] (fixed: H(psi(X) - theta(X-H)) term); H_2 normalisation E_f = 1 stated;
"case l = 1" corrected to k = l = 1; script description toned down (discrete x, powers of 2); (i) made meaningful by
modifying mu, not f; source for eta << H^{-delta} cited (Prop. 2.1, Remark 2.2); vague sentence replaced.

## Paper
papers/parity-barrier v0.15, Remark rem:lt22 (one remark, per the review rule); bib LT22; rem:ford-twin updated.
