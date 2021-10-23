def apply(self):
    '\n            Call create / delete cluster pair methods\n        '
    pair_id = self.check_if_already_paired()
    cd_action = self.na_helper.get_cd_action(pair_id, self.parameters)
    if (cd_action == 'create'):
        self.pair_clusters()
    elif (cd_action == 'delete'):
        self.unpair_clusters(pair_id)
    self.module.exit_json(changed=self.na_helper.changed)