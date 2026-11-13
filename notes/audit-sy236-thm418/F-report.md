# Literature check F: Polymath8a (arXiv:1402.0811v3) against Song–Yue §§4.1–4.7

## Source authentication
- arXiv:1402.0811v3 (submitted 3 Sep 2014, 107 pp, comment "revised version, focusing solely on equidistribution estimates").
  - PDF: polymath8a/dl-v3/1402.0811v3.pdf, sha256 f4b4556f9451ea0524b974376b9dbe4478faf3734847897460274f6bae98b65c (HTTP 200).
  - Source: polymath8a/dl-v3/src.bin (gzip of newgap.tex), sha256 4db2b22532e291782aaed923170de165e0392e49e83b3436163996503f6e13bf; extracted to polymath8a/src/newgap.tex.
  - Text: polymath8a/txt/pm8a.txt (pdftotext -layout).
- Published version: Algebra & Number Theory 8:9 (2014) 2067–2199, DOI 10.2140/ant.2014.8.2067. MSP landing page: received 4 Feb 2014, **revised 12 Oct 2014** (after v3), accepted 12 Nov 2014. MSP served the full 136-page PDF openly (HTTP 200, no login): polymath8a/dl-ant/ant.pdf, sha256 220232ac124e2adb984fd6082d959057314a0006adc7cdf10d7185683bba47a8. Paywall not bypassed.
  - Statement numbers are the same for every item checked (Thm 2.8, 2.9, Lemmas 3.1/3.3/3.4, Cor 4.16, Lemma 5.2, Cor 5.3, Props 5.10/5.13, Lemma 6.25, Cor 6.26, Lemmas 7.3–7.5). Statement texts of Thm 2.8(v), Thm 2.9, Cor 4.16, Lemma 6.25 and Cor 6.26 are identical to v3.
  - **Equation numbers differ in §5.** v3 (5.38)–(5.42) are published (5-39)–(5-43). §7 (7.11)–(7.15) are the same as (7-11)–(7-15). Song–Yue cite v3, and their numbers match v3.
- Paths are relative to /tmp/claude-0/-home-user-twin-primes/8743bfbf-f30b-5726-9539-44cac1e153cb/scratchpad/.

All page numbers below are v3 PDF pages.

## Item-by-item

### Theorem 2.9 (bilinear Bombieri–Vinogradov), v3 p.11
Quote: "Let N,M ≫ 1 be such that NM ∼ x and N ≥ x^ε for some fixed ε>0. Let α,β be coefficient sequences at scale M,N respectively such that β has the Siegel-Walfisz property. Then for any fixed A>0 there exists a fixed B>0 such that Σ_{q ≤ x^{1/2} log^{-B} x} sup_{a∈(Z/qZ)^×} |Δ(α⋆β; a (q))| ≪ x log^{-A} x."
- Only the Siegel–Walfisz factor β needs N ≥ x^ε. α needs no lower bound.
- The coefficient sequences of Definition 2.5 (p.9) are real-valued, with |α(n)| ≪ τ^{O(1)}(n) log^{O(1)} x. Siegel–Walfisz (2.3) is |Δ(α1_{(·,r)=1}; a (q))| ≪ τ(qr)^{O(1)} N log^{-A} x.
- Constants are uniform under the asymptotic convention of Definition 1.2: objects may depend on x, and implied constants depend only on the fixed quantities.

Song–Yue invocations:
1. Prop 4.2 (sy.txt l.764): d ≤ X^{1/2}(log X)^{-K_C}, with β at N ≥ X^{11/25} and Siegel–Walfisz. **Met.**
2. Prop 4.2, Δ₂ (l.914): modulus r ≤ R ≪ X^{1/2−τ₀}, applied to α1_{(·,q)=1} and β1_{(·,q)=1}. Uniform Siegel–Walfisz for the restricted β is proved in Song–Yue by the p > D₀ mass bound. This is needed because Polymath's τ(q)^{O(1)} allowance would not give log savings uniformly in q. **Met**, with uniformity in q supplied by Song–Yue.
3. Prop 4.4 (l.1043, 1167): same as items 1 and 2, with N ≥ X^{7997/20000}. **Met.**
4. Prop 4.6 (l.1258): the Siegel–Walfisz factor is one smooth ψ_i at N_i ≥ X^{1/5}. The other factor is α⋆ψ_j⋆ψ_k. Smooth sequences have Siegel–Walfisz by Lemma 3.4(iii), case k>j. **Met.**
- Complex coefficients and n^{it} twists: Polymath states real α. Song–Yue split into real and imaginary parts (l.979). This is valid because Δ is real-linear.

