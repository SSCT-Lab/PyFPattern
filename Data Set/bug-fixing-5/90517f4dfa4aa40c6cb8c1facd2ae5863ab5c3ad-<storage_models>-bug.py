@property
def storage_models(self):
    self.log('Getting storage models...')
    return StorageManagementClient.models('2017-10-01')