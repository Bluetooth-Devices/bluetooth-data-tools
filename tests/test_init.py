from bluetooth_data_tools import (
    address_to_bytes,
    human_readable_name,
    manufacturer_data_to_raw,
    newest_manufacturer_data,
    short_address,
)


def test_newest_manufacturer_data():
    data = {1: b"\x01\x02\x03\x04"}
    assert newest_manufacturer_data(data) == b"\x01\x02\x03\x04"
    assert newest_manufacturer_data({}) is None


def test_address_to_bytes():
    assert address_to_bytes("00:00:00:00:00:00") == b"\x00\x00\x00\x00"
    assert address_to_bytes("a-c-b") == b"\x00\x00\x00\x00"


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
