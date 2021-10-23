def _get_program_spec_program_path_and_arguments(self, cmd):
    if self.windowsGuest:
        cmd_parts = self._shell._encode_script(cmd, as_list=False, strict_mode=False, preserve_rc=False)
        program_path = 'cmd.exe'
        arguments = ('/c %s' % cmd_parts)
    else:
        program_path = self.get_option('executable')
        arguments = re.sub(('^%s\\s*' % program_path), '', cmd)
    return (program_path, arguments)