def get_end_state(self):
    ' Get end state '
    self.cli_get_netstream_config()
    if self.netstream_cfg:
        self.end_state['type'] = self.type
        self.end_state['record_name'] = self.record_name
        if self.description:
            tmp_value = re.findall('description (.*)', self.netstream_cfg)
            if tmp_value:
                self.end_state['description'] = tmp_value[0]
        if self.match:
            if (self.type == 'ip'):
                tmp_value = re.findall('match ip (.*)', self.netstream_cfg)
            else:
                tmp_value = re.findall('match inner-ip (.*)', self.netstream_cfg)
            if tmp_value:
                self.end_state['match'] = tmp_value
        if self.collect_counter:
            tmp_value = re.findall('collect counter (.*)', self.netstream_cfg)
            if tmp_value:
                self.end_state['collect_counter'] = tmp_value
        if self.collect_interface:
            tmp_value = re.findall('collect interface (.*)', self.netstream_cfg)
            if tmp_value:
                self.end_state['collect_interface'] = tmp_value