# Source transcription: Matomäki-Radziwiłł, Multiplicative functions in short intervals

Source [MR16]: Kaisa Matomäki and Maksym Radziwiłł, "Multiplicative functions in short intervals",
arXiv:1501.04585 [math.NT], **version v4**. The PDF stamp reads "arXiv:1501.04585v4 [math.NT] 15 Oct 2017".
Published in Ann. of Math. 183 (2016). That journal reference comes from the coordinator. It is **not printed in the
PDF**, and the journal version was not consulted.
- File: the coordinator downloaded it to the session scratchpad (dlmr/mr.pdf). It is 41 pages and 421378 bytes,
  produced by LaTeX with dvips/Ghostscript. PDF CreationDate is 17 Oct 2017.
- SHA-256: ec546fdf256b3b3b26b161886c5bab5efb372978ab430c0032e55919f5329277
- It was read with `pdftotext -layout`, and some places were checked with `-raw`. Pages 1 and 3 were rendered to PNG
  so that the absolute-value bars in Thm 1 and Cor 2 could be checked, since those bars are not extracted as text.
  Nothing from the download was run.
- The PDF page number equals the printed page number throughout (p. 1 carries no printed number, and p. 2 is printed "2").
- **Pages read**: pp. 1-14 in full (abstract, introduction, §2 reduction and outline, §3 Halász lemmas); pp. 15-19
  (statements of Lemmas 5-12 and the remarks between them); pp. 21-24 (Lemma 14, Proposition 1 and its remark);
  pp. 29-31 (proofs of Thms 1 and 3); pp. 36-38 (proofs of Cors 2-4 and the start of Cor 5); bibliography pp. 39-41.
  Not read: pp. 19-21 (proof of Lemma 12, §6 moment computation), pp. 24-29 (body of the proof of Prop. 1),
  pp. 31-36 (Thms 2 and 4, smooth-number corollaries), and pp. 38-39 (the rest of Cor 5).

Conventions:
- "Q:" marks verbatim text. Math glyphs are rewritten in ASCII/LaTeX.
- "[transcribed]" marks a display rebuilt from a split layout.
- "Mine:" marks my own remark. It is not a statement of the source.

## (a) Main results

**Theorem 1, pp. 1-2** [transcribed; the bars were checked on the rendered p. 1].
Q: "Let f : N -> [-1, 1] be a multiplicative function. There exist absolute constants C, C' > 1 such that for any
2 <= h <= X and delta > 0,
  | (1/h) sum_{x<=n<=x+h} f(n) - (1/X) sum_{X<=n<=2X} f(n) | <= delta + C' (log log h)/(log h)
for all but at most
  C X ( (log h)^{1/3} / (delta^2 h^{delta/25}) + 1/(delta^2 (log X)^{1/50}) )
integers x in [X, 2X]. One can take C' = 20000."
- Hypotheses: the function is real-valued with values in [-1, 1] (so it is 1-bounded) and multiplicative. Complete
  multiplicativity is not required. The range is any 2 <= h <= X. The result says something only when h -> infinity,
  because the error term contains C' log log h / log h.
- Q (p. 2): "Note that Theorem 1 allows h, delta and f to vary uniformly. For example taking delta = (log h)^{-1/200}
  gives a saving of 2(log h)^{-1/200} with an exceptional set of at most CX(log h)^{-1/100}."
- Q (p. 2): "Already for the Möbius function mu(n) Theorem 1 goes beyond what was previously known conditionally".
  Under the density hypothesis the earlier results held only for h >= x^eps, and under RH only for h > (log X)^A.
- Abstract (p. 1). Q: "for the Möbius function we show that there are cancellations in the sum of mu(n) in almost all
  intervals of the form [x, x + psi(x)] with psi(x) -> infinity arbitrarily slowly."

**Theorem 2, p. 2** (bilinear version, all intervals of length about sqrt(x)) [transcribed]. Q: "Let f : N -> [-1, 1]
be a multiplicative function. Then, for any 10 <= h <= x,
  1/(h sqrt(x) log 2) sum_{x <= n1 n2 <= x + h sqrt(x), sqrt(x) <= n1 <= 2 sqrt(x)} f(n1) f(n2)
  = ( 1/sqrt(x) sum_{sqrt(x) <= n <= 2 sqrt(x)} f(n) )^2 + O( log log h / log h + 1/(log x)^{1/100} )."

