# Open question 3: absolute-value, fixed-residue level of distribution beyond x^{1/2}

Date: 15 Nov 2026. Conventions: "Q:" is a verbatim quote from the source (pdftotext; formulas re-typeset in
TeX-like ASCII where pdftotext garbled exponents, nothing else changed), with the page. arXiv pages are given as
PDF pages, which equal the printed page numbers in all files below. "Mine:" is my own remark. "Heuristic:" is
an expectation stated in no source.

Target (main.tex, Sec. `sec:fi`, read first): (R_3) of FI98 Theorem 2 is
`sum^{3}_{d < D L^2} |r_d(t)| <= A(x) L^{-2}`, `L=(log x)^{2^{24}}`, with (R1) `x^{2/3} < D(x) < x`. So it is
summed over ALL cubefree d, with ABSOLUTE VALUES and a saving of a huge power of log x. For a_n = Lambda(n+2),
r_d(t) = psi(t+2; d, 2) - (main term) + O(log t) for odd d, so this is a FIXED residue class a = 2.

Retrieval: all files downloaded with plain curl into the new empty directory /tmp/claude-0/oq3 (HTTP 200,
application/pdf), version checked on the arXiv abstract page (latest listed version taken), read with pdftotext.

| arXiv id (version) | SHA-256 |
|---|---|
| 2006.06572v2 (Maynard I, v2 5 Apr 2021) | 7732d1c035258ef8946b4720c06b8a6c80b1606f5e82bf97c0590474b412de0c |
| 2006.07088v1 (Maynard II, 12 Jun 2020) | 04516b141dfac689f317d533189eabf9b50cec200706159aaa3d8dbe1e25bfb4 |
| 2006.08250v1 (Maynard III, 15 Jun 2020) | 561508e19cd9b56a8cbb68be5c238b213f58aa3973dbec3eb201b7834ad56f4c |
| 2211.09641v1 (Lichtman, 14 Nov 2022) | 78a22cc13b68ab72a4c7ee4cb60bcb9a57d344a0ea60da36e372abd6763c82c4 |
| 2309.08522v1 (Lichtman + Drappeau appendix, 30 Aug 2023) | 665693af46aee2d743e0a1f61c6e35464dc8113e3083b9f3546bfa7de98c55b5 |
| 1402.0811v3 (Polymath8a; abs page: Algebra Number Theory 8 (2014) 2067-2199) | f4b4556f9451ea0524b974376b9dbe4478faf3734847897460274f6bae98b65c |

