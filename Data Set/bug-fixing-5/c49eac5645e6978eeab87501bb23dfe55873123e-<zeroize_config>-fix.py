def zeroize_config(module, result):
    if (not module.check_mode):
        module.connection.cli('request system zeroize')
    result['changed'] = True