**Corollary 1, p. 2 (smooth numbers).** Q: "Let eps > 0 be given. There exists a positive constant C(eps) such that the
number of X^eps-smooth numbers in [X, X + C(eps) sqrt(X)] is at least sqrt(X)(log X)^{-4} for all large enough X."

**Corollary 2, p. 3** (bars checked on the rendered p. 3). Q: "For every integer h >= 1, there exists delta(h) > 0
such that (1/X) | sum_{n<=X} lambda(n) lambda(n + h) | <= 1 - delta(h) for all large enough X > 1. In fact the same
results holds for any completely multiplicative function f : N -> [-1, 1] such that f(n) < 0 for some n > 0."
- The proof (pp. 37-38) deduces it from Corollary 3. Q: "By Corollary 3, there is a positive proportion delta of
  integers n such that f(n)f(n+1) <= 0." The lower bound uses the identity
  f(n)f(n+1)f(2n)f(2n+1)^2 f(2(n+1)) = (f(2)f(n)f(n+1)f(2n+1))^2 >= 0, which uses complete multiplicativity at 2.
  The step from h = 1 to h >= 2 splits n by whether h divides n.
- Mine: this gives only a bound 1 - delta(h). It does not give o(1).

**Corollary 3, p. 4.** Q: "Let f : N -> R be a multiplicative function. Then f(n) has a positive proportion of sign
changes if and only if f(n) < 0 for some integer n > 0 and f(n) != 0 for a positive proportion of integers n."

**Corollary 4, p. 4 (sign changes in almost all short intervals).** Q: "Let f : N -> R be a multiplicative function.
If f(n) < 0 for some integer n and f(n) != 0 for a positive proportion of integers n, then, for any psi(x) -> infinity,
almost every interval [x, x + psi(x)] contains a sign change of f."
- Q (pp. 4-5): "This is an optimal result, since on probabilistic grounds we expect that for any fixed h > 0 there is a
  positive proportion of intervals [x, x + h] of length h on which f is of the same sign."
- For lambda and mu this gives a sign change in almost every [x, x + psi(x)] (Mine: these are special cases of
  Corollary 4. The paper does not state them separately; mu is named in the abstract, p. 1).
- Proof (p. 37): the exceptional set has size Q: "<< X/h^{1/6-eps} + (log X)^{-1/50} for any eps > 0".

**Corollary 5, p. 5 (all intervals of length about sqrt(x)).** Q: "Let f : N -> R be a completely multiplicative
function. If f(n) < 0 for some integer n > 0 and f(n) != 0 for a positive proportion of integers n, then there exists
a constant C > 0 such that f has a sign change in the interval [x, x + C sqrt(x)] for all large enough x."
- **Liouville consequence, p. 5.** Q: "As a consequence of Corollary 5 there exists a constant C > 0, such that every
  interval [n, n + C sqrt(n)] has a number with an even number of prime factors, and one with an odd number of prime
  factors."

**Corollary 6, p. 5 (smooth numbers in almost all short intervals).** Q: "Let psi(x) -> infinity and let u > 0 be
given. Then, for almost all x the number of x^{1/u}-smooth integers in [x, x + psi(x)] is asymptotically rho(u)psi(x)."

## (b) Structure of the proof, as the authors describe it

1. **Restriction to typical n (pp. 6-7).** Q (p. 6): "We will deduce Theorem 1 from a variant where n is restricted to a
   dense subset S_X in [X, 2X] which contains only those n which have prime divisors from certain convenient ranges."
   S is the set of n in [X, 2X] that have at least one prime factor in each interval [P_j, Q_j] for j <= J. Here
   Q_1 <= exp(sqrt(log X)), and the intervals satisfy the spacing conditions (2) and (3) (p. 6). Q (p. 6): "most integers
   in [X, 2X] belong to S". Theorem 3 (p. 7) is the mean-square version on S, with bound
   << (log h)^{1/3}/P_1^{1/6-eta} + 1/(log X)^{1/50}. The n not in S are removed by the fundamental lemma of the sieve
   (pp. 30-31). The conditions on the intervals are [P_1, Q_1] in [1, h] (p. 7), and the choice is Q_1 = h when
   h <= exp((log X)^{1/2}) (p. 31).
