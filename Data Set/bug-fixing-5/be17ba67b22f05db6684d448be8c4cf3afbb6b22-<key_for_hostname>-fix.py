def key_for_hostname(hostname):
    if (not KEYCZAR_AVAILABLE):
        raise AnsibleError('python-keyczar must be installed on the control machine to use accelerated modes')
    key_path = os.path.expanduser(C.ACCELERATE_KEYS_DIR)
    if (not os.path.exists(key_path)):
        with _LOCK:
            if (not os.path.exists(key_path)):
                tmp_dir = tempfile.mkdtemp(dir=os.path.dirname(key_path))
                os.chmod(tmp_dir, int(C.ACCELERATE_KEYS_DIR_PERMS, 8))
                os.rename(tmp_dir, key_path)
    elif (not os.path.isdir(key_path)):
        raise AnsibleError('ACCELERATE_KEYS_DIR is not a directory.')
    if (stat.S_IMODE(os.stat(key_path).st_mode) != int(C.ACCELERATE_KEYS_DIR_PERMS, 8)):
        raise AnsibleError(('Incorrect permissions on the private key directory. Use `chmod 0%o %s` to correct this issue, and make sure any of the keys files contained within that directory are set to 0%o' % (int(C.ACCELERATE_KEYS_DIR_PERMS, 8), C.ACCELERATE_KEYS_DIR, int(C.ACCELERATE_KEYS_FILE_PERMS, 8))))
    key_path = os.path.join(key_path, hostname)
    if ((not os.path.exists(key_path)) or ((time.time() - os.path.getmtime(key_path)) > ((60 * 60) * 2))):
        with _LOCK:
            if ((not os.path.exists(key_path)) or ((time.time() - os.path.getmtime(key_path)) > ((60 * 60) * 2))):
                key = AesKey.Generate()
                with tempfile.NamedTemporaryFile(mode='w', dir=os.path.dirname(key_path), delete=False) as fh:
                    tmp_key_path = fh.name
                    fh.write(str(key))
                os.chmod(tmp_key_path, int(C.ACCELERATE_KEYS_FILE_PERMS, 8))
                os.rename(tmp_key_path, key_path)
                return key
    if (stat.S_IMODE(os.stat(key_path).st_mode) != int(C.ACCELERATE_KEYS_FILE_PERMS, 8)):
        raise AnsibleError(('Incorrect permissions on the key file for this host. Use `chmod 0%o %s` to correct this issue.' % (int(C.ACCELERATE_KEYS_FILE_PERMS, 8), key_path)))
    fh = open(key_path)
    key = AesKey.Read(fh.read())
    fh.close()
    return key