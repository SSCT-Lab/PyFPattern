def _check_link_discovery_requirements(self):
    if ((self.want.link_discovery == 'enabled') and (self.want.virtual_server_discovery == 'disabled')):
        raise F5ModuleError('Virtual server discovery must be enabled if link discovery is enabled')