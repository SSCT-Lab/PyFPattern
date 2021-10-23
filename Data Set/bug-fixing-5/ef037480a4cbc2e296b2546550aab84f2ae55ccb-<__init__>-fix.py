def __init__(self):
    self.argument_spec = netapp_utils.na_ontap_host_argument_spec()
    self.argument_spec.update(dict(state=dict(required=False, choices=['present', 'absent'], default='present'), service_state=dict(required=False, choices=['online', 'offline']), name=dict(required=True, type='str'), from_name=dict(required=False, type='str'), disk_count=dict(required=False, type='int', default=None), disk_type=dict(required=False, choices=['ATA', 'BSAS', 'FCAL', 'FSAS', 'LUN', 'MSATA', 'SAS', 'SSD', 'VMDISK']), raid_type=dict(required=False, type='str'), disk_size=dict(required=False, type='int'), nodes=dict(required=False, type='list'), raid_size=dict(required=False, type='int'), unmount_volumes=dict(required=False, type='bool')))
    self.module = AnsibleModule(argument_spec=self.argument_spec, required_if=[('service_state', 'offline', ['unmount_volumes'])], supports_check_mode=True)
    self.na_helper = NetAppModule()
    self.parameters = self.na_helper.set_parameters(self.module.params)
    if (HAS_NETAPP_LIB is False):
        self.module.fail_json(msg='the python NetApp-Lib module is required')
    else:
        self.server = netapp_utils.setup_na_ontap_zapi(module=self.module)