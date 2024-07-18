zip -r cairo-lang-0.13.2a0.zip cairo-lang-0.13.2a0
pip install cairo-lang-0.13.2a0.zip

cairo-compile --cairo_path=./src src/starkware/cairo/cairo_verifier/layouts/all_cairo/cairo_verifier.cairo --output cairo_verifier.json --no_debug_info --proof_mode

cairo-run \
    --program=cairo_verifier.json \
    --layout=recursive_with_poseidon \
    --program_input=cairo_verifier_input.json \
    --print_output \
    --print_info