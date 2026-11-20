/-!
# Odd-order Chowla inputs and the Fano target (Session 38)

Sign patterns on 7 positions are encoded by `m < 128`: bit `i` of `m` is set iff `s_i = -1`
(position `i` "prime-like"). The target is "all three positions of some Fano line are prime".
* `fano_not_two_colourable`: no pattern `m` has both `m` and its complement free of lines.
  Hence no pattern weight with `Ψ(s) = Ψ(-s)` (all odd Fourier coefficients zero) kills the target.
* `fano_fair_weight`: the weight `1` on the all-plus pattern and on the 7 complements of lines
  is non-negative, kills the target and is fair (all singleton sums vanish).
* `fano_line_certificate`: on every line-free pattern, `Σ_i s_i + Σ_L Π_{i∈L} s_i ≥ 2`; so a
  non-negative weight supported on line-free patterns whose singleton and line coefficients all
  vanish is zero (sum the inequality against the weight).
-/
namespace TwinPrimes

/-- Bit masks of the 7 lines {0,1,2}, {0,3,4}, {0,5,6}, {1,3,5}, {1,4,6}, {2,3,6}, {2,4,5}. -/
def fanoLines : List Nat := [7, 25, 97, 42, 82, 76, 52]

/-- `m` contains no line. -/
def fanoFree (m : Nat) : Bool := fanoLines.all (fun L => (m &&& L) != L)

/-- The sign `s_i` of pattern `m`. -/
def fanoSgn (m i : Nat) : Int := if m.testBit i then -1 else 1

/-- The character `Π_{i ∈ L} s_i`. -/
def fanoChi (m L : Nat) : Int := ((List.range 7).filter (fun i => L.testBit i)).foldl (fun a i => a * fanoSgn m i) 1

theorem fanoLines_pairwise_meet :
    fanoLines.all (fun L => fanoLines.all (fun L' => L == L' || (L &&& L') != 0)) = true := by decide

set_option maxRecDepth 20000 in
theorem fano_not_two_colourable :
    (List.range 128).all (fun m => !(fanoFree m && fanoFree (127 ^^^ m))) = true := by decide

/-- The fair weight: `1` on the all-plus pattern `0` and on the complements of the lines. -/
def fanoW (m : Nat) : Int := if m == 0 || (fanoLines.map (fun L => 127 ^^^ L)).contains m then 1 else 0

set_option maxRecDepth 20000 in
theorem fano_fair_weight :
    (List.range 128).all (fun m => fanoW m == 0 || fanoFree m) = true ∧
    (List.range 7).all (fun i => ((List.range 128).map (fun m => fanoW m * fanoSgn m i)).sum == 0) = true ∧
    ((List.range 128).map fanoW).sum = 8 := by decide

set_option maxRecDepth 20000 in
theorem fano_line_certificate :
    (List.range 128).all (fun m => !fanoFree m ||
      decide (2 ≤ ((List.range 7).map (fanoSgn m)).sum + (fanoLines.map (fanoChi m)).sum)) = true := by decide

end TwinPrimes
