# Parity-barrier programme: plan and sources (Phase B, top priority)

Paper: `papers/parity-barrier/main.tex` ("The parity barrier and twin primes: what is known and what is missing").
Attempts: `notes/parity-attempts/` (one route card per run, index in its README).
The twin prime conjecture is open. Nothing in this programme claims to prove it or to break parity for it.

## Sources read (file hashes of the copies read; PDFs not kept)
| key | source | version | SHA-256 | read where / when |
|---|---|---|---|---|
| FI98 | Friedlander–Iwaniec, Asymptotic sieve for primes, Ann. Math. 148 (1998) | arXiv:math/9811186v1 | d39f5249d9003a8a7ce121c93e785dcffa2dfb5ccc9e728820a705826d953d1f | pp. 1041-1046 (hypotheses, Thm 1, Selberg example, twin primes remark), §9 Thm 2, §10 Thm 3; 14 Nov (coordinator) and 15 Nov (Session 17) |
| PM8b | Polymath, Variants of the Selberg sieve... | arXiv:1407.4897v4 | 4085a675d4716db2b22e672d083d4e38262b88b37b8d05b06bcdceb7cb4086a7 | §8 pp. 68-71 (of 80), re-read 15 Nov |
| Tao16 | Tao, The logarithmically averaged Chowla and Elliott conjectures for two-point correlations | arXiv:1509.05422 (current version) | 467329ae414b669808555fddf131be3bc07025777ae3af8ccdea6e98db6722e9 | Thm 1.2, Thm 1.3, Cor 1.5, Remarks 1.4, 1.6, pp. 2-6; 15 Nov |
| Tao07 | Tao, blog "Open question: the parity problem in sieve theory" (2007) | HTML | (14 Nov, see attempt details) | quoted in the 14 Nov route card only; re-read before use in the paper |
| Li21 | Lichtman, Averages of the Möbius function on shifted primes | arXiv:2009.08969v2 | (14 Nov) | abstract, §1 |

Not opened yet: Bombieri, Le grand crible / The asymptotic sieve (1976); Opera de Cribro (paywalled); Selberg's original parity papers;
Friedlander–Iwaniec 1998 x^2+y^4 (Annals); Heath-Brown x^3+2y^3 (Acta 2001); Matomäki–Radziwiłł 2016; MRT averaged Chowla;
Tao–Teräväinen; Sawin–Shusterman (arXiv:1808.04001).

## Threads and status (one bounded step per run)
1. Selberg's parity problem / PM8b obstruction: v0.1 Section 2 (Literature, re-read 15 Nov). Next: a Lean check of the finite
   combinatorial fact that omega vanishes on A_1 and on the twin set (trivial; only if it costs nothing); Bombieri's formal statement.
2. Known parity-breaking results: only Tao16 Thm 1.2 so far (used in Prop. prop:tao-weight). Next: FI x^2+y^4 statement and the
   structure it uses (norm form, Type II for the Jacobi symbol), then Heath-Brown, then Sawin–Shusterman.
3. Conditional statements: FI98 Thm 2 specialised to Lambda(n+2) (Prop. prop:fi-twin). Next: which hypotheses are known NOT to suffice
   (EH/GEH for sieve methods: PM8b §8).
4. Numerical illustrations: Selberg-weighted lambda(n)lambda(n+2) (Sec. 4, Heuristic).
5. Open questions: Sec. 5.

## Literature-check record
- 15 Nov: one standard web search ("logarithmically averaged Chowla two-point correlation in arithmetic progressions uniform modulus
  ... sieve weights") found no source stating Prop. prop:tao-weight or a uniform-in-modulus version; hence "possibly folklore" stays.
