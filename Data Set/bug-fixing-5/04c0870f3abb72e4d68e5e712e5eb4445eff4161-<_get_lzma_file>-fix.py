def _get_lzma_file(lzma):
    "\n    Importing the `LZMAFile` class from the `lzma` module.\n\n    Returns\n    -------\n    class\n        The `LZMAFile` class from the `lzma` module.\n\n    Raises\n    ------\n    RuntimeError\n        If the `lzma` module was not imported correctly, or didn't exist.\n    "
    if (lzma is None):
        raise RuntimeError('lzma module not available. A Python re-install with the proper dependencies, might be required to solve this issue.')
    return lzma.LZMAFile