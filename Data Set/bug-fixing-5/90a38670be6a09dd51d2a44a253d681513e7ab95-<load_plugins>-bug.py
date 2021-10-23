def load_plugins(version, force_reload):
    'Load plugins from ansible-doc.\n    :type version: str\n    :type force_reload: bool\n    :rtype: list[PluginDescription]\n    '
    plugin_cache_path = os.path.join(CHANGELOG_DIR, '.plugin-cache.yaml')
    plugins_data = {
        
    }
    if ((not force_reload) and os.path.exists(plugin_cache_path)):
        with open(plugin_cache_path, 'r') as plugin_cache_fd:
            plugins_data = yaml.safe_load(plugin_cache_fd)
            if (version != plugins_data['version']):
                LOGGER.info('version %s does not match plugin cache version %s', version, plugins_data['version'])
                plugins_data = {
                    
                }
    if (not plugins_data):
        LOGGER.info('refreshing plugin cache')
        plugins_data['version'] = version
        for plugin_type in C.DOCUMENTABLE_PLUGINS:
            plugins_data['plugins'][plugin_type] = json.loads(subprocess.check_output([os.path.join(BASE_DIR, 'bin', 'ansible-doc'), '--json', '-t', plugin_type]))
        for section in plugins_data['plugins'].values():
            for plugin in section.values():
                if (plugin['namespace'] is None):
                    del plugin['namespace']
        with open(plugin_cache_path, 'w') as plugin_cache_fd:
            yaml.safe_dump(plugins_data, plugin_cache_fd, default_flow_style=False)
    plugins = PluginDescription.from_dict(plugins_data['plugins'])
    return plugins