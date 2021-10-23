def revert(self):
    'Revert svn working directory.'
    self._exec(['revert', '-R', self.dest])