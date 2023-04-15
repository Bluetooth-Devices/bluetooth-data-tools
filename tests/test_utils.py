from bluetooth_data_tools import int_to_bluetooth_address


def test_int_to_bluetooth_address():
    assert int_to_bluetooth_address(0) == "00:00:00:00:00:00"
    assert int_to_bluetooth_address(1) == "00:00:00:00:00:01"
    assert int_to_bluetooth_address(0xFFFFFFFFFFFF) == "FF:FF:FF:FF:FF:FF"
