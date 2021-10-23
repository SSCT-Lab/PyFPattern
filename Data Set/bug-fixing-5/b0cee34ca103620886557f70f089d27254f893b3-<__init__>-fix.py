def __init__(self):
    argument_spec = eseries_host_argument_spec()
    argument_spec.update(dict(state=dict(required=True, choices=['present', 'absent']), target=dict(required=False, default=None), volume_name=dict(required=True, aliases=['volume']), lun=dict(type='int', required=False), target_type=dict(required=False, choices=['host', 'group'])))
    self.module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    args = self.module.params
    self.state = (args['state'] in ['present'])
    self.target = args['target']
    self.volume = args['volume_name']
    self.lun = args['lun']
    self.target_type = args['target_type']
    self.ssid = args['ssid']
    self.url = args['api_url']
    self.check_mode = self.module.check_mode
    self.creds = dict(url_username=args['api_username'], url_password=args['api_password'], validate_certs=args['validate_certs'])
    self.mapping_info = None
    if (not self.url.endswith('/')):
        self.url += '/'