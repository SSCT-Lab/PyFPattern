def _parse_account_key(self, key):
    '\n        Parses an RSA key file in PEM format and returns the modulus\n        and public exponent of the key\n        '
    openssl_keydump_cmd = [self._openssl_bin, 'rsa', '-in', key, '-noout', '-text']
    (_, out, _) = self.module.run_command(openssl_keydump_cmd, check_rc=True)
    (pub_hex, pub_exp) = re.search('modulus:\\n\\s+00:([a-f0-9\\:\\s]+?)\\npublicExponent: ([0-9]+)', out.decode('utf8'), (re.MULTILINE | re.DOTALL)).groups()
    pub_exp = '{0:x}'.format(int(pub_exp))
    if (len(pub_exp) % 2):
        pub_exp = '0{0}'.format(pub_exp)
    return (pub_hex, pub_exp)