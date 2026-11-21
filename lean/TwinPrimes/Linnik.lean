/-!
# The combinatorial core of Linnik's identity on squarefree numbers

For squarefree `n` with `Ω(n) = r` prime factors, an ordered factorisation of `n` into `j`
factors, each `≥ 2`, is the same as an ordered set partition of the `r` primes into `j` nonempty
blocks, so there are `j! S(r, j)` of them (`S` = Stirling numbers of the second kind). Linnik's
identity `∑_{j ≥ 1} (-1)^{j-1} t_j(n) / j = Λ(n) / log n` (with `t_j(n)` the number of such
factorisations) therefore reduces, on squarefree `n`, to the alternating identity

  `T(r) = ∑_{j=1}^{r} (-1)^{j-1} (j-1)! S(r, j) = [r = 1]`.

* `stirling2`, `stirling2_eq_zero_of_lt`, `stirling2_succ_zero`, `stirling2_five_two`,
  `stirling2_six_three`: Stirling numbers of the second kind via the standard recursion,
  their vanishing for `j > r`, `S(r+1, 0) = 0`, and the sanity values `S(5,2) = 15`,
  `S(6,3) = 90`;
* `linnikT`, `linnik_stirling`: the alternating identity `T(r) = [r = 1]`, proved for **all**
  `r` (a general telescoping proof, no finite check);
* `orderedFact`, `orderedFact_squarefree_check`: the count of ordered factorisations into `j`
  factors `≥ 2`, and a `decide` check that it equals `j! S(Ω(n), j)` for the squarefree
  `n = 30, 210, 2310` (`Ω = 3, 4, 5`) and all `j ≤ Ω(n) + 1`, together with the squarefreeness
  and the value of `Ω(n)` of these `n`.

