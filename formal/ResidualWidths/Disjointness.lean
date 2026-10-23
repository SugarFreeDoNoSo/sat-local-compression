import ResidualWidths.Diagram

/-!
P03: the grouped-order disjointness predicate has minimum midpoint width `2^m`.
The input is a list of `2*m` selector bits, first the positive selectors and then
the negative selectors. This is not a conventional binary encoding of SAT.
-/

namespace ResidualWidths

/-- Coordinatewise disjointness. Unequal-length lists are rejected. -/
def disjointBits : Word → Word → Bool
  | [], [] => true
  | a :: as, b :: bs => (!(a && b)) && disjointBits as bs
  | _, _ => false

@[simp] theorem disjointBits_zero_right (a : Word) :
    disjointBits a (List.replicate a.length false) = true := by
  induction a with
  | nil => rfl
  | cons bit rest ih => simp [disjointBits, List.replicate_succ, ih]

/-- Equal disjointness answers against every equally sized suffix identify the
prefix. The head is probed by a singleton; false-leading probes recover tails. -/
theorem disjointBits_left_injective (a a' : Word)
    (lengths : a.length = a'.length)
    (same : ∀ b, b.length = a.length → disjointBits a b = disjointBits a' b) :
    a = a' := by
  induction a generalizing a' with
  | nil =>
      have empty : a' = [] := List.length_eq_zero_iff.mp lengths.symm
      exact empty.symm
  | cons bit rest ih =>
      cases a' with
      | nil => simp at lengths
      | cons bit' rest' =>
          have tails : rest.length = rest'.length := by simpa using lengths
          have zeros : disjointBits rest' (List.replicate rest.length false) = true := by
            rw [tails]
            exact disjointBits_zero_right rest'
          have probe := same (true :: List.replicate rest.length false) (by simp)
          have heads : bit = bit' := by
            apply Bool.not_inj
            simpa [disjointBits, zeros] using probe
          have tailSame : ∀ b, b.length = rest.length →
              disjointBits rest b = disjointBits rest' b := by
            intro b hb
            have probeTail := same (false :: b) (by simp [hb])
            simpa [disjointBits] using probeTail
          rw [heads, ih rest' tails tailSame]

/-- Total supported extension of the grouped incidence predicate. -/
def groupedDisjointness (m : Nat) : Word → Bool :=
  atLength (m + m) (fun w => disjointBits (w.take m) (w.drop m))

theorem groupedDisjointness_supported (m : Nat) :
    SupportedAt (groupedDisjointness m) (m + m) :=
  atLength_supported _ _

/-- On a valid grouped input, the total extension is precisely disjointness. -/
theorem groupedDisjointness_append (m : Nat) (a b : Word)
    (ha : a.length = m) (hb : b.length = m) :
    groupedDisjointness m (a ++ b) = disjointBits a b := by
  subst m
  simp [groupedDisjointness, atLength, List.length_append, hb]

/-- All `m`-bit prefixes have distinct residuals at the grouped midpoint. -/
theorem grouped_residual_injective (m : Nat) (a a' : Word)
    (ha : a.length = m) (ha' : a'.length = m)
    (same : residual (groupedDisjointness m) a =
      residual (groupedDisjointness m) a') : a = a' := by
  apply disjointBits_left_injective a a' (ha.trans ha'.symm)
  intro b hb
  have bLength : b.length = m := hb.trans ha
  have probe := congrFun same b
  simpa only [residual, groupedDisjointness_append m a b ha bLength,
    groupedDisjointness_append m a' b ha' bLength] using probe

private theorem nodup_map_of_injective (xs : List A) (f : A → B)
    (nodup : xs.Nodup) (injective : ∀ a b, f a = f b → a = b) :
    (xs.map f).Nodup := by
  induction xs with
  | nil => simp
  | cons a xs ih =>
      rcases List.nodup_cons.mp nodup with ⟨absent, tail⟩
      apply List.nodup_cons.mpr
      constructor
      · intro present
        rcases List.mem_map.mp present with ⟨b, hb, same⟩
        exact absent ((injective b a same) ▸ hb)
      · exact ih tail

/-- `allWords` enumerates each Boolean word exactly once. -/
theorem nodup_allWords (m : Nat) : (allWords m).Nodup := by
  induction m with
  | zero => simp [allWords]
  | succ m ih =>
      apply List.nodup_append.mpr
      refine ⟨?_, ?_, ?_⟩
      · exact nodup_map_of_injective (allWords m) (false :: ·) ih
          (fun _ _ h => List.cons.inj h |>.2)
      · exact nodup_map_of_injective (allWords m) (true :: ·) ih
          (fun _ _ h => List.cons.inj h |>.2)
      · intro a ha b hb same
        rcases List.mem_map.mp ha with ⟨x, _, rfl⟩
        rcases List.mem_map.mp hb with ⟨y, _, rfl⟩
        cases same

private theorem distinctCount_of_nodup (xs : List A) (nodup : xs.Nodup) :
    distinctCount xs = xs.length := by
  induction xs with
  | nil => rfl
  | cons a xs ih =>
      rcases List.nodup_cons.mp nodup with ⟨absent, tail⟩
      rw [distinctCount_cons]
      simp [absent, ih tail]

/-- P03's exact count: every one of the `2^m` prefixes gives a different residual. -/
theorem grouped_residual_count (m : Nat) :
    residualCount (groupedDisjointness m) m = 2 ^ m := by
  have imageCount := distinctCount_eq_of_fiber_iff (allWords m)
    (residual (groupedDisjointness m)) (fun a => a) (by
      intro a ha a' ha'
      constructor
      · intro same
        exact congrArg (residual (groupedDisjointness m)) same
      · intro same
        exact grouped_residual_injective m a a'
          (mem_allWords_iff.mp ha) (mem_allWords_iff.mp ha') same)
  calc
    residualCount (groupedDisjointness m) m = distinctCount (allWords m) := by
      simpa [residualCount] using imageCount
    _ = (allWords m).length := distinctCount_of_nodup _ (nodup_allWords m)
    _ = 2 ^ m := length_allWords m

/-- Any correct fixed grouped-order layered diagram needs at least `2^m`
reachable states at its midpoint. -/
theorem grouped_width_lower_bound (m : Nat) (D : Diagram Q)
    (correct : CorrectAt D (groupedDisjointness m) (m + m)) :
    2 ^ m ≤ reachableWidth D m := by
  rw [← grouped_residual_count m]
  exact residualCount_le_reachableWidth D _ (m + m)
    (groupedDisjointness_supported m) correct m (by omega)

/-- One correct canonical diagram attains the lower bound; hence it is the
minimum, not merely a lower bound. This also covers the empty `m = 0` input. -/
theorem grouped_width_characterization (m : Nat) :
    (∀ (D : Diagram Q), CorrectAt D (groupedDisjointness m) (m + m) →
      2 ^ m ≤ reachableWidth D m) ∧
    (CorrectAt (canonical (groupedDisjointness m)) (groupedDisjointness m) (m + m) ∧
      reachableWidth (canonical (groupedDisjointness m)) m = 2 ^ m) := by
  refine ⟨fun D correct => grouped_width_lower_bound m D correct, ?_⟩
  refine ⟨canonical_correct _ _, ?_⟩
  rw [canonical_width, grouped_residual_count]

end ResidualWidths
