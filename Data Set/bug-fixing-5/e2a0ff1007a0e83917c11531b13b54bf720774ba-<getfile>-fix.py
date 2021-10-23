def getfile(self, releasefile):
    cutoff = options.get('releasefile.cache-limit')
    file_size = releasefile.file.size
    if (file_size < cutoff):
        metrics.timing('release_file.cache.get.size', file_size, tags={
            'cutoff': True,
        })
        return releasefile.file.getfile()
    file_id = six.text_type(releasefile.file_id)
    organization_id = six.text_type(releasefile.organization_id)
    file_path = os.path.join(self.cache_path, organization_id, file_id)
    hit = True
    try:
        os.stat(file_path)
    except OSError as e:
        if (e.errno != errno.ENOENT):
            raise
        releasefile.file.save_to(file_path)
        hit = False
    metrics.timing('release_file.cache.get.size', file_size, tags={
        'hit': hit,
        'cutoff': False,
    })
    return open(file_path, 'rb')