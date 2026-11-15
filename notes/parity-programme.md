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
| FI98b | Friedlander–Iwaniec, The polynomial X^2+Y^4 captures its primes, Ann. Math. 148 (1998) 945-1040 | arXiv:math/9811185v1 | 7c1ef7c50fe5ac405560c0bf56baea5fd6c014bdc6fc5d248727b96f66cdb07a | Thm 1, Prop 2.1, 3.5, 4.1, (5.2), Lemma 17.1, Prop 17.2, pp. 945-1017 (helper, notes/sources-fi-x2y4.md; key quotes re-checked by the coordinator); 15 Nov (Session 18) |
| PM8b (again) | §8 incl. Remark 8.1 (p. 70), Thm 1.4 (pp. 2-3) | arXiv:1407.4897v4 | same hash | 15 Nov (Session 18) |
| TT25 | Tao–Teräväinen, Quantitative correlations and some problems on prime factors of consecutive integers (preprint) | arXiv:2512.01739v2 | see notes/sources-chowla-quantitative.md | Thm 3.1, Remarks 3.2, pp. 24-25 (re-checked by the coordinator) |
| HR, Pil, Guo, Hughes | Helfgott–Radziwiłł 2103.06853v2; Pilatte 2310.19357v3; Guo 2608.23500; Hughes 2609.28526 | arXiv | notes/sources-chowla-quantitative.md | helper reading only (statements, uniformity ranges); not used in the paper yet |
| TT25 (again) | Thm 3.1, Remarks 3.2, §1.6, §3.2 opening (pp. 9-10, 24-27) | arXiv:2512.01739v2 | ce10e83b10c6544e1dbff037a5e4efa0e387892e0fc596ae09dce76025d7b41e | Session 19 (helper + independent auditor, same hash) |
| MRT15 | Matomäki–Radziwiłł–Tao, An averaged form of Chowla's conjecture, ANT 9 (2015) | arXiv:1503.05121v3 | 8a2633b1594615fe0c340bbca01ad059be5bd66d3495bd028e7e9d2264f1e688 | eq. (1.12), Thm 1.6 (pp. 5-6); Session 19 |
| HB01 | Heath-Brown, Primes represented by x^3+2y^3, Acta Math. 186 (2001) 1-84 | journal scan supplied by Jerry | 96ffd7eb27e724d1ddecd6c738e7261c739c329f02fb222a9c964d0046ec10ae | pp. 2-10, 17-21, 52, 66-69, 72-73, 78-79; Session 19 follow-up (secondary notes by Maynard, X. Li also in notes/sources-hb-x3-2y3.md) |
| Li21 | Lichtman, Averages of the Möbius function on shifted primes | arXiv:2009.08969v2 | (14 Nov) | abstract, §1 |

Not opened yet: Bombieri, Le grand crible / The asymptotic sieve (1976); Opera de Cribro (paywalled); Selberg's original parity papers;
Heath-Brown x^3+2y^3 (Acta 2001); Matomäki–Radziwiłł 2016; MRT averaged Chowla;
Tao–Teräväinen; Sawin–Shusterman (arXiv:1808.04001).

## Threads and status (one bounded step per run)
1. Selberg's parity problem / PM8b obstruction: v0.1 Section 2 (Literature, re-read 15 Nov). Next: a Lean check of the finite
   combinatorial fact that omega vanishes on A_1 and on the twin set (trivial; only if it costs nothing); Bombieri's formal statement.
2. Known parity-breaking results: Tao16 Thm 1.2 (Prop. prop:tao-weight), TT25 Thm 3.1 (Prop. prop:tao-weight-logc, v0.3), FI x^2+y^4
   (v0.2). Heath-Brown x^3+2y^3: read in the source (v0.4, Session 19 follow-up). Next: Sawin–Shusterman
   (arXiv:1808.04001) and the step with no integer analogue.
3. Conditional statements: FI98 Thm 2 specialised to Lambda(n+2) (Prop. prop:fi-twin). Next: which hypotheses are known NOT to suffice
   (EH/GEH for sieve methods: PM8b §8).
4. Numerical illustrations: Selberg-weighted lambda(n)lambda(n+2) (Sec. 4, Heuristic).
5. Open questions: Sec. 5.

## Literature-check record
- 15 Nov: one standard web search ("logarithmically averaged Chowla two-point correlation in arithmetic progressions uniform modulus
  ... sieve weights") found no source stating Prop. prop:tao-weight or a uniform-in-modulus version; hence "possibly folklore" stays.

## Session 18 (15 Nov) updates
- Thread 1: new Section sec:bip of the paper (v0.2): exact criterion for which targets a Liouville-pattern weight can block
  (Prop. prop:bipartite, Cor. cor:six); PM8b Remark 8.1 correction (subsec:rem81). Lean: lean/TwinPrimes/Parity.lean.
- Thread 2: FI a^2+b^4 done (subsec:fi-x2y4, Remark rem:fi-transfer). Next: Heath-Brown x^3+2y^3, then Sawin–Shusterman.
- Open question 1: TT25 Thm 3.1 would give level (log x)^{c0} (deduction not written; next candidate step: write and audit it,
  as a strengthening of Prop. prop:tao-weight, labelled conditional on the preprint).
- Next attempt candidates: (a) the deduction above; (b) weights outside the class (residue-class version explored: classwise
  fairness gives nothing new, global fairness is the wrong notion; see notes/explorations.md); (c) the function-field step.

## Bonus run (15 Nov, after Session 19) updates
- Sources read: SS19 arXiv:1808.04001v2 (SHA-256 5b762a0888363d2d1140bb9831a6d940586208f690b4dda3fa6e712337e0a687; notes/sources-sawin-shusterman.md);
  Li21 again (p. 1); Cantarini arXiv:2607.09110v1 (15625c8524d6a89944f085ece4dd75c8ab0d5dc4e04fd98f2ebeb531114afc9c; pp. 1-3, quoting Murty-Vatwani);
  for open question 3 (helper): Polymath8a 1402.0811v3, Maynard 2006.06572v2 / 2006.07088v1 / 2006.08250v1, Lichtman 2211.09641v1 / 2309.08522v1
  (hashes in notes/sources-oq3-level.md). Not opened: Murty-Vatwani (JNT 2017), BFI (Acta 1986); see notes/sources-needed.md.
- Thread 2: Sawin-Shusterman done (paper v0.5, Section sec:ss). Next: Matomaki-Radziwill (2016) or the original Murty-Vatwani.
- Thread 3: Prop. prop:ss-split. Open question 3 answered from the literature (no all-moduli fixed-residue absolute-value result
  beyond x^{1/2}; weighted records 17/32 bilinear and 66/107 well-factorable; none reaches 2/3).
- Open question 5 answered conditionally (Cor. cor:maynard-logc).
- Next attempt candidates: (b') weights that change the twisted main terms (open question 2); (c) an integer structure in
  which "mu restricted to a line is a character" has a substitute (we know none for n -> n+2).