Verdict: **hypotheses met.**

### Corollary 4.16, v3 p.37 (source label `dons`)
Hypotheses:
- ψ_N(x) = ψ((x−x₀)/N), with ψ smooth, compactly supported, and |ψ^{(j)}| ≪ log^{O(1)} N.
- "d₁,d₂ squarefree, not necessarily coprime", with c₁,c₂,l₁,l₂ integers.
- "[d₁,d₂] is y-densely divisible".
- "d a divisor of [d₁,d₂] and a (d) any residue class".
- "If N ≤ [d₁,d₂]^{O(1)}" (this is the polynomial length condition).

Second ("variant") bound: |Σ_{n≡a (d)} ψ_N(n) e_{d₁}(c₁/(n+l₁)) e_{d₂}(c₂/(n+l₂))| ≪ [d₁,d₂]^ε ( d^{-1/2}[d₁,d₂]^{1/2} + d^{-1} (c₁,δ₁′)/δ₁′ · (c₂,δ₂′)/δ₂′ · N ), where δ_i = d_i/(d₁,d₂) and δ_i′ = δ_i/(d,δ_i).
- The proof derives the second bound from Prop 4.12(i) (Pólya–Vinogradov plus Ramanujan–Weil), which uses no dense divisibility.
- Every n is n-densely divisible by Definition 2.1: take r = 1 when R ≤ n and r = n when n < R ≤ n². So the hypothesis is vacuous with y = [d₁,d₂]. Song–Yue's remark (l.841–842, l.1105) is correct.
- Polymath uses the same corollary the same way in its own Type II proof (Prop 5.10).

Song–Yue invocations:
1. IIa, (30), l.835–843: d₁ = rq₀[q₁,s₁], d₂′ = [q₂,s₂], d = q₀, at most z classes mod q₀.
   - Completion term: q₀^{-1/2}(q₀R(Q/q₀)^4)^{1/2} = R^{1/2}(Q/q₀)^2. ✓
   - Mean term: r divides δ₁′ and (r,q₀)=1, so (c₁,δ₁′)/δ₁′ ≤ (c₁,r)/r. The r-component of c₁ is a unit times h₁s₁s₂ − h₂q₁q₂. ✓
   - Length: [d₁,d₂] ≥ r ≫ X^{γ−η₂} with γ−η₂ ≥ 0.42179, and N ≤ X^{1/2}. ✓
2. IIb, (40), l.1100–1110: d₁′ = rq₀u₁[v₁,v₂] and d₂′ = q₂ are coprime, d = q₀. Completion term (ru₁[v₁,v₂]q₂)^{1/2}. The mean-term gcd is (h₁v₂ − h₂v₁, r). Length: γ−η₂ ≥ 0.38164 and N ≤ X^{11/25}. ✓
- This matches Polymath Prop 5.13 (`exse-3`) except that Song–Yue use the second bound where Polymath uses the first. Song–Yue say so (l.1109).

Minor point, shared with Polymath: Song–Yue's convention "a noninvertible denominator contributes zero" puts implicit indicators 1_{(n,d₁)=1} 1_{(n+ℓr,d₂)=1} into S and T. Corollary 4.16 uses the P¹ convention of §4.1. Möbius inversion over e₁|d₁, e₂|d₂, using the "n ≡ a (d)" clause with d = lcm(q₀,e₁,e₂), removes the indicators at a cost of τ(d₁)τ(d₂) = X^{o(1)}. A larger d only decreases both terms. Not stated in Song–Yue, harmless.

Verdict: **hypotheses met. Transcription correct.**

