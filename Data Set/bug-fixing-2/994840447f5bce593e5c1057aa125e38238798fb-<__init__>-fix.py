

def __init__(self):
    self.argument_spec = netapp_utils.ontap_sf_host_argument_spec()
    self.argument_spec.update(dict(state=dict(required=True, choices=['present', 'absent']), name=dict(required=True, type='str'), root_volume=dict(type='str'), root_volume_aggregate=dict(type='str'), root_volume_security_style=dict(type='str', choices=['unix', 'ntfs', 'mixed', 'unified'])))
    self.module = AnsibleModule(argument_spec=self.argument_spec, required_if=[('state', 'present', ['root_volume', 'root_volume_aggregate', 'root_volume_security_style'])], supports_check_mode=True)
    p = self.module.params
    self.state = p['state']
    self.name = p['name']
    self.root_volume = p['root_volume']
    self.root_volume_aggregate = p['root_volume_aggregate']
    self.root_volume_security_style = p['root_volume_security_style']
    if (HAS_NETAPP_LIB is False):
        self.module.fail_json(msg='the python NetApp-Lib module is required')
    else:
        self.server = netapp_utils.setup_ontap_zapi(module=self.module)
