from bluetooth_data_tools.utils import _mac_to_int, mac_to_int


def test_mac_to_int_uncached(benchmark):
    benchmark(lambda: _mac_to_int("AA:BB:CC:DD:EE:FF"))


def test_mac_to_int_cached(benchmark):
    benchmark(lambda: mac_to_int("AA:BB:CC:DD:EE:FF"))
