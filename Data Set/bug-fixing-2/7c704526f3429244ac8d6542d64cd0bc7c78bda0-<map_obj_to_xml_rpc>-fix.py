

def map_obj_to_xml_rpc(self):
    self._log_file_meta.update([('files', {
        'xpath': 'syslog/files',
        'tag': True,
        'operation': 'edit',
    }), ('file', {
        'xpath': 'syslog/files/file',
        'tag': True,
        'operation': 'edit',
        'attrib': 'operation',
    }), ('a:name', {
        'xpath': 'syslog/files/file/file-name',
        'operation': 'edit',
    }), ('file-attrib', {
        'xpath': 'syslog/files/file/file-log-attributes',
        'tag': True,
        'operation': 'edit',
    }), ('a:size', {
        'xpath': 'syslog/files/file/file-log-attributes/max-file-size',
        'operation': 'edit',
    }), ('a:level', {
        'xpath': 'syslog/files/file/file-log-attributes/severity',
        'operation': 'edit',
    })])
    self._log_host_meta.update([('host-server', {
        'xpath': 'syslog/host-server',
        'tag': True,
        'operation': 'edit',
    }), ('vrfs', {
        'xpath': 'syslog/host-server/vrfs',
        'tag': True,
        'operation': 'edit',
    }), ('vrf', {
        'xpath': 'syslog/host-server/vrfs/vrf',
        'tag': True,
        'operation': 'edit',
    }), ('a:vrf', {
        'xpath': 'syslog/host-server/vrfs/vrf/vrf-name',
        'operation': 'edit',
    }), ('ipv4s', {
        'xpath': 'syslog/host-server/vrfs/vrf/ipv4s',
        'tag': True,
        'operation': 'edit',
    }), ('ipv4', {
        'xpath': 'syslog/host-server/vrfs/vrf/ipv4s/ipv4',
        'tag': True,
        'operation': 'edit',
        'attrib': 'operation',
    }), ('a:name', {
        'xpath': 'syslog/host-server/vrfs/vrf/ipv4s/ipv4/address',
        'operation': 'edit',
    }), ('ipv4-sev', {
        'xpath': 'syslog/host-server/vrfs/vrf/ipv4s/ipv4/ipv4-severity-port',
        'tag': True,
        'operation': 'edit',
    }), ('a:level', {
        'xpath': 'syslog/host-server/vrfs/vrf/ipv4s/ipv4/ipv4-severity-port/severity',
        'operation': 'edit',
    })])
    self._log_console_meta.update([('a:enable-console', {
        'xpath': 'syslog/enable-console-logging',
        'operation': 'edit',
        'attrib': 'operation',
    }), ('console', {
        'xpath': 'syslog/console-logging',
        'tag': True,
        'operation': 'edit',
        'attrib': 'operation',
    }), ('a:console-level', {
        'xpath': 'syslog/console-logging/logging-level',
        'operation': 'edit',
    })])
    self._log_monitor_meta.update([('monitor', {
        'xpath': 'syslog/monitor-logging',
        'tag': True,
        'operation': 'edit',
        'attrib': 'operation',
    }), ('a:monitor-level', {
        'xpath': 'syslog/monitor-logging/logging-level',
        'operation': 'edit',
    })])
    self._log_buffered_size_meta.update([('buffered', {
        'xpath': 'syslog/buffered-logging',
        'tag': True,
        'operation': 'edit',
        'attrib': 'operation',
    }), ('a:size', {
        'xpath': 'syslog/buffered-logging/buffer-size',
        'operation': 'edit',
    })])
    self._log_buffered_level_meta.update([('buffered', {
        'xpath': 'syslog/buffered-logging',
        'tag': True,
        'operation': 'edit',
        'attrib': 'operation',
    }), ('a:level', {
        'xpath': 'syslog/buffered-logging/logging-level',
        'operation': 'edit',
    })])
    self._log_facility_meta.update([('facility', {
        'xpath': 'syslog/logging-facilities',
        'tag': True,
        'operation': 'edit',
        'attrib': 'operation',
    }), ('a:facility', {
        'xpath': 'syslog/logging-facilities/facility-level',
        'operation': 'edit',
    })])
    self._log_prefix_meta.update([('a:hostnameprefix', {
        'xpath': 'syslog/host-name-prefix',
        'operation': 'edit',
        'attrib': 'operation',
    })])
    state = self._module.params['state']
    _get_filter = build_xml('syslog', opcode='filter')
    running = get_config(self._module, source='running', config_filter=_get_filter)
    file_ele = etree_findall(running, 'file')
    file_list = list()
    if len(file_ele):
        for file in file_ele:
            file_name = etree_find(file, 'file-name')
            file_list.append((file_name.text if (file_name is not None) else None))
    vrf_ele = etree_findall(running, 'vrf')
    host_list = list()
    for vrf in vrf_ele:
        host_ele = etree_findall(vrf, 'ipv4')
        for host in host_ele:
            host_name = etree_find(host, 'address')
            host_list.append((host_name.text if (host_name is not None) else None))
    console_ele = etree_find(running, 'console-logging')
    console_level = (etree_find(console_ele, 'logging-level') if (console_ele is not None) else None)
    have_console = (console_level.text if (console_level is not None) else None)
    monitor_ele = etree_find(running, 'monitor-logging')
    monitor_level = (etree_find(monitor_ele, 'logging-level') if (monitor_ele is not None) else None)
    have_monitor = (monitor_level.text if (monitor_level is not None) else None)
    buffered_ele = etree_find(running, 'buffered-logging')
    buffered_size = (etree_find(buffered_ele, 'buffer-size') if (buffered_ele is not None) else None)
    have_buffered = (buffered_size.text if (buffered_size is not None) else None)
    facility_ele = etree_find(running, 'logging-facilities')
    facility_level = (etree_find(facility_ele, 'facility-level') if (facility_ele is not None) else None)
    have_facility = (facility_level.text if (facility_level is not None) else None)
    prefix_ele = etree_find(running, 'host-name-prefix')
    have_prefix = (prefix_ele.text if (prefix_ele is not None) else None)
    file_params = list()
    host_params = list()
    console_params = dict()
    monitor_params = dict()
    buffered_params = dict()
    facility_params = dict()
    prefix_params = dict()
    opcode = None
    if (state == 'absent'):
        opcode = 'delete'
        for item in self._want:
            if ((item['dest'] == 'file') and (item['name'] in file_list)):
                item['level'] = severity_level[item['level']]
                file_params.append(item)
            elif ((item['dest'] == 'host') and (item['name'] in host_list)):
                item['level'] = severity_level[item['level']]
                host_params.append(item)
            elif ((item['dest'] == 'console') and have_console):
                console_params.update({
                    'console-level': item['level'],
                })
            elif ((item['dest'] == 'monitor') and have_monitor):
                monitor_params.update({
                    'monitor-level': item['level'],
                })
            elif ((item['dest'] == 'buffered') and have_buffered):
                buffered_params['size'] = (str(item['size']) if item['size'] else None)
                buffered_params['level'] = (item['level'] if item['level'] else None)
            elif ((item['dest'] is None) and (item['hostnameprefix'] is None) and (item['facility'] is not None) and have_facility):
                facility_params.update({
                    'facility': item['facility'],
                })
            elif ((item['dest'] is None) and (item['hostnameprefix'] is not None) and have_prefix):
                prefix_params.update({
                    'hostnameprefix': item['hostnameprefix'],
                })
    elif (state == 'present'):
        opcode = 'merge'
        for item in self._want:
            if (item['dest'] == 'file'):
                item['level'] = severity_level[item['level']]
                file_params.append(item)
            elif (item['dest'] == 'host'):
                item['level'] = severity_level[item['level']]
                host_params.append(item)
            elif (item['dest'] == 'console'):
                console_params.update({
                    'console-level': item['level'],
                })
            elif (item['dest'] == 'monitor'):
                monitor_params.update({
                    'monitor-level': item['level'],
                })
            elif (item['dest'] == 'buffered'):
                buffered_params['size'] = (str(item['size']) if item['size'] else None)
                buffered_params['level'] = (item['level'] if item['level'] else None)
            elif ((item['dest'] is None) and (item['hostnameprefix'] is None) and (item['facility'] is not None)):
                facility_params.update({
                    'facility': item['facility'],
                })
            elif ((item['dest'] is None) and (item['hostnameprefix'] is not None)):
                prefix_params.update({
                    'hostnameprefix': item['hostnameprefix'],
                })
    self._result['xml'] = []
    _edit_filter_list = list()
    if opcode:
        if len(file_params):
            _edit_filter_list.append(build_xml('syslog', xmap=self._log_file_meta, params=file_params, opcode=opcode))
        if len(host_params):
            _edit_filter_list.append(build_xml('syslog', xmap=self._log_host_meta, params=host_params, opcode=opcode))
        if len(console_params):
            _edit_filter_list.append(build_xml('syslog', xmap=self._log_console_meta, params=console_params, opcode=opcode))
        if len(monitor_params):
            _edit_filter_list.append(build_xml('syslog', xmap=self._log_monitor_meta, params=monitor_params, opcode=opcode))
        if len(buffered_params):
            _edit_filter_list.append(build_xml('syslog', xmap=self._log_buffered_size_meta, params=buffered_params, opcode=opcode))
            _edit_filter_list.append(build_xml('syslog', xmap=self._log_buffered_level_meta, params=buffered_params, opcode=opcode))
        if len(facility_params):
            _edit_filter_list.append(build_xml('syslog', xmap=self._log_facility_meta, params=facility_params, opcode=opcode))
        if len(prefix_params):
            _edit_filter_list.append(build_xml('syslog', xmap=self._log_prefix_meta, params=prefix_params, opcode=opcode))
        diff = None
        if len(_edit_filter_list):
            commit = (not self._module.check_mode)
            diff = load_config(self._module, _edit_filter_list, commit=commit, running=running, nc_get_filter=_get_filter)
        if diff:
            if self._module._diff:
                self._result['diff'] = dict(prepared=diff)
            self._result['xml'] = _edit_filter_list
            self._result['changed'] = True
