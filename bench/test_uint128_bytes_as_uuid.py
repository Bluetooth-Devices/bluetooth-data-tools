from bluetooth_data_tools.gap import _uint128_bytes_as_uuid

_UUID_BYTES = bytes(range(16))


def test_uint128_bytes_as_uuid_cached(benchmark):
    benchmark(lambda: _uint128_bytes_as_uuid(_UUID_BYTES))


def test_uint128_bytes_as_uuid_uncached(benchmark):
    def run():
        _uint128_bytes_as_uuid.cache_clear()
        _uint128_bytes_as_uuid(_UUID_BYTES)

    benchmark(run)
