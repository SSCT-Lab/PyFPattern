def get_end_state(self):
    ' Get end state '
    if self.version:
        version = self.get_snmp_version()
        if version:
            self.end_state['version'] = version
    if self.connect_port:
        tmp_cfg = self.xml_get_connect_port()
        if tmp_cfg:
            self.end_state['connect port'] = tmp_cfg
    if self.host_name:
        self.end_state['target host info'] = self.end_netconf_cfg['target_host_info']
    if (self.existing == self.end_state):
        self.changed = False
        self.updates_cmd = list()