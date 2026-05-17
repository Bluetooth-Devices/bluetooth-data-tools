# cython: language_level=3, c_string_type=str, c_string_encoding=ascii

from libc.stdint cimport uint64_t, UINT64_MAX

cdef extern from "utils_wrapper.h":
    void _uint64_to_bdaddr(uint64_t address, char bdaddr[17]) nogil
    uint64_t _bdaddr_to_uint64(const char *bdaddr, size_t length) nogil


def _int_to_bluetooth_address(addr: int) -> str:
    cdef char bdaddr[17]
    _uint64_to_bdaddr(<uint64_t>addr, bdaddr)
    return <str>bdaddr[:17]


def _mac_to_int(address: str) -> int:
    cdef Py_ssize_t str_len = len(address)
    cdef bytes encoded
    cdef const char *buf
    cdef size_t length
    cdef uint64_t result

    if str_len == 17:
        if (address[2] not in ":-" or address[5] not in ":-"
                or address[8] not in ":-" or address[11] not in ":-"
                or address[14] not in ":-"):
            raise ValueError(f"Invalid MAC address: {address!r}")
    elif str_len != 12:
        raise ValueError(f"Invalid MAC address: {address!r}")

    try:
        encoded = address.encode("ascii")
    except UnicodeEncodeError:
        raise ValueError(f"Invalid MAC address: {address!r}") from None

    buf = encoded
    length = len(encoded)
    result = _bdaddr_to_uint64(buf, length)
    if result == UINT64_MAX:
        # Sentinel: shape already validated, so this is bad hex. int() raises
        # ValueError with a message describing the actual offending input.
        return int(address.replace(":", "").replace("-", ""), 16)
    return result
