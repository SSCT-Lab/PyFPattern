def do_one(nb, to=None, execute=None, allow_errors=None, timeout=None, kernel_name=''):
    from traitlets.traitlets import TraitError
    import jupyter_client
    name = os.path.basename(nb)
    if execute:
        dst = os.path.join(EXECUTED_DIR, name)
        print(('Executeing %s to %s' % (nb, dst)))
        nb = execute_nb(nb, dst, allow_errors=allow_errors, timeout=timeout, kernel_name=kernel_name)
    dst = ((os.path.splitext(os.path.join(DST_DIR, name))[0] + '.') + to)
    print(('Converting %s to %s' % (nb, dst)))
    try:
        convert(nb, dst, to=to)
    except TraitError:
        kernels = jupyter_client.kernelspec.find_kernel_specs()
        msg = (('Could not find kernel named `%s`, Available kernels:\n %s' % kernel_name), kernels)
        raise ValueError(msg)
    return dst