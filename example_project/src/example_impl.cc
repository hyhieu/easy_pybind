#include "example_impl.h"

template <typename T>
T add(T i, T j) {
    return i + j;
}

template int add<int>(int, int);
