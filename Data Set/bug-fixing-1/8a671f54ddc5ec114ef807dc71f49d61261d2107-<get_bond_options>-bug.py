

def get_bond_options(mode, usr_opts):
    MIIMON_100 = dict(miimon='100')
    DEFAULT_MODE_OPTS = {
        '1': MIIMON_100,
        '2': MIIMON_100,
        '3': MIIMON_100,
        '4': dict(xmit_hash_policy='2', **MIIMON_100),
    }
    options = []
    if (mode is None):
        return options

    def get_type_name(mode_number):
        '\n        We need to maintain this type strings, for the __compare_options method,\n        for easier comparision.\n        '
        modes = ['Active-Backup', 'Load balance (balance-xor)', None, 'Dynamic link aggregation (802.3ad)']
        if (not (0 < mode_number <= (len(modes) - 1))):
            return None
        return modes[(mode_number - 1)]
    try:
        mode_number = int(mode)
    except ValueError:
        raise Exception('Bond mode must be a number.')
    options.append(otypes.Option(name='mode', type=get_type_name(mode_number), value=str(mode_number)))
    opts_dict = DEFAULT_MODE_OPTS.get(mode, {
        
    })
    opts_dict.update(**usr_opts)
    options.extend([otypes.Option(name=opt, value=value) for (opt, value) in six.iteritems(opts_dict)])
    return options
