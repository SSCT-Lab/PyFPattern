@enable_mode
def get_config(self, source='running', format='text', flags=None):
    lookup = {
        'running': 'running-config',
        'startup': 'startup-config',
    }
    if (source not in lookup):
        return self.invalid_params(('fetching configuration from %s is not supported' % source))
    if (format == 'text'):
        cmd = (b'show %s ' % lookup[source])
    else:
        cmd = (b'show %s | %s' % (lookup[source], format))
    flags = ([] if (flags is None) else flags)
    cmd += ' '.join(flags)
    cmd = cmd.strip()
    return self.send_command(cmd)