"""Entry point to generate PyBind11 bindings."""

# setup.py
SETUP_PY = '''"""Setup script for {}."""
from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext

ext_modules = [
    Pybind11Extension(
        "example",
        ["src/example.cc"],
        define_macros=[('VERSION_INFO', "0.0.1")],
    ),
]

setup(
    name="example",
    version="0.0.1",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)
'''

# pyproject.toml
PYPROJECT_TOML = '''# pyproject.toml
[build-system]

requires = [
    "setuptools>=42",
    "wheel",
    "pybind11>=2.11",
]

build-backend = "setuptools.build_meta"
'''

# project.cc
PROJECT_CC = '''#include "pybind11/pybind11.h"

auto& entry_fn(int i, int j) {
    return i + j;
}

PYBIND11_MODULE({project_name}, m) {
    m.doc() = "pybind11 example plugin"; // optional module docstring
    m.def("add", &add, "A function which adds two numbers");
}
'''

# main.py
MAIN_PY = """"""

# main.py
PROJECT_TEST_PY = """"""


def main(unused_args: list[str] | None = None) -> None:
    print("Hello world!")


if __name__ == "__main__":
    main()
