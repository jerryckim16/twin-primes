# Audit of parity paper v0.12 changes (Session 27, 16 Nov 2026)

Fresh-context adversarial helper (mathbox:proof-audit not available), comparing the working tree with origin/main.
Scope: the shortened proofs (prop:siegel-bias, cor:siegel-typeI, prop:fi-twin, prop:B-parity, prop:bomb-twin, prop:ss-split),
new Remark rem:chen (against the definitions and lean/TwinPrimes/Parity.lean chen_*), the shortened MR16 digest.

Result: no ERROR. All shortened proofs remain correct (B_b counting, Jacobsthal step, normalisation with O_w(s_2) checked;
TT22 (1.4), (3.22), (3.23) used no more strongly than before; F'(0) = 2C_2 in ss-split; mirror target of rem:chen correct
up to prime powers; Lean statements match).

GAPs (fixed): (1) the remark after prop:B-parity had dropped the hypothesis Delta(x) <= x^{1/3}(log x)^{-2^23-3}, the target
size and the conditions n1 != n2, (m, n1 n2) = 1 -- restored, with the nonnegativity for a^+; (2) rem:chen said "Under EH" where
prop:bomb-twin also assumes Bombieri's conclusion applies -- fixed.

MINOR (fixed): (3.23) "uniformly in m >= 2", "(their eps = 1)", T -> infinity justified; Heath-Brown sentence reverted to the
careful wording; script description (f = chi off a random set, non-vacuous in 10 of 30); fi-twin: g(2) = 0, g(p^2) << p^{-2},
(9.2) step; "since lambda = +1 on products of two primes" restored; rem:chen: definition of "kills" for non-prime targets,
"n and n+2 prime", integer-valued Lean weights, Tao 2007 quoted exactly; MR16: "applies to" wording, caveat on how Tao16 uses
MR16, absolute constants C, C' (C' = 20000), delta > 0, PDF page = printed page.
MINOR (not changed): ss-split remark that log d <= log x converts x(log x)^{-A-1} to x(log x)^{-A} (implicit).
