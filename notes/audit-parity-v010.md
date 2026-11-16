# Audit of parity paper v0.10: Section sec:siegel (fresh context, 2026-11-16)

Scope: `papers/parity-barrier/main.tex`, Section "The Siegel-zero world" (now lines
1630-1815; the working file has shifted by +6 lines against HEAD e63cd2e, text unchanged),
open question 8 (lines 2085-2091), `code/parity/siegel_class_bias.py` and `.out`.
Sources: TT22 = arXiv:2109.06291v2, text in `/tmp/src/tt.txt` (line numbers below refer to it).
Independent checks: scratch script (Jacobsthal sum for q = 3..1009; CRT identity
sum_{b in G} chi(b)chi(b+2) = -|G|/(q-2); Prop. (2) and (3) on intervals (y, y+x] with
y = 0, 5, 12345, 777777, q = 7, 13, 29, w = 2, 3, 5, random F and F = split primes). All passed.

## Proposition prop:siegel-bias (lines 1681-1740)

1. **OK** (1), lines 1684-1686, 1701-1705. Prime factors of n(n+2) are > w and coprime to q, so
   chi(p) = +-1 and f(p) = chi(p) eps_p. Correct. p = 2 is excluded because w >= 2 puts 2 in W.
2. **OK** (2), lines 1706-1727. Checked line by line: chi(n)chi(n+2) = chi(b)chi(b+2) = +-1 for
   b in G; the summand is >= 1 - 2*1_bad; the union bound gives #bad <= B; N_b >= floor(x/Q) >= x/Q - 1;
   for p <= x/Q, p does not divide Q (p > w, p != q), so each b gives one class mod pQ with at most x/(pQ)+1 elements,
   and the same for n+2 = 0 mod p; for p > x/Q, at most x/p + 1 multiples in I and in I+2, none if
   p > y+x+2. B <= 2|G|(x/Q)s_1 + 2|G|P_1 + 2x s_2 + 2P_2, and dividing by rho x = |G|x/Q gives
   exactly the stated right-hand side. No factor is off. The case n+2 outside I is handled by counting in I+2.
   The hypothesis x >= Q is never used, which is harmless.
3. **OK** (3), lines 1729-1739. |M| <= x/Q+1, since each of the phi(Q) coprime classes meets I at most
   ceil(x/Q) times. CRT: Q = Wq because q > w, G = G_W x {b mod q : b != 0, -2}, so |G_W| = |G|/(q-2); the
   terms with b = 0 or -2 mod q vanish, so the sum over all b mod q is legitimate. The Jacobsthal-type evaluation
   is correct: (c-y)(c+y) = 1 has q-1 solutions, and the count also equals q + sum. Verified numerically. The final
   chain of inequalities and the normalisation are correct. Verified numerically on the 16 cases above,
   including y != 0.
4. **WORDING** lines 1689-1690, 1694-1696. Part (3) is the only place that uses "q odd prime". State
   "chi is the Legendre symbol mod q" (it is, being the unique real primitive character mod an odd prime).
   For composite conductors |sum_b chi(b)chi(b+2)| = |G| prod_{p | q} 1/(p-2) (odd part), which is not small when q
   has only small prime factors. This matters for item 13.

## Error terms and Corollary cor:siegel-typeI (lines 1742-1766)

5. **GAP** lines 1742-1745 vs 1750 and 1761-1765. The paragraph shows the error terms are o(1) only for a
   *fixed* delta (Q <= x^{1-delta}). The corollary takes delta = 1/sqrt(log eta) -> 0, so the paragraph does
   not apply. What is needed: Q P_1/x << 1/log(x/Q) <= 1/log R_0 = sqrt(log eta)/log x, and Q/x <= 1/R_0,
   with R_0 = exp(log x/sqrt(log eta)). Both are o(1) only if log x/sqrt(log eta) -> infinity. That holds
   because x >= Q > q and log eta <= log q + O(1). This follows from Siegel's bound (1.4) of TT22 (tt.txt
   line 101), or ineffectively-free from any bound eta << q^{O(1)}, which gives sqrt(log eta)/log x << (log q)^{-1/2}.
   The proof never mentions this.
   *Fix:* add to the proof: "By TT22 (1.4), log eta <= log q + O(1), and x > q, so
   log(x/Q) >= log R_0 = log x/sqrt(log eta) >> sqrt(log q) -> infinity. Hence Q/x, QP_1/x, P_2/(rho x) are o(1)
   (w fixed)." Also say that eta -> infinity forces q -> infinity (by (1.4)), so q > w and 1/(q-2) = o(1).
