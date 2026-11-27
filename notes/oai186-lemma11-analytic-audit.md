# Audit of notes/oai186-lemma11-analytic.md and code/oai186_lemma11_check.py

Fresh-context adversarial audit, 27 Nov 2026. Nothing committed.

## Method

- I fetched [8] with curl into the new empty directory `/tmp/claude-0/oai186-l11-audit/`: `short_gaps.pdf`,
  SHA-256 `456f05e0...0b30`, which equals the value recorded in the note. I read it with `pdftotext -layout`.
- [14] was read from `code/third_party/openai186/short_gaps_numerics.pdf` (copied into `.../c14/`), SHA-256
  `79190b2c...0c31`, which also equals the recorded value.
- Nothing from the authors' repository was opened or run.
- I ran `/usr/bin/python3 -I code/oai186_lemma11_check.py`: exit 0, 112 checks, 0 failures. The output matches the
  committed `.out` apart from the runtime line.
- I wrote three independent scripts in the session scratchpad:
  - `indep.py` recomputes the ladders from my own reading of [14] (1.13)-(1.16). It re-checks every retained row
    against my own transcription of [8] Props 2.16-2.18, Cor 2.19 and Prop 2.22, including the τ-reduced form.
  - `ends.py` evaluates the hypotheses at the printed ω-enclosure endpoints, which is [14]'s own affine argument.
  - `mut.py` runs 9 source mutations of the check script.

## 1. Transcription of the hypotheses of [8]: correct

I checked each item against the text of [8]. All strict/non-strict choices in the script match [8].

- **Prop 2.16 (p. 10).** Hypotheses: 0<ω<1/12, 0<δ<1/4+ω, 0<σ<1/2, 68ω+14δ<1, and (2.11), which is
  54ω+15δ+5σ<1 (r=1) or 56ω+16δ+4σ<1 (r=2). All strict; the script matches.
- **Prop 2.17, (2.12).** 1/18+28ω/9+2δ/9 < σ < 1/2, strict on both sides; the script matches.
- **Prop 2.18, (2.14).** ω, δ, σ > 0, 72ω+24δ<1, 48ω+16δ+4σ<1 and 64ω+20δ+2σ<1; the script matches.
- **Cor 2.19, (2.15) and its proof.** The proof needs σ>1/10, σ>2ω, (2.12), and σ := 1/10+(3-240ω-80δ)/40 at
  r=3; the script matches.
- **Prop 2.22, (2.24) and its proof.**
  - The hypotheses are 0<ω<1/12 and 0<δ<1/4+ω, plus the three strict bounds of (2.24).
  - At r=1,2 it also needs 68ω+14δ<1 and (2.11) with σm; at r=3, (2.14) with σm.
  - The proof needs σm+τ in place of σm and the three bounds lowered by τ, for some fixed 0<τ≤10^-10.
  - Type III needs σ3 ∈ (second lower bound, 19/200-τ). I re-derived this from (2.13): with lengths in
    [x^{0.19-τ}, x^{0.405+τ}] and pairwise products ≥ x^{0.595-τ}, the binding constraints are
    σ3 ≤ 0.095-τ (from both N_i ≤ x^{1/2-σ3} and N_iN_j ≥ x^{1/2+σ3}). So "1/18+... < 19/200-τ" is exactly
    the existence condition.
  - Lemma 2.20 at length x^{c*-τ} gives 4(1/2-c*+τ)+28ω+8δ<1 ⇔ 1/4+7ω+2δ < c*-τ, as the note's R4 says.
  - The script matches all of this.
- **(2.19) constants.** a*=0.40481, b*=0.59519, c*=0.33856, printed as exact.
- **Lemma 4.1 (pp. 24-25).** It needs s_D≤S, s_E≤T, Q>R^B, guard (i) B+ξ≥2T and guard (ii)
  B+ξ≥max(2S-T, 2T-S), all non-strict. Exponentiating these against Prop 2.4 gives exactly D0²≤XY E0,
  E0²≤XY D0, E0²≤XY and pD_{≥p}≤XY/E0 ⇔ H_{2,ξ}≤a+ξ, which I re-derived myself.
- **Prop 4.2 / Prop 2.3.** These need (4.6) A+C≤B+ξ (non-strict), and φ_D, φ_E nonnegative and nondecreasing with
  φ_D+φ_E=3u. Against (2.1), these give f(p)D_{≥p}≤A ⇔ H_{φD,ξ}≤A, and g(p)≤B_cap ⇔ φ_E(M_ξ)≤C, since φ_E is
  nondecreasing.
