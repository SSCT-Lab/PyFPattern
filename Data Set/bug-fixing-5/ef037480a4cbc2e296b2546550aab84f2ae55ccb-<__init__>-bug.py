def __init__(self):
    self.argument_spec = netapp_utils.na_ontap_host_argument_spec()
    self.argument_spec.update(dict(state=dict(required=False, choices=['present', 'absent'], default='present'), service_state=dict(required=False, choices=['online', 'offline']), name=dict(required=True, type='str'), rename=dict(required=False, type='str'), disk_count=dict(required=False, type='int', default=None), nodes=dict(required=False, type='list'), unmount_volumes=dict(required=False, type='bool')))
    self.module = AnsibleModule(argument_spec=self.argument_spec, required_if=[('service_state', 'offline', ['unmount_volumes'])], supports_check_mode=True)
    parameters = self.module.params
    self.state = parameters['state']
    self.service_state = parameters['service_state']
    self.name = parameters['name']
    self.rename = parameters['rename']
    self.disk_count = parameters['disk_count']
    self.nodes = parameters['nodes']
    self.unmount_volumes = parameters['unmount_volumes']
    if (HAS_NETAPP_LIB is False):
        self.module.fail_json(msg='the python NetApp-Lib module is required')
    else:
        self.server = netapp_utils.setup_na_ontap_zapi(module=self.module)