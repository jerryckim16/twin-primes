# Audit: route card 2026-11-27-lww-prop44.md (LWW Prop. 4.4 and (4.73), pp. 31-33)

Fresh-context adversarial audit, 2026-11-27. No repository file was edited; this file is new.

## Verdict
- **The mathematics stands.** I re-derived every step of LWW's proof of Prop. 4.4 from the printed definitions,
  independently of the card. That covers (4.67), the bijection Ω ∩ C ↔ primitive odd-first points of Ω', unitarity,
  (4.75), (4.76), the complement (-2c, d - c), (4.77), S, (4.72), the adjoints, (4.73), and (4.54) ⟺ (4.78). I found
  no error in LWW and no error in the card's derivations Q1-Q6.
- The correction to U2 of the Prop. 4.5 card is right. The left side of (4.95) (p. 37) is literally the (4.78) sum
  (p. 33), and Prop. 4.4 is what links (4.78) to (4.54).
- **The problems are in the chain-status claims and in how the computations are described.** The most serious:
  the card says the M_R bound (Sections 4.6-4.7, Prop. 4.6) is "unchecked". Three earlier cards check it
  conditionally. The card also leaves out the one place where (4.73) is an explicit input of an earlier card
  (I7 of the p. 55-58 card).
- Counts: **1 error, 2 gaps, 4 overstatements, 4 slips** (11 findings).

## Source and reproduction
- PDF: /tmp/claude-0/lww-p31-33/lww.pdf, SHA-256 `7ac341311b4a648c32c2b23b3029e1f4a3202258b55614a33ba7e8282423d000`
  (re-verified), 895,874 bytes. abs.html lists v1 and v2 only.
- I rendered pp. 17-24, 27, 31-37, 47, 53 and 58 at 110 dpi myself and read them visually.
- Ran `/usr/bin/python3 -I code/parity/lww_prop44_check.py` (numpy 2.5.3). The output is identical to
  `lww_prop44_check.out` except the wall time (18.2 s vs 18.3 s).
- Mutation runs, scratch only (not committed): sections (A)-(E) were re-run with altered pieces. The numbers are quoted
  in findings 5-7.

## Findings

**1. Error (card; chain status).** Header line 15 says "Also still unchecked: the M_R bound (Sections 4.6-4.7,
Prop. 4.6)". Q6 says "Section 4.7 not checked". "What this does NOT show" says "the M_R bound of Sections 4.6-4.7,
which are unchecked". All three are false for the repository as it stands. Three earlier cards cover this ground
conditionally:
- 2026-11-26-lww-p48-53-norms.md: (4.124)-(4.125) and (4.135), conditional on its U1-U11;
- 2026-11-25-lww-p54-identity.md: the M_R identity, proved under reading R1;
- 2026-11-25-lww-p55-58-emem.md: [I1-I11] ⟹ |M_R| ≪ L^{-2R(E_0+4)} ⟹ (4.78) ⟹ (4.136), under R1.

Proposed correction (header, line 14-15):
> Also not established here: the M_R bound of Sections 4.6-4.7 (Prop. 4.6). It is proved conditionally in
> 2026-11-26-lww-p48-53-norms.md, 2026-11-25-lww-p54-identity.md (under reading R1) and
> 2026-11-25-lww-p55-58-emem.md (inputs I1-I11, under R1). Prop. 4.5(ii) / (4.96) and Section 4.8 are unchecked.

Proposed correction (Q6, last bullet): replace "(checked as arithmetic only; Section 4.7 not checked)" with
"(checked as arithmetic only here; Section 4.7 is checked conditionally in 2026-11-25-lww-p55-58-emem.md)".

Proposed correction ("What this does NOT show", first bullet):
> Not that (4.54) holds. That needs (4.78), i.e. Prop. 4.5(i) (earlier cards, relative to their inputs) plus the
> M_R bound of Sections 4.6-4.7 (conditional, earlier cards, under R1).

**2. Gap (card; role in the chain).** The card does not say which existing input Prop. 4.4 discharges. The only
earlier card that takes (4.73) as an input is 2026-11-25-lww-p55-58-emem.md, as I7 ("(4.73), Prop. 4.4 (p. 32)").
This card discharges I7, relative to LWW's definitions. That is the real role of Prop. 4.4 in the repository's chain,
and the card names only the Prop. 4.5 card's U-list. Proposed addition to the "Role in the chain" bullet:
> It discharges input I7 ((4.73)) of 2026-11-25-lww-p55-58-emem.md, relative to LWW's definitions.

