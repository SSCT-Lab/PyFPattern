def get_existing(self):
    'get existing info'
    if self.dfs_group_id:
        self.dfs_group_info = self.get_dfs_group_info()
    if (self.peer_link_id and self.eth_trunk_id):
        self.peer_link_info = self.get_peer_link_info()
    if self.dfs_group_info:
        if self.dfs_group_id:
            self.existing['dfs_group_id'] = self.dfs_group_info['groupId']
        if self.nickname:
            self.existing['nickname'] = self.dfs_group_info['localNickname']
        if self.pseudo_nickname:
            self.existing['pseudo_nickname'] = self.dfs_group_info['pseudoNickname']
        if self.pseudo_priority:
            self.existing['pseudo_priority'] = self.dfs_group_info['pseudoPriority']
        if self.ip_address:
            self.existing['ip_address'] = self.dfs_group_info['ipAddress']
        if self.vpn_instance_name:
            self.existing['vpn_instance_name'] = self.dfs_group_info['srcVpnName']
        if self.priority_id:
            self.existing['priority_id'] = self.dfs_group_info['priority']
    if self.peer_link_info:
        if self.eth_trunk_id:
            self.existing['eth_trunk_id'] = self.peer_link_info['portName']
        if self.peer_link_id:
            self.existing['peer_link_id'] = self.peer_link_info['linkId']