def get_existing(self):
    'get existing info'
    if (not self.startup_info):
        self.existing['StartupInfos'] = None
    else:
        self.existing['StartupInfos'] = self.startup_info['StartupInfos']