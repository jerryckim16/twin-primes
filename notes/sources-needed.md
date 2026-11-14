# Sources needed (one entry per source; status 'needed' or 'received')

## Song, Yue: "Bounded Gaps Between Primes: An Upper Bound of 236", IACR ePrint 2026/1893
- Why: rung 236 (witness, reference integers, Remark 4.23).
- Tried: ePrint server returned HTTP 403 to us (session 8).
- Status: received (supplied by Jerry, 13 Nov 2026; notes in notes/sources-236-song-yue.md, data in code/cap6/songyue236_*.json).

## Trial-function data of the claimed 182 (GPT-6 Astra / R. Sharifi): repository romyar1/prime-gaps-lean
- What: the 726 rational coefficients of the 182 trial function (file `formal/TrialData182.lean`, or the `independent_components` JSON, commit b77bf175...; SHA-256 of the trial file is in notes/sources-182.md), and, if available, the 43 + 55 source-row tables and the low-witness / Chernoff kernel parameters of the restoration step, and the exact value of T0.
- Why: rung 182. The expository bundle (https://www.math.ucla.edu/~sharifi/AI/prime_gaps_182_expository_bundle.pdf, read in Session 14, notes/sources-182.md) does not print the coefficients; without them neither I nor J can be recomputed.
- Tried: the bundle's directory lists no data files. The data sit in a GitHub repository outside this session's permitted scope, so I did not fetch them (Session 14, 14 Nov 2026).
- Status: received (formal/TrialData182.lean pasted by Jerry Kim, 14 Nov 2026, Session 14 follow-up; verbatim copy in code/data182/ with integrity checks code/sharifi182_data.py). The restoration-step tables (source-row inequalities) are covered by its source rows; Chernoff/witness kernel parameters still to be located.

## OpenAI, "Numerical certificate for prime gaps at most 186" (short_gaps_numerics.pdf), Section 2.4 and Tables 2.1-2.7
- What: the forms (2.16)-(2.29) of the support-failure loss L^+ (outer components R_j, V_j, inner components (2.19)) and the parameters of the 97 components, to reproduce L^+/I_H <= 696075110e-12.
- Why: rung 186. Session 14 reproduced the main terms I_H and J_{lambda,H} of its Lemma 2.5 (paper Prop. prop:oai186-main); the loss bound is the remaining numerical ingredient. notes/sources-186-forms.md transcribes only Sections 1-2.3 and the final values.
- Tried: earlier sessions read the PDF from the GitHub repository openai/PrimeGaps186; the local copy was not kept (copyright), and this session's GitHub access is limited to jerryckim16/twin-primes, so I did not fetch it again (Session 14, 14 Nov 2026).
- Status: received (PDF supplied by Jerry Kim, 14 Nov 2026, in the Session 14 follow-up; not committed). Tables 2.1-2.6 transcribed to code/oai186_tables_2_1_to_2_6.json and checked (code/oai186_tables_check.py); source data (1.13)-(1.24) recomputed exactly (code/oai186_support_data.py); loss-cover forms transcribed in notes/sources-186-loss.md.