6. **WORDING** line 1744. Add "w fixed": the P_2/x term carries the factor 4/rho << log^2 w.
7. **WORDING** lines 1749 and 1752. The same letter epsilon is used for TT's range parameter
   q^{(1+eps)/2} and for the discrepancy size eps x/Q. Rename one of them (for example eps_0 for the range,
   consistent with line 1649). In fact the range lower bound is redundant, because Q <= x^{1-1/sqrt(log eta)}
   already forces x > q.
8. **OK** lines 1761-1765. With x/Q >= R_0: s_2 <= sum over R_0 <= p <= x+2 with chi(p) = 1 is o(1) by
   (eq:tt-exc). The extra prime in (x, x+2] adds <= 1/x. Since F for lambda is {p > w : chi(p) = 1}, the
   conclusion s_1 >= (1-eps)/4 - 1/(4(q-2)) - o(1) follows, and so does the version below R_0. (4/rho) s_2 = o(1)
   because w is fixed.
9. **OK, with a caveat in TT** lines 1655-1658 vs tt.txt 1130-1160. Corollary 3.6 is quoted faithfully:
   the range is q^{(1+eps)/2} <= x <= q^{eta^{1/2}}, the bound is exp(-sqrt(log eta)/2), the sum is over
   exceptional primes p* (chi(p*) != -1, tt.txt 357-361, which includes chi = 0), and R_0 = x^{1/sqrt(log eta)}
   (tt.txt 441). The caveat concerns TT's own proof, which sums (3.23) over 2 <= m <= sqrt(log eta)+1. That only covers
   p* > q^{1/(sqrt(log eta)+1)}, which lies above R_0 when x < q. The corollary only uses x > q, where R_0 > q^{1/sqrt(log eta)},
   so it is unaffected. No fix needed. Optionally note "we use it only for x > q".

## Literature quotations (lines 1638-1662)

10. **OK** Definition 1.4 (tt.txt 92-96): beta = 1 - 1/(eta log q_chi), eta >= 10, primitive quadratic character.
    Theorem 1.5(i) (tt.txt 111-118): O(1/log log eta), uniformly for q^250 <= x <= q^300, attributed to
    [11, Theorem 1] = Heath-Brown, Proc. LMS 47 (1983) 193-224 (tt.txt 3348). This matches the bibliography.
    Corollary 1.8(i) (tt.txt 172-182): O(log^{-1/20} eta) on q^{41/2+eps0} <= x <= q^{eta^{1/2}}. Correct.
    Corollary 1.8(ii): for any fixed distinct shifts, << log^{-1/10} eta on q^{1/2+eps0} <= x <= q^{eta^{1/2}}. Correct.
    Section 1.2 (tt.txt 226-230): "lambda pretends to be like chi", "Lambda = mu*log ... like chi*log". Correct.
    (4.1) (tt.txt 1458): lambda_Siegel := lambda_(<=R) * chi_(>R). The bibliography lists it. Open question 8 cites
    lambda^sharp_Siegel of TT section 6 (tt.txt 249, 1869). Correct.
11. **WORDING** line 1634. "This section reads the statement in the source": HB83 was not opened (line 1662).
    Say "reads the statements in TT22".

## Remark rem:siegel-locates (lines 1768-1794) and open question 8 (2085-2091)

