def create_interface(self):
    ' calling zapi to create interface '
    required_keys = set(['role', 'address', 'home_port', 'netmask'])
    data_protocols_obj = self.set_protocol_option(required_keys)
    self.validate_create_parameters(required_keys)
    options = {
        'interface-name': self.parameters['interface_name'],
        'role': self.parameters['role'],
        'home-node': self.parameters.get('home_node'),
        'vserver': self.parameters['vserver'],
    }
    self.set_options(options, self.parameters)
    interface_create = netapp_utils.zapi.NaElement.create_node_with_children('net-interface-create', **options)
    if (data_protocols_obj is not None):
        interface_create.add_child_elem(data_protocols_obj)
    try:
        self.server.invoke_successfully(interface_create, enable_tunneling=True)
    except netapp_utils.zapi.NaApiError as exc:
        self.module.fail_json(msg=('Error Creating interface %s: %s' % (self.parameters['interface_name'], to_native(exc))), exception=traceback.format_exc())