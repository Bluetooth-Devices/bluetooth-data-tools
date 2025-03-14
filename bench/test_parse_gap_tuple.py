from bluetooth_data_tools import parse_advertisement_data_tuple
from bluetooth_data_tools.gap import _uncached_parse_advertisement_data

#  cythonize -X language_level=3 -a -i  src/bluetooth_data_tools/gap.py

advs = (
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F33163\x03\x19\xc1\x03",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F330F3\x03\x19\xc1\x03",
    b"\x02\x01\x06\x0f\xffi\t`U\xf97\x95\x06.\x00\x00<\x00\x00",
    b"\x02\x01\x1a\x02\n\x07\n\xffL\x00\x10\x05\x1f\x1c8#\xe2",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F33208\x03\x19\xc1\x03",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F330B5\x03\x19\xc1\x03",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F330B4\x03\x19\xc1\x03",
    b"\x1b\xffu\x00B\x04\x01\x80n\xe0\x9d\x13\x99\x0f\xf3\xe2\x9d\x13\x99\x0f\xf2\x01\x00\x00\x00\x00\x00\x00",
    b"\x02\x01\x1a\x02\n\x06\x11\xffL\x00\x0f\x08\xd0\n\x7fnt\x00\x08\x0c\x10\x02#\x04",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F330C2\x03\x19\xc1\x03",
    b"\x02\x01\x1a\x0b\xffL\x00\t\x06\x03\x13\xc0\xa8k\xef",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F330B5\x03\x19\xc1\x03",
    b'\x02\x01\x04\x03\x03\x07\xfe\x10\xff\xa7\x05\x05\x10\x01\x00\x00\x00\x00\x00\x00\x02"\x00\xca\x03\x19\x00\x00\x02\n\x00',
    b'\x02\x01\x06\x16\xffL\x00\x061\x00\xcdnI\xa1\x91\xb2\x06\x007\x00\x04\x02\xcb\xd7,"\x04\x08LF0',
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F33208\x03\x19\xc1\x03",
    b"\x02\x01\x1a\x0b\xffL\x00\t\x06\x03\x13\xc0\xa8k\xef",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F330B5\x03\x19\xc1\x03",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F3320D\x03\x19\xc1\x03",
    b"\x02\x01\x06\x05\tRZSS",
    b"\x1b\xffu\x00B\x04\x01\x80f\x8c\xeaHM\x93;\x8e\xeaHM\x93:\x01\x00\x00\x00\x00\x00\x00",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F3320D\x03\x19\xc1\x03",
    b"\x1e\xff\x01ZR\x02\xb4\xe8B\xdb\xcf\xd4\x00\x97\x0c\x03\x01\x02\x03\x04\x05\x06\x07\x08\t\xa1\xa2\xa3\xa4\xa5\xa6",
    b"\x02\x01\x06\x05\tRZSS",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F331F5\x03\x19\xc1\x03",
    b"\x1b\xffu\x00B\x04\x01\x80f\x8c\xeaHM\x93;\x8e\xeaHM\x93:\x01\x00\x00\x00\x00\x00\x00",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F330C2\x03\x19\xc1\x03",
    b"\x02\x01\x06\t\xffY\x00\xd8.\xad\xcd\r\x85",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F330F3\x03\x19\xc1\x03",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F33231\x03\x19\xc1\x03",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F33208\x03\x19\xc1\x03",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F330B5\x03\x19\xc1\x03",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F330C2\x03\x19\xc1\x03",
    b"\x02\x01\x1a\x0b\xffL\x00\t\x06\x03+\xc0\xa8kZ",
    b"\x1b\xffu\x00B\x04\x01\x80n\xe0\x9d\x13\x99\x0f\xf3\xe2\x9d\x13\x99\x0f\xf2\x01\x00\x00\x00\x00\x00\x00",
    b"\x02\x01\x06\x05\tRZSS",
    b"\x1b\xffu\x00B\x04\x01\x80\xa0\xf8\x04.\xe1\x9f\x19\xfa\x04.\xe1\x9f\x18\x01\x00\x00\x00\x00\x00\x00",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F330B5\x03\x19\xc1\x03",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F330C2\x03\x19\xc1\x03",
    b"\x02\x01\x06\x05\tRZSS",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F33105\x03\x19\xc1\x03",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F330F3\x03\x19\xc1\x03",
    b"\x02\x01\x06\x16\xffL\x00\x061\x00\x8aO\xa3\xed?\x1e\x05\x00H\x04\x01\x02\xd8E\xf3\xc6\x04\x08Nan",
    b"\x02\x01\x1a\x02\n\x06\x0e\xffL\x00\x0f\x05\x90\x00QB\n\x10\x02#\x04",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F330B3\x03\x19\xc1\x03",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F33231\x03\x19\xc1\x03",
    b"\x02\x01\x06\t\xffY\x00\xc5-^\xabRv",
    b"\x02\x01\x06\x05\tRZSS",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F330B4\x03\x19\xc1\x03",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F330F3\x03\x19\xc1\x03",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F33208\x03\x19\xc1\x03",
    b"\x02\x01\x1a\x02\n\x06\x0e\xffL\x00\x0f\x05\x90\x00QB\n\x10\x02#\x04",
    b"\x02\x01\x06\x16\xffL\x00\x061\x00\x8aO\xa3\xed?\x1e\x05\x00H\x04\x01\x02\xd8E\xf3\xc6\x04\x08Nan",
    b"\x02\x01\x1a\x0b\xffL\x00\t\x06\x03\x89\xc0\xa8j(",
    b"\x02\x01\x06\t\xffY\x00\xc5-^\xabRv",
    b"\x02\x01\x06\x03\x02$\xfe\x04\xff\xd1\x01\x00",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F330B5\x03\x19\xc1\x03",
    b"\x02\x01\x06\x03\x02$\xfe\x04\xff\xd1\x01\x00",
    b"\x02\x01\x06\x0f\xffi\t`U\xf97\x95\x06.\x00\x00<\x00\x00",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F330C2\x03\x19\xc1\x03",
    b'\x02\x01\x02\x10\xff\xa7\x05\x05\x10\x01\x00\x00\x00\x00\x00\x00\x02"\x00\xca\x02\n\t\x03\x03\x07\xfe',
    b"\x02\x01\x06\x05\tRZSS",
    b"\x02\x01\x06\x0f\xffi\t`U\xf97\x95\x06.\x00\x00<\x00\x00",
    b"\x02\x01\x1a\x02\n\x0c\n\xffL\x00\x10\x05\x1b\x1c\x03\xc5\xbe",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F331F5\x03\x19\xc1\x03",
    b"\x1b\xffu\x00B\x04\x01\x80f\x8c\xeaHM\x93;\x8e\xeaHM\x93:\x01\x00\x00\x00\x00\x00\x00",
    b"\x02\x01\x06\x05\tRZSS",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F330C2\x03\x19\xc1\x03",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F33208\x03\x19\xc1\x03",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F330F3\x03\x19\xc1\x03",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F33163\x03\x19\xc1\x03",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F3320D\x03\x19\xc1\x03",
    b"\x02\x01\x1a\x0b\xffL\x00\t\x06\x03+\xc0\xa8kZ",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F330B5\x03\x19\xc1\x03",
    b"\x02\x01\x1a\x02\n\x0c\n\xffL\x00\x10\x05\x1b\x1c\x03\xc5\xbe",
    b"\x02\x01\x06\x03\x03\x12\x18\x10\tLOOKin_98F330B5\x03\x19\xc1\x03",
)


def test_parse_advertisement_data_tuple(benchmark):
    benchmark(lambda: parse_advertisement_data_tuple(advs))


def test_parse_advertisement_data_tuple_uncached(benchmark):
    joined_advs = b"".join(advs)
    benchmark(lambda: _uncached_parse_advertisement_data(joined_advs))
