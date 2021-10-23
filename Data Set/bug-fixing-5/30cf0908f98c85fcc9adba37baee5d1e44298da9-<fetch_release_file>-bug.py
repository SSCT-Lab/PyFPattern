def fetch_release_file(filename, release):
    cache_key = (('releasefile:v1:%s:%s' % (release.id, md5_text(filename).hexdigest())),)
    filename_path = None
    if (filename is not None):
        parsed_url = urlparse(filename)
        filename_path = ('~' + parsed_url.path)
        if parsed_url.query:
            filename_path += ('?' + parsed_url.query)
    logger.debug('Checking cache for release artifact %r (release_id=%s)', filename, release.id)
    result = cache.get(cache_key)
    if (result is None):
        logger.debug('Checking database for release artifact %r (release_id=%s)', filename, release.id)
        filename_idents = [ReleaseFile.get_ident(filename)]
        if ((filename_path is not None) and (filename_path != filename)):
            filename_idents.append(ReleaseFile.get_ident(filename_path))
        possible_files = list(ReleaseFile.objects.filter(release=release, ident__in=filename_idents).select_related('file'))
        if (len(possible_files) == 0):
            logger.debug('Release artifact %r not found in database (release_id=%s)', filename, release.id)
            cache.set(cache_key, (- 1), 60)
            return None
        elif (len(possible_files) == 1):
            releasefile = possible_files[0]
        else:
            target_ident = filename_idents[0]
            releasefile = next((f for f in possible_files if (f.ident == target_ident)))
        logger.debug('Found release artifact %r (id=%s, release_id=%s)', filename, releasefile.id, release.id)
        try:
            with releasefile.file.getfile() as fp:
                (z_body, body) = compress_file(fp)
        except Exception as e:
            logger.exception(six.text_type(e))
            cache.set(cache_key, (- 1), 3600)
            result = None
        else:
            cache.set(cache_key, (releasefile.file.headers, z_body, 200), 3600)
            result = (releasefile.file.headers, body.decode('utf-8'), 200)
    elif (result == (- 1)):
        result = None
    else:
        body = zlib.decompress(result[1])
        result = (result[0], body.decode('utf-8'), result[2])
    return result