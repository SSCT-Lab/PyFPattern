def _vector_str(tensor):
    (fmt, scale, _) = _number_format(tensor.storage())
    strt = ''
    if (scale != 1):
        strt += SCALE_FORMAT.format(scale)
    return ('\n'.join((fmt.format((val / scale)) for val in tensor)) + '\n')