"""Differential tests: the compiled build must behave like the pure-Python one.

Two modules ship a second implementation that the test suite never compares
against the first:

* ``utils.py`` picks the native ``_utils_impl`` parsers when the extension
  built, and defines pure-Python fallbacks otherwise. Only one of the two
  exists per interpreter, so no ordinary test can catch them drifting apart --
  which is how the ``mac_to_int`` fallback ended up accepting non-ASCII digits
  the native parser rejected (#290).
* ``gap.py`` is compiled in place against ``gap.pxd``, which types the parse
  loop's locals as C integers and ``gap_data`` as a raw ``const unsigned
  char *``. C semantics are not Python semantics: the ``uuid32_int`` local is
  declared ``cython.uint`` precisely because a shift-by-24 of an unsigned char
  promotes to *signed* int in C and would otherwise yield a negative 32-bit
  UUID. The raw pointer also means the compiled parser has no bounds-check
  safety net -- every check in the loop is manual.

CI runs the suite once with ``SKIP_CYTHON`` and once with ``REQUIRE_CYTHON``,
but each run only ever asserts against a single build. These tests load the
``.py`` sources a second time, as pure-Python modules, so both implementations
are live in one process and can be compared directly. Under ``SKIP_CYTHON``
that comparison is pure-vs-pure and near-free; under ``REQUIRE_CYTHON`` it is a
real compiled-vs-interpreted differential.
"""

from __future__ import annotations

import importlib.util
import random
import sys
from collections.abc import Callable
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

import bluetooth_data_tools.gap as gap_build
import bluetooth_data_tools.utils as utils_build

_PACKAGE = "bluetooth_data_tools"
_SOURCE_DIR = Path(utils_build.__file__).parent


def _load_pure(name: str, *, block: str | None = None) -> ModuleType:
    """Import ``<name>.py`` from the installed package as a pure-Python module.

    The module is given a distinct import name so it coexists with the
    (possibly compiled) module already in ``sys.modules``, but keeps
    ``bluetooth_data_tools`` as its package so relative imports still resolve.
    ``block`` names a submodule to make unimportable for the duration of the
    exec, which is how ``utils.py`` is forced down its ``except ImportError``
    fallback branch even when the native extension is present.
    """
    source = _SOURCE_DIR / f"{name}.py"
    # Compiled builds ship the .py sources alongside the extension modules, so a
    # missing source means packaging changed and this comparison silently stopped
    # being possible -- fail loudly rather than skip.
    assert source.is_file(), f"{source} is not shipped alongside the built module"

    spec = importlib.util.spec_from_file_location(f"{_PACKAGE}._pure_{name}", source)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    module.__package__ = _PACKAGE

    blocked = f"{_PACKAGE}.{block}" if block else None
    sentinel = object()
    previous: Any = sentinel
    if blocked is not None:
        previous = sys.modules.get(blocked, sentinel)
        # Binding a module name to None in sys.modules makes importing it raise
        # ImportError, which is exactly the branch we want to take.
        sys.modules[blocked] = None  # type: ignore[assignment]
    try:
        spec.loader.exec_module(module)
    finally:
        if blocked is not None:
            if previous is sentinel:
                del sys.modules[blocked]
            else:
                sys.modules[blocked] = previous
    return module


pure_gap = _load_pure("gap")
pure_utils = _load_pure("utils", block="_utils_impl")


def _outcome(func: Callable[..., Any], *args: Any) -> Any:
    """Return the call's result, or its exception type when it raises.

    Comparing exception *types* rather than messages keeps the assertion on the
    contract callers actually branch on; the native and pure parsers word their
    ``ValueError`` identically today but that is not the property under test.
    """
    try:
        return ("return", func(*args))
    except Exception as err:  # noqa: BLE001 - the type is the assertion
        return ("raise", type(err))


def test_pure_modules_are_distinct_objects() -> None:
    """Guard the harness itself: a no-op load would make every test vacuous."""
    assert pure_gap is not gap_build
    assert pure_utils is not utils_build
    assert pure_gap._uncached_parse_advertisement_bytes is not (
        gap_build._uncached_parse_advertisement_bytes
    )
    # The fallback must be the pure-Python def, never the native cyfunction.
    assert pure_utils._mac_to_int.__module__ != f"{_PACKAGE}._utils_impl"


def _encode_ad(ad_type: int, payload: bytes) -> bytes:
    """Encode one ``[length][type][payload...]`` AD structure."""
    return bytes([1 + len(payload), ad_type]) + payload


