def warn_if_reserved(myvars):
    ' this function warns if any variable passed conflicts with internally reserved names '
    varnames = set(myvars)
    varnames.discard('vars')
    for varname in varnames.intersection(_RESERVED_NAMES):
        display.warning(('Found variable using reserved name: %s' % varname))