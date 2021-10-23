def __init__(self):
    'Initialize module parameters'
    self._size_unit_map = dict(bytes=1, b=1, kb=1024, mb=(1024 ** 2), gb=(1024 ** 3), tb=(1024 ** 4), pb=(1024 ** 5), eb=(1024 ** 6), zb=(1024 ** 7), yb=(1024 ** 8))
    self.argument_spec = netapp_utils.na_ontap_host_argument_spec()
    self.argument_spec.update(dict(state=dict(required=False, choices=['present', 'absent'], default='present'), name=dict(required=True, type='str'), vserver=dict(required=True, type='str'), new_name=dict(required=False, type='str'), is_infinite=dict(required=False, type='bool', default=False), is_online=dict(required=False, type='bool', default=True), size=dict(type='int', default=None), size_unit=dict(default='gb', choices=['bytes', 'b', 'kb', 'mb', 'gb', 'tb', 'pb', 'eb', 'zb', 'yb'], type='str'), aggregate_name=dict(type='str', default=None), type=dict(type='str', default=None), policy=dict(type='str', default=None), junction_path=dict(type='str', default=None), space_guarantee=dict(choices=['none', 'volume'], default=None), percent_snapshot_space=dict(type='str', default=None), volume_security_style=dict(choices=['mixed', 'ntfs', 'unified', 'unix'], default='mixed')))
    self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=True)
    parameters = self.module.params
    self.state = parameters['state']
    self.name = parameters['name']
    self.new_name = parameters['new_name']
    self.is_infinite = parameters['is_infinite']
    self.is_online = parameters['is_online']
    self.size_unit = parameters['size_unit']
    self.vserver = parameters['vserver']
    self.type = parameters['type']
    self.policy = parameters['policy']
    self.junction_path = parameters['junction_path']
    self.space_guarantee = parameters['space_guarantee']
    self.percent_snapshot_space = parameters['percent_snapshot_space']
    self.aggregate_name = parameters['aggregate_name']
    self.volume_security_style = parameters['volume_security_style']
    if (parameters['size'] is not None):
        self.size = (parameters['size'] * self._size_unit_map[self.size_unit])
    else:
        self.size = None
    if (HAS_NETAPP_LIB is False):
        self.module.fail_json(msg='the python NetApp-Lib module is required')
    else:
        self.server = netapp_utils.setup_na_ontap_zapi(module=self.module, vserver=self.vserver)
        self.cluster = netapp_utils.setup_na_ontap_zapi(module=self.module)