

def get_name(self):
    ' return the name of the task '
    return (self.name or ('%s : %s' % (self.action, self._role_name)))
