def __init__(self):
    self.argument_spec = netapp_utils.na_ontap_host_argument_spec()
    self.argument_spec.update(dict(state=dict(required=False, choices=['present', 'absent'], default='present'), name=dict(required=True, type='str'), application=dict(required=True, type='str', choices=['console', 'http', 'ontapi', 'rsh', 'snmp', 'sp', 'service-processor', 'ssh', 'telnet']), authentication_method=dict(required=True, type='str', choices=['community', 'password', 'publickey', 'domain', 'nsswitch', 'usm']), set_password=dict(required=False, type='str'), role_name=dict(required=False, type='str'), lock_user=dict(required=False, type='bool'), vserver=dict(required=True, type='str')))
    self.module = AnsibleModule(argument_spec=self.argument_spec, required_if=[('state', 'present', ['role_name'])], supports_check_mode=True)
    parameters = self.module.params
    self.state = parameters['state']
    self.name = parameters['name']
    self.application = parameters['application']
    self.authentication_method = parameters['authentication_method']
    self.set_password = parameters['set_password']
    self.role_name = parameters['role_name']
    self.lock_user = parameters['lock_user']
    self.vserver = parameters['vserver']
    if (HAS_NETAPP_LIB is False):
        self.module.fail_json(msg='the python NetApp-Lib module is required')
    else:
        self.server = netapp_utils.setup_na_ontap_zapi(module=self.module, vserver=self.vserver)