def get_ssh_key_fingerprint(ssh_key):
    '\n    Return the public key fingerprint of a given public SSH key\n    in format "FB:0C:AC:0A:07:94:5B:CE:75:6E:63:32:13:AD:AD:D7 [user@host] (ssh-rsa)"\n    :param ssh_key:\n    :return:\n    '
    parts = ssh_key.strip().split()
    if (len(parts) == 0):
        return None
    key_type = parts[0]
    key = base64.b64decode(parts[1].encode('ascii'))
    fp_plain = hashlib.md5(key).hexdigest()
    key_fp = ':'.join(((a + b) for (a, b) in zip(fp_plain[::2], fp_plain[1::2]))).upper()
    if (len(parts) < 3):
        return ('%s (%s)' % (key_fp, key_type))
    else:
        user_host = parts[2]
        return ('%s %s (%s)' % (key_fp, user_host, key_type))