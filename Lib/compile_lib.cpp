#include <pybind11/pybind11.h>
#include "library.h"

namespace py = pybind11;

PYBIND11_MODULE(cpp_text_check, m) {
    m.def("checkResult", &checkResult);
};
