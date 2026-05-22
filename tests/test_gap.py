import base64
import logging

import pytest

from bluetooth_data_tools import (
    parse_advertisement_data,
    parse_advertisement_data_bytes,
    parse_advertisement_data_tuple,
)


def test_parse_advertisement_data_Prodigio_D83567A4F5A5_bytes():
    data = b"".join(
        [
            base64.b64decode("AgoEFglQcm9kaWdpb19EODM1NjdBNEY1QTU="),
            base64.b64decode("AgEGEQYbxdWlAgCqneMRKvIQGaoGCf8CJUQJgAcAAg=="),
        ]
    )

    (local_name, service_uuids, service_data, manufacturer_data, tx_power) = (
        parse_advertisement_data_bytes(data)
    )

    assert local_name == "Prodigio_D83567A4F5A5"
    assert service_uuids == ["06aa1910-f22a-11e3-9daa-0002a5d5c51b"]
    assert service_data == {}
    assert manufacturer_data == {9474: b"D\t\x80\x07\x00\x02"}
    assert tx_power == 4


def test_parse_advertisement_data_Prodigio_D83567A4F5A5():
    data = [
        base64.b64decode("AgoEFglQcm9kaWdpb19EODM1NjdBNEY1QTU="),
        base64.b64decode("AgEGEQYbxdWlAgCqneMRKvIQGaoGCf8CJUQJgAcAAg=="),
    ]

    adv = parse_advertisement_data(data)

    assert adv.local_name == "Prodigio_D83567A4F5A5"
    assert adv.service_uuids == ["06aa1910-f22a-11e3-9daa-0002a5d5c51b"]
    assert adv.service_data == {}
    assert adv.manufacturer_data == {9474: b"D\t\x80\x07\x00\x02"}
    assert adv.tx_power == 4


def test_parse_advertisement_data_unknown_apple_device():
    data = [
        base64.b64decode("AgEaAgoFCv9MABAFChx3+Vs="),
    ]

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == []
    assert adv.service_data == {}
    assert adv.manufacturer_data == {76: b"\x10\x05\n\x1cw\xf9["}
    assert adv.tx_power == 5


def test_parse_advertisement_data_empty():
    data = [
        b"\x00",
    ]

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == []
    assert adv.service_data == {}
    assert adv.manufacturer_data == {}
    assert adv.tx_power is None


def test_parse_advertisement_data_flags_only():
    data = [
        b"\x01\x01\x06",
    ]

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == []
    assert adv.service_data == {}
    assert adv.manufacturer_data == {}
    assert adv.tx_power is None


def test_parse_advertisement_data_ignores_invalid():
    data = [
        b"\x02\x01\x1a\x02\n\x05\n\xffL\x00\x10\x05\n\x1cw\xf9[\x02\x01",
    ]

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == []
    assert adv.service_data == {}
    assert adv.manufacturer_data == {76: b"\x10\x05\n\x1cw\xf9["}
    assert adv.tx_power == 5


def test_parse_advertisement_data_trailing_minimum_ad_struct(caplog):
    # Manufacturer-data struct (5 bytes) followed by a trailing minimum-AD
    # struct [length=1][type=0x09] (2 bytes). The loop must enter the trailing
    # struct rather than silently skip it; preceding data must still parse.
    data = [b"\x04\xff\x4c\x00\x10\x01\x09"]

    with caplog.at_level(logging.DEBUG, logger="bluetooth_data_tools.gap"):
        adv = parse_advertisement_data(data)

    assert adv.manufacturer_data == {76: b"\x10"}
    assert any("Invalid BLE GAP AD structure" in r.message for r in caplog.records)


def test_parse_advertisement_data_ignores_zero_type():
    data = [
        b"\x02\x01\x1a\x02\n\x05\n\xffL\x00\x10\x05\n\x1cw\xf9[\x02\x00",
    ]

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == []
    assert adv.service_data == {}
    assert adv.manufacturer_data == {76: b"\x10\x05\n\x1cw\xf9["}
    assert adv.tx_power == 5


def test_parse_advertisement_data_unknown_fd3d():
    data = [
        base64.b64decode("AgEGD/9pCWBV+Tw02tgAEDEAAA=="),
        base64.b64decode("BhY9/WcAZA=="),
    ]

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == []
    assert adv.service_data == {"0000fd3d-0000-1000-8000-00805f9b34fb": b"g\x00d"}
    assert adv.manufacturer_data == {2409: b"`U\xf9<4\xda\xd8\x00\x101\x00\x00"}
    assert adv.tx_power is None


def test_parse_advertisement_data_moat():
    data = [
        base64.b64decode("AgEGAwMAEBUWABDfeeOmErMVUHBjVGIcb7kL//8="),
        base64.b64decode("AgoAAwMAIAsWAFDfeeOmErO5CwgJTW9hdF9TMg=="),
    ]

    adv = parse_advertisement_data(data)

    assert adv.local_name == "Moat_S2"
    assert adv.service_uuids == [
        "00001000-0000-1000-8000-00805f9b34fb",
        "00002000-0000-1000-8000-00805f9b34fb",
    ]
    assert adv.service_data == {
        "00001000-0000-1000-8000-00805f9b34fb": b"\xdfy\xe3\xa6\x12\xb3\x15PpcTb"
        b"\x1co\xb9\x0b\xff\xff",
        "00005000-0000-1000-8000-00805f9b34fb": b"\xdfy\xe3\xa6\x12\xb3\xb9\x0b",
    }
    assert adv.manufacturer_data == {}
    assert adv.tx_power == 0


