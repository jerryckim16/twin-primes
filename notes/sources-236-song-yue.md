# Song–Yue, "Bounded Gaps Between Primes: An Upper Bound of 236" (IACR ePrint 2026/1893)

These notes are from the full text: the version dated 2 September 2026, 82 pages, which Jerry supplied on 13 Nov 2026 (the ePrint server returns 403 to us).
Nothing here is a result of ours. **Q:** marks a quote from the paper (via `pdftotext`). **Mine:** marks my own reading or arithmetic.
The PDF itself is not committed. The data needed to check it is in `code/cap6/songyue236_witness.json` (Appendix A) and `code/cap6/songyue236_appC.json` (Appendix C).

## 1. The claim and its structure
- Q: "we prove H1 ≤ 236" (abstract). Theorem 1.1 / 4.33: two-prime translates of every admissible 48-tuple. The 48-tuple of diameter 236 is taken from the MIT Prime Gaps data (Lemma 4.32).
- Analytic input: Theorem 4.18 is a new equidistribution estimate for the squarefree "D182" moduli, q ≤ X^{(1-σ)·253/500}. It is proved via IIa, IIb and Type III estimates and a Heath–Brown decomposition (§§4.2–4.7). **Status: Claimed.** We have not verified it, and the same caveat applies as for Stadlmann's 240.
- Variational input: a single exact integer sign (Prop. 4.21).

## 2. Parameters (§4.1, Eqs. (21)–(23))
- k = 48, A = 253/1000, ε = 3/400, U = A + ε = 521/2000, L = A − ε = 491/2000, δ = 91/5000, B = 1899/10000.
- Caps: B_0 = 0 and B_m = B for all m ≥ 1 (a single constant cap). Support T = {t ∈ R^48_{≥0} : s(t) < U, R(t) ≤ B_{r(t)}}, where R is the sum of the coordinates > δ and r is their number. Q: "r(t) ≤ 10 on T" (Lemma 4.1).
- **Mine:** in Polymath scaling (u = 4t) this is exactly Kintali's D182 support from `notes/sources-236.md`: L = 521/500, τ = 491/500, g = 91/1250, caps 1899/2500. So "Kintali" and "Song–Yue" are the same support, matching the name "D182" (182 = 10^4 δ). Q: "The original witness was constructed for k = 50. Here the same symbolic polynomial is evaluated in 48 variables" (§4.8). Kintali also transports a k = 50 certificate.
- J uses the base cutoff s(x) ≤ L on the 47-dimensional base, and the final coordinate runs over the capped fibre [0, h(x)], with h = min{H, max{δ, B_{r+1} − R}} and H = U − s(x) (Lemma 4.20).

## 3. The witness (§4.8, Appendix A)
- P(z) = Σ c_{a,α} (26/25 − s(z))^a m_α(z) over 1295 integer triples, with a + |α| ≤ 25. Then P_U(t) = P(26t/(25U)) and F = P_U 1_T.
- Integer coordinates are x = 10^4 t, with U* = 2605, L* = 2455, δ* = 182 and B* = 1899. Q(x) has integer coefficients (Eq. (71)).
- Our extraction: `code/cap6/songyue236_witness.json`, with rows [row, a, alpha (list of parts), c]. Checks done at extraction:
  - 1295 rows, numbered 1..1295 with none missing;
  - every α nondecreasing;
  - max a + |α| = 25, max part 24, max length 12;
  - no table line left unparsed.

  Exponent superscripts (q^r = r copies of q) were read from font sizes with pdfplumber. **Spot-check before use:** rows 17 = (1, [2,2], 6593890543566) and 41 = (1, [2,2,2], −2137258613006123) match the printed table.

## 4. The certificate (§4.12, Prop. 4.21, Lemma 4.22, Appendices B–C)
- **The criterion uses the CAP-FREE denominator:** 48 J(F)/I0 > 2001/2000, where I0 = ∫ P_U^2 over the full simplex {s < U}. Since I(F) ≤ I0, this gives 48 J(F)/I(F) > 2001/2000 > 1. In Stadlmann scaling the threshold is > 1, i.e. > 4 in Polymath scaling.
  - **Mine:** this avoids the capped denominator entirely. We only need the exact cap-free I0 (simplex moments, as in `code/mk_general.py` / Lemma 3) and the capped J (the J-part of `code/capped_check.py`, with B_m = B for every m ≥ 1, base cutoff L and fibre h(x)).
- Q (Prop. 4.21 and Appendix C, "Verification status"): "A fresh exact evaluation of the uncapped denominator reproduces Iref. The reference numerator Jref is the exact sum of the uncapped numerator and the three signed correction totals [which] were found with AI assistance ... Full fresh regeneration of the capped numerator from the coefficient table remains incomplete at this revision."
  - **So the authors themselves have NOT independently recomputed the capped numerator.** An exact recomputation of J from the coefficient table is exactly what this project can add.
