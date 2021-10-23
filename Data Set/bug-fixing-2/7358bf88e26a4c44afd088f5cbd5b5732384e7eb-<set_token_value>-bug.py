

def set_token_value(self, token, value):
    if (len(value.split()) > 0):
        value = (('"' + value) + '"')
    if (self.platform == 'openbsd'):
        thiscmd = ('%s %s=%s' % (self.sysctl_cmd, token, value))
    else:
        thiscmd = ('%s -w %s=%s' % (self.sysctl_cmd, token, value))
    (rc, out, err) = self.module.run_command(thiscmd)
    if (rc != 0):
        self.module.fail_json(msg=('setting %s failed: %s' % (token, (out + err))))
    else:
        return rc
