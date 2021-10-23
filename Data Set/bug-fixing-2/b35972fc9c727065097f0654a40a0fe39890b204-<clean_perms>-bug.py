

def clean_perms(self):
    '\n        FAB leaves faulty permissions that need to be cleaned up\n        '
    self.log.debug('Cleaning faulty perms')
    sesh = self.get_session
    pvms = sesh.query(sqla_models.PermissionView).filter(or_((sqla_models.PermissionView.permission is None), (sqla_models.PermissionView.view_menu is None)))
    deleted_count = 0
    for pvm in pvms:
        sesh.delete(pvm)
        deleted_count += 1
    sesh.commit()
    if deleted_count:
        self.log.info('Deleted %s faulty permissions', deleted_count)
