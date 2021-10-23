def _module_is_enabled(module):
    control_binary = _get_ctl_binary(module)
    name = module.params['name']
    (result, stdout, stderr) = module.run_command(('%s -M' % control_binary))
    '\n    Work around for Ubuntu Xenial listing php7_module as php7.0\n    '
    if (name == 'php7.0'):
        name = 'php7'
    if (result != 0):
        module.fail_json(msg=('Error executing %s: %s' % (control_binary, stderr)))
    if re.search(((' ' + name) + '_module'), stdout):
        return True
    else:
        return False