#  cythonize -X language_level=3 -a -i  src/bluetooth_data_tools/gap.py
"""pytest-benchmark mirror of tests/benchmarks/test_parse_gap_uuid_lists.

Kept in sync with the codspeed suite so CI step summaries surface the same
multi-entry UUID list scenarios that the safe_end hoist (PR #253) targets.
"""

from bluetooth_data_tools.gap import _uncached_parse_advertisement_bytes

_FLAGS = b"\x02\x01\x06"
_LOCAL_NAME = b"\x07\tDevice"
_UUIDS_16 = b"\x0f\x03\x12\x18\x0a\x18\x0d\x18\x0f\x18\x05\x18\x09\x18\x02\x18"
_UUIDS_32 = b"\x0d\x05\x12\x18\x00\x00\x0a\x18\x00\x00\x0d\x18\x00\x00"
_UUIDS_128 = b"\x21\x07" + bytes(range(16)) + bytes(range(16, 32))

ADV_16BIT_LIST = _FLAGS + _UUIDS_16 + _LOCAL_NAME
ADV_32BIT_LIST = _FLAGS + _UUIDS_32 + _LOCAL_NAME
ADV_128BIT_LIST = _FLAGS + _UUIDS_128 + _LOCAL_NAME
ADV_MIXED_LIST = _FLAGS + _UUIDS_16 + _UUIDS_32 + _UUIDS_128 + _LOCAL_NAME


def test_parse_advertisement_16bit_uuid_list(benchmark):
    benchmark(lambda: _uncached_parse_advertisement_bytes(ADV_16BIT_LIST))


def test_parse_advertisement_32bit_uuid_list(benchmark):
    benchmark(lambda: _uncached_parse_advertisement_bytes(ADV_32BIT_LIST))


def test_parse_advertisement_128bit_uuid_list(benchmark):
    benchmark(lambda: _uncached_parse_advertisement_bytes(ADV_128BIT_LIST))


def test_parse_advertisement_mixed_uuid_lists(benchmark):
    benchmark(lambda: _uncached_parse_advertisement_bytes(ADV_MIXED_LIST))
