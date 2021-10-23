def set_jumboframe(self):
    ' set_jumboframe'
    if (self.state == 'present'):
        if ((not self.jbf_max) and (not self.jbf_min)):
            return
        jbf_value = self.get_jumboframe_config()
        self.jbf_config = copy.deepcopy(jbf_value)
        if (len(jbf_value) == 1):
            jbf_value.append('1518')
            self.jbf_config.append('1518')
        if (not self.jbf_max):
            return
        if ((len(jbf_value) > 2) or (len(jbf_value) == 0)):
            self.module.fail_json(msg='Error: Get jubmoframe config value num error.')
        if (self.jbf_min is None):
            if (jbf_value[0] == self.jbf_max):
                return
        elif ((jbf_value[0] == self.jbf_max) and (jbf_value[1] == self.jbf_min)):
            return
        if (jbf_value[0] != self.jbf_max):
            jbf_value[0] = self.jbf_max
        if ((jbf_value[1] != self.jbf_min) and (self.jbf_min is not None)):
            jbf_value[1] = self.jbf_min
        else:
            jbf_value.pop(1)
    else:
        jbf_value = self.get_jumboframe_config()
        self.jbf_config = copy.deepcopy(jbf_value)
        if (jbf_value == [9216, 1518]):
            return
        jbf_value = [9216, 1518]
    command = ('interface %s' % self.interface)
    self.cli_add_command(command)
    if (len(jbf_value) == 2):
        self.jbf_cli = ('jumboframe enable %s %s' % (jbf_value[0], jbf_value[1]))
    else:
        self.jbf_cli = ('jumboframe enable %s' % jbf_value[0])
    self.cli_add_command(self.jbf_cli)
    if self.commands:
        self.cli_load_config(self.commands)
        self.changed = True
    if (self.state == 'present'):
        if self.jbf_min:
            self.updates_cmd.append(('jumboframe enable %s %s' % (self.jbf_max, self.jbf_min)))
        else:
            self.updates_cmd.append(('jumboframe enable %s' % self.jbf_max))
    else:
        self.updates_cmd.append('undo jumboframe enable')
    return