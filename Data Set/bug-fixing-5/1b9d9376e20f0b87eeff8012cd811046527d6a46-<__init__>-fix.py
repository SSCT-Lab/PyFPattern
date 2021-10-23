def __init__(self):
    argument_spec = eseries_host_argument_spec()
    argument_spec.update(dict(state=dict(type='str', required=True, choices=['absent', 'present']), group=dict(type='str', required=False), ports=dict(type='list', required=False), force_port=dict(type='bool', default=False), name=dict(type='str', required=True), host_type_index=dict(type='int', required=True)))
    self.module = AnsibleModule(argument_spec=argument_spec)
    args = self.module.params
    self.group = args['group']
    self.ports = args['ports']
    self.force_port = args['force_port']
    self.name = args['name']
    self.host_type_index = args['host_type_index']
    self.state = args['state']
    self.ssid = args['ssid']
    self.url = args['api_url']
    self.user = args['api_username']
    self.pwd = args['api_password']
    self.certs = args['validate_certs']
    self.ports = args['ports']
    self.post_body = dict()
    if (not self.url.endswith('/')):
        self.url += '/'