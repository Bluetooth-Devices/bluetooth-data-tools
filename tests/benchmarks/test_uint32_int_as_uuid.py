from pytest_codspeed import BenchmarkFixture

from bluetooth_data_tools.gap import _uint32_int_as_uuid


def test_uint32_int_as_uuid_cached(benchmark: BenchmarkFixture) -> None:
    benchmark(lambda: _uint32_int_as_uuid(0x12345678))
