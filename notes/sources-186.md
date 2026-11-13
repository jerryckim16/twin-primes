# Rung 186 (k = 40): source notes

Source: OpenAI, "Improved short gaps between primes", dated 30 August 2026 ("The proof is due to GPT 6 Astra").
PDF: https://cdn.openai.com/pdf/51126fac-1b68-4128-9666-c908bcc16033/short_gaps.pdf (fetched 13 Nov 2026 with
WebFetch, read with pdftotext, Session 11). Companion: [14] "Numerical certificate for prime gaps at most 186"
(short_gaps_numerics.pdf) and the repository github.com/openai/PrimeGaps186 (PrimeGaps186.lean, Challenge.lean,
prime_gap_186_certificate.py; README read 13 Nov; script NOT downloaded or run). Status everywhere: Claimed.

## What is claimed
- Thm 1.1: DHL[40, 2]. Cor 1.2: H1 <= 186 with the 40-tuple (1.3), diameter 186:
  {0,2,6,12,20,26,30,32,36,42,48,50,56,60,68,72,78,86,90,92,98,102,110,116,120,126,132,138,140,146,152,156,
   158,162,168,170,176,180,182,186}.
- Lean 4 formalisation "conditional on numerical integral and cap bounds and on finite-field exponential-sum
  estimates" (Deligne); the exponential-sum bounds of their Lemma A.4 are explicit assumptions.

## Structure (different from Stadlmann / Kintali / Song-Yue / Charton et al.)
- Not a single capped-simplex ratio k J_T / I > 4. One outer Selberg sum A and, per coordinate i, two inner sums
  B_i^(0) (base region) and B_i^(1) (enlarged), C_i = B^(1) - B^(0); square completion (1.6) as in Polymath8b 5.3.
- Divisor-product bounds (1.7): A: x^0.2742997, B^(0): x^0.2499106033, B^(1): x^0.251. Outer square modulus
  x^0.5485994; A B^(0): x^0.5242103033 (needs Polymath8a dense divisibility + a TRIPLY densely divisible adaptation
  of Stadlmann's bilinear estimate, their App. A.4, using Sarajian-Weingartner's criterion); A B^(1): x^0.5252997,
  handled with Stadlmann's prime minorant rho = P - b (exponent 0.5253, mass >= 1 - 2e-5).
- Section 4.1 parameters: k = 40, S = 2742997/2624989, rho* = 2624989/10^7, T0 = 2499106033/2624989000,
  T1 = 2510000/2624989, rho = 262499/10^6; trial F = "rational midpoint step function" on mesh h = S/98304, with
  cap domains H_O, H_0, H_1, H_f (cells listed in [14, 1.1]).
- Criterion, Thm 4.5 (signed minorant): with I = ||F||^2, J_{0,i} = ||1_{L0} V_i||^2, J_{+,i} = ||1_{L1\L0} V_i||^2,
  E_{0,i} = ||V_i||^2 - J_{0,i}, kappa_def = 1/50000, m0 = 49999/50000:
     (rho*/I) sum_i ( sqrt(J_{0,i} + m0 J_{+,i}) - sqrt(kappa_def K_ex E_{0,i}) )_+^2 > 1  =>  DHL[k, 2].
- Lemma 4.8 (numbers, from [14, Lem 2.5]): rho* J^-/I^+ > 500103/500000 and L^+/I^- <= 696075110/10^12 < 697/10^6,
  giving (4.45): (rho*(J^- - L^+) - I^+)/I^+ > 1/50000. Prop 4.7: support failures covered by six classes.

## What reproducing the variational step would need (not started)
1. The step function F and the cap-domain cells from [14] (or by running their script to emit them; any run of
   their script would be "their program", so an independent evaluator of I, J_0, J_+, E_0 and L^+ is needed).
2. An evaluator for step functions on the mesh (exact rationals; the integrals are sums over cells, so this is
   simpler than our polynomial pipeline but the cell count may be large) and for the support-error bound L^+
   (Palm-Chernoff cover, [14, 1.5]) -- the hardest part to re-derive.
3. Record every place where our formulation differs. Analytic inputs (triply densely divisible estimate, minorant,
   App. A) stay Claimed.
Next concrete step: fetch short_gaps_numerics.pdf ([14]) and record the cell lists / the definition of the step
function and of L^+; estimate the cell count.

## Companion [14] "Numerical certificate for prime gaps at most 186" (short_gaps_numerics.pdf, fetched from
## raw.githubusercontent.com/openai/PrimeGaps186/main, 13 Nov 2026, read with pdftotext)
- Framework: NOT the Maynard simplex. Coordinates carry "fragment configurations" (multisets of prime fragments)
  with the measure nu_c = e^gamma c Law(Poisson process on (0, c] with intensity dv/v); a coordinate total has
  Dickman density rho_D(t/c). Erased-coordinate operator E_i F(Y) = int F(Y (+)_i X) d nu(X).
- Trial: 77 integer coefficients (c_{sigma,d} = 10^-10 C_{sigma,d}, Table 1.1), signatures sigma in {(), (2), ...,
  (6), (2,2), (2,3), (2,4), (3,3), (2,2,2)}, radial degrees 0..6; grid N = 98304 cells per coordinate, h = S/N.
- Lemma 2.5: 23685317816e-24 <= I_H <= 23685317890e-24, J_{lambda,H} >= 90248755123e-24 (160-bit Arb production,
  224/192-bit convolutions; "the independent exact replay ... does not recompute their integrals"),
  L^+/I_H^- <= 696075110/10^12 (97 loss components, Tables 2.1-2.6).
- CHECKED HERE (Session 11, exact rationals, Python fractions; trivial but recorded): rho* x 90248755123/23685317890
  - 500103/500000 = 18806715247/236853178900000000 exactly, and 500103/500000 - 1 - rho* x 697/10^6 =
  230382667/10^13 > 1/50000, as displayed in (2.34)-(2.35); also rho* S = 2742997/10^7, rho* T0 = 0.2499106033,
  rho* T1 = 251/1000 as in (1.2). This checks only the final arithmetic, not any integral.
- Lean scope (their Remark 2.7): 149 numerical inequalities are inputs (axioms) of the Lean development.
- Assessment for the ladder: an independent reproduction of 186's variational step means re-implementing the
  fragment-measure forms I_H, J_{lambda,H} (Dickman kernels on a 98304-cell grid in 40 variables, reduced by
  symmetry to finite contractions) and the 97-component loss L^+. This is a separate project, much larger than
  rungs 240/236/212. First feasible sub-step: re-evaluate I_H and J_{lambda,H} for the 77-coefficient trial
  with our own code, after writing down the forms (2.12), (2.15) precisely from [14, Sec. 2.1-2.2].
