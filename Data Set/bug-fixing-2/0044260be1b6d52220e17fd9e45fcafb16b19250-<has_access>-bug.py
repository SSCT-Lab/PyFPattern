

def has_access(self, permission, view_name, user=None):
    '\n        Verify whether a given user could perform certain permission\n        (e.g can_read, can_write) on the given dag_id.\n\n        :param permission: permission on dag_id(e.g can_read, can_edit).\n        :type permission: str\n        :param view_name: name of view-menu(e.g dag id is a view-menu as well).\n        :type permission: str\n        :param user: user name\n        :type permission: str\n        :return: a bool whether user could perform certain permission on the dag_id.\n        :rtype bool\n        '
    if (not user):
        user = g.user
    if user.is_anonymous:
        return self.is_item_public(permission, view_name)
    return self._has_view_access(user, permission, view_name)
