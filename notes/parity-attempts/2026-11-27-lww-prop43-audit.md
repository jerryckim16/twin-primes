# Audit: route card 2026-11-27-lww-prop43.md (LWW Prop. 4.3, (4.54) ⟹ (4.55), pp. 27-30)

Fresh-context adversarial audit, 2026-11-27. No repository file was edited; this file is new.

## Verdict
- **The mathematics stands.** I re-derived (4.56)-(4.66) and the final display from the printed text, independently of
  the card. That covers the localisation (ψ_{-2}(u) = ψ_1(-u/2) = 0 for |u| ≥ 16, D < 2d_0, P_1, Q_1 ≥ d_0YM, so
  |j-k| ≤ 32), the block count (|det(P^{(0)},P)| < 256d_0Y, ≤ 16 solutions per h from the P_1-range), the PSD and trace
  steps (4.61)-(4.62), the norm identities, (4.63), Hölder (4.64), (4.65), and the bookkeeping
  X_0²L^{8C-2E_0}(d_0Y)^{1/R} → (4.66). I found no error in LWW and no wrong derivation in D0-D7.
- Every formula the card quotes matches the rendered pages: the bar in (4.21), the bars in (4.42) and (4.62),
  c_ν = ⟨e_ν, f_j⟩, the half-open I_j, the window 32, the constants 16/32/256/65, the floor before (4.43), and
  E_0 > A + 4C + 2. The page and equation references are right except for finding 8.
- **The problems are in the chain claim and in what the toy computation is said to show.** The most important: the
  toy check (C) of (4.57) has almost no power. If the kernel's support is widened by 50% (so LWW's window-32 proof
  would no longer apply), (C) still passes 0/260. The localisation is carried by the exact check (A) alone, and the
  card does not say so.
- Counts: **0 errors, 3 gaps, 3 overstatements, 5 slips** (11 findings).

## Source and reproduction
- PDF: curl into a new empty directory /tmp/claude-0/audit-p27-30/. SHA-256
  `7ac341311b4a648c32c2b23b3029e1f4a3202258b55614a33ba7e8282423d000` (matches), 895,874 bytes. The abs page lists v1 and
  v2 only. I ran pdftotext -layout, rendered pp. 19, 24, 27, 28, 29 and 30 at 110 dpi, and read the images.
- `/usr/bin/python3 -I code/parity/lww_prop43_check.py` (numpy 2.5.3). The output is identical to
  `lww_prop43_check.out` except the wall time (8.1 s vs 8.2 s). All of the card's quoted numbers (1,125,768 pairs,
  1,258, 6,636, 40,566, 59, 130/212, 767/1,516, 12/260, 195/260, 75/260, 36.684, 3.6e-15, 2/4, 348, 2,000, 1,200)
  match.
- Mutation runs went to the scratchpad only and nothing was committed. They are quoted in findings 1 and 2.

## Findings

**1. Overstatement (card, D2 "(C)" bullet; Criteria, "A toy operator ... confirms (4.57)"; Computation/Limits, "It
tests the locality").** In the toy, (d_0,Y,M,N) = (2,3,4,10). Block indices run over [2, 72], only 52 are occupied,
and the 65-block window covers almost the whole range. So g_j = g for most j, and the (4.57) check is close to
vacuous. Mutation: replacing ψ_{-2}(u) = ψ_1(-u/2) with ψ_1(-u/3) gives support |det| < 24DY < 48d_0Y, which LWW's
argument does not cover. (C) still reports **0/260 failures**. With ψ_1(-u/4) (support 64d_0Y), it reports only 15/260.
By contrast, the exact check (A) catches the 48d_0Y mutation (92 failures, max |j-k| = 41). Fix: say that (A) carries
the localisation and that (C) only checks the linear algebra. Better still, rerun (C) with MN ≫ 65 (the j-range is
≈ [MN/16, 2MN]; for example MN ≥ 2000) and add the ψ_1(-u/3) mutation as a NEG.

**2. Overstatement (card, D7 "(D)" bullet and Criteria "assembled bound").** The assembled-bound check in (C) has
6-8 orders of magnitude of slack (|⟨f,Af⟩|² = 0.93 against bounds 1.3e6 to 7.3e7) and no negative control, so it
cannot fail under any plausible misreading. The (D) exponent checks are tautological, which the card admits. The
(D) "log (d_0Y)^{1/(2R)} ≤ 4K" check feeds in the derived upper bound 2KJL^{0.2} + 2KL^{0.2} as the input, so it
tests only lg/(2R) ≤ 4K, a one-line inequality, at finitely many L. Its NEG (unlocalised factor) also satisfies
≤ e^{4K} in 248/1200 cases. So "≤ e^{4K} at L ≤ 1e14" is not the O_K(1)-versus-e^{L^{1/2}} distinction the card
describes. Fix: describe these checks as arithmetic sanity checks, not as confirmation.

**3. Gap (card, header "First unresolved implication" and "Role in the chain").** The unresolved reduction is wider
than "(4.44)-(4.52), pp. 25-27". Upstream of (4.44) and unchecked for correctness by any card are:
- p. 24: the primitivity argument (gcd(Dbm, s) = gcd(Dar, n) = 1 via 0 < |t| ≪ Y = o(Z)), which is needed to put the
  terms into S; the identity \overline{f(P)}f(Q) = α_m\overline{α_r}β_n\overline{β_s}; and ρ^{...} = 1;
- pp. 17-18: the insertion of ψ_{-2} and the (4.12) equivalence;
- Lemma 4.1 (pp. 16-17), which (4.47) uses on p. 26 to drop gcd(a,b) > 1.

Fix: "First unresolved implication: the reduction from Q_Y − Q_Y^maj to (4.52), pp. 23-27 (from (4.35); including the
p. 24 primitivity/identity step and Lemma 4.1 as used on p. 26)."

