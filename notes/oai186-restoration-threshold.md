# Rung 186: which margin threshold the restoration step needs (Session 52, 24 Nov 2026)

Source: OpenAI, "Improved short gaps between primes" (30 Aug 2026), the main 186 paper ([8] of the companion),
https://cdn.openai.com/pdf/51126fac-1b68-4128-9666-c908bcc16033/short_gaps.pdf, re-fetched 24 Nov 2026,
SHA-256 456f05e0a3ef589ebb0e9abcfd31f140f3c945adbf6950e00ef371a3c88b0930 (PDF not committed; read with
pdftotext -layout, printed pp. 27-31). Label: Literature (preprint, Claimed) for the statements; our reading below.

## Question (open in paper/main.tex, prop:oai186-budget; review of 23 Nov)
Our budget proposition gives two slacks for the total loss L+: 1.84% before the normalised margin
mu = (rho*(J^- - L) - I^+)/I^+ falls to 1/50000, and 12.8% before it falls to 0. Which one does the
restoration step ([8, Prop. 4.6]) need?

## Answer: strict positivity (mu > 0). The 1/50000 is a reported cushion, not a hypothesis.
- [8, Prop. 4.6, (4.41)], p. 30: "DHL[k, 2] holds if rho*(J^-_{lambda,H} - E_O^+ - d0 beta_old^+ - (1 - b_h) beta_new^+)
  > I_H^+". A strict inequality with no fixed margin. With (4.43) (d0 beta_old + (1 - b_h) beta_new + E_O <= L+,
  Lemma 4.8, p. 31) this is exactly mu(L+) > 0 in our notation.
- The other terms of (4.40) are handled inside the proposition: the alpha term has coefficient 1 - rho*|b_h| C_op > 0
  (rho* < 1/3, |b_h| < 1/1000, C_op = 4 by (4.33)); the companion records 1 - 4 rho*|b_h| = 2497786653900013/
  2500000000000000 (notes/sources-186-loss.md). The deficit kappa_def = 1/50000 of Stadlmann's minorant mass already
  sits in the coefficients b_h = (1 - m0/lambda) kappa_def K_ex (§4.3, (4.21), (4.28)-(4.29), pp. 27-28); it is not
  subtracted again from the margin.
- Proof of Thm 1.1 (p. 31): (4.45) states that the margin exceeds 1/50000 and then uses only "the strict inequality
  above makes its restored quadratic form positive". So 1/50000 is a stated lower bound for the margin, coinciding
  numerically with kappa_def, not a requirement.
- Finite-band approximation (§4.2.4, p. 26; Thm 4.5's proof, p. 28): bands and inward smoothing are chosen "fine enough
  to preserve" the strict margins, "up to arbitrarily small fixed approximation errors", before x -> infinity. So any
  strict positive margin suffices qualitatively; no quantitative margin is consumed.

## Consequence for our budget (Computed values from code/oai186_margin_budget.py, unchanged)
- The relevant slack is the larger one: the total loss may exceed the published L+ by up to 12.8% (O_{5/2} alone by up
  to 14.3%) before the claimed DHL[40, 2] fails, conditional on the rest of the argument.
- This is a reading, by one reader, of a Claimed preprint. It does not verify Prop. 4.6 itself (its realization and
  source hypotheses, Thm 4.5, §4.2.4) and does not change the project's bound. 186 stays not adopted (paper/main.tex,
  rem on 186 status): the analytic inputs remain Claimed.
- Status of the companion's majorisation lemmas after this run: 1.4, 1.5, 1.6, 1.7, 2.3, 2.4 each verified as stated
  by one program (helper-written, re-run here). Not checked: Lemma 2.2's proof (spot checks only), the 40-dimensional
  contractions (2.16)-(2.21), profile-power-2 rounding.
