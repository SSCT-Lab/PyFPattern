def modify_admin_user(self):
    '\n        Modify a admin user. If a password is set the user will be modified as there is no way to compare a new password with an existing one\n        :return: if a user was modified or not\n        '
    changed = False
    admin_user = self.get_admin_user()
    if ((not (admin_user.access == self.access)) and (self.access is not None)):
        changed = True
    if self.element_password:
        changed = True
    if changed:
        self.sfe.modify_cluster_admin(cluster_admin_id=admin_user.cluster_admin_id, access=self.access, password=self.element_password, attributes=self.attributes)
    return changed