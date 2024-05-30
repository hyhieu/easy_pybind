#include "example_impl.h"

template<typename T>
T add(T a, T b) { return a + b; }

template<> int add<int>(int a, int b) {
    return a + b;
}