def test_parse_advertisement_data_unknown_apple_215():
    data = [
        base64.b64decode("AgEGGv9MAAIV1Ubfl0dXR+++CT4ty90MdxU2zcm1"),
    ]

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == []
    assert adv.service_data == {}
    assert adv.manufacturer_data == {
        76: b"\x02\x15\xd5F\xdf\x97GWG\xef\xbe\t>-\xcb\xdd\x0cw\x156\xcd\xc9\xb5"
    }
    assert adv.tx_power is None


def test_parse_advertisement_data_oral_b_toothbrush():
    data = [
        base64.b64decode("AgEGDv/cAAYyawNSAAEECQAEAwIN/g=="),
        base64.b64decode("EglPcmFsLUIgVG9vdGhicnVzaAUSEABQAAIKAA=="),
    ]

    adv = parse_advertisement_data(data)

    assert adv.local_name == "Oral-B Toothbrush"
    assert adv.service_uuids == ["0000fe0d-0000-1000-8000-00805f9b34fb"]
    assert adv.service_data == {}
    assert adv.manufacturer_data == {220: b"\x062k\x03R\x00\x01\x04\t\x00\x04"}
    assert adv.tx_power == 0

    assert parse_advertisement_data_tuple(tuple(data)) == (
        "Oral-B Toothbrush",
        ["0000fe0d-0000-1000-8000-00805f9b34fb"],
        {},
        {220: b"\x062k\x03R\x00\x01\x04\t\x00\x04"},
        0,
    )


def test_parse_advertisement_short_local_name():
    data = [
        base64.b64decode("AgEGFv9MAAYxAOTEm+77PgUADQABAmMRIGUECE5hbg=="),
    ]

    adv = parse_advertisement_data(data)

    assert adv.local_name == "Nan"
    assert adv.service_uuids == []
    assert adv.service_data == {}
    assert adv.manufacturer_data == {
        76: b"\x061\x00\xe4\xc4\x9b\xee\xfb>\x05\x00\r\x00\x01\x02c\x11 e"
    }
    assert adv.tx_power is None


def test_parse_advertisement_complete_overrides_short_local_name():
    # SHORT (0x08) appears first then COMPLETE (0x09) follows; COMPLETE must
    # overwrite the short form so callers always see the longer name when
    # both are present.
    data = [b"\x04\x08Bar\x04\x09Foo"]

    adv = parse_advertisement_data(data)

    assert adv.local_name == "Foo"


def test_parse_advertisement_short_local_name_ignored_after_complete():
    # COMPLETE (0x09) appears first then SHORT (0x08) follows; the SHORT
    # branch is gated on ``local_name is None``, so the previously-set
    # complete name must survive.
    data = [b"\x04\x09Foo\x04\x08Bar"]

    adv = parse_advertisement_data(data)

    assert adv.local_name == "Foo"


def test_parse_advertisement_data_32bit_service_data():
    data = [
        b"\x07\x20\x1a\x02\n\x05\n\xff",
    ]

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == []
    assert adv.service_data == {"050a021a-0000-1000-8000-00805f9b34fb": b"\n\xff"}
    assert adv.manufacturer_data == {}
    assert adv.tx_power is None


def test_parse_advertisement_data_128bit_service_data():
    data = [
        b"\x12\x21\x1a\x02\n\x05\n\xff\x062k\x03R\x00\x01\x04\t\x00\x04",
    ]

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == []
    assert adv.service_data == {"00090401-0052-036b-3206-ff0a050a021a": b"\x04"}
    assert adv.manufacturer_data == {}
    assert adv.tx_power is None


def test_parse_advertisement_data_32bit_and_128bit_service_data():
    data = [
        b"\x07\x20\x1a\x02\n\x05\n\xff",
        b"\x12\x21\x1a\x02\n\x05\n\xff\x062k\x03R\x00\x01\x04\t\x00\x04",
    ]

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == []
    assert adv.service_data == {
        "00090401-0052-036b-3206-ff0a050a021a": b"\x04",
        "050a021a-0000-1000-8000-00805f9b34fb": b"\n\xff",
    }
    assert adv.manufacturer_data == {}
    assert adv.tx_power is None


def test_parse_advertisement_data_128bit_and_32bit_service_data():
    data = [
        b"\x12\x21\x1a\x02\n\x05\n\xff\x062k\x03R\x00\x01\x04\t\x00\x04",
        b"\x07\x20\x1a\x02\n\x05\n\xff",
    ]

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == []
    assert adv.service_data == {
        "00090401-0052-036b-3206-ff0a050a021a": b"\x04",
        "050a021a-0000-1000-8000-00805f9b34fb": b"\n\xff",
    }
    assert adv.manufacturer_data == {}
    assert adv.tx_power is None


def test_parse_advertisement_data_128bit_service_data_tuple():
    data = (b"\x12\x21\x1a\x02\n\x05\n\xff\x062k\x03R\x00\x01\x04\t\x00\x04",)

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == []
    assert adv.service_data == {"00090401-0052-036b-3206-ff0a050a021a": b"\x04"}
    assert adv.manufacturer_data == {}
    assert adv.tx_power is None


