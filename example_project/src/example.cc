#include "pybind11/pybind11.h"

#include "example_impl.h"


PYBIND11_MODULE(example, m) {
    m.doc() = "pybind11 example plugin"; // optional module docstring
    m.def("add", &add<int>, "A function which adds two numbers");
}
