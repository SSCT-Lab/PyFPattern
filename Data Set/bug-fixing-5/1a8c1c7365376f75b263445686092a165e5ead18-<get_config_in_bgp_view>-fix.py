def get_config_in_bgp_view(self):
    'Get configuration in BGP view'
    cmd = 'display current-configuration | section include'
    if self.as_number:
        if self.bgp_instance:
            cmd += (' bgp %s instance %s' % (self.as_number, self.bgp_instance))
        else:
            cmd += (' bgp %s' % self.as_number)
    (rc, out, err) = exec_command(self.module, cmd)
    if (rc != 0):
        self.module.fail_json(msg=err)
    config = (out.strip() if out else '')
    if (cmd == config):
        return ''
    return config