def test_parse_advertisement_data_zero_padded():
    data = [
        bytes.fromhex(
            "02.01.06.0E.FF.69.09.FA.62.0F.CF.2D.F2.DA.0F"
            ".00.22.04.00.09.16.3D.FD.63.C0.56.00.22.04".replace(".", "")
        )
    ]

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == []
    assert adv.service_data == {
        "0000fd3d-0000-1000-8000-00805f9b34fb": b'c\xc0V\x00"\x04'
    }
    assert adv.manufacturer_data == {2409: b'\xfab\x0f\xcf-\xf2\xda\x0f\x00"\x04'}
    assert adv.tx_power is None


def test_parse_adv_data():
    data = [
        bytes.fromhex(
            "02.01.06.05.02.E0.FF.E7.FE.0B.FF.65.0B.88.A0"
            ".C8.47.8C.EA.D1.C1.0C.09.4D.32.5F.42.31.41.38"
            ".53.31.30.50".replace(".", "")
        )
    ]
    adv = parse_advertisement_data(data)

    assert adv.local_name == "M2_B1A8S10P"
    assert adv.service_uuids == [
        "0000ffe0-0000-1000-8000-00805f9b34fb",
        "0000fee7-0000-1000-8000-00805f9b34fb",
    ]
    assert adv.service_data == {}
    assert adv.manufacturer_data == {2917: b"\x88\xa0\xc8G\x8c\xea\xd1\xc1"}
    assert adv.tx_power is None


def test_parse_multiple_16bit_uuids():
    """Test parsing advertisement data with 3 16-bit service UUIDs."""
    # Build advertisement data with 3 16-bit UUIDs
    # Length: 7 (1 byte type + 6 bytes for 3 UUIDs)
    # Type: 0x02 (16-bit service UUID more available)
    # UUIDs in little-endian: 0x1234 -> 3412, 0x5678 -> 7856, 0x9ABC -> BC9A
    data = [bytes.fromhex("070234127856BC9A")]
    adv = parse_advertisement_data(data)

    assert adv.service_uuids == [
        "00001234-0000-1000-8000-00805f9b34fb",
        "00005678-0000-1000-8000-00805f9b34fb",
        "00009abc-0000-1000-8000-00805f9b34fb",
    ]
    assert adv.local_name is None
    assert adv.service_data == {}
    assert adv.manufacturer_data == {}
    assert adv.tx_power is None


def test_parse_multiple_32bit_uuids():
    """Test parsing advertisement data with 2 32-bit service UUIDs."""
    # Build advertisement data with 2 32-bit UUIDs
    # Length: 9 (1 byte type + 8 bytes for 2 UUIDs)
    # Type: 0x04 (32-bit service UUID more available)
    # UUIDs in little-endian: 0x12345678 -> 78563412, 0x9ABCDEF0 -> F0DEBC9A
    data = [bytes.fromhex("090478563412F0DEBC9A")]
    adv = parse_advertisement_data(data)

    assert adv.service_uuids == [
        "12345678-0000-1000-8000-00805f9b34fb",
        "9abcdef0-0000-1000-8000-00805f9b34fb",
    ]
    assert adv.local_name is None
    assert adv.service_data == {}
    assert adv.manufacturer_data == {}
    assert adv.tx_power is None


def test_parse_mixed_16bit_32bit_uuids():
    """Test parsing advertisement data with 16-bit UUID followed by 32-bit UUID."""
    # Build advertisement data with:
    # - One 16-bit UUID: 0x1234
    # - Two 32-bit UUIDs: 0x56789ABC, 0xDEF01234
    data = [
        bytes.fromhex(
            "03023412"  # Length=3, Type=0x02, UUID=0x1234 (little-endian)
            "090478563412F0DEBC9A"  # Length=9, Type=0x04, UUIDs in little-endian
        )
    ]
    adv = parse_advertisement_data(data)

    assert adv.service_uuids == [
        "00001234-0000-1000-8000-00805f9b34fb",  # 16-bit
        "12345678-0000-1000-8000-00805f9b34fb",  # 32-bit
        "9abcdef0-0000-1000-8000-00805f9b34fb",  # 32-bit
    ]
    assert adv.local_name is None
    assert adv.service_data == {}
    assert adv.manufacturer_data == {}
    assert adv.tx_power is None


def test_parse_mixed_16bit_128bit_uuids():
    """Test parsing advertisement data with 16-bit UUID followed by 128-bit UUID."""
    # Build advertisement data with:
    # - One 16-bit UUID: 0x1234
    # - One 128-bit UUID: 550e8400-e29b-41d4-a716-446655440000
    # Note: 128-bit UUIDs are stored in reverse byte order in BLE
    data = [
        bytes.fromhex(
            "03023412"  # Length=3, Type=0x02, UUID=0x1234 (little-endian)
            "110600004455664416a7d4419be200840e55"  # Length=17, Type=0x06, 128-bit UUID (reversed)
        )
    ]
    adv = parse_advertisement_data(data)

    assert adv.service_uuids == [
        "00001234-0000-1000-8000-00805f9b34fb",  # 16-bit
        "550e8400-e29b-41d4-a716-446655440000",  # 128-bit
    ]
    assert adv.local_name is None
    assert adv.service_data == {}
    assert adv.manufacturer_data == {}
    assert adv.tx_power is None


