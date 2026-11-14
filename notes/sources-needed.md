# Sources needed (one entry per source; status 'needed' or 'received')

## Song, Yue: "Bounded Gaps Between Primes: An Upper Bound of 236", IACR ePrint 2026/1893
- Why: rung 236 (witness, reference integers, Remark 4.23).
- Tried: ePrint server returned HTTP 403 to us (session 8).
- Status: received (supplied by Jerry, 13 Nov 2026; notes in notes/sources-236-song-yue.md, data in code/cap6/songyue236_*.json).

## Trial-function data of the claimed 182 (GPT-6 Astra / R. Sharifi): repository romyar1/prime-gaps-lean
- What: the 726 rational coefficients of the 182 trial function (file `formal/TrialData182.lean`, or the `independent_components` JSON, commit b77bf175...; SHA-256 of the trial file is in notes/sources-182.md), and, if available, the 43 + 55 source-row tables and the low-witness / Chernoff kernel parameters of the restoration step, and the exact value of T0.
- Why: rung 182. The expository bundle (https://www.math.ucla.edu/~sharifi/AI/prime_gaps_182_expository_bundle.pdf, read in Session 14, notes/sources-182.md) does not print the coefficients; without them neither I nor J can be recomputed.
- Tried: the bundle's directory lists no data files. The data sit in a GitHub repository outside this session's permitted scope, so I did not fetch them (Session 14, 14 Nov 2026).
- Status: needed.
