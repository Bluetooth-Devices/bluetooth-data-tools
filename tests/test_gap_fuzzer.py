"""Fuzz coverage for the GAP parser.

The broad fuzz loop is intentionally unseeded so each CI run explores
fresh inputs — that is how regressions like the off-by-one fixed in
PR #221 surface. The seed used for a given run is printed (and can be
pinned with the ``FUZZ_SEED`` environment variable) so any failure is
reproducible locally.

Only the uncached parse path is fuzzed: ``parse_advertisement_data`` and
friends are thin LRU-cache wrappers around it, so re-running the same
bytes through them adds cost without coverage.
"""

import os
import random

from bluetooth_data_tools.gap import (
    _uncached_parse_advertisement_data,
    parse_advertisement_data,
    parse_advertisement_data_bytes,
)

_FUZZ_ITERATIONS = 1000

# AD type bytes used by the constructive fuzzer below. Kept as literals (rather
# than importing BLEGAPType) so the test pins the wire format independently of
# the production enum — a regression that renumbered a type would be caught.
_AD_TYPE_FLAGS = 0x01
_AD_TYPE_16BIT_UUID_COMPLETE = 0x03
_AD_TYPE_32BIT_UUID_COMPLETE = 0x05
_AD_TYPE_128BIT_UUID_COMPLETE = 0x07
_AD_TYPE_COMPLETE_LOCAL_NAME = 0x09
_AD_TYPE_TX_POWER = 0x0A
_AD_TYPE_APPEARANCE = 0x19  # unhandled by the parser -> must be ignored
_AD_TYPE_SERVICE_DATA_16BIT = 0x16
_AD_TYPE_MANUFACTURER_SPECIFIC = 0xFF

_BLE_BASE_UUID_TAIL = "0000-1000-8000-00805f9b34fb"


def _encode_ad(ad_type: int, payload: bytes) -> bytes:
    """Encode one AD structure as ``[length][type][payload...]``.

    ``length`` covers the type byte plus the payload, mirroring the on-the-wire
    GAP framing the parser consumes.
    """
    return bytes([1 + len(payload), ad_type]) + payload


def _expected_16bit_uuid(value: int) -> str:
    return f"0000{value:04x}-{_BLE_BASE_UUID_TAIL}"


def _expected_32bit_uuid(value: int) -> str:
    return f"{value:08x}-{_BLE_BASE_UUID_TAIL}"


def _expected_128bit_uuid(le_bytes: bytes) -> str:
    # The wire form is little-endian; the canonical string is big-endian hex.
    hex_ = le_bytes[::-1].hex()
    return f"{hex_[:8]}-{hex_[8:12]}-{hex_[12:16]}-{hex_[16:20]}-{hex_[20:]}"


def test_gap_fuzzer_random_bytes_do_not_crash() -> None:
    seed = int(os.environ.get("FUZZ_SEED", random.randrange(2**64)))
    print(f"fuzz seed: {seed:#x}")
    rng = random.Random(seed)
    for _ in range(_FUZZ_ITERATIONS):
        adv = (
            bytes(rng.randint(0, 255) for _ in range(rng.randint(1, 31))),
            bytes(rng.randint(0, 255) for _ in range(rng.randint(1, 31))),
            bytes(rng.randint(0, 255) for _ in range(rng.randint(1, 31))),
        )
        _uncached_parse_advertisement_data(b"".join(adv))


def test_gap_fuzzer_truncated_length_does_not_crash() -> None:
    """An AD struct that claims more bytes than remain must be rejected, not read."""
    rng = random.Random(0xB1EC0FFEE)
    for _ in range(200):
        # Claim a length that overruns the buffer, then provide a shorter body.
        body = bytes(rng.randint(0, 255) for _ in range(rng.randint(0, 5)))
        payload = bytes([100, rng.randint(1, 0xFF)]) + body
        adv = parse_advertisement_data((payload,))
        assert adv.local_name is None
        assert adv.manufacturer_data == {}
        assert adv.service_data == {}
        assert adv.service_uuids == []


