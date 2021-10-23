def _vector_str(self):
    (fmt, scale, _) = _number_format(self)
    strt = ''
    ident = ''
    if (scale != 1):
        strt += SCALE_FORMAT.format(scale)
        ident = ' '
    return ((strt + '\n'.join(((ident + fmt.format((val / scale))) for val in self))) + '\n')