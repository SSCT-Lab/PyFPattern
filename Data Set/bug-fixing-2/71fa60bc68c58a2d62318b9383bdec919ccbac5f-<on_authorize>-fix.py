

def on_authorize(self, passwd=None):
    if self._get_prompt().strip().endswith(b'#'):
        return
    cmd = {
        'command': 'enable',
    }
    if passwd:
        cmd['prompt'] = to_text('[\\r\\n]?password: $', errors='surrogate_or_strict')
        cmd['answer'] = passwd
    try:
        self._exec_cli_command(to_bytes(json.dumps(cmd), errors='surrogate_or_strict'))
    except AnsibleConnectionFailure:
        raise AnsibleConnectionFailure('unable to elevate privilege to enable mode')
    self.disable_pager()
