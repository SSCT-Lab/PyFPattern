def is_pubkey(string):
    'Verifies if string is a pubkey'
    pgp_regex = '.*?(-----BEGIN PGP PUBLIC KEY BLOCK-----.*?-----END PGP PUBLIC KEY BLOCK-----).*'
    return re.match(pgp_regex, string, re.DOTALL)