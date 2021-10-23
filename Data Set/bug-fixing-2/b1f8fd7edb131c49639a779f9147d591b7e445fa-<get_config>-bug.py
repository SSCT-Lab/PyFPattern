

@enable_mode
def get_config(self, source='running', format='text', flags=None):
    if (source not in ('running', 'startup')):
        return self.invalid_params(('fetching configuration from %s is not supported' % source))
    if (source == 'running'):
        cmd = 'show running-config all'
    else:
        cmd = 'show startup-config'
    cmd += ' '.join(to_list(flags))
    cmd = cmd.strip()
    return self.send_command(cmd)
