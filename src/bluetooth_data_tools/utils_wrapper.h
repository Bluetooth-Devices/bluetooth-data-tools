

#include <stdint.h>
#include <stdio.h>

void _uint64_to_bdaddr(uint64_t address, char *bdaddr) {
    static const char hex_table[] = "0123456789ABCDEF";
    *bdaddr++ = hex_table[(address >> 44) & 0x0F];
    *bdaddr++ = hex_table[(address >> 40) & 0x0F];
    *bdaddr++ = ':';
    *bdaddr++ = hex_table[(address >> 36) & 0x0F];
    *bdaddr++ = hex_table[(address >> 32) & 0x0F];
    *bdaddr++ = ':';
    *bdaddr++ = hex_table[(address >> 28) & 0x0F];
    *bdaddr++ = hex_table[(address >> 24) & 0x0F];
    *bdaddr++ = ':';
    *bdaddr++ = hex_table[(address >> 20) & 0x0F];
    *bdaddr++ = hex_table[(address >> 16) & 0x0F];
    *bdaddr++ = ':';
    *bdaddr++ = hex_table[(address >> 12) & 0x0F];
    *bdaddr++ = hex_table[(address >> 8) & 0x0F];
    *bdaddr++ = ':';
    *bdaddr++ = hex_table[(address >> 4) & 0x0F];
    *bdaddr++ = hex_table[address & 0x0F];
    *bdaddr++ = '\0';
}
