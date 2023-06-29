import cython


cdef str BLE_UUID

cdef object from_bytes
cdef object from_bytes_little

cdef object _cached_uint64_bytes_as_uuid
cdef object _cached_uint16_bytes_as_uuid
cdef object _cached_uint32_bytes_as_uuid
cdef object _cached_uint128_bytes_as_uuid


cdef class BLEGAPAdvertisement:

    cdef public object local_name
    cdef public object service_uuids
    cdef public object service_data
    cdef public object manufacturer_data
    cdef public object tx_power

cdef cython.uint TYPE_SHORT_LOCAL_NAME
cdef cython.uint TYPE_COMPLETE_LOCAL_NAME
cdef cython.uint TYPE_MANUFACTURER_SPECIFIC_DATA
cdef cython.uint TYPE_16BIT_SERVICE_UUID_COMPLETE
cdef cython.uint TYPE_16BIT_SERVICE_UUID_MORE_AVAILABLE
cdef cython.uint TYPE_128BIT_SERVICE_UUID_COMPLETE
cdef cython.uint TYPE_128BIT_SERVICE_UUID_MORE_AVAILABLE
cdef cython.uint TYPE_SERVICE_DATA
cdef cython.uint TYPE_SERVICE_DATA_32BIT_UUID
cdef cython.uint TYPE_SERVICE_DATA_128BIT_UUID
cdef cython.uint TYPE_TX_POWER_LEVEL


@cython.locals(
    gap_data=cython.bytes,
    gap_value=cython.bytes,
    gap_type_num=cython.uint,
    total_length=cython.uint,
    length=cython.uint,
    offset=cython.uint,
    start=cython.uint,
    end=cython.uint,
)
cpdef parse_advertisement_data(object data)
