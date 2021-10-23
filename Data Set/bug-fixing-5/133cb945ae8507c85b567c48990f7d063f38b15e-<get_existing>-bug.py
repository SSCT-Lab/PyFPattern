def get_existing(self):
    'get existing info'
    if (not self.rollback_info):
        return
    self.existing['RollBackInfos'] = self.rollback_info['RollBackInfos']