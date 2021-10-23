def _download_url_to_file(url, dst, hash_prefix, progress):
    u = urlopen(url)
    if requests_available:
        file_size = int(u.headers['Content-Length'])
        u = u.raw
    else:
        meta = u.info()
        if hasattr(meta, 'getheaders'):
            file_size = int(meta.getheaders('Content-Length')[0])
        else:
            file_size = int(meta.get_all('Content-Length')[0])
    f = tempfile.NamedTemporaryFile(delete=False)
    try:
        sha256 = hashlib.sha256()
        with tqdm(total=file_size, disable=(not progress)) as pbar:
            while True:
                buffer = u.read(8192)
                if (len(buffer) == 0):
                    break
                f.write(buffer)
                sha256.update(buffer)
                pbar.update(len(buffer))
        f.close()
        digest = sha256.hexdigest()
        if (digest[:len(hash_prefix)] != hash_prefix):
            raise RuntimeError('invalid hash value (expected "{}", got "{}")'.format(hash_prefix, digest))
        shutil.move(f.name, dst)
    finally:
        f.close()
        if os.path.exists(f.name):
            os.remove(f.name)