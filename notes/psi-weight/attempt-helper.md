# Fibre integral of the weight psi_m: bounded attempt (scratch)

Parameters: k = 50, eps = 1/25, L = 1 + eps, tau = 1 - eps, W := L - tau = 2 eps = 2/25,
a > tau, c0 := a - tau > 0 (c0 = 0.077 at a = 1.037). For t' = x = (x_1..x_{k-1}), x_j >= 0,
T = sum x_j <= tau:

    I(a,x) = int_0^{L-T} (1+|A(u)|) / (a + sum_{j in A(u)} (u - x_j)) du,   A(u) = {j : x_j >= T + u - tau}.

## 1. Classification

**Partially proved, with a sufficient bound proved.** The exact equality in the task is **refuted** at
a = 1.036. At a = 1.037 the exact equality is still unproved. But the bound that was actually needed
is proved, with one computer-assisted step done in interval arithmetic:

* **Theorem A (proved, every a > tau; no numerics).** For every admissible x,

      I(a,x) <= G_a(s, nu),   s := tau - T,   nu := 1 + (1/W) sum_j min(x_j, W),

  where
  G_a(s,nu) = F(s) + int_0^W nu / (c0 + nu s + (nu-1) w) dw and F(s) = k/(k-1) log((c0+ks)/(c0+s)).
  The pair (s,nu) lies in R := {0 <= s <= tau, nu >= 1, (nu-1) W <= tau - s}.
  Equality holds when every non-zero x_j is >= W. So
  sup_{(s,nu) in R, nu-1 in Z} G_a <= sup_x I(a,x) <= sup_R G_a.
  (With nu = 1, the lower family is used only at s = tau.)
  This is the reduction to a finite-dimensional problem: only two real parameters remain, and
  small coordinates (0 < x_j < 2eps) are eliminated completely. The only thing relaxed is that
  nu may be fractional.
* **Theorem B (computer-assisted, interval arithmetic, rigorous modulo the correctness of mpmath.iv).**
  At a = 1037/1000, a * sup_R G_a < 4.14636. Hence

      4.1463295701 = a * I(a, (2eps)^10 0^39)  <=  a * sup_x I(a,x)  <  4.14636  <  4.15153462 = (1+eps) k/(k-1) log k.

  So, given Lemma lem:dual as stated in the task, the weight psi gives M_k(L,tau) < 4.14636 at
  (k, eps) = (50, 1/25). That is below the scaling bound by about 0.0052.
  (Also certified: a*sup_R G_a < 4.1472 at a = 1.036, and < 4.1466 at a = 1.038.)
* **Refuted (floating point, cross-checked three ways):** the exact claim
  "sup_x I = max_r I(a,(2eps)^r 0^{k-1-r})" fails at a = 1.036. Counterexample:
  x = (y^10, 0^39) with y = 0.0811278446 > 2eps (T = 0.8112784459):

      I(1.036, x)        = 4.0027973224   (exact piecewise-log formula, psi_weight_fibers.I)
                         = 4.0027973224   (scipy adaptive quadrature of the original u-integrand)
                         = 4.0027973103   (2*10^6-point midpoint rule of the original u-integrand)
      max_r I(1.036,(2eps)^r) = 4.0027592022 (r = 10)

  The difference is 3.8e-5, and the quadrature error is about 1e-8. In a*I terms this is
  4.14689803 against 4.14685853. It also fails at a = 1.030 and 1.035 (excess above 2eps helps
  there too). The mechanism is the excess Q = T - sum min(x_j, W): it lowers s and changes nothing
  else. At a = 1.037 the numerics support the exact claim: the best value found is 4.1463296, at
  (2eps)^10. Within the equal family with excess (s free), r = 8 and r = 9 do gain from excess at
  1.037, but they stay below r = 10 (4.1459693 and 4.1454224). The gap left open at 1.037 is between
  4.1463296 and 4.14636 (float sup_R G: 4.14635248 at s = 0.1708, nu = 10.865, a non-integer nu).

What is **not** proved: the exact equality at a = 1.037 (or for any a). Theorem A loses the
integrality of nu, and that costs at most 2.3e-5 in a*I at a = 1.037. I also did **not** re-verify
Lemma lem:dual or the claim that the weight gives exactly a * sup I; both are taken from the task.

## 2. Proofs

Throughout, W = L - tau = 2 eps, c0 = a - tau > 0, s = tau - T in [0, tau]. The fibre length is
L - T = s + W.

