

def assert_team_admin_can_access(self, path, **kwargs):
    return self.assert_role_can_access(path, 'admin', **kwargs)
