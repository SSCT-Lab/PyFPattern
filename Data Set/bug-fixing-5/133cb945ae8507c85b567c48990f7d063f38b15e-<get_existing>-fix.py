def get_existing(self):
    'get existing info'
    if (not self.rollback_info):
        self.existing['RollBackInfos'] = None
    else:
        self.existing['RollBackInfos'] = self.rollback_info['RollBackInfos']