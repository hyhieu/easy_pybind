#!/bin/bash

PROJECT_NAME="example"

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
  ${undefined_dynamic_lookup} \
  ${PYBIND11_INCLUDES} \
  src/${PROJECT_NAME}.cc \
  src/${PROJECT_NAME}_impl.cc \
  -o ${PROJECT_NAME}.so
