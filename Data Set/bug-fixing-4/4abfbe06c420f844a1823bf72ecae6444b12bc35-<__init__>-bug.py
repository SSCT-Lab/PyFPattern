def __init__(self):
    '\n            Initialize the Ontap Net Route class\n        '
    self.argument_spec = netapp_utils.na_ontap_host_argument_spec()
    self.argument_spec.update(dict(state=dict(required=False, choices=['present', 'absent'], default='present'), vserver=dict(required=False, type='str'), broadcast_domain=dict(required=True, type='str'), ipspace=dict(required=False, type='str', default=None), ports=dict(required=True, type='list')))
    self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=True)
    parameters = self.module.params
    self.state = parameters['state']
    self.vserver = parameters['vserver']
    self.broadcast_domain = parameters['broadcast_domain']
    self.ipspace = parameters['ipspace']
    self.ports = parameters['ports']
    if (HAS_NETAPP_LIB is False):
        self.module.fail_json(msg='the python NetApp-Lib module is required')
    else:
        self.server = netapp_utils.setup_na_ontap_zapi(module=self.module)
    return