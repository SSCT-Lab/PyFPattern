

def waitall():
    'Wait for all async operations to finish in MXNet.\n\n    This function is used for benchmarking only.\n    .. warning::\n    If your code has exceptions, `waitall` can cause silent failures.\n    For this reason you should avoid `waitall` in your code.\n    Use it only if you are confident that your code is error free.\n    Then make sure you call `wait_to_read` on all outputs after `waitall`.\n    '
    check_call(_LIB.MXNDArrayWaitAll())
