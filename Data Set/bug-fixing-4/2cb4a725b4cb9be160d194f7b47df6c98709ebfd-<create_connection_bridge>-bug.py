def create_connection_bridge(self):
    cmd = [self.module.get_bin_path('nmcli', True)]
    return cmd