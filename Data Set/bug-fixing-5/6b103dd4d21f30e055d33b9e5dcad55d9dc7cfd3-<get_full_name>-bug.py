def get_full_name(self):
    if (self.team.name not in self.name):
        return ('%s %s' % (self.team.name, self.name))
    return self.name