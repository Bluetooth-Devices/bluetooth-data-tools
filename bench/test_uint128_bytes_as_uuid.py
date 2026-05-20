from bluetooth_data_tools.gap import _uint128_bytes_as_uuid

_UUID_BYTES = bytes(range(16))


def test_uint128_bytes_as_uuid_cached(benchmark):
    _uint128_bytes_as_uuid(_UUID_BYTES)
    benchmark(lambda: _uint128_bytes_as_uuid(_UUID_BYTES))


def test_uint128_bytes_as_uuid_miss(benchmark):
    cache_clear = _uint128_bytes_as_uuid.cache_clear

    def run():
        cache_clear()
        _uint128_bytes_as_uuid(_UUID_BYTES)

    benchmark(run)
