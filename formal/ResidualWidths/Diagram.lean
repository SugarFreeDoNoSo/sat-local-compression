import ResidualWidths.FiniteImage

/-!
The residual-function width characterization for deterministic layered diagrams.

`Q` is a common carrier for states; the transition also receives the current
layer. Only reachable states at a given cut are counted. Different original
layer carriers can be embedded as disjoint copies in one common carrier.
Inputs have one fixed order; their list positions are the ordered variables.

A function supported at length `n` is false outside that length. This lets
residuals use the same total suffix type while preserving exactly equality of
the functions on the unread suffixes at each valid cut.
-/

namespace ResidualWidths

abbrev Word := List Bool

/-- Enumerate every Boolean word of a specified length. -/
def allWords : Nat → List Word
  | 0 => [[]]
  | k + 1 => (allWords k).map (false :: ·) ++ (allWords k).map (true :: ·)

theorem mem_allWords_iff {k : Nat} {p : Word} :
    p ∈ allWords k ↔ p.length = k := by
  induction k generalizing p with
  | zero => simp [allWords, List.length_eq_zero_iff]
  | succ k ih =>
    cases p with
    | nil => simp [allWords]
    | cons b p => cases b <;> simp [allWords, ih]

theorem length_allWords (k : Nat) : (allWords k).length = 2 ^ k := by
  induction k with
  | zero => rfl
  | succ k ih => simp [allWords, ih, Nat.pow_succ, Nat.mul_two]

/-- Layer-indexed deterministic transitions, initial state, and final output. -/
structure Diagram (Q : Type u) where
  initial : Q
  step : Nat → Q → Bool → Q
  output : Q → Bool

/-- Run a word from an arbitrary layer and state, reading each bit once. -/
def runFrom (D : Diagram Q) (layer : Nat) (state : Q) : Word → Q
  | [] => state
  | bit :: rest => runFrom D (layer + 1) (D.step layer state bit) rest

def run (D : Diagram Q) (p : Word) : Q := runFrom D 0 D.initial p

