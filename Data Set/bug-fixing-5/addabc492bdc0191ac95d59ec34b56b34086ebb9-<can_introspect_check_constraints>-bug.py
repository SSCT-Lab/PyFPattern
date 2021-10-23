@cached_property
def can_introspect_check_constraints(self):
    if self.connection.mysql_is_mariadb:
        version = self.connection.mysql_version
        if (((version >= (10, 2, 22)) and (version < (10, 3))) or (version >= (10, 3, 10))):
            return True
    return (self.connection.mysql_version >= (8, 0, 16))