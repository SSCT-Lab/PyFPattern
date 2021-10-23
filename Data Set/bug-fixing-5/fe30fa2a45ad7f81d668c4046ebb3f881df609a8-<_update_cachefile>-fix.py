def _update_cachefile(self, debug_file, tf):
    try:
        fo = FatObject.from_path(tf.name)
        o = fo.get_object(id=debug_file.debug_id)
        if (o is None):
            return (None, None)
        symcache = o.make_symcache()
    except SymbolicError as e:
        default_cache.set(('scbe:%s:%s' % (debug_file.debug_id, debug_file.file.checksum)), e.message, CONVERSION_ERROR_TTL)
        if (not isinstance(e, (SymCacheErrorMissingDebugSection, SymCacheErrorMissingDebugInfo))):
            logger.error('dsymfile.symcache-build-error', exc_info=True, extra=dict(debug_id=debug_file.debug_id))
        return (None, e.message)
    for iteration in range(5):
        file = File.objects.create(name=debug_file.debug_id, type='project.symcache')
        file.putfile(symcache.open_stream())
        try:
            with transaction.atomic():
                return (ProjectSymCacheFile.objects.get_or_create(project=debug_file.project, cache_file=file, dsym_file=debug_file, defaults=dict(checksum=debug_file.file.checksum, version=symcache.file_format_version))[0], None)
        except IntegrityError:
            file.delete()
            try:
                return (ProjectSymCacheFile.objects.get(project=debug_file.project, dsym_file=debug_file), None)
            except ProjectSymCacheFile.DoesNotExist:
                continue
    raise RuntimeError('Concurrency error on symcache update')