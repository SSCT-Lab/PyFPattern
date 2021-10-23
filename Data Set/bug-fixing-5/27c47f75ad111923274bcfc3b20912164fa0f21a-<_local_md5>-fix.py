def _local_md5(self, file):
    md5 = hashlib.md5()
    with io.open(file, 'rb') as f:
        for chunk in iter((lambda : f.read(8192)), ''):
            md5.update(chunk)
    return md5.hexdigest()