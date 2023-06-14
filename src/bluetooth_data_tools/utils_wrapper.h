

#include <stdint.h>
#include <stdio.h>

void _uint64_to_bdaddr(uint64_t address, char *bdaddr) {
    snprintf(bdaddr, 18, "%02X:%02X:%02X:%02X:%02X:%02X", (uint8_t) (address >> 40) & 0xff,
                       (uint8_t) (address >> 32) & 0xff, (uint8_t) (address >> 24) & 0xff,
                       (uint8_t) (address >> 16) & 0xff, (uint8_t) (address >> 8) & 0xff,
                       (uint8_t) (address >> 0) & 0xff);
}
