from pytest_codspeed import BenchmarkFixture

from bluetooth_data_tools import get_cipher_for_irk, resolve_private_address

# IRK + addresses borrowed from tests/test_privacy.py so the AES path
# walks the same code shape as the existing functional coverage.
_IRK = b"\x00" * 16
_CIPHER = get_cipher_for_irk(_IRK)

# Top two bits != 0b01: skipped before the AES encrypt. Real BLE scans
# see this every time a public/static-random address is encountered.
_NON_RPA = "00:01:ff:a0:3a:76"

# Top two bits == 0b01 with a hash that matches under the zero IRK.
_RPA_MATCH = "40:01:02:0a:c4:a6"

# Top two bits == 0b01 but the hash does not match — exercises the full
# encrypt + compare_digest path with a False result.
_RPA_MISMATCH = "40:00:00:d2:74:ce"


def test_resolve_private_address_non_rpa(benchmark: BenchmarkFixture) -> None:
    benchmark(lambda: resolve_private_address(_CIPHER, _NON_RPA))


def test_resolve_private_address_match(benchmark: BenchmarkFixture) -> None:
    benchmark(lambda: resolve_private_address(_CIPHER, _RPA_MATCH))


def test_resolve_private_address_mismatch(benchmark: BenchmarkFixture) -> None:
    benchmark(lambda: resolve_private_address(_CIPHER, _RPA_MISMATCH))
