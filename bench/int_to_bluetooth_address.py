import timeit

from bluetooth_data_tools.utils import (
    _int_to_bluetooth_address,
    int_to_bluetooth_address,
)


def uncached_parse() -> None:
    _int_to_bluetooth_address(0)


def cached_parse() -> None:
    int_to_bluetooth_address(0)


count = 10000000
time = timeit.Timer(uncached_parse).timeit(count)
print(f"Parsing {count} bluetooth addresses took {time} seconds (uncached)")
time = timeit.Timer(cached_parse).timeit(count)
print(f"Parsing {count} bluetooth addresses took {time} seconds (cached)")