**4. Overstatement (card, header lines 21-24 and "Role in the chain": "both unchecked").** The card does not
mention 2026-11-25-lww-prop42-thinning.md. That card already went through this ground for set-dependence:
- item 1: 1 − w(a,b) (p. 26);
- item 2: (4.49)-(4.51);
- item 3: Prop. 4.3, where it says "I re-derived (4.66) from (4.63)-(4.65)";
- item 12: Section 4.8, (4.149)-(4.157).

None of these is a full correctness check, so "unresolved" is defensible. But "unchecked" without that citation
misstates the record, and the card's "Prop. 4.3 now proved" should acknowledge the earlier partial re-derivation.
Fix: add "partially examined (set-dependence only) in 2026-11-25-lww-prop42-thinning.md, items 1-3, 12".

**5. Gap (card, D7 "Uniformity").** The card says (4.55) holds "uniformly in v and in the dyadic (M, N)". The
operator A_{-2}^C does not depend on α, β or v, so uniformity in v is automatic. Uniformity in M, N and Y, however,
holds only if the implied constant in (4.54) is uniform in M, N, Y (and d_0). Prop. 4.3 assumes this only for d_0
("uniformly for all d_0"). Fix: state the requirement on (4.54) explicitly (uniform in d_0, Y, M, N), and name it as
a burden on the upstream cards (Prop. 4.5(i), M_R bound). Add Y to the uniformity list.

**6. Gap (card, D1, re-derivation of (4.43)).** "m_0 | P_1" needs the K(J+1) primes to be distinct. Within a tuple,
distinctness comes from (4.19). Across tuples, it needs the P_i to be pairwise disjoint (p. 7, (2.12)), and the card
does not cite this. The same disjointness is used in T1 (G(P_1) is a product over ∪P_i). Fix: add "the P_i are
pairwise disjoint (p. 7)" to D1 and to the inputs list.

**7. Slip (card, D3 "Total: #block ≤ 16(2·256d_0Y − 1)").** The count of integers h with |h| < 256d_0Y is
2·256d_0Y − 1 only when 256d_0Y is an integer. That is true, because d_0 = 2^{ℓ_0} and Y = 2^ℓ (p. 16), but neither
fact is stated or listed among the inputs. With LWW's ≤ the count is 16(512d_0Y + 1). Fix: cite Y = 2^ℓ (p. 16), or
write ≤ 16(512d_0Y + 1) ≪ d_0Y.

**8. Slip (card, header line 23 and "Role in the chain": "Prop. 4.5(ii)/(4.96) (pp. 45-46)").** (4.96) is
*stated* on p. 37 and proved on pp. 45-46. Fix: "Prop. 4.5(ii)/(4.96) (stated p. 37, proof pp. 45-46)".

**9. Slip (card, D5 and the (C) result line: "ratio 36.7, below 65 because of the boundary blocks of the toy").**
Over all j ∈ Z the identity Σ_j‖g_j‖² = 65‖g‖² is exact, as the card itself says in D5. The script sums only over
the 52 *occupied* blocks, so it never tests the "= 65" it states. The shortfall comes from the empty blocks as well
as the boundary. (Summing over occupied j is in fact what (4.63) needs, since f_j = 0 elsewhere.) Fix: reword as
"summed over occupied blocks only (which is all (4.63) needs); ratio 36.7 ≤ 65".

**10. Slip (card, D7 constant).** "The constant is at most 65·32²·8192·c_{(4.54)}" applies to |⟨f,Ag⟩|², and after
"c^{1/R} ≤ max(1, c)" it should read 65·32²·8192·max(1, c_{(4.54)}). This is immaterial.

**11. Slip (card, "Terse places / slips", S2; also S1).** S2 is labelled a "slip", but the card says the statement
(O_K(L) intervals) is true. A true weaker bound is not a slip, so S2 should be a remark. S1 ("for sufficiently
large A" should be "for every A") is fair as a wording slip. Fix: relabel S2 as a remark, which gives 1 slip and
3 remarks.

## What I checked and found correct (no finding)
- T1-T6 are accurate descriptions of terse places. T4 is right: eigenvectors with eigenvalue 0 need not be
  C-supported unless the eigenvectors are chosen inside H_C.
- The S3 remark (≤ 2 solutions per h from the P_2-range, since P_2^{(0)} ≥ N) and the S4 remark (strict inequality)
  are correct.
- The log(d_0Y) ≤ 4KL^{0.21} bound and R ≥ 2 for L > 4 are correct. The count of dyadic d_0 is O_K(L^{0.21}), and the
  final exponent is −E_0 + 4C + 1 < −A − 1.
- The NEG controls in (A) (window 16), (B) (constant 1; P_1-range lowered to d_0YM/4), (C) (indefinite A + A*; no
  block count; swapped Hölder) and (D) (E_0 = A + 4C + 1/2; square root dropped) are meaningful, if weak. Two are
  pure sensitivity checks: "≤ 1 per h", a single boolean, and the non-local operator, which fails trivially.
- p. 58 does say "inserting it and the estimate (4.55) for the first sum into (4.52)". Section 4.8 is (4.148)-(4.157),
  pp. 58-61.
