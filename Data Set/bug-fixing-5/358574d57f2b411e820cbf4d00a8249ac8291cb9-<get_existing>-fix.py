def get_existing(self):
    'get existing info'
    if (not self.sflow_dict):
        return
    if self.agent_ip:
        self.existing['agent'] = self.sflow_dict['agent']
    if self.source_ip:
        self.existing['source'] = self.sflow_dict['source']
    if self.collector_id:
        self.existing['collector'] = self.sflow_dict['collector']
    if self.export_route:
        self.existing['export'] = self.sflow_dict['export']
    if self.sflow_interface:
        self.existing['sampling'] = self.sflow_dict['sampling']
        self.existing['counter'] = self.sflow_dict['counter']