def write_changes(module, lines, dest):
    (tmpfd, tmpfile) = tempfile.mkstemp()
    f = os.fdopen(tmpfd, 'wb')
    f.writelines(to_bytes(lines, errors='surrogate_or_strict'))
    f.close()
    module.atomic_move(tmpfile, os.path.realpath(dest))