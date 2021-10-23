def do(fp=None, directory=None, to='html', execute=True, allow_errors=True, timeout=1000, kernel_name=''):
    if (fp is None):
        nbs = find_notebooks(directory)
    else:
        nbs = [fp]
    if (kernel_name is None):
        kernel_name = find_kernel_name()
    func = partial(do_one, to=to, execute=execute, allow_errors=allow_errors, timeout=timeout, kernel_name=kernel_name)
    if par:
        with futures.ProcessPoolExecutor() as pool:
            for dst in pool.map(func, nbs):
                print(('Finished %s' % dst))
    else:
        for nb in nbs:
            func(nb)
            print(('Finished %s' % nb))