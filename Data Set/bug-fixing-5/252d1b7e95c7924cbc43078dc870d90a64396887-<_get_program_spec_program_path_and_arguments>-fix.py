def _get_program_spec_program_path_and_arguments(self, cmd):
    if self.windowsGuest:
        '\n            we need to warp the execution of powershell into a cmd /c because\n            the call otherwise fails with "Authentication or permission failure"\n            #FIXME: Fix the unecessary invocation of cmd and run the command directly\n            '
        program_path = 'cmd.exe'
        arguments = ('/c %s' % cmd)
    else:
        program_path = self.get_option('executable')
        arguments = re.sub(('^%s\\s*' % program_path), '', cmd)
    return (program_path, arguments)