def check_params(self):
    'Check all input params'
    if self.agent_ip:
        self.agent_ip = self.agent_ip.upper()
        if (not check_ip_addr(self.agent_ip)):
            self.module.fail_json(msg='Error: agent_ip is invalid.')
    if self.source_ip:
        self.source_ip = self.source_ip.upper()
        if (not check_ip_addr(self.source_ip)):
            self.module.fail_json(msg='Error: source_ip is invalid.')
    if self.collector_id:
        if self.collector_ip:
            self.collector_ip = self.collector_ip.upper()
            if (not check_ip_addr(self.collector_ip)):
                self.module.fail_json(msg='Error: collector_ip is invalid.')
            if (self.collector_ip_vpn and (not is_valid_ip_vpn(self.collector_ip_vpn))):
                self.module.fail_json(msg='Error: collector_ip_vpn is invalid.')
        if self.collector_datagram_size:
            if (not self.collector_datagram_size.isdigit()):
                self.module.fail_json(msg='Error: collector_datagram_size is not digit.')
            if ((int(self.collector_datagram_size) < 1024) or (int(self.collector_datagram_size) > 8100)):
                self.module.fail_json(msg='Error: collector_datagram_size is not ranges from 1024 to 8100.')
        if self.collector_udp_port:
            if (not self.collector_udp_port.isdigit()):
                self.module.fail_json(msg='Error: collector_udp_port is not digit.')
            if ((int(self.collector_udp_port) < 1) or (int(self.collector_udp_port) > 65535)):
                self.module.fail_json(msg='Error: collector_udp_port is not ranges from 1 to 65535.')
        if self.collector_description:
            if self.collector_description.count(' '):
                self.module.fail_json(msg='Error: collector_description should without spaces.')
            if ((len(self.collector_description) < 1) or (len(self.collector_description) > 255)):
                self.module.fail_json(msg='Error: collector_description is not ranges from 1 to 255.')
    if self.sflow_interface:
        intf_type = get_interface_type(self.sflow_interface)
        if (not intf_type):
            self.module.fail_json(msg='Error: intf_type is invalid.')
        if (intf_type not in ['ge', '10ge', '25ge', '4x10ge', '40ge', '100ge', 'eth-trunk']):
            self.module.fail_json(msg=('Error: interface %s is not support sFlow.' % self.sflow_interface))
        if self.sample_collector:
            self.sample_collector.sort()
            if (self.sample_collector not in [['1'], ['2'], ['1', '2']]):
                self.module.fail_json(msg='Error: sample_collector is invalid.')
        if self.sample_rate:
            if (not self.sample_rate.isdigit()):
                self.module.fail_json(msg='Error: sample_rate is not digit.')
            if ((int(self.sample_rate) < 1) or (int(self.sample_rate) > 4294967295)):
                self.module.fail_json(msg='Error: sample_rate is not ranges from 1 to 4294967295.')
        if self.sample_length:
            if (not self.sample_length.isdigit()):
                self.module.fail_json(msg='Error: sample_rate is not digit.')
            if ((int(self.sample_length) < 18) or (int(self.sample_length) > 512)):
                self.module.fail_json(msg='Error: sample_length is not ranges from 18 to 512.')
        if self.counter_collector:
            self.counter_collector.sort()
            if (self.counter_collector not in [['1'], ['2'], ['1', '2']]):
                self.module.fail_json(msg='Error: counter_collector is invalid.')
        if self.counter_interval:
            if (not self.counter_interval.isdigit()):
                self.module.fail_json(msg='Error: counter_interval is not digit.')
            if ((int(self.counter_interval) < 10) or (int(self.counter_interval) > 4294967295)):
                self.module.fail_json(msg='Error: sample_length is not ranges from 10 to 4294967295.')
    if self.rate_limit:
        if (not self.rate_limit.isdigit()):
            self.module.fail_json(msg='Error: rate_limit is not digit.')
        if ((int(self.rate_limit) < 100) or (int(self.rate_limit) > 1500)):
            self.module.fail_json(msg='Error: rate_limit is not ranges from 100 to 1500.')
        if (self.rate_limit_slot and (not self.rate_limit_slot.isdigit())):
            self.module.fail_json(msg='Error: rate_limit_slot is not digit.')
    if self.forward_enp_slot:
        self.forward_enp_slot.lower()
        if ((not self.forward_enp_slot.isdigit()) and (self.forward_enp_slot != 'all')):
            self.module.fail_json(msg='Error: forward_enp_slot is invalid.')