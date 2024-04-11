pip install --upgrade pip
zip -r cairo-lang-0.13.1a0.zip cairo-lang-0.13.1a0
pip install cairo-lang-0.13.1a0.zip
pip install aiofiles

cairo-compile --cairo_path=./src src/starkware/cairo/cairo_verifier/layouts/all_cairo/cairo_verifier.cairo --output cairo_verifier.json --no_debug_info --proof_mode

cairo-run \
    --program=cairo_verifier.json \
    --layout=recursive_with_poseidon \
    --program_input=cairo_verifier_input.json \
    --air_public_input=cairo_verifier_public_input.json \
    --air_private_input=cairo_verifier_private_input.json \
    --trace_file=cairo_verifier_trace.json \
    --memory_file=cairo_verifier_memory.json \
    --print_output \
    --proof_mode \
    --print_info