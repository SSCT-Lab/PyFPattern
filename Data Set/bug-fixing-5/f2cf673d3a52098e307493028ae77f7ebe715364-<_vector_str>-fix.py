def _vector_str(self):
    (fmt, scale, _) = _number_format(self)
    strt = ''
    if (scale != 1):
        strt += SCALE_FORMAT.format(scale)
    return ('\n'.join((fmt.format((val / scale)) for val in self)) + '\n')