

def _update_server(self, server=None, start_server=True):
    server = self._update_auto_backups_setting(server=server, start_server=start_server)
    server = self._update_ipv6_setting(server=server, start_server=start_server)
    server = self._update_private_network_setting(server=server, start_server=start_server)
    server = self._update_plan_setting(server=server, start_server=start_server)
    user_data = self.get_user_data()
    server_user_data = self.get_server_user_data(server=server)
    if ((user_data is not None) and (user_data != server_user_data)):
        self.result['changed'] = True
        self.result['diff']['before']['tag'] = server_user_data
        self.result['diff']['after']['tag'] = user_data
        if (not self.module.check_mode):
            data = {
                'SUBID': server['SUBID'],
                'userdata': user_data,
            }
            self.api_query(path='/v1/server/set_user_data', method='POST', data=data)
    tag = self.module.params.get('tag')
    if ((tag is not None) and (tag != server.get('tag'))):
        self.result['changed'] = True
        self.result['diff']['before']['tag'] = server.get('tag')
        self.result['diff']['after']['tag'] = tag
        if (not self.module.check_mode):
            data = {
                'SUBID': server['SUBID'],
                'tag': tag,
            }
            self.api_query(path='/v1/server/tag_set', method='POST', data=data)
    firewall_group = self.get_firewall_group()
    if (firewall_group and (firewall_group.get('description') != server.get('firewall_group'))):
        self.result['changed'] = True
        self.result['diff']['before']['firewall_group'] = server.get('firewall_group')
        self.result['diff']['after']['firewall_group'] = firewall_group.get('description')
        if (not self.module.check_mode):
            data = {
                'SUBID': server['SUBID'],
                'FIREWALLGROUPID': firewall_group.get('FIREWALLGROUPID'),
            }
            self.api_query(path='/v1/server/firewall_group_set', method='POST', data=data)
    if (not self.module.check_mode):
        if ((self.server_power_state in ['starting', 'running']) and start_server):
            server = self.start_server(skip_results=True)
    server = self._wait_for_state(key='server_state', state='ok')
    return server
