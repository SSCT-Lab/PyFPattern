def exec_command_old(self, cmd, in_data=None, sudoable=True):
    super(Connection, self).exec_command(cmd, in_data=in_data, sudoable=sudoable)
    cmd_parts = shlex.split(to_bytes(cmd), posix=False)
    cmd_parts = map(to_text, cmd_parts)
    script = None
    cmd_ext = ((cmd_parts and self._shell._unquote(cmd_parts[0]).lower()[(- 4):]) or '')
    if (cmd_ext == '.ps1'):
        script = ('& %s' % cmd)
    elif (cmd_ext in ('.bat', '.cmd')):
        script = ('[System.Console]::OutputEncoding = [System.Text.Encoding]::Default; & %s' % cmd)
    elif ('-EncodedCommand' not in cmd_parts):
        script = cmd
    if script:
        cmd_parts = self._shell._encode_script(script, as_list=True, strict_mode=False)
    if ('-EncodedCommand' in cmd_parts):
        encoded_cmd = cmd_parts[(cmd_parts.index('-EncodedCommand') + 1)]
        decoded_cmd = to_text(base64.b64decode(encoded_cmd).decode('utf-16-le'))
        display.vvv(('EXEC %s' % decoded_cmd), host=self._winrm_host)
    else:
        display.vvv(('EXEC %s' % cmd), host=self._winrm_host)
    try:
        result = self._winrm_exec(cmd_parts[0], cmd_parts[1:], from_exec=True)
    except Exception:
        traceback.print_exc()
        raise AnsibleConnectionFailure(('failed to exec cmd %s' % to_native(cmd)))
    result.std_out = to_bytes(result.std_out)
    result.std_err = to_bytes(result.std_err)
    if self.is_clixml(result.std_err):
        try:
            result.std_err = self.parse_clixml_stream(result.std_err)
        except Exception:
            pass
    return (result.status_code, result.std_out, result.std_err)