def test_parse_advertisement_data_zero_padded_scan_included():
    data = [
        b"\x02\x01\x06\t\xffY\x00\xfe\x024\x9e\xa6\xba\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11\x07\x1b\xc5\xd5\xa5\x02\x00\xb8"
        b'\x9f\xe6\x11M"\x00\r\xa2\xcb\x06\x16\x00\rH\x10\x00\x00\x00\x00\x00\x00\x00'
    ]

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == ["cba20d00-224d-11e6-9fb8-0002a5d5c51b"]
    assert adv.service_data == {"00000d00-0000-1000-8000-00805f9b34fb": b"H\x10\x00"}
    assert adv.manufacturer_data == {89: b"\xfe\x024\x9e\xa6\xba"}
    assert adv.tx_power is None


def test_parse_advertisement_data_recovers_from_corrupt_data():
    data = [
        b"\x03\x03\x9f\xfe\x17\x16\x9f\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x06\xf8"
    ]

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == ["0000fe9f-0000-1000-8000-00805f9b34fb"]
    assert adv.service_data == {
        "0000fe9f-0000-1000-8000-00805f9b34fb": b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    }
    assert adv.manufacturer_data == {}
    assert adv.tx_power is None


def test_parse_advertisement_data_recovers_from_corrupt_data_2():
    data = [
        b"\x1a\xff\xc3\x03_\xef5B\xb0I\x0f\xbb\x00&\x01\x00m*"
        b"\xb2c\xd8\xb0\x02\n\x00\x00\xf2\x02\x01\x06 "
    ]

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == []
    assert adv.service_data == {}
    assert adv.manufacturer_data == {
        963: b"_\xef5B\xb0I\x0f\xbb\x00&\x01\x00m*\xb2c\xd8\xb0\x02\n\x00\x00\xf2"
    }
    assert adv.tx_power is None


def test_parse_advertisement_data_recovers_from_corrupt_data_3():
    data = [
        b"\x03\x03\x9f\xfe\x17\x16\x9f\xfe\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x06 "
    ]

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == ["0000fe9f-0000-1000-8000-00805f9b34fb"]
    assert adv.service_data == {
        "0000fe9f-0000-1000-8000-00805f9b34fb": b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    }
    assert adv.manufacturer_data == {}
    assert adv.tx_power is None


def test_parse_advertisement_data_recovers_from_corrupt_data_43():
    data = [
        b"\x1a\xff\xc3\x03_\xef5B\xb3I\x0f\xbb\x00&\x01\x01m*"
        b"\xb2c\xd8.\x02\n\x00\x00\xf2\x02\x01\xc6\xf8"
    ]

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == []
    assert adv.service_data == {}
    assert adv.manufacturer_data == {
        963: b"_\xef5B\xb3I\x0f\xbb\x00&\x01\x01m*\xb2c\xd8.\x02\n\x00\x00\xf2"
    }
    assert adv.tx_power is None


def test_name_parser():
    """Test parsing name from https://github.com/esphome/issues/issues/4838."""

    data = (
        b"\t\tPineTime\002\001\006\021\007\236\312\334$\016\345\251(340\223\363\243\265\001\000@n",
    )

    adv = parse_advertisement_data(data)

    assert adv.local_name == "PineTime"
    assert adv.service_uuids == ["01b5a3f3-9330-3433-28a9-e50e24dcca9e"]
    assert adv.service_data == {}
    assert adv.manufacturer_data == {}
    assert adv.tx_power is None

    assert parse_advertisement_data_tuple(tuple(data)) == (
        "PineTime",
        ["01b5a3f3-9330-3433-28a9-e50e24dcca9e"],
        {},
        {},
        None,
    )


def test_invalid_gap_num():
    """Test skip invalid gap type."""

    data = (
        b"\t\x00PineTime\002\001\006\021\007\236\312\334$\016\345\251(340\223\363\243\265\001\000@n",
    )

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == ["01b5a3f3-9330-3433-28a9-e50e24dcca9e"]
    assert adv.service_data == {}
    assert adv.manufacturer_data == {}
    assert adv.tx_power is None

    assert parse_advertisement_data_tuple(tuple(data)) == (
        None,
        ["01b5a3f3-9330-3433-28a9-e50e24dcca9e"],
        {},
        {},
        None,
    )


def test_out_of_bounds_length():
    """Test out of bound length."""

    data = (
        b"\xff\x00PineTime\002\001\006\021\007\236\312\334$\016\345\251(340\223\363\243\265\001\000@n",
    )

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == []
    assert adv.service_data == {}
    assert adv.manufacturer_data == {}
    assert adv.tx_power is None

    assert parse_advertisement_data_tuple(tuple(data)) == (
        None,
        [],
        {},
        {},
        None,
    )


def test_invalid_ad_debug_log_renders_without_error(caplog):
    """Malformed AD must produce a renderable debug log (regression: format-string mismatch)."""
    # length=5 (claims 4 payload bytes after the type byte) but only 2 follow.
    # Unique payload so the lru_cache doesn't return a previous result.
    data = b"\x05\x09\xab\xcd"
    with caplog.at_level("DEBUG", logger="bluetooth_data_tools.gap"):
        adv = parse_advertisement_data((data,))
    assert adv.local_name is None
    # Render every captured record — a format-string mismatch raises here.
    messages = [r.getMessage() for r in caplog.records]
    assert any("Invalid BLE GAP AD structure" in m for m in messages)


