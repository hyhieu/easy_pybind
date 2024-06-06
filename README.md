# Easy PyBind11

A simple package to generate the boilerplate research code needed to
build a Python/C++ project with PyBind11.

## Installation

From source:
```bash
$ git clone https://github.com/hyhieu/easy_pybind.git
$ cd easy_pybind
$ pip install .
```

From PyPI:
```bash
$ pip install easy_pybind
```

## Usage

The intended usage for `easy_pybind` is to generate a new project:
```plaintext
$ easy-pybind create \
    --module-name="cpp_example" \
    [--cuda] [--with-gitignore] [--with-pytest] [--with-pymain]
```

This will create a folder called `cpp_example` with the following files:
```bash
cpp_example/
├─ .gitignore              # if you have --with-ignore
├─ build.sh                # script to build the module
├─ clean.sh                # script to clean up the build
├─ src/
│  ├─ cpp_example.cc       # entry file to the module
│  ├─ cpp_example_impl.cc  # main implementation of the module, will
│  │                       # be cpp_example_impl.cu if --cuda is given
│  └─ cpp_example_impl.h
├─ cpp_example_test.py     # if you have --with-pytest
└─ main.py                 # if you have --with-pymain
```

For further usage options, please refer to `easy-pybind --help`.
