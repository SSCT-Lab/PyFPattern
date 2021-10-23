

def __init__(self):
    self.argument_spec = netapp_utils.na_ontap_host_argument_spec()
    self.argument_spec.update(dict(state=dict(required=False, choices=['present', 'absent'], default='present'), initiator_group_name=dict(required=True, type='str'), path=dict(type='str'), vserver=dict(required=True, type='str'), lun_id=dict(required=False, type='str', default=None)))
    self.module = AnsibleModule(argument_spec=self.argument_spec, required_if=[('state', 'present', ['path'])], supports_check_mode=True)
    p = self.module.params
    self.state = p['state']
    self.initiator_group_name = p['initiator_group_name']
    self.path = p['path']
    self.vserver = p['vserver']
    self.lun_id = p['lun_id']
    if (HAS_NETAPP_LIB is False):
        self.module.fail_json(msg='the python NetApp-Lib module is required')
    else:
        self.server = netapp_utils.setup_na_ontap_zapi(module=self.module, vserver=self.vserver)
