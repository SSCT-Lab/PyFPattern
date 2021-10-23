def write_sysctl(self):
    (fd, tmp_path) = tempfile.mkstemp('.conf', '.ansible_m_sysctl_', os.path.dirname(self.sysctl_file))
    f = open(tmp_path, 'w')
    try:
        for l in self.fixed_lines:
            f.write((l.strip() + '\n'))
    except IOError:
        e = get_exception()
        self.module.fail_json(msg=('Failed to write to file %s: %s' % (tmp_path, str(e))))
    f.flush()
    f.close()
    self.module.atomic_move(tmp_path, self.sysctl_file)