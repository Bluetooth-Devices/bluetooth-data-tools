from pytest_codspeed import BenchmarkFixture

from bluetooth_data_tools import monotonic_time_coarse


def test_monotonic_time_coarse(benchmark: BenchmarkFixture) -> None:
    benchmark(monotonic_time_coarse)
