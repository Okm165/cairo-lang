# Introduction

[Cairo](https://cairo-lang.org/) is a programming language for writing provable programs.

# Documentation

The Cairo documentation consists of two parts: "Hello Cairo" and "How Cairo Works?".
Both parts can be found in https://cairo-lang.org/docs/.

We recommend starting from [Setting up the environment](https://cairo-lang.org/docs/quickstart.html).

# Installation instructions

You should be able to download the python package zip file directly from
[github](https://github.com/starkware-libs/cairo-lang/releases/tag/v0.12.0)
and install it using ``pip``.
See [Setting up the environment](https://cairo-lang.org/docs/quickstart.html).

However, if you want to build it yourself, you can build it from the git repository.
It is recommended to run the build inside a docker (as explained below),
since it guarantees that all the dependencies
are installed. Alternatively, you can try following the commands in the
[docker file](https://github.com/starkware-libs/cairo-lang/blob/master/Dockerfile).

## Building using the dockerfile

*Note*: This section is relevant only if you wish to build the Cairo python-package yourself,
rather than downloading it.

The root directory holds a dedicated Dockerfile, which automatically builds the package and runs
the unit tests on a simulated Ubuntu 18.04 environment.
You should have docker installed (see https://docs.docker.com/get-docker/).

Clone the repository and initialize the git submodules using:

```bash
> git clone git@github.com:starkware-libs/cairo-lang.git
> cd cairo-lang
```

Build the docker image:

```bash
> docker build --tag cairo .
```

If everything works, you should see

```bash
Successfully tagged cairo:latest
```

Once the docker image is built, you can fetch the python package zip file using:

```bash
> container_id=$(docker create cairo)
> docker cp ${container_id}:/app/cairo-lang-0.12.0.zip .
> docker rm -v ${container_id}
```
```bash
zip -r cairo-lang-0.12.0.zip cairo-lang-0.12.0
pip install cairo-lang-0.12.0.zip
```

Compile verifier:
```bash
cairo-compile --cairo_path=./src src/starkware/cairo/cairo_verifier/layouts/all_cairo/cairo_verifier.cairo --output cairo_verifier.json --no_debug_info
```

Create cairo_verifier_input.json
```json
{
    "proof": // <proof from stone prover>
}
```

Run verifier:
```bash
cairo-run \
    --program=cairo_verifier.json \
    --layout=starknet_with_keccak \
    --program_input=cairo_verifier_input.json \
    --trace_file=cairo_verifier_trace.json \
    --memory_file=cairo_verifier_memory.json \
    --print_output
```
