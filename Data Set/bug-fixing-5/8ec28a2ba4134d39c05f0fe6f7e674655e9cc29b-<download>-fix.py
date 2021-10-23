def download(module, deb):
    tempdir = os.path.dirname(__file__)
    package = os.path.join(tempdir, str(deb.rsplit('/', 1)[1]))
    BUFSIZE = 65536
    try:
        (rsp, info) = fetch_url(module, deb)
        f = open(package, 'wb')
        while True:
            data = rsp.read(BUFSIZE)
            data = to_bytes(data, errors='surrogate_or_strict')
            if (len(data) < 1):
                break
            f.write(data)
        f.close()
        deb = package
    except Exception:
        e = get_exception()
        module.fail_json(msg=('Failure downloading %s, %s' % (deb, e)))
    return deb