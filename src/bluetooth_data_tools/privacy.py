"""Helpers for resolving a private address if you know its identity resolving key.

This process uses 128bit IRK as encryption key for ECB AES.

One half of the address stores a random 24bit number (prand).
This is encrypted to produce a "hash": the least significant 24
bits of the AES output. That hash should match the other half of
the MAC address.

See https://www.mdpi.com/2227-7390/10/22/4346
"""

import binascii
import hmac

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

PADDING = b"\x00" * 13
ADDRESS_LENGTH = 6


def get_cipher_for_irk(irk: bytes) -> Cipher:
    return Cipher(algorithms.AES(irk), modes.ECB())  # noqa: S305


def resolve_private_address(
    cipher: Cipher,
    address: str,
) -> bool:
    """Return True if ``address`` is a private address resolvable by ``cipher``.

    ``address`` may be colon-separated, hyphen-separated, or unseparated, the
    same three forms ``mac_to_int`` and ``short_address`` accept. Anything that
    is not six hex octets raises ``ValueError``.
    """
    # Strip both separators (matching mac_to_int / short_address) so every
    # accepted spelling reaches the same bytes.
    rpa = binascii.unhexlify(address.replace(":", "").replace("-", ""))
    if len(rpa) != ADDRESS_LENGTH:
        # Without this, a wrong-length address is not an error: a short one
        # trips IndexError or the cipher's block-length check, and any other
        # length loses the compare_digest below and returns a silent False
        # that reads as "this IRK does not match".
        raise ValueError(f"Invalid Bluetooth address: {address!r}")

    if rpa[0] & 0xC0 != 0x40:
        # Not an RPA
        return False

    pt = PADDING + rpa[:3]

    encryptor = cipher.encryptor()
    ct = encryptor.update(pt) + encryptor.finalize()

    return hmac.compare_digest(ct[13:], rpa[3:])