def test_out_of_bounds_length_by_one():
    """Test out of bound length by one."""

    data = (b"\x01\x08",)

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == []
    assert adv.service_data == {}
    assert adv.manufacturer_data == {}
    assert adv.tx_power is None

    assert parse_advertisement_data_tuple(tuple(data)) == (
        None,
        [],
        {},
        {},
        None,
    )


def test_manufacturer_data_short_by_one():
    """Test short manufacturer data."""

    data = (b"\x02\xff\x01",)

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == []
    assert adv.service_data == {}
    assert adv.manufacturer_data == {}
    assert adv.tx_power is None

    assert parse_advertisement_data_tuple(tuple(data)) == (
        None,
        [],
        {},
        {},
        None,
    )


def test_manufacturer_data_short_by_two():
    """Test short manufacturer data."""

    data = (b"\x02\xff\x01\x01",)

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == []
    assert adv.service_data == {}
    assert adv.manufacturer_data == {}
    assert adv.tx_power is None

    assert parse_advertisement_data_tuple(tuple(data)) == (
        None,
        [],
        {},
        {},
        None,
    )


def test_manufacturer_data_short_by_three():
    """Test manufacturer data with minimum size (company ID only, no payload).

    This is now valid after fixing issue #179 - manufacturer data with just
    a company ID and empty payload is accepted, consistent with service data.
    """

    data = (b"\x03\xff\x01\x01",)

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == []
    assert adv.service_data == {}
    assert adv.manufacturer_data == {257: b""}
    assert adv.tx_power is None

    assert parse_advertisement_data_tuple(tuple(data)) == (
        None,
        [],
        {},
        {257: b""},
        None,
    )


def test_manufacturer_data_short_by_four():
    """Test short manufacturer data.

    Manufacturer data claims length of 4 but only has 3 bytes available
    (type + company ID, no payload bytes when 1 payload byte is claimed).
    """

    data = (b"\x04\xff\x01\x01",)

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == []
    assert adv.service_data == {}
    assert adv.manufacturer_data == {}
    assert adv.tx_power is None

    assert parse_advertisement_data_tuple(tuple(data)) == (
        None,
        [],
        {},
        {},
        None,
    )


def test_manufacturer_data_short_by_five():
    """Test short manufacturer data."""

    data = (b"\x05\xff\x01\x01\x01",)

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == []
    assert adv.service_data == {}
    assert adv.manufacturer_data == {}
    assert adv.tx_power is None

    assert parse_advertisement_data_tuple(tuple(data)) == (
        None,
        [],
        {},
        {},
        None,
    )


def test_manufacturer_data_single_byte():
    """Test single byte manufacturer data."""

    data = (b"\x04\xff\x01\x01\x01",)

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == []
    assert adv.service_data == {}
    assert adv.manufacturer_data == {257: b"\x01"}
    assert adv.tx_power is None

    assert parse_advertisement_data_tuple(tuple(data)) == (
        None,
        [],
        {},
        {257: b"\x01"},
        None,
    )


def test_service_data_short():
    """Test short service data."""

    data = (b"\x02\x16\x01",)

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == []
    assert adv.service_data == {}
    assert adv.manufacturer_data == {}
    assert adv.tx_power is None

    assert parse_advertisement_data_tuple(tuple(data)) == (
        None,
        [],
        {},
        {},
        None,
    )


def test_32bit_uuid_short():
    """Test short 32bit uuid data."""

    data = (b"\x02 \x01",)

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == []
    assert adv.service_data == {}
    assert adv.manufacturer_data == {}
    assert adv.tx_power is None

    assert parse_advertisement_data_tuple(tuple(data)) == (
        None,
        [],
        {},
        {},
        None,
    )


def test_128bit_uuid_short():
    """Test short 128bit uuid data."""

    data = (b"\x02!\x01",)

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == []
    assert adv.service_data == {}
    assert adv.manufacturer_data == {}
    assert adv.tx_power is None

    assert parse_advertisement_data_tuple(tuple(data)) == (
        None,
        [],
        {},
        {},
        None,
    )


def test_zero_padded_end():
    """Test name with zero padded end."""

    data = (b"\x02\x08a\x00",)

    adv = parse_advertisement_data(data)

    assert adv.local_name == "a"
    assert adv.service_uuids == []
    assert adv.service_data == {}
    assert adv.manufacturer_data == {}
    assert adv.tx_power is None

    assert parse_advertisement_data_tuple(tuple(data)) == (
        "a",
        [],
        {},
        {},
        None,
    )


def test_zero_padded_out_of_bounds_length():
    """Test zero padded out of bound length."""

    data = (
        b"\x00\xff\x00PineTime\002\001\006\021\007\236\312\334$\016\345\251(340\223\363\243\265\001\000@n",
    )

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == []
    assert adv.service_data == {}
    assert adv.manufacturer_data == {}
    assert adv.tx_power is None

    assert parse_advertisement_data_tuple(
        tuple(
            data,
        )
    ) == (
        None,
        [],
        {},
        {},
        None,
    )


def test_data_shorter_than_length() -> None:
    """Test data shorter than length."""

    for len in range(0, 30):
        data = bytes((len,)) + b"!\x01"

        adv = parse_advertisement_data((data,))

        assert adv.local_name is None
        assert adv.service_uuids == []
        assert adv.service_data == {}
        assert adv.manufacturer_data == {}
        assert adv.tx_power is None

        assert parse_advertisement_data_tuple((data,)) == (
            None,
            [],
            {},
            {},
            None,
        )


