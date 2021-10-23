def __init__(self):
    '\n            Initialize the NetAppOntapServiceProcessorNetwork class\n        '
    self.argument_spec = netapp_utils.na_ontap_host_argument_spec()
    self.argument_spec.update(dict(state=dict(required=False, choices=['present'], default='present'), address_type=dict(required=True, choices=['ipv4', 'ipv6']), is_enabled=dict(required=True, choices=['true', 'false']), node=dict(required=True, type='str'), dhcp=dict(required=False, choices=['v4', 'none']), gateway_ip_address=dict(required=False, type='str'), ip_address=dict(required=False, type='str'), netmask=dict(required=False, type='str'), prefix_length=dict(required=False, type='int')))
    self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=True)
    parameters = self.module.params
    self.state = parameters['state']
    self.address_type = parameters['address_type']
    self.dhcp = parameters['dhcp']
    self.gateway_ip_address = parameters['gateway_ip_address']
    self.ip_address = parameters['ip_address']
    self.is_enabled = parameters['is_enabled']
    self.netmask = parameters['netmask']
    self.node = parameters['node']
    self.prefix_length = parameters['prefix_length']
    if (HAS_NETAPP_LIB is False):
        self.module.fail_json(msg='the python NetApp-Lib module is required')
    else:
        self.server = netapp_utils.setup_na_ontap_zapi(module=self.module, vserver=None)
    return