### 2.0 Positivity of the denominator
Let D(u) = a + sum_{j in A(u)} (u - x_j) = a - sum_{j in A(u)} (x_j - u). For u >= 0 we have
x_j - u <= x_j, so sum_{A(u)} (x_j - u) <= sum_{A(u)} x_j <= sum_j x_j = T <= tau.
(The x_j are >= 0, so dropping indices can only lower the sum.) Hence D(u) >= a - tau = c0 > 0.

### 2.1 Splitting the fibre at u = s
Write A(u) = {j : x_j >= u - s}, since T - tau = -s.

*Part 1: u in [0, s].* Here u - s <= 0 <= x_j for every j, so A(u) = {1..k-1} and |A| = k-1.
D(u) = a + (k-1)u - T = c0 + s + (k-1)u, using a - T = a - tau + s = c0 + s. So

    int_0^s k/(c0+s+(k-1)u) du = k/(k-1) [log(c0+s+(k-1)u)]_0^s = k/(k-1) log((c0+ks)/(c0+s)) = F(s).

*Part 2: u = s + w, w in (0, W].* Here j is in A iff x_j >= w. Let N(w) = #{j : x_j >= w}. Then
D = a + N(w)(s+w) - m(w), where m(w) = sum_{x_j >= w} x_j.

Layer cake. For any real y >= 0 and w > 0, (y - w)^+ = int_w^inf 1[y >= v] dv. Indicators
for x_j < w vanish, so sum_{x_j >= w} (x_j - w) = sum_j (x_j - w)^+ = int_w^inf N(v) dv. With
w = 0 this gives T = int_0^inf N(v) dv. Hence

    m(w) = N(w) w + int_w^inf N(v) dv = N(w) w + T - M(w),   M(w) := int_0^w N(v) dv = sum_j min(x_j, w)

(the last identity because int_0^w 1[x_j >= v] dv = min(x_j, w)). So

    D(s+w) = a + N s + N w - N w - T + M(w) = c0 + s + N(w) s + M(w).

Write n(w) = 1 + N(w). Then

    (*)  I(a,x) = F(s) + int_0^W n(w) / (c0 + n(w) s + M(w)) dw,  M(w) = int_0^w (n(v)-1) dv.

Here N is a non-increasing, integer-valued step function on (0, W] with finitely many jumps (at the
values x_j < W). Also M(W) = sum_j min(x_j, W) <= T = tau - s.

(Formula (*) is implemented in code/explore/psi_scratch_wform.py, function I_w. It agrees with
psi_weight_fibers.I to 1e-15 and with direct quadrature of the original integrand to about 1e-7.)

### 2.2 Lemma J (same truncated mass: the constant profile is best)
**Lemma J.** Let s >= 0 and A := c0 + s > s. Let m : (0,W] -> {0,1,2,...} be non-increasing
with finitely many jumps. Put M(w) = int_0^w m, B = M(W), mu = B/W. Then

    J := int_0^W (1+m(w)) / (A + m(w) s + M(w)) dw  <=  J_mu := int_0^W (1+mu) / (A + mu s + mu w) dw.

(With m = N and A + m s = c0 + n s this is the integral in (*). J_mu is the same integral for the
constant real profile m = mu.)

*Proof.*

(i) If mu = 0, then m = 0 almost everywhere, and both sides equal W/A. Assume mu > 0 from now on.

(ii) Let w_e = sup{w : m(w) > 0}, which lies in (0, W]. Because m is non-increasing and
integer-valued, m >= 1 on (0, w_e) and m = 0 on (w_e, W]. So M is continuous and piecewise linear.
It is strictly increasing on [0, w_e] with slope m >= 1, M(w_e) = B, and M = B on [w_e, W]. The
tail contributes int_{w_e}^W 1/(A+B) dw = (W - w_e)/(A+B).

(iii) Change of variable on [0, w_e]. Let tau(w) = M(w)/mu. This is an increasing, piecewise-linear
bijection [0, w_e] -> [0, W], because M(w_e)/mu = B/mu = W. On each linear piece
d tau = (m/mu) dw, so dw = mu q dtau with q(tau) := 1/m(w(tau)). Then q is a step function on
[0, W) with values in [1/(k-1), 1], and it is **non-decreasing**, because m is non-increasing in w
and w(tau) is increasing. Also w_e = int_0^W mu q dtau. Write C(tau) := A + mu tau. Multiplying
numerator and denominator by q, the integrand at w = w(tau) is

    (1+m)/(A + m s + M) = (1 + 1/q)/(A + s/q + mu tau) = (q+1)/(C(tau) q + s).

So int_0^{w_e} ... dw = mu int_0^W f_tau(q(tau)) dtau, where f_tau(q) := q(q+1)/(C(tau) q + s).
Adding the tail and using W - w_e = W - mu int q,

    J = W/(A+B) + mu int_0^W psi_tau(q(tau)) dtau,    psi_tau(q) := f_tau(q) - q/(A+B).

