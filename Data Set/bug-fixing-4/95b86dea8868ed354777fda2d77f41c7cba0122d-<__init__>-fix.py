def __init__(self):
    self.argument_spec = netapp_utils.na_ontap_host_argument_spec()
    self.argument_spec.update(dict(state=dict(required=False, choices=['present', 'absent'], default='present'), name=dict(required=True, type='str'), from_name=dict(required=False, type='str'), flexvol_name=dict(type='str'), vserver=dict(required=True, type='str')))
    self.module = AnsibleModule(argument_spec=self.argument_spec, required_if=[('state', 'present', ['flexvol_name'])], supports_check_mode=True)
    p = self.module.params
    self.state = p['state']
    self.name = p['name']
    self.from_name = p['from_name']
    self.flexvol_name = p['flexvol_name']
    self.vserver = p['vserver']
    if (HAS_NETAPP_LIB is False):
        self.module.fail_json(msg='the python NetApp-Lib module is required')
    else:
        self.server = netapp_utils.setup_na_ontap_zapi(module=self.module, vserver=self.vserver)