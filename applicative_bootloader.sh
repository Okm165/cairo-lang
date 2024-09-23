export PYTHONPATH=.
cairo-compile --cairo_path=src src/starkware/cairo/bootloaders/applicative_bootloader/applicative_bootloader.cairo --no_debug_info --output compiled_programs/applicative_bootloader.compiled.json
cairo-run --program compiled_programs/applicative_bootloader.compiled.json --program_input compiled_programs/applicative_bootloader.input.json  --print_info --print_output --layout recursive_with_poseidon