2. **Parseval / mean square of a Dirichlet polynomial (p. 7; Lemma 14, p. 21).** The first step is Q (p. 7): "reducing the
   problem essentially to showing that" int_{(log X)^{1/15}}^{X/h} | sum_{X<=n<=2X, n in S} f(n)/n^{1+it} |^2 dt
   << (log h)^{1/3}/P_1^{1/6-eta} + 1/(log X)^{1/50} (5). Lemma 14 (§7, "Parseval bound") does this through Perron's
   formula. Q (p. 21): "This is in the spirit of previous work on primes in almost all intervals". The bound (5) is
   Proposition 1 (p. 23). Q (p. 24): "The 'trivial bound' ... obtained by applying a standard mean-value theorem
   (Lemma 6), is T/X + 1."
3. **Splitting t by the size of prime polynomials (p. 8).** The range of t is split into sets T_1, ..., T_J and U,
   according to the size of sum_{P_j <= p <= Q_j} f(p)/p^{1+it}. A point t is in T_j if j is the smallest index for which
   all subdivisions of that sum are small. Q (p. 8): "The set U is rather sparse (its measure is O(T^{1/2-eps}))".
4. **Factorisation (Ramaré-type identity) (p. 9; §5, pp. 18-19).** Q (p. 9): "When t in T_j we use an analogue of
   Buchstab's identity (a variant of Ramaré's identity [8, Section 17.3]) to extract from the Dirichlet polynomial ...
   a Dirichlet polynomial over the primes in [P_j, Q_j], which is known to be small". The weight is
   1/(#{P_j <= q <= Q_j : q | m} + 1_{(p,m)=1}), see (9). The body version is Lemma 12 (p. 19). Q (p. 18): "We are
   grateful to Terry Tao for pointing out that our 'Buchstab decomposition' is a variant of Ramaré's identity".
   - Footnote 1, p. 9. Q: "In the published version of this paper the term 1_{(p,m)=1} was incorrectly expressed as 1
     leading to a slight gap in the argument that affected only the proof of Lemma 12. This is corrected here."
     Mine: this means the arXiv v4 corrects the Annals text at this point.
   - Then (p. 9) comes a pointwise bound for the prime polynomial together with "a mean value theorem for Dirichlet
     polynomials for the remaining polynomial over m". For j > 1 the m-polynomial is too short. The authors raise the
     large polynomial from the previous range [P_{j-1}, Q_{j-1}] to a power l, see (11) on p. 10, using
     Q: "the assumption that there exists a narrow interval [P, Q] in [P_{j-1}, Q_{j-1}] for which
     |sum f(p)/p^{1+it}| is large, say >= V". The moments are computed in §6.
5. **Large values / Halász-Montgomery on U (pp. 10-11; §4).** On U the problem reduces to
   (log X)^{2+eps} sum_{t in T} |P(1+it) M(1+it)|^2 over well-spaced t, see (12) on p. 10. Q (pp. 10-11): "on the set
   where it is small we are done by simply bounding P and applying Halász's large value estimate to sum |M(1+it)|^2
   over the well-spaced points". Lemma 9 is the "Halász inequality for integers" (p. 16, cited from Iwaniec-Kowalski
   Thm 9.6). Lemma 11 is a new "Halász inequality for primes" (p. 17), proved by duality (Lemma 10). Lemma 8 (p. 15) is
   a large-values count for prime polynomials. Lemmas 6 and 7 (p. 15) are the mean value theorem and its discrete form.
