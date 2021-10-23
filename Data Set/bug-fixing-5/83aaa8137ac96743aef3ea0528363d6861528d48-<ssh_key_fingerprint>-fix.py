def ssh_key_fingerprint(ssh_pub_key):
    key = ssh_pub_key.split(None, 2)[1]
    fingerprint = hashlib.md5(base64.b64decode(key)).hexdigest()
    return ':'.join(((a + b) for (a, b) in zip(fingerprint[::2], fingerprint[1::2])))