from pytest_codspeed import BenchmarkFixture

from bluetooth_data_tools import short_address


def test_short_address_colon(benchmark: BenchmarkFixture) -> None:
    benchmark(lambda: short_address("AA:BB:CC:DD:EE:FF"))


def test_short_address_dash(benchmark: BenchmarkFixture) -> None:
    benchmark(lambda: short_address("AA-BB-CC-DD-EE-FF"))
