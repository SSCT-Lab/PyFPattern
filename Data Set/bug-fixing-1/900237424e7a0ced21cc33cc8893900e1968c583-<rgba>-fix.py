

def rgba(s, *args):
    'Return a Kivy color (4 value from 0-1 range) from either a hex string or\n    a list of 0-255 values.\n\n    .. versionadded:: 1.10.0\n    '
    if isinstance(s, string_types):
        return get_color_from_hex(s)
    if isinstance(s, (list, tuple)):
        s = [(x / 255.0) for x in s]
        if (len(s) == 3):
            s.append(1)
        return s
    if isinstance(s, (int, float)):
        s = [(s / 255.0)]
        s.extend(((x / 255.0) for x in args))
        if (len(s) == 3):
            s.append(1)
        return s
    raise Exception('Invalid value (not a string / list / tuple)')
