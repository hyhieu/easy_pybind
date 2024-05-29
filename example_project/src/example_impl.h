#pragma once

template <typename T>
T add(T i, T j);

extern template int add<int>(int, int);
