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
