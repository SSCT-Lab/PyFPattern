def _get_lzma_file(lzma):
    "\n    Attempting to get the lzma.LZMAFile class.\n\n    Returns\n    -------\n    class\n        The lzma.LZMAFile class.\n\n    Raises\n    ------\n    RuntimeError\n        If the module lzma was not imported correctly, or didn't exist.\n    "
    if (lzma is None):
        raise RuntimeError('lzma module not available. A Python re-install with the proper dependencies might be required to solve this issue.')
    return lzma.LZMAFile