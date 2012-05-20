from libc.stdint cimport int32_t

cdef extern from "avbin.h":
    int32_t avbin_get_version()
