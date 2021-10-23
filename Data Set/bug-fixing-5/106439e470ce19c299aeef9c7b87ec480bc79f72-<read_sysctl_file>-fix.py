def read_sysctl_file(self):
    lines = []
    if os.path.isfile(self.sysctl_file):
        try:
            f = open(self.sysctl_file, 'r')
            lines = f.readlines()
            f.close()
        except IOError:
            e = get_exception()
            self.module.fail_json(msg=('Failed to open %s: %s' % (self.sysctl_file, str(e))))
    for line in lines:
        line = line.strip()
        self.file_lines.append(line)
        if ((not line) or line.startswith(('#', ';'))):
            continue
        (k, v) = line.split('=', 1)
        k = k.strip()
        v = v.strip()
        self.file_values[k] = v.strip()