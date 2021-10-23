def _get_common_args(self):
    args = {
        'name': self.module.params.get('name'),
        'isolationmethods': self.module.params.get('isolation_method'),
        'broadcastdomainrange': self.module.params.get('broadcast_domain_range'),
        'networkspeed': self.module.params.get('network_speed'),
        'tags': self.module.params.get('tags'),
        'vlan': self.module.params.get('vlan'),
    }
    state = self.module.params.get('state')
    if (state in ['enabled', 'disabled']):
        args['state'] = state.capitalize()
    return args