- **Retreat.** E_r in (2.5) sums over q ≤ x^{1/2+2ω-ε}, q ∈ D^(r)(x^δ). So ρ*B⁺<1/2+2ω, together with
  Y=R^ξ≤x^δ (with D^(r)(Y) ⊆ D^(r)(x^δ) for Y ≤ x^δ), is the right pair of conditions, in the right direction.
- **The full domain H_f.** It has totals up to (N-2)h > T1, but no source is needed there. Its face term enters
  with b_h<0 and "cancels from D" ([8] (4.32)), so the radius checks over outer/base/enlarged only are complete.

## 2. Row parameters versus [14]

[14] does not print rows individually; it prints the generating data (1.13)-(1.15). So a "row spot-check" means two
things:
- checking that the script transcribes (1.13)/(1.14) correctly;
- recomputing rows independently and comparing them with every printed checkpoint.

**Transcription.**
- (1.13): g0, ε_o, ε_n, τ, σ0, σ_{m,τ}, Ω_o, Ω_n, ρ, ρ*, S, T1, T0, e and ζ all match.
- (1.14): all six (c, s) pairs match.
- (1.15): the min/stop rule matches.
- (1.20)-(1.24): the source-row sets, the ξ_G/U_G/b_G/t_G assignments and the z_G/h, p_G/h values match.

**Independent recomputation** (`indep.py`, my own code). I compared eight rows:
- (o,0) 10^6ω = 2533.721389;
- (o,11) 5695.945118;
- (o,23) 8854.930969;
- (o,27) floor(B/h) = 187773, δ = 2.61048e-4;
- (n,12) 7267.912953;
- (n,24) 10326.154435;
- (n,38) floor(B/h) = 188254, δ = 8.8236e-6, ξ = 3.36138e-5;
- (n,42) δ = 89999/10^11.

All eight agree with the script's values and with the printed enclosures, floors, and least density. The row
counts (29, 43), W_{n,3} = 0.01265075 > Ω_n, and floor(B/h) at (o,28) = 188087 and (n,39) = 188256 also agree. My
independent hypothesis check found no failing retained row, including the level bound 1/2+2ω ≤ 0.53 (§3, G1).

## 3. Issues

Classification: **error** = a wrong mathematical claim or check that matters; **gap** = something needed but not
checked or argued; **overstatement** = a claim stronger than the evidence; **slip** = a local inaccuracy that
changes nothing.

### Errors: none

The verdict that every retained row satisfies the [8] hypotheses is correct. I reproduced it independently.

### Gaps (3)

- **G1. A hidden level hypothesis of Prop 2.22's proof is not mentioned.**
  - Problem: Lemma A.8 and Lemma A.9 ([8] §A.6, used in the proof of Prop 2.22) need level Q ≤ x^{0.53}, and
    Lemma A.1 handles endpoints for Q ≤ x^{0.53}. Prop 2.22's statement has only 1/2+2ω < b* = 0.595, so this is
    an extra requirement of the proof.
  - Why it holds: the first bound of (2.24) forces ω < 0.01265, so 1/2+2ω < 0.5253 holds automatically. The
    largest new ω is Ω_n, giving 0.5253; ω_s gives 0.5062.
  - Fix: add a row to the note's §2/§3 and one check `1/2+2w <= 53/100` to the new-row conditions.
- **G2. The role of τ is not fully argued.**
  - Problem: the proof of Prop 2.22 picks a τ ≤ 10^-10 and may "decrease τ further" (for σ3). [14] fixes
    τ = 10^-10. Every τ-dependent condition (σm+τ in (2.11)/(2.14), the bounds minus τ) is monotone: it only
    becomes weaker as τ decreases. So the check at τ = 10^-10 covers every τ' ≤ 10^-10 that [8]'s proof may
    choose. The note says only "τ = 10^-10 is allowed".
  - The note also does not say that τ never binds. The least τ-sensitive margin is 9.69e-6 (first (2.24) bound,
    (n,38)), four orders of magnitude above τ. Mutation tests confirm this: replacing σ_{m,τ} by σm, or removing
    "-τ" from all three (2.24) bounds, still gives 112/112 on the main checks.
  - Fix: state the monotonicity and the non-binding margin explicitly in the note's row 1/row 5.
- **G3. The negative controls leave most check families unexercised.**
  - The script's own checks are sound under mutation: guard r=1 with 2S fails, old r=3 with σ=1/10 fails, one extra
    retained row fails, and one extra T1 cell fails.
  - But no negative control perturbs input to exercise:
    - the Type III condition (2.12) (deleting it entirely still gives 112/112);
    - the transfer guards;
    - the radius checks;
    - band coverage;
    - the cap running-minimum;
    - the (1.5) masks;
    - the old r=3 or new r≤2 bilinear conditions specifically.
  - Fix: add controls through `build(over)` and the main check code, not inline arithmetic. Suggested controls:
    - σ0 := 0.1555 makes (2.12) fail at r=2;
    - T0 shifted by +e·2 makes the r=1 guard fail;
    - one more cell in a Tbox makes the radius check fail;
    - drop the last retained row and coverage fails;
    - change one printed cap and the (1.18) comparison fails.

