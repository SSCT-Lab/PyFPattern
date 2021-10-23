def apply(self):
    'Call create/modify/delete operations'
    current = self.get_volume()
    (rename, cd_action) = (None, None)
    if self.parameters.get('from_name'):
        rename = self.na_helper.is_rename_action(self.get_volume(self.parameters['from_name']), current)
    else:
        cd_action = self.na_helper.get_cd_action(current, self.parameters)
    modify = self.na_helper.get_modified_attributes(current, self.parameters)
    if self.na_helper.changed:
        if self.module.check_mode:
            pass
        else:
            if rename:
                self.rename_volume()
            if (cd_action == 'create'):
                self.create_volume()
            elif (cd_action == 'delete'):
                self.delete_volume()
            elif modify:
                self.modify_volume(modify)
    self.module.exit_json(changed=self.na_helper.changed)