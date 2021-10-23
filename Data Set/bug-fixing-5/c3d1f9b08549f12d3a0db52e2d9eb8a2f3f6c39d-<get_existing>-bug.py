def get_existing(self):
    ' Get existing configuration '
    self.cli_get_stp_config()
    if (self.interface and (self.interface != 'all')):
        self.cli_get_interface_stp_config()
    if self.stp_mode:
        if ('stp mode stp' in self.stp_cfg):
            self.cur_cfg['stp_mode'] = 'stp'
            self.existing['stp_mode'] = 'stp'
        elif ('stp mode rstp' in self.stp_cfg):
            self.cur_cfg['stp_mode'] = 'rstp'
            self.existing['stp_mode'] = 'rstp'
        else:
            self.cur_cfg['stp_mode'] = 'mstp'
            self.existing['stp_mode'] = 'mstp'
    if self.stp_enable:
        if ('stp disable' in self.stp_cfg):
            self.cur_cfg['stp_enable'] = 'disable'
            self.existing['stp_enable'] = 'disable'
        else:
            self.cur_cfg['stp_enable'] = 'enable'
            self.existing['stp_enable'] = 'enable'
    if self.stp_converge:
        if ('stp converge fast' in self.stp_cfg):
            self.cur_cfg['stp_converge'] = 'fast'
            self.existing['stp_converge'] = 'fast'
        else:
            self.cur_cfg['stp_converge'] = 'normal'
            self.existing['stp_converge'] = 'normal'
    if self.edged_port:
        if (self.interface == 'all'):
            if ('stp edged-port default' in self.stp_cfg):
                self.cur_cfg['edged_port'] = 'enable'
                self.existing['edged_port'] = 'enable'
            else:
                self.cur_cfg['edged_port'] = 'disable'
                self.existing['edged_port'] = 'disable'
        elif ('stp edged-port enable' in self.interface_stp_cfg):
            self.cur_cfg['edged_port'] = 'enable'
            self.existing['edged_port'] = 'enable'
        else:
            self.cur_cfg['edged_port'] = 'disable'
            self.existing['edged_port'] = 'disable'
    if self.bpdu_filter:
        if (self.interface == 'all'):
            if ('stp bpdu-filter default' in self.stp_cfg):
                self.cur_cfg['bpdu_filter'] = 'enable'
                self.existing['bpdu_filter'] = 'enable'
            else:
                self.cur_cfg['bpdu_filter'] = 'disable'
                self.existing['bpdu_filter'] = 'disable'
        elif ('stp bpdu-filter enable' in self.interface_stp_cfg):
            self.cur_cfg['bpdu_filter'] = 'enable'
            self.existing['bpdu_filter'] = 'enable'
        else:
            self.cur_cfg['bpdu_filter'] = 'disable'
            self.existing['bpdu_filter'] = 'disable'
    if self.bpdu_protection:
        if ('stp bpdu-protection' in self.stp_cfg):
            self.cur_cfg['bpdu_protection'] = 'enable'
            self.existing['bpdu_protection'] = 'enable'
        else:
            self.cur_cfg['bpdu_protection'] = 'disable'
            self.existing['bpdu_protection'] = 'disable'
    if self.tc_protection:
        if ('stp tc-protection' in self.stp_cfg):
            self.cur_cfg['tc_protection'] = 'enable'
            self.existing['tc_protection'] = 'enable'
        else:
            self.cur_cfg['tc_protection'] = 'disable'
            self.existing['tc_protection'] = 'disable'
    if self.tc_protection_interval:
        if ('stp tc-protection interval' in self.stp_cfg):
            tmp_value = re.findall('stp tc-protection interval (.*)', self.stp_cfg)
            if (not tmp_value):
                self.module.fail_json(msg='Error: Can not find tc-protection interval on the device.')
            self.cur_cfg['tc_protection_interval'] = tmp_value[0]
            self.existing['tc_protection_interval'] = tmp_value[0]
        else:
            self.cur_cfg['tc_protection_interval'] = 'null'
            self.existing['tc_protection_interval'] = 'null'
    if self.tc_protection_threshold:
        if ('stp tc-protection threshold' in self.stp_cfg):
            tmp_value = re.findall('stp tc-protection threshold (.*)', self.stp_cfg)
            if (not tmp_value):
                self.module.fail_json(msg='Error: Can not find tc-protection threshold on the device.')
            self.cur_cfg['tc_protection_threshold'] = tmp_value[0]
            self.existing['tc_protection_threshold'] = tmp_value[0]
        else:
            self.cur_cfg['tc_protection_threshold'] = '1'
            self.existing['tc_protection_threshold'] = '1'
    if self.cost:
        tmp_value = re.findall('stp instance (.*) cost (.*)', self.interface_stp_cfg)
        if (not tmp_value):
            self.cur_cfg['cost'] = 'null'
            self.existing['cost'] = 'null'
        else:
            self.cur_cfg['cost'] = tmp_value[0][1]
            self.existing['cost'] = tmp_value[0][1]
    if (self.root_protection or self.loop_protection):
        if ('stp root-protection' in self.interface_stp_cfg):
            self.cur_cfg['root_protection'] = 'enable'
            self.existing['root_protection'] = 'enable'
        else:
            self.cur_cfg['root_protection'] = 'disable'
            self.existing['root_protection'] = 'disable'
        if ('stp loop-protection' in self.interface_stp_cfg):
            self.cur_cfg['loop_protection'] = 'enable'
            self.existing['loop_protection'] = 'enable'
        else:
            self.cur_cfg['loop_protection'] = 'disable'
            self.existing['loop_protection'] = 'disable'