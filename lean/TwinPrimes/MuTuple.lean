import TwinPrimes.MuMult
import TwinPrimes.MaynardS1

/-!
# `μ` of the product of a pairwise coprime tuple

Tuples are `List Nat` as in `MaynardInv` / `MaynardS1`; pairwise coprimality is
`L.Pairwise Nat.Coprime` as in `crt_tuple_residue` / `maynard_S1_error`.

* `mu_prod_coprime`: `μ(∏ᵢ rᵢ) = ∏ᵢ μ(rᵢ)` for pairwise coprime `rᵢ` (induction on
  `mu_mul_coprime`, with `coprime_prod_of_forall` from `MaynardS1`);
* `tmu_eq_mu_prod`: the same for the rational `tmu` of `MaynardInv`, i.e. `tmu r = μ(∏ rᵢ)`;
* `pairwise_coprime_of_lcm_left/right`: if the `lcm(dᵢ, eᵢ)` are pairwise coprime (hypothesis
  `hpw` of `maynard_S1_error`), so are the `dᵢ` and the `eᵢ`;
* `mu_prod_lcm`, `tmu_lcm_left`, `tmu_lcm_right`: under that hypothesis
  `μ(∏ᵢ lcm(dᵢ,eᵢ)) = ∏ᵢ μ(lcm(dᵢ,eᵢ))`, `tmu d = μ(∏ dᵢ)`, `tmu e = μ(∏ eᵢ)` — the form in
  which `μ` enters the main term `∑ λ_d λ_e / ∏ᵢ lcm(dᵢ,eᵢ)` of `S₁` before its
  diagonalisation in `y`.

NOT formalised here: the diagonalisation itself.
-/

namespace TwinPrimes
namespace MuTuple

open MuMult MaynardInv

