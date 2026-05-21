from bluetooth_data_tools import human_readable_name

_NAME = "Living Room Sensor"
_LOCAL_NAME = "RZSS"
_ADDRESS = "AA:BB:CC:DD:EE:FF"


def test_human_readable_name_with_name(benchmark):
    benchmark(lambda: human_readable_name(_NAME, _LOCAL_NAME, _ADDRESS))


def test_human_readable_name_local_only(benchmark):
    benchmark(lambda: human_readable_name(None, _LOCAL_NAME, _ADDRESS))
