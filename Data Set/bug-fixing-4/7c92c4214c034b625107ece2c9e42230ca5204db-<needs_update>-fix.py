def needs_update(self):
    (curr, url) = self.get_revision()
    out2 = '\n'.join(self._exec(['info', '-r', self.revision, self.dest]))
    head = re.search('^Revision:.*$', out2, re.MULTILINE).group(0)
    rev1 = int(curr.split(':')[1].strip())
    rev2 = int(head.split(':')[1].strip())
    change = False
    if (rev1 < rev2):
        change = True
    return (change, curr, head)