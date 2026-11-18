# Route card: Fejér averages, pair correlation, and the scale log X (Session 31, 18 Nov 2026)

The twin prime conjecture is open. This attempt does not break parity; it locates where conditional averaged results stop.

**Question (parity paper, open question oq:mrtcond).** Under which hypotheses, and down to which H, does an averaged
Hardy-Littlewood statement hold? And what would be missing for a fixed shift such as h = 2?

**Success criterion.** A precise conditional range for some averaged form, with a proof from cited statements read in the
sources. **No-go criterion.** The range does not go below the mean gap log X, or needs a hypothesis that already contains
the fixed-shift statement.

**Mechanism.** The exact window identity of rem:mrt17, written in terms of the Goldston-Montgomery mean square
I(K) = sum_{0<=x<N} (psi(x+K) - psi(x) - K)^2:
  2 sum_{1<=j<K} (K-j) c(j) = I(K) - K c(0) + K^2 N + 2K^2 (psi(N) - N) + O(K^3 log^2 N).   (*)

**Results (paper Remark rem:gm; Proved here, elementary, folklore in substance).**
- (a) Unconditionally, the Fejér mean satisfies F(K) >= 1 - (1+o(1)) log N / K + o(1). This is the Lambda form of Merikoski's
  Main Thm 2 (arXiv:1605.04757v1), which he proves for prime counts.
- (b) For K = o(log N), the asymptotic I(K) ~ KN log(N/K) holds unconditionally (the diagonal term alone), so it carries no
  pair information there.
- (c) Under RH and the strong pair correlation conjecture (SPC): by Goldston-Montgomery (Goldston's notes
  arXiv:math/0412313v1, Thm 7 and (9.3)), SPC is equivalent on RH to I(K) ~ KN log(N/K) for 1 <= K <= N^{1-eps}. This
  gives F(K) -> 1 whenever liminf K/log N > 0. Conversely, at K ~ log N the two statements are equivalent.
- (d) For a fixed shift, c(2) = N + (I(3) - 2I(2) + I(1))/2 + O(|psi - N| + log^2 N). The twin asymptotic needs I(K) for
  K <= 3 to o(N), one logarithm beyond any form of the variance asymptotic. Those lower-order terms are, through (*),
  equivalent to HL at h = 2 itself. Keating-Smith (arXiv:1903.07057, abstract only, heuristic) state the corresponding
  equivalence with lower-order terms of the zeros' two-point correlation.

**Classification.** Located (conditional; literature plus an elementary identity). First unresolved implication: the
variance at bounded K to precision o(N), i.e. lower-order terms of pair correlation. The missing step is precision, not
parity, and the hypothesis (SPC) concerns zeros, not sieve axioms. The almost-all form of MRT17 under GRH/EH stays open
(not found in print).

**Checks.**
- Fresh-context adversarial audit (mathbox not available): identity and (a)-(d) correct. It found 3 errors (SPC named as
  "pair correlation" in three places; two numerical ranges misquoted from the .out) and 4 gaps (overclaim on the -KN log K
  term; "answer" read as "smallest H"; ambiguous bound value; missing converse citation). All fixed.
- Numerics: code/parity/variance_fejer.py [X KMAX] (/usr/bin/python3 -I; 2 min at 1e8, < 2 GB), output .out. The identity
  is exact, F(K) is within 5e-4 of the HL means, and (I - KN log(N/K))/(KN) ~ -2.41 against B - 1 = -2.415 (MS04 Thm 3).
- Sources read (SHA-256 of the copies): Merikoski 1605.04757v1 0a719f39...7efd51; Goldston math/0412313v1 d4107ba6...615473c;
  Montgomery-Soundararajan math/0409258v1 4814387d...d7a8176. Abstract only: Keating-Smith 1903.07057v1;
  Conrey-Keating 1604.06124v2 (heuristic, ratios conjecture; not used).
- Not opened: Selberg 1943 (an RH mean-square bound would give F -> 1 for K/log^2 N -> infinity; not stated in the paper).

**Do not repeat.** Fejér/variance averages at leading order. A new input would be lower-order terms, or the almost-all
form under GRH/EH.
