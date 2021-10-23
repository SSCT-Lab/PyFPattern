def check_vswitch_configuration(self):
    host = get_all_objs(self.content, [vim.HostSystem])
    if (not host):
        self.module.fail_json(msg='Unable to find host')
    self.host_system = list(host.keys())[0]
    self.vss = find_vswitch_by_name(self.host_system, self.switch)
    if (self.vss is None):
        return 'absent'
    else:
        return 'present'