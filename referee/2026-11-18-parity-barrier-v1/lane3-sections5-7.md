# Lane 3 (mathematics of Sections 5-7 and sec:num) -- fresh-context referee, 18 Nov 2026

Saved by the coordinator from the helper's final report (in substance). Checked correct: singular series in prop:ss-split
(-sum_{d odd} mu(d) log d/phi(d) = 2C_2); H = 2C_2 in prop:fi-twin; 4C_2 in prop:bomb-twin; Jacobsthal sum -1 (q = 7, 11, 13,
163); CRT step and the bound for sum B_b in prop:siegel-bias; cor:siegel-typeI; Gowers count and c_d; window identity and second
difference; the constant 216 in prop:lt22; identity (*) and (d), tested numerically at N = 10^5, K <= 20; (a)-(c) algebra;
sec:num arithmetic.
Errors: (1) prop:lt22: "for H = o(log X)" does not give H^{1+delta} <= c log X; state the range H <= (c log X)^{1/(1+delta)}
(the old version had the same flaw); qualify rem:mrt17. (2) Siegel subsection lost "w fixed".
Gaps: (3) (B) reduction lost its hypothesis on Delta and is a sufficient condition, not an equivalence; (4) "f_- has bounded sums
over every interval" needs 4 | L; (5) the V(3) equivalence also needs V(2) to o(X) (restore "V(2) is known by the PNT");
(6) prop:lt22 third claim is about f' = mu' 1_S: one line on the shifted primes outside S; (7) prop:gm(c) rests on the reading of
Gol04 (uniform in K) and inherits K <= N^{1/3}; (8) rem:ss-transfer: T_D = o(x) does not need the e = 1 term alone to be o(x);
(9) cor:siegel-typeI: restore "(their eps = 1)" and a word on (x, 2x+2].
Labels: rem:ford-twin -> Literature + Heuristic; prop:gm needs "conditional" for (c); window paragraph's last sentence Heuristic.
Minor: redundant lower limit in cor:siegel-typeI; K ~ log N equivalence is unconditional; restore S(2) = 1.3203...; "would tend
to 1/2" ambiguous; (B) separation at C = 1; restore that f_- correlates with e(n/4).
