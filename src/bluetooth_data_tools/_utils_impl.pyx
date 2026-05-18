# cython: language_level=3, c_string_type=str, c_string_encoding=ascii

from libc.stdint cimport uint64_t

cdef extern from "utils_wrapper.h":
    const uint64_t BDADDR_PARSE_ERROR
    const int SHORT_ADDR_PARSE_ERROR
    void _uint64_to_bdaddr(uint64_t address, char bdaddr[17]) nogil
    uint64_t _bdaddr_to_uint64(const char *bdaddr, size_t length) nogil
    int _short_address_to_buf(const char *bdaddr, size_t length, char out[4]) nogil


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


def _short_address(address: str) -> str:
    cdef char out[4]
    cdef bytes encoded
    try:
        encoded = address.encode("ascii")
    except UnicodeEncodeError:
        return _short_address_py(address)
    cdef int rc = _short_address_to_buf(encoded, len(encoded), out)
    if rc != 0:
        return _short_address_py(address)
    return <str>out[:4]


cdef str _short_address_py(str address):
    """Pure-Python fallback for inputs the native fast path rejects.

    Mirrors the historical behaviour: split on ':' (after normalising '-' to ':')
    and return the last 4 characters of the concatenation of the last two
    groups, uppercased."""
    results = address.replace("-", ":").split(":")
    last = results[-1]
    second_last = results[-2]
    return f"{second_last.upper()}{last.upper()}"[-4:]
