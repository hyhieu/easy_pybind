"""Entry point to generate PyBind11 bindings.

python3 main.py --module-name example
"""

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


CLEAN_SH = r"""#!/bin/bash

rm -rf *.so build*
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


def main(args: argparse.Namespace) -> None:
    module_name = args.module_name
    module_path = args.module_path / module_name

    print(f"Generating PyBind11 bindings for project {module_name}...", flush=True)
    module_path.mkdir(parents=True, exist_ok=True)

    (module_path / "build.sh").write_text(BUILD_SH.format(module_name=module_name))
    (module_path / "build.sh").chmod(0o755)

    (module_path / "clean.sh").write_text(CLEAN_SH)
    (module_path / "clean.sh").chmod(0o755)

    src = module_path / "src"
    src.mkdir(parents=True, exist_ok=True)
    (src / f"{module_name}.cc").write_text(PROJECT_CC.format(module_name=module_name))
    (src / f"{module_name}_impl.cc").write_text(IMPL_CC.format(module_name=module_name))
    (src / f"{module_name}_impl.h").write_text(IMPL_H.format(module_name=module_name))

    if args.with_gitignore:
        (module_path / ".gitignore").write_text(GITIGNORE)

    if args.with_pytest:
        (module_path / f"{module_name}_test.py").write_text(
            TEST_PY.format(module_name=module_name)
        )

    if args.with_pymain:
        (module_path / "main.py").write_text(MAIN_PY.format(module_name=module_name))



if __name__ == "__main__":
    class _CustomHelpFormatter(argparse.HelpFormatter):
        def _format_action_invocation(self, action):
            print(dir(action))
            if action.option_strings == ["--with-gitignore"]:
                return "--[no-]with-gitignore"
            return super()._format_action_invocation(action)

    parser = argparse.ArgumentParser(formatter_class=_CustomHelpFormatter)

    parser.add_argument(
        "--module-name",
        type=str,
        required=True,
        help=("Name of the module to generate bindings for. For instance, if the name "
              "is `cpp_example`, then a folder called `cpp_example` will be created. "
              "Later, when the module is built, you can `import cpp_example` from "
              "to use the module."),
    )

    parser.add_argument(
        "--module-path",
        type=Path,
        default=Path("."),
        required=False,
        help="Where the module should be. Defaults to the current directory.",
    )

    # --with-gitignore
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "--with-gitignore",
        dest="with_gitignore",
        action="store_true",
        help=("If given, will add `.gitignore` file to the module directory to "
              "avoid committing build outputs into GIT."),
    )
    group.add_argument(
        "--no-with-gitignore",
        dest="with_gitignore",
        action="store_false",
        help=argparse.SUPPRESS)
    parser.set_defaults(with_gitignore=True)

    # --with-pytest
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "--with-pytest",
        dest="with_pytest",
        action="store_true",
        help=("If given, will generate a pytest to smoke test the module.")
    )
    group.add_argument(
        "--no-with-pytest",
        dest="with_pytest",
        action="store_false",
        help=argparse.SUPPRESS)
    parser.set_defaults(with_pytest=False)

    # --with-pymain
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "--with-pymain",
        dest="with_pymain",
        action="store_true",
        help=("If given, will generate a main.py to import and run the module.")
    )
    group.add_argument(
        "--no-with-pymain",
        dest="with_pymain",
        action="store_false",
        help=argparse.SUPPRESS)
    parser.set_defaults(with_pymain=False)

    args = parser.parse_args()
    main(args)
