# Exploration log (newest first)

Each entry: date, session, idea, what was tried, outcome (dead end / inconclusive / promising), why.
"Promising" is not a result: it goes to the ideas ledger (origin "exploration") and needs the usual checks.

## 2026-11-13, Session 10 -- Is Song-Yue's objection to [Sta26, Lemma 5] real? (exponential sums / Type I-II area)
- Idea: [SY26, Remark 4.23] says the large-gamma step of the proof of [Sta26, Lemma 5] (Baker-Irving Type I)
  applies the Type IIa lemma with the factors swapped, although Type IIa needs the shorter factor to be
  Siegel-Walfisz and Lemma 5 assumes nothing about it. Read the arXiv v1 text (fetched 13 Nov, pdftotext) and
  check the claim against the statements.
- What we read (arXiv:2608.31126v1, Sec. 3.2, 3.3.5, Def. 9, proof of Prop. 3, Case I):
  * Lemma 3 (Polymath Type II): f = alpha * beta, beta at scale N = x^gamma <= x^{1/2}, "Suppose also that beta has
    the Siegel-Walfisz property".
  * Lemma 5 (Baker-Irving Type I): alpha an arbitrary coefficient sequence at scale M, beta smooth at scale
    N = x^gamma; no Siegel-Walfisz hypothesis on alpha.
  * Proof of Lemma 5, range gamma in (1/2, 1/2 + 2 omega + eps]: "we can apply our Lemma 3 (with the roles of alpha
    and beta swapped and gamma replaced by 1 - gamma)". After the swap the shorter factor is alpha (scale x^{1-gamma}
    <= x^{1/2}), so Lemma 3 needs alpha to be Siegel-Walfisz.
  * Definition 9 (I) and Case I of the proof of Prop. 3 apply Lemma 5 to "alpha a coefficient sequence at scale M"
    (again no Siegel-Walfisz hypothesis); Case (II) states the hypothesis explicitly for both factors.
- Outcome: INCONCLUSIVE, but the textual gap is CONFIRMED: as written in v1, that step uses a hypothesis that neither
  Lemma 5 nor Def. 9 (I) provides. Whether it matters is open: the alpha's that occur in a Harman-sieve
  decomposition are usually built from primes / rough numbers and may well be Siegel-Walfisz (then adding the
  hypothesis to Def. 9 (I) for that gamma-range repairs the proof); alternatively that gamma-range might be covered
  differently. We have not checked either repair. Status for the paper: "possible gap in the analytic input of 240,
  raised by [SY26, Rem. 4.23]; the cited step reads as they say (checked against arXiv v1); repair not checked".
- Why it matters: 240 (and 236, which reuses Stadlmann's estimates) rests on this analytic input; our reproduced
  240 is already labelled conditional on it.
