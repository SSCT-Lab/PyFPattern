def revert(self):
    'Revert svn working directory.'
    output = self._exec(['revert', '-R', self.dest])
    for line in output:
        if (re.search('^Reverted ', line) is None):
            return True
    return False