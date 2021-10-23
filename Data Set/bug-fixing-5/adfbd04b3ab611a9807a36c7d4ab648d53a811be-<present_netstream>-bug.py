def present_netstream(self):
    ' Present netstream configuration '
    cmds = list()
    need_create_record = False
    if (self.type == 'ip'):
        cmd = ('netstream record %s ip' % self.record_name)
    else:
        cmd = ('netstream record %s vxlan inner-ip' % self.record_name)
    cmds.append(cmd)
    if (not self.netstream_cfg):
        self.updates_cmd.append(cmd)
        need_create_record = True
    if self.description:
        cmd = ('description %s' % self.description)
        if ((not self.netstream_cfg) or (cmd not in self.netstream_cfg)):
            cmds.append(cmd)
            self.updates_cmd.append(cmd)
    if self.match:
        if (self.type == 'ip'):
            cmd = ('match ip %s' % self.match)
            cfg = 'match ip'
        else:
            cmd = ('match inner-ip %s' % self.match)
            cfg = 'match inner-ip'
        if ((not self.netstream_cfg) or (cfg not in self.netstream_cfg) or (self.match != self.existing['match'][0])):
            cmds.append(cmd)
            self.updates_cmd.append(cmd)
    if self.collect_counter:
        cmd = ('collect counter %s' % self.collect_counter)
        if ((not self.netstream_cfg) or (cmd not in self.netstream_cfg)):
            cmds.append(cmd)
            self.updates_cmd.append(cmd)
    if self.collect_interface:
        cmd = ('collect interface %s' % self.collect_interface)
        if ((not self.netstream_cfg) or (cmd not in self.netstream_cfg)):
            cmds.append(cmd)
            self.updates_cmd.append(cmd)
    if ((not need_create_record) and (len(cmds) == 1)):
        if (self.type == 'ip'):
            cmd = ('netstream record %s ip' % self.record_name)
        else:
            cmd = ('netstream record %s vxlan inner-ip' % self.record_name)
        cmds.remove(cmd)
    if cmds:
        self.cli_load_config(cmds)
        self.changed = True