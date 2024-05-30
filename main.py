"""Entry point to generate PyBind11 bindings."""

import argparse
from pathlib import Path


#########################################
# Content of the files to be generated. #
#########################################
PROJECT_CC = r"""#include "pybind11/pybind11.h"

#include "{module_name}_impl.h"

PYBIND11_MODULE({module_name}, m) {{
    m.doc() = "pybind11 {module_name} plugin";  // module docstring

    m.def("add", &add<int>, "An example function to add two numbers.");
}}
"""

IMPL_H = r"""#pragma once

template<typename T>
T add(T a, T b);

template<> int add<int>(int, int);
"""

IMPL_CC = r"""#include "{module_name}_impl.h"

template<typename T>
T add(T a, T b) {{ return a + b; }}

template<> int add<int>(int a, int b) {{
    return a + b;
}}
"""

BUILD_SH = r"""#!/bin/bash

MODULE_NAME="{module_name}"

PYBIND11_INCLUDES=$(python3 -m pybind11 --includes)

# If the system is MacOS, add an extra flag to the final compilation command.
if [[ "$(uname)" == "Darwin" ]]; then
    undefined_dynamic_lookup="-undefined dynamic_lookup"
else
    undefined_dynamic_lookup=""
fi

g++ \
  -O3 \
  -Wall \
  -shared \
  --std=c++17 \
  -fPIC \
  ${{undefined_dynamic_lookup}} \
  ${{PYBIND11_INCLUDES}} \
  src/${{MODULE_NAME}}.cc \
  src/${{MODULE_NAME}}_impl.cc \
  -o ${{MODULE_NAME}}.so
"""


def main(args: argparse.Namespace) -> None:
    module_name = args.module_name
    module_path = args.module_path / module_name

    print(f"Generating PyBind11 bindings for project {module_name}...", flush=True)
    module_path.mkdir(parents=True, exist_ok=True)

    (module_path / "build.sh").write_text(BUILD_SH.format(module_name=module_name))
    (module_path / "build.sh").chmod(0o755)

    src = module_path / "src"
    src.mkdir(parents=True, exist_ok=True)
    (src / f"{module_name}.cc").write_text(PROJECT_CC.format(module_name=module_name))
    (src / f"{module_name}_impl.cc").write_text(IMPL_CC.format(module_name=module_name))
    (src / f"{module_name}_impl.h").write_text(IMPL_H.format(module_name=module_name))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--module-name", type=str, required=True)
    parser.add_argument("--module-path", type=Path, default=Path("."), required=False)

    args = parser.parse_args()

    main(args)