### Proposition 5.10, v3 p.52
Quote: "For any p=(h₁,h₂,q₁,q₂,s₁,s₂) with (q₀q₁q₂s₁s₂,r)=1, any ℓ≠0 and r as above with q₀q_i, q₀s_i ≪ Q, r ≪ R, we have |S_{ℓ,r}(p)| ⪅ (q₀,ℓ)( q₀^{-2} Q² R^{1/2} + N/(q₀R) (h₁s₁s₂ − h₂q₁q₂, r) )."
- Song–Yue (30) is identical, with z = (q₀,ℓ).
- The proof (pp.53–54) uses only the second bound of Cor 4.16. Dense divisibility enters only through that corollary's vacuous y.
- The polynomial length condition is not checked explicitly in Polymath. Song–Yue check it.

Verdict: **met.** "Its proof applies without dense divisibility" is accurate.

### §5.6, eqs (5.38)–(5.42), v3 pp.57–58, and Proposition 5.13, p.58
- (5.38) Υ_{U,V} ⪅ x^{-ε}(q₀,ℓ)Q²Nq₀^{-2}
- (5.39) q₀^{-1}x^{-δ-2ε}Q/H ⪅ U ⪅ x^{-2ε}Q/H
- (5.40) q₀^{-1}x^{2ε}H ⪅ V ⪅ x^{δ+2ε}H
- (5.41) UV ∼ Q/q₀
- (5.42) definition of T_{ℓ,r}

Polymath obtains the factorization q₁ = u₁v₁ from dense divisibility (Lemma 2.10(i)). Prop 5.13 uses the first bound of Cor 4.16, with x^{δ/3} y-dependence.

Song–Yue cite these only as the template for the rebalanced Cauchy–Schwarz. They take u from their own Lemma 4.5 divisor, not from dense divisibility, and they use the second bound. Their numbering matches v3; published is (5-39)–(5-43).

Verdict: **citation accurate. No hypothesis of Prop 5.13 is used.**

### Lemma 1.3 (ii)–(iii), p.6; Lemma 5.2 and Corollary 5.3, p.43
- 1.3(ii): Σ_{d≤y} τ^C(d) ≪ y log^{O(1)} x.
- 1.3(iii): Σ_{d≤y, d≡a (q)} τ^C(d) ≪ (y/q) τ^{O(1)}(q) log^{O(1)} x + x^{o(1)}, for any class, not necessarily primitive.
- Lemma 5.2: with D₀ = exp(log^{1/3} x), the set E(D) of d∈[D,2D] with Π_{p|d, p≤D₀} p > exp(log^{2/3} x) satisfies |E(D)| ≪ D log^{-A} x, "for D obeying (5.6)" (x^{1/2} ⪅ D ⪅ x^{1/2+2ϖ}). The proof works for any D.
- Cor 5.3: the exceptional contribution is ≪ x log^{-A} x, via the trivial bound |Δ| ≪ xD^{-1}τ(d)^{O(1)} log^{O(1)} x, Cauchy–Schwarz and (ii).

Song–Yue (l.764–775) use the same D₀ and the same exceptional set verbatim, with D ≤ X^{253/500} = X^{1/2+2·0.003}. The term x^{o(1)} in (iii) is absorbed because X/d ≥ X^{0.49}. The τ^{2v}-weighted variants (l.971, 1191, 1491) follow from (ii)–(iii). Neither lemma assumes dense divisibility.

Verdict: **met.**

### Lemma 3.1, p.14
Quote: "Let 1/10 < σ < 1/2, and let t₁,…,t_n ≥ 0 with Σt_i = 1. Then at least one holds:
- (Type 0) some t_i ≥ 1/2+σ;
- (Type I/II) a partition S∪T with 1/2−σ < Σ_S ≤ Σ_T < 1/2+σ;
- (Type III) distinct i,j,k with 2σ ≤ t_i ≤ t_j ≤ t_k ≤ 1/2−σ and all three pair sums ≥ 1/2+σ."

Song–Yue Lemma 4.9 uses σ = s = 1001/10000 ∈ (1/10, 1/2). The three alternatives agree verbatim. Song–Yue's recalled proof follows Polymath's "powerful/powerless" argument.

Verdict: **met.**

### Lemma 3.3 (Heath-Brown identity), p.16
Quote: "Λ = Σ_{j=1}^K (−1)^{j−1} C(K,j) μ_≤^{⋆j} ⋆ 1^{⋆(j−1)} ⋆ L on [x,2x], with μ_≤(n) = μ(n)1_{n ≤ (2x)^{1/K}}."

Song–Yue (53) has K = 10 and Z = (2X)^{1/10}, which is the same.

