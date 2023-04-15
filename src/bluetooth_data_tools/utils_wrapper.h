

#include <stdint.h>
#include <string>
#include <memory>

#define BDADDR_SIZE 18  // 17 + '\0'

using namespace std;


std::string _cpp_uint64_to_bdaddr(uint64_t address) {
    std::unique_ptr<char[]> buf( new char[ BDADDR_SIZE ] );
    std::snprintf( buf.get(), BDADDR_SIZE, "%02X:%02X:%02X:%02X:%02X:%02X", (uint8_t) (address >> 40) & 0xff,
                       (uint8_t) (address >> 32) & 0xff, (uint8_t) (address >> 24) & 0xff,
                       (uint8_t) (address >> 16) & 0xff, (uint8_t) (address >> 8) & 0xff,
                       (uint8_t) (address >> 0) & 0xff );
    return std::string( buf.get(), buf.get() + BDADDR_SIZE - 1 ); // We don't want the '\0' inside
}
