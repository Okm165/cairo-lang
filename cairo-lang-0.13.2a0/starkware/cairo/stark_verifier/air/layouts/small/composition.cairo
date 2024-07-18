from starkware.cairo.common.ec import StarkCurve
from starkware.cairo.common.math import assert_nn
from starkware.cairo.common.pow import pow
from starkware.cairo.common.registers import get_fp_and_pc
from starkware.cairo.stark_verifier.air.diluted import get_diluted_prod
from starkware.cairo.stark_verifier.air.layout import AirWithLayout
from starkware.cairo.stark_verifier.air.layouts.small.autogenerated import (
    CONSTRAINT_DEGREE,
    ECDSA_BUILTIN_RATIO,
    ECDSA_BUILTIN_REPETITIONS,
    MASK_SIZE,
    N_CONSTRAINTS,
    PEDERSEN_BUILTIN_RATIO,
    PEDERSEN_BUILTIN_REPETITIONS,
    PUBLIC_MEMORY_STEP,
    eval_composition_polynomial,
)
from starkware.cairo.stark_verifier.air.layouts.small.global_values import (
    EcdsaSigConfig,
    EcPoint,
    GlobalValues,
    InteractionElements,
)
from starkware.cairo.stark_verifier.air.layouts.small.periodic_columns import (
    eval_ecdsa_x,
    eval_ecdsa_y,
    eval_pedersen_x,
    eval_pedersen_y,
)
from starkware.cairo.stark_verifier.air.layouts.small.public_verify import segments
from starkware.cairo.stark_verifier.air.public_input import get_public_memory_product_ratio
from starkware.cairo.stark_verifier.air.traces import TracesCommitment

// Constants.
const SHIFT_POINT_X = 0x49ee3eba8c1600700ee1b87eb599f16716b0b1022947733551fde4050ca6804;
const SHIFT_POINT_Y = 0x3ca0cfe4b3bc6ddf346d49d06ea0ed34e621062c0e056c1d0405d266e10268a;

// Evaluates the composition polynomial at a point, given the mask_values and the constraint
// coefficients.
func traces_eval_composition_polynomial{range_check_ptr}(
    air: AirWithLayout*,
    commitment: TracesCommitment*,
    mask_values: felt*,
    constraint_coefficients: felt*,
    point: felt,
    trace_domain_size: felt,
    trace_generator: felt,
) -> (res: felt) {
    alloc_locals;

    tempvar interaction_elements: InteractionElements* = cast(
        commitment.interaction_elements, InteractionElements*
    );
    tempvar public_input = commitment.public_input;
    let (__fp__, _) = get_fp_and_pc();

    // Public memory.
    let memory_z = interaction_elements.memory__multi_column_perm__perm__interaction_elm;
    let memory_alpha = interaction_elements.memory__multi_column_perm__hash_interaction_elm0;
    tempvar public_memory_column_size = trace_domain_size / PUBLIC_MEMORY_STEP;
    assert_nn(public_memory_column_size);
    let (public_memory_prod_ratio) = get_public_memory_product_ratio(
        public_input=public_input,
        z=memory_z,
        alpha=memory_alpha,
        public_memory_column_size=public_memory_column_size,
    );

    // Periodic columns.
    let (n_steps) = pow(2, public_input.log_n_steps);
    tempvar n_pedersen_hash_copies = n_steps / (
        PEDERSEN_BUILTIN_RATIO * PEDERSEN_BUILTIN_REPETITIONS
    );
    assert_nn(n_pedersen_hash_copies);
    let (pedersen_point) = pow(point, n_pedersen_hash_copies);
    let (pedersen__points__x) = eval_pedersen_x(pedersen_point);
    let (pedersen__points__y) = eval_pedersen_y(pedersen_point);

    tempvar n_ecdsa_signature_copies = n_steps / (ECDSA_BUILTIN_RATIO * ECDSA_BUILTIN_REPETITIONS);
    assert_nn(n_ecdsa_signature_copies);
    let (ecdsa_point) = pow(point, n_ecdsa_signature_copies);
    let (ecdsa__generator_points__x) = eval_ecdsa_x(ecdsa_point);
    let (ecdsa__generator_points__y) = eval_ecdsa_y(ecdsa_point);

    // Global values.
    local global_values: GlobalValues = GlobalValues(
        trace_length=trace_domain_size,
        initial_pc=public_input.segments[segments.PROGRAM].begin_addr,
        final_pc=public_input.segments[segments.PROGRAM].stop_ptr,
        initial_ap=public_input.segments[segments.EXECUTION].begin_addr,
        final_ap=public_input.segments[segments.EXECUTION].stop_ptr,
        initial_pedersen_addr=public_input.segments[segments.PEDERSEN].begin_addr,
        initial_range_check_addr=public_input.segments[segments.RANGE_CHECK].begin_addr,
        initial_ecdsa_addr=public_input.segments[segments.ECDSA].begin_addr,
        range_check_min=public_input.range_check_min,
        range_check_max=public_input.range_check_max,
        offset_size=2 ** 16,
        half_offset_size=2 ** 15,
        pedersen__shift_point=EcPoint(x=SHIFT_POINT_X, y=SHIFT_POINT_Y),
        ecdsa__sig_config=EcdsaSigConfig(
            alpha=StarkCurve.ALPHA,
            beta=StarkCurve.BETA,
            shift_point=EcPoint(x=SHIFT_POINT_X, y=SHIFT_POINT_Y),
        ),
        pedersen__points__x=pedersen__points__x,
        pedersen__points__y=pedersen__points__y,
        ecdsa__generator_points__x=ecdsa__generator_points__x,
        ecdsa__generator_points__y=ecdsa__generator_points__y,
        memory__multi_column_perm__perm__interaction_elm=memory_z,
        memory__multi_column_perm__hash_interaction_elm0=memory_alpha,
        range_check16__perm__interaction_elm=(
            interaction_elements.range_check16__perm__interaction_elm
        ),
        memory__multi_column_perm__perm__public_memory_prod=public_memory_prod_ratio,
        range_check16__perm__public_memory_prod=1,
    );

    return eval_composition_polynomial(
        mask_values=mask_values,
        constraint_coefficients=constraint_coefficients,
        point=point,
        trace_generator=trace_generator,
        global_values=&global_values,
    );
}
