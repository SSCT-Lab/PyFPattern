

def fetch_file(self, in_path, out_path):
    super(Connection, self).fetch_file(in_path, out_path)
    in_path = self._shell._unquote(in_path)
    out_path = out_path.replace('\\', '/')
    display.vvv(('FETCH "%s" TO "%s"' % (in_path, out_path)), host=self._winrm_host)
    buffer_size = (2 ** 19)
    makedirs_safe(os.path.dirname(out_path))
    out_file = None
    try:
        offset = 0
        while True:
            try:
                script = ('\n                        $path = "%(path)s"\n                        If (Test-Path -Path $path -PathType Leaf)\n                        {\n                            $buffer_size = %(buffer_size)d\n                            $offset = %(offset)d\n\n                            $stream = New-Object -TypeName IO.FileStream($path, [IO.FileMode]::Open, [IO.FileAccess]::Read, [IO.FileShare]::ReadWrite)\n                            $stream.Seek($offset, [System.IO.SeekOrigin]::Begin) > $null\n                            $buffer = New-Object -TypeName byte[] $buffer_size\n                            $bytes_read = $stream.Read($buffer, 0, $buffer_size)\n                            if ($bytes_read -gt 0) {\n                                $bytes = $buffer[0..($bytes_read - 1)]\n                                [System.Convert]::ToBase64String($bytes)\n                            }\n                            $stream.Close() > $null\n                        }\n                        ElseIf (Test-Path -Path $path -PathType Container)\n                        {\n                            Write-Host "[DIR]";\n                        }\n                        Else\n                        {\n                            Write-Error "$path does not exist";\n                            Exit 1;\n                        }\n                    ' % dict(buffer_size=buffer_size, path=self._shell._escape(in_path), offset=offset))
                display.vvvvv(('WINRM FETCH "%s" to "%s" (offset=%d)' % (in_path, out_path, offset)), host=self._winrm_host)
                cmd_parts = self._shell._encode_script(script, as_list=True, preserve_rc=False)
                result = self._winrm_exec(cmd_parts[0], cmd_parts[1:])
                if (result.status_code != 0):
                    raise IOError(to_native(result.std_err))
                if (result.std_out.strip() == '[DIR]'):
                    data = None
                else:
                    data = base64.b64decode(result.std_out.strip())
                if (data is None):
                    makedirs_safe(out_path)
                    break
                else:
                    if (not out_file):
                        if os.path.isdir(to_bytes(out_path, errors='surrogate_or_strict')):
                            break
                        out_file = open(to_bytes(out_path, errors='surrogate_or_strict'), 'wb')
                    out_file.write(data)
                    if (len(data) < buffer_size):
                        break
                    offset += len(data)
            except Exception:
                traceback.print_exc()
                raise AnsibleError(('failed to transfer file to "%s"' % out_path))
    finally:
        if out_file:
            out_file.close()
