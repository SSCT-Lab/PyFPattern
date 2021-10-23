

def parse(self, inventory, loader, path, cache=True):
    if (not HAS_GOOGLE_LIBRARIES):
        raise AnsibleParserError(('gce inventory plugin cannot start: %s' % missing_required_lib('google-auth')))
    super(InventoryModule, self).parse(inventory, loader, path)
    config_data = {
        
    }
    config_data = self._read_config_data(path)
    if self.get_option('use_contrib_script_compatible_sanitization'):
        self._sanitize_group_name = self._legacy_script_compatible_group_sanitization
    params = {
        'filters': self.get_option('filters'),
        'projects': self.get_option('projects'),
        'scopes': self.get_option('scopes'),
        'zones': self.get_option('zones'),
        'auth_kind': self.get_option('auth_kind'),
        'service_account_file': self.get_option('service_account_file'),
        'service_account_contents': self.get_option('service_account_contents'),
        'service_account_email': self.get_option('service_account_email'),
    }
    self.fake_module = GcpMockModule(params)
    self.auth_session = GcpSession(self.fake_module, 'compute')
    query = self._get_query_options(params['filters'])
    if self.get_option('retrieve_image_info'):
        project_disks = self._get_project_disks(config_data, query)
    else:
        project_disks = None
    if cache:
        cache = self.get_option('cache')
        cache_key = self.get_cache_key(path)
    else:
        cache_key = None
    cache_needs_update = False
    if cache:
        try:
            results = self._cache[cache_key]
            for project in results:
                for zone in results[project]:
                    self._add_hosts(results[project][zone], config_data, False, project_disks=project_disks)
        except KeyError:
            cache_needs_update = True
    if ((not cache) or cache_needs_update):
        cached_data = {
            
        }
        for project in params['projects']:
            cached_data[project] = {
                
            }
            params['project'] = project
            zones = params['zones']
            link = (self._instances % project)
            resp = self.fetch_list(params, link, query)
            if (('items' in resp) and resp['items']):
                for (key, value) in resp.get('items').items():
                    if ('instances' in value):
                        zone = key[6:]
                        if ((not zones) or (zone in zones)):
                            self._add_hosts(value['instances'], config_data, project_disks=project_disks)
                            cached_data[project][zone] = value['instances']
    if cache_needs_update:
        self._cache[cache_key] = cached_data
