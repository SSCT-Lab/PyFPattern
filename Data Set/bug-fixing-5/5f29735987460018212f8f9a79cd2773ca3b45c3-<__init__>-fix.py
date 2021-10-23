def __init__(self):
    self._size_unit_map = dict(bytes=1, b=1, kb=1024, mb=(1024 ** 2), gb=(1024 ** 3), tb=(1024 ** 4), pb=(1024 ** 5), eb=(1024 ** 6), zb=(1024 ** 7), yb=(1024 ** 8))
    self.argument_spec = netapp_utils.na_ontap_host_argument_spec()
    self.argument_spec.update(dict(state=dict(required=False, choices=['present', 'absent'], default='present'), name=dict(required=True, type='str'), size=dict(type='int'), size_unit=dict(default='gb', choices=['bytes', 'b', 'kb', 'mb', 'gb', 'tb', 'pb', 'eb', 'zb', 'yb'], type='str'), force_resize=dict(default=False, type='bool'), force_remove=dict(default=False, type='bool'), force_remove_fenced=dict(default=False, type='bool'), flexvol_name=dict(required=True, type='str'), vserver=dict(required=True, type='str'), ostype=dict(required=False, type='str', default='image'), space_reserve=dict(required=False, type='bool', default=True), space_allocation=dict(required=False, type='bool', default=False)))
    self.module = AnsibleModule(argument_spec=self.argument_spec, required_if=[('state', 'present', ['size'])], supports_check_mode=True)
    parameters = self.module.params
    self.state = parameters['state']
    self.name = parameters['name']
    self.size_unit = parameters['size_unit']
    if (parameters['size'] is not None):
        self.size = (parameters['size'] * self._size_unit_map[self.size_unit])
    else:
        self.size = None
    self.force_resize = parameters['force_resize']
    self.force_remove = parameters['force_remove']
    self.force_remove_fenced = parameters['force_remove_fenced']
    self.flexvol_name = parameters['flexvol_name']
    self.vserver = parameters['vserver']
    self.ostype = parameters['ostype']
    self.space_reserve = parameters['space_reserve']
    self.space_allocation = parameters['space_allocation']
    if (HAS_NETAPP_LIB is False):
        self.module.fail_json(msg='the python NetApp-Lib module is required')
    else:
        self.server = netapp_utils.setup_na_ontap_zapi(module=self.module, vserver=self.vserver)