Verdict: **met.**

### Lemma 3.4(iii), p.19
Quote: "If N_k ≫ x^ε then α_k satisfies the Siegel-Walfisz property. More generally α_S satisfies it if Π_{k∈S} N_k ≫ x^ε."
- The Möbius case is only sketched: "follows from the Siegel-Walfisz theorem for the Möbius function … using summation by parts to handle the smooth cutoff, and we omit the details".
- Polymath's atoms use its finer-than-dyadic ψ_N, with no n^{it} twists.

Song–Yue (l.1556–1575) cite it "in the form used in … and its proof". They supply the summation by parts for their dyadic w_L and for twists |t| ≤ (log X)^T. Their convolution identity is correct and is a valid variant of Polymath's argument.

Verdict: **met** (the source is a sketch, and Song–Yue add the missing steps).

### Lemma 6.25 and Corollary 6.26, v3 pp.79–80; the (49) issue

**Lemma 6.25 statement.** "Let s,r₁,r₂ be squarefree integers with (s,r₁)=(s,r₂)=1. Let a₁∈(Z/r₁s)^×, a₂∈(Z/r₂s)^×, n∈Z/([r₁,r₂]s)Z. Then
Σ_{h∈(Z/s[r₁,r₂]Z)^×} Kl₃(a₁h; r₁s) conj(Kl₃(a₂h; r₂s)) e_{[r₁,r₂]s}(nh) ≪ (s[r₁,r₂])^ε s^{1/2}[r₁,r₂]^{1/2} (a₂−a₁, n, r₁, r₂)^{1/2} (a₂r₁³ − a₁r₂³, n, s)^{1/2}."

**Corollary 6.26 statement.** Same s, r_i, a_i; H ≥ 1 with H ≪ (s[r₁,r₂])^{O(1)} (the polynomial length condition); ψ_H shifted smooth. Then
|Σ_{(h,s[r₁,r₂])=1} ψ_H(h) Kl₃(a₁h; r₁s) conj(Kl₃(a₂h; r₂s))| ≪ (s[r₁,r₂])^ε (H/([r₁,r₂]s) + 1) s^{1/2}[r₁,r₂]^{1/2} (a₂−a₁, r₁, r₂)^{1/2} (a₂r₁³ − a₁r₂³, s)^{1/2}.

