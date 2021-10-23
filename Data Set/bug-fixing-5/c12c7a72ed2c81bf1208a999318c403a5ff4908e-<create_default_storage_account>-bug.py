def create_default_storage_account(self):
    '\n        Create a default storage account <vm name>XXXX, where XXXX is a random number. If <vm name>XXXX exists, use it.\n        Otherwise, create one.\n\n        :return: storage account object\n        '
    account = None
    valid_name = False
    storage_account_name_base = self.name[:20].lower()
    for i in range(0, 5):
        rand = random.randrange(1000, 9999)
        storage_account_name = (storage_account_name_base + str(rand))
        if self.check_storage_account_name(storage_account_name):
            valid_name = True
            break
    if (not valid_name):
        self.fail('Failed to create a unique storage account name for {0}. Try using a different VM name.'.format(self.name))
    try:
        account = self.storage_client.storage_accounts.get_properties(self.resource_group, storage_account_name)
    except CloudError:
        pass
    if account:
        self.log('Storage account {0} found.'.format(storage_account_name))
        self.check_provisioning_state(account)
        return account
    sku = Sku(SkuName.standard_lrs)
    Sku.tier = SkuTier.standard
    kind = Kind.storage
    parameters = StorageAccountCreateParameters(sku, kind, self.location)
    self.log('Creating storage account {0} in location {1}'.format(storage_account_name, self.location))
    self.results['actions'].append('Created storage account {0}'.format(storage_account_name))
    try:
        poller = self.storage_client.storage_accounts.create(self.resource_group, storage_account_name, parameters)
        self.get_poller_result(poller)
    except Exception as exc:
        self.fail('Failed to create storage account: {0} - {1}'.format(storage_account_name, str(exc)))
    return self.get_storage_account(storage_account_name)