# AD types that exercise every branch of the parse loop, including the C-typed
# UUID assembly and the multi-entry list loops.
_AD_TYPES = (
    0x00,  # empty type -> whole structure skipped
    0x01,  # flags, short-circuited
    0x02,
    0x03,  # 16-bit UUID lists
    0x04,
    0x05,  # 32-bit UUID lists
    0x06,
    0x07,  # 128-bit UUID lists
    0x08,
    0x09,  # short / complete local name
    0x0A,  # tx power
    0x16,  # 16-bit service data
    0x19,  # appearance, unhandled
    0x20,  # 32-bit service data
    0x21,  # 128-bit service data
    0xFF,  # manufacturer specific
)

# Payload bodies chosen to straddle the C-integer edges: 0xFF... bytes drive the
# high bit of the assembled 16/32-bit UUIDs, and the odd lengths leave the
# trailing remainders the list loops must discard.
_PAYLOADS = (
    b"",
    b"\x00",
    b"\xff",
    b"\x80",
    b"\x00\x00",
    b"\xff\xff",
    b"\xff\xff\xff\xff",
    b"\x00\x00\x00\x80",
    b"\xff\xff\xff\xff\xff\xff\xff",  # 3x16-bit + 1 leftover byte
    b"\xff" * 12,  # 3x32-bit
    b"\x80" * 16,
    b"\xff" * 16,
    b"\xff" * 31,  # 1x128-bit + 15 leftover
    b"\xff" * 32,
    bytes(range(0, 40)),
    "hello wörld".encode(),
    b"\xc3\x28",  # invalid UTF-8, must decode with "replace" identically
    b"\xed\xa0\x80",  # UTF-8-encoded surrogate
)


def _structured_payloads() -> list[bytes]:
    """Every (AD type, body) pair, plus framing edge cases around each."""
    payloads: list[bytes] = [b"", b"\x00", b"\x01", b"\x02", b"\x00\x00", b"\xff"]
    for ad_type in _AD_TYPES:
        for body in _PAYLOADS:
            encoded = _encode_ad(ad_type, body)
            payloads.append(encoded)
            # Truncated: the declared length runs past the buffer.
            payloads.append(encoded[:-1])
            # Zero padding before and after, which the loop skips byte-wise.
            payloads.append(b"\x00" + encoded)
            payloads.append(encoded + b"\x00\x00")
            # A declared length that overruns while the bytes are present.
            payloads.append(bytes([len(body) + 8, ad_type]) + body)
            # Two of the same structure back to back.
            payloads.append(encoded * 2)
    # Every AD type at length 1 (type byte, no body) and length 2.
    for ad_type in _AD_TYPES:
        payloads.append(bytes([1, ad_type]))
        payloads.append(bytes([2, ad_type]))
    return payloads