@pytest.mark.parametrize(
    "data",
    [
        (b"\x02 a\xc4|\x04@*'\x9c\xa5C\r\xa1\xe6\x1e\xe7\x8f\xa57D\xe6$\x03",),
        (
            b"\xe8\x9d\x83\x8b\x96\x85\x07U\x19$&\x1c\x91\x80\xba\x04Z",
            b'"EU\xcb\x11\xeb\xdc\xd4)\xc9\x1b\x8c\xfe\x1e\xd7\xca\x98\xfe\xcd%\xf6>\xbb\xe3\xbc\xfc5',
            b"(\x86\x18\xe9m>\x89\xa7\xe1=\x9fE\x0f\xbcE\xb2<",
        ),
        (
            b"\xf4\x9e\x0f!\x93n\xae\x1e\x89\xc2\xb4\x97\x98\xdc~\x9a\xb3\x06\x7f\x11",
            b"\x89\xc2\x07\xff\xe7QEG&;\x06\xab\xebN\xf5\xc4g\xfe",
            b"\xeb\x852\x0b,KB",
        ),
        (
            b'\xcbu\xa5\xe4\xa1\xdd`c\x88\xa9\xe2\xaah\xe5"%X\x87\xf0',
            b'\xac;\x8f\xc43!\xb0?"\xb8\n<',
            b"\x10nyT\xed\x96\x07\x9a",
        ),
        (
            b"\r\xd6'\xder\xfc@T\xb3Q\x12EH\x9e\xe9\xf8x\xe3\xcc\ti\xfb",
            b"\xfe@\x89",
            b"Gt\xc3_\xf9\x8e\xdd#",
        ),
        (
            b'\x17b\x02c\xbe%"\x06\xfe\x05c4\x04\x97\x03)|\xd0\xf4\xeb~\xb1gI',
            b"r\xc0\x9a>^o\xcb\xdb\xc2r\xca\x1a'VL\xac\xd7\x8e\xa7\xeb\xc2:\xe2_\x96\xe31r",
            b"\\^\xe6\x96]%\x17\x02\xa5\xdcAE\x92\xb2\x1c\x1a\xd4Y\x07\xddZ\xebC\x12B\xb6\xcb\x8a",
        ),
        (
            b"\x1b\x87c\xb7\x12nK\xf3_\xb4\x18)x<\xe2\x05\xc8\xdb\xf8\x1b\xf7 \xe6\x99\xe3Z\xd1C\x88\xda\x98",
            b"\xbb\xbe@,\xa6\xdcj*\x85u\xe3\xc4",
            b"w\xb7\xeb\xb0",
        ),
        (
            b"\x88\x83\x7fN\xd0E\xa6\xc5(h\xcd\xe7\x80\\\xf0\xe6n:\x10K\x02\x92",
            b"\xc5\xe6`a\xf7\xf5 \x1eV\xd6]8$\xf0\xf0",
            b"\x01rS\xf1\xe2ht\xd6\x8f\xc6\x0e\xd0~",
        ),
        (
            b"\x10\xa6\xc4}\xb6\xc9n\x00",
            b"\xa8\xd8#'@\xde\x9a\xf6;&\x88\x0f\xc1m\xe5v\xa3\x17O\x8b\x92\x94\\\x91\x8b\xee\xa1\xed",
            b'\xccA\x9c\x01;\xd1\xe8e\xeb\xf3\x8b\xa1\xd6\xe5P]\xc7"_@\x10\x1e\x8b\x90o\r\xd9',
        ),
    ],
)
def test_negative_splice_pos_does_not_crash(data: tuple[bytes, bytes, bytes]) -> None:
    """Test data that would cause a negative splice position.

    All of the data here will result in a negative splice position
    when attempting to parse the advertisement data. This is a
    regression test to ensure that the parser does not crash
    when it encounters this data.

    A negative splice position is caused by the parser
    attempting to splice the data at a position that is
    greater than the length of the data. This can happen
    when the data is malformed or when the parser is
    attempting to parse data that is not in the expected
    format. The parser should be able to handle this
    gracefully and return an empty advertisement object
    without crashing.
    """

    adv = parse_advertisement_data(data)

    assert adv.local_name is None
    assert adv.service_uuids == []
    assert adv.service_data == {}
    assert adv.manufacturer_data == {}
    assert adv.tx_power is None

    assert parse_advertisement_data_tuple(
        tuple(
            data,
        )
    ) == (
        None,
        [],
        {},
        {},
        None,
    )


def test_parse_advertisement_with_empty_service_data():
    """Test parsing advertisement with empty service data payload (issue #179).

    This tests the case where service data contains only a UUID with no payload bytes.
    The parser should accept this as valid empty service data and continue parsing
    subsequent advertisement structures.
    """
    # Data from issue #179:
    # 02 01 06 - Flags (type 0x01, data 0x06)
    # 03 16 0a 18 - Service Data (type 0x16, UUID 0x180a, empty payload)
    # 03 03 fa ff - Complete 16-bit Service UUIDs (type 0x03, UUID 0xfffa)
    # 07 ff 00 01 50 90 40 a2 - Manufacturer Data (type 0xff, company 0x0100, data)
    # 10 09 4b 54... - Complete Local Name (type 0x09, "KT12200-B-00100")
    data = bytes.fromhex(
        "02010603160a180303faff07ff0001509040a210094b5431323230302d422d3030313030"
    )

    adv = parse_advertisement_data((data,))

    assert adv.local_name == "KT12200-B-00100"
    assert adv.service_uuids == ["0000fffa-0000-1000-8000-00805f9b34fb"]
    assert adv.service_data == {"0000180a-0000-1000-8000-00805f9b34fb": b""}
    assert adv.manufacturer_data == {256: b"\x50\x90\x40\xa2"}
    assert adv.tx_power is None


