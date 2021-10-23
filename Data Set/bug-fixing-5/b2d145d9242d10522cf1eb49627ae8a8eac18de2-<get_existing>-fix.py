def get_existing(self):
    'get existing info'
    self.mlag_info = self.get_mlag_info()
    self.mlag_global_info = self.get_mlag_global_info()
    self.mlag_error_down_info = self.get_mlag_error_down_info()
    if (self.eth_trunk_id or self.dfs_group_id or self.mlag_id):
        if ((not self.mlag_system_id) and (not self.mlag_priority_id)):
            if self.mlag_info:
                self.existing['mlagInfos'] = self.mlag_info['mlagInfos']
    if (self.mlag_system_id or self.mlag_priority_id):
        if self.eth_trunk_id:
            if self.mlag_trunk_attribute_info:
                if self.mlag_system_id:
                    self.existing['lacpMlagSysId'] = self.mlag_trunk_attribute_info['lacpMlagSysId']
                if self.mlag_priority_id:
                    self.existing['lacpMlagPriority'] = self.mlag_trunk_attribute_info['lacpMlagPriority']
        elif self.mlag_global_info:
            if self.mlag_system_id:
                self.existing['lacpMlagSysId'] = self.mlag_global_info['lacpMlagSysId']
            if self.mlag_priority_id:
                self.existing['lacpMlagPriority'] = self.mlag_global_info['lacpMlagPriority']
    if (self.interface or self.mlag_error_down):
        if self.mlag_error_down_info:
            self.existing['mlagErrorDownInfos'] = self.mlag_error_down_info['mlagErrorDownInfos']