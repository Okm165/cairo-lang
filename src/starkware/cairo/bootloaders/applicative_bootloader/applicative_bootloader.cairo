%builtins output pedersen range_check bitwise poseidon

from starkware.cairo.bootloaders.simple_bootloader.run_simple_bootloader import (
    run_simple_bootloader,
    verify_non_negative,
)
from starkware.cairo.common.cairo_builtins import HashBuiltin, PoseidonBuiltin
from starkware.cairo.common.hash import hash2
from starkware.cairo.common.memcpy import memcpy
from starkware.cairo.common.registers import get_fp_and_pc
from starkware.cairo.cairo_verifier.objects import CairoVerifierOutput

func main{
    output_ptr: felt*,
    pedersen_ptr: HashBuiltin*,
    range_check_ptr,
    bitwise_ptr,
    poseidon_ptr: PoseidonBuiltin*,
}() {
    alloc_locals;

    let (__fp__, _) = get_fp_and_pc();

    // A pointer to the aggregator's task output.
    local aggregator_output_ptr: felt*;
    %{
        from starkware.cairo.bootloaders.applicative_bootloader.objects import ApplicativeBootloaderInput
        from starkware.cairo.bootloaders.simple_bootloader.objects import SimpleBootloaderInput

        # Create a segment for the aggregator output.
        ids.aggregator_output_ptr = segments.add()

        # Load the applicative bootloader input and the aggregator task.
        applicative_bootloader_input = ApplicativeBootloaderInput.Schema().load(program_input)
        aggregator_task = applicative_bootloader_input.aggregator_task.load_task()

        # Create the simple bootloader input.
        simple_bootloader_input = SimpleBootloaderInput(
            tasks=[aggregator_task], fact_topologies_path=None, single_page=True
        )

        # Change output builtin state to a different segment in preparation for running the
        # aggregator task.
        applicative_output_builtin_state = output_builtin.get_state()
        output_builtin.new_state(base=ids.aggregator_output_ptr)
    %}

    // Save aggregator output start.
    let aggregator_output_start: felt* = aggregator_output_ptr;

    // Execute the simple bootloader with the aggregator task.
    run_simple_bootloader{output_ptr=aggregator_output_ptr}();
    let range_check_ptr = range_check_ptr;
    let bitwise_ptr = bitwise_ptr;
    let pedersen_ptr: HashBuiltin* = pedersen_ptr;
    let poseidon_ptr: PoseidonBuiltin* = poseidon_ptr;
    local aggregator_output_end: felt* = aggregator_output_ptr;

    // Check that exactly one task was executed.
    assert aggregator_output_start[0] = 1;

    // Extract the aggregator output size and program hash.
    let aggregator_output_length = aggregator_output_end - aggregator_output_start - 1;
    let aggregator_program_hash = aggregator_output_start[1];
    let aggregator_input_ptr = &aggregator_output_start[2];

    // Allocate a segment for the bootloader output.
    local bootloader_output_ptr: felt*;
    %{
        from starkware.cairo.bootloaders.simple_bootloader.objects import SimpleBootloaderInput

        # Save the aggregator's fact_topologies before running the bootloader.
        aggregator_fact_topologies = fact_topologies
        fact_topologies = []

        # Create a segment for the bootloader output.
        ids.bootloader_output_ptr = segments.add()

        # Create the bootloader input.
        bootloader_input = SimpleBootloaderInput(
            tasks=[applicative_bootloader_input.tasks], fact_topologies_path=None, single_page=True
        )

        # Change output builtin state to a different segment in preparation for running the
        # bootloader.
        output_builtin.new_state(base=ids.bootloader_output_ptr)
    %}

    // Save the bootloader output start.
    let bootloader_output_start = bootloader_output_ptr;

    // Execute the bootloader.
    run_simple_bootloader{output_ptr=bootloader_output_ptr}();
    let range_check_ptr = range_check_ptr;
    let bitwise_ptr = bitwise_ptr;
    let pedersen_ptr: HashBuiltin* = pedersen_ptr;
    let poseidon_ptr: PoseidonBuiltin* = poseidon_ptr;
    local bootloader_output_end: felt* = bootloader_output_ptr;

    // Check that exactly two tasks were executed.
    assert bootloader_output_start[0] = 2;

    // Extract the bootloader outputs.
    let bootloader_output_length = bootloader_output_end - bootloader_output_start - 1;
    let bootloader_left_program_hash = bootloader_output_start[1];
    let bootloader_left_program_output: CairoVerifierOutput* = cast(
        &bootloader_output_start[2], CairoVerifierOutput*
    );
    let bootloader_right_program_hash = bootloader_output_start[4];
    let bootloader_right_program_output: CairoVerifierOutput* = cast(
        &bootloader_output_start[5], CairoVerifierOutput*
    );

    // Assert that the bootloader ran cairo0 verifiers.
    assert bootloader_left_program_hash = bootloader_right_program_hash;
    // TODO assert verifier program hash

    // Assert that the verifiers verify applicative bootloader runs.
    assert bootloader_left_program_output.program_hash = bootloader_right_program_output.program_hash;
    // TODO assert applicative bootloader program hash

    // Assert that the bootloader output agrees with the aggregator input.
    assert aggregator_input_ptr[0] = bootloader_left_program_output.output_hash;
    assert aggregator_input_ptr[1] = bootloader_right_program_output.output_hash;

    %{
        # Restore the output builtin state.
        output_builtin.set_state(applicative_output_builtin_state)
    %}

    // Output:
    // * The aggregator program hash.
    assert output_ptr[0] = aggregator_program_hash;
    let output_ptr = &output_ptr[1];

    // Output the aggregated output.
    let aggregated_output_ptr = aggregator_input_ptr + bootloader_output_length;
    let aggregated_output_length = aggregator_output_end - aggregated_output_ptr;
    memcpy(dst=output_ptr, src=aggregated_output_ptr, len=aggregated_output_length);
    let output_ptr = output_ptr + aggregated_output_length;

    return ();
}
