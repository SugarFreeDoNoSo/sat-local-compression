import Std

/-!
# Finite image cardinality without Mathlib

`distinctList` keeps exactly one occurrence of every list element.  Its length
is therefore a numerical cardinality of a finite image, even when the ambient
type is infinite.  Classical equality is used only to define this finite
deduplication; no extra axioms or theorem placeholders are declared here.
-/

namespace ResidualWidths

universe u v w

attribute [local instance] Classical.propDecidable

/-- Remove duplicates, keeping the last occurrence of each element. -/
noncomputable def distinctList {A : Type u} : List A → List A
  | [] => []
  | a :: xs => by
      classical
      exact if a ∈ xs then distinctList xs else a :: distinctList xs

/-- Number of distinct elements, defined as the length of a deduplicated list. -/
noncomputable def distinctCount {A : Type u} (xs : List A) : Nat :=
  (distinctList xs).length

@[simp] theorem mem_distinctList {A : Type u} (a : A) (xs : List A) :
    a ∈ distinctList xs ↔ a ∈ xs := by
  classical
  induction xs with
  | nil => simp [distinctList]
  | cons b xs ih =>
      by_cases hb : b ∈ xs
      · rw [distinctList, ite_eq_left hb, ih]
        constructor
        · intro ha
          exact List.mem_cons_of_mem b ha
        · intro ha
          rcases List.mem_cons.mp ha with hab | ha
          · simpa [hab] using hb
          · exact ha
      · simp only [distinctList, ite_eq_right hb, List.mem_cons, ih]

theorem nodup_distinctList {A : Type u} (xs : List A) :
    (distinctList xs).Nodup := by
  classical
  induction xs with
  | nil => simp [distinctList]
  | cons a xs ih =>
      by_cases ha : a ∈ xs
      · simpa [distinctList, ha] using ih
      · rw [distinctList, ite_eq_right ha]
        exact List.nodup_cons.mpr ⟨by simpa using ha, ih⟩

@[simp] theorem distinctCount_nil {A : Type u} :
    distinctCount ([] : List A) = 0 := rfl

theorem distinctCount_cons {A : Type u} (a : A) (xs : List A) :
    distinctCount (a :: xs) =
      if a ∈ xs then distinctCount xs else distinctCount xs + 1 := by
  classical
  by_cases ha : a ∈ xs <;> simp [distinctCount, distinctList, ha]

/-- A finite image has at most as many distinct elements as its enumeration. -/
theorem distinctCount_le_length {A : Type u} (xs : List A) :
    distinctCount xs ≤ xs.length := by
  classical
  induction xs with
  | nil => simp
  | cons a xs ih =>
      rw [distinctCount_cons]
      by_cases ha : a ∈ xs
      · simp only [ite_eq_left ha, List.length_cons]
        exact Nat.le_trans ih (Nat.le_succ _)
      · simp only [ite_eq_right ha, List.length_cons]
        exact Nat.add_le_add_right ih 1

/-- If equality of `g`-images forces equality of `f`-images on a finite list,
the image of `f` has no more distinct values than the image of `g`. -/
theorem distinctCount_le_of_fiber_imp
    {P : Type u} {A : Type v} {B : Type w}
    (xs : List P) (f : P → A) (g : P → B)
    (h : ∀ p ∈ xs, ∀ q ∈ xs, g p = g q → f p = f q) :
    distinctCount (xs.map f) ≤ distinctCount (xs.map g) := by
  classical
  revert h
  induction xs with
  | nil => intro h; simp
  | cons p xs ih =>
      intro h
      have htail : ∀ q ∈ xs, ∀ r ∈ xs, g q = g r → f q = f r := by
        intro q hq r hr hqr
        exact h q (by simp [hq]) r (by simp [hr]) hqr
      have hle := ih htail
      by_cases hg : g p ∈ xs.map g
      · have hf : f p ∈ xs.map f := by
          rcases List.mem_map.mp hg with ⟨q, hq, hqp⟩
          exact List.mem_map.mpr
            ⟨q, hq, (h p (by simp) q (by simp [hq]) hqp.symm).symm⟩
        simpa only [List.map_cons, distinctCount_cons, ite_eq_left hf, ite_eq_left hg]
          using hle
      · by_cases hf : f p ∈ xs.map f
        · simp only [List.map_cons, distinctCount_cons, ite_eq_left hf, ite_eq_right hg]
          exact Nat.le_trans hle (Nat.le_succ _)
        · simpa only [List.map_cons, distinctCount_cons, ite_eq_right hf, ite_eq_right hg]
            using Nat.add_le_add_right hle 1

/-- Equal fibers on the enumerated domain give equal finite image cardinalities. -/
theorem distinctCount_eq_of_fiber_iff
    {P : Type u} {A : Type v} {B : Type w}
    (xs : List P) (f : P → A) (g : P → B)
    (h : ∀ p ∈ xs, ∀ q ∈ xs, g p = g q ↔ f p = f q) :
    distinctCount (xs.map f) = distinctCount (xs.map g) := by
  apply Nat.le_antisymm
  · exact distinctCount_le_of_fiber_imp xs f g
      (fun p hp q hq => (h p hp q hq).mp)
  · exact distinctCount_le_of_fiber_imp xs g f
      (fun p hp q hq => (h p hp q hq).mpr)

/-- A pointwise change of representation preserves the finite image count. -/
theorem distinctCount_map_eq_of_pointwise
    {P : Type u} {A : Type v}
    (xs : List P) (f g : P → A)
    (h : ∀ p ∈ xs, f p = g p) :
    distinctCount (xs.map f) = distinctCount (xs.map g) := by
  apply distinctCount_eq_of_fiber_iff xs f g
  intro p hp q hq
  rw [h p hp, h q hq]

end ResidualWidths
