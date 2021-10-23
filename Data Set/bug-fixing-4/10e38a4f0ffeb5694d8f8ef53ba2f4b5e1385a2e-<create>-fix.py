def create(name='local'):
    "Creates a new KVStore.\n\n    Parameters\n    ----------\n    name : {'local'}\n        The type of KVStore.\n        - local works for multiple devices on a single machine (single process).\n        - dist works for multiple machines (multiple processes).\n    Returns\n    -------\n    kv : KVStore\n        The created KVStore.\n    "
    if (not isinstance(name, string_types)):
        raise TypeError('name must be a string')
    handle = KVStoreHandle()
    check_call(_LIB.MXKVStoreCreate(c_str(name), ctypes.byref(handle)))
    return KVStore(handle)