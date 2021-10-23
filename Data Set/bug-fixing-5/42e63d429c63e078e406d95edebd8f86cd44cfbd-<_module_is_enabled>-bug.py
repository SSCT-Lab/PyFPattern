def _module_is_enabled(module):
    control_binary = _get_ctl_binary(module)
    name = module.params['name']
    ignore_configcheck = module.params['ignore_configcheck']
    (result, stdout, stderr) = module.run_command(('%s -M' % control_binary))
    '\n    Work around for Ubuntu Xenial listing php7_module as php7.0\n    '
    if (name == 'php7.0'):
        name = 'php7'
    if (result != 0):
        error_msg = ('Error executing %s: %s' % (control_binary, stderr))
        if ignore_configcheck:
            if (('AH00534' in stderr) and ('mpm_' in name)):
                module.warnings.append('No MPM module loaded! apache2 reload AND other module actions will fail if no MPM module is loaded immediatly.')
            else:
                module.warnings.append(error_msg)
            return False
        else:
            module.fail_json(msg=error_msg)
    return bool(re.search(((' ' + name) + '_module'), stdout))