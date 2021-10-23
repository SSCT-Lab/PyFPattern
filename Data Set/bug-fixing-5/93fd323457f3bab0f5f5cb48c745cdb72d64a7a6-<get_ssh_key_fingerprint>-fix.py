def get_ssh_key_fingerprint(ssh_key, hash_algo='sha256'):
    '\n    Return the public key fingerprint of a given public SSH key\n    in format "[fp] [user@host] (ssh-rsa)" where fp is of the format:\n    FB:0C:AC:0A:07:94:5B:CE:75:6E:63:32:13:AD:AD:D7\n    for md5 or\n    SHA256:[base64]\n    for sha256\n    :param ssh_key:\n    :param hash_algo:\n    :return:\n    '
    parts = ssh_key.strip().split()
    if (len(parts) == 0):
        return None
    key_type = parts[0]
    key = base64.b64decode(parts[1].encode('ascii'))
    if (hash_algo == 'md5'):
        fp_plain = hashlib.md5(key).hexdigest()
        key_fp = ':'.join(((a + b) for (a, b) in zip(fp_plain[::2], fp_plain[1::2]))).upper()
    elif (hash_algo == 'sha256'):
        fp_plain = base64.b64encode(hashlib.sha256(key).digest()).decode('ascii').rstrip('=')
        key_fp = 'SHA256:{fp}'.format(fp=fp_plain)
    if (len(parts) < 3):
        return ('%s (%s)' % (key_fp, key_type))
    else:
        user_host = parts[2]
        return ('%s %s (%s)' % (key_fp, user_host, key_type))