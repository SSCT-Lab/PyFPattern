def create_network(self):
    '\n            Add VLAN\n        '
    try:
        self.validate_keys()
        create_params = self.parameters.copy()
        for key in ['username', 'hostname', 'password', 'state', 'vlan_tag']:
            del create_params[key]
        self.elem.add_virtual_network(virtual_network_tag=self.parameters['vlan_tag'], **create_params)
    except solidfire.common.ApiServerError as err:
        self.module.fail_json(msg=('Error creating VLAN %s' % self.parameters['vlan_tag']), exception=to_native(err))