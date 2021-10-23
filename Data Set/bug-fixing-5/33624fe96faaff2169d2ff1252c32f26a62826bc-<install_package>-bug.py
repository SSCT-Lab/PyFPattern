def install_package(module):
    junos = SW(module.connection.device)
    package = module.params['src']
    no_copy = module.params['no_copy']
    progress_log = (lambda x, y: module.log(y))
    module.log('installing package')
    result = junos.install(package, progress=progress_log, no_copy=no_copy)
    if (not result):
        module.fail_json(msg='Unable to install package on device')
    if module.params['reboot']:
        module.log('rebooting system')
        junos.reboot()