12. **ERROR** lines 1786-1788 ("(3.23) controls them only down to about q^{1/log^{1-eps} eta}, with a bound
    that is not small there"). This is false. (3.23) (tt.txt 977-984) gives, for each m >= 2,
    sum over q^{(1+eps)/(2m)} < p* <= q^{(1+eps)/(2(m-1))} of 1/p* <<_eps m/eta^{1/m}, uniformly in m.
    At m = log^{1-eps'} eta this is log^{1-eps'} eta * exp(-log^{eps'} eta) -> 0. Summing over 2 <= m <= M = log^{1-eps'} eta
    gives << M^2 exp(-log^{eps'} eta) = o(1). Together with (3.22) for p* > q^{(1+eps)/2}, which contributes
    << log_q x/eta <= eta^{-1/2}, the exceptional primes in [q^{(1+eps)/(2M)}, x] contribute o(1). TT's own words (tt.txt 986-987)
    are "non-trivial for primes p* as small as q^{1/log^{1-eps0} eta}". (In fact (3.23) is non-trivial down to about
    q^{(log log eta)/log eta}.)
    Consequences: (a) the sentence must be corrected. (b) Corollary cor:siegel-typeI can be sharpened: the lower bound holds for
    the split primes in w < p < q^{1/log^{1-eps'} eta}, not just below R_0. (c) Open question 8 (line 2086) and bullet 3
    (line 1785) should use that threshold. The statement on line 1660 ("Nothing comparable is stated for the primes below
    R_0") is literally true of Corollary 3.6 only. Add "but (3.23) covers primes down to about q^{1/log^{1-eps} eta}; see ...".
    *Fix:* replace lines 1787-1788 by "(3.23) and (3.22) show that the exceptional primes in
    [q^{1/\log^{1-\varepsilon}\eta}, x] have reciprocal sum o(1). So the lower bound of Corollary~... holds for
    w<p<q^{1/\log^{1-\varepsilon}\eta}. Nothing in TT22 controls the primes below that."
    Then restate the corollary's last clause and open question 8 accordingly, and check the arithmetic in a note.
13. **GAP** lines 1772-1773 and 1777-1778 ("the twisted Type I input (144) of the obstruction fails at the single
    modulus Q"; "the obstruction says nothing"). Section 2 (line ~102) correctly says that the obstruction uses bounds for the
    discrepancies (142)/(144) *on average* over q <= x^theta (EH/BV type: sum_q max_a |Delta| << x log^{-A} x). A single modulus
    with max_b |Delta_b| ~ c x/Q is *consistent* with such an averaged bound as soon as Q >= log^{A} x, which holds throughout TT's
    range. So what is shown to fail is a per-modulus (uniform in q) form of (144), not the averaged input PM8b state.
    The translation from lambda(n)lambda(n+2) to the weight omega = 1 - lambda lambda is also not written: Delta^omega_b =
    Delta^1_b - Delta_b, with |Delta^1_b| <= 1. And (144) is over x <= n <= 2x, while the corollary uses (0,x]. The proposition
    covers (y, y+x], so I = (x, 2x] works with TT at 2x, but this should be said.
    *Fix:* say "(144) in its per-modulus form (uniformly in q <= x^theta, every class) fails at Q = Wq. Whether the averaged form
    fails is not shown: one modulus does not contradict an average bound". Soften "the obstruction says nothing" to "this
    instance of the obstruction's hypothesis is unavailable". Add the omega translation in one line.
14. **ERROR (overstatement)** lines 1780-1782 ("the obstruction rests on Chowla in progressions to moduli x^theta, which is
    strictly stronger than Chowla in any world of this kind"). "Strictly stronger" would need a world where Chowla holds and
    Chowla in progressions fails. The corollary produces one only if the Siegel character has split-prime sum < 1/4 - c below
    the threshold. That is unknown (bullet 4 says so itself), and Siegel worlds are conjecturally empty. "In any world of this
    kind" is also wrong: for a Siegel character with many small split primes nothing is shown. The same applies to the section
    opening, line 1635-1636 ("locates ... the step ... that fails in that world"), and to the section title.
    *Fix:* "So the obstruction needs Chowla in progressions to moduli x^theta. In a Siegel world whose character has few split
    primes below [threshold] (if such a world exists) this fails at modulus Wq although two-point Chowla holds." Change line 1636
    to "the step ... that would fail in that world, under a condition on the small split primes". Consider retitling to "...: where
    the obstruction's hypothesis can fail".
15. **GAP** lines 1782-1785 and open question 8, lines 2085-2088 ("a positive answer to open question 1 at a modulus Wq would
    force ..."; "the twisted Type I input at level x^theta (question 1) would exclude Siegel zeros"). Open question 1 (line ~2013)
    is a *logarithmically averaged* statement, sum_{n<=x, n=c (q)} lambda(n)lambda(n+2)/n = o(log x/q), *on average over q*. The
    corollary needs an *unweighted* discrepancy bound eps x/Q at one x and at the *single* modulus Q = Wq. Neither
    implication is proved: log-averaged smallness does not give unweighted smallness at a given x, and an average over q does not give one modulus.
    Three further restrictions are dropped in the open question. (i) Prime conductor only (item 4); Siegel conductors are fundamental
    discriminants and may be composite. (ii) "Exclude Siegel zeros" can only mean "exclude a sequence of Siegel zeros with eta -> infinity",
    since all statements are o(1) as eta -> infinity. (iii) The condition on q, x: one needs (Wq)^{1/theta} <= x <= q^{eta^{1/2}}.
    *Fix:* phrase both as "a per-modulus, unweighted version of the twisted Type I input at modulus Wq (all classes, error o(x/Q))
    would force ...", and "would exclude Siegel zeros of prime conductor with eta -> infinity". Alternatively, prove a log-averaged
    version of Prop. (2)-(3). This looks routine for the scales t in [Q R_0, x], but the scales t < Q R_0 carry log-proportion
    about log Q/log x <= theta, so one would get only (1 - theta)-type constants. Do not claim it without writing it out.
16. **WORDING** lines 1773-1776. "The class sums ... are then of size >> x/Q, with sign chi(b)chi(b+2)" is proved only *on average*
    over b in G (Prop. (2) is an average; for p > x/Q the bad count is not bounded class by class). "Their total cancels because
    sum_b chi(b)chi(b+2) is small" is not proved: sum_{b in G} S_b is a Chowla sum restricted to (n(n+2), Wq) = 1, which TT
    Corollary 1.8(ii) does not cover.
    *Fix:* "on average over b, with sign chi(b)chi(b+2); heuristically their total cancels ...".
17. **WORDING** line 1770. "Two-point Chowla holds": in the range q^{1/2+eps0} <= x <= q^{eta^{1/2}}, with error log^{-1/10} eta.
18. **OK** honesty rule. Prop. and Cor. carry "Proved here; possibly folklore". Line 1791-1792 says nothing bears on
    twin primes in the actual world. No implied progress on twin primes, apart from the overstatements in items 13-15.
19. **OK** matching of (144) to part (3). Delta_b is the discrepancy against phi(Q)^{-1} times the sum over (n,Q) = 1. That is PM8b's
    normalisation for h = 0 (line ~104 of the paper). G consists of coprime classes, so the hypothesis "every b in G" is
    weaker than "every coprime class". This is consistent (modulo items 13 and 16).

## Remark rem:siegel-num and the script (lines 1796-1815)

20. **OK** The script does check exactly what is claimed. Per class it checks |S_b - chi(b)chi(b+2)N_b| <= 2 Bad_b, with Bad_b
    an exact count. It checks (2) with the proof's bound on B (small/large primes split at x/Q, P_1 = len(small),
    P_2 = len(large), y = 0) and the normalised right-hand side of (2). There are 3 runs x 10 cases = 30, all PASS in the .out.
    The parameters (q, w, Q, x, primes >= 50) match the text. Float sums of +-1 are exact at this size.
21. **WORDING** line 1802. In 20 of the 30 cases the right-hand side of (2) is negative ("bound=-0.37" etc.), so the check of
    (2) is vacuous there. It is non-vacuous only for F empty or s <= 0.05 (q = 163), and for s <= 0.02 (q = 1009).
    *Fix:* say "(2) is non-vacuous in 10 of the 30 cases".
    Part (3) and the CRT/Jacobsthal step are not checked by the script. (I checked them separately; they hold.)
22. **ERROR** lines 1805-1807 ("for random F with s <= 0.2 the mean normalised bias lies between 1-4s and
    prod (p-3)/(p+1)"). The .out contradicts this in 3 of 12 non-trivial cases, where the bias is below 1-4s:
    - q = 163, x = 10^7, s = 0.0220: bias 0.91202 < 1-4s = 0.9122;
    - q = 1009, s = 0.0195: 0.91990 < 0.9220;
    - q = 1009, s = 0.0410: 0.83430 < 0.8360.
    This is not surprising. 1-4s is not the proved bound: the proved bound is 1-4s_1-(4/rho)s_2-..., and it concerns the weighted
    average, not the mean of per-class ratios.
    *Fix:* "lies close to, and in 9 of 12 cases between, ..."; or "lies below prod (p-3)/(p+1) in all cases, and within 0.003 of 1-4s
    or above it". Also fix the script docstring, which calls "1 - 4 s" "the proved lower bound". It is only a crude heuristic
    comparison.
23. **OK** The example numbers 0.394 / 0.203 / 0.450 at s = 0.199 match the x = 5*10^7 row (0.39404, 0.2026, 0.44966). The
    lambda case (5*10^-4 against 0.045) matches the x = 5*10^7 row (4.9956e-4, 4.4757e-2). "The class fixes chi(n), hence the
    parity of the number of inert prime factors" is correct for (n, Q) = 1. The Session 16 entry exists
    (notes/explorations.md line 105).
