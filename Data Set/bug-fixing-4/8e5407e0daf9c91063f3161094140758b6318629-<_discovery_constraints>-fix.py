def _discovery_constraints(self):
    if (self.want.virtual_server_discovery is None):
        virtual_server_discovery = self.have.virtual_server_discovery
    else:
        virtual_server_discovery = self.want.virtual_server_discovery
    if (self.want.link_discovery is None):
        link_discovery = self.have.link_discovery
    else:
        link_discovery = self.want.link_discovery
    if ((link_discovery in ['enabled', 'enabled-no-delete']) and (virtual_server_discovery == 'disabled')):
        raise F5ModuleError('Virtual server discovery must be enabled if link discovery is enabled')