### Overstatements (2)

- **O1. "11 negative controls, all caught".** Only some of the 11 are true negative controls:
  - Four perturb inputs through `build`/`sec_dist`: ε_o=0, c*−1e-5, σ0=1/10 and τ=1e-4. A fifth, ρ*=ρ, perturbs
    through `build` but re-implements the check inline.
  - Two are positive assertions labelled NEG: "(o,28) is excluded" and "guard is not vacuous".
  - Three are inline arithmetic on hard-coded constants, and none of them goes through the check code: the O2
    z+1 cell, the I2new p+1 cell, and δ_s+1e-4.
  - One tests ladder termination, not a hypothesis: Ω_n+1e-5.
  - Fix: say "5 input perturbations caught, plus 6 tightness/sanity assertions", and relabel the two positive ones.
- **O2. R1 is presented as a wording caveat on [14]; it is not one.**
  - [14]'s proof argues by affinity "at the endpoints" of the printed ω-enclosures. The upper enclosure endpoint
    for (n, r=3) is 12650·10^-6 = Ω_n. There δ = c−sΩ_n−ε_n = 89999/10^11 exactly (`ends.py`).
  - So "the least positive density is 89999/10^11" is literally correct for [14]'s method, and the note's
    "verified as stated, with one wording caveat" should drop the caveat.
  - Relatedly, the note's step 7 ("true; not needed") is the one step it did not check. I checked it: at all 12
    enclosure endpoints, with δ = c−sω−ε, every hypothesis holds with least margin 8.9999e-7 > 10^-8. So "every
    line of the proof checks out" is now justified.
  - Fix: rewrite R1 accordingly and record the endpoint check, optionally as a script check.

### Slips (5)

- **S1. Several lower bounds are rounded up.**
  - §3 row 3: "68ω+14δ<1 ≥ 0.31" (actual least 0.30677, o r=2 row 23) and "(2.12) ≥ 0.0155" (actual 0.015451).
  - Row 5: "third ≥ 0.0699" (actual 0.069895) and "first (2.24) bound 9.69e-6" (actual 9.6856e-6).
  - Row 9: "least slack 0.0888" (actual 0.088762).
  - Fix: round down (0.306, 0.0154, 0.0698, 9.68e-6, 0.0887).
- **S2. A script label claims more than the check tests.** The label "a_{n,0} < a_{o,0}, a_{n,24} < a_{o,24}, and
  b_{o,t}, b_{n,t} increasing" (section [5]) does not test the b-monotonicity, although it follows from the separate
  "B strictly increasing" check. Fix: add the b test or trim the label. Similarly, "τ = 10^-10 is allowed" is a
  tautology (it checks the input against itself); relabel it as a parameter-range check.
- **S3. R4 misreads why the third bound is needed.** R4 says the third (2.24) bound, lowered by τ, is "needed by
  (2.18)". [8] needs only b*+τ ≥ θ+ε0, i.e. b* > 1/2+2ω ("since 1/2+2ω<b*"). The τ-lowered form comes from [8]'s
  blanket prescription and is stronger than needed. Fix: say so.
- **S4. The ρ*=ρ control changes more than ρ*.** It is implemented as `rho_star_shift`, which also changes S, T0
  and T1, because they are defined through ρ*. The label "rho* = rho" understates the perturbation. Fix: note this,
  or hold S, T fixed in that control.
- **S5. A note table omits a condition the script checks.** The note's §2 table row for Prop 2.18 omits ω, δ, σ > 0.
  The script does check them. Fix: add them to the table.

## 4. Verdict on the note

Its central claim holds, and I reproduced it independently:
- every retained row satisfies the exact hypotheses of [8] Props 2.16-2.18, Cor 2.19 and Prop 2.22 (τ-reduced),
  Lemma 4.1 and Prop 4.2;
- the retreat, coverage, cap, group and inner-square claims of [14] Lemma 1.1 hold.

Counts: 0 errors, 3 gaps (G1 hidden x^{0.53} level, which holds; G2 τ monotonicity and non-binding; G3 control
coverage), 2 overstatements (O1 negative-control count; O2 R1/step 7), 5 slips. None of them changes the
conclusion. The status should stay "Claimed", with the analytic content of [8] unverified, as the note says.