(iv) The same identity for the constant profile. Put q0 := 1/mu, so that mu int_0^W q0 = W. Then
W/(A+B) + mu int_0^W psi_tau(q0) dtau = mu int_0^W f_tau(1/mu) dtau. The integrand of the
right-hand side is mu (1/mu)(1/mu + 1)/(C/mu + s) = (1+mu)/(C + mu s) = (1+mu)/(A + mu s + mu tau).
So this equals J_mu. (This is a direct computation; it does not need mu to be an integer.) Hence

    J - J_mu = mu int_0^W [psi_tau(q(tau)) - psi_tau(q0)] dtau.

(v) Concavity. For q > 0,
f_tau'(q) = [(2q+1)(Cq+s) - C(q^2+q)]/(Cq+s)^2 = (C q^2 + 2 s q + s)/(Cq+s)^2.
Since C(Cq^2+2sq+s) - (Cq+s)^2 = Cs - s^2, we get f_tau'(q) = 1/C + s(C-s)/(C (Cq+s)^2), and so
f_tau''(q) = -2 s (C-s)/(Cq+s)^3. Now C - s = c0 + mu tau > 0, so f_tau'' <= 0, and psi_tau is
concave on (0, inf) (f_tau minus a linear function). By the tangent-line inequality for
differentiable concave functions, psi_tau(q) <= psi_tau(q0) + psi_tau'(q0)(q - q0). Hence

    J - J_mu <= mu int_0^W g(tau) h(tau) dtau,  g(tau) := psi_tau'(q0) = f_tau'(q0) - 1/(A+B),  h := q - q0.

(vi) Sign and monotonicity of g.
  (a) g >= 0. By (v), f_tau'(q0) >= 1/C(tau), since s(C-s) >= 0. Also C(tau) = A + mu tau <= A + mu W
      = A + B. So f_tau'(q0) >= 1/(A+B).
  (b) g is non-increasing in tau. For fixed q > 0, view phi(C) = (Cq^2+2sq+s)/(Cq+s)^2 as a function
      of C > 0:
      phi'(C) = [q^2 (Cq+s)^2 - (Cq^2+2sq+s) 2q (Cq+s)]/(Cq+s)^4
             = [q^2 (Cq+s) - 2q (Cq^2+2sq+s)]/(Cq+s)^3 = -(C q^3 + 3 s q^2 + 2 s q)/(Cq+s)^3 <= 0.
      C(tau) is increasing in tau, so tau -> f_tau'(q0) = phi(C(tau)) is non-increasing.
  (c) h is non-decreasing (step (iii)), and int_0^W h = (w_e - W)/mu <= 0.

(vii) Chebyshev's inequality. g is continuous and h is a bounded step function, so both are
integrable. For all sigma, tau we have (g(tau)-g(sigma))(h(tau)-h(sigma)) <= 0, because g is
non-increasing and h is non-decreasing. Integrating over [0,W]^2 gives
2W int gh - 2 (int g)(int h) <= 0, that is, int gh <= (1/W)(int g)(int h). The right side is <= 0
because int g >= 0 by (a) and int h <= 0 by (c). With (v), J - J_mu <= 0. QED.

### 2.3 Theorem A
Apply Lemma J with m = N and A = c0 + s to (*). This gives I(a,x) <= F(s) + J_mu, where
mu = M(W)/W = (1/W) sum_j min(x_j,W). Since A + mu s = c0 + nu s with nu = 1 + mu,

    J_mu = int_0^W nu/(c0 + nu s + (nu-1) w) dw,  so I(a,x) <= G_a(s, nu).

Admissibility: nu >= 1, 0 <= s <= tau, and (nu-1)W = sum min(x_j, W) <= T = tau - s.

Equality case: if every non-zero x_j is >= W, then N is constant on (0,W], equal to g = #{x_j > 0}.
So m = mu = g, q = q0, and every inequality in Lemma J is an equality. Such x realise every point
(s, g+1) with g >= 1 an integer and 0 <= s <= tau - gW: take x = ((tau-s)/g)^g, since (tau-s)/g >= W.
With g = 0 they realise only x = 0, that is, s = tau. QED.

(Sanity check: on 20000 random x, with a in [0.97, 1.2] and mixed scales, max(I - G) = 8e-15, which is
rounding error; see psi_scratch_checks.py, part (1).)

