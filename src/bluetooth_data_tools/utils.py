"""Bluetooth utils."""
from __future__ import annotations

from functools import lru_cache

try:
    from ._utils_impl import _int_to_bluetooth_address  # noqa: F811 F401

    int_to_bluetooth_address = lru_cache(maxsize=256)(_int_to_bluetooth_address)

except ImportError:

    @lru_cache(maxsize=256)
    def int_to_bluetooth_address(address: int) -> str:
        """Convert an integer to a bluetooth address."""
        mac_hex = f"{address:012X}"
        return f"{mac_hex[0:2]}:{mac_hex[2:4]}:{mac_hex[4:6]}:{mac_hex[6:8]}:{mac_hex[8:10]}:{mac_hex[10:12]}"  # noqa: E501
