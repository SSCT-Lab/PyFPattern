def _write_file(self, f, data):
    (tmp_f_fd, tmp_f) = tempfile.mkstemp()
    if isinstance(data, str):
        os.write(tmp_f_fd, data)
    else:
        os.write(tmp_f_fd, data.read())
    try:
        os.close(tmp_f_fd)
    except IOError:
        e = get_exception()
        self.module.fail_json(msg=('Cannot close the temporal plugin file %s.' % tmp_f), details=to_native(e))
    self.module.atomic_move(tmp_f, f)