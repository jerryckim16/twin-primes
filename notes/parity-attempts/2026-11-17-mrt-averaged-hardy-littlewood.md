# Route card: averaging over the shift (Matomaki-Radziwill-Tao) and why h = 2 stays out (Session 29, 17 Nov 2026)

Candidate (d) of the weekly review of 16 Nov. Bounded attempt; method as in mathbox:research-attempt (not available; done by
hand, sources read here, the new text audited by a fresh-context helper: notes/audit-parity-v014.md).

## Question
Matomaki-Radziwill-Tao prove the Hardy-Littlewood asymptotic for Lambda(n)Lambda(n+h) for almost all h in windows of length
H >= X^{8/33+eps}; for lambda(n)lambda(n+h) they need only H -> infinity. What exactly does averaging over the shift buy, where
does the obstruction sit between a single shift and these windows, and is it parity?

## Success / no-go criteria (fixed before work)
- Success (location): a sourced, precise statement of what is proved on average and at which scales, an elementary mechanism
  explaining why averaging helps (and why it cannot reach a prescribed h), and an honest statement of which obstruction blocks
  each range.
- No-go: if the averaged results were found to give information about a prescribed shift (they would then be stronger than
  stated), or if the gap below X^{8/33} were already closed in the literature (then the location would be wrong).

## Sources read (this run; PDFs not committed)
- MRT17: Matomaki-Radziwill-Tao, Correlations of the von Mangoldt and higher divisor functions I. Long shift ranges,
  arXiv:1707.01315v3 (SHA-256 e93924c5a97b7813320ca84dcbf4619a958b47781e2e7ab36f6e2fd11a9493a1), pp. 1-11: Thm 1.3(i),
  sigma = 8/33 (13), footnote 4 (H below log X impossible for these methods even under GLH/GRH/EH; MRT15 relies on
  multiplicativity at small primes), p. 5 (averaged HL for most h = O(X^{1/6-eps}) would give PNT in most short intervals),
  pp. 9-11 (circle method, (16), Gallagher, Dirichlet polynomials).
- MRT17b: arXiv:1712.08840, abstract only (H = (log X)^{10000 k log k} for d_k d_l and Lambda d_k; Lambda Lambda only at
  X^{8/33+eps} in MRT17).
- MRT15: arXiv:1503.05121v3, abstract (averaged Chowla for H -> infinity, H <= X, qualitative o(H^k X)).
- One web search for improvements of 8/33 for Lambda Lambda: none found (Lichtman-Teravainen, hybrid Lambda-lambda, noted
  but not read).

## Work
- Elementary identity (folklore): sum_x |sum_{x<n<=x+K} f(n)|^2 = sum_{|h|<K} (K-|h|) c_f(h); hence V(K+1) - 2V(K) + V(K-1)
  = 2 c_f(K): the twin count is half the second difference V(3) - 2V(2) + V(1) of the second moment of primes in windows of
  length K, so V(3) to relative precision o(1/log X) is equivalent to the twin asymptotic. Verified exactly by
  code/parity/mrt_averaged_hl.py (K = 2, 3, 7; window 10^6 at 10^8).
- Location (paper subsec:mrt17, Remark rem:mrt17): on average over shifts the Liouville model of parity is solved (MRT15);
  the prime problem is proved for H >= X^{8/33+eps}, open below; for H <= X^{1/6-eps} the obstruction named by MRT17 is
  PNT in almost all short intervals (not parity), between X^{1/6} and X^{8/33} a limit of method; methods through second
  moments need H/log X -> infinity (diagonal); Thm 1.3 says nothing about a prescribed h (exceptional set unidentified and of
  size > 1). Fixed windows: positivity only (PM8b 246; parity stops it at 6 even under GEH).
- Numerics (Heuristic): r(h) = c(h)/(S(h) L(h)) for prime pairs in (1e8, 2e8], even h <= 2000: r(2) = 0.99906, mean 0.99992,
  sd 0.00088 (Poisson 0.0014), no |r-1| > 0.005. At 1e7: sd 0.0023 vs Poisson 0.0039.
- Audit (fresh-context helper): identity, second difference, diagonal and numbers verified; 3 errors (page attribution of the
  d3/d4 sums; the PNT-in-short-intervals obstruction attributed to the whole range below X^{8/33}; "any averaged statement"
  overgeneralised) and 5 gaps (precision needed in V(3); H >> log X vs H/log X -> infinity; MRT15 qualitative and H <= X;
  "needed"; the 6 is under GEH), all fixed. Minor items fixed except journal references (from memory; not added).

## Classification
LOCATED (literature + folklore identity). No parity-breaking content. Averaging over h removes the parity obstruction for the
Liouville model, but for Lambda the averaged problem is limited by short-interval distribution of primes, and no averaged
statement reaches a prescribed shift. Entered the paper as one short subsection (review rule). First unresolved implication:
the averaged Hardy-Littlewood statement for Lambda Lambda in windows below X^{8/33} (even under GRH/EH, not found in print).

## Not to repeat
Any attempt to reach h = 2 from almost-all-h averaged correlation results (unidentified exceptional sets), or from
second moments of primes in windows of fixed length without relative precision o(1/log X).
