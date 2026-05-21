import cython


cdef str BLE_UUID

cdef dict _EMPTY_MANUFACTURER_DATA
cdef dict _EMPTY_SERVICE_DATA
cdef list _EMPTY_SERVICE_UUIDS

cdef object _cached_uint16_int_as_uuid
cdef object _cached_uint32_int_as_uuid
cdef object _cached_uint128_bytes_as_uuid
cdef object _cached_parse_advertisement_data
cdef object _cached_parse_advertisement_data_from_tuple

cdef object _LOGGER

cdef class BLEGAPAdvertisement:

    cdef readonly object local_name
    cdef readonly object service_uuids
    cdef readonly object service_data
    cdef readonly object manufacturer_data
    cdef readonly object tx_power

cdef cython.uint TYPE_SHORT_LOCAL_NAME
cdef cython.uint TYPE_COMPLETE_LOCAL_NAME
cdef cython.uint TYPE_MANUFACTURER_SPECIFIC_DATA
cdef cython.uint TYPE_16BIT_SERVICE_UUID_COMPLETE
cdef cython.uint TYPE_16BIT_SERVICE_UUID_MORE_AVAILABLE
cdef cython.uint TYPE_32BIT_SERVICE_UUID_COMPLETE
cdef cython.uint TYPE_32BIT_SERVICE_UUID_MORE_AVAILABLE
cdef cython.uint TYPE_128BIT_SERVICE_UUID_COMPLETE
cdef cython.uint TYPE_128BIT_SERVICE_UUID_MORE_AVAILABLE
cdef cython.uint TYPE_SERVICE_DATA
cdef cython.uint TYPE_SERVICE_DATA_32BIT_UUID
cdef cython.uint TYPE_SERVICE_DATA_128BIT_UUID
cdef cython.uint TYPE_TX_POWER_LEVEL

cdef unsigned char _INT8_SIGN_THRESHOLD
cdef cython.int _INT8_RANGE

cpdef parse_advertisement_data(object data)

@cython.locals(
    gap_data="const unsigned char *",
    gap_type_num="unsigned char",
    total_length=cython.uint,
    length="unsigned char",
    offset=cython.uint,
    start=cython.uint,
    end=cython.uint,
    i=cython.uint,
    tx_power_byte="unsigned char",
    uuid32_int=cython.uint,
)
cpdef _uncached_parse_advertisement_bytes(bytes gap_bytes)

cpdef _parse_advertisement_data_miss_via_bytes(bytes data)

cpdef _parse_advertisement_tuple_miss_via_bytes(tuple data)
