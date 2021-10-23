def get_lib_extension():
    '\n    Return the platform-dependent extension for compiled modules.\n\n    '
    if (sys.platform == 'win32'):
        return 'pyd'
    elif (sys.platform == 'cygwin'):
        return 'dll'
    else:
        return 'so'