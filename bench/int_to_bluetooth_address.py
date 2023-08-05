import timeit

from bluetooth_data_tools.utils import _int_to_bluetooth_address


def parse_adv() -> None:
    _int_to_bluetooth_address(0)


count = 10000000
time = timeit.Timer(parse_adv).timeit(count)
print(f"Parsing {count} bluetooth addresses took {time} seconds")
