def __init__(self):
    'Initialize module parameters'
    self._size_unit_map = dict(bytes=1, b=1, kb=1024, mb=(1024 ** 2), gb=(1024 ** 3), tb=(1024 ** 4), pb=(1024 ** 5), eb=(1024 ** 6), zb=(1024 ** 7), yb=(1024 ** 8))
    self.argument_spec = netapp_utils.na_ontap_host_argument_spec()
    self.argument_spec.update(dict(state=dict(required=False, choices=['present', 'absent'], default='present'), name=dict(required=True, type='str'), vserver=dict(required=True, type='str'), from_name=dict(required=False, type='str'), is_infinite=dict(required=False, type='bool', default=False), is_online=dict(required=False, type='bool', default=True), size=dict(type='int', default=None), size_unit=dict(default='gb', choices=['bytes', 'b', 'kb', 'mb', 'gb', 'tb', 'pb', 'eb', 'zb', 'yb'], type='str'), aggregate_name=dict(type='str', default=None), type=dict(type='str', default=None), policy=dict(type='str', default=None), junction_path=dict(type='str', default=None), space_guarantee=dict(choices=['none', 'volume'], default=None), percent_snapshot_space=dict(type='str', default=None), volume_security_style=dict(choices=['mixed', 'ntfs', 'unified', 'unix'], default='mixed'), encrypt=dict(required=False, type='bool', default=False), efficiency_policy=dict(required=False, type='str')))
    self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=True)
    self.na_helper = NetAppModule()
    self.parameters = self.na_helper.set_parameters(self.module.params)
    if self.parameters.get('size'):
        self.parameters['size'] = (self.parameters['size'] * self._size_unit_map[self.parameters['size_unit']])
    if (HAS_NETAPP_LIB is False):
        self.module.fail_json(msg='the python NetApp-Lib module is required')
    else:
        self.server = netapp_utils.setup_na_ontap_zapi(module=self.module, vserver=self.parameters['vserver'])
        self.cluster = netapp_utils.setup_na_ontap_zapi(module=self.module)