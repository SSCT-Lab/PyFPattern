def __init__(self):
    self.module_arg_spec = dict(resource_group=dict(type='str', required=True), name=dict(type='str', required=True), location=dict(type='str'), sku=dict(type='dict', options=sku_spec), enable_non_ssl_port=dict(type='bool', default=False), maxfragmentationmemory_reserved=dict(type='int'), maxmemory_reserved=dict(type='int'), maxmemory_policy=dict(type='str', choices=['volatile_lru', 'allkeys_lru', 'volatile_random', 'allkeys_random', 'volatile_ttl', 'noeviction']), notify_keyspace_events=dict(type='int'), shard_count=dict(type='int'), static_ip=dict(type='str'), subnet=dict(type='raw'), tenant_settings=dict(type='dict'), state=dict(type='str', default='present', choices=['present', 'absent']), reboot=dict(type='dict', options=reboot_spec), regenerate_key=dict(type='dict', options=regenerate_key_spec), wait_for_provisioning=dict(type='bool', default='True'))
    self._client = None
    self.resource_group = None
    self.name = None
    self.location = None
    self.sku = None
    self.size = None
    self.enable_non_ssl_port = False
    self.configuration_file_path = None
    self.shard_count = None
    self.static_ip = None
    self.subnet = None
    self.tenant_settings = None
    self.reboot = None
    self.regenerate_key = None
    self.wait_for_provisioning = None
    self.wait_for_provisioning_polling_interval_in_seconds = 30
    self.wait_for_provisioning_polling_times = 120
    self.tags = None
    self.results = dict(changed=False, id=None, host_name=None)
    self.state = None
    self.to_do = Actions.NoAction
    super(AzureRMRedisCaches, self).__init__(derived_arg_spec=self.module_arg_spec, supports_check_mode=True, supports_tags=True)