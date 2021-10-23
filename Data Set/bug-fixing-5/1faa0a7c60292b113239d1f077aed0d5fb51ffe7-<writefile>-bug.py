def writefile(module, filename, content):
    (fd, tmp_path) = tempfile.mkstemp('', 'tmp', os.path.dirname(filename))
    f = open(tmp_path, 'w')
    try:
        f.write(content)
    except IOError:
        e = get_exception()
        module.fail_json(msg=('Failed to write to file %s: %s' % (tmp_path, str(e))))
    f.close()
    module.atomic_move(tmp_path, filename)