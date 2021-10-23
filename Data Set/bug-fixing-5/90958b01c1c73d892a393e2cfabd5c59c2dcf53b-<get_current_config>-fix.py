def get_current_config(self):
    'get current configuration'
    cmd = ('display current-configuration | section include bgp %s' % self.bgp_instance)
    (rc, out, err) = exec_command(self.module, cmd)
    if (rc != 0):
        self.module.fail_json(msg=err)
    return out