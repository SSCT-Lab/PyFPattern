def exec_command(self, cmd, in_data=None, sudoable=True):
    super(Connection, self).exec_command(cmd, in_data=in_data, sudoable=sudoable)
    cmd_parts = self._shell._encode_script(cmd, as_list=True, strict_mode=False, preserve_rc=False)
    display.vvv('EXEC (via pipeline wrapper)')
    stdin_iterator = None
    if in_data:
        stdin_iterator = self._wrapper_payload_stream(in_data)
    result = self._winrm_exec(cmd_parts[0], cmd_parts[1:], from_exec=True, stdin_iterator=stdin_iterator)
    result.std_out = to_bytes(result.std_out)
    result.std_err = to_bytes(result.std_err)
    if self.is_clixml(result.std_err):
        try:
            result.std_err = self.parse_clixml_stream(result.std_err)
        except Exception:
            pass
    return (result.status_code, result.std_out, result.std_err)