def _connect(self):
    api_region = (self.module.params.get('api_region') or os.environ.get('CLOUDSTACK_REGION'))
    try:
        config = read_config(api_region)
    except KeyError:
        config = {
            
        }
    api_config = {
        'endpoint': (self.module.params.get('api_url') or config.get('endpoint')),
        'key': (self.module.params.get('api_key') or config.get('key')),
        'secret': (self.module.params.get('api_secret') or config.get('secret')),
        'timeout': (self.module.params.get('api_timeout') or config.get('timeout')),
        'method': (self.module.params.get('api_http_method') or config.get('method')),
    }
    self.result.update({
        'api_region': api_region,
        'api_url': api_config['endpoint'],
        'api_key': api_config['key'],
        'api_timeout': api_config['timeout'],
        'api_http_method': api_config['method'],
    })
    if (not all([api_config['endpoint'], api_config['key'], api_config['secret']])):
        self.fail_json(msg='Missing api credentials: can not authenticate')
    self.cs = CloudStack(**api_config)