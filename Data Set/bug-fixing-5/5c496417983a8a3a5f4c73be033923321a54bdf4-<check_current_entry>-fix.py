def check_current_entry(module):
    existsdict = {
        'exist': False,
    }
    lsitab = module.get_bin_path('lsitab')
    (rc, out, err) = module.run_command([lsitab, module.params['name']])
    if (rc == 0):
        keys = ('name', 'runlevel', 'action', 'command')
        values = out.split(':')
        values = map((lambda s: s.strip()), values)
        existsdict = dict(izip(keys, values))
        existsdict.update({
            'exist': True,
        })
    return existsdict