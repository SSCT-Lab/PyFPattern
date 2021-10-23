def __init__(self):
    self.argument_spec = netapp_utils.na_ontap_host_argument_spec()
    self.argument_spec.update(state=dict(type='str', default='present', choices=['absent', 'present']), interface_name=dict(type='str', required=True), home_node=dict(type='str'), home_port=dict(type='str'), role=dict(type='str'), address=dict(type='str'), netmask=dict(type='str'), vserver=dict(type='str', required=True), firewall_policy=dict(type='str'), failover_policy=dict(type='str'), admin_status=dict(type='str', choices=['up', 'down']), subnet_name=dict(type='str'), is_auto_revert=dict(type='bool'), protocols=dict(type='list'))
    self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=True)
    self.na_helper = NetAppModule()
    self.parameters = self.na_helper.set_parameters(self.module.params)
    if (HAS_NETAPP_LIB is False):
        self.module.fail_json(msg='the python NetApp-Lib module is required')
    else:
        self.server = netapp_utils.setup_na_ontap_zapi(module=self.module)