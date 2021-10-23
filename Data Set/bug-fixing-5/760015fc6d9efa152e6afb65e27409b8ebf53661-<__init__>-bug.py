def __init__(self):
    self._size_unit_map = dict(bytes=1, b=1, kb=1024, mb=(1024 ** 2), gb=(1024 ** 3), tb=(1024 ** 4), pb=(1024 ** 5), eb=(1024 ** 6), zb=(1024 ** 7), yb=(1024 ** 8))
    self._post_headers = dict(Accept='application/json')
    self._post_headers['Content-Type'] = 'application/json'
    argument_spec = basic_auth_argument_spec()
    argument_spec.update(dict(state=dict(required=True, choices=['present', 'absent']), ssid=dict(required=True, type='str'), name=dict(required=True, type='str'), storage_pool_name=dict(type='str'), size_unit=dict(default='gb', choices=['bytes', 'b', 'kb', 'mb', 'gb', 'tb', 'pb', 'eb', 'zb', 'yb'], type='str'), size=dict(type='int'), segment_size_kb=dict(default=128, choices=[8, 16, 32, 64, 128, 256, 512], type='int'), ssd_cache_enabled=dict(type='bool'), data_assurance_enabled=dict(default=False, type='bool'), thin_provision=dict(default=False, type='bool'), thin_volume_repo_size=dict(type='int'), thin_volume_max_repo_size=dict(type='int'), log_path=dict(type='str'), api_url=dict(type='str'), api_username=dict(type='str'), api_password=dict(type='str', no_log=True), validate_certs=dict(type='bool')))
    self.module = AnsibleModule(argument_spec=argument_spec, required_if=[('state', 'present', ['storage_pool_name', 'size']), ('thin_provision', 'true', ['thin_volume_repo_size'])], supports_check_mode=True)
    p = self.module.params
    log_path = p['log_path']
    self._logger = logging.getLogger(self.__class__.__name__)
    self.debug = self._logger.debug
    if log_path:
        logging.basicConfig(level=logging.DEBUG, filename=log_path)
    self.state = p['state']
    self.ssid = p['ssid']
    self.name = p['name']
    self.storage_pool_name = p['storage_pool_name']
    self.size_unit = p['size_unit']
    self.size = p['size']
    self.segment_size_kb = p['segment_size_kb']
    self.ssd_cache_enabled = p['ssd_cache_enabled']
    self.data_assurance_enabled = p['data_assurance_enabled']
    self.thin_provision = p['thin_provision']
    self.thin_volume_repo_size = p['thin_volume_repo_size']
    self.thin_volume_max_repo_size = p['thin_volume_max_repo_size']
    if (not self.thin_volume_max_repo_size):
        self.thin_volume_max_repo_size = self.size
    self.validate_certs = p['validate_certs']
    try:
        self.api_usr = p['api_username']
        self.api_pwd = p['api_password']
        self.api_url = p['api_url']
    except KeyError:
        self.module.fail_json(msg='You must pass in api_username and api_password and api_url to the module.')