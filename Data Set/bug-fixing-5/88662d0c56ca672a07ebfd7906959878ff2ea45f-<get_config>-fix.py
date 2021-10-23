@enable_mode
def get_config(self, source='running', format='text', flags=None):
    lookup = {
        'running': 'running-config',
        'startup': 'startup-config',
    }
    if (source not in lookup):
        return self.invalid_params(('fetching configuration from %s is not supported' % source))
    cmd = (b'show %s ' % lookup[source])
    if (format and (format is not 'text')):
        cmd += (b'| %s ' % format)
    cmd += ' '.join(to_list(flags))
    cmd = cmd.strip()
    return self.send_command(cmd)