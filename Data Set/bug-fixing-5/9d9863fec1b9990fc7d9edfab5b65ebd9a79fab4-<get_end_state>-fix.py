def get_end_state(self):
    'get end state info'
    ospf_info = self.get_ospf_dict(self.process_id)
    if (not ospf_info):
        return
    self.end_state['process_id'] = self.process_id
    self.end_state['areas'] = ospf_info['areas']
    self.end_state['nexthops'] = ospf_info['nexthops']
    self.end_state['max_load_balance'] = ospf_info.get('maxLoadBalancing')
    if (self.end_state == self.existing):
        if ((not self.auth_text_simple) and (not self.auth_text_md5)):
            self.changed = False