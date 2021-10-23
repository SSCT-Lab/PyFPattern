def get_end_state(self):
    'get end state info'
    config = self.get_current_config()
    if config:
        if self.rate_limit:
            self.end_state['rate_limit'] = get_rate_limit(config)
        if self.forward_enp_slot:
            self.end_state['forward_enp_slot'] = get_forward_enp(config)
    sflow_dict = self.get_sflow_dict()
    if (not sflow_dict):
        return
    if self.agent_ip:
        self.end_state['agent'] = sflow_dict['agent']
    if self.source_ip:
        self.end_state['source'] = sflow_dict['source']
    if self.collector_id:
        self.end_state['collector'] = sflow_dict['collector']
    if self.export_route:
        self.end_state['export'] = sflow_dict['export']
    if self.sflow_interface:
        self.end_state['sampling'] = sflow_dict['sampling']
        self.end_state['counter'] = sflow_dict['counter']