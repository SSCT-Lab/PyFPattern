def get_end_state(self):
    'get end state info'
    if self.dfs_group_id:
        self.dfs_group_info = self.get_dfs_group_info()
    if (self.peer_link_id and self.eth_trunk_id):
        self.peer_link_info = self.get_peer_link_info()
    if self.dfs_group_info:
        if self.dfs_group_id:
            self.end_state['dfs_group_id'] = self.dfs_group_info['groupId']
        if self.nickname:
            self.end_state['nickname'] = self.dfs_group_info['localNickname']
        if self.pseudo_nickname:
            self.end_state['pseudo_nickname'] = self.dfs_group_info['pseudoNickname']
        if self.pseudo_priority:
            self.end_state['pseudo_priority'] = self.dfs_group_info['pseudoPriority']
        if self.ip_address:
            self.end_state['ip_address'] = self.dfs_group_info['ipAddress']
        if self.vpn_instance_name:
            self.end_state['vpn_instance_name'] = self.dfs_group_info['srcVpnName']
        if self.priority_id:
            self.end_state['priority_id'] = self.dfs_group_info['priority']
    if self.peer_link_info:
        if self.eth_trunk_id:
            self.end_state['eth_trunk_id'] = self.peer_link_info['portName']
        if self.peer_link_id:
            self.end_state['peer_link_id'] = self.peer_link_info['linkId']
    if (self.end_state == self.existing):
        self.changed = False