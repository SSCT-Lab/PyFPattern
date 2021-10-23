

def get_lib_extension():
    '\n    Return the platform-dependent extension for compiled modules.\n\n    '
    if (sys.platform in ['win32', 'cygwin']):
        return 'pyd'
    else:
        return 'so'
