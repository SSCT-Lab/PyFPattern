def fetch_rpm_from_url(spec, module=None):
    tempdir = tempfile.mkdtemp()
    package = os.path.join(tempdir, str(spec.rsplit('/', 1)[1]))
    try:
        (rsp, info) = fetch_url(module, spec)
        if (not rsp):
            module.fail_json(msg=('Failure downloading %s, %s' % (spec, info['msg'])))
        f = open(package, 'w')
        data = rsp.read(BUFSIZE)
        while data:
            f.write(data)
            data = rsp.read(BUFSIZE)
        f.close()
    except Exception:
        e = get_exception()
        shutil.rmtree(tempdir)
        if module:
            module.fail_json(msg=('Failure downloading %s, %s' % (spec, e)))
    return package