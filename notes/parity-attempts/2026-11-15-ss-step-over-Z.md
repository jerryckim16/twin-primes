# Route card: the step of Sawin-Shusterman's twin-prime proof that has no integer analogue (15 Nov 2026, bonus run)

Status: **located (reformulation; proved here, elementary, possibly folklore; compare Murty-Vatwani Thm 1.1 as quoted secondhand)**.
The twin prime conjecture is open. Nothing here claims progress on it.

## Question
Sawin-Shusterman (SS19, arXiv:1808.04001v2) prove the twin prime asymptotic in F_q[T] for odd p and q > 685090 p^2.
Which step of their proof has no integer analogue? And if the other steps are transposed to Z, what exactly is left?

## Success and no-go criteria
- Success: find an integer statement S that is not visibly as hard as twin primes and not visibly parity-blocked, with
  S => twin primes by SS's bookkeeping.
- No-go: the residual statement is a binary correlation of mu with primes at the range where it carries the parity
  information, i.e. as hard as the problem itself.
- Cheapest decisive check: write SS's split, (5.7) and (6.19)-(6.22), over Z and see what is left.

## Sources read
- SS19 v2, SHA-256 5b762a08...0e687: Thm 1.1 (p. 2), Thm 1.7 (p. 5), Thm 1.9 (p. 6), Lemma 3.2 (p. 15), Thm 4.5 (p. 22),
  (5.7) (p. 25), Cor 6.1 (p. 27), Thm 6.3 (p. 30). Transcription by a helper: notes/sources-sawin-shusterman.md; the key
  quotes were re-checked against the text by the coordinator.
- Lichtman arXiv:2009.08969v2, SHA-256 7f7421c3...a4456, p. 1: Sum_{p<=X} mu(p+h) = o(pi(X)) is called a folklore
  conjecture; it is proved on average over h <= H.
- Cantarini arXiv:2607.09110v1, SHA-256 15625c85...afc9c, pp. 1-3: it quotes Murty-Vatwani (JNT 180 (2017)) Thm 1.1.
  Under EH_theta and EH^{mu_h}_{1-theta}, Sum Lambda(n)Lambda(n+h) ~ S(h)N is equivalent to Sum Lambda(n)mu(n+h) = o(N).
  The original could not be opened: the Queen's URL returned an HTML page instead of a PDF; see notes/sources-needed.md.

## What was done
- Over Z: Lambda(n) = -sum_{d|n} mu(d) log d. Split at d = D.
  - The part d <= D is a Type I sum for primes p = 2 mod d. Bombieri-Vinogradov handles it at D = x^{1/2}(log x)^{-B};
    EH handles it up to x^{1-c}.
  - The part d > D equals exactly -T_D(x), where T_D = Sum_{e<x/D} Sum_{D<d<=x/e} mu(d) log d Lambda(de+2).
  - The main term is -x Sum_{d odd} mu(d) log d/phi(d) = 2 C_2 x, by the Euler product.
- Paper v0.5, Prop. prop:ss-split, unconditionally: the twin prime asymptotic holds iff T_D(x) = o(x) at
  D = x^{1/2}(log x)^{-B}. Under EH the same holds at any D = x^theta, theta < 1.
- When D is near x, the e = 1 part of T_D is of the type of Lichtman's folklore conjecture (shift -2). But o(x) for it is
  stronger than that conjecture by more than a factor log x (audit, item 4).
- In F_q[T], T_D is exactly the sum that SS bound in Cor 6.1, through Thm 4.5 and Lemma 3.2: in characteristic p,
  (r+s^p)' = r', and Pellet's formula then turns mu(r+s^p) into a quadratic character in s.

## Classification
- **No-go reached.** The step with no integer analogue is SS Lemma 3.2 (with the sub-Burgess character sums of their
  Sec. 2 that it feeds). Transposed to Z, SS's split is a reformulation: it moves the whole problem into T_D, a
  mu-Lambda correlation. Prop. prop:B-parity(1)-(2) shows that a correlation of this kind carries the parity information.
- First unresolved implication: T_D(x) = o(x) for even one admissible D.
- Not new in spirit: compare Murty-Vatwani Thm 1.1 (as quoted). Theirs is conditional (EH plus a Mobius-twisted EH) and
  uses a different quantity. Audit: notes/audit-parity-v05.md (2 errors, 3 gaps, all fixed). Our version is unconditional at the
  BV level, and its residual is written in SS's variables.
- Not to repeat: integer transpositions of SS's split without a new input for T_D.
- Possible next inputs (open): an integer substitute for "mu restricted to a line is a character". The nearest
  known structures are the norm forms of FI and Heath-Brown (Remarks rem:fi-transfer, rem:hb-transfer). We see no
  such substitute for n -> n+2.
