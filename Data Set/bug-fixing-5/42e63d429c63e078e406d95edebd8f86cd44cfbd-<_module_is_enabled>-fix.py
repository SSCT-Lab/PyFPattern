def _module_is_enabled(module):
    control_binary = _get_ctl_binary(module)
    name = module.params['name']
    ignore_configcheck = module.params['ignore_configcheck']
    (result, stdout, stderr) = module.run_command(('%s -M' % control_binary))
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
    '\n    Work around for php modules; php7.x are always listed as php7_module\n    '
    php_module = re.search('^(php\\d)\\.', name)
    if php_module:
        name = php_module.group(1)
    '\n    Workaround for shib2; module is listed as mod_shib\n    '
    if re.search('shib2', name):
        return bool(re.search(' mod_shib', stdout))
    return bool(re.search(((' ' + name) + '_module'), stdout))