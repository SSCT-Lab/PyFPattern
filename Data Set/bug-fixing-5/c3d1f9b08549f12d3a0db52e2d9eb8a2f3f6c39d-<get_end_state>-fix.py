def get_end_state(self):
    ' Get end state '
    self.cli_get_stp_config()
    if (self.interface and (self.interface != 'all')):
        self.cli_get_interface_stp_config()
    if self.stp_mode:
        if ('stp mode stp' in self.stp_cfg):
            self.end_state['stp_mode'] = 'stp'
        elif ('stp mode rstp' in self.stp_cfg):
            self.end_state['stp_mode'] = 'rstp'
        else:
            self.end_state['stp_mode'] = 'mstp'
    if self.stp_enable:
        if ('stp disable' in self.stp_cfg):
            self.end_state['stp_enable'] = 'disable'
        else:
            self.end_state['stp_enable'] = 'enable'
    if self.stp_converge:
        if ('stp converge fast' in self.stp_cfg):
            self.end_state['stp_converge'] = 'fast'
        else:
            self.end_state['stp_converge'] = 'normal'
    if self.edged_port:
        if (self.interface == 'all'):
            if ('stp edged-port default' in self.stp_cfg):
                self.end_state['edged_port'] = 'enable'
            else:
                self.end_state['edged_port'] = 'disable'
        elif ('stp edged-port enable' in self.interface_stp_cfg):
            self.end_state['edged_port'] = 'enable'
        else:
            self.end_state['edged_port'] = 'disable'
    if self.bpdu_filter:
        if (self.interface == 'all'):
            if ('stp bpdu-filter default' in self.stp_cfg):
                self.end_state['bpdu_filter'] = 'enable'
            else:
                self.end_state['bpdu_filter'] = 'disable'
        elif ('stp bpdu-filter enable' in self.interface_stp_cfg):
            self.end_state['bpdu_filter'] = 'enable'
        else:
            self.end_state['bpdu_filter'] = 'disable'
    if self.bpdu_protection:
        if ('stp bpdu-protection' in self.stp_cfg):
            self.end_state['bpdu_protection'] = 'enable'
        else:
            self.end_state['bpdu_protection'] = 'disable'
    if self.tc_protection:
        pre_cfg = self.stp_cfg.split('\n')
        if ('stp tc-protection' in pre_cfg):
            self.end_state['tc_protection'] = 'enable'
        else:
            self.end_state['tc_protection'] = 'disable'
    if self.tc_protection_interval:
        if ('stp tc-protection interval' in self.stp_cfg):
            tmp_value = re.findall('stp tc-protection interval (.*)', self.stp_cfg)
            if (not tmp_value):
                self.module.fail_json(msg='Error: Can not find tc-protection interval on the device.')
            self.end_state['tc_protection_interval'] = tmp_value[0]
        else:
            self.end_state['tc_protection_interval'] = 'null'
    if self.tc_protection_threshold:
        if ('stp tc-protection threshold' in self.stp_cfg):
            tmp_value = re.findall('stp tc-protection threshold (.*)', self.stp_cfg)
            if (not tmp_value):
                self.module.fail_json(msg='Error: Can not find tc-protection threshold on the device.')
            self.end_state['tc_protection_threshold'] = tmp_value[0]
        else:
            self.end_state['tc_protection_threshold'] = '1'
    if self.cost:
        tmp_value = re.findall('stp instance (.*) cost (.*)', self.interface_stp_cfg)
        if (not tmp_value):
            self.end_state['cost'] = 'null'
        else:
            self.end_state['cost'] = tmp_value[0][1]
    if (self.root_protection or self.loop_protection):
        if ('stp root-protection' in self.interface_stp_cfg):
            self.end_state['root_protection'] = 'enable'
        else:
            self.end_state['root_protection'] = 'disable'
        if ('stp loop-protection' in self.interface_stp_cfg):
            self.end_state['loop_protection'] = 'enable'
        else:
            self.end_state['loop_protection'] = 'disable'
    if (self.existing == self.end_state):
        self.changed = False
        self.updates_cmd = list()