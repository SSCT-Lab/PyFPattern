def is_pubkey(string):
    'Verifies if string is a pubkey'
    pgp_regex = '.*?(-----BEGIN PGP PUBLIC KEY BLOCK-----.*?-----END PGP PUBLIC KEY BLOCK-----).*'
    return bool(re.match(pgp_regex, to_native(string, errors='surrogate_or_strict'), re.DOTALL))