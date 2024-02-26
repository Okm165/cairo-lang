from starkware.cairo.common.cairo_builtins import BitwiseBuiltin, PoseidonBuiltin, KeccakBuiltin
from starkware.cairo.common.hash import HashBuiltin
from starkware.cairo.common.registers import get_label_location
from starkware.cairo.stark_verifier.air.layout import AirWithLayout, Layout
from starkware.cairo.stark_verifier.air.layouts.recursive_with_poseidon.autogenerated import (
    CONSTRAINT_DEGREE,
    MASK_SIZE,
    N_CONSTRAINTS,
    N_DYNAMIC_PARAMS,
    NUM_COLUMNS_FIRST,
    NUM_COLUMNS_SECOND,
    eval_oods_polynomial,
)
from starkware.cairo.stark_verifier.air.layouts.recursive_with_poseidon.composition import (
    traces_eval_composition_polynomial,
)
from starkware.cairo.stark_verifier.air.layouts.recursive_with_poseidon.global_values import (
    InteractionElements,
)
from starkware.cairo.stark_verifier.air.layouts.recursive_with_poseidon.public_verify import (
    public_input_validate,
)
from starkware.cairo.stark_verifier.air.oods import eval_oods_boundary_poly_at_points
from starkware.cairo.stark_verifier.air.public_input import public_input_hash
from starkware.cairo.stark_verifier.air.traces import (
    traces_commit,
    traces_config_validate,
    traces_decommit,
)
from starkware.cairo.stark_verifier.core.air_interface import AirInstance
from starkware.cairo.stark_verifier.core.stark import StarkProof, verify_stark_proof

// Builds an AirInstance object to use for STARK verification. See AirInstance at
// air_interface.cairo.
func build_air() -> (air: AirWithLayout*) {
    let (arg_public_input_hash) = get_label_location(public_input_hash);
    let (arg_public_input_validate) = get_label_location(public_input_validate);
    let (arg_traces_config_validate) = get_label_location(traces_config_validate);
    let (arg_traces_commit) = get_label_location(traces_commit);
    let (arg_traces_decommit) = get_label_location(traces_decommit);
    let (arg_traces_eval_composition_polynomial) = get_label_location(
        traces_eval_composition_polynomial
    );
    let (arg_eval_oods_boundary_poly_at_points) = get_label_location(
        eval_oods_boundary_poly_at_points
    );
    let (arg_eval_oods_polynomial) = get_label_location(eval_oods_polynomial);

    tempvar air = new AirWithLayout(
        air=AirInstance(
            public_input_hash=arg_public_input_hash,
            public_input_validate=arg_public_input_validate,
            traces_config_validate=arg_traces_config_validate,
            traces_commit=arg_traces_commit,
            traces_decommit=arg_traces_decommit,
            traces_eval_composition_polynomial=arg_traces_eval_composition_polynomial,
            eval_oods_boundary_poly_at_points=arg_eval_oods_boundary_poly_at_points,
            n_dynamic_params=N_DYNAMIC_PARAMS,
            n_constraints=N_CONSTRAINTS,
            constraint_degree=CONSTRAINT_DEGREE,
            mask_size=MASK_SIZE,
        ),
        layout=Layout(
            eval_oods_polynomial=arg_eval_oods_polynomial,
            n_original_columns=NUM_COLUMNS_FIRST,
            n_interaction_columns=NUM_COLUMNS_SECOND,
            n_interaction_elements=InteractionElements.SIZE,
        ),
    );
    return (air=air);
}

func verify_proof{
    range_check_ptr,
    pedersen_ptr: HashBuiltin*,
    bitwise_ptr: BitwiseBuiltin*,
    poseidon_ptr: PoseidonBuiltin*,
    keccak_ptr: KeccakBuiltin*,
}(proof: StarkProof*, security_bits: felt) -> () {
    let (air) = build_air();
    return verify_stark_proof(air=&air.air, proof=proof, security_bits=security_bits);
}
