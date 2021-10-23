def test_keytool(module, executable):
    ' Test if keytool is actuall executable or not '
    test_cmd = ('%s' % executable)
    module.run_command(test_cmd, check_rc=True)