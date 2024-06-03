"""Content of the files to be generated."""

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


CLEAN_SH = r"""#!/bin/bash

rm -rf *.so build/*
"""


GITIGNORE = r"""# Do not add SO files to GIT.
*.so

# Do not add build outputs to GIT, if using setuptools.
build/*
"""


TEST_PY = r'''"""Tests for {module_name}.

Usage: pytest {module_name}_test.py
"""

import sys
from pathlib import Path


# Add the directory where {module_name}.so is located to sys.path
sys.path.insert(0, Path(__file__).absolute().parent)


def test_add():
    import {module_name}
    assert {module_name}.add(1, 2) == 3
'''


MAIN_PY = r'''"""Entry point to run {module_name}."""
import {module_name}


def main():
    output = {module_name}.add(1, 2)
    print(f"{module_name}.add(1, 2) = {{output}}.")


if __name__ == "__main__":
    main()
'''


def build_sh(module_name: str):
    return BUILD_SH.format(module_name=module_name)

def clean_sh(module_name: str):
    return CLEAN_SH.format(module_name=module_name)

def project_cc(module_name: str):
    return PROJECT_CC.format(module_name=module_name)

def impl_h(module_name: str):
    return IMPL_H.format(module_name=module_name)

def impl_cc(module_name: str):
    return IMPL_CC.format(module_name=module_name)

def gitignore():
    return GITIGNORE

def test_py(module_name: str):
    return TEST_PY.format(module_name=module_name)

def main_py(module_name: str):
    return MAIN_PY.format(module_name=module_name)
