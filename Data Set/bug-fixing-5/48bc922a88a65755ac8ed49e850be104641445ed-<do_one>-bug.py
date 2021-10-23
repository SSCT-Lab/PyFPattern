def do_one(nb, to=None, execute=None, allow_errors=None, timeout=None, kernel_name=''):
    name = os.path.basename(nb)
    if execute:
        dst = os.path.join(EXECUTED_DIR, name)
        print(('Executeing %s to %s' % (nb, dst)))
        nb = execute_nb(nb, dst, allow_errors=allow_errors, timeout=timeout, kernel_name=kernel_name)
    dst = ((os.path.splitext(os.path.join(DST_DIR, name))[0] + '.') + to)
    print(('Converting %s to %s' % (nb, dst)))
    convert(nb, dst, to=to)
    return dst