### 2.4 Theorem B: certifying sup_R G_a
Cell bound. On a cell [s1,s2] x [n1,n2] (with n1 >= 1):
* F is increasing: F'(s) = k/(k-1) [k/(c0+ks) - 1/(c0+s)] = k c0 / ((c0+ks)(c0+s)) > 0. So F <= F(s2).
* For fixed nu > 0 and w, the integrand nu/(c0 + nu s + (nu-1) w) is decreasing in s. Use s1.
* d/dnu [nu/(c0 + nu s + (nu-1)w)] = [(c0 + nu s + (nu-1)w) - nu(s+w)]/den^2 = (c0 - w)/den^2.
  So the integrand is increasing in nu for w < c0 and non-increasing for w >= c0. At a = 1.037,
  0 < c0 = 0.077 < W = 0.08, and this is asserted in interval arithmetic in the script.

Therefore G_a <= F(s2) + int_0^{c0} [nu = n2, s = s1] + int_{c0}^W [nu = n1, s = s1] on the cell.
Each integral has a closed form: nu/(nu-1) log(...), or (hi-lo)/(c0+s) when nu = 1.

Covering: s in [0, 24/25] (the last cell's right end is an interval enclosure of 24/25), and
nu in [1, 13]. Since (nu-1)W <= tau, nu <= 1 + 12 = 13. A cell is discarded only if
(n1-1)W > tau - s1 holds rigorously. Cells are bisected adaptively in floating point, and every
leaf is then re-evaluated with mpmath.iv (80-bit precision, outward rounding).

Result (`python3 code/explore/psi_scratch_certify.py 1037 1000 4.14636`): 644775 leaves, every
leaf bound has interval upper end < 4.14636, and 0 cells fail. The coarser run with theta = 4.1500
needs only 8654 leaves. At a = 1.036 and theta = 4.1472, and at a = 1.038 and theta = 4.1466,
0 cells fail as well.

## 3. Where the exact statement stands, and evidence

* The bound sup_R G_a is attained at a fractional nu (a = 1.037: nu = 10.865, s = 0.1708, value
  4.14635248). So Theorem A cannot by itself give the exact equality. One would need a version of
  Lemma J that respects integer nu (a finite-mass comparison with nu-floor/nu-ceil), and I did not
  attempt that.
* The exact equality would also need excess (x_j > 2eps) to be useless at a = 1.037 for every r.
  Numerically, dG/ds(s0-) at s0 = tau - 2eps r is -0.0060, -0.0046, +0.0130 and +0.2198 for
  r = 8, 9, 10 and 11 at a = 1.037. So excess helps r = 8 and 9 locally. Their best values
  (4.1454224 and 4.1459693) are still below r = 10 (4.1463296).
* Adversarial searches (floating point) found nothing above the equal family with excess:
  - psi_scratch_search.py: coordinate ascent in which each step maximises over one coordinate on
    its whole feasible range, with 25 random starts of six shapes (tiny coordinates, exponential,
    one large plus small, near 2eps, wide, all < 0.019). At a = 1.037, 1.04, 1.045 and 1.05 it
    found exactly the (2eps)^r value. At a = 1.03 and 1.035 it found excess configurations.
  - psi_scratch_shape.py: multi-level profiles (up to 4 levels of n, all breakpoints and s free,
    4000 Nelder-Mead runs per a). The best profile was always constant.
  - frac.py: 200000 random multi-level profiles. max(J - J_mu) = -3.6e-12, which is consistent
    with Lemma J.
  - conv.py: in a single coordinate y in [0, min(2eps, s0)], I is **not** convex (the minimum
    second difference is negative when s is small, because F is concave in s). Even so, no
    interior maximum was found. Lemma J avoids needing that.

## 4. Scripts (all floating point unless stated)
* /home/user/twin-primes/code/explore/psi_scratch_wform.py: formula (*) (I_w) and an independent
  midpoint quadrature of the original integrand (I_quad).
* /home/user/twin-primes/code/explore/psi_scratch_certify.py: **interval-arithmetic certificate**
  (Theorem B). Usage: `python3 psi_scratch_certify.py 1037 1000 4.14636`.
* /home/user/twin-primes/code/explore/psi_scratch_checks.py: the random test of Theorem A, the
  a = 1.036 counterexample by three evaluations (psi_weight_fibers.I, scipy quad, midpoint), and the
  one-sided derivatives.
* /home/user/twin-primes/code/explore/psi_scratch_search.py: adversarial coordinate ascent.
* /home/user/twin-primes/code/explore/psi_scratch_shape.py: multi-level profile search.
* /home/user/twin-primes/notes/scratch-psi/{conv,shape,frac}.py: single-coordinate convexity test,
  derivative shapes, and the same-mass profile test together with the fractional-relaxation grid.
