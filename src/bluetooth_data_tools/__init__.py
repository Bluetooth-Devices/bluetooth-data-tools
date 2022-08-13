"""Bluetooth data tools."""
from __future__ import annotations

__version__ = "0.1.2"


from struct import Struct

L_PACK = Struct(">L")


def short_address(address: str) -> str:
    """Convert a Bluetooth address to a short address."""
    results = address.replace("-", ":").split(":")
    return f"{results[-2].upper()}{results[-1].upper()}"[-4:]


def newest_manufacturer_data(manufacturer_data: dict[int, bytes]) -> bytes | None:
    """Return the raw data from manufacturer data."""
    if manufacturer_data and (last_id := list(manufacturer_data)[-1]):
        return manufacturer_data[last_id]
    return None


def address_to_bytes(address: str) -> bytes:
    """Return the address as bytes."""
    if ":" not in address:
        address_as_int = 0
    else:
        address_as_int = int(address.replace(":", ""), 16)
    return L_PACK.pack(address_as_int)


def manufacturer_data_to_raw(manufacturer_id: int, manufacturer_data: bytes) -> bytes:
    """Return the raw data from manufacturer data."""
    return _pad_manufacturer_data(
        int(manufacturer_id).to_bytes(2, byteorder="little") + manufacturer_data
    )


def _pad_manufacturer_data(manufacturer_data: bytes) -> bytes:
    """Pad manufacturer data to the format needs."""
    return b"\x00" * 2 + manufacturer_data