theorem runFrom_append (D : Diagram Q) (layer : Nat) (state : Q)
    (p s : Word) :
    runFrom D layer state (p ++ s) =
      runFrom D (layer + p.length) (runFrom D layer state p) s := by
  induction p generalizing layer state with
  | nil => simp [runFrom]
  | cons b p ih =>
    simpa [runFrom, Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using
      ih (layer + 1) (D.step layer state b)

theorem run_append (D : Diagram Q) (p s : Word) :
    run D (p ++ s) = runFrom D p.length (run D p) s := by
  simpa [run] using runFrom_append D 0 D.initial p s

theorem run_snoc (D : Diagram Q) (p : Word) (bit : Bool) :
    run D (p ++ [bit]) = D.step p.length (run D p) bit := by
  rw [run_append]
  rfl

def residual (f : Word → Bool) (p : Word) : Word → Bool :=
  fun s => f (p ++ s)

def SupportedAt (f : Word → Bool) (n : Nat) : Prop :=
  ∀ w, w.length ≠ n → f w = false

/-- Extend any fixed-length table to all words by giving false outside its length. -/
def atLength (n : Nat) (f : Word → Bool) (w : Word) : Bool :=
  if w.length = n then f w else false

theorem atLength_supported (n : Nat) (f : Word → Bool) :
    SupportedAt (atLength n f) n := by
  intro w h
  simp [atLength, h]

theorem atLength_agrees (n : Nat) (f : Word → Bool) (w : Word)
    (h : w.length = n) : atLength n f w = f w := by
  simp [atLength, h]

def CorrectAt (D : Diagram Q) (f : Word → Bool) (n : Nat) : Prop :=
  ∀ w, w.length = n → D.output (run D w) = f w

/-- Correctness at the full length forces equal residuals for equal prefix states.
The support hypothesis also handles suffixes of the wrong length. -/
theorem equal_state_equal_residual (D : Diagram Q) (f : Word → Bool) (n k : Nat)
    (support : SupportedAt f n) (correct : CorrectAt D f n)
    {p q : Word} (hp : p.length = k) (hq : q.length = k)
    (same : run D p = run D q) : residual f p = residual f q := by
  funext s
  change f (p ++ s) = f (q ++ s)
  by_cases full : (p ++ s).length = n
  · have fullq : (q ++ s).length = n := by
      simpa [List.length_append, hp, hq] using full
    calc
      f (p ++ s) = D.output (run D (p ++ s)) := (correct _ full).symm
      _ = D.output (run D (q ++ s)) := by rw [run_append, run_append, hp, hq, same]
      _ = f (q ++ s) := correct _ fullq
  · have notfullq : (q ++ s).length ≠ n := by
      simpa [List.length_append, hp, hq] using full
    rw [support _ full, support _ notfullq]

/-- Total supported residuals agree exactly when they agree on unread suffixes
of the valid length; all other suffixes give false on both sides. -/
theorem residual_eq_iff_on_valid_suffix (f : Word → Bool) (n k : Nat)
    (support : SupportedAt f n) {p q : Word}
    (hp : p.length = k) (hq : q.length = k) :
    residual f p = residual f q ↔
      ∀ s, k + s.length = n → f (p ++ s) = f (q ++ s) := by
  constructor
  · intro same s _
    exact congrFun same s
  · intro agree
    funext s
    change f (p ++ s) = f (q ++ s)
    by_cases valid : k + s.length = n
    · exact agree s valid
    · have pbad : (p ++ s).length ≠ n := by
        simpa [List.length_append, hp] using valid
      have qbad : (q ++ s).length ≠ n := by
        simpa [List.length_append, hq] using valid
      rw [support _ pbad, support _ qbad]

theorem valid_suffix_length_iff (n k : Nat) (cut : k ≤ n) (s : Word) :
    k + s.length = n ↔ s.length = n - k := by
  omega

/-- The canonical diagram's states are total residual functions.
Unreachable functions in the carrier are not counted toward any layer's width. -/
def canonical (f : Word → Bool) : Diagram (Word → Bool) where
  initial := f
  step := fun _ r bit => fun s => r (bit :: s)
  output := fun r => r []

theorem runFrom_canonical_apply (f r : Word → Bool) (layer : Nat) (p s : Word) :
    (runFrom (canonical f) layer r p) s = r (p ++ s) := by
  induction p generalizing layer r with
  | nil => rfl
  | cons b p ih =>
    simpa [runFrom, canonical] using
      ih (fun t => r (b :: t)) (layer + 1)

theorem run_canonical (f : Word → Bool) (p : Word) :
    run (canonical f) p = residual f p := by
  funext s
  exact runFrom_canonical_apply f f 0 p s

theorem canonical_correct (f : Word → Bool) (n : Nat) :
    CorrectAt (canonical f) f n := by
  intro w _
  change (run (canonical f) w) [] = f w
  rw [run_canonical]
  simp [residual]

/-- Distinct suffix functions induced by every prefix of a cut. -/
noncomputable def residualCount (f : Word → Bool) (k : Nat) : Nat :=
  distinctCount ((allWords k).map (residual f))

/-- Distinct reachable states, not the size of the ambient state carrier. -/
noncomputable def reachableWidth (D : Diagram Q) (k : Nat) : Nat :=
  distinctCount ((allWords k).map (run D))

/-- Every edge from a reachable state reaches a state in the next finite layer. -/
theorem reachable_step (D : Diagram Q) (k : Nat) (state : Q) (bit : Bool)
    (reachable : state ∈ (allWords k).map (run D)) :
    D.step k state bit ∈ (allWords (k + 1)).map (run D) := by
  rcases List.mem_map.mp reachable with ⟨p, hp, rfl⟩
  have plen : p.length = k := mem_allWords_iff.mp hp
  apply List.mem_map.mpr
  refine ⟨p ++ [bit], mem_allWords_iff.mpr ?_, ?_⟩
  · simp [plen]
  · simpa [plen] using run_snoc D p bit

/-- The ambient carrier may be infinite, but every reachable layer is finite. -/
theorem reachableWidth_le_prefixes (D : Diagram Q) (k : Nat) :
    reachableWidth D k ≤ 2 ^ k := by
  calc
    reachableWidth D k ≤ ((allWords k).map (run D)).length :=
      distinctCount_le_length _
    _ = 2 ^ k := by simp [length_allWords]

/-- L02 lower bound: every correct diagram has at least as many reachable states
as distinct residual functions. The result includes the initial and final cuts. -/
theorem residualCount_le_reachableWidth (D : Diagram Q) (f : Word → Bool)
    (n : Nat) (support : SupportedAt f n) (correct : CorrectAt D f n)
    (k : Nat) (_cut : k ≤ n) : residualCount f k ≤ reachableWidth D k := by
  apply distinctCount_le_of_fiber_imp (allWords k) (residual f) (run D)
  intro p hp q hq same
  exact equal_state_equal_residual D f n k support correct
    (mem_allWords_iff.mp hp) (mem_allWords_iff.mp hq) same

/-- The one canonical diagram attains the residual bound at every cut. -/
theorem canonical_width (f : Word → Bool) (k : Nat) :
    reachableWidth (canonical f) k = residualCount f k := by
  exact distinctCount_map_eq_of_pointwise (allWords k)
    (run (canonical f)) (residual f) (fun p _ => run_canonical f p)

theorem canonical_attains_all_cuts (f : Word → Bool) (n : Nat) :
    CorrectAt (canonical f) f n ∧
      ∀ k, k ≤ n → reachableWidth (canonical f) k = residualCount f k := by
  exact ⟨canonical_correct f n, fun k _ => canonical_width f k⟩

/-- Numerical lower bound and simultaneous attainability, the two parts of L02. -/
theorem residual_width_characterization (f : Word → Bool) (n : Nat)
    (support : SupportedAt f n) :
    (∀ (D : Diagram Q), CorrectAt D f n →
      ∀ k, k ≤ n → residualCount f k ≤ reachableWidth D k) ∧
    (CorrectAt (canonical f) f n ∧
      ∀ k, k ≤ n → reachableWidth (canonical f) k = residualCount f k) := by
  constructor
  · intro D correct k cut
    exact residualCount_le_reachableWidth D f n support correct k cut
  · exact canonical_attains_all_cuts f n

theorem initial_width (D : Diagram Q) : reachableWidth D 0 = 1 := by
  classical
  simp [reachableWidth, allWords, distinctCount_cons]

theorem initial_residual_count (f : Word → Bool) : residualCount f 0 = 1 := by
  classical
  simp [residualCount, allWords, distinctCount_cons]

/-- At the final cut the residuals are classified by their output bit.
This does not assume that both Boolean answers occur. -/
theorem terminal_residual_count (f : Word → Bool) (n : Nat)
    (support : SupportedAt f n) :
    residualCount f n = distinctCount ((allWords n).map f) := by
  apply distinctCount_eq_of_fiber_iff (allWords n) (residual f) f
  intro p hp q hq
  have plen : p.length = n := mem_allWords_iff.mp hp
  have qlen : q.length = n := mem_allWords_iff.mp hq
  constructor
  · intro same
    funext s
    change f (p ++ s) = f (q ++ s)
    cases s with
    | nil => simpa using same
    | cons b s =>
      have pbad : (p ++ b :: s).length ≠ n := by simp [List.length_append, plen]
      have qbad : (q ++ b :: s).length ≠ n := by simp [List.length_append, qlen]
      rw [support _ pbad, support _ qbad]
  · intro same
    have atEmpty := congrFun same []
    simpa [residual] using atEmpty

end ResidualWidths
