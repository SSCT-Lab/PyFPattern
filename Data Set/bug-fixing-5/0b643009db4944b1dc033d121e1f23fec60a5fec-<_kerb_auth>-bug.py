def _kerb_auth(self, principal, password):
    if (password is None):
        password = ''
    self._kerb_ccache = tempfile.NamedTemporaryFile()
    display.vvvvv(('creating Kerberos CC at %s' % self._kerb_ccache.name))
    krb5ccname = ('FILE:%s' % self._kerb_ccache.name)
    os.environ['KRB5CCNAME'] = krb5ccname
    krb5env = dict(KRB5CCNAME=krb5ccname)
    kinit_flags = []
    if boolean(self.get_option('_extras').get('ansible_winrm_kerberos_delegation', False)):
        kinit_flags.append('-f')
    kinit_cmdline = [self._kinit_cmd]
    kinit_cmdline.extend(kinit_flags)
    kinit_cmdline.append(principal)
    if HAS_PEXPECT:
        kinit_cmdline = ' '.join(kinit_cmdline)
        password = to_text(password, encoding='utf-8', errors='surrogate_or_strict')
        display.vvvv(('calling kinit with pexpect for principal %s' % principal))
        events = {
            '.*:': (password + '\n'),
        }
        (stderr, rc) = pexpect.run(kinit_cmdline, withexitstatus=True, events=events, env=krb5env, timeout=60)
    else:
        password = to_bytes(password, encoding='utf-8', errors='surrogate_or_strict')
        display.vvvv(('calling kinit with subprocess for principal %s' % principal))
        p = subprocess.Popen(kinit_cmdline, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=krb5env)
        (stdout, stderr) = p.communicate((password + b'\n'))
        rc = (p.returncode != 0)
    if (rc != 0):
        raise AnsibleConnectionFailure(('Kerberos auth failure: %s' % stderr.strip()))
    display.vvvvv(('kinit succeeded for principal %s' % principal))