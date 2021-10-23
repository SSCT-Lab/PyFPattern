

def waitall():
    'Wait for all async operations to finish in MXNet.\n\n    This function is used for benchmarking only.\n    '
    check_call(_LIB.MXNDArrayWaitAll())
