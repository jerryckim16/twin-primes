# Vendored copy of openai/PrimeGaps186 (Apache License 2.0)

Upstream: https://github.com/openai/PrimeGaps186, commit `61340d0b74163003b32756bb16e91d9209a5e330`
(2 Sep 2026). The coordinator session fetched it read-only on 14 Nov 2026 at Jerry Kim's request.
The repository is published under the Apache License 2.0 (`LICENSE` here), which permits
redistribution. These files are copied unchanged:

- `short_gaps_numerics.pdf`: "Numerical certificate for prime gaps at most 186" (23 pp.), the
  numerical companion. It includes the group data for the loss components: the radial intervals of
  (1.22), the row cores and thresholds of the clipping (1.26) with Lemma 1.6, and the
  delay-recurrence / renewal-majorant rule (2.3).
- `prime_gap_186_certificate.py`: the authors' own certificate program. Its `build_inputs()`
  holds the per-group rows (`a`/`A` cores and thresholds, radial shells) and the
  `low_dickman_method` setting.
- `UPSTREAM_README.md`: the upstream README.

**How to use them.** The authors' program is a **reference, not an independent check**. This
project's two programs for rung 186 must be written from the paper's formulas without copying the
script's logic. The script may be consulted afterwards to locate a disagreement or to read off
input data (parameters, rows) that the paper does not print in full. Record any such use in the
log.
