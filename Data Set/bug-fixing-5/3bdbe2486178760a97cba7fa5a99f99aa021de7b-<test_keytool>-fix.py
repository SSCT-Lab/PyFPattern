def test_keytool(module, executable):
    ' Test if keytool is actually executable or not '
    module.run_command(('%s' % executable), check_rc=True)