"""GATT Advertisement and Scan Response Data (GAP)."""


from __future__ import annotations

import logging
from collections.abc import Iterable
from dataclasses import dataclass
from enum import IntEnum
from uuid import UUID

BLE_UUID = "0000-1000-8000-00805f9b34fb"
_LOGGER = logging.getLogger(__name__)


@dataclass
class BLEGAPAdvertisement:

    local_name: str | None
    service_uuids: list[str]
    service_data: dict[str, bytes]
    manufacturer_data: dict[int, bytes]
    tx_power: int | None


class BLEGAPType(IntEnum):
    """Advertising data types."""

    TYPE_UNKNOWN = 0x00
    TYPE_FLAGS = 0x01
    TYPE_16BIT_SERVICE_UUID_MORE_AVAILABLE = 0x02
    TYPE_16BIT_SERVICE_UUID_COMPLETE = 0x03
    TYPE_32BIT_SERVICE_UUID_MORE_AVAILABLE = 0x04
    TYPE_32BIT_SERVICE_UUID_COMPLETE = 0x05
    TYPE_128BIT_SERVICE_UUID_MORE_AVAILABLE = 0x06
    TYPE_128BIT_SERVICE_UUID_COMPLETE = 0x07
    TYPE_SHORT_LOCAL_NAME = 0x08
    TYPE_COMPLETE_LOCAL_NAME = 0x09
    TYPE_TX_POWER_LEVEL = 0x0A
    TYPE_CLASS_OF_DEVICE = 0x0D
    TYPE_SIMPLE_PAIRING_HASH_C = 0x0E
    TYPE_SIMPLE_PAIRING_RANDOMIZER_R = 0x0F
    TYPE_SECURITY_MANAGER_TK_VALUE = 0x10
    TYPE_SECURITY_MANAGER_OOB_FLAGS = 0x11
    TYPE_SLAVE_CONNECTION_INTERVAL_RANGE = 0x12
    TYPE_SOLICITED_SERVICE_UUIDS_16BIT = 0x14
    TYPE_SOLICITED_SERVICE_UUIDS_128BIT = 0x15
    TYPE_SERVICE_DATA = 0x16
    TYPE_PUBLIC_TARGET_ADDRESS = 0x17
    TYPE_RANDOM_TARGET_ADDRESS = 0x18
    TYPE_APPEARANCE = 0x19
    TYPE_ADVERTISING_INTERVAL = 0x1A
    TYPE_LE_BLUETOOTH_DEVICE_ADDRESS = 0x1B
    TYPE_LE_ROLE = 0x1C
    TYPE_SIMPLE_PAIRING_HASH_C256 = 0x1D
    TYPE_SIMPLE_PAIRING_RANDOMIZER_R256 = 0x1E
    TYPE_SERVICE_DATA_32BIT_UUID = 0x20
    TYPE_SERVICE_DATA_128BIT_UUID = 0x21
    TYPE_URI = 0x24
    TYPE_3D_INFORMATION_DATA = 0x3D
    TYPE_MANUFACTURER_SPECIFIC_DATA = 0xFF


_BLEGAPType_MAP = {gap_ad.value: gap_ad for gap_ad in BLEGAPType}


def decode_advertisement_data(
    encoded_struct: bytes,
) -> Iterable[tuple[BLEGAPType, bytes]]:
    """Decode a BLE GAP AD structure."""
    offset = 0
    while offset < len(encoded_struct):
        try:
            length = encoded_struct[offset]
            if not length:
                return
            type_ = encoded_struct[offset + 1]
            if not type_:
                return
            start = offset + 2
            end = start + length - 1
            value = encoded_struct[start:end]
        except IndexError as ex:
            _LOGGER.error(
                "Invalid BLE GAP AD structure at offset %s: %s (%s)",
                offset,
                encoded_struct,
                ex,
            )
            return

        yield _BLEGAPType_MAP.get(type_, BLEGAPType.TYPE_UNKNOWN), value
        offset += 1 + length


def parse_advertisement_data(
    data: Iterable[bytes],
) -> BLEGAPAdvertisement:
    """Parse advertisement data."""
    manufacturer_data: dict[int, bytes] = {}
    service_data: dict[str, bytes] = {}
    service_uuids: list[str] = []
    local_name: str | None = None
    tx_power: int | None = None

    for gap_data in data:
        for gap_type, gap_value in decode_advertisement_data(gap_data):
            if gap_type == BLEGAPType.TYPE_SHORT_LOCAL_NAME and not local_name:
                local_name = gap_value.decode("utf-8", errors="replace")
            elif gap_type == BLEGAPType.TYPE_COMPLETE_LOCAL_NAME:
                local_name = gap_value.decode("utf-8", errors="replace")
            elif gap_type == BLEGAPType.TYPE_MANUFACTURER_SPECIFIC_DATA:
                manufacturer_id = int.from_bytes(gap_value[:2], "little")
                manufacturer_data[manufacturer_id] = gap_value[2:]
            elif gap_type in {
                BLEGAPType.TYPE_16BIT_SERVICE_UUID_COMPLETE,
                BLEGAPType.TYPE_16BIT_SERVICE_UUID_MORE_AVAILABLE,
            }:
                uuid_int = int.from_bytes(gap_value[:2], "little")
                service_uuids.append(f"0000{uuid_int:04x}-{BLE_UUID}")
            elif gap_type in {
                BLEGAPType.TYPE_128BIT_SERVICE_UUID_MORE_AVAILABLE,
                BLEGAPType.TYPE_128BIT_SERVICE_UUID_COMPLETE,
            }:
                uuid_str = str(UUID(int=int.from_bytes(gap_value[:16], "little")))
                service_uuids.append(uuid_str)
            elif gap_type == BLEGAPType.TYPE_SERVICE_DATA:
                uuid_int = int.from_bytes(gap_value[:2], "little")
                service_data[f"0000{uuid_int:04x}-{BLE_UUID}"] = gap_value[2:]
            elif gap_type == BLEGAPType.TYPE_SERVICE_DATA_32BIT_UUID:
                uuid_int = int.from_bytes(gap_value[:4], "little")
                service_data[f"{uuid_int:08x}-{BLE_UUID}"] = gap_value[4:]
            elif gap_type == BLEGAPType.TYPE_SERVICE_DATA_128BIT_UUID:
                uuid_str = str(UUID(int=int.from_bytes(gap_value[:16], "little")))
                service_data[uuid_str] = gap_value[16:]
            elif gap_type == BLEGAPType.TYPE_TX_POWER_LEVEL:
                tx_power = int.from_bytes(gap_value, "little", signed=True)

    return BLEGAPAdvertisement(
        local_name,
        service_uuids,
        service_data,
        manufacturer_data,
        tx_power,
    )
