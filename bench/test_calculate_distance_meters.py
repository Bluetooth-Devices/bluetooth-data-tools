from bluetooth_data_tools import calculate_distance_meters

_CLOSE_POWER = -4
_CLOSE_RSSI = -3

_FAR_POWER = -59
_FAR_RSSI = -60

_ZERO_POWER = 59
_ZERO_RSSI = 0


def test_calculate_distance_meters_close(benchmark):
    benchmark(lambda: calculate_distance_meters(_CLOSE_POWER, _CLOSE_RSSI))


def test_calculate_distance_meters_far(benchmark):
    benchmark(lambda: calculate_distance_meters(_FAR_POWER, _FAR_RSSI))


def test_calculate_distance_meters_zero(benchmark):
    benchmark(lambda: calculate_distance_meters(_ZERO_POWER, _ZERO_RSSI))
