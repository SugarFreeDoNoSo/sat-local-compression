import ResidualWidths

set_option pp.fullNames true

-- The verification script checks each declaration's complete axiom closure.
#print axioms ResidualWidths.mem_allWords_iff
#print axioms ResidualWidths.distinctCount_le_of_fiber_imp
#print axioms ResidualWidths.equal_state_equal_residual
#print axioms ResidualWidths.residualCount_le_reachableWidth
#print axioms ResidualWidths.canonical_correct
#print axioms ResidualWidths.canonical_width
#print axioms ResidualWidths.canonical_attains_all_cuts
#print axioms ResidualWidths.residual_width_characterization
#print axioms ResidualWidths.atLength_supported
#print axioms ResidualWidths.atLength_agrees
#print axioms ResidualWidths.initial_width
#print axioms ResidualWidths.initial_residual_count
#print axioms ResidualWidths.terminal_residual_count
#print axioms ResidualWidths.residual_eq_iff_on_valid_suffix
#print axioms ResidualWidths.valid_suffix_length_iff
#print axioms ResidualWidths.reachable_step
#print axioms ResidualWidths.length_allWords
#print axioms ResidualWidths.reachableWidth_le_prefixes

-- P03 grouped-order disjointness; no other claims are formalized here.
#print axioms ResidualWidths.disjointBits_zero_right
#print axioms ResidualWidths.disjointBits_left_injective
#print axioms ResidualWidths.groupedDisjointness_supported
#print axioms ResidualWidths.groupedDisjointness_append
#print axioms ResidualWidths.grouped_residual_injective
#print axioms ResidualWidths.nodup_allWords
#print axioms ResidualWidths.grouped_residual_count
#print axioms ResidualWidths.grouped_width_lower_bound
#print axioms ResidualWidths.grouped_width_characterization
