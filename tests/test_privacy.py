from bluetooth_data_tools import get_cipher_for_irk, resolve_private_address


def test_resolve_private_address():
    cipher = get_cipher_for_irk(b"\x00" * 16)

    assert resolve_private_address(cipher, "40:01:02:0a:c4:a6")
    assert resolve_private_address(cipher, "40:02:03:d2:74:ce")
    assert not resolve_private_address(cipher, "40:00:00:d2:74:ce")
    assert not resolve_private_address(cipher, "00:01:ff:a0:3a:76")
