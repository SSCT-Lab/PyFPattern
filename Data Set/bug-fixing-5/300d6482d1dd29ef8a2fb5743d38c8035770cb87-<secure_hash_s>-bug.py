def secure_hash_s(data, hash_func=sha1):
    ' Return a secure hash hex digest of data. '
    digest = hash_func()
    try:
        if (not isinstance(data, string_types)):
            data = ('%s' % data)
        digest.update(data)
    except UnicodeEncodeError:
        digest.update(data.encode('utf-8'))
    return digest.hexdigest()