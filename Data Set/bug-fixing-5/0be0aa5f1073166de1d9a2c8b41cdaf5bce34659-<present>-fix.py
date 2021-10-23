def present(dest, username, password, crypt_scheme, create, check_mode):
    ' Ensures user is present\n\n    Returns (msg, changed) '
    if (crypt_scheme in apache_hashes):
        context = htpasswd_context
    else:
        context = CryptContext(schemes=([crypt_scheme] + apache_hashes))
    if (not os.path.exists(dest)):
        if (not create):
            raise ValueError(('Destination %s does not exist' % dest))
        if check_mode:
            return (('Create %s' % dest), True)
        create_missing_directories(dest)
        if (LooseVersion(passlib.__version__) >= LooseVersion('1.6')):
            ht = HtpasswdFile(dest, new=True, default_scheme=crypt_scheme, context=context)
        else:
            ht = HtpasswdFile(dest, autoload=False, default=crypt_scheme, context=context)
        if getattr(ht, 'set_password', None):
            ht.set_password(username, password)
        else:
            ht.update(username, password)
        ht.save()
        return (('Created %s and added %s' % (dest, username)), True)
    else:
        if (LooseVersion(passlib.__version__) >= LooseVersion('1.6')):
            ht = HtpasswdFile(dest, new=False, default_scheme=crypt_scheme, context=context)
        else:
            ht = HtpasswdFile(dest, default=crypt_scheme, context=context)
        found = None
        if getattr(ht, 'check_password', None):
            found = ht.check_password(username, password)
        else:
            found = ht.verify(username, password)
        if found:
            return (('%s already present' % username), False)
        else:
            if (not check_mode):
                if getattr(ht, 'set_password', None):
                    ht.set_password(username, password)
                else:
                    ht.update(username, password)
                ht.save()
            return (('Add/update %s' % username), True)