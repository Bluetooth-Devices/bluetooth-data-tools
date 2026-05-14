from bluetooth_data_tools import (
    human_readable_name,
    int_to_bluetooth_address,
    mac_to_int,
    manufacturer_data_to_raw,
    newest_manufacturer_data,
    short_address,
)


def test_int_to_bluetooth_address():
    assert int_to_bluetooth_address(0) == "00:00:00:00:00:00"
    assert int_to_bluetooth_address(1) == "00:00:00:00:00:01"
    assert int_to_bluetooth_address(0xFFFFFFFFFFFF) == "FF:FF:FF:FF:FF:FF"
    assert int_to_bluetooth_address(0x123456789ABC) == "12:34:56:78:9A:BC"
    assert int_to_bluetooth_address(0xDEF012345678) == "DE:F0:12:34:56:78"


def test_newest_manufacturer_data():
    data = {1: b"\x01\x02\x03\x04"}
    assert newest_manufacturer_data(data) == b"\x01\x02\x03\x04"
    assert newest_manufacturer_data({}) is None


def test_newest_manufacturer_data_id_zero():
    """Manufacturer ID 0 is assigned (Ericsson Technology Licensing) and must
    not be dropped by an accidental truthiness check on the dict key."""
    assert newest_manufacturer_data({0: b"\x01\x02\x03\x04"}) == b"\x01\x02\x03\x04"
    assert newest_manufacturer_data({1: b"first", 0: b"newest"}) == b"newest"


def test_manufacturer_data_to_raw():
    assert (
        manufacturer_data_to_raw(1, b"\x01\x02\x03\x04")
        == b"\x00\x00\x01\x00\x01\x02\x03\x04"
    )


def test_short_address():
    assert short_address("AA:BB:CC:DD:EE:FF") == "EEFF"


def test_human_readable_name():
    assert (
        human_readable_name("My Device", "Your Device", "AA:BB:CC:DD:EE:FF")
        == "My Device (EEFF)"
    )


def test_mac_to_int():
    assert mac_to_int("00:00:00:00:00:00") == 0
    assert mac_to_int("00:00:00:00:00:01") == 1
    assert mac_to_int("FF:FF:FF:FF:FF:FF") == 0xFFFFFFFFFFFF
