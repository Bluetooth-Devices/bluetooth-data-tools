from pytest_codspeed import BenchmarkFixture

from bluetooth_data_tools import calculate_distance_meters

# Close: ratio < 1, takes the pow(ratio, 10) branch.
_CLOSE_POWER = -4
_CLOSE_RSSI = -3

# Far: ratio > 1, takes the 0.89976 * pow(ratio, 7.7095) + 0.111 branch.
_FAR_POWER = -59
_FAR_RSSI = -60

# Zero rssi short circuits to None before any pow call.
_ZERO_POWER = 59
_ZERO_RSSI = 0


def test_calculate_distance_meters_close(benchmark: BenchmarkFixture) -> None:
    benchmark(lambda: calculate_distance_meters(_CLOSE_POWER, _CLOSE_RSSI))


def test_calculate_distance_meters_far(benchmark: BenchmarkFixture) -> None:
    benchmark(lambda: calculate_distance_meters(_FAR_POWER, _FAR_RSSI))


def test_calculate_distance_meters_zero(benchmark: BenchmarkFixture) -> None:
    benchmark(lambda: calculate_distance_meters(_ZERO_POWER, _ZERO_RSSI))
