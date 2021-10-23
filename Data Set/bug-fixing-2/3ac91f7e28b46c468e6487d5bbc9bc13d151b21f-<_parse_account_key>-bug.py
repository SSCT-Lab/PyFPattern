

def _parse_account_key(self, key):
    '\n        Parses an RSA or Elliptic Curve key file in PEM format and returns a pair\n        (error, key_data).\n        '
    account_key_type = None
    with open(key, 'rt') as f:
        for line in f:
            m = re.match('^\\s*-{5,}BEGIN\\s+(EC|RSA)\\s+PRIVATE\\s+KEY-{5,}\\s*$', line)
            if (m is not None):
                account_key_type = m.group(1).lower()
                break
    if (account_key_type is None):
        account_key_type = 'rsa'
    if (account_key_type not in ('rsa', 'ec')):
        return (('unknown key type "%s"' % account_key_type), {
            
        })
    openssl_keydump_cmd = [self._openssl_bin, account_key_type, '-in', key, '-noout', '-text']
    (dummy, out, dummy) = self.module.run_command(openssl_keydump_cmd, check_rc=True)
    if (account_key_type == 'rsa'):
        (pub_hex, pub_exp) = re.search('modulus:\\n\\s+00:([a-f0-9\\:\\s]+?)\\npublicExponent: ([0-9]+)', to_text(out, errors='surrogate_or_strict'), (re.MULTILINE | re.DOTALL)).groups()
        pub_exp = '{0:x}'.format(int(pub_exp))
        if (len(pub_exp) % 2):
            pub_exp = '0{0}'.format(pub_exp)
        return (None, {
            'type': 'rsa',
            'alg': 'RS256',
            'jwk': {
                'kty': 'RSA',
                'e': nopad_b64(binascii.unhexlify(pub_exp.encode('utf-8'))),
                'n': nopad_b64(binascii.unhexlify(re.sub('(\\s|:)', '', pub_hex).encode('utf-8'))),
            },
            'hash': 'sha256',
        })
    elif (account_key_type == 'ec'):
        pub_data = re.search('pub:\\s*\\n\\s+04:([a-f0-9\\:\\s]+?)\\nASN1 OID: (\\S+)\\nNIST CURVE: (\\S+)', to_text(out, errors='surrogate_or_strict'), (re.MULTILINE | re.DOTALL))
        if (pub_data is None):
            return ('cannot parse elliptic curve key', {
                
            })
        pub_hex = binascii.unhexlify(re.sub('(\\s|:)', '', pub_data.group(1)).encode('utf-8'))
        curve = pub_data.group(3).lower()
        if (curve == 'p-256'):
            bits = 256
            alg = 'ES256'
            hash = 'sha256'
            point_size = 32
        elif (curve == 'p-384'):
            bits = 384
            alg = 'ES384'
            hash = 'sha384'
            point_size = 48
        elif (curve == 'p-521'):
            bits = 521
            alg = 'ES512'
            hash = 'sha512'
            point_size = 66
        else:
            return (('unknown elliptic curve: %s' % curve), {
                
            })
        bytes = ((bits + 7) // 8)
        if (len(pub_hex) != (2 * bytes)):
            return (('bad elliptic curve point (%s)' % curve), {
                
            })
        return (None, {
            'type': 'ec',
            'alg': alg,
            'jwk': {
                'kty': 'EC',
                'crv': curve.upper(),
                'x': nopad_b64(pub_hex[:bytes]),
                'y': nopad_b64(pub_hex[bytes:]),
            },
            'hash': hash,
            'point_size': point_size,
        })
