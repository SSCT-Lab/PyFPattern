def __init__(self):
    self.argument_spec = netapp_utils.na_ontap_host_argument_spec()
    self.argument_spec.update(dict(state=dict(required=False, choices=['present', 'absent'], default='present'), allow_list=dict(required=False, type='list'), policy=dict(required=True, type='str'), service=dict(required=True, type='str', choices=['dns', 'http', 'https', 'ndmp', 'ndmps', 'ntp', 'rsh', 'snmp', 'ssh', 'telnet']), vserver=dict(required=True, type='str'), enable=dict(required=False, type='str', choices=['enable', 'disable'], default='enable'), logging=dict(required=False, type='str', choices=['enable', 'disable'], default='disable'), node=dict(required=True, type='str')))
    self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=True)
    self.na_helper = NetAppModule()
    self.parameters = self.na_helper.set_parameters(self.module.params)
    if (HAS_NETAPP_LIB is False):
        self.module.fail_json(msg='the python NetApp-Lib module is required')
    else:
        self.server = netapp_utils.setup_na_ontap_zapi(module=self.module)
    return