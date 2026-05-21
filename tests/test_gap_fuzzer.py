"""Fuzz coverage for the GAP parser.

The broad fuzz loop is intentionally unseeded so each CI run explores
fresh inputs — that is how regressions like the off-by-one fixed in
PR #221 surface. The seed used for a given run is printed (and can be
pinned with the ``FUZZ_SEED`` environment variable) so any failure is
reproducible locally.

Only the uncached parse path is fuzzed: ``parse_advertisement_data`` and
friends are thin LRU-cache wrappers around it, so re-running the same
bytes through them adds cost without coverage.
"""

import os
import random

from bluetooth_data_tools.gap import (
    _parse_advertisement_data_miss_via_bytes,
    parse_advertisement_data,
)

_FUZZ_ITERATIONS = 1000


def test_gap_fuzzer_random_bytes_do_not_crash() -> None:
    seed = int(os.environ.get("FUZZ_SEED", random.randrange(2**64)))
    print(f"fuzz seed: {seed:#x}")
    rng = random.Random(seed)
    for _ in range(_FUZZ_ITERATIONS):
        adv = (
            bytes(rng.randint(0, 255) for _ in range(rng.randint(1, 31))),
            bytes(rng.randint(0, 255) for _ in range(rng.randint(1, 31))),
            bytes(rng.randint(0, 255) for _ in range(rng.randint(1, 31))),
        )
        _parse_advertisement_data_miss_via_bytes(b"".join(adv))


def test_gap_fuzzer_truncated_length_does_not_crash() -> None:
    """An AD struct that claims more bytes than remain must be rejected, not read."""
    rng = random.Random(0xB1EC0FFEE)
    for _ in range(200):
        # Claim a length that overruns the buffer, then provide a shorter body.
        body = bytes(rng.randint(0, 255) for _ in range(rng.randint(0, 5)))
        payload = bytes([100, rng.randint(1, 0xFF)]) + body
        adv = parse_advertisement_data((payload,))
        assert adv.local_name is None
        assert adv.manufacturer_data == {}
        assert adv.service_data == {}
        assert adv.service_uuids == []
