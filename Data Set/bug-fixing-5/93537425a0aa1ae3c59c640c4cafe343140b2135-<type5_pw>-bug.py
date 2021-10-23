def type5_pw(password, salt=None):
    if (not HAS_PASSLIB):
        raise AnsibleFilterError('type5_pw filter requires PassLib library to be installed')
    if (not isinstance(password, string_types)):
        raise AnsibleFilterError(('type5_pw password input should be a string, but was given a input of %s' % type(password).__name__))
    salt_chars = ansible_password._gen_candidate_chars(['ascii_letters', 'digits', './'])
    if ((salt is not None) and (not isinstance(salt, string_types))):
        raise AnsibleFilterError(('type5_pw salt input should be a string, but was given a input of %s' % type(salt).__name__))
    elif (not salt):
        salt = random_password(length=4, chars=salt_chars)
    elif (not (set(salt) <= set(salt_chars))):
        raise AnsibleFilterError(('type5_pw salt used inproper characters, must be one of %s' % salt_chars))
    encrypted_password = md5_crypt.encrypt(password, salt=salt)
    return encrypted_password