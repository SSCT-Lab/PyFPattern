def _kerb_auth(self, principal, password):
    if (password is None):
        password = ''
    self._kerb_ccache = tempfile.NamedTemporaryFile()
    display.vvvvv(('creating Kerberos CC at %s' % self._kerb_ccache.name))
    krb5ccname = ('FILE:%s' % self._kerb_ccache.name)
    krbenv = dict(KRB5CCNAME=krb5ccname)
    os.environ['KRB5CCNAME'] = krb5ccname
    kinit_cmdline = [self._kinit_cmd, principal]
    display.vvvvv(('calling kinit for principal %s' % principal))
    p = subprocess.Popen(kinit_cmdline, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=krbenv)
    (stdout, stderr) = p.communicate((password + b'\n'))
    if (p.returncode != 0):
        raise AnsibleConnectionFailure(('Kerberos auth failure: %s' % stderr.strip()))
    display.vvvvv(('kinit succeeded for principal %s' % principal))