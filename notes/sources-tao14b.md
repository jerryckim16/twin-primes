# Tao, "A general parity problem obstruction" (blog post, 21 Nov 2014) and Akeno, arXiv:2508.02769v3

Found by the literature check of Session 22 (15 Nov 2026), via a footnote in Akeno's paper.

## Tao14b: https://terrytao.wordpress.com/2014/11/21/a-general-parity-problem-obstruction/
- Read through WebFetch (a text extract with short verbatim quotes; formulas on the page are images, so the extract
  transcribes them). Not a full reading of the page; re-read in a browser if anything depends on details.
- Q (Claim 1, hypothesis): "Suppose P(l_1,...,l_k) is such that that the convex hull of the forbidden sign patterns of P
  contains the origin." Conclusion: "Then one cannot use the above sieve-theoretic approach to establish the existence
  of an n such that" P(L_1(n),...,L_k(n)) holds. Called "slightly informal"; "This claim is not precisely a theorem,
  because it presumes a certain 'Liouville pseudorandomness conjecture'".
- Q: "the property 'at least j of the k numbers l_1,...,l_k is prime' is subject to the parity obstruction as soon as
  j >= k/2 + 1." "Thus, the largest number of elements of a k-tuple that one can force to be prime by purely
  sieve-theoretic methods is k/2, rounded up."
- Q (Example 4, graph G, property "an edge {i,j} with l_i, l_j both prime"): "We claim that this property is subject to
  the parity problem precisely when G is two-colourable." Converse via an odd cycle.
- Weight construction: non-negative p on forbidden sign patterns summing to 1 with mean zero; w = 1 + Q(lambda(L_1(n)),...),
  "the mean zero condition allows one to eliminate the linear terms". Absence of obstruction outside the hull is
  "expected" (Hahn-Banach), not proved.
- Zeb Brady: credited with Example 5 (a six-pair property, "which Zeb Brady and I recently formalised").

## Relation to our parity paper
- Prop. prop:bipartite (1) <=> (3), item (a) (bipartite) and item (b) (k <= 2m) are in the post (heuristic framework,
  same construction). Our "Proved here" covers only the combinatorial equivalence for the stated class. NOT in the post
  as far as read: the window form (c) and Cor. cor:six (H_m < H(2m+1)), the Remark 8.1 correction.
- Earlier versions (0.2-0.6) labelled the proposition "possibly folklore" without this citation; corrected in v0.7
  (Remark rem:tao14b).

## Ake25: M. Akeno, Small gaps between Goldbach primes, arXiv:2508.02769v3 (30 Nov 2025)
- PDF via WebFetch, SHA-256 895112307a77b35ce68387f3603d8fb02dcffc9ad05da46c8c50223469061230 (not committed).
- p. 38, Sec. 5: Q "We note that there is no parity barrier for this problem when k >= 5; this follows from a
  generalization of an argument of Zeb Brady and Terence Tao" (footnote 3: "See Tao's blog post [24]. For k = 3, one can
  (albeit non-rigorously) verify the absence of the parity barrier using the non-negative weight ..."; "The case k = 4
  is more complicated."). Different setting (Goldbach primes, pairs m + n = N).
