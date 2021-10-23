def switch(self):
    "Change working directory's repo."
    self._exec(['switch', self.repo, self.dest])