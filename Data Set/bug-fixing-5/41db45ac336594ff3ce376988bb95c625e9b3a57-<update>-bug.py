def update(self):
    'Update existing svn working directory.'
    self._exec(['update', '-r', self.revision, self.dest])