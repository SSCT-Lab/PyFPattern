

def __init__(self):
    self._size_unit_map = netapp_utils.SF_BYTE_MAP
    self.argument_spec = netapp_utils.ontap_sf_host_argument_spec()
    self.argument_spec.update(dict(state=dict(required=True, choices=['present', 'absent']), name=dict(required=True, type='str'), account_id=dict(required=True, type='int'), enable512e=dict(type='bool', aliases=['512emulation']), qos=dict(required=False, type='str', default=None), attributes=dict(required=False, type='dict', default=None), volume_id=dict(type='int', default=None), size=dict(type='int'), size_unit=dict(default='gb', choices=['bytes', 'b', 'kb', 'mb', 'gb', 'tb', 'pb', 'eb', 'zb', 'yb'], type='str'), access=dict(required=False, type='str', default=None, choices=['readOnly', 'readWrite', 'locked', 'replicationTarget'])))
    self.module = AnsibleModule(argument_spec=self.argument_spec, required_if=[('state', 'present', ['size', 'enable512e'])], supports_check_mode=True)
    p = self.module.params
    self.state = p['state']
    self.name = p['name']
    self.account_id = p['account_id']
    self.enable512e = p['enable512e']
    self.qos = p['qos']
    self.attributes = p['attributes']
    self.volume_id = p['volume_id']
    self.size_unit = p['size_unit']
    if (p['size'] is not None):
        self.size = (p['size'] * self._size_unit_map[self.size_unit])
    else:
        self.size = None
    self.access = p['access']
    if (HAS_SF_SDK is False):
        self.module.fail_json(msg='Unable to import the SolidFire Python SDK')
    else:
        self.sfe = netapp_utils.create_sf_connection(module=self.module)
