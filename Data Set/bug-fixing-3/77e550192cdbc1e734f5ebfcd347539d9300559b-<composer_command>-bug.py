def composer_command(module, command, arguments='', options=[]):
    php_path = module.get_bin_path('php', True, ['/usr/local/bin'])
    composer_path = module.get_bin_path('composer', True, ['/usr/local/bin'])
    cmd = ('%s %s %s %s %s' % (php_path, composer_path, command, ' '.join(options), arguments))
    return module.run_command(cmd)