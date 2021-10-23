def exec_command(self, cmd, in_data=None, sudoable=True):
    if self._ssh_shell:
        try:
            cmd = json.loads(to_text(cmd, errors='surrogate_or_strict'))
            kwargs = {
                'command': to_bytes(cmd['command'], errors='surrogate_or_strict'),
            }
            for key in ('prompt', 'answer', 'send_only'):
                if (key in cmd):
                    kwargs[key] = to_bytes(cmd[key], errors='surrogate_or_strict')
            return self.send(**kwargs)
        except ValueError:
            cmd = to_bytes(cmd, errors='surrogate_or_strict')
            return self.send(command=cmd)
    else:
        return self._local.exec_command(cmd, in_data, sudoable)