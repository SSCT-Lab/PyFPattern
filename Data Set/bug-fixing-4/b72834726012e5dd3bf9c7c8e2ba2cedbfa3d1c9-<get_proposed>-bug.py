def get_proposed(self):
    'get proposed info'
    self.proposed['session_name'] = self.session_name
    self.proposed['create_type'] = self.create_type
    self.proposed['addr_type'] = self.addr_type
    self.proposed['out_if_name'] = self.out_if_name
    self.proposed['dest_addr'] = self.dest_addr
    self.proposed['src_addr'] = self.src_addr
    self.proposed['vrf_name'] = self.vrf_name
    self.proposed['use_default_ip'] = self.use_default_ip
    self.proposed['state'] = self.state