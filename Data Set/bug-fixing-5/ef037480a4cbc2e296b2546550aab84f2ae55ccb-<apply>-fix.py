def apply(self):
    '\n        Apply action to the aggregate\n        :return: None\n        '
    self.asup_log_for_cserver('na_ontap_aggregate')
    current = self.get_aggr()
    (rename, cd_action) = (None, None)
    if self.parameters.get('from_name'):
        rename = self.na_helper.is_rename_action(self.get_aggr(self.parameters['from_name']), current)
        if (rename is None):
            self.module.fail_json(msg=('Error renaming: aggregate %s does not exist' % self.parameters['from_name']))
    else:
        cd_action = self.na_helper.get_cd_action(current, self.parameters)
    modify = self.na_helper.get_modified_attributes(current, self.parameters)
    if self.na_helper.changed:
        if self.module.check_mode:
            pass
        elif rename:
            self.rename_aggregate()
        elif (cd_action == 'create'):
            self.create_aggr()
        elif (cd_action == 'delete'):
            self.delete_aggr()
        elif modify:
            self.modify_aggr(modify)
    self.module.exit_json(changed=self.na_helper.changed)