def _handle_existing_file(self, conn, source, dest, proto, timeout):
    cwd = self._loader.get_basedir()
    filename = str(uuid.uuid4())
    source_file = os.path.join(cwd, filename)
    try:
        out = conn.get_file(source=dest, destination=source_file, proto=proto, timeout=timeout)
    except Exception as exc:
        pattern = to_text(exc)
        not_found_exc = 'No such file or directory'
        if re.search(not_found_exc, pattern, re.I):
            if os.path.exists(source_file):
                os.remove(source_file)
            return True
        else:
            try:
                os.remove(source_file)
            except OSError as osex:
                raise Exception(osex)
    try:
        with open(source, 'r') as f:
            new_content = f.read()
        with open(source_file, 'r') as f:
            old_content = f.read()
    except (IOError, OSError) as ioexc:
        os.remove(source_file)
        raise IOError(ioexc)
    sha1 = hashlib.sha1()
    old_content_b = to_bytes(old_content, errors='surrogate_or_strict')
    sha1.update(old_content_b)
    checksum_old = sha1.digest()
    sha1 = hashlib.sha1()
    new_content_b = to_bytes(new_content, errors='surrogate_or_strict')
    sha1.update(new_content_b)
    checksum_new = sha1.digest()
    os.remove(source_file)
    if (checksum_old == checksum_new):
        return False
    else:
        return True