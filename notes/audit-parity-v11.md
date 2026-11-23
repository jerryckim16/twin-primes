# Audit of the parity-paper v1.1 subsection (Section 6.4, subsec:lww-transfer), Session 49, 23 Nov 2026

Fresh-context adversarial helper (general-purpose agent; mathbox not available). It downloaded and read LWW
arXiv:2610.20242v2 pp. 2-5, 7, 10-18, 61-64, 69-70; Li arXiv:2508.18285v3 pp. 1-2; Ding-Wang arXiv:2510.04026v2
pp. 1-2; Wang (Zenodo 10.5281/zenodo.23687596, v1.3) Remark 6.17.

Confirmed: the pointers (range 1/10 < a_i < 1/5 in (2.12); moduli qr <= x^{2/5+o(1)}, p. 13; mu(ah) = (-1)^K mu(h),
p. 15; Cauchy-Schwarz over h at (4.6); Prop. 4.2 in Sect. 4.1, p. 18; (5.1) p. 61; Prop. 5.3 p. 63; 0.677 at Li p. 2
and Ding-Wang p. 2; the EH statement Ding-Wang p. 2 (1.3)). The central implication holds: Q_Y (4.7) and Q_Y^maj
(4.14) do not involve the target; Prop. 5.3 needs only alpha_m = mu(m) R_Z(m) and |beta_n| <= L^C R_Z(n), both from
Vaughan's identity. The count >>_K x/L^2, the bound a <= exp(2K L^{1/5}) and the main term 2 C_2 x check out.

Findings (12) and what was done (all applied in the released v1.1 text):
1. Error: "Type II part O(xL^{-A}) for every target bounded by a power of L" is false for general targets (take the
   sign of the Type II convolution). Restricted to targets G_g with |g| <= L^C; smoothing parameter chosen after K
   (||G_Lambda|| <= L^{1+0.9K}). Fixed.
2. Overstatement: "uses the target in two places only" (LWW also use it in the smoothing error, the removal of
   (a,h) > 1, the prime-power remark, the removal of W). Restricted to targets G_g, "essentially". Fixed.
3. Mis-citation: "our reading of Sections 2-5" (pp. 18-60 not read); bibitem's "read" list inconsistent. Precise
   pointer list in the text; bibitem updated. Fixed.
4. Wording: "Moebius coefficient of the prime variable" -> the coefficient alpha_m = mu(m) R_Z(m) of Vaughan's
   identity. Fixed.
5. Typo-level: mu(ah) = (-1)^K mu(h) only for (a,h) = 1. Fixed.
6. Mis-citation: Wang's Remark 6.17 is an analysis, inserting the roughness indicator into LWW's target; "states no
   consequence" limited to that remark. Fixed.
7. Gap in the dichotomy: add "unless our outline has a gap"; name both propositions; say the statement agrees with
   Hardy-Littlewood (not implausible, only out of reach). Fixed.
8. Vague "goes beyond what that argument gives": replaced by the a <= x^eps comparison and "not given by any of the
   cited sources". Fixed.
9. Convention p^{0.677 - eps} (Li's); Li's 0.679 stated as p^{0.679 - eps}. Fixed.
10. P(D) undefined; D = L^B clashed with LWW's B -> B_1. Fixed.
11. Why each p carries weight << L^2 (uniqueness since l > x^{1-o(1)}). Fixed.
12. "We found no source" -> "in the sources listed, with the search scope". Fixed.
Verdict of the auditor: fit to publish after the fixes (1, 3, 6, 7 required). After the fixes: compiled, no
overfull boxes, 26 pp.; the rendered pages 17-18 checked.
