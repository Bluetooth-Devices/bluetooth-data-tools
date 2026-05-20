#  cythonize -X language_level=3 -a -i  src/bluetooth_data_tools/gap.py
"""Benchmarks for the 16/32/128-bit Service UUID list parse loops.

These exercise the multi-entry UUID list branches of
``_uncached_parse_advertisement_bytes`` so the per-iteration hoist of the
length bounds check (``safe_end = start + ((end - start) & ~(N-1))``) has
something to measure against. The wider real-world dataset in
``test_parse_gap_bytes`` is dominated by single-UUID payloads and 16-byte
slice allocations, both of which mask changes in the loop body.
"""

from pytest_codspeed import BenchmarkFixture

from bluetooth_data_tools.gap import _uncached_parse_advertisement_bytes

_FLAGS = b"\x02\x01\x06"
_LOCAL_NAME = b"\x07\tDevice"

# Complete 16-bit Service UUID list (type 0x03) carrying 7 UUIDs.
# length = 1 (type) + 14 (data) = 15.
_UUIDS_16 = b"\x0f\x03\x12\x18\x0a\x18\x0d\x18\x0f\x18\x05\x18\x09\x18\x02\x18"

# Complete 32-bit Service UUID list (type 0x05) carrying 3 UUIDs.
# length = 1 + 12 = 13.
_UUIDS_32 = b"\x0d\x05\x12\x18\x00\x00\x0a\x18\x00\x00\x0d\x18\x00\x00"

# Complete 128-bit Service UUID list (type 0x07) carrying 2 UUIDs.
# length = 1 + 32 = 33. Larger than a legacy 31-byte adv but valid for
# extended advertising payloads, which is exactly the path PR #253 targets.
_UUIDS_128 = b"\x21\x07" + bytes(range(16)) + bytes(range(16, 32))

ADV_16BIT_LIST = _FLAGS + _UUIDS_16 + _LOCAL_NAME
ADV_32BIT_LIST = _FLAGS + _UUIDS_32 + _LOCAL_NAME
ADV_128BIT_LIST = _FLAGS + _UUIDS_128 + _LOCAL_NAME
ADV_MIXED_LIST = _FLAGS + _UUIDS_16 + _UUIDS_32 + _UUIDS_128 + _LOCAL_NAME


def test_parse_advertisement_16bit_uuid_list(benchmark: BenchmarkFixture) -> None:
    benchmark(lambda: _uncached_parse_advertisement_bytes(ADV_16BIT_LIST))


def test_parse_advertisement_32bit_uuid_list(benchmark: BenchmarkFixture) -> None:
    benchmark(lambda: _uncached_parse_advertisement_bytes(ADV_32BIT_LIST))


def test_parse_advertisement_128bit_uuid_list(benchmark: BenchmarkFixture) -> None:
    benchmark(lambda: _uncached_parse_advertisement_bytes(ADV_128BIT_LIST))


def test_parse_advertisement_mixed_uuid_lists(benchmark: BenchmarkFixture) -> None:
    benchmark(lambda: _uncached_parse_advertisement_bytes(ADV_MIXED_LIST))
