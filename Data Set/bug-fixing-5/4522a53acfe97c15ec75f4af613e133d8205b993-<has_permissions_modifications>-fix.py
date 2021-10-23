def has_permissions_modifications(self):
    return (sorted(self._permissions) != sorted(self.permissions))