def _get_csr_domains(self):
    '\n        Parse the CSR and return the list of requested domains\n        '
    openssl_csr_cmd = [self._openssl_bin, 'req', '-in', self.csr, '-noout', '-text']
    (_, out, _) = self.module.run_command(openssl_csr_cmd, check_rc=True)
    domains = set([])
    common_name = re.search('Subject:.*? CN\\s?=\\s?([^\\s,;/]+)', out.decode('utf8'))
    if (common_name is not None):
        domains.add(common_name.group(1))
    subject_alt_names = re.search('X509v3 Subject Alternative Name: \\n +([^\\n]+)\\n', out.decode('utf8'), (re.MULTILINE | re.DOTALL))
    if (subject_alt_names is not None):
        for san in subject_alt_names.group(1).split(', '):
            if san.startswith('DNS:'):
                domains.add(san[4:])
    return domains