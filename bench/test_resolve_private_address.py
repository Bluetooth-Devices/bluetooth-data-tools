from bluetooth_data_tools import get_cipher_for_irk, resolve_private_address

_IRK = b"\x00" * 16
_CIPHER = get_cipher_for_irk(_IRK)

_NON_RPA = "00:01:ff:a0:3a:76"
_RPA_MATCH = "40:01:02:0a:c4:a6"
_RPA_MISMATCH = "40:00:00:d2:74:ce"


def test_resolve_private_address_non_rpa(benchmark):
    benchmark(lambda: resolve_private_address(_CIPHER, _NON_RPA))


def test_resolve_private_address_match(benchmark):
    benchmark(lambda: resolve_private_address(_CIPHER, _RPA_MATCH))


def test_resolve_private_address_mismatch(benchmark):
    benchmark(lambda: resolve_private_address(_CIPHER, _RPA_MISMATCH))
