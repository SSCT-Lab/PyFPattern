def _parse_value(self, value):
    if (value is None):
        return ''
    elif isinstance(value, bool):
        if value:
            return '1'
        else:
            return '0'
    elif isinstance(value, string_types):
        if (value.lower() in BOOLEANS_TRUE):
            return '1'
        elif (value.lower() in BOOLEANS_FALSE):
            return '0'
        else:
            return value.strip()
    else:
        return value