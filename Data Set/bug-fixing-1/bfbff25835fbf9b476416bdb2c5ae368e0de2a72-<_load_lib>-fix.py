

def _load_lib():
    'Load library by searching possible path.'
    lib_path = libinfo.find_lib_path()
    lib = ctypes.CDLL(lib_path[0], ctypes.RTLD_LOCAL)
    lib.MXGetLastError.restype = ctypes.c_char_p
    return lib
