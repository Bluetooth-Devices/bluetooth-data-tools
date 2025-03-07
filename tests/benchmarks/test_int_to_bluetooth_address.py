from pytest_codspeed import BenchmarkFixture

from bluetooth_data_tools.utils import (
    _int_to_bluetooth_address,
    int_to_bluetooth_address,
)


def test_parse_int_to_bluetooth_address_uncached(benchmark: BenchmarkFixture) -> None:
    benchmark(lambda: _int_to_bluetooth_address(0))


def test_parse_int_to_bluetooth_address_cached(benchmark: BenchmarkFixture) -> None:
    benchmark(lambda: int_to_bluetooth_address(0))
