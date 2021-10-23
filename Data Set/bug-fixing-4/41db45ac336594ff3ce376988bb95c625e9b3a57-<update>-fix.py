def update(self):
    'Update existing svn working directory.'
    output = self._exec(['update', '-r', self.revision, self.dest])
    for line in output:
        if re.search('^[ABDUCGE]\\s', line):
            return True
    return False