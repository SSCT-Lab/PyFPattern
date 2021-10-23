def __init__(self):
    self.argument_spec = netapp_utils.na_ontap_host_argument_spec()
    self.argument_spec.update(dict(state=dict(required=False, type='str', choices=['present', 'absent'], default='present'), name=dict(required=True, type='str'), new_name=dict(required=False, type='str', default=None), vserver=dict(required=False, type='str')))
    self.module = AnsibleModule(argument_spec=self.argument_spec, required_if=[('state', 'present', ['vserver'])], supports_check_mode=True)
    parameters = self.module.params
    self.state = parameters['state']
    self.name = parameters['name']
    self.new_name = parameters['new_name']
    self.vserver = parameters['vserver']
    if (HAS_NETAPP_LIB is False):
        self.module.fail_json(msg='the python NetApp-Lib module is required')
    else:
        self.server = netapp_utils.setup_na_ontap_zapi(module=self.module, vserver=self.vserver)