6. **Halász's theorem for the long-interval benchmark (§3, pp. 11-14).** Q (p. 11): "we use Halász's theorem which says
   that unless a multiplicative function pretends to be p^{it}, it is small on average". On U, Q (p. 11): "|M(1+it)|^2
   is always << (log X)^{-delta}, for some small fixed delta > 0, by Halász's theorem on multiplicative functions
   (since f in R and |t| > (log X)^{1/15} is bounded away from zero)". Lemma 2 (p. 12, "essentially due to Granville and
   Soundararajan") gives D(f, p^{i alpha}; x) >= (1/(2 sqrt 3) - eps) sqrt(log log x) + O(1) for 1 <= |alpha| <= x^A and
   real f, using the zero-free region. Lemma 3 (p. 12) applies Halász to the not-quite-multiplicative weighted
   polynomial R(s). Lemma 4 (p. 13, Granville-Soundararajan "Lipschitz type result") compares averages over
   [x, x+y] with y >= X/(log X)^{1/5} to the long average. This is where the long average (1/X) sum_{X<=n<=2X} f(n)
   enters (proof of Thm 3, p. 30).
- Q (p. 8): "for intervals of length h = X^eps it is enough to take J = 1 and most of the work consists in dealing with
  U. In addition, in the special case h = X^eps and f(n) = mu(n) we do not even need to consider the integral over U".

## (c) Limitations stated by the authors

- **Real-valuedness (p. 5).** Q: "Theorem 1 and its variants do not hold for complex valued multiplicative functions as
  the example f(p) = p^{it} shows. However, the result does extend to complex-valued functions which are not
  n^{it}-pretentious."
- **Almost all versus all intervals (p. 2).** Q: "One naturally wonders if it is possible to establish Theorem 1 in all
  intervals of length h ≍ sqrt(X). However, this is not possible in general, since it would require us to control the
  contribution of the large primes factors which is completely arbitrary for general f."
- **Very short intervals in the "all" sense (p. 5).** Q: "one cannot hope to establish general results on sign changes
  of a multiplicative function f : N -> R in all short intervals [x, x + y(x)] with
  y(x) < exp(((2 + o(1)) log x log log x)^{1/2}). Indeed in an interval of this length every integer might be divisible
  by a distinct prime factor."
- **Typical integers have small prime factors.** This is used structurally, through S on p. 6 (item 1 above). The
  authors do not phrase it as a limitation.
- **Multiplicativity.** Every main statement assumes f is multiplicative (pp. 1-5). The factorisation (9) is the point
  where it is used. Q (p. 9): "for completely multiplicative f(n) (the same ideas works for general multiplicative
  functions, but is more transparent in this case)". Not found in the source: an explicit remark that the method
  *needs* multiplicativity or fails without it.
- **Correlations, Chowla, parity.** Q (p. 3): "Chowla's conjecture is believed to be at least as deep as the twin prime
  conjecture [18]" ([18] = Hildebrand, Multiplicative functions at consecutive integers, 1986). The paper's only result
  on lambda(n)lambda(n+h) is the bound 1 - delta(h) of Cor 2. Q (p. 3): "The ternary analogue of Corollary 2 ... is
  surprisingly much easier". **Not found in the source:** any use of the word "parity" or any discussion of the parity
  problem (grep over the full text). Also not found: a statement that the method cannot give o(1) for
  sum lambda(n)lambda(n+h). The paper makes no claim about twin primes beyond the sentence just quoted.

## (d) Consequences for averaged Chowla / later work, as stated

- Q (p. 5): "We carried out this extension in [31] (joint with Terence Tao), where we used this complex variant, together
  with other ideas, to prove an averaged version of Chowla's conjecture." [31] = Matomäki, Radziwiłł, Tao, "An averaged
  form of Chowla's conjecture", ANT, arXiv:1503.05121 (= MRT15 in the paper's bibliography).
- Forthcoming work (pp. 5-6): functions vanishing on a positive proportion of primes (Q: "naturally related to sieves of
  small dimensions"), the case |f(p)| > 1 including the k-fold divisor function, and work with Granville and Harper on
  intervals x^theta with theta > 1/2.
- Q (p. 8): the authors cite their "short note [29]" (arXiv:1502.02374, "A note on the Liouville function in short
  intervals") for the case h = X^eps.
- Not found in the source: Tao's log-averaged two-point Chowla (Tao16) and the entropy decrement argument. Both
  postdate the paper and are not mentioned in v4.
