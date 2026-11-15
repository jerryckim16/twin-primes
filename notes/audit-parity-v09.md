# Audit of parity paper v0.9 (Session 24, 15 Nov 2026)

Mathbox skills not available; two fresh-context general-purpose agents used as adversarial auditors.

## Audit 1: the Debouzy factor-2 claim (Remark rem:debouzy)
Verdict: CONFIRMED. The auditor tried to rescue the printed constant 2 S_2 (normalisation of S_2, of Lambda^{(k)}, of script-F
(eq. 59), the model sum (Lemma 2.6, (61), (67)), Ford's normalisation) and failed. The factor is lost in V_sigma/V_sigma0
((65): product over 3 <= p <= z; or, under the coprime-to-2 convention, the f0 model density 1/2 vs sigma0(d)F(y) = y/d
before (66)). Her p.1 "sum Lambda(n)Lambda(n+2) ~ S_2 X" is off by the same factor.
Found a BUG in code/parity/bombieri_twin_split.py: (Lambda*Lambda)(p^a q^b) was set to 0 unless a = b = 1. Fixed
(2 log p log q for p != q, all a, b >= 1); table recomputed; the fix strengthens the claim. After the fix the untwisted column
matches 1 - 2 gamma0/(log x - 1) to within 4e-4.

## Audit 2: Section sec:bomb, table, open question 7, bibliography, abstract
Proof of Prop. prop:bomb-twin: correct. Errors (all fixed):
1. p+2 = p1p2 written for p-2 = p1p2 (abstract, text, changelog, main paper, README, notes). Fixed everywhere.
2. Selberg-type twisted sequence attributed to Ford's Theorem 1; it is the analogue of Selberg's example 1 + lambda(n). Fixed.
3. "R(nu) for all nu < 1 is a form of EH, as Ford notes": Ford only says it is conjectured; it follows from EH. Fixed.
4. Bombieri reference: Ford's [1] is "On twin almost-primes", Acta Arith. 28 (1975); Asterisque 18 was not cited by Ford. Fixed.
5. "reproduces to four decimals" -> "to within 4e-4". Fixed.
Gaps fixed: R(nu) is used only through the assumed conclusion (said in the proof); conditional framing restored in the text and
abstract ("would"); Ford's "essentially ... (and no other information about the sequence)" restored; rem:ford-twin and open
question 7 rewritten (Ford's constructions are for one fixed nu and say nothing for sequences with R(nu) for all nu < 1;
the hypothesis and the implication are separately open); prime powers in the Hooley display (<< x^{1/2+eps}); pages 36-38;
D_gamma definition; which ratio tends to 1/2; table header abbreviated. Wording items 12-17 applied.
