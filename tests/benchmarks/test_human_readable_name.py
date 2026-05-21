from pytest_codspeed import BenchmarkFixture

from bluetooth_data_tools import human_readable_name

# Realistic scan shape: a known peripheral with a name plus a fresh
# adv carrying only a local_name, both keyed by a hex BLE address.
_NAME = "Living Room Sensor"
_LOCAL_NAME = "RZSS"
_ADDRESS = "AA:BB:CC:DD:EE:FF"


def test_human_readable_name_with_name(benchmark: BenchmarkFixture) -> None:
    benchmark(lambda: human_readable_name(_NAME, _LOCAL_NAME, _ADDRESS))


def test_human_readable_name_local_only(benchmark: BenchmarkFixture) -> None:
    benchmark(lambda: human_readable_name(None, _LOCAL_NAME, _ADDRESS))
