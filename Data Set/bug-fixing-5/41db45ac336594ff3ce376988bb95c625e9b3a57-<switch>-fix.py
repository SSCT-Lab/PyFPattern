def switch(self):
    "Change working directory's repo."
    output = self._exec(['switch', self.repo, self.dest])
    for line in output:
        if re.search('^[ABDUCGE]\\s', line):
            return True
    return False