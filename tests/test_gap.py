import base64

from bluetooth_data_tools import (
    parse_advertisement_data,
    parse_advertisement_data_tuple,
)


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
    """Test short manufacturer data."""

    data = (b"\x03\xff\x01\x01",)

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
