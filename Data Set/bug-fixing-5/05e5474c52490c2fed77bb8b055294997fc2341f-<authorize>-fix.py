def authorize(self, params, **kwargs):
    passwd = params['auth_pass']
    errors = self.shell.errors
    self.shell.errors = []
    cmd = Command('enable', prompt=self.NET_PASSWD_RE, response=passwd)
    self.execute([cmd, 'no terminal pager'])
    self.shell.errors = errors