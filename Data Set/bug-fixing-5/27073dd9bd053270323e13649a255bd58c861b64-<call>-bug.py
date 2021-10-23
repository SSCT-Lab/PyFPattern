def call(self, call_type):
    config_source = ''
    direct = ''
    changed = False
    out = ''
    if ((self.config_source is not None) and (len(self.config_source) > 0)):
        config_source = ('--config-source ' + self.config_source)
    if self.direct:
        direct = '--direct'
    try:
        if (call_type == 'get'):
            process = subprocess.Popen([('gconftool-2 --get ' + self.key)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        else:
            process = subprocess.Popen([((((((((((('gconftool-2 ' + direct) + ' ') + config_source) + ' --type ') + self.value_type) + ' --') + call_type) + ' ') + self.key) + ' ') + self.value)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out = process.stdout.read()
        err = process.stderr.read()
        if (len(err) > 0):
            self.ansible.fail_json(msg=('gconftool-2 failed with error: %s' % str(err)))
        else:
            changed = True
    except OSError:
        self.ansible.fail_json(msg='gconftool-2 failed with and exception')
    return (changed, out.rstrip())