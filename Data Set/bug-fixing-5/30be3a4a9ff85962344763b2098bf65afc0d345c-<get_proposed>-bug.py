def get_proposed(self):
    'get proposed info'
    if self.agent_ip:
        self.proposed['agent_ip'] = self.agent_ip
    if self.source_ip:
        self.proposed['source_ip'] = self.source_ip
    if self.export_route:
        self.proposed['export_route'] = self.export_route
    if self.collector_id:
        self.proposed['collector_id'] = self.collector_id
        if self.collector_ip:
            self.proposed['collector_ip'] = self.collector_ip
            self.proposed['collector_ip_vpn'] = self.collector_ip_vpn
        if self.collector_datagram_size:
            self.proposed['collector_datagram_size'] = self.collector_datagram_size
        if self.collector_udp_port:
            self.proposed['collector_udp_port'] = self.collector_udp_port
        if self.collector_meth:
            self.proposed['collector_meth'] = self.collector_meth
        if self.collector_description:
            self.proposed['collector_description'] = self.collector_description
    if self.sflow_interface:
        self.proposed['sflow_interface'] = self.sflow_interface
        if self.sample_collector:
            self.proposed['sample_collector'] = self.sample_collector
        if self.sample_rate:
            self.proposed['sample_rate'] = self.sample_rate
        if self.sample_length:
            self.proposed['sample_length'] = self.sample_length
        if self.sample_direction:
            self.proposed['sample_direction'] = self.sample_direction
        if self.counter_collector:
            self.proposed['counter_collector'] = self.counter_collector
        if self.counter_interval:
            self.proposed['counter_interval'] = self.counter_interval
    self.proposed['state'] = self.state