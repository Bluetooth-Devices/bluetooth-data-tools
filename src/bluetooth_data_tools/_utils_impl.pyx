# cython: language_level=3, c_string_type=str, c_string_encoding=ascii

from libc.stdint cimport uint64_t

cdef extern from "utils_wrapper.h":
    const uint64_t BDADDR_PARSE_ERROR
    void _uint64_to_bdaddr(uint64_t address, char bdaddr[17]) nogil
    uint64_t _bdaddr_to_uint64(const char *bdaddr, size_t length) nogil


def _int_to_bluetooth_address(addr: int) -> str:
    cdef char bdaddr[17]
    _uint64_to_bdaddr(<uint64_t>addr, bdaddr)
    return <str>bdaddr[:17]


def _mac_to_int(address: str) -> int:
    cdef bytes encoded
    try:
        encoded = address.encode("ascii")
    except UnicodeEncodeError:
        raise ValueError(f"Invalid MAC address: {address!r}") from None
    cdef uint64_t result = _bdaddr_to_uint64(encoded, len(encoded))
    if result == BDADDR_PARSE_ERROR:
        raise ValueError(f"Invalid MAC address: {address!r}")
    return result
