def is_mlag_info_exist(self):
    'whether mlag info exist'
    if (not self.mlag_info):
        return False
    eth_trunk = 'Eth-Trunk'
    eth_trunk += self.eth_trunk_id
    for info in self.mlag_info['mlagInfos']:
        if (info['localMlagPort'] == eth_trunk):
            return True
    return False