NOT formalised here: the bijection between ordered factorisations and ordered set partitions for
general squarefree `n` (only the three finite checks above), the identity for non-squarefree `n`,
and anything analytic (`Λ`, `log`, Dirichlet series, or Linnik's identity itself).
-/

namespace TwinPrimes

/-- Stirling numbers of the second kind: `S(0,0) = 1`, `S(n+1,0) = S(0,k+1) = 0`,
`S(n+1,k+1) = (k+1) S(n,k+1) + S(n,k)`. -/
def stirling2 : Nat → Nat → Nat
  | 0, 0 => 1
  | _ + 1, 0 => 0
  | 0, _ + 1 => 0
  | n + 1, k + 1 => (k + 1) * stirling2 n (k + 1) + stirling2 n k

/-- `S(r, j) = 0` for `j > r`. -/
theorem stirling2_eq_zero_of_lt : ∀ r j, r < j → stirling2 r j = 0
  | 0, 0, h => absurd h (Nat.lt_irrefl 0)
  | _ + 1, 0, h => absurd h (Nat.not_lt_zero _)
  | 0, _ + 1, _ => rfl
  | r + 1, j + 1, h => by
    simp only [stirling2]
    rw [stirling2_eq_zero_of_lt r (j + 1) (by omega), stirling2_eq_zero_of_lt r j (by omega)]
    simp

/-- `S(r+1, 0) = 0`. -/
theorem stirling2_succ_zero (r : Nat) : stirling2 (r + 1) 0 = 0 := rfl

/-- Sanity value `S(5,2) = 15`. -/
theorem stirling2_five_two : stirling2 5 2 = 15 := by decide

/-- Sanity value `S(6,3) = 90`. -/
theorem stirling2_six_three : stirling2 6 3 = 90 := by decide

/-- Factorial (local, to stay in core Lean). -/
def linnikFact : Nat → Nat
  | 0 => 1
  | n + 1 => (n + 1) * linnikFact n

/-- `∑_{i < N} f i` in `Int`. -/
def linnikSum (f : Nat → Int) : Nat → Int
  | 0 => 0
  | N + 1 => linnikSum f N + f N

/-- The `j = i + 1` term `(-1)^{j-1} (j-1)! S(r, j) = (-1)^i i! S(r, i+1)`. -/
def linnikTerm (r i : Nat) : Int :=
  (-1) ^ i * (linnikFact i : Int) * (stirling2 r (i + 1) : Int)

/-- `T(r) = ∑_{j=1}^{r} (-1)^{j-1} (j-1)! S(r, j)` (an empty sum, `0`, for `r = 0`). -/
def linnikT (r : Nat) : Int := linnikSum (linnikTerm r) r

/-- The auxiliary `u_r(i) = (-1)^i (i+1)! S(r, i+1)`. -/
private def linnikU (r i : Nat) : Int :=
  (-1) ^ i * (linnikFact (i + 1) : Int) * (stirling2 r (i + 1) : Int)

/-- Telescoping: for `r ≥ 1`, `∑_{i ≤ N} (-1)^i i! S(r+1, i+1) = u_r(N)`. -/
private theorem linnik_telescope (r : Nat) (hr : 1 ≤ r) :
    ∀ N, linnikSum (linnikTerm (r + 1)) (N + 1) = linnikU r N
  | 0 => by
    obtain ⟨s, rfl⟩ : ∃ s, r = s + 1 := ⟨r - 1, by omega⟩
    simp [linnikSum, linnikTerm, linnikU, stirling2, linnikFact]
  | N + 1 => by
    rw [linnikSum, linnik_telescope r hr N]
    simp only [linnikU, linnikTerm, stirling2, linnikFact, Int.pow_succ]
    push_cast
    generalize ((-1 : Int) ^ N) = a
    generalize (linnikFact N : Int) = b
    generalize (stirling2 r (N + 1 + 1) : Int) = c
    generalize (stirling2 r (N + 1) : Int) = d
    grind

/-- **Alternating Stirling identity (all `r`).**
`∑_{j=1}^{r} (-1)^{j-1} (j-1)! S(r, j) = 1` if `r = 1` and `0` otherwise. -/
theorem linnik_stirling : ∀ r, linnikT r = if r = 1 then 1 else 0
  | 0 => rfl
  | 1 => by decide
  | r + 2 => by
    simp only [linnikT]
    rw [linnik_telescope (r + 1) (by omega) (r + 1), linnikU,
      stirling2_eq_zero_of_lt (r + 1) (r + 1 + 1) (by omega)]
    simp

/-- The number of ordered factorisations `n = m₁ ⋯ m_j` with every `m_i ≥ 2`. -/
def orderedFact (n : Nat) : Nat → Nat
  | 0 => if n = 1 then 1 else 0
  | j + 1 => (((List.range (n + 1)).filter (fun m => 2 ≤ m && n % m == 0)).map
      fun m => orderedFact (n / m) j).sum

/-- `n` is squarefree (`d² ∤ n` for all `2 ≤ d ≤ n`), as a `Bool`. -/
def squarefreeB (n : Nat) : Bool :=
  (List.range (n + 1)).all fun d => d < 2 || n % (d * d) != 0

/-- `Ω(n)` by trial division from `p` on, with fuel. -/
def bigOmegaAux : Nat → Nat → Nat → Nat
  | 0, _, _ => 0
  | fuel + 1, n, p =>
    if n ≤ 1 then 0
    else if n % p = 0 then bigOmegaAux fuel (n / p) p + 1
    else bigOmegaAux fuel n (p + 1)

/-- `Ω(n)`, the number of prime factors counted with multiplicity (for `n ≥ 1`). -/
def bigOmega (n : Nat) : Nat := bigOmegaAux (2 * n) n 2

set_option maxRecDepth 100000 in
/-- **Ordered factorisations of squarefree `n` (finite check).** For `n ∈ {30, 210, 2310}`:
`n` is squarefree, `Ω(n) = 3, 4, 5`, and for every `j ≤ Ω(n) + 1` the number of ordered
factorisations of `n` into `j` factors `≥ 2` is `j! S(Ω(n), j)`. -/
theorem orderedFact_squarefree_check :
    ∀ p ∈ [(30, 3), (210, 4), (2310, 5)],
      squarefreeB p.1 = true ∧ bigOmega p.1 = p.2 ∧
      ∀ j, j ≤ p.2 + 1 → orderedFact p.1 j = linnikFact j * stirling2 p.2 j := by
  decide

end TwinPrimes
