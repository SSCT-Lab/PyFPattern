

def run_subscription_manager(module, arguments):
    rhsm_bin = module.get_bin_path('subscription-manager')
    if (not rhsm_bin):
        module.fail_json(msg='The executable file subscription-manager was not found in PATH')
    lang_env = dict(LANG='C', LC_ALL='C', LC_MESSAGES='C')
    (rc, out, err) = module.run_command(('%s %s' % (rhsm_bin, ' '.join(arguments))), environ_update=lang_env)
    if ((rc == 1) and ((err == 'The password you typed is invalid.\nPlease try again.\n') or (os.getuid() != 0))):
        module.fail_json(msg='The executable file subscription-manager must be run using root privileges')
    elif ((rc == 0) and (out == 'This system has no repositories available through subscriptions.\n')):
        module.fail_json(msg='This system has no repositories available through subscriptions')
    elif (rc == 1):
        module.fail_json(msg=('subscription-manager failed with the following error: %s' % err))
    else:
        return (rc, out, err)
