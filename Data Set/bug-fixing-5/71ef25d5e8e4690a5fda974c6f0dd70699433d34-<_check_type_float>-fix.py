def _check_type_float(self, value):
    if isinstance(value, float):
        return value
    if isinstance(value, (binary_type, text_type, int)):
        return float(value)
    raise TypeError(('%s cannot be converted to a float' % type(value)))