**Translation to Song–Yue.** a_i = aB*/(b³m_i) (Song–Yue's "b3" is b³ lost in extraction), with B* = b₁b₂b₃. Then:
- a₂ − a₁ is a unit times m₁ − m₂;
- a₂r₁³ − a₁r₂³ is a unit times m₁r₁³ − m₂r₂³ = D.

So **Song–Yue (49) is a faithful transcription of Cor 6.26.** Polymath itself writes exactly this bound in §7.3 (p.90): "U ⪅ (H_b/([r₁,r₂]s)+1)(s[r₁,r₂])^{1/2} × (r₁,r₂,m₂−m₁)^{1/2}(m₁r₁³−m₂r₂³,s)^{1/2}". Song–Yue did not mis-transcribe it.

**The defect is in Polymath's Lemma 6.25 itself, for r₁ ≠ r₂ with g = (r₁,r₂) > 1.**
- The proof uses CRT for Kl₃(a h; r_i s), which is right. Then it "split[s] further … over the primes dividing [r₁,r₂]" and reduces to the local bound (6.25*): p^{1/2}(b₁−b₂, m, d₁, d₂)^{1/2}.
- By CRT (Kl₃(x;q₁q₂) = Kl₃(x q̄₂³; q₁) Kl₃(x q̄₁³; q₂)), the local parameters at p | g are b_i = a_i s̄³ (r_i/p)^{-3}. These are not a_i up to a common unit.
- Write r_i = g t_i, with (t_i, g) = 1 because r_i is squarefree. Then b₁ ≡ b₂ (mod p) holds iff a₁t₂³ ≡ a₂t₁³ (mod p).
- The correct factor is (a₁t₂³ − a₂t₁³, n, g)^{1/2}. For Song–Yue this is **gcd(g, m₁t₁³ − m₂t₂³)^{1/2}**, up to a unit. This confirms the caller's repair.
- The s-factor (a₂r₁³ − a₁r₂³, n, s) is correct, because there the twists r̄_i³ are exactly what appears. The stated g-factor is correct when r₁ = r₂.
- The published version (2014) has the identical statement and proof (p.2163–2164). No erratum was found (one web search; see Gaps below).

**Numerical check.** Script: sy-audit/out-F/scripts/kl3corr.py and kl3corr_g.py. Setup s = 1, n = 0, r_i = p t_i, t₁ = 2, t₂ = 3.

| p | a₁ = a₂ = 1 (Polymath factor = p) | a₁t₂³ ≡ a₂t₁³ mod p, a₁ ≢ a₂ (Polymath factor = 1) |
|---|---|---|
| 13 | |S| = 0.180 | |S| = 1.986 |
| 31 | |S| = 0.172 | |S| = 4.994 |
| 61 | |S| = 0.169 | |S| = 9.997 (≈ p/(t₁t₂)) |

For composite g = 35: |S| = 0.24 against 3.66. The local factor at p | g is ≍ p exactly when a₁t₂³ ≡ a₂t₁³, not when a₁ ≡ a₂.

With g a product of many primes and t₁, t₂ fixed, the true size is about g/(t₁t₂), while the stated bound is (gt₁t₂)^{1/2+ε}. **So the lemma as stated is false in general.**

**Corollary 6.26 inherits the defect.** Its proof is Möbius inversion plus completion from Lemma 6.25. Its "gcd factors are divisors of those for δ=1" reasoning goes through with the repaired factor.

**The downstream sum survives.** Fix g, t₁, t₂ and m₂. For e | g, the condition e | m₁t₁³ − m₂t₂³ is one residue class for m₁ mod e, because t₁ is invertible mod g. Hence
Σ_{m₁,m₂≍M} gcd(g, m₁t₁³−m₂t₂³)^{1/2} ≤ Σ_{m₂} Σ_{e|g} e^{1/2}(M/e + 1) ≪ τ(g) M (M + g^{1/2}) = X^{o(1)}(M² + Mg^{1/2}).
- This is exactly the bound Song–Yue use (p.28, l.1408–1410) and the one Polymath uses in Lemma 7.4.
- (50), (51), (52) and Song–Yue's three exponent margins are unchanged. The same repair fixes Polymath's own Theorem 2.8(v) proof.
- The off-diagonal condition D ≠ 0 is equivalent to m₁t₁³ ≠ m₂t₂³, since D = g³(m₁t₁³ − m₂t₂³). The diagonal treatment (50) is unchanged.

**Other hypotheses of Cor 6.26 in Song–Yue's use.**
- s, r_i squarefree with (r_i, s) = 1: ✓.
- a_i units: ✓ by (m_i, br_is) = 1 and (aB*, d) = 1.
- (ℓ, sr₁r₂) = 1: ✓.
- ψ_{H_b} smooth: ✓.
- Song–Yue's fallback when H_b is not ≪ (s[r₁,r₂])^{O(1)}: they complete the sum directly with Lemma 6.25 at frequencies j, using gcd(u,j,v) ≤ gcd(u,v). This is sound, and the same g-repair applies.

**Verdict.**
- Transcription: correct.
- Cited result: **defective as stated** (a mis-stated gcd factor at primes of (r₁,r₂) in Polymath v3 and in the published version).
- Song–Yue (49) as written is therefore unsupported. With the corrected factor gcd(g, m₁t₁³ − m₂t₂³)^{1/2} the next step holds verbatim. **The Type III conclusion is unaffected** once (49) is restated.

### §7.2 eqs (7.11)–(7.15), v3 pp.85–88; Lemma 7.3 p.89; Lemma 7.4 p.91; Lemma 7.5 p.92
- (7.11) defines Σ₁. (7.12) is discrete Fourier inversion. It needs supp ψ_i ⊂ (−q/2, q/2], which follows from N_i ⪅ x^{−σ}Q; Song–Yue have N_i ≪ X^{2/5} and Q ≫ X^{1/2−ζ}.
- (7.13) is the Taylor expansion with q in an interval of relative width x^{−ε} and |h| ≤ x^{ε/2}H_i. Song–Yue use the same with ζ. (7.14) is H = Q³/N. (7.15) defines F.
- No dense divisibility is used before the b/d split, where Polymath invokes Lemma 2.10(i); Song–Yue replace that with their Lemma 4.7.
- Small imprecision, shared by both: c_i(j,h) is only ≪ x^{jε/2+o(1)}, not ≪ 1. It is compensated by ((q−Q)/q)^j ≪ x^{−jε}, so it is harmless.
- Lemma 7.3 (|F mod b| ≤ b₁♭b₂♭b₃♭/b², independent of d and m) matches Song–Yue l.1326–1330.
- Lemma 7.5 (Σ b₁♭b₂♭b₃♭/((b₁b₂b₃)^{1/2}b³) converges) is the same series as Song–Yue's.
- Song–Yue's (51) reproduces Lemma 7.4 with y = bX^{η₃}. Lemma 7.4 inherits the Lemma 6.25 issue, repaired as above.

Verdict: **met** (Lemma 7.4 is conditional on the repair).

### Deligne Type III condition, Theorem 2.8(v), p.11
Quote: "If σ > 1/18 + 28ϖ/9 + 2δ/9 and ϖ < 1/12, then Type_III^{(1)}[ϖ,δ,σ] holds." The auditor's memory is exact. The published version is identical.

Song–Yue do **not** invoke Theorem 2.8(v). They redo the exponent count with a fixed S = X^{143/375}, and I recomputed their three exponents:
- 1 − 1/3000;
- 1 − 137/3000;
- 1 − 71/2400 (at N = X^{9/10}).

For comparison, Song–Yue's Type III range (X^{1/5} ≪ N_i ≪ X^{2/5}, N_iN_j ≫ X^{3/5}) is σ = 1/10. With ϖ = 3/1000:
- with δ replaced by the window η₃ = 39/1000: 1/18 + 28ϖ/9 + 2η₃/9 = 0.0736 < 0.1;
- with δ = 91/5000: the value is 0.0690.

So Polymath's numerology would also be satisfied, but it is stated for x^δ-densely divisible moduli, which Song–Yue do not use.

Verdict: **not relied on. Parameters compatible.**

## Summary of verdicts
| Item | v3 locator | Verdict |
|---|---|---|
| Thm 2.9 | p.11 | met (Siegel–Walfisz on the factor ≥ x^ε; uniformity via Def 1.2; Song–Yue supply uniform Siegel–Walfisz after the (·,q)=1 restriction) |
| Cor 4.16, second bound | p.37 | met; dense divisibility vacuous with y = [d₁,d₂]; length condition checked; coprimality indicators need a one-line Möbius step (unstated) |
| Prop 5.10 | p.52 | met; identical to Song–Yue (30) |
| §5.6 (5.38)–(5.42), Prop 5.13 | pp.57–58 | template only; Prop 5.13 not used; v3 numbering (published (5-39)–(5-43)) |
| Lemma 1.3(ii)–(iii) | p.6 | met |
| Lemma 5.2, Cor 5.3 | p.43 | met |
| Lemma 3.1 | p.14 | met (σ = 0.1001) |
| Lemma 3.3 | p.16 | met (K = 10) |
| Lemma 3.4(iii) | p.19 | met; source only sketches the Möbius case |
| Lemma 6.25 / Cor 6.26 | pp.79–80 | Song–Yue transcribe faithfully, but the source is false as stated when (r₁,r₂) > 1 and r₁ ≠ r₂; correct factor (a₁t₂³ − a₂t₁³, n, g); repaired bound still gives X^{o(1)}(M² + Mg^{1/2}) |
| §7.2 (7.11)–(7.15), Lemmas 7.3–7.5 | pp.85–92 | met; Lemma 7.4 needs the same repair |
| Thm 2.8(v) | p.11 | σ > 1/18 + 28ϖ/9 + 2δ/9, ϖ < 1/12 confirmed; not relied on by Song–Yue |

## Gaps
- Bibliographic: the ANT article lists individual authors (Castryck, Fouvry, Harcos, Kowalski, Michel, Nelson, Paldi, Pintz, Sutherland, Tao, …) in its metadata and "D. H. J. Polymath" on the title page. Song–Yue's citation is fine.
- Erratum search: one web search (query: Polymath "New equidistribution estimates of Zhang type" erratum correlation hyper-Kloosterman Lemma 6.25) found no erratum. This does not prove that none exists.
