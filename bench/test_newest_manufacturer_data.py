from bluetooth_data_tools.utils import newest_manufacturer_data


def test_newest_manufacturer_data_single(benchmark):
    data = {0x004C: b"\x10\x05\x03\x18\x42\xC4\xFF\xAA"}
    benchmark(lambda: newest_manufacturer_data(data))


def test_newest_manufacturer_data_multi(benchmark):
    data = {
        0x004C: b"\x10\x05\x03\x18\x42\xC4\xFF\xAA",
        0x00FF: b"\x01\x02\x03\x04",
    }
    benchmark(lambda: newest_manufacturer_data(data))
