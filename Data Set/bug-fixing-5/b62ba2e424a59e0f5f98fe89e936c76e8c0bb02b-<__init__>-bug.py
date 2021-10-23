def __init__(self, module):
    super(VMwareHostFactManager, self).__init__(module)
    self.host = find_obj(self.content, [vim.HostSystem], None)
    if (self.host is None):
        self.module.fail_json(msg='Failed to find host system.')