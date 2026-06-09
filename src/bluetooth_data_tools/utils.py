"""Bluetooth utils."""

from __future__ import annotations

from functools import lru_cache

try:
    from ._utils_impl import (  # noqa: F811 F401
        _int_to_bluetooth_address,
        _mac_to_int,
    )


except ImportError:

    def _int_to_bluetooth_address(address: int) -> str:
        """Convert an integer to a bluetooth address."""
        mac_hex = f"{address:012X}"
        return f"{mac_hex[0:2]}:{mac_hex[2:4]}:{mac_hex[4:6]}:{mac_hex[6:8]}:{mac_hex[8:10]}:{mac_hex[10:12]}"  # noqa: E501

    _HEX_DIGITS = frozenset("0123456789abcdefABCDEF")

    def _mac_to_int(address: str) -> int:
        """Convert a mac address to an integer.

        Mirrors the native parser: accepts the 17-char separated form
        ("AA:BB:CC:DD:EE:FF" or the Windows "AA-BB-CC-DD-EE-FF" form) and
        the 12-char unseparated form ("AABBCCDDEEFF"). Any other length, a
        separator in the wrong position, an unexpected separator character,
        or a non-hex digit raises ValueError.
        """
        length = len(address)
        if length == 17:
            if any(address[i] not in ":-" for i in (2, 5, 8, 11, 14)):
                raise ValueError(f"Invalid MAC address: {address!r}")
            hex_part = (
                address[0:2]
                + address[3:5]
                + address[6:8]
                + address[9:11]
                + address[12:14]
                + address[15:17]
            )
        elif length == 12:
            hex_part = address
        else:
            raise ValueError(f"Invalid MAC address: {address!r}")
        if not _HEX_DIGITS.issuperset(hex_part):
            raise ValueError(f"Invalid MAC address: {address!r}")
        return int(hex_part, 16)


int_to_bluetooth_address = lru_cache(maxsize=256)(_int_to_bluetooth_address)
mac_to_int = lru_cache(maxsize=256)(_mac_to_int)


def short_address(address: str) -> str:
    """Convert a Bluetooth address to a short address."""
    results = address.replace("-", ":").split(":")
    last: str = results[-1]
    second_last: str = results[-2]
    return f"{second_last.upper()}{last.upper()}"[-4:]


def human_readable_name(name: str | None, local_name: str, address: str) -> str:
    """Return a human readable name for the given name, local_name, and address."""
    return f"{name or local_name} ({short_address(address)})"


def newest_manufacturer_data(manufacturer_data: dict[int, bytes]) -> bytes | None:
    """Return the raw data from manufacturer data."""
    if not manufacturer_data:
        return None
    return manufacturer_data[next(reversed(manufacturer_data))]


def manufacturer_data_to_raw(manufacturer_id: int, manufacturer_data: bytes) -> bytes:
    """Return the raw data from manufacturer data."""
    init_bytes: bytes = int(manufacturer_id).to_bytes(2, byteorder="little")
    return b"\x00" * 2 + init_bytes + manufacturer_data
