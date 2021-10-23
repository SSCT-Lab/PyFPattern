def __init__(self):
    self.argument_spec = netapp_utils.na_ontap_host_argument_spec()
    self.argument_spec.update(dict(state=dict(required=False, choices=['present', 'absent'], default='present'), interface_name=dict(required=True, type='str'), home_node=dict(required=False, type='str', default=None), home_port=dict(required=False, type='str'), role=dict(required=False, type='str'), address=dict(required=False, type='str'), netmask=dict(required=False, type='str'), vserver=dict(required=True, type='str'), firewall_policy=dict(required=False, type='str', default=None), failover_policy=dict(required=False, type='str', default=None), admin_status=dict(required=False, choices=['up', 'down']), subnet_name=dict(required=False, type='str'), is_auto_revert=dict(required=False, type='bool', default=None), protocols=dict(required=False, type='list')))
    self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=True)
    self.na_helper = NetAppModule()
    self.parameters = self.na_helper.set_parameters(self.module.params)
    if (HAS_NETAPP_LIB is False):
        self.module.fail_json(msg='the python NetApp-Lib module is required')
    else:
        self.server = netapp_utils.setup_na_ontap_zapi(module=self.module)