def test_parse_advertisement_data_multiple_128bit_uuids():
    """Two 128-bit UUIDs packed into a single AD struct must both be returned.

    Per Core Spec Vol 3 Part C §11, the Complete/Incomplete List of 128-bit
    Service UUIDs AD types carry a list (length = 1 + 16N), not a single UUID.
    Larger packets (scan response / extended advertising) can carry more than one.
    """
    uuid1 = bytes.fromhex("00112233445566778899aabbccddeeff")
    uuid2 = bytes.fromhex("0f1e2d3c4b5a69788796a5b4c3d2e1f0")
    # Length = 0x21 (33 = 1 type byte + 32 UUID bytes), type = 0x07 (complete list)
    data = b"\x21\x07" + uuid1 + uuid2

    adv = parse_advertisement_data((data,))

    assert adv.local_name is None
    assert adv.service_uuids == [
        # bytes are stored little-endian in BLE — reverse for canonical form
        "ffeeddcc-bbaa-9988-7766-554433221100",
        "f0e1d2c3-b4a5-9687-7869-5a4b3c2d1e0f",
    ]
    assert adv.service_data == {}
    assert adv.manufacturer_data == {}
    assert adv.tx_power is None


def test_parse_advertisement_data_128bit_uuid_malformed_length():
    """Malformed 128-bit UUID payloads (length not 1 + 16N) must be skipped.

    Previously the parser passed the truncated/excess bytes straight to the
    UUID formatter, producing bogus UUID strings (all zeros for short, a
    64-hex-char garbage string for double-length).
    """
    # Length=0x0a (10 = 1 type + 9 bytes), type=0x07 — only 9 bytes of "UUID"
    short = b"\x0a\x07" + bytes(9)
    adv = parse_advertisement_data((short,))
    assert adv.service_uuids == []

    # Length=0x12 (18 = 1 type + 17 bytes), type=0x07 — one valid UUID plus
    # a 1-byte tail that must be ignored, not folded into a second UUID.
    one_and_a_half = (
        b"\x12\x07" + bytes.fromhex("00112233445566778899aabbccddeeff") + b"\x42"
    )
    adv = parse_advertisement_data((one_and_a_half,))
    assert adv.service_uuids == ["ffeeddcc-bbaa-9988-7766-554433221100"]


def test_parse_advertisement_data_tx_power_single_byte():
    """Per BLE Core Spec Vol 3 Part C §11, TX Power Level is exactly 1 signed octet."""
    # length=2 (1 type byte + 1 data byte), type=0x0a, tx_power=-50 (0xCE)
    data = (b"\x02\x0a\xce",)
    adv = parse_advertisement_data(data)
    assert adv.tx_power == -50


def test_parse_advertisement_data_tx_power_multibyte_rejected():
    """Malformed multi-byte TX Power must be skipped, not folded into a multi-byte signed int.

    The previous behaviour read the entire (variable-length) payload as a
    little-endian signed integer, producing values like -32768 for what
    should be invalid input.
    """
    # length=3 (1 type byte + 2 data bytes), type=0x0a, payload=\x00\x80.
    # Old parser: from_bytes(b"\x00\x80", little, signed=True) = -32768.
    # Spec-compliant parser: skip entirely, tx_power is None.
    data = (b"\x03\x0a\x00\x80",)
    adv = parse_advertisement_data(data)
    assert adv.tx_power is None


def test_parse_advertisement_data_16bit_uuid_malformed_length():
    """16-bit UUID list with a trailing odd byte must drop the remainder, not
    emit a UUID built from a 1-byte slice.

    Mirrors the 128-bit malformed-length protection (PR #226) for the
    16-bit list branch.
    """
    # length=0x06 (6 = 1 type + 5 bytes), type=0x03 — two valid UUIDs plus a
    # 1-byte tail that must not be folded into a third UUID.
    payload = b"\x06\x03\xaa\xbb\xcc\xdd\xee"
    adv = parse_advertisement_data((payload,))
    assert adv.service_uuids == [
        "0000bbaa-0000-1000-8000-00805f9b34fb",
        "0000ddcc-0000-1000-8000-00805f9b34fb",
    ]

    # length=0x04 (4 = 1 type + 3 bytes), type=0x02 — one UUID + 1 trailing
    # byte; the trailing byte must not be folded into a second UUID.
    one_and_a_half = b"\x04\x02\x11\x22\x33"
    adv = parse_advertisement_data((one_and_a_half,))
    assert adv.service_uuids == ["00002211-0000-1000-8000-00805f9b34fb"]


