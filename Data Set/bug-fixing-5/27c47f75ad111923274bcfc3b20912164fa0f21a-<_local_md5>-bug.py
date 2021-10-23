def _local_md5(self, file):
    md5 = hashlib.md5()
    f = open(file, 'rb')
    for chunk in iter((lambda : f.read(8192)), ''):
        md5.update(chunk)
    f.close()
    return md5.hexdigest()