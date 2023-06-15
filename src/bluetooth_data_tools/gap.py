"""GATT Advertisement and Scan Response Data (GAP)."""
import logging
from enum import IntEnum
from functools import lru_cache
from typing import Dict, Iterable, List, Tuple

BLE_UUID = "0000-1000-8000-00805f9b34fb"
_LOGGER = logging.getLogger(__name__)


class BLEGAPAdvertisement:
    """GATT Advertisement and Scan Response Data (GAP)."""

    __slots__ = (
        "local_name",
        "service_uuids",
        "service_data",
        "manufacturer_data",
        "tx_power",
    )

    def __init__(
        self,
        local_name: str | None,
        service_uuids: List[str],
        service_data: Dict[str, bytes],
        manufacturer_data: Dict[int, bytes],
        tx_power: int | None,
    ) -> None:
        """Initialize GAP Advertisement."""
        self.local_name = local_name
        self.service_uuids = service_uuids
        self.service_data = service_data
        self.manufacturer_data = manufacturer_data
        self.tx_power = tx_power


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

_bytes = bytes


def _decode_advertisement_data(
    encoded_struct: _bytes,
) -> list[Tuple[int, bytes]]:
    """Decode a BLE GAP AD structure."""
    offset = 0
    total_length = len(encoded_struct)
    msgs: list[Tuple[int, bytes]] = []
    while offset < total_length:
        try:
            length = encoded_struct[offset]
            if not length:
                if offset + 2 < total_length:
                    # Maybe zero padding
                    offset += 1
                    continue
                break
            type_ = encoded_struct[offset + 1]
            if not type_:
                break
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
            break

        msgs.append((type_, value))
        offset += 1 + length

    return msgs


TYPE_SHORT_LOCAL_NAME = BLEGAPType.TYPE_SHORT_LOCAL_NAME.value
TYPE_COMPLETE_LOCAL_NAME = BLEGAPType.TYPE_COMPLETE_LOCAL_NAME.value
TYPE_MANUFACTURER_SPECIFIC_DATA = BLEGAPType.TYPE_MANUFACTURER_SPECIFIC_DATA.value
TYPE_16BIT_SERVICE_UUID_COMPLETE = BLEGAPType.TYPE_16BIT_SERVICE_UUID_COMPLETE.value
TYPE_16BIT_SERVICE_UUID_MORE_AVAILABLE = (
    BLEGAPType.TYPE_16BIT_SERVICE_UUID_MORE_AVAILABLE.value
)
TYPE_128BIT_SERVICE_UUID_COMPLETE = BLEGAPType.TYPE_128BIT_SERVICE_UUID_COMPLETE.value
TYPE_128BIT_SERVICE_UUID_MORE_AVAILABLE = (
    BLEGAPType.TYPE_128BIT_SERVICE_UUID_MORE_AVAILABLE.value
)
TYPE_SERVICE_DATA = BLEGAPType.TYPE_SERVICE_DATA.value
TYPE_SERVICE_DATA_32BIT_UUID = BLEGAPType.TYPE_SERVICE_DATA_32BIT_UUID.value
TYPE_SERVICE_DATA_128BIT_UUID = BLEGAPType.TYPE_SERVICE_DATA_128BIT_UUID.value
TYPE_TX_POWER_LEVEL = BLEGAPType.TYPE_TX_POWER_LEVEL.value

bytes_ = bytes


@lru_cache(maxsize=256)
def _uint64_bytes_as_uuid(uint64_bytes: bytes_) -> str:
    """Convert an integer to a UUID str."""
    int_value = int.from_bytes(uint64_bytes, "little")
    hex = "%032x" % int_value
    return f"{hex[:8]}-{hex[8:12]}-{hex[12:16]}-{hex[16:20]}-{hex[20:]}"


@lru_cache(maxsize=256)
def _uint16_bytes_as_uuid(uuid16_bytes: bytes_) -> str:
    """Convert a 16-bit UUID to a UUID str."""
    uuid_int = int.from_bytes(uuid16_bytes, "little")
    return f"0000{uuid_int:04x}-{BLE_UUID}"


@lru_cache(maxsize=256)
def _uint32_bytes_as_uuid(uuid32_bytes: bytes_) -> str:
    """Convert a 32-bit UUID to a UUID str."""
    uuid_int = int.from_bytes(uuid32_bytes, "little")
    return f"{uuid_int:08x}-{BLE_UUID}"


@lru_cache(maxsize=256)
def _manufacturer_id_bytes_to_int(manufacturer_id_bytes: bytes_) -> int:
    """Convert manufacturer ID bytes to an int."""
    return int.from_bytes(manufacturer_id_bytes, "little")


def parse_advertisement_data(
    data: Iterable[bytes],
) -> BLEGAPAdvertisement:
    """Parse advertisement data."""
    manufacturer_data: Dict[int, bytes] = {}
    service_data: Dict[str, bytes] = {}
    service_uuids: List[str] = []
    local_name: str | None = None
    tx_power: int | None = None

    for gap_data in data:
        for gap_type_num, gap_value in _decode_advertisement_data(gap_data):
            if gap_type_num == TYPE_SHORT_LOCAL_NAME and not local_name:
                local_name = gap_value.decode("utf-8", "replace")
            elif gap_type_num == TYPE_COMPLETE_LOCAL_NAME:
                local_name = gap_value.decode("utf-8", "replace")
            elif gap_type_num == TYPE_MANUFACTURER_SPECIFIC_DATA:
                manufacturer_data[
                    _manufacturer_id_bytes_to_int(gap_value[2:])
                ] = gap_value[2:]
            elif gap_type_num in {
                TYPE_16BIT_SERVICE_UUID_COMPLETE,
                TYPE_16BIT_SERVICE_UUID_MORE_AVAILABLE,
            }:
                service_uuids.append(_uint16_bytes_as_uuid(gap_value[:2]))
            elif gap_type_num in {
                TYPE_128BIT_SERVICE_UUID_MORE_AVAILABLE,
                TYPE_128BIT_SERVICE_UUID_COMPLETE,
            }:
                service_uuids.append(_uint64_bytes_as_uuid(gap_value[:16]))
            elif gap_type_num == TYPE_SERVICE_DATA:
                service_data[_uint16_bytes_as_uuid(gap_value[:2])] = gap_value[2:]
            elif gap_type_num == TYPE_SERVICE_DATA_32BIT_UUID:
                service_data[_uint32_bytes_as_uuid(gap_value[:4])] = gap_value[4:]
            elif gap_type_num == TYPE_SERVICE_DATA_128BIT_UUID:
                service_data[_uint64_bytes_as_uuid(gap_value[:16])] = gap_value[16:]
            elif gap_type_num == TYPE_TX_POWER_LEVEL:
                tx_power = int.from_bytes(gap_value, "little", signed=True)

    return BLEGAPAdvertisement(
        local_name,
        service_uuids,
        service_data,
        manufacturer_data,
        tx_power,
    )
