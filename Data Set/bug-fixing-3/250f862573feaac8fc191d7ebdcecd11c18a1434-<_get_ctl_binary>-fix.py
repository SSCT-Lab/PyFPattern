def _get_ctl_binary(module):
    for command in ['apache2ctl', 'apachectl']:
        ctl_binary = module.get_bin_path(command)
        if (ctl_binary is not None):
            return ctl_binary
    module.fail_json(msg='Neither of apache2ctl nor apachctl found. At least one apache control binary is necessary.')