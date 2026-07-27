"""Every way the GAP parser can drop data must say so at DEBUG.

The parser never raises on malformed input -- it drops the offending AD
structure and returns whatever else parsed. That is the right behaviour for
untrusted radio data, but it means the debug log is the *only* signal that a
field went missing. An operator who enables
``bluetooth_data_tools.gap`` at DEBUG because a device looks wrong is asking
exactly one question: did you throw something away, and where?

Before this file the answer was "sometimes". Two of the twelve ways a
structure can be discarded were reported; the other ten -- a truncated
manufacturer id, a service-data header shorter than its UUID, a UUID list
ending mid-element, a TX Power field that is not one byte, an undefined type
0x00, and a trailing length byte with no type after it -- vanished in silence,
taking a whole field of the result with them.

These tests pin the contract per malformation class rather than in aggregate,
so a future refactor that collapses a branch cannot quietly take its
diagnostic with it. Each case asserts three things: the parse result is
unchanged (this is a diagnostics contract, not a behaviour change), exactly one
record is emitted, and the record names the structure's own offset.

``_uncached_parse_advertisement_bytes`` is called directly because the public
entry points are lru_cached -- a second call with the same payload would return
a cached tuple and log nothing, which would make a per-case assertion depend on
test ordering.
"""

from __future__ import annotations

import logging

import pytest

from bluetooth_data_tools.gap import _uncached_parse_advertisement_bytes

_LOGGER_NAME = "bluetooth_data_tools.gap"

# (id, gap_bytes, reason substring, offset of the malformed structure)
_MALFORMED = [
    (
        "undefined_type_zero",
        b"\x03\x00\xaa\xbb",
        "0x00 is not a defined AD type",
        0,
    ),
    (
        "length_overruns_buffer",
        b"\x40\x09\x41",
        "declared length overruns the buffer",
        0,
    ),
    (
        "length_leaves_no_payload",
        b"\x01\x09",
        "declared length leaves no payload",
        0,
    ),
    (
        "manufacturer_id_truncated",
        b"\x02\xff\xaa",
        "manufacturer-specific data needs a 2-byte company id",
        0,
    ),
    (
        "service_data_16_uuid_truncated",
        b"\x02\x16\xaa",
        "service data needs a 2-byte UUID",
        0,
    ),
    (
        "service_data_32_uuid_truncated",
        b"\x04\x20\x01\x02\x03",
        "32-bit service data needs a 4-byte UUID",
        0,
    ),
    (
        "service_data_128_uuid_truncated",
        b"\x05\x21\x01\x02\x03\x04",
        "128-bit service data needs a 16-byte UUID",
        0,
    ),
    (
        "uuid16_list_ends_mid_uuid",
        b"\x04\x03\x0d\x18\xaa",
        "16-bit service UUID list ends mid-UUID",
        0,
    ),
    (
        "uuid32_list_ends_mid_uuid",
        b"\x06\x05\x01\x02\x03\x04\xaa",
        "32-bit service UUID list ends mid-UUID",
        0,
    ),
    (
        "uuid128_list_ends_mid_uuid",
        b"\x05\x07\x01\x02\x03\x04",
        "128-bit service UUID list ends mid-UUID",
        0,
    ),
    (
        "tx_power_wrong_width",
        b"\x03\x0a\x10\x20",
        "TX Power Level must be exactly 1 byte",
        0,
    ),
    (
        "trailing_length_byte_without_type",
        b"\x02\x01\x06\x05",
        "length byte is the last byte with no type following",
        3,
    ),
]


@pytest.mark.parametrize(
    ("gap_bytes", "reason", "offset"),
    [pytest.param(*case[1:], id=case[0]) for case in _MALFORMED],
)
def test_every_dropped_ad_structure_is_reported(
    caplog: pytest.LogCaptureFixture, gap_bytes: bytes, reason: str, offset: int
) -> None:
    """Each way of discarding a structure emits exactly one located diagnostic."""
    with caplog.at_level(logging.DEBUG, logger=_LOGGER_NAME):
        _uncached_parse_advertisement_bytes(gap_bytes)

    # getMessage() renders the format string against its args -- an argument
    # count or type mismatch raises here rather than being swallowed by
    # logging's internal error handling.
    messages = [r.getMessage() for r in caplog.records if r.name == _LOGGER_NAME]
    assert len(messages) == 1, messages
    assert reason in messages[0], messages[0]
    assert f"at offset {offset}:" in messages[0], messages[0]


