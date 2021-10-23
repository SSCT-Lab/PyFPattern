def convert_to_bytes(param):
    '\n    This method convert units to bytes, which follow IEC standard.\n\n    :param param: value to be converted\n    '
    if (param is None):
        return None
    param = ''.join(param.split())
    if ((len(param) > 3) and (param[(- 3)].lower() in ['k', 'm', 'g', 't', 'p'])):
        return (int(param[:(- 3)]) * BYTES_MAP.get(param[(- 3):].lower(), 1))
    elif param.isdigit():
        return (int(param) * (2 ** 10))
    else:
        raise ValueError("Unsupported value(IEC supported): '{value}'".format(value=param))