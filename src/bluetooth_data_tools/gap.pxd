import cython


cdef object BLE_UID

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
    gap_value=cython.bytes,
    gap_type_num=cython.uint
)
cpdef parse_advertisement_data(object data)

cdef _decode_advertisement_data(cython.bytes encoded_struct)

cdef _int_as_uuid(object uuid_int)
