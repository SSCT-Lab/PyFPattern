def __init__(self):
    self.argument_spec = netapp_utils.na_ontap_host_argument_spec()
    self.argument_spec.update(state=dict(type='str', default='present', choices=['absent', 'present']), vserver=dict(type='str', required=True), status_admin=dict(type='bool'))
    self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=True)
    self.na_helper = NetAppModule()
    self.parameters = self.na_helper.set_parameters(self.module.params)
    if (HAS_NETAPP_LIB is False):
        self.module.fail_json(msg='the python NetApp-Lib module is required')
    else:
        self.server = netapp_utils.setup_na_ontap_zapi(module=self.module, vserver=self.parameters['vserver'])