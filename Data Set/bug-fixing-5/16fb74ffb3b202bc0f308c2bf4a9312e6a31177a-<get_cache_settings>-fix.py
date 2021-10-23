def get_cache_settings(cloud=None):
    config_files = (cloud_config.CONFIG_FILES + CONFIG_FILES)
    if cloud:
        config = cloud_config.OpenStackConfig(config_files=config_files).get_one(cloud=cloud)
    else:
        config = cloud_config.OpenStackConfig(config_files=config_files).get_all()[0]
    cache_expiration_time = config.get_cache_expiration_time()
    cache_path = config.get_cache_path()
    if cloud:
        cache_path = '{0}_{1}'.format(cache_path, cloud)
    if (not os.path.exists(cache_path)):
        os.makedirs(cache_path)
    cache_file = os.path.join(cache_path, 'ansible-inventory.cache')
    return (cache_file, cache_expiration_time)