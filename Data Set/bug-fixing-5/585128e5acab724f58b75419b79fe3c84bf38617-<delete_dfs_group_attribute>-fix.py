def delete_dfs_group_attribute(self):
    'delete dfg group attribute info'
    conf_str = (CE_NC_DELETE_DFS_GROUP_ATTRIBUTE_HEADER % self.dfs_group_id)
    change = False
    if (self.priority_id and (self.dfs_group_info['priority'] == self.priority_id)):
        conf_str += ('<priority>%s</priority>' % self.priority_id)
        change = True
        self.updates_cmd.append(('undo priority %s' % self.priority_id))
    if (self.ip_address and (self.dfs_group_info['ipAddress'] == self.ip_address)):
        if (self.vpn_instance_name and (self.dfs_group_info['srcVpnName'] == self.vpn_instance_name)):
            conf_str += ('<ipAddress>%s</ipAddress>' % self.ip_address)
            conf_str += ('<srcVpnName>%s</srcVpnName>' % self.vpn_instance_name)
            self.updates_cmd.append(('undo source ip %s vpn-instance %s' % (self.ip_address, self.vpn_instance_name)))
        else:
            conf_str += ('<ipAddress>%s</ipAddress>' % self.ip_address)
            self.updates_cmd.append(('undo source ip %s' % self.ip_address))
        change = True
    conf_str += CE_NC_DELETE_DFS_GROUP_ATTRIBUTE_TAIL
    if change:
        self.updates_cmd.append('undo dfs-group 1')
        recv_xml = set_nc_config(self.module, conf_str)
        if ('<ok/>' not in recv_xml):
            self.module.fail_json(msg='Error: Delete DFS group attribute failed.')
        self.changed = True