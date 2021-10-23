def apply(self):
    '\n            Call create / delete cluster pair methods\n        '
    pair_id_source = self.get_src_pair_id()
    if pair_id_source:
        pair_id_dest = self.get_dest_pair_id()
    cd_action = self.na_helper.get_cd_action(pair_id_source, self.parameters)
    if (cd_action == 'create'):
        self.pair_clusters()
    elif (cd_action == 'delete'):
        self.unpair_clusters(pair_id_source, pair_id_dest)
    self.module.exit_json(changed=self.na_helper.changed)