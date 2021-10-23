def __init__(self):
    self.argument_spec = netapp_utils.na_ontap_host_argument_spec()
    self.argument_spec.update(dict(state=dict(required=False, choices=['present', 'absent'], default='present'), name=dict(required=True, type='str'), command_directory_name=dict(required=True, type='str'), access_level=dict(required=False, type='str', default='all', choices=['none', 'readonly', 'all']), vserver=dict(required=True, type='str')))
    self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=True)
    parameters = self.module.params
    self.state = parameters['state']
    self.name = parameters['name']
    self.command_directory_name = parameters['command_directory_name']
    self.access_level = parameters['access_level']
    self.vserver = parameters['vserver']
    if (HAS_NETAPP_LIB is False):
        self.module.fail_json(msg='the python NetApp-Lib module is required')
    else:
        self.server = netapp_utils.setup_na_ontap_zapi(module=self.module, vserver=self.vserver)