"""Bluetooth utils."""

from __future__ import annotations

from functools import lru_cache
from struct import Struct

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

    def _mac_to_int(address: str) -> int:
        """Convert a mac address to an integer."""
        length = len(address)
        if length != 17 and length != 12:
            raise ValueError(f"Invalid MAC address: {address!r}")
        return int(address.replace(":", "").replace("-", ""), 16)


int_to_bluetooth_address = lru_cache(maxsize=256)(_int_to_bluetooth_address)
mac_to_int = lru_cache(maxsize=256)(_mac_to_int)


def short_address(address: str) -> str:
    """Convert a Bluetooth address to a short address."""
    results = address.replace("-", ":").split(":")
    last: str = results[-1]
    second_last: str = results[-2]
    return f"{second_last.upper()}{last.upper()}"[-4:]


@lru_cache(maxsize=512)
def human_readable_name(name: str | None, local_name: str, address: str) -> str:
    """Return a human readable name for the given name, local_name, and address."""
    return f"{name or local_name} ({short_address(address)})"


def newest_manufacturer_data(manufacturer_data: dict[int, bytes]) -> bytes | None:
    """Return the raw data from manufacturer data."""
    if not manufacturer_data:
        return None
    return manufacturer_data[next(reversed(manufacturer_data))]


# Two pad bytes followed by a little-endian uint16 manufacturer ID.
# Mirrors the on-the-wire MSD AD prefix so callers can splice the body in
# without a separate concatenation step.
_pack_manufacturer_prefix = Struct("<2xH").pack


def manufacturer_data_to_raw(manufacturer_id: int, manufacturer_data: bytes) -> bytes:
    """Return the raw data from manufacturer data."""
    return _pack_manufacturer_prefix(manufacturer_id) + manufacturer_data
