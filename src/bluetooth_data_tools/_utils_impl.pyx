from libcpp.string cimport string

import cython


cdef extern from "stdint.h":
    ctypedef unsigned long long uint64_t

cdef extern from "utils_wrapper.h":
    string _cpp_uint64_to_bdaddr(uint64_t addr)

def _int_to_bluetooth_address(addr: int) -> str:
    return _cpp_uint64_to_bdaddr(addr).decode('ascii')
