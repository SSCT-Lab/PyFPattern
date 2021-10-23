def write_changes(module, lines, dest):
    (tmpfd, tmpfile) = tempfile.mkstemp()
    f = os.fdopen(tmpfd, 'wb')
    f.writelines(lines)
    f.close()
    module.atomic_move(tmpfile, os.path.realpath(dest))