import cython

from libc.stdlib cimport malloc


cdef extern from "stdint.h":
    ctypedef unsigned long long uint64_t

cdef extern from "utils_wrapper.h":
    void _uint64_to_bdaddr(uint64_t addr, char *bdaddr)

cdef char* uint64_to_bdaddr(uint64_t address):
    cdef char* bdaddr = <char *> malloc((18) * sizeof(char))
    if not bdaddr:
        return NULL  # malloc failed
    _uint64_to_bdaddr(address, bdaddr)
    return bdaddr



def _int_to_bluetooth_address(addr: int) -> str:
    return uint64_to_bdaddr(addr).decode('ascii')
