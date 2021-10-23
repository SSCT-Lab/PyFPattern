def _write_file(self, f, data):
    tmp_f = tempfile.mkstemp()
    try:
        fd = open(tmp_f, 'wb')
    except IOError:
        e = get_exception()
        self.module.fail_json(msg=('Cannot open the temporal plugin file %s.' % tmp_f), details=str(e))
    if isinstance(data, str):
        d = data
    else:
        d = data.read()
    fd.write(d)
    try:
        fd.close()
    except IOError:
        e = get_exception()
        self.module.fail_json(msg=('Cannot close the temporal plugin file %s.' % tmp_f), details=str(e))
    self.module.atomic_move(tmp_f, f)