/-- **`μ(∏ᵢ rᵢ) = ∏ᵢ μ(rᵢ)`** for a pairwise coprime tuple `r`. -/
theorem mu_prod_coprime : ∀ L : List Nat, L.Pairwise Nat.Coprime →
    mu L.prod = (L.map mu).prod
  | [], _ => by simp [mu_one]
  | x :: L, h => by
    have h' := List.pairwise_cons.mp h
    rw [List.prod_cons, List.map_cons, List.prod_cons,
      mu_mul_coprime x L.prod (coprime_prod_of_forall h'.1), mu_prod_coprime L h'.2]

theorem iprod_cast {α} (f : α → Int) : ∀ l : List α,
    (((l.map f).prod : Int) : Rat) = (l.map fun x => (f x : Rat)).prod
  | [] => rfl
  | x :: l => by simp only [List.map_cons, List.prod_cons, Rat.intCast_mul, iprod_cast f l]

/-- **`tmu r = μ(∏ᵢ rᵢ)`** for a pairwise coprime tuple `r`. -/
theorem tmu_eq_mu_prod (r : List Nat) (h : r.Pairwise Nat.Coprime) :
    tmu r = ((mu r.prod : Int) : Rat) := by
  rw [mu_prod_coprime r h, iprod_cast]; rfl

theorem exists_mem_zipWith {f : Nat → Nat → Nat} {x : Nat} : ∀ {l l' : List Nat},
    l.length = l'.length → x ∈ l → ∃ y ∈ l', f x y ∈ List.zipWith f l l'
  | [], _, _, h => by simp at h
  | _ :: _, [], hl, _ => by simp at hl
  | a :: l, b :: l', hl, h => by
    rw [List.mem_cons] at h
    rcases h with rfl | h
    · exact ⟨b, List.mem_cons_self, by simp⟩
    · obtain ⟨y, hy, hm⟩ := exists_mem_zipWith (f := f) (by simpa using hl) h
      exact ⟨y, List.mem_cons_of_mem _ hy, by
        rw [List.zipWith_cons_cons]; exact List.mem_cons_of_mem _ hm⟩

/-- If `f a b` is always a multiple of `a`, pairwise coprimality of `zipWith f l l'` passes
to `l`. -/
theorem pairwise_coprime_of_zipWith {f : Nat → Nat → Nat} (hf : ∀ a b, a ∣ f a b) :
    ∀ {l l' : List Nat}, l.length = l'.length →
      (List.zipWith f l l').Pairwise Nat.Coprime → l.Pairwise Nat.Coprime
  | [], _, _, _ => List.Pairwise.nil
  | _ :: _, [], hl, _ => by simp at hl
  | a :: l, b :: l', hl, h => by
    rw [List.zipWith_cons_cons, List.pairwise_cons] at h
    have hl' : l.length = l'.length := by simpa using hl
    refine List.pairwise_cons.mpr ⟨fun c hc => ?_, pairwise_coprime_of_zipWith hf hl' h.2⟩
    obtain ⟨y, _, hm⟩ := exists_mem_zipWith (f := f) hl' hc
    exact Nat.Coprime.coprime_dvd_right (hf c y)
      (Nat.Coprime.coprime_dvd_left (hf a b) (h.1 _ hm))

/-- If the `lcm(dᵢ, eᵢ)` are pairwise coprime, so are the `dᵢ`. -/
theorem pairwise_coprime_of_lcm_left {ds es : List Nat} (hl : ds.length = es.length)
    (h : (List.zipWith Nat.lcm ds es).Pairwise Nat.Coprime) : ds.Pairwise Nat.Coprime :=
  pairwise_coprime_of_zipWith (fun a b => Nat.dvd_lcm_left a b) hl h

/-- If the `lcm(dᵢ, eᵢ)` are pairwise coprime, so are the `eᵢ`. -/
theorem pairwise_coprime_of_lcm_right {ds es : List Nat} (hl : ds.length = es.length)
    (h : (List.zipWith Nat.lcm ds es).Pairwise Nat.Coprime) : es.Pairwise Nat.Coprime := by
  rw [List.zipWith_comm_of_comm Nat.lcm_comm] at h
  exact pairwise_coprime_of_lcm_left hl.symm h

/-- **`μ(∏ᵢ lcm(dᵢ,eᵢ)) = ∏ᵢ μ(lcm(dᵢ,eᵢ))`** when the `lcm(dᵢ,eᵢ)` are pairwise coprime. -/
theorem mu_prod_lcm (ds es : List Nat) (h : (List.zipWith Nat.lcm ds es).Pairwise Nat.Coprime) :
    mu (List.zipWith Nat.lcm ds es).prod = (List.zipWith (fun d e => mu (Nat.lcm d e)) ds es).prod := by
  rw [mu_prod_coprime _ h, List.map_zipWith]

/-- **`tmu d = μ(∏ᵢ dᵢ)`** when the `lcm(dᵢ,eᵢ)` are pairwise coprime. -/
theorem tmu_lcm_left (ds es : List Nat) (hl : ds.length = es.length)
    (h : (List.zipWith Nat.lcm ds es).Pairwise Nat.Coprime) :
    tmu ds = ((mu ds.prod : Int) : Rat) :=
  tmu_eq_mu_prod ds (pairwise_coprime_of_lcm_left hl h)

/-- **`tmu e = μ(∏ᵢ eᵢ)`** when the `lcm(dᵢ,eᵢ)` are pairwise coprime. -/
theorem tmu_lcm_right (ds es : List Nat) (hl : ds.length = es.length)
    (h : (List.zipWith Nat.lcm ds es).Pairwise Nat.Coprime) :
    tmu es = ((mu es.prod : Int) : Rat) :=
  tmu_eq_mu_prod es (pairwise_coprime_of_lcm_right hl h)

/-- Non-vacuity check: `μ(2·3·5) = μ(2)μ(3)μ(5) = -1`. -/
theorem mu_prod_coprime_example : mu [2, 3, 5].prod = ([2, 3, 5].map mu).prod ∧
    mu [2, 3, 5].prod = -1 := by decide

end MuTuple
end TwinPrimes
