def secure_hash_s(data, hash_func=sha1):
    ' Return a secure hash hex digest of data. '
    digest = hash_func()
    data = to_bytes(data, errors='strict')
    digest.update(data)
    return digest.hexdigest()