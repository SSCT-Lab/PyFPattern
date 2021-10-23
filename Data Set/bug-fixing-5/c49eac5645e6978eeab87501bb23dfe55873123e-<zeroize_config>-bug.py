def zeroize_config(module, result):
    if (not module.check_mode):
        module.cli.run_commands('request system zeroize')
    result['changed'] = True