def _build_random_advertisement(rng: random.Random) -> tuple[bytes, dict]:
    """Build a well-formed advertisement and the output it must parse back to.

    Returns ``(gap_bytes, expected)`` where ``expected`` mirrors the parser's
    accumulation rules: service UUID lists append in encounter order, the
    manufacturer-data and service-data dicts apply last-writer-wins per key, and
    local name / tx power keep the last well-formed value. ``FLAGS`` and an
    unhandled type are interleaved to assert they never corrupt the result.
    """
    chunks: list[bytes] = []
    expected: dict = {
        "local_name": None,
        "service_uuids": [],
        "service_data": {},
        "manufacturer_data": {},
        "tx_power": None,
    }

    for _ in range(rng.randint(0, 8)):
        kind = rng.choice(
            [
                "flags",
                "appearance",
                "name",
                "uuid16",
                "uuid32",
                "uuid128",
                "service_data16",
                "manufacturer",
                "tx_power",
            ]
        )
        if kind == "flags":
            # Common in real adverts and explicitly fast-skipped — no output.
            chunks.append(_encode_ad(_AD_TYPE_FLAGS, bytes([rng.randint(0, 0xFF)])))
        elif kind == "appearance":
            # A type the parser does not handle — must fall through to nothing.
            body = bytes(rng.randint(0, 255) for _ in range(rng.randint(1, 4)))
            chunks.append(_encode_ad(_AD_TYPE_APPEARANCE, body))
        elif kind == "name":
            # Restrict to printable ASCII so decode("utf-8") is unambiguous.
            name = bytes(rng.randint(0x20, 0x7E) for _ in range(rng.randint(1, 12)))
            chunks.append(_encode_ad(_AD_TYPE_COMPLETE_LOCAL_NAME, name))
            expected["local_name"] = name.decode("utf-8")
        elif kind == "uuid16":
            values = [rng.randint(0, 0xFFFF) for _ in range(rng.randint(1, 4))]
            payload = b"".join(v.to_bytes(2, "little") for v in values)
            chunks.append(_encode_ad(_AD_TYPE_16BIT_UUID_COMPLETE, payload))
            expected["service_uuids"].extend(_expected_16bit_uuid(v) for v in values)
        elif kind == "uuid32":
            values = [rng.randint(0, 0xFFFFFFFF) for _ in range(rng.randint(1, 3))]
            payload = b"".join(v.to_bytes(4, "little") for v in values)
            chunks.append(_encode_ad(_AD_TYPE_32BIT_UUID_COMPLETE, payload))
            expected["service_uuids"].extend(_expected_32bit_uuid(v) for v in values)
        elif kind == "uuid128":
            uuids = [
                bytes(rng.randint(0, 255) for _ in range(16))
                for _ in range(rng.randint(1, 2))
            ]
            chunks.append(_encode_ad(_AD_TYPE_128BIT_UUID_COMPLETE, b"".join(uuids)))
            expected["service_uuids"].extend(_expected_128bit_uuid(u) for u in uuids)
        elif kind == "service_data16":
            uuid16 = rng.randint(0, 0xFFFF)
            body = bytes(rng.randint(0, 255) for _ in range(rng.randint(0, 6)))
            payload = uuid16.to_bytes(2, "little") + body
            chunks.append(_encode_ad(_AD_TYPE_SERVICE_DATA_16BIT, payload))
            expected["service_data"][_expected_16bit_uuid(uuid16)] = body
        elif kind == "manufacturer":
            mid = rng.randint(0, 0xFFFF)
            body = bytes(rng.randint(0, 255) for _ in range(rng.randint(0, 6)))
            payload = mid.to_bytes(2, "little") + body
            chunks.append(_encode_ad(_AD_TYPE_MANUFACTURER_SPECIFIC, payload))
            expected["manufacturer_data"][mid] = body
        elif kind == "tx_power":
            raw = rng.randint(0, 0xFF)
            chunks.append(_encode_ad(_AD_TYPE_TX_POWER, bytes([raw])))
            expected["tx_power"] = raw - 256 if raw >= 128 else raw

    return b"".join(chunks), expected


def test_gap_fuzzer_constructive_round_trip() -> None:
    """Well-formed adverts must parse back to exactly the values that built them.

    The existing fuzzers only assert the parser does not crash; this one asserts
    output correctness. A regression in UUID byte order, service-data slicing,
    manufacturer-id decode, or tx-power sign-folding would change a parsed field
    away from the value the encoder put in, and fail here.
    """
    seed = int(os.environ.get("FUZZ_SEED", random.randrange(2**64)))
    print(f"constructive fuzz seed: {seed:#x}")
    rng = random.Random(seed)
    for _ in range(_FUZZ_ITERATIONS):
        gap_bytes, expected = _build_random_advertisement(rng)
        local_name, service_uuids, service_data, manufacturer_data, tx_power = (
            parse_advertisement_data_bytes(gap_bytes)
        )
        assert local_name == expected["local_name"]
        assert service_uuids == expected["service_uuids"]
        assert service_data == expected["service_data"]
        assert manufacturer_data == expected["manufacturer_data"]
        assert tx_power == expected["tx_power"]

        # The same payload split across a multi-chunk tuple must agree, since
        # the tuple path joins before delegating to the bytes parser.
        adv = parse_advertisement_data((gap_bytes,))
        assert adv.local_name == expected["local_name"]
        assert adv.service_uuids == expected["service_uuids"]
        assert adv.service_data == expected["service_data"]
        assert adv.manufacturer_data == expected["manufacturer_data"]
        assert adv.tx_power == expected["tx_power"]
