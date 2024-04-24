zip -r cairo-lang-0.13.1.zip cairo-lang-0.13.1
pip install cairo-lang-0.13.1.zip

cairo-compile --cairo_path=./src src/starkware/starknet/core/os/os.cairo --output starknet_os_compiled.json --no_debug_info --proof_mode