@pytest.mark.parametrize(
    ("gap_bytes", "reason", "offset"),
    [pytest.param(*case[1:], id=case[0]) for case in _MALFORMED],
)
def test_reporting_a_drop_does_not_change_the_parse(
    gap_bytes: bytes, reason: str, offset: int
) -> None:
    """Diagnosing a malformed structure must not alter what the parser returns.

    Pins the parse of every malformed payload above against the values the
    parser produced before any diagnostic existed: partially-valid input keeps
    the fields that did parse, and a dropped structure contributes nothing.
    """
    expected = {
        b"\x04\x03\x0d\x18\xaa": (
            None,
            ["0000180d-0000-1000-8000-00805f9b34fb"],
            {},
            {},
            None,
        ),
        b"\x06\x05\x01\x02\x03\x04\xaa": (
            None,
            ["04030201-0000-1000-8000-00805f9b34fb"],
            {},
            {},
            None,
        ),
    }.get(gap_bytes, (None, [], {}, {}, None))

    assert _uncached_parse_advertisement_bytes(gap_bytes) == expected


@pytest.mark.parametrize(
    "gap_bytes",
    [
        pytest.param(b"", id="empty"),
        pytest.param(b"\x02\x01\x06", id="flags_only"),
        # Zero padding is legal and extremely common: a controller pads the
        # 31-byte advertising payload with 0x00. Reporting it would drown the
        # log in noise on every well-formed advertisement.
        pytest.param(b"\x02\x01\x06\x00\x00", id="trailing_zero_padding"),
        pytest.param(b"\x00\x00\x00", id="all_zero_padding"),
        pytest.param(
            b"\x02\x01\x06"
            b"\x03\x03\x0d\x18"
            b"\x05\xff\x4c\x00\x10\x05"
            b"\x05\x16\x0d\x18\xaa\xbb"
            b"\x02\x0a\xf4",
            id="well_formed_advertisement",
        ),
        # Unhandled-but-defined types (appearance, URI) are not malformed --
        # the parser has nothing to do with them and must not complain.
        pytest.param(b"\x03\x19\x00\x02", id="appearance"),
        pytest.param(b"\x03\x24\x16\x2f", id="uri"),
    ],
)
def test_well_formed_input_is_silent(
    caplog: pytest.LogCaptureFixture, gap_bytes: bytes
) -> None:
    """Nothing the parser accepts -- or legitimately ignores -- may log."""
    with caplog.at_level(logging.DEBUG, logger=_LOGGER_NAME):
        _uncached_parse_advertisement_bytes(gap_bytes)

    assert [r.getMessage() for r in caplog.records if r.name == _LOGGER_NAME] == []


def test_each_structure_in_a_payload_is_reported_separately(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Two bad structures in one payload produce two located records.

    A shared reporting helper makes it easy to accidentally report per
    *advertisement* instead of per *structure*; this pins the granularity, and
    pins that the offsets track the structures rather than restarting at 0.
    """
    # offset 0: valid flags. offset 3: MSD with a 1-byte company id.
    # offset 6: 16-bit service data with a 1-byte UUID.
    gap_bytes = b"\x02\x01\x06\x02\xff\xaa\x02\x16\xbb"

    with caplog.at_level(logging.DEBUG, logger=_LOGGER_NAME):
        result = _uncached_parse_advertisement_bytes(gap_bytes)

    messages = [r.getMessage() for r in caplog.records if r.name == _LOGGER_NAME]
    assert len(messages) == 2, messages
    assert "at offset 3:" in messages[0], messages[0]
    assert "manufacturer-specific data needs a 2-byte company id" in messages[0]
    assert "at offset 6:" in messages[1], messages[1]
    assert "service data needs a 2-byte UUID" in messages[1]
    # The valid flags structure still parses; neither drop corrupts the result.
    assert result == (None, [], {}, {}, None)


def test_diagnostics_are_debug_level(caplog: pytest.LogCaptureFixture) -> None:
    """Malformed radio data is routine -- it must not surface above DEBUG.

    Broken firmware in range would otherwise emit a warning per advertisement.
    """
    with caplog.at_level(logging.DEBUG, logger=_LOGGER_NAME):
        _uncached_parse_advertisement_bytes(b"\x02\xff\xaa")

    records = [r for r in caplog.records if r.name == _LOGGER_NAME]
    assert records
    assert {r.levelno for r in records} == {logging.DEBUG}
