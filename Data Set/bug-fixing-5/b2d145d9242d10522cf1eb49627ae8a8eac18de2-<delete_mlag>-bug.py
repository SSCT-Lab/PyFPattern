def delete_mlag(self):
    'delete mlag info'
    if self.is_mlag_info_exist():
        mlag_port = 'Eth-Trunk'
        mlag_port += self.eth_trunk_id
        conf_str = (CE_NC_DELETE_MLAG_INFO % (self.dfs_group_id, self.mlag_id, mlag_port))
        recv_xml = set_nc_config(self.module, conf_str)
        if ('<ok/>' not in recv_xml):
            self.module.fail_json(msg='Error: delete mlag info failed.')
        self.updates_cmd.append(('interface %s' % mlag_port))
        self.updates_cmd.append(('undo dfs-group %s m-lag %s' % (self.dfs_group_id, self.mlag_id)))
        self.changed = True