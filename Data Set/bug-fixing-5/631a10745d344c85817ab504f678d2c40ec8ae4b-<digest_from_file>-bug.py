def digest_from_file(self, filename, algorithm):
    ' Return hex digest of local file for a digest_method specified by name, or None if file is not present. '
    if (not os.path.exists(filename)):
        return None
    if os.path.isdir(filename):
        self.fail_json(msg=('attempted to take checksum of directory: %s' % filename))
    if hasattr(algorithm, 'hexdigest'):
        digest_method = algorithm
    else:
        try:
            digest_method = AVAILABLE_HASH_ALGORITHMS[algorithm]()
        except KeyError:
            self.fail_json(msg=("Could not hash file '%s' with algorithm '%s'. Available algorithms: %s" % (filename, algorithm, ', '.join(AVAILABLE_HASH_ALGORITHMS))))
    blocksize = (64 * 1024)
    infile = open(filename, 'rb')
    block = infile.read(blocksize)
    while block:
        digest_method.update(block)
        block = infile.read(blocksize)
    infile.close()
    return digest_method.hexdigest()