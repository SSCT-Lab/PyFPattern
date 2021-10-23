def _import_lzma():
    '\n    Importing the `lzma` module.\n\n    Warns\n    -----\n    When the `lzma` module is not available.\n    '
    try:
        import lzma
        return lzma
    except ImportError:
        msg = 'Could not import the lzma module. Your installed Python is incomplete. Attempting to use lzma compression will result in a RuntimeError.'
        warnings.warn(msg)