def create(self):
    if ((self.want.address is None) or (self.want.netmask is None)):
        raise F5ModuleError('An address and a netmask must be specified')
    if (self.want.vlan is None):
        raise F5ModuleError('A VLAN name must be specified')
    if (self.want.traffic_group is None):
        self.want.update({
            'traffic_group': '/Common/traffic-group-local-only',
        })
    if (self.want.route_domain is None):
        self.want.update({
            'route_domain': 0,
        })
    if self.want.allow_service:
        if ('all' in self.want.allow_service):
            self.want.update(dict(allow_service=['all']))
        elif ('none' in self.want.allow_service):
            self.want.update(dict(allow_service=[]))
        elif ('default' in self.want.allow_service):
            self.want.update(dict(allow_service=['default']))
    self._set_changed_options()
    if self.want.check_mode:
        return True
    self.create_on_device()
    if self.exists():
        return True
    else:
        raise F5ModuleError('Failed to create the Self IP')