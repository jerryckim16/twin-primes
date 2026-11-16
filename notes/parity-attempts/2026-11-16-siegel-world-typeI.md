# Route card: the Siegel-zero world and the twisted Type I input of the obstruction (Session 25, 15/16 Nov 2026)

Classification: **located (proved under an explicit hypothesis on small split primes; literature read in the source)**.
No parity-breaking content for twin primes in the actual world (Siegel zeros are conjectured not to exist).

## Question
Heath-Brown (1983) proves twin primes from infinitely many Siegel zeros, so the parity obstruction of Polymath8b sec. 8
must fail in that world. Which of its hypotheses fails, and where exactly?

## Success / no-go criteria (fixed before the attempt)
- Success: a proved statement that, in a world with an exceptional character, the twisted Type I discrepancies (PM8b (144))
  of lambda(n)lambda(n+2) are large at some modulus <= x^theta, with every hypothesis explicit, and a numerical check
  of the inequality.
- No-go: if the failure needs moduli > x^theta or needs information on chi at all small primes that a Siegel zero
  is known not to give, record the first unresolved implication instead.

## Sources read
- Tao-Teraeväinen, arXiv:2109.06291v2 (SHA-256 d0b968cef35d40a1ab7a9dad9838e6c41046ed20209fcba91e5cec2125308956):
  Def. 1.4, Thm 1.5 (quotes Heath-Brown [11, Thm 1], Germán-Kátai, Chinis), Thm 1.6, Cor. 1.8, sec. 1.2 (strategy),
  sec. 2.3-2.4 (exceptional primes, scales R0, R), Lemma 3.2, Prop. 3.5, Cor. 3.6, (4.1), Lemma 4.1.
- Matomäki-Merikoski arXiv:2112.11412 downloaded (SHA-256 2e664b17...521ff), not used.
- Heath-Brown, Prime twins and Siegel zeros, PLMS 47 (1983) 193-224: NOT opened (quoted from TT only; notes/sources-needed.md).

## Result (paper v0.10, Section sec:siegel)
- Prop. prop:siegel-bias (Proved here, possibly folklore): for chi real primitive mod q, f completely multiplicative +-1,
  Q = lcm(prod_{p<=w} p, q), F = {p > w, p not dividing q, f(p) != chi(p)}:
  (1/(rho x)) sum_{b in G} chi(b)chi(b+2) S_b >= 1 - 4 s1 - (4/rho)(s2 + P2/x) - (Q/x)(1 + 4 P1); and for q an odd prime > w,
  discrepancies (against the coprime average, as in PM8b (144)) at modulus Q are at least that minus (1+Q/x)/(q-2) times x/Q.
  Elementary (counting in classes; Jacobsthal sum = -1).
- Cor. cor:siegel-typeI (corrected after the audit): with a Siegel zero, TT (3.22)-(3.23) summed over m <= M = log^{1-eps'} eta
  control the exceptional primes above T = q^{1/M}; a PER-MODULUS, UNWEIGHTED discrepancy bound eps x/Q at the single modulus
  Q = Wq <= x/T forces sum_{w<p<T, chi(p)=1} 1/p >= (1-eps)/4 - o(1) (eta -> infinity; prime conductor).
- Reading: in the Siegel world two-point Chowla holds (TT Cor. 1.8(ii)) but, if the exceptional character has few split
  primes in (w, T), the per-modulus form of PM8b (144) fails at modulus Wq, consistent with Heath-Brown's theorem.
  NOT shown: failure of the averaged (EH-type) input; anything for characters with many small split primes.

## First unresolved implication
Whether a Siegel zero forces sum_{w<p<T, chi(p)=1} 1/p < 1/4 - c (TT controls nothing below T = q^{1/log^{1-eps'} eta}).
If it held, a per-modulus unweighted twisted Type I input at the moduli Wq <= x^theta would exclude sequences of Siegel zeros
with eta -> infinity (prime conductor). Open question 1 as stated (log-averaged, averaged over q) is a different statement. Alternative route (not checked): a Type I weight from TT's lambda^sharp_Siegel (sec. 6) with an l^1 bound.

## Checks
- code/parity/siegel_class_bias.py (/usr/bin/python3 -I; x q w seed), output code/parity/siegel_class_bias.out: the pointwise
  inequality and part (2) checked exactly in 30 cases (q = 163, 1009; x = 1e7, 5e7). PASS.
- Fresh-context adversarial audit: notes/audit-parity-v010.md (3 errors: misreading of TT (3.23), 'strictly stronger' overstatement,
  a numerical sentence; 3 gaps: error terms with delta -> 0, per-modulus vs averaged (144), OQ1 mismatch; all fixed in v0.10).
- Full-paper referee pass: referee/2026-11-16-parity-barrier/report.md.
- Literature check (2 standard web searches, 16 Nov): no source found stating the progression bias of lambda(n)lambda(n+h)
  under an exceptional character; hence "possibly folklore".

## Do not repeat
The exact identity lambda = chi * (lambda chi) on classes mod q is trivial; any new attempt here must add control of the
small split primes or a Type I construction, not re-derive the bias.
