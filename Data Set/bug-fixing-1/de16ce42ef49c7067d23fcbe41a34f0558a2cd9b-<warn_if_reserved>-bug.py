

def warn_if_reserved(myvars):
    ' this function warns if any variable passed conflicts with internally reserved names '
    reserved = get_reserved_names()
    for varname in myvars:
        if (varname == 'vars'):
            continue
        if (varname in reserved):
            display.warning(('Found variable using reserved name: %s' % varname))
