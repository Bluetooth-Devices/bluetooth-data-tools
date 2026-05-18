from bluetooth_data_tools.utils import (
    _short_address,
    short_address,
)


def test_short_address_uncached(benchmark):
    benchmark(lambda: _short_address("AA:BB:CC:DD:EE:FF"))


def test_short_address_cached(benchmark):
    benchmark(lambda: short_address("AA:BB:CC:DD:EE:FF"))


def test_short_address_unseparated_uncached(benchmark):
    benchmark(lambda: _short_address("AABBCCDDEEFF"))