**3. Overstatement (card; U2).** Header line 12-13 says Prop. 4.4 "does discharge the part of U2 that says that
A_1^{Ω',odd} ((4.68)-(4.69)) is the transported form of A_{-2}^C ((4.38)-(4.41))". U2 of
2026-11-26-lww-p37-47-prop45.md contains no such statement. It reads: definitions "read as printed"; (4.69) and (4.91)
are built from "the same expressions" (checked in N2); and "the equality of (4.95)'s left side with the (4.78) sum
is Prop. 4.4, which is not used here". A reading convention cannot be discharged. The only sentence of U2 about
Prop. 4.4 is the misattribution that this card itself corrects. Proposed replacement:
> So it discharges none of U1-U7 of the Prop. 4.5 card (U1 was discharged separately by
> 2026-11-26-lww-lemmaA1.md). It corrects the last sentence of U2 (see the end of the Slips section).

**4. Overstatement (card, against LWW; T2).** T2 says D odd "is automatic ... but not said". LWW says it twice:
- on p. 23, right after (4.35): "Since D, a, b are odd";
- in the very sentence on p. 32 that the card criticises: "we have D | P_1, D | Q_1, and P, Q ∈ C", with P_1 odd
  for P ∈ C.

The step from there to "t ∈ 2Z" is a one-line inference from text that is printed. Proposed replacement for T2:
> **T2 (p. 32, remark).** "t ∈ 2Z" uses D odd. This follows from D | P_1 (same sentence) and P_1 odd, and LWW state
> D odd on p. 23 after (4.35). Not a terse place.

Also Q3, first bullet: change "(it divides the odd P_1; not stated, T2)" to "(it divides the odd P_1; also stated
on p. 23)". The header count "five terse places (T1-T5)" becomes four terse places plus one remark.

**5. Overstatement (script coverage; signs in the integral).** All five toy M_1 sets in (D) and the set in (E)
(k ≤ k_max with every j coprime to k) are symmetric under φ ↦ -φ. So ∫_{M_1} e(nφ)dφ is real and even in n (the
imaginary parts in (E) are ≤ 1.4e-18). The checks therefore cannot see:
- a sign error in the phase (t' - b + a vs -(t' - b + a));
- θ ↦ +2θ used in place of -2θ in M_{-2}.

