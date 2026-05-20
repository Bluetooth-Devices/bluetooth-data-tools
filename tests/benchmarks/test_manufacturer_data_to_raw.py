from pytest_codspeed import BenchmarkFixture

from bluetooth_data_tools.utils import manufacturer_data_to_raw


def test_manufacturer_data_to_raw_short(benchmark: BenchmarkFixture) -> None:
    benchmark(lambda: manufacturer_data_to_raw(0x004C, b"\x01\x02\x03\x04"))


def test_manufacturer_data_to_raw_long(benchmark: BenchmarkFixture) -> None:
    payload = bytes(range(64))
    benchmark(lambda: manufacturer_data_to_raw(0xFFFF, payload))
