def get_full_name(self):
    team_name = self.teams.values_list('name', flat=True).first()
    if ((team_name is not None) and (team_name not in self.name)):
        return ('%s %s' % (team_name, self.name))
    return self.name