"""The setup.py file for the example project.

Usage: python3 setup.py build_ext --inplace
"""

import os
import sys
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension
from setuptools.command.build_ext import build_ext


class CustomBuildExtCommand(_build_ext):
    def run(self):
        build_ext.run(self)
        for ext in self.extensions:
            build_ext_ = self.get_ext_fullpath(ext.name)
            new_name = os.path.join(os.path.dirname(build_ext), "my_project.so")
            if os.path.exists(new_name):
                os.remove(new_name)
            os.rename(build_ext, new_name)


ext_modules = [
    Pybind11Extension(
        "example",  # This will be the intermediate name
        [
            "src/example.cc",
            "src/example_impl.cc",
        ],
        define_macros=[("VERSION_INFO", "0.0.1")],
    ),
]


setup(
    name="example",
    version="0.0.1",
    ext_modules=ext_modules,
    cmdclass={
        "build_ext": CustomBuildExtCommand,
    },
    zip_safe=False,
)
