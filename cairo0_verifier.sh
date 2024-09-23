export PYTHONPATH=.
cairo-compile --cairo_path=src src/starkware/cairo/cairo_verifier/layouts/all_cairo/cairo_verifier.cairo --no_debug_info --output compiled_programs/cairo0_verifier.compiled.json
cairo-run --program compiled_programs/cairo0_verifier.compiled.json --program_input compiled_programs/cairo0_verifier.input.json  --print_info --print_output --layout recursive_with_poseidon

