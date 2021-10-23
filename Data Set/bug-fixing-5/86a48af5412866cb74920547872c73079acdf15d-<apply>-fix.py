def apply(self):
    '\n        Run Module based on play book\n        '
    netapp_utils.ems_log_event('na_ontap_net_routes', self.server)
    current = self.get_net_route()
    (modify, cd_action) = (None, None)
    modify_params = {
        'destination': self.parameters.get('new_destination'),
        'gateway': self.parameters.get('new_gateway'),
        'metric': self.parameters.get('new_metric'),
    }
    if any(modify_params.values()):
        d = self.get_net_route(modify_params)
        modify = self.na_helper.is_rename_action(current, d)
        if (modify is None):
            self.module.fail_json(msg=('Error modifying: route %s does not exist' % self.parameters['destination']))
    else:
        cd_action = self.na_helper.get_cd_action(current, self.parameters)
    if (cd_action == 'create'):
        self.create_net_route()
    elif (cd_action == 'delete'):
        self.delete_net_route()
    elif modify:
        self.modify_net_route(current, modify_params)
    self.module.exit_json(changed=self.na_helper.changed)