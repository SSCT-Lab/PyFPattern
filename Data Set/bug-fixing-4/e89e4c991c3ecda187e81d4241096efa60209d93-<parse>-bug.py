def parse(self, inventory, loader, path, cache=True):
    super(InventoryModule, self).parse(inventory, loader, path)
    cache_key = self._get_cache_prefix(path)
    self._config_data = self._read_config_data(path)
    msg = ''
    if (not self._config_data):
        msg = 'File empty. this is not my config file'
    elif (('plugin' in self._config_data) and (self._config_data['plugin'] != self.NAME)):
        msg = ('plugin config file, but not for us: %s' % self._config_data['plugin'])
    elif (('plugin' not in self._config_data) and ('clouds' not in self._config_data)):
        msg = "it's not a plugin configuration nor a clouds.yaml file"
    elif (not HAS_SDK):
        msg = 'openstacksdk is required for the OpenStack inventory plugin. OpenStack inventory sources will be skipped.'
    if msg:
        raise AnsibleParserError(msg)
    if ('clouds' in self._config_data):
        self._config_data = {
            
        }
    source_data = None
    if (cache and (cache_key in self._cache)):
        try:
            source_data = self._cache[cache_key]
        except KeyError:
            pass
    if (not source_data):
        clouds_yaml_path = self._config_data.get('clouds_yaml_path')
        if clouds_yaml_path:
            config_files = (clouds_yaml_path + client_config.CONFIG_FILES)
        else:
            config_files = None
        sdk.enable_logging()
        cloud_inventory = sdk_inventory.OpenStackInventory(config_files=config_files, private=self._config_data.get('private', False))
        only_clouds = self._config_data.get('only_clouds', [])
        if (only_clouds and (not isinstance(only_clouds, list))):
            raise ValueError('OpenStack Inventory Config Error: only_clouds must be a list')
        if only_clouds:
            new_clouds = []
            for cloud in cloud_inventory.clouds:
                if (cloud.name in only_clouds):
                    new_clouds.append(cloud)
            cloud_inventory.clouds = new_clouds
        expand_hostvars = self._config_data.get('expand_hostvars', False)
        fail_on_errors = self._config_data.get('fail_on_errors', False)
        source_data = cloud_inventory.list_hosts(expand=expand_hostvars, fail_on_cloud_config=fail_on_errors)
        self._cache[cache_key] = source_data
    self._populate_from_source(source_data)