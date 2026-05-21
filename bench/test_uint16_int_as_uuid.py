from bluetooth_data_tools.gap import _uint16_int_as_uuid


def test_uint16_int_as_uuid_cached(benchmark):
    benchmark(lambda: _uint16_int_as_uuid(0x1234))
