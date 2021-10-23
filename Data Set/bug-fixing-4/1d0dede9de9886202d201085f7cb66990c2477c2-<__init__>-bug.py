def __init__(self):
    self.argument_spec = netapp_utils.na_ontap_host_argument_spec()
    self.argument_spec.update(dict(state=dict(required=False, choices=['present', 'absent'], default='present'), name=dict(required=True, type='str'), new_name=dict(required=False, type='str', default=None), ostype=dict(required=False, type='str'), initiator_group_type=dict(required=False, type='str', choices=['fcp', 'iscsi', 'mixed']), initiator=dict(required=False, type='str'), vserver=dict(required=True, type='str'), force_remove_initiator=dict(required=False, type='bool', default=False), bind_portset=dict(required=False, type='str')))
    self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=True)
    params = self.module.params
    self.state = params['state']
    self.name = params['name']
    self.ostype = params['ostype']
    self.initiator_group_type = params['initiator_group_type']
    self.initiator = params['initiator']
    self.vserver = params['vserver']
    self.new_name = params['new_name']
    self.force_remove_initiator = params['force_remove_initiator']
    self.bind_portset = params['bind_portset']
    if (HAS_NETAPP_LIB is False):
        self.module.fail_json(msg='the python NetApp-Lib module is required')
    else:
        self.server = netapp_utils.setup_na_ontap_zapi(module=self.module, vserver=self.vserver)