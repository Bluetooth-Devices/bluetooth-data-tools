"""Pin the shared-container and cache-identity contract of the GAP parser.

``parse_advertisement_data``/``_bytes``/``_tuple`` are all ``lru_cache``-wrapped,
and an advertisement that carries none of a given AD type is handed a
module-level empty container rather than a fresh one. Both facts are documented
in ``gap.py``, and both are load-bearing beyond this package: downstream
consumers use ``is``/``is not`` on the returned containers to skip an expensive
merge when a repeated advertisement carries the same objects, and the shared
empties keep the hot parse path allocation-free for the common case.

Nothing in the rest of the suite distinguishes "the same object" from "an equal
object", so a refactor that starts returning fresh copies -- or that drops one
of the six ``if x is _EMPTY_...: x = {}`` copy-on-write guards in the parse loop
-- passes every equality assertion while silently breaking the contract. These
tests assert identity, which is exactly the part equality cannot see.
"""

from bluetooth_data_tools import (
    parse_advertisement_data,
    parse_advertisement_data_bytes,
    parse_advertisement_data_tuple,
)

# A legacy advertisement carrying every container-bearing AD type: flags, a
# two-entry 16-bit UUID list, 16-bit service data, and manufacturer data.
FULL = (
    b"\x02\x01\x06"  # flags
    b"\x05\x03\xaa\xfe\x0d\x18"  # 16-bit UUIDs: 0xfeaa, 0x180d
    b"\x05\x16\xaa\xfe\x01\x02"  # service data for 0xfeaa
    b"\x05\xff\x4c\x00\x03\x04"  # manufacturer data for 0x004c
)
# Two advertisements carrying none of those AD types, with differing content so
# they cannot share a cache entry with each other.
BARE_A = b"\x02\x01\x06\x05\tRZSS"
BARE_B = b"\x02\x01\x1a\x05\tWXYZ"


def test_same_payload_returns_the_same_advertisement_instance():
    """The cache hands every caller one instance, not one equal copy."""
    assert parse_advertisement_data((FULL,)) is parse_advertisement_data((FULL,))


def test_repeated_parse_returns_the_same_containers():
    """Downstream skips its merge on ``is``, so repeats must be identical.

    An equal-but-fresh container would silently defeat that fast path: the
    result stays correct and every equality assertion still passes, while the
    consumer pays for a full merge on every repeated advertisement.
    """
    first = parse_advertisement_data((FULL,))
    second = parse_advertisement_data((FULL,))

    assert first.service_uuids is second.service_uuids
    assert first.service_data is second.service_data
    assert first.manufacturer_data is second.manufacturer_data


def test_all_entry_points_share_one_set_of_containers():
    """The three public entry points route through one bytes-keyed cache."""
    adv = parse_advertisement_data((FULL,))
    _, uuids, service_data, manufacturer_data, _ = parse_advertisement_data_bytes(FULL)

    assert uuids is adv.service_uuids
    assert service_data is adv.service_data
    assert manufacturer_data is adv.manufacturer_data

    _, tuple_uuids, tuple_service_data, tuple_manufacturer_data, _ = (
        parse_advertisement_data_tuple((FULL,))
    )

    assert tuple_uuids is adv.service_uuids
    assert tuple_service_data is adv.service_data
    assert tuple_manufacturer_data is adv.manufacturer_data


def test_absent_ad_types_reuse_the_shared_empty_containers():
    """Two unrelated bare advertisements get the same empties, not new ones."""
    first = parse_advertisement_data((BARE_A,))
    second = parse_advertisement_data((BARE_B,))

    assert first is not second
    assert first.service_uuids is second.service_uuids
    assert first.service_data is second.service_data
    assert first.manufacturer_data is second.manufacturer_data


def test_parsing_a_populated_advertisement_does_not_poison_the_empties():
    """A populated parse must copy-on-write, never append to the shared empty.

    Dropping one of the ``is _EMPTY_...`` guards leaves the offending
    advertisement itself correct, so this only surfaces on the *next*
    advertisement that lacks the type -- process-wide corruption that no
    equality assertion about the populated payload can catch.
    """
    populated = parse_advertisement_data((FULL,))
    assert populated.service_uuids
    assert populated.service_data
    assert populated.manufacturer_data

    bare = parse_advertisement_data((BARE_A,))

    assert bare.service_uuids == []
    assert bare.service_data == {}
    assert bare.manufacturer_data == {}
    assert bare.service_uuids is not populated.service_uuids
    assert bare.service_data is not populated.service_data
    assert bare.manufacturer_data is not populated.manufacturer_data
