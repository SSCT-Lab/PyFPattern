def call(self, call_type, fail_onerr=True):
    ' Helper function to perform gconftool-2 operations '
    config_source = ''
    direct = ''
    changed = False
    out = ''
    if ((self.config_source is not None) and (len(self.config_source) > 0)):
        config_source = ('--config-source ' + self.config_source)
    if self.direct:
        direct = '--direct'
    cmd = 'gconftool-2 '
    try:
        if (call_type == 'get'):
            cmd += '--get {0}'.format(self.key)
        elif (call_type == 'set'):
            cmd += '{0} {1} --type {2} --{3} {4} "{5}"'.format(direct, config_source, self.value_type, call_type, self.key, self.value)
        elif (call_type == 'unset'):
            cmd += '--unset {0}'.format(self.key)
        process = Popen([cmd], stdout=PIPE, stderr=PIPE, shell=True)
        out = process.stdout.read()
        err = process.stderr.read()
        if (len(err) > 0):
            if fail_onerr:
                self.ansible.fail_json(msg=('gconftool-2 failed with error: %s' % str(err)))
        else:
            changed = True
    except OSError:
        exception = get_exception()
        self.ansible.fail_json(msg=('gconftool-2 failed with exception: %s' % exception))
    return (changed, out.rstrip())