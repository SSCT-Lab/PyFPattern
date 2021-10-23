def writefile(module, filename, content):
    (fd, tmp_path) = tempfile.mkstemp('', 'tmp', os.path.dirname(filename))
    f = open(tmp_path, 'w')
    try:
        f.write(content)
    except IOError as e:
        module.fail_json(msg=('Failed to write to file %s: %s' % (tmp_path, to_native(e))))
    f.close()
    module.atomic_move(tmp_path, filename)