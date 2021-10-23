def work(self):
    'worker'
    self.check_params()
    self.sflow_dict = self.get_sflow_dict()
    self.get_existing()
    self.get_proposed()
    xml_str = ''
    if self.export_route:
        xml_str += self.config_export()
    if self.agent_ip:
        xml_str += self.config_agent()
    if self.source_ip:
        xml_str += self.config_source()
    if (self.state == 'present'):
        if (self.collector_id and self.collector_ip):
            xml_str += self.config_collector()
        if self.sflow_interface:
            xml_str += self.config_sampling()
            xml_str += self.config_counter()
    else:
        if self.sflow_interface:
            xml_str += self.config_sampling()
            xml_str += self.config_counter()
        if self.collector_id:
            xml_str += self.config_collector()
    if xml_str:
        self.netconf_load_config(xml_str)
        self.changed = True
    self.get_end_state()
    self.results['changed'] = self.changed
    self.results['proposed'] = self.proposed
    self.results['existing'] = self.existing
    self.results['end_state'] = self.end_state
    if self.changed:
        self.results['updates'] = self.updates_cmd
    else:
        self.results['updates'] = list()
    self.module.exit_json(**self.results)