Not opened: Bombieri-Friedlander-Iwaniec, "Primes in arithmetic progressions to large moduli", Acta Math. 156
(1986). `curl -L https://doi.org/10.1007/BF02399204` redirected to https://projecteuclid.org/euclid.acta/1485890416
and returned HTTP 200 with a 1157-byte Incapsula challenge page ("Request unsuccessful. Incapsula incident ID:
304000070156151499-773846020339532238"). Not worked around. BFI results below are only as QUOTED by Maynard and
Lichtman, not read in the original. BFI II (Math. Ann. 1987) and III (JAMS 1989) were not tried.

## 1. Polymath8a, "New equidistribution estimates of Zhang type", arXiv:1402.0811v3
Q (Theorem 1.1, pp. 2-3): "Let θ = 1/2+7/300. Let ε > 0 and A ≥ 1 be fixed real numbers. For all primes p, let
a_p be a fixed invertible residue class modulo p, and for q ≥ 1 squarefree, denote by a_q the unique invertible
residue class modulo q such that a_q ≡ a_p modulo all primes p dividing q. There exists δ > 0, depending only on
ε, such that for x ≥ 1, we have `sum_{q ≤ x^{θ-ε}, q x^δ-smooth, squarefree} |ψ(x; q, a_q) - x/φ(q)| << x/(log x)^A`,
where the implied constant depends only on A, ε and δ, and in particular is independent of the residue classes (a_p)."
Q (Claim 2.3, p. 8, MPZ^{(i)}[ϖ,δ]): "... let Q << x^{1/2+2ϖ}. If a is an integer coprime to P_I, and A ≥ 1 is
fixed, then `sum_{q ≤ Q, q ∈ D_I^{(i)}(x^δ)} |Δ(Λ1_{[x,2x]}; a (q))| << x log^{-A} x`."
Q (Theorem 2.4, p. 9): "(i) We have MPZ^{(4)}[ϖ,δ] for any fixed ϖ, δ > 0 such that 600ϖ + 180δ < 7."
Mine: absolute values, log-power saving, uniform in a (so covers a = 2), but only squarefree x^δ-smooth (densely
divisible) moduli; level 1/2 + 7/300 = 157/300 ≈ 0.523. No mention of parity or the asymptotic sieve (grep).

## 2. Maynard I, "Primes in arithmetic progressions to large moduli I: Fixed residue classes", arXiv:2006.06572v2
Q (Theorem 1.1, p. 3): "Let a ∈ Z, let ε > 0 and let Q_1, Q_2 satisfy (1.3) Q_1 Q_2^2 < x^{1-100ε},
(1.4) Q_1^{12} Q_2^7 < x^{4-100ε}, (1.5) Q_1^{20} Q_2^{19} < x^{10-100ε}. Then for every A > 0 we have
`sum_{q_1 ≤ Q_1, (q_1,a)=1} sum_{q_2 ≤ Q_2, (q_2,a)=1} |π(x; q_1q_2, a) - π(x)/φ(q_1q_2)| <<_{a,ε,A} x/(log x)^A`."
Q (p. 3): "The main qualitative feature of Theorem 1.1 is that it bounds the error term for primes in arithmetic
progressions with absolute values and a strong error term, whilst simultaneously applying to 'most' moduli."
Q (Corollary 1.3, p. 3): "Let a ∈ Z, 0 < δ < 1/55, A > 0 and Q ≤ x^{1/2+δ}. Then for all but at most
18δQφ(a)/a moduli q ∈ [Q, 2Q] with (q, a) = 1 we have π(x; q, a) = (1 + O_{a,δ,A}(1/(log x)^A)) π(x)/φ(q)."
Q (Corollary 1.4, p. 4): the same bound with `q_1 ≤ x^{1/21}`, `q_2 ≤ x^{10/21-ε}`.
Q (p. 4, "This is the first such result"): "The key qualitative features of Theorem 1.1 are that it gives good
savings over the trivial bound for 'most' moduli of size x^{1/2+δ} and treats the error terms with absolute values."
Q (Theorem A, BFI as quoted, p. 4): "Let a ∈ Z, δ > 0 and Q = x^{1/2+δ}. Then we have
`sum_{q ∈ [Q,2Q], (q,a)=1} |π(x; q, a) - π(x)/φ(q)| <<_a δ^2 x/log x + x(log log x)^{O(1)}/(log x)^3`."
Q (Theorem B, BFI [3, Theorem 10] as quoted, p. 4): well-factorable λ_q of level Q < x^{4/7-ε}, fixed a, saving
(log x)^{-A}. Q (Theorem C, p. 4): Zhang/Polymath, "0 < δ < 7/300 and Q = x^{1/2+δ}", moduli with p|q ⇒ p ≤ x^η.
Q (p. 5): "Theorem 1.1 holds for moduli as large as x^{11/21-ε}, which is slightly larger than the largest moduli
covered by Theorem C (of size x^{157/300-ε}). Indeed, for a fixed residue class, Theorem 1.1 implies that Theorem C
holds with moduli of size up to x^{11/20-ε}."
Q (p. 2): estimates via Kuznetsov "requires us to only consider the situation when a is fixed (or a small power of x)".
Mine: Theorem A is the only quoted ALL-moduli absolute-value result past x^{1/2}, and its saving is a factor δ^2
(trivial bound is about π(x)), not a power of log x. No mention of parity, twin primes or the asymptotic sieve (grep).

## 3. Maynard II, "... II: Well-factorable estimates", arXiv:2006.07088v1
Q (Theorem 1.1, p. 2): "Let a ∈ Z and A, ε > 0. Let λ_q be triply well factorable of level Q ≤ x^{3/5-ε}. Then
`sum_{q ≤ Q, (a,q)=1} λ_q (π(x; q, a) - π(x)/φ(q)) <<_{a,A,ε} x/(log x)^A`."
Q (Theorem 1.2, p. 3): the same for "the well-factorable upper bound sieve weights for the linear sieve of level
D ≤ x^{7/12-ε}".
Q (p. 3): "It appears that handling moduli of size x^{3/5-ε} is the limit of the current method. In particular,
there appears to be no further benefit of imposing stronger constraints on the coefficients such as being
'quadruply well factorable'."
Q (p. 1): "unfortunately we do not know how to establish (1.1) with the summation extended to q ≤ x^{1/2+δ} for any
fixed δ > 0." Q (p. 3, only twin-prime remark): "It doesn't directly improve upon estimates such as the upper bound
for the number of twin primes, but we expect the underlying methods to give a suitable improvement ..."

## 4. Maynard III, "... III: Uniform residue classes", arXiv:2006.08250v1
Q (Theorem 1.1, p. 3): "Let Q_1 ≤ x^{1/10-3δ}/(log x)^C and Q_2 ≤ x^{4/10+4δ}(log x)^C. Then
`sum_{Q_1≤q_1≤2Q_1} sum_{Q_2≤q_2≤2Q_2} sup_{(a,q_1q_2)=1} |π(x; q_1q_2, a) - π(x)/φ(q_1q_2)| <<_C δπ(x) + x(log log x)^2/(log x)^2`."
Q (p. 3): "we are only winning a factor O(δ) over the trivial bound." Theorem 1.2 (p. 3): log-power saving, moduli
q_1q_2q_3 = x^{1/2+δ}, 0 < δ < 1/1000, with Q_2, Q_3 in prescribed ranges (factor near x^{1/10}).
Mine: uniform in a, but restricted moduli and δ < 1/1000; not relevant to level 2/3.

## 5. Lichtman, "... and shifted primes without large prime factors", arXiv:2211.09641v1
Q (Theorem 1.4, p. 2): "Fix nonzero a ∈ Z. Let ε > 0 and let Q, R, S satisfy (1.2) QR < x^{1/2+ε},
QS^2 < x^{1/2-2ε}, S^2 < R < x^{1/32-ε}. Let λ_q, ν_q, η_q, μ_q be complex sequences with |λ_q|, |ν_q|, |η_q|,
|μ_q| ≤ τ(q)^{B_0}. Then for every A > 0 we have `sum_{q≤Q} sum_{r≤R} sum_{s≤S} sum_{t≤S} λ_q ν_r η_s μ_t
(π(x; qrst, a) - π(x)/φ(qrst)) <<_{a,ε,A} x/(log x)^A`." Q (p. 2): "Theorem 1.4 may handle quadrilinear forms of
moduli up to x^{17/32-ε}".
Q (p. 3): BFI [5, Theorem 8] bilinear forms up to x^{29/56}, "only recently extended to moduli up to x^{11/21-ε} by
Maynard [22, Theorem 1.1] ... (even with weights replaced by absolute values)"; "the quadrilinear weights in
Theorem 1.4 are more flexible than the absolute values appearing in [22, Theorem 1.1]".

## 6. Lichtman (appendix Drappeau), "... and Goldbach beyond the square-root barrier", arXiv:2309.08522v1
Q (Abstract, p. 1): "We show the primes have level of distribution 66/107 ≈ 0.617 using triply well-factorable
weights. This gives the highest level of distribution for primes in any setting, improving on the prior record
level 3/5 = 0.60 of Maynard. We also extend this level to 5/8 = 0.625, assuming Selberg's eigenvalue conjecture."
Q (Corollary 1.5, p. 3): "Take nonzero a ∈ Z and let A, ε > 0. Let λ_q be triply well-factorable of level x^ϑ
with ϑ < 66/107. Then `sum_{q ≤ x^ϑ, (a,q)=1} λ_q (π(x; q, a) - π(x)/φ(q)) <<_{a,A,ε} x/(log x)^A`."
Q (Theorem 1.7, p. 4): for θ the exponent towards Selberg's conjecture, ϑ = (5-4θ)/(8-6θ) - ε, uniformly in
0 < |a| < x^ε; θ = 7/32 (Kim-Sarnak) gives 66/107. Q (p. 3): "the prior level ϑ < 3/5 has been a natural barrier".
Q (p. 2, twin primes, upper bound only): "Theorem 1.1. For x ∈ R sufficiently large, we have π_2(x) ≲ 3.2290 Π_2(x)."
Mine: weighted (not absolute values); no mention of parity or the asymptotic sieve (grep).

## Answer to open question 3 (Mine, not from a source unless quoted above)
Largest level read in a source, prime counts in progressions, with saving (log x)^{-A}:
- All moduli, absolute values (needed for (R_3)): 1/2 (Bombieri-Vinogradov, as recalled in all papers above). Beyond
  1/2 only BFI Theorem A (quoted by Maynard I, p. 4; original paywalled): all q ∈ [Q, 2Q], Q = x^{1/2+δ}, fixed a,
  absolute values, but saving only δ^2. Maynard II (p. 1) and Lichtman 2023 (pp. 2-3) both say extending (1.1)/(1.2) to
  x^{1/2+δ} for all moduli is open. I found no post-2014 result for all (or all squarefree) moduli past x^{1/2}.
- Smooth / densely divisible squarefree moduli, absolute values, uniform a: 157/300 ≈ 0.523 (Polymath8a Thm 1.1);
  for fixed a, 11/20 (Maynard I, p. 5, as a consequence of his Theorem 1.1).
- Moduli with a convenient factor, absolute values, fixed a: 11/21 ≈ 0.524 (Maynard I, Thm 1.1 / Cor. 1.4); for
  q ~ x^{1/2+δ} it covers all but O(δQ) moduli (Cor. 1.3), which leaves an exceptional set, not a log-power saving.
- Bilinear / quadrilinear weights, fixed a: 29/56 (BFI, as quoted), 17/32 ≈ 0.531 (Lichtman 2022, Thm 1.4).
- Well-factorable weights, fixed a: 4/7 (BFI Thm 10, as quoted); 7/12 for linear-sieve weights, 3/5 triply
  well-factorable (Maynard II); 66/107 ≈ 0.617 triply well-factorable, 5/8 under Selberg (Lichtman 2023).
Gap: (R_3) needs D > x^{2/3} ≈ x^{0.667}, all cubefree d, absolute values, a = 2. No form, not even the weighted
ones, reaches 2/3: the record 66/107 ≈ 0.617 (5/8 = 0.625 under Selberg) is still below it, and Maynard II calls 3/5
"the limit of the current method" for that method. In the absolute-value all-moduli form the gap is 1/2 → 2/3+.
Mine: I have not checked whether FI98's proof could run with r_d weighted by well-factorable coefficients instead of
|r_d|. As stated, (R)/(R_3) carry absolute values, and the weighted results do not supply them.
Second barrier? Logically, (R_3) at x^{2/3+} and (B) are separate hypotheses of FI98 Theorem 2. FI98 p. 1046 (quoted
in main.tex, read there): "Even proving (R) to such a high level is currently beyond reach." Heuristic: the
level-of-distribution problem is a Type I (linear) problem, while parity sits in the bilinear (B) (Prop. B-parity
of main.tex). Even the full Elliott-Halberstam conjecture would give (R_3) and still leave (B) untouched, so a proof of
(R_3) alone would not break parity, and breaking parity alone would not give (R_3). In that sense it is a second,
independent obstacle. "Independent" here means logically separate inputs: no source read here relates the
square-root barrier to parity, and none of the six papers mentions parity or FI's asymptotic sieve (grep, all
six). Whether the 2/3 requirement could be lowered by a different sieve is not addressed by any source read here.
