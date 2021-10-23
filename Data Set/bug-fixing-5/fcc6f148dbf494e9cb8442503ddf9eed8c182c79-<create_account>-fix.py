def create_account(self):
    self.log('Creating account {0}'.format(self.name))
    if (not self.location):
        self.fail('Parameter error: location required when creating a storage account.')
    if (not self.account_type):
        self.fail('Parameter error: account_type required when creating a storage account.')
    if ((not self.access_tier) and (self.kind == 'BlobStorage')):
        self.fail('Parameter error: access_tier required when creating a storage account of type BlobStorage.')
    self.check_name_availability()
    self.results['changed'] = True
    if self.check_mode:
        account_dict = dict(location=self.location, account_type=self.account_type, name=self.name, resource_group=self.resource_group, tags=dict())
        if self.tags:
            account_dict['tags'] = self.tags
        return account_dict
    sku = Sku(SkuName(self.account_type))
    sku.tier = (SkuTier.standard if ('Standard' in self.account_type) else SkuTier.premium)
    parameters = StorageAccountCreateParameters(sku, self.kind, self.location, tags=self.tags, access_tier=self.access_tier)
    self.log(str(parameters))
    try:
        poller = self.storage_client.storage_accounts.create(self.resource_group, self.name, parameters)
        self.get_poller_result(poller)
    except CloudError as e:
        self.log('Error creating storage account.')
        self.fail('Failed to create account: {0}'.format(str(e)))
    return self.get_account()