"""Benchmark for the 128-bit UUID bytes-to-string conversion.

The cached entry point ``_cached_uint128_bytes_as_uuid`` short-circuits the
work for repeat UUIDs, but every cache miss pays the full bytes-to-str
round-trip. This benchmark covers both the cached hit path and the underlying
uncached body so the miss-path optimization can be measured without parser
overhead drowning the signal.
"""

from pytest_codspeed import BenchmarkFixture

from bluetooth_data_tools.gap import _uint128_bytes_as_uuid

_UUID_BYTES = bytes(range(16))


def test_uint128_bytes_as_uuid_cached(benchmark: BenchmarkFixture) -> None:
    _uint128_bytes_as_uuid(_UUID_BYTES)
    benchmark(lambda: _uint128_bytes_as_uuid(_UUID_BYTES))


def test_uint128_bytes_as_uuid_miss(benchmark: BenchmarkFixture) -> None:
    cache_clear = _uint128_bytes_as_uuid.cache_clear

    def run() -> None:
        cache_clear()
        _uint128_bytes_as_uuid(_UUID_BYTES)

    benchmark(run)
