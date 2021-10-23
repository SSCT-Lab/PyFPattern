

def rgba(s, *args):
    'Return a Kivy color (4 value from 0-1 range) from either a hex string or\n    a list of 0-255 values.\n\n    .. versionadded:: 1.10.0\n    '
    if isinstance(s, string_types):
        return get_color_from_hex(s)
    elif isinstance(s, (list, tuple)):
        s = map((lambda x: (x / 255.0)), s)
        if (len(s) == 3):
            return (list(s) + [1])
        return s
    elif isinstance(s, (int, float)):
        s = map((lambda x: (x / 255.0)), ([s] + list(args)))
        if (len(s) == 3):
            return (list(s) + [1])
        return s
    raise Exception('Invalid value (not a string / list / tuple)')
