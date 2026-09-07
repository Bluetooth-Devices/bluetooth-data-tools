# cython: language_level=3, c_string_type=str, c_string_encoding=ascii

from libc.stdint cimport uint64_t

cdef extern from "utils_wrapper.h":
    const uint64_t BDADDR_PARSE_ERROR
    void _uint64_to_bdaddr(uint64_t address, char bdaddr[17]) nogil
    uint64_t _bdaddr_to_uint64(const char *bdaddr, size_t length) nogil


def _int_to_bluetooth_address(addr: int) -> str:
    """Convert an integer to a bluetooth address.

    A Bluetooth address is 48 bits. A wider value used to be truncated to
    its low 48 bits by the uint64_t cast (and raised OverflowError past
    2**64), handing back a valid-looking address for a device that was
    never asked about; reject it instead. Kept spelled exactly as the
    pure-Python fallback: the chained comparison measures within noise of
    the unguarded cast, while converting to a cdef uint64_t first (or
    wrapping the cast in try/except) costs ~30ns per miss.
    """
    cdef char bdaddr[17]
    if not 0 <= addr <= 0xFFFFFFFFFFFF:
        raise ValueError(f"Invalid Bluetooth address: {addr!r}")
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
