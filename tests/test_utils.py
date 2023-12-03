from bluetooth_data_tools import int_to_bluetooth_address


def test_int_to_bluetooth_address():
    assert int_to_bluetooth_address(0) == "00:00:00:00:00:00"
    assert int_to_bluetooth_address(1) == "00:00:00:00:00:01"
    assert int_to_bluetooth_address(0xFFFFFFFFFFFF) == "FF:FF:FF:FF:FF:FF"
    assert int_to_bluetooth_address(0x123456789ABC) == "12:34:56:78:9A:BC"
    assert int_to_bluetooth_address(0xDEF012345678) == "DE:F0:12:34:56:78"
