def __init__(self):
    self.argument_spec = netapp_utils.na_ontap_host_argument_spec()
    self.argument_spec.update(dict(state=dict(required=False, choices=['present', 'absent'], default='present'), name=dict(required=True, type='str'), new_name=dict(required=False, type='str'), root_volume=dict(type='str'), root_volume_aggregate=dict(type='str'), root_volume_security_style=dict(type='str', choices=['unix', 'ntfs', 'mixed', 'unified']), allowed_protocols=dict(type='list'), aggr_list=dict(type='list')))
    self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=True)
    p = self.module.params
    self.state = p['state']
    self.name = p['name']
    self.new_name = p['new_name']
    self.root_volume = p['root_volume']
    self.root_volume_aggregate = p['root_volume_aggregate']
    self.root_volume_security_style = p['root_volume_security_style']
    self.allowed_protocols = p['allowed_protocols']
    self.aggr_list = p['aggr_list']
    if (HAS_NETAPP_LIB is False):
        self.module.fail_json(msg='the python NetApp-Lib module is required')
    else:
        self.server = netapp_utils.setup_na_ontap_zapi(module=self.module)