def _random_payloads(count: int, seed: int) -> list[bytes]:
    """Random payloads biased toward plausible framing.

    Purely uniform bytes almost always fail the first length check, so half the
    corpus is assembled from real AD structures with random bodies and the rest
    is raw noise.
    """
    rng = random.Random(seed)
    payloads: list[bytes] = []
    for _ in range(count // 2):
        chunk = b"".join(
            _encode_ad(
                rng.choice(_AD_TYPES),
                bytes(rng.getrandbits(8) for _ in range(rng.randrange(0, 34))),
            )
            for _ in range(rng.randrange(1, 4))
        )
        payloads.append(chunk)
    for _ in range(count - len(payloads)):
        payloads.append(bytes(rng.getrandbits(8) for _ in range(rng.randrange(0, 48))))
    return payloads


@pytest.mark.parametrize(
    "payloads",
    (
        pytest.param(_structured_payloads(), id="structured"),
        pytest.param(_random_payloads(2000, seed=0x5EED), id="random"),
    ),
)
def test_gap_parse_matches_pure_python(payloads: list[bytes]) -> None:
    """The built parser must return exactly what the .py source returns.

    ``_uncached_parse_advertisement_bytes`` is the single function every public
    entry point funnels into, so comparing it covers the cached wrappers too
    without paying for their LRU churn.
    """
    built = gap_build._uncached_parse_advertisement_bytes
    pure = pure_gap._uncached_parse_advertisement_bytes
    for payload in payloads:
        assert _outcome(built, payload) == _outcome(pure, payload), payload.hex()


def test_gap_advertisement_object_matches_pure_python() -> None:
    """The cdef class must expose the same attributes as the Python class.

    ``BLEGAPAdvertisement`` is a ``cdef class`` with ``readonly`` members in the
    compiled build and a ``__slots__`` class otherwise -- different object
    models reaching the same public surface.
    """
    for payload in _structured_payloads():
        built = gap_build.parse_advertisement_data((payload,))
        pure = pure_gap.parse_advertisement_data((payload,))
        assert built.local_name == pure.local_name
        assert built.service_uuids == pure.service_uuids
        assert built.service_data == pure.service_data
        assert built.manufacturer_data == pure.manufacturer_data
        assert built.tx_power == pure.tx_power


def test_gap_tuple_entry_points_match_pure_python() -> None:
    """Multi-chunk input joins identically in both builds."""
    chunks = _structured_payloads()
    for data in zip(chunks, reversed(chunks), strict=True):
        assert _outcome(gap_build.parse_advertisement_data_tuple, data) == _outcome(
            pure_gap.parse_advertisement_data_tuple, data
        )


def _mac_corpus() -> list[str]:
    """Address strings spanning both accepted forms and the ways they fail."""
    base = "AABBCCDDEEFF"
    octets = [base[i : i + 2] for i in range(0, 12, 2)]
    corpus = [
        base,
        base.lower(),
        "aAbBcCdDeEfF",
        ":".join(octets),
        "-".join(octets),
        "AA:bb:CC:dd:EE:ff",
        "AA-BB:CC-DD:EE-FF",  # separators may be mixed
        "000000000000",
        "00:00:00:00:00:00",
        "FFFFFFFFFFFF",
        "FF:FF:FF:FF:FF:FF",
    ]
    # Wrong lengths, including the two accepted ones off by one either way.
    corpus += ["A" * n for n in (0, 1, 11, 13, 16, 18, 34)]
    # Wrong separator character, and a separator in the wrong column.
    corpus += [".".join(octets), "_".join(octets), " ".join(octets)]
    corpus += ["AAB:BCC:DDE:EFF:00:11", "A:ABBCCDDEEFF", "AA:BB:CC:DD:EEFF:"]
    # Non-hex, non-ASCII, and the Unicode digits int(x, 16) would otherwise
    # accept -- the exact class of input that diverged in #290.
    corpus += [
        "GG:BB:CC:DD:EE:FF",
        "ZZZZZZZZZZZZ",
        "٠" * 12,
        "１" * 12,
        "AABBCCDDEE٠١",
        "AA:BB:CC:DD:EE:٠١",
        "AABBCCDDEE\U0001f600",
        "AABBCCDDEE\x00\x00",
        "AA:BB:CC:DD:EE:F\x00",
        "+AABBCCDDEEF",
        "-AABBCCDDEEF",
        " AABBCCDDEEFF",
        "AABBCCDDEEFF ",
        "0x0AABBCCDDE",
    ]
    # Every single-character mutation of both accepted forms.
    for form in ("AA:BB:CC:DD:EE:FF", base):
        for index in range(len(form)):
            for char in "0fFzZ:-. \x00٠":
                corpus.append(form[:index] + char + form[index + 1 :])
    return corpus


def test_mac_to_int_matches_pure_python() -> None:
    """Accepted forms and rejections must be identical in both builds."""
    for address in _mac_corpus():
        assert _outcome(utils_build._mac_to_int, address) == _outcome(
            pure_utils._mac_to_int, address
        ), address


def test_int_to_bluetooth_address_matches_pure_python() -> None:
    """Both builds must agree across the whole 48-bit address space.

    The domain is deliberately ``[0, 2**48)``: a Bluetooth address is 48 bits,
    and outside that range the two implementations legitimately differ (the
    native parser masks to the low 48 bits, the pure one formats the value as
    given). Nothing in the package produces an out-of-range value -- both
    ``mac_to_int`` and six-byte address parsing are bounded by 2**48 -- so the
    contract is the in-range behaviour and only that is asserted here.
    """
    rng = random.Random(0xADD8E55)
    values = [*range(0, 512), 2**24, 2**47, 2**48 - 1]
    values += [rng.randrange(0, 2**48) for _ in range(2000)]
    for value in values:
        assert utils_build._int_to_bluetooth_address(
            value
        ) == pure_utils._int_to_bluetooth_address(value), value


def test_int_to_bluetooth_address_round_trips_through_mac_to_int() -> None:
    """Pin the invariant that keeps the out-of-domain divergence unreachable."""
    rng = random.Random(0xB0A7)
    for _ in range(2000):
        value = rng.randrange(0, 2**48)
        address = utils_build._int_to_bluetooth_address(value)
        assert utils_build._mac_to_int(address) == value
        assert pure_utils._mac_to_int(address) == value