def test_parse_advertisement_data_32bit_uuid_malformed_length():
    """32-bit UUID list with a tail < 4 bytes must drop the remainder.

    Mirrors the 128-bit malformed-length protection (PR #226) for the
    32-bit list branch.
    """
    # length=0x08 (8 = 1 type + 7 bytes), type=0x05 — one valid 32-bit UUID
    # plus a 3-byte tail.
    payload = b"\x08\x05\x11\x22\x33\x44\xaa\xbb\xcc"
    adv = parse_advertisement_data((payload,))
    assert adv.service_uuids == ["44332211-0000-1000-8000-00805f9b34fb"]

    # length=0x06 (6 = 1 type + 5 bytes), type=0x04 — one UUID + 1 trailing
    # byte; the trailing byte must not be folded into a second UUID.
    one_and_a_quarter = b"\x06\x04\xde\xad\xbe\xef\x99"
    adv = parse_advertisement_data((one_and_a_quarter,))
    assert adv.service_uuids == ["efbeadde-0000-1000-8000-00805f9b34fb"]


def test_parse_advertisement_data_32bit_uuid_high_bit_set():
    """32-bit UUIDs with bit 31 set must decode as the unsigned value.

    Guards the signed-shift UB fix: ``gap_data[i + 3] << 24`` on an
    ``unsigned char`` promotes to (signed) ``int`` in C, so values >= 0x80
    in the top byte would be undefined behavior under Cython without the
    intermediate ``unsigned int`` staging. The decoded UUID must reflect
    the full unsigned 32-bit value, not a sign-extended negative.
    """
    # length=0x09 (9 = 1 type + 8 bytes), type=0x05 — two 32-bit UUIDs
    # in little-endian: 0xFF112233 -> 33 22 11 FF, 0x80000001 -> 01 00 00 80.
    payload = b"\x09\x05\x33\x22\x11\xff\x01\x00\x00\x80"
    adv = parse_advertisement_data((payload,))
    assert adv.service_uuids == [
        "ff112233-0000-1000-8000-00805f9b34fb",
        "80000001-0000-1000-8000-00805f9b34fb",
    ]


def test_parse_advertisement_data_32bit_service_data_high_bit_set():
    """32-bit service-data UUID with bit 31 set must key on the unsigned value.

    Same UB guard as the list branch, applied to the
    ``TYPE_SERVICE_DATA`` 32-bit decode.
    """
    # length=0x07 (7 = 1 type + 4 UUID bytes + 2 data bytes), type=0x20
    # UUID little-endian: 0xFF112233 -> 33 22 11 FF; data: AA BB.
    payload = b"\x07\x20\x33\x22\x11\xff\xaa\xbb"
    adv = parse_advertisement_data((payload,))
    assert adv.service_data == {
        "ff112233-0000-1000-8000-00805f9b34fb": b"\xaa\xbb",
    }


def test_parse_advertisement_data_multiple_manufacturer_entries():
    """Two manufacturer-specific-data AD structs in one packet must both
    survive into the resulting dict, keyed by company ID.

    BLE Core Spec Vol 3 Part C §11 permits the Manufacturer Specific Data
    AD type to appear more than once in a single advertisement.
    """
    # First MSD: company 0x004C (Apple), payload \x01\x02
    # Second MSD: company 0x0059 (Nordic), payload \x03\x04\x05
    payload = b"\x05\xff\x4c\x00\x01\x02" + b"\x06\xff\x59\x00\x03\x04\x05"
    adv = parse_advertisement_data((payload,))
    assert adv.manufacturer_data == {
        0x004C: b"\x01\x02",
        0x0059: b"\x03\x04\x05",
    }


def test_parse_advertisement_data_multi_chunk_tuple_matches_bytes():
    """A multi-chunk tuple input must produce the same result as the joined bytes.

    This pins the parse_advertisement_data tuple fast-path that caches on the
    tuple itself rather than on the joined bytes.
    """
    chunks = (
        b"\x02\x01\x06\x03\x03\x12\x18",
        b"\x10\tLOOKin_98F33163\x03\x19\xc1\x03",
    )
    joined = b"".join(chunks)

    from_tuple = parse_advertisement_data(chunks)
    from_bytes = parse_advertisement_data([joined])

    assert from_tuple.local_name == from_bytes.local_name == "LOOKin_98F33163"
    assert from_tuple.service_uuids == from_bytes.service_uuids
    assert from_tuple.service_data == from_bytes.service_data
    assert from_tuple.manufacturer_data == from_bytes.manufacturer_data
    assert from_tuple.tx_power == from_bytes.tx_power


def test_parse_advertisement_data_single_element_tuple_unwraps_to_bytes_cache():
    """A 1-element tuple skips the join and uses the bytes-keyed cache directly."""
    payload = b"\x02\x01\x06\x05\tRZSS"
    from_tuple = parse_advertisement_data((payload,))
    from_list = parse_advertisement_data([payload])
    assert from_tuple.local_name == from_list.local_name == "RZSS"


def test_parse_advertisement_data_tuple_miss_falls_through_bytes_cache():
    """A tuple-cache miss must consult the bytes-keyed cache before paying for
    a full parse, so identical content arriving via a fresh tuple identity
    still benefits from a previous bytes-form call.
    """
    payload = b"\x02\x01\x06\x05\tRZSS"

    # Prime the bytes cache only.
    parse_advertisement_data_tuple.cache_clear()
    expected = parse_advertisement_data_bytes(payload)

    # Tuple cache is empty, so this call must miss the tuple cache and resolve
    # via the bytes cache.
    assert parse_advertisement_data_tuple((payload,)) == expected
    # Multi-chunk path: same content, fresh tuple identity, still bytes-cached.
    assert parse_advertisement_data_tuple((b"", payload)) == expected
