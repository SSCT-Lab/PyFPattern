

def create_dsym_from_id(project, dsym_type, cpu_name, debug_id, basename, fileobj=None, file=None):
    'This creates a mach dsym file or proguard mapping from the given\n    debug id and open file object to a dsym file.  This will not verify the\n    debug id (intentionally so).  Use `create_files_from_dsym_zip` for doing\n    everything.\n    '
    if (dsym_type == 'proguard'):
        object_name = 'proguard-mapping'
    elif (dsym_type in ('macho', 'elf')):
        object_name = basename
    elif (dsym_type == 'breakpad'):
        object_name = (basename[:(- 4)] if basename.endswith('.sym') else basename)
    else:
        raise TypeError(('unknown dsym type %r' % (dsym_type,)))
    if (file is None):
        assert (fileobj is not None), 'missing file object'
        h = hashlib.sha1()
        while 1:
            chunk = fileobj.read(16384)
            if (not chunk):
                break
            h.update(chunk)
        checksum = h.hexdigest()
        fileobj.seek(0, 0)
        try:
            rv = ProjectDSymFile.objects.get(debug_id=debug_id, project=project)
            if (rv.file.checksum == checksum):
                return (rv, False)
        except ProjectDSymFile.DoesNotExist:
            rv = None
        file = File.objects.create(name=debug_id, type='project.dsym', headers={
            'Content-Type': DSYM_MIMETYPES[dsym_type],
        })
        file.putfile(fileobj)
        kwargs = {
            'file': file,
            'debug_id': debug_id,
            'cpu_name': cpu_name,
            'object_name': object_name,
            'project': project,
        }
        if (rv is None):
            try:
                with transaction.atomic():
                    rv = ProjectDSymFile.objects.create(**kwargs)
            except IntegrityError:
                rv = ProjectDSymFile.objects.get(debug_id=debug_id, project=project)
                oldfile = rv.file
                rv.update(**kwargs)
                oldfile.delete()
        else:
            oldfile = rv.file
            rv.update(**kwargs)
            oldfile.delete()
    else:
        try:
            rv = ProjectDSymFile.objects.get(debug_id=debug_id, project=project)
        except ProjectDSymFile.DoesNotExist:
            try:
                with transaction.atomic():
                    rv = ProjectDSymFile.objects.create(file=file, debug_id=debug_id, cpu_name=cpu_name, object_name=object_name, project=project)
            except IntegrityError:
                rv = ProjectDSymFile.objects.get(debug_id=debug_id, project=project)
                oldfile = rv.file
                rv.update(file=file)
                oldfile.delete()
        else:
            oldfile = rv.file
            rv.update(file=file)
            oldfile.delete()
        rv.file.headers['Content-Type'] = DSYM_MIMETYPES[dsym_type]
        rv.file.save()
    resolve_processing_issue(project=project, scope='native', object=('dsym:%s' % debug_id))
    return (rv, True)
