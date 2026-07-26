#include <stddef.h>
#include <stdint.h>

/**
* Sentinel returned by _bdaddr_to_uint64 to signal a parse failure.
*/
#define BDADDR_PARSE_ERROR UINT64_MAX

/**
* Decode one hex character to its 4-bit value, or 0xFF on invalid input.
*/
static inline uint8_t _hex_nibble(char c) {
    if (c >= '0' && c <= '9') return (uint8_t)(c - '0');
    if (c >= 'A' && c <= 'F') return (uint8_t)(c - 'A' + 10);
    if (c >= 'a' && c <= 'f') return (uint8_t)(c - 'a' + 10);
    return 0xFF;
}

/**
* Parse a bluetooth address string into a uint64_t.
*
* Accepts either the 17-byte separated form ("AA:BB:CC:DD:EE:FF" — also
* the "AA-BB-CC-DD-EE-FF" Windows form) or the 12-byte unseparated form
* ("AABBCCDDEEFF"). Returns BDADDR_PARSE_ERROR on any parse error.
*/
static inline uint64_t _bdaddr_to_uint64(const char *bdaddr, size_t length) {
    size_t step;
    if (length == 17) {
        step = 3;
    } else if (length == 12) {
        step = 2;
    } else {
        return BDADDR_PARSE_ERROR;
    }
    uint64_t result = 0;
    for (size_t i = 0; i < 6; ++i) {
        size_t pos = i * step;
        uint8_t hi = _hex_nibble(bdaddr[pos]);
        uint8_t lo = _hex_nibble(bdaddr[pos + 1]);
        if (hi == 0xFF || lo == 0xFF) {
            return BDADDR_PARSE_ERROR;
        }
        result = (result << 8) | (uint64_t)((hi << 4) | lo);
        if (step == 3 && i < 5) {
            char sep = bdaddr[pos + 2];
            if (sep != ':' && sep != '-') {
                return BDADDR_PARSE_ERROR;
            }
        }
    }
    return result;
}

/**
* Convert the given integer bluetooth address to its hexadecimal string representation.
* The buffer passed in must accept at least 17 bytes. It will NOT be null-terminated.
*/
void _uint64_to_bdaddr(uint64_t address, char bdaddr[17]) {
    static const char hex_table[] = "0123456789ABCDEF";
    bdaddr[0] = hex_table[(address >> 44) & 0x0F];
    bdaddr[1] = hex_table[(address >> 40) & 0x0F];
    bdaddr[2] = ':';
    bdaddr[3] = hex_table[(address >> 36) & 0x0F];
    bdaddr[4] = hex_table[(address >> 32) & 0x0F];
    bdaddr[5] = ':';
    bdaddr[6] = hex_table[(address >> 28) & 0x0F];
    bdaddr[7] = hex_table[(address >> 24) & 0x0F];
    bdaddr[8] = ':';
    bdaddr[9] = hex_table[(address >> 20) & 0x0F];
    bdaddr[10] = hex_table[(address >> 16) & 0x0F];
    bdaddr[11] = ':';
    bdaddr[12] = hex_table[(address >> 12) & 0x0F];
    bdaddr[13] = hex_table[(address >> 8) & 0x0F];
    bdaddr[14] = ':';
    bdaddr[15] = hex_table[(address >> 4) & 0x0F];
    bdaddr[16] = hex_table[address & 0x0F];
}
