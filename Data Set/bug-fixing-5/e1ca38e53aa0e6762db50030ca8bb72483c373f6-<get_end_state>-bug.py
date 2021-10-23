def get_end_state(self):
    ' Get end_state state '
    tmp_cfg = self.cli_get_config()
    if tmp_cfg:
        temp_cfg_lower = tmp_cfg.lower()
        temp_data = tmp_cfg.split('\n')
        temp_data_lower = temp_cfg_lower.split('\n')
        for item in temp_data:
            if ('snmp-agent trap source-port ' in item):
                if self.port_number:
                    item_tmp = item.split('snmp-agent trap source-port ')
                    self.end_state['trap source-port'] = item_tmp[1]
            elif ('snmp-agent trap source ' in item):
                if self.interface_type:
                    item_tmp = item.split('snmp-agent trap source ')
                    self.end_state['trap source interface'] = item_tmp[1]
        if self.feature_name:
            for item in temp_data_lower:
                if (item == 'snmp-agent trap enable'):
                    self.end_state['snmp-agent trap'].append('enable')
                elif (item == 'snmp-agent trap disable'):
                    self.end_state['snmp-agent trap'].append('disable')
                elif ('undo snmp-agent trap enable ' in item):
                    item_tmp = item.split('undo snmp-agent trap enable ')
                    self.end_state['undo snmp-agent trap'].append(item_tmp[1])
                elif ('snmp-agent trap enable ' in item):
                    item_tmp = item.split('snmp-agent trap enable ')
                    self.end_state['snmp-agent trap'].append(item_tmp[1])
        else:
            del self.end_state['snmp-agent trap']
            del self.end_state['undo snmp-agent trap']