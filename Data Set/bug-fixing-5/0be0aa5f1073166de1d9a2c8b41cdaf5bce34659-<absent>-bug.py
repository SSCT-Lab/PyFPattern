def absent(dest, username, check_mode):
    ' Ensures user is absent\n\n    Returns (msg, changed) '
    if (StrictVersion(passlib.__version__) >= StrictVersion('1.6')):
        ht = HtpasswdFile(dest, new=False)
    else:
        ht = HtpasswdFile(dest)
    if (username not in ht.users()):
        return (('%s not present' % username), False)
    else:
        if (not check_mode):
            ht.delete(username)
            ht.save()
        return (('Remove %s' % username), True)