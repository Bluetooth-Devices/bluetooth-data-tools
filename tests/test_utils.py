import pytest

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


def test_mac_to_int_hyphen_separator():
    """Windows-style hyphen-separated addresses are accepted, matching short_address."""
    assert mac_to_int("AA-BB-CC-DD-EE-FF") == 0xAABBCCDDEEFF
    assert mac_to_int("00-00-00-00-00-00") == 0


def test_mac_to_int_lowercase():
    assert mac_to_int("aa:bb:cc:dd:ee:ff") == 0xAABBCCDDEEFF


def test_mac_to_int_unseparated():
    """Unseparated 12-char form is accepted."""
    assert mac_to_int("AABBCCDDEEFF") == 0xAABBCCDDEEFF
    assert mac_to_int("0123456789ab") == 0x0123456789AB


@pytest.mark.parametrize(
    "value",
    [0, 1, 0xAB, 0xDEADBEEF, 0xFFFFFFFFFFFF, 0x123456789ABC],
)
def test_mac_to_int_round_trip(value):
    """mac_to_int is the inverse of int_to_bluetooth_address."""
    assert mac_to_int(int_to_bluetooth_address(value)) == value


@pytest.mark.parametrize(
    "bad",
    [
        "not-a-mac",
        "AA:BB:CC:DD:EE:GG",
        "AA/BB/CC/DD/EE/FF",
        "",
    ],
)
def test_mac_to_int_invalid(bad):
    """Malformed input raises ValueError (matches int() fallback semantics)."""
    with pytest.raises(ValueError):
        mac_to_int(bad)


@pytest.mark.parametrize(
    "bad",
    [
        "AABBCCDDEEFFA1234",  # 17 hex chars, no separators
        "AABB-CCDDEEFF-123",  # 17 chars, separators in the wrong positions
        "AA:BB:CC:DD:EE:F",  # 16 chars (too short by one)
        "AA:BB:CC:DD:EE:FFF",  # 18 chars (too long by one)
        "AABBCCDDEE_F",  # 12 chars with a non-hex underscore
        "AABBCCDDEE F",  # 12 chars with embedded whitespace
    ],
)
def test_mac_to_int_invalid_parity(bad):
    """Inputs the native parser rejects must also be rejected by the
    pure-Python fallback, so both build modes behave identically.

    The old fallback (strip separators, then int(..., 16)) was looser than
    the native C parser: it ignored separator position, accepted a fully
    unseparated 17-char hex string as a 68-bit value, and let int() honor
    underscore digit separators / surrounding whitespace.
    """
    with pytest.raises(ValueError):
        mac_to_int(bad)