- Reference integers (`code/cap6/songyue236_appC.json`):
  - Iref = (98!)^2 I0,*, with 655 digits.
  - Jref = (99!)^2 (26!)^2 J*, with 715 digits.
  - Nref = 48 Jref.
  - D* = 10^4 · 99^2 · (26!)^2, and Dref = D* Iref.
  - Δref = 2000 Nref − 2001 Dref > 0.
  - Checked on extraction: the digit counts match, Nref = 48 Jref and Dref = D* Iref hold exactly, and Δref recomputes to the printed value. **Mine:** Nref/Dref = 1.0006649216, which would be about 4.00266 in Polymath scaling. The margin over 2001/2000 is only 0.000165.
- The paper states 272 distinct marginal signatures, 37128 unordered products and 7338 output signatures (Prop. 4.21). Appendix B (pp. 76–79) gives the evaluation rules:
  - the full marginal via Eq. (74) and g_{a,q}(H) = q! a!/(a+q+1)! · H^{a+q+1} (Eq. (75));
  - three correction regions C, D, E (Lemma 4.20, Eqs. (79)–(80)), with signed corrections b^2 − 2gb on C ∪ D and −g^2 on E;
  - capped moments by rough/small strata, inclusion–exclusion and radial integrals (§4.10, Eqs. (76)–(77)).

## 5. A remark about Stadlmann's proof (relevant to our 240 caveat)
- Q (Remark 4.23): "The large-γ argument in the proof of [Sta26, Lemma 5] invokes its Type IIa lemma after swapping the two factors. Type IIa requires the shorter factor to be Siegel–Walfisz, whereas the Type I statement only assumes an arbitrary divisor-bounded shorter factor and a smooth longer factor. Thus that particular invocation is not justified by those assumptions. This observation identifies a missing hypothesis in that proof step; it is not a counterexample to the distribution conclusion itself."
- Q (same remark): Stadlmann's Prop. 3 states its auxiliary slack as 10^-10, so a different slack "requires checking its proof".
- **Mine:** this is a *claimed gap in Stadlmann's analytic proof*, raised by other authors, and we have not checked it. It does not affect what we verified (the variational step), but it strengthens the "conditional" label on 240. Record it in the paper's status table as "a possible gap in [Sta26, Lemma 5] noted by [SY26, Remark 4.23]; unverified".

## 6. Plan for the next runs (rung 236)
1. Load `songyue236_witness.json` and build P (expand (26/25 − s)^a m_α into the evaluators' basis, or directly in the integer coordinates of Eq. (71)). Before anything else, check that the expansion reproduces the paper's structure: degree ≤ 25 and the stated signature counts if feasible.
2. I0: exact cap-free mass in k = 48 by simplex moments. Compare with Iref after the normalisation of §4.12 (the paper says it was regenerated; this is our independent check).
3. Capped J: run the J-part of `code/capped_check.py` with k = 48, the D182 parameters above, base cutoff L and B_m = B. Compare with Jref **exactly**. Then compute 48 J/I0 and check > 2001/2000. A second, independent program is needed as for every rung (e.g. `capped_exact.py`'s J path, or a direct implementation of Appendix B).
4. Memory: degree 25 at k = 48 is heavy, and our own k = 48 builds ran out of memory twice. Run it alone and use chunking (GRAM_CHUNKS-style) or disk-backed accumulation.
5. If J matches Jref exactly and the ratio clears 2001/2000, then the variational step of [SY26] is independently reproduced, and 236 becomes our conditional bound with the same caveat as 240 (analytic input Claimed). If it does not match, report the discrepancy precisely. This would be the first fresh regeneration of their numerator, which the authors say is still pending.

## 7. Result (Session 10, 13 Nov 2026)
- Plan step 1-3 done. Witness converted exactly (`code/songyue_convert.py`, pointwise check exact); all parts of every alpha are even, so the witness lies in our even-power-sum degree-25 space (1311 terms).
- I0: (98!)^2 10^192 5^150 521^50 I0 = Iref exactly (`code/songyue_I0.py`, monomial basis). So Q = 65125^25 P_U in their integer coordinates (our reading of Eq. (71), confirmed by the equality).
- J (capped, `code/capped_check.py`): (99!)^2 (26!)^2 10^196 5^150 521^50 J = Jref exactly. 48 J/I0 = 1.000664921591 > 2001/2000. Capped denominator: 4.0030988047 (Kintali's 4.0030988); cap-free: 4.0036348167 (Kintali's 4.0036348).
- Second program (`capped_exact.py --jonly --ckpt`) in progress; see STATE.md.
