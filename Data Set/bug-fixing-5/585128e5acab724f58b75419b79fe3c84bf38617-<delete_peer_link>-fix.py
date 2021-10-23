def delete_peer_link(self):
    'delete peer link info'
    eth_trunk_id = 'Eth-Trunk'
    eth_trunk_id += self.eth_trunk_id
    if (self.eth_trunk_id and (eth_trunk_id == self.peer_link_info.get('portName'))):
        conf_str = (CE_NC_DELETE_PEER_LINK_INFO % (self.peer_link_id, eth_trunk_id))
        recv_xml = set_nc_config(self.module, conf_str)
        if ('<ok/>' not in recv_xml):
            self.module.fail_json(msg='Error: Delete peer link failed.')
        self.updates_cmd.append(('undo peer-link %s' % self.peer_link_id))
        self.changed = True