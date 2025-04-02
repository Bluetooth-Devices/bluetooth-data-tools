import random

from bluetooth_data_tools.gap import _uncached_parse_advertisement_data


def test_gap_fuzzer() -> None:
    """Test random data does not crash."""
    for i in range(1000):
        adv = (
            bytes([random.randint(0, 255) for _ in range(random.randint(1, 31))]),
            bytes([random.randint(0, 255) for _ in range(random.randint(1, 31))]),
            bytes([random.randint(0, 255) for _ in range(random.randint(1, 31))]),
        )
        print([i, adv])
        _uncached_parse_advertisement_data(adv)