Mutation: replacing the right side of (D) by I_M1(-(t' - b + a)) gives **0/6,480** detected failures. With an
asymmetric toy set M_1 = [1/10, 1/5] ∪ [1/2, 3/5], the correct identity still holds (0/41 failures) and the sign-flip
mutation is detected (36/41). This does not affect LWW, whose M_1 is symmetric. But the card's "asymmetric toy ψ_1
(so that sign slips are visible)" covers only ψ_{-2}. Proposed addition to Limits:
> All toy major-arc sets are symmetric (as LWW's M_1 is), so (D) and (E) do not detect sign errors in the
> e(θ(·)) phase or in θ ↦ -2θ; those signs rest on the argument in Q3. (A sign-flip mutation of (D) passes 6,480/6,480;
> with an asymmetric toy M_1 it is caught.)

Optional script fix: add one asymmetric arc set to the (D) list, plus a NEG control with the phase sign flipped.

**6. Slip (card Q5 / script (E) diagnostic).** "722 non-zero kernel entries, 38 of them with t = 2(a - b)" is wrong.
The script's `ind_hits` loop counts edges with t = 2(a - b) and ψ ≠ 0, but it ignores η(a/Y)η(b/Y). In 32 of the 38
edges, a or b is 3, so η(3/4) = 0 and the entry vanishes. **Only 6 non-zero entries carry the indicator term.** The
indicator control (max difference 0.38) still shows that the indicator is exercised. Proposed text:
> 722 non-zero kernel entries, 6 of which carry the indicator 1_{t=2(a-b)} (38 edges satisfy t = 2(a-b) inside
> supp ψ, but 32 of them have a or b = 3, where η vanishes).

**7. Slip (card Q5; (4.73) count).** "(4.73) holds for all 413 positions ... (1,239 comparisons)". At R = 1, only
**147 of the 413 positions have a non-zero moment**; the other 266 compare 0 with 0. Proposed text:
> (4.73) holds for all 413 positions and R = 1, 2, 3 (1,239 comparisons; at R = 1, 147 positions have a non-zero
> moment, the rest are 0 = 0).

**8. Slip (card Q1, Q2; descriptions of (A), (B)).**
- (A) draws 3,000 random pairs but tests only the coprime ones: 2,453. The total 3,174 = 720 + 1 + 2,453.
- (A) also does not compute TgE. It enters g' = [[u, -2c], [(u - v)/2, d - c]] by hand and checks only that the
  entries are integers and det g' = 1. (TgE = g' is correct; I checked it by hand.)
- (B): all 989 indicator hits come from the second loop, which uses D = 5 only and positive second coordinates.

Proposed text for Q2:
> Also g' (entered as [[u, -2c], [(u-v)/2, d-c]], i.e. TgE computed by hand) has integer entries and det 1, for
> 2,453 random coprime odd pairs.

Proposed text for Q1: "(989 hits, all at D = 5)".

**9. Overstatement (negative controls, and two positive checks).** The card says the 10 controls are "all failing as
they must", as if each were evidence that the checks discriminate. Five of them are mutations of the positive
pipeline and are meaningful:
- NEG D one copy;
- NEG D phase;
- NEG E kernel / one copy / ψ sign;
- NEG E r_P;
- NEG E (4.73).

I also confirmed that a G_{-2} mutation using r_P in place of -2r_P is caught: max |ΔA| = 0.034, and 30 of the 413
positions differ in (4.73).

The others are controls by construction:
- **NEG A** tests the gcd identity for even u, v, outside its domain. It never runs the bijection check.
- **NEG B** compares det(T~P, T~Q)/D with -t/2 for a matrix of determinant -1. It fails whenever t ≠ 0, whatever the
  indicator does.
- **NEG C** (+2r_P) is a direct inequality test of the same kind.

In (E), two positive checks are tautological:
- the "unitarity" check (Pm·Pmᵀ = I) holds for any injective index map, which is already asserted;
- the S check holds because S does not depend on P.

Proposed addition to Limits:
> NEG A, NEG B and NEG C are controls by construction: they do not perturb the positive checks. The unitarity and S
> checks in (E) are tautological given the asserted bijection. The discriminating controls are those of (D) and (E).

**10. Gap (card Q5 labels).** Q5 is labelled "Proved here; Computed (E)". But the toy model is built only on S ∩ C:
- positions with an even coordinate are never constructed;
- σ is constant, so the adjoint is the conjugate transpose.

So the T4 content (C-support preservation, adjoint in H = adjoint in H_C) is not exercised by (E). It is argument
only. Proposed change: label the adjoint bullet of Q5 "Proved here (argument only; (E) is built on S ∩ C and does not
test it)", and add the same to Limits.

**11. Slip (card Q2).** "This is the set used later in (4.90) (2 ∤ z_1, primitive)." (4.90) (p. 35) is a condition on
the relative position z = (g')^{-1}TQ, not on TQ. The two sets correspond under TQ = g'z, because g' ∈ SL_2(Z) and
(g'z)_1 = uz_1 - 2cz_2 ≡ z_1 (mod 2) for u odd. Proposed text:
> This set corresponds, via TQ = g'z (g' ∈ SL_2(Z), (g'z)_1 ≡ z_1 mod 2 since u is odd), to the z-conditions
> "primitive, 2 ∤ z_1, g̃z ∈ Ω'" of (4.90).

## Checked and confirmed (no finding)
- **(4.67):** det T = -1/2, so t' = -t/2, and t = 2(a - b) ⟺ t' = b - a.
- **(4.68):** T^{-1}(u, v) = (u, u - 2v), hence N ≤ u - 2v ≤ 2N.
- **Bijection:** both gcd identities hold.
- **(4.75):** ψ_{-2}(t/Y) = ψ_1(-t/(2Y)) = ψ_1(t'/Y), with no symmetry of ψ_1 used.
- **(4.76):**
  - t - 2(a - b) = -2(t' - b + a);
  - LWW's substitution φ = j + 1 - 2θ maps [j/2, (j+1)/2] onto [0, 1] with dθ = -dφ/2;
  - it uses 1-periodicity of 1_{M_1}, and the dropped phase e(-(j+1)(t' - b + a)) = 1 (T3 is accurate).
- **(4.77):** P_1(d - c) + (P_1 - P_2)c = P_1d - P_2c = 1, so r_{TP} ≡ -2c/P_1. (4.26) and (4.27) depend on r only
  through ||m r||, with integer m depending only on p.
- **(4.72), (4.73):** the operator algebra and the adjoint argument via P_C A P_C = A.
- **(4.54) ⟺ (4.78):** termwise, after summing over P ∈ Ω ∩ C.
- **Chain:** p. 58 says "(4.95) gives (4.78) ... (4.73) then gives (4.136)". Prop. 4.4 is not used in the proof of
  Prop. 4.5(i) (p. 37), which uses only the definition of A_1^{Ω',odd} and TQ = g'z.
- **The script builds the two operators independently, as claimed:**
  - The image space is enumerated from (4.68) and is not obtained by mapping.
  - U_T is an index lookup into that enumeration.
  - The primed kernel uses det(TP, TQ), the indicator b - a and ∫_{M_1}.
  - The unprimed kernel uses det(P, Q), ψ_1(-t/(2Y)), the indicator 2(a - b) and the M_{-2} preimage formula. The
    preimage formula is tied to the membership definition only by 4 Riemann sums on one arc set.
  - G uses r_{TP} from TP's own extended-Euclid complement, against -2r_P.
  - Shared code (edge structure, the coefficient d_0/D·η·η·ρ, `good`) implements factors that are the same by
    definition.
