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

## OpenAI 186 numerical companion (short_gaps_numerics.pdf): group data for the remaining loss components
- What: for each loss group, the radial interval (b_G, t_G] of (1.22) and the row cores c_t and thresholds V_t used by the clipping (1.26); and the acceptance test that selects the delay recurrence vs the renewal majorant (2.3) for the low kernels. A transcription of these (or the PDF again) is enough.
- Why: rung 186. Session 15 reproduced the 7 raw bounds of group I2old (code/oai186_loss_I2old.py) but had to infer the radial interval and the delay/renewal choice from the table; for the 5/2 groups the clipping (1.26) is active and cannot be inferred. notes/sources-186-loss.md does not contain these items.
- Tried: the PDF supplied in the Session 14 follow-up was not committed (copyright) and is not available to later runs; its GitHub repository (openai/PrimeGaps186) is outside this session's GitHub scope (Session 15, 14 Nov 2026).
- Status: received (14 Nov 2026: the coordinator session fetched the public, Apache-2.0 repository openai/PrimeGaps186 at commit 61340d0b at Jerry's request; the PDF itself, which the licence allows us to redistribute, and the authors' certificate script are now committed in code/third_party/openai186/ (see its README). The group data are (1.22), (1.26) with Lemma 1.6, and (2.3) in the PDF, and build_inputs() in the script. Use the script only as a reference, not as one of our two independent programs.)

## Polymath8b, journal version: "Variants of the Selberg sieve, and bounded intervals containing many primes", Res. Math. Sci. 1 (2014), Art. 12, doi:10.1186/s40687-014-0012-7
- Why: to see whether Remark 8.1's weight (printed in arXiv v4 as a product over 0 <= i <= i' <= H, identically zero; see notes/flags-for-jerry.md, 15 Nov) was corrected in the published version. Low priority.
- Tried (Session 18, 15 Nov 2026): curl https://link.springer.com/content/pdf/10.1186/s40687-014-0012-7.pdf and https://resmathsci.springeropen.com/counter/pdf/10.1186/s40687-014-0012-7.pdf: both HTTP 200 but an HTML "Client Challenge" page instead of the PDF (bot check). Not worked around.
- Status: received (14-15 Nov 2026, coordinator session: the journal version is Open Access, CC-BY 4.0; fetched from https://link.springer.com/content/pdf/10.1186/s40687-014-0012-7.pdf, HTTP 200, 83 pp. Its Remark 45 (= arXiv v4 Remark 8.1) prints the same weight, product over 0 <= i <= i' <= H with (n+i,3) = (n+i',3) = 1 and i' - i <= 4; so the slip is in the published text too. Not committed; notes only.).

## Heath-Brown, "Primes represented by x^3 + 2y^3", Acta Math. 186 (2001), 1-84, doi:10.1007/BF02392715
- Why: parity paper thread 2 (results that break or sidestep parity): the exact theorem, which sieve it uses (Harman's, according to X. Li, arXiv:2111.05403, p. 2), and the structure of its bilinear (Type II) estimate (Lemmas 3.1, 5.1, 9.3, 13.1 as cited by Li), plus any remark on the limits of the method.
- Tried (Session 19, 15 Nov 2026, helper): no arXiv copy found (arXiv math/0007012 is a different paper); intlpress.com Acta archive: HTTP 403; projecteuclid.org: Incapsula bot-challenge page; link.springer.com: paywall (preview only); people.maths.ox.ac.uk/hbrown/: HTTP 404. A third-party mirror was not used. Not worked around.
- What we have: secondary descriptions only (Maynard arXiv:1507.05080v2; X. Li arXiv:2111.05403v1), in notes/sources-hb-x3-2y3.md. Nothing from Heath-Brown's paper enters the parity paper until the primary source is read.
- Status: received (journal scan uploaded by Jerry Kim, 15 Nov 2026, Session 19 follow-up; SHA-256 96ffd7eb...ec10ae, not committed; notes in notes/sources-hb-x3-2y3.md, used in parity paper v0.4).

## Murty, Vatwani: "Twin primes and the parity problem", J. Number Theory 180 (2017), 643-659, doi:10.1016/j.jnt.2017.05.011
- Why: parity paper v0.5, Prop. prop:ss-split. It is essentially their Thm 1.1 (as quoted by Cantarini, arXiv:2607.09110v1, p. 2).
  We need the exact statement, its hypotheses, and whether the unconditional BV-level form is in it.
- Tried (bonus run, 15 Nov 2026): https://mast.queensu.ca/~murty/TwinPrimes-Parity.pdf returned HTTP 200, but the content was an HTML page
  (the Queen's website), not the PDF. No arXiv version found (one standard web search). Not worked around.
- Status: needed.

## Bombieri, Friedlander, Iwaniec: "Primes in arithmetic progressions to large moduli", Acta Math. 156 (1986), 203-251, doi:10.1007/BF02399204
- Why: parity paper open question 3 (fixed-residue level beyond 1/2: "Theorem A" and Theorem 10, known to us only as quoted by Maynard and Lichtman).
- Tried (bonus run, 15 Nov 2026, helper): doi.org redirects to projecteuclid.org, which returned a 1157-byte Incapsula challenge page. Not worked around.
- Status: needed (low priority; the secondary quotes are enough for the open question).


## Restoration-step data of the claimed 182 (GPT-6 Astra / R. Sharifi): repository romyar1/prime-gaps-lean, `inputs/source_certificates/` (the three `independent_components` arrays) or any file listing the 197 restoration components
- What: for each of the 197 source components of the support restoration (Thm 8.1, (8.6); 60 outer, 137 inner; families G1-G6 and C of the bundle's Sec. 9.1), the values A_j and M_j, the low-witness bin windows, the Chernoff parameter beta, the count prefixes R and the dyadic scale Q. These are the inputs of the 197 restoration integrals, the last unchecked numerical piece of rung 182.
- Why: rung 182. The cap quotient (I, J0, J+, T, kappa_true) is reproduced by two programs and the printed restoration arithmetic is re-done exactly (Session 21), but the restoration loss sum (2 sum sqrt(A_j M_j) etc., about 155e-6 of the 211e-6 total) cannot be recomputed without the per-component data, which the expository bundle says are "in the digital supplement".
- Tried: TrialData182_part1..3.lean (in code/data182/) contain the trial function, the 43 + 55 source rows and T0, but no A_j, M_j, beta, R, Q or witness windows (grep for chernoff / witness / beta / window: no hits; Session 22, 15 Nov 2026). The repository is outside this session's GitHub scope, so it was not fetched.
- Status: needed.

## Heath-Brown, "Prime twins and Siegel zeros", Proc. London Math. Soc. (3) 47 (1983), 193-224, doi:10.1112/plms/s3-47.2.193
- Why: parity paper v0.10, Section sec:siegel quotes Heath-Brown's theorem only as stated in Tao-Teraeväinen, arXiv:2109.06291v2, Thm 1.5(i). The original would let us state its exact hypotheses and see how its proof uses the exceptional character at small primes (the first unresolved implication of the 16 Nov route card).
- Tried (Session 25, 16 Nov 2026): curl https://doi.org/10.1112/plms/s3-47.2.193 -> redirected to doi.wiley.com, HTTP 403, a Cloudflare "Just a moment..." challenge page; https://londmathsoc.onlinelibrary.wiley.com/doi/pdf/10.1112/plms/s3-47.2.193 -> HTTP 403, same challenge. Not worked around. No arXiv copy (1983). One standard web search found only secondary statements.
- Status: needed (low priority; the secondary statement is enough for the current section).
