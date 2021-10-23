

def createOrUpdateGroup(self, name, parent, options):
    changed = False
    if (self.groupObject is None):
        parent_id = self.getGroupId(parent)
        group = self.createGroup({
            'name': name,
            'path': options['path'],
            'parent_id': parent_id,
        })
        changed = True
    else:
        (changed, group) = self.updateGroup(self.groupObject, {
            'name': name,
            'description': options['description'],
            'visibility': options['visibility'],
        })
    self.groupObject = group
    if changed:
        if self._module.check_mode:
            self._module.exit_json(changed=True, msg=('Successfully created or updated the group %s' % name))
        try:
            group.save()
        except Exception as e:
            self._module.fail_json(msg=('Failed to update group: %s ' % e))
        return True
    else:
        return False
