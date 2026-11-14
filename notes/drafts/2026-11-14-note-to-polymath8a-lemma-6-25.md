# Draft note to the Polymath8a authors: Lemma 6.25 (DRAFT; not sent)

Status: draft written 14 Nov 2026 for Jerry Kim to review and send himself, by email or as a comment
on Terence Tao's blog post about the paper. Nothing has been sent.

---

**Subject:** A small mis-statement in Lemma 6.25 of "New equidistribution estimates of Zhang type"

Dear Professor Tao (and the Polymath8a contributors),

While independently checking the 2026 bounded-gaps preprint of Song and Yue, I believe I found a
small error in the statement of Lemma 6.25 (Correlation of hyper-Kloosterman sums) of D. H. J.
Polymath, *New equidistribution estimates of Zhang type*, Algebra & Number Theory 8 (2014),
2067–2199 (arXiv:1402.0811v3). Corollary 6.26 has the same factor. It does not seem to affect any
result of the paper, but I wanted to let you know in case it is not already known.

**The issue.** The lemma bounds
$\sum_{h}\mathrm{Kl}_3(a_1h;r_1s)\overline{\mathrm{Kl}_3(a_2h;r_2s)}e_{[r_1,r_2]s}(nh)$ with the factor
$(a_2-a_1,n,r_1,r_2)^{1/2}$. Write $g=(r_1,r_2)$ and $r_i=gt_i$. At a prime $p\mid g$, the local
arguments in the proof are $b_i=a_i\bar s^{3}(r_i/p)^{-3}$. These coincide when
$a_1t_2^3\equiv a_2t_1^3 \pmod p$, not when $a_1\equiv a_2$. So the proof gives the factor
$(a_1t_2^3-a_2t_1^3,\,n,\,g)^{1/2}$, which agrees with the printed one only when $r_1=r_2$.

**A family showing the printed bound fails.**
- **Parameters.** Take $s=1$, $n=0$, $r_1=5g$, $r_2=7g$ with $g$ a product of distinct primes
  $p\ge 11$, $p\ne 109$, and $a_2=1$, $a_1\equiv 5^3\cdot 7^{-3} \pmod g$, $a_1\equiv 1 \pmod 5$.
- **The printed factor is 1.** Since $5^3-7^3=-2\cdot109$, $a_1-a_2$ is a unit mod $g$, so
  $(a_2-a_1,0,r_1,r_2)=1$ and the lemma predicts $\ll(35g)^{1/2+\varepsilon}$.
- **The exact value.** By CRT the sum factors over primes:
  - each $p\in\{5,7\}$ contributes $-1/p$;
  - each $p\mid g$ contributes $\sum_{x\in\mathbb F_p^\times}|\mathrm{Kl}_3(x;p)|^2=p-1-1/p-1/p^2$, by
    Parseval over multiplicative characters with $|G(\chi)|^2=p$.

  Hence the sum equals $\frac1{35}\prod_{p\mid g}(p-1-1/p-1/p^2)$, which exceeds $(35g)^{1/2+\varepsilon}$
  by an unbounded factor for every $\varepsilon<1/2$. Numerically, over $g=11,\,11\cdot13,\ldots,11\cdots59$,
  the ratio to $(35g)^{1/2}$ grows from about $0.014$ to $8.3\times10^6$.

**Effect.** As far as I can tell, nothing downstream changes. Where the lemma is applied (e.g. Lemma 7.4
and Theorem 2.8(v)), the factor is summed over the $m$-variables. The corrected factor still gives
$\sum_{m_1,m_2\asymp M}(g,m_1t_1^3-m_2t_2^3)^{1/2}\ll\tau(g)M(M+g^{1/2})$, since $t_1$ is invertible mod $g$,
which is the same bound as before. The same applies to eq. (49) of Song–Yue, who quote the lemma.

A short script reproducing the computation is at
https://github.com/jerryckim16/twin-primes/tree/main/code/audit_sy236/pm8a_lemma625 (README with the
argument; `counterexample.py`).

For transparency: I am not a professional number theorist. This check was carried out with the help
of AI tools (Claude), and I have tried to verify the argument carefully; any errors are my own. Please
excuse me if this is already known. I would be grateful to hear whether the corrected form above is
what was intended.

With best regards,
Jerry Kim
