# Route card: what the level of distribution alone gives for twin primes (Bombieri's asymptotic sieve)

Date: 15 Nov 2026, Session 24 (11:34 AM CT slot). Thread 3 of the parity programme ("which hypotheses are known not to suffice").
Not a repeat: earlier cards treated the Friedlander-Iwaniec bilinear axiom (what must be ADDED) and Polymath8b's GEH criteria;
this card asks what Type I / level information ALONE gives, in Bombieri's framework, and what is known to be insufficient.

## Question
For a_n = Lambda(n+2), what does R(nu) for all nu < 1 (EH) give, exactly? Is there a sharp, sourced statement of "EH does not
suffice" beyond the heuristic Polymath8b section 8 argument?

## Success / no-go criteria (fixed before reading)
- Success: (i) Bombieri's theorem and its known limits read in a primary or reliable secondary source; (ii) a precise statement of
  what EH gives for twin primes, with proof; (iii) the first unresolved implication stated sharply.
- No-go: no openable source states Bombieri's theorem (originals: Mem. Accad. XL 1976, Asterisque 18 -- not online).

## What was done
1. Sources read: Ford, On Bombieri's asymptotic sieve, arXiv:math/0401215v1 (SHA-256 4af579db...86b3), pp. 1-5: Bombieri's (1.3)
   as quoted, Selberg's example, Theorems 1-2, Hooley's averaged condition (open for alpha + nu > 1). Debouzy, arXiv:1907.06393v1
   (SHA-256 0743fb64...7838), pp. 1-3, 36-37 (localised Bombieri sieve for twins under EH). Lichtman arXiv:2009.08969v2
   (SHA-256 7f7421c3...4456), pp. 1-2 (Moebius on shifted primes). FI98 p. 1044 (same hash as before): "with (R) alone one cannot
   capture the primes, even for D(x) = x^{1-eps}, which is the case treated by Bombieri".
2. Paper Prop. prop:bomb-twin (proved here, folklore; conditional on Bombieri's theorem applying to this sequence): under EH,
   sum Lambda(n+2)Lambda(n) log n + sum Lambda(n+2)(Lambda*Lambda)(n) = (4 C_2 + o(1)) x log x; hence twin-prime asymptotic <=>
   (Lambda*Lambda)-weighted asymptotic for p-2 = p1 p2; and the factor-2 upper bound.
3. Remark rem:ford-twin: Ford's (1.6) for this sequence = quantitative Moebius-on-shifted-primes (shift -2; Lichtman proves only an
   average over shifts); Hooley's condition = level-alpha version; under EH every alpha > 0 is in Ford's open range.
4. Remark rem:debouzy: probable factor-2 slip in Debouzy's constant (2 S_2 printed, 4 S_2 = 4 C_2 meant): Cor 2.7 with
   nu1 = nu2 = 1 contradicts Bombieri's constant; eq. (65) omits the p = 2 local factor (or, under the coprime-to-2 convention,
   the f0 model sum has density 1/2 not 1). Fresh-context adversarial audit: CONFIRMED; it also found a bug in our script
   (Lambda*Lambda(p^a q^b) dropped for (a,b) != (1,1)), fixed; after the fix the untwisted baseline matches the known
   second-order term 1 - 2 gamma0/(log x - 1) to four decimals.
5. Numerics (Heuristic): code/parity/bombieri_twin_split.py (.out): (P+Q)/(2M) = 0.968, 0.974, 0.975 at x = 1e6, 1e7, 3e7
   (-> 1 under Bombieri's constant; would -> 1/2 under the printed constant of [De19]).

## Classification
Located / literature + folklore reduction (success criteria (i)-(iii) met; (i) only through Ford's quotation, Bombieri's originals
not opened). No parity-breaking content: it sharpens WHERE the barrier sits in the asymptotic-sieve formulation (the
prime / P2 split of the Lambda_2 sum). First unresolved implication: does EH + Hooley's averaged absence of parity bias at some
level x^alpha imply the twin-prime asymptotic (Ford: open for alpha + nu > 1), and can that hypothesis be proved for
mu(p-2) in progressions even for alpha = 0 (open: Moebius on shifted primes)? Paper: open question 7.
Side result: flag (c) for Jerry (probable factor-2 slip in a 2019 preprint's constant).
