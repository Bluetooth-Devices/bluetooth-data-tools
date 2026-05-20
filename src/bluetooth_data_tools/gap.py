"""GATT Advertisement and Scan Response Data (GAP)."""

import logging
from collections.abc import Iterable
from enum import IntEnum
from functools import lru_cache
from typing import TYPE_CHECKING

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
        service_uuids: list[str],
        service_data: dict[str, bytes],
        manufacturer_data: dict[int, bytes],
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


# Signed-fold constants for the one-byte TX Power Level decode.
# A uint8 value at or above _INT8_SIGN_THRESHOLD is negative when interpreted
# as int8, and recovers its signed value via subtraction of _INT8_RANGE.
_INT8_SIGN_THRESHOLD = 128
_INT8_RANGE = 256

TYPE_SHORT_LOCAL_NAME = BLEGAPType.TYPE_SHORT_LOCAL_NAME.value
TYPE_COMPLETE_LOCAL_NAME = BLEGAPType.TYPE_COMPLETE_LOCAL_NAME.value
TYPE_MANUFACTURER_SPECIFIC_DATA = BLEGAPType.TYPE_MANUFACTURER_SPECIFIC_DATA.value
TYPE_16BIT_SERVICE_UUID_COMPLETE = BLEGAPType.TYPE_16BIT_SERVICE_UUID_COMPLETE.value
TYPE_16BIT_SERVICE_UUID_MORE_AVAILABLE = (
    BLEGAPType.TYPE_16BIT_SERVICE_UUID_MORE_AVAILABLE.value
)
TYPE_32BIT_SERVICE_UUID_COMPLETE = BLEGAPType.TYPE_32BIT_SERVICE_UUID_COMPLETE.value
TYPE_32BIT_SERVICE_UUID_MORE_AVAILABLE = (
    BLEGAPType.TYPE_32BIT_SERVICE_UUID_MORE_AVAILABLE.value
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

BLEGAPAdvertisementTupleType = tuple[
    str | None, list[str], dict[str, bytes], dict[int, bytes], int | None
]


@lru_cache(maxsize=256)
def _uint128_bytes_as_uuid(uint128_bytes: bytes_) -> str:
    """Convert 16 little-endian bytes to a canonical UUID str."""
    # bytes.hex() is a single C call; reversing the 16-byte slice yields the
    # big-endian hex form directly, skipping the int.from_bytes + format-spec
    # round-trip used previously (~40% faster on the cache-miss path).
    hex = uint128_bytes[::-1].hex()
    return f"{hex[:8]}-{hex[8:12]}-{hex[12:16]}-{hex[16:20]}-{hex[20:]}"


_cached_uint128_bytes_as_uuid = _uint128_bytes_as_uuid


@lru_cache(maxsize=256)
def _uint16_int_as_uuid(uuid16_int: int) -> str:
    """Convert a 16-bit UUID integer to a UUID str."""
    return f"0000{uuid16_int:04x}-{BLE_UUID}"


_cached_uint16_int_as_uuid = _uint16_int_as_uuid


@lru_cache(maxsize=256)
def _uint32_int_as_uuid(uuid32_int: int) -> str:
    """Convert a 32-bit UUID integer to a UUID str."""
    return f"{uuid32_int:08x}-{BLE_UUID}"


_cached_uint32_int_as_uuid = _uint32_int_as_uuid


_EMPTY_MANUFACTURER_DATA: dict[int, bytes] = {}
_EMPTY_SERVICE_DATA: dict[str, bytes] = {}
_EMPTY_SERVICE_UUIDS: list[str] = []


@lru_cache(maxsize=256)
def _parse_advertisement_data(
    data: bytes,
) -> BLEGAPAdvertisement:
    """Parse advertisement data and return a BLEGAPAdvertisement."""
    return _uncached_parse_advertisement_data(data)


_cached_parse_advertisement_data = _parse_advertisement_data


@lru_cache(maxsize=256)
def _parse_advertisement_data_from_tuple(
    data: tuple[bytes, ...],
) -> BLEGAPAdvertisement:
    """Parse a multi-chunk advertisement tuple, caching on the tuple itself.

    Hashing a tuple of bytes elements skips the per-call ``b"".join`` allocation
    on cache hits, which is the hot path when the same scan callback delivers
    the same (adv_data, scan_response_data) tuple repeatedly.
    """
    return _cached_parse_advertisement_data(b"".join(data))


_cached_parse_advertisement_data_from_tuple = _parse_advertisement_data_from_tuple


def parse_advertisement_data(
    data: Iterable[bytes],
) -> BLEGAPAdvertisement:
    """Parse advertisement data and return a BLEGAPAdvertisement."""
    if type(data) is tuple:
        if len(data) == 1:
            return _cached_parse_advertisement_data(data[0])
        return _cached_parse_advertisement_data_from_tuple(data)
    return _cached_parse_advertisement_data(b"".join(data))


def _uncached_parse_advertisement_data(data: bytes) -> BLEGAPAdvertisement:
    # Route BLEGAPAdvertisement-cache misses through the bytes-keyed cache
    # (symmetric with _uncached_parse_advertisement_tuple, see #261). Identical
    # payloads reaching this miss path skip the full parse when the bytes-tuple
    # cache already holds the result, and a true miss populates that cache so
    # subsequent parse_advertisement_data_bytes / parse_advertisement_data_tuple
    # calls on the same payload also win.
    return BLEGAPAdvertisement(*parse_advertisement_data_bytes(data))


def _uncached_parse_advertisement_tuple(
    data: tuple[bytes, ...],
) -> BLEGAPAdvertisementTupleType:
    # Route tuple-cache misses through the bytes-keyed cache so identical
    # content arriving via a fresh tuple identity still skips the full parse.
    # The outer lru_cache around parse_advertisement_data_tuple owns the
    # hit-path (C-level hash on the tuple, no join).
    if len(data) == 1:
        return parse_advertisement_data_bytes(data[0])
    return parse_advertisement_data_bytes(b"".join(data))


def _uncached_parse_advertisement_bytes(
    gap_bytes: bytes,
) -> BLEGAPAdvertisementTupleType:
    manufacturer_data = _EMPTY_MANUFACTURER_DATA
    service_data = _EMPTY_SERVICE_DATA
    service_uuids = _EMPTY_SERVICE_UUIDS
    local_name: str | None = None
    tx_power: int | None = None

    offset = 0
    total_length = len(gap_bytes)
    gap_data = gap_bytes
    # IMPORTANT: All data must be manually bounds checked
    # because the data is untrusted and can be malformed.
    while offset + 2 <= total_length:
        if not (length := gap_data[offset]):
            offset += 1  # Handle zero padding
            continue
        if not (gap_type_num := gap_data[offset + 1]):
            offset += 1 + length  # Skip empty type
            continue
        start = offset + 2
        end = start + length - 1
        offset += 1 + length
        if end > total_length or end - start <= 0:
            _LOGGER.debug(
                "Invalid BLE GAP AD structure at offset %s: %s (length=%s)",
                offset,
                gap_bytes,
                length,
            )
            continue
        if gap_type_num == TYPE_SHORT_LOCAL_NAME and local_name is None:
            local_name = gap_data[start:end].decode("utf-8", "replace")
        elif gap_type_num == TYPE_COMPLETE_LOCAL_NAME:
            local_name = gap_data[start:end].decode("utf-8", "replace")
        elif gap_type_num == TYPE_MANUFACTURER_SPECIFIC_DATA:
            splice_pos = start + 2
            if splice_pos > end:
                continue
            if manufacturer_data is _EMPTY_MANUFACTURER_DATA:
                manufacturer_data = {}
            manufacturer_data[gap_data[start] | (gap_data[start + 1] << 8)] = gap_data[
                splice_pos:end
            ]
        elif gap_type_num in {
            TYPE_16BIT_SERVICE_UUID_COMPLETE,
            TYPE_16BIT_SERVICE_UUID_MORE_AVAILABLE,
        }:
            if service_uuids is _EMPTY_SERVICE_UUIDS:
                service_uuids = []
            # Parse multiple 16-bit UUIDs (each is 2 little-endian bytes).
            # Decode inline to an int and look up by int key to skip the
            # per-iteration bytes-slice allocation.
            for i in range(start, end, 2):
                if i + 2 <= end:
                    service_uuids.append(
                        _cached_uint16_int_as_uuid(gap_data[i] | (gap_data[i + 1] << 8))
                    )
        elif gap_type_num in {
            TYPE_32BIT_SERVICE_UUID_COMPLETE,
            TYPE_32BIT_SERVICE_UUID_MORE_AVAILABLE,
        }:
            if service_uuids is _EMPTY_SERVICE_UUIDS:
                service_uuids = []
            # Parse multiple 32-bit UUIDs (each is 4 little-endian bytes).
            for i in range(start, end, 4):
                if i + 4 <= end:
                    # Assemble via uint local: in Cython the shift-by-24 of an
                    # unsigned char promotes to signed int and would yield a
                    # negative value when bit 31 is set; assigning to a
                    # cython.uint local recovers the unsigned 32-bit value.
                    uuid32_int = (
                        gap_data[i]
                        | (gap_data[i + 1] << 8)
                        | (gap_data[i + 2] << 16)
                        | (gap_data[i + 3] << 24)
                    )
                    service_uuids.append(_cached_uint32_int_as_uuid(uuid32_int))
        elif gap_type_num in {
            TYPE_128BIT_SERVICE_UUID_MORE_AVAILABLE,
            TYPE_128BIT_SERVICE_UUID_COMPLETE,
        }:
            if service_uuids is _EMPTY_SERVICE_UUIDS:
                service_uuids = []
            # Parse multiple 128-bit UUIDs (each is 16 bytes). The AD length
            # may not be a clean multiple of 16 for malformed input — skip
            # any trailing remainder rather than emitting a truncated UUID.
            for i in range(start, end, 16):
                if i + 16 <= end:
                    service_uuids.append(
                        _cached_uint128_bytes_as_uuid(gap_data[i : i + 16])
                    )
        elif gap_type_num == TYPE_SERVICE_DATA:
            splice_pos = start + 2
            if splice_pos > end:
                continue
            if service_data is _EMPTY_SERVICE_DATA:
                service_data = {}
            service_data[
                _cached_uint16_int_as_uuid(gap_data[start] | (gap_data[start + 1] << 8))
            ] = gap_data[splice_pos:end]
        elif gap_type_num == TYPE_SERVICE_DATA_32BIT_UUID:
            splice_pos = start + 4
            if splice_pos > end:
                continue
            if service_data is _EMPTY_SERVICE_DATA:
                service_data = {}
            uuid32_int = (
                gap_data[start]
                | (gap_data[start + 1] << 8)
                | (gap_data[start + 2] << 16)
                | (gap_data[start + 3] << 24)
            )
            service_data[_cached_uint32_int_as_uuid(uuid32_int)] = gap_data[
                splice_pos:end
            ]
        elif gap_type_num == TYPE_SERVICE_DATA_128BIT_UUID:
            splice_pos = start + 16
            if splice_pos > end:
                continue
            if service_data is _EMPTY_SERVICE_DATA:
                service_data = {}
            service_data[_cached_uint128_bytes_as_uuid(gap_data[start:splice_pos])] = (
                gap_data[splice_pos:end]
            )
        elif gap_type_num == TYPE_TX_POWER_LEVEL:
            # BLE Core Spec Vol 3 Part C §11: TX Power Level is exactly one
            # signed octet. Anything else is malformed — skip instead of
            # decoding the bytes as a wider little-endian signed integer.
            if end - start == 1:
                tx_power_byte = gap_data[start]
                tx_power = (
                    tx_power_byte - _INT8_RANGE
                    if tx_power_byte >= _INT8_SIGN_THRESHOLD
                    else tx_power_byte
                )

    return (local_name, service_uuids, service_data, manufacturer_data, tx_power)


if TYPE_CHECKING:

    @lru_cache(maxsize=1024)
    def parse_advertisement_data_bytes(
        gap_bytes: bytes,
    ) -> BLEGAPAdvertisementTupleType:
        """Parse a tuple of raw advertisement data and return a tuple of BLEGAPAdvertisementTupleType.

        The format of the tuple is:
        (local_name, service_uuids, service_data, manufacturer_data, tx_power)

        This is tightly coupled to bleak. If you are not using bleak
        it is recommended to use parse_advertisement_data instead.

        local_name: str | None
        service_uuids: list[str]
        service_data: dict[str, bytes]
        manufacturer_data: dict[int, bytes]
        tx_power: int | None
        """
        return _uncached_parse_advertisement_bytes(gap_bytes)

    @lru_cache(maxsize=256)
    def parse_advertisement_data_tuple(
        data: tuple[bytes, ...],
    ) -> BLEGAPAdvertisementTupleType:
        """Parse raw advertisement bytes and return a tuple of BLEGAPAdvertisementTupleType.

        The format of the tuple is:
        (local_name, service_uuids, service_data, manufacturer_data, tx_power)

        This is tightly coupled to bleak. If you are not using bleak
        it is recommended to use parse_advertisement_data instead.

        local_name: str | None
        service_uuids: list[str]
        service_data: dict[str, bytes]
        manufacturer_data: dict[int, bytes]
        tx_power: int | None
        """
        return _uncached_parse_advertisement_tuple(data)
else:
    parse_advertisement_data_bytes = lru_cache(maxsize=1024)(
        _uncached_parse_advertisement_bytes
    )
    parse_advertisement_data_tuple = lru_cache(maxsize=256)(
        _uncached_parse_advertisement_tuple
    )
