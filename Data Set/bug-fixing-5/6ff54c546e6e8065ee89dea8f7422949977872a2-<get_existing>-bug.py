def get_existing(self):
    'get existing info'
    if (not self.startup_info):
        return
    self.existing['StartupInfos'] = self.startup_info['StartupInfos']