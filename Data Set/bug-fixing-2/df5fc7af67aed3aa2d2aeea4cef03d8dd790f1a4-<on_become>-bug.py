

def on_become(self, passwd=None):
    if self._get_prompt().endswith(b'#'):
        return
    cmd = {
        'command': 'enable',
    }
    if passwd:
        cmd['prompt'] = to_text('[\\r\\n]password: $', errors='surrogate_or_strict')
        cmd['answer'] = passwd
        cmd['prompt_retry_check'] = True
    try:
        self._exec_cli_command(to_bytes(json.dumps(cmd), errors='surrogate_or_strict'))
        prompt = self._get_prompt()
        if ((prompt is None) or (not prompt.endswith(b'#'))):
            raise AnsibleConnectionFailure(('failed to elevate privilege to enable mode still at prompt [%s]' % prompt))
    except AnsibleConnectionFailure as e:
        prompt = self._get_prompt()
        raise AnsibleConnectionFailure(('unable to elevate privilege to enable mode, at prompt [%s] with error: %s' % (prompt, e.message)))
