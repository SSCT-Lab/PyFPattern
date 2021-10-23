def get_blob_client(self, resource_group_name, storage_account_name, storage_blob_type='block'):
    keys = dict()
    try:
        self.log('Getting keys')
        account_keys = self.storage_client.storage_accounts.list_keys(resource_group_name, storage_account_name)
    except Exception as exc:
        self.fail('Error getting keys for account {0} - {1}'.format(storage_account_name, str(exc)))
    try:
        self.log('Create blob service')
        if (storage_blob_type == 'page'):
            return PageBlobService(endpoint_suffix=self._cloud_environment.suffixes.storage_endpoint, account_name=storage_account_name, account_key=account_keys.keys[0].value)
        elif (storage_blob_type == 'block'):
            return BlockBlobService(endpoint_suffix=self._cloud_environment.suffixes.storage_endpoint, account_name=storage_account_name, account_key=account_keys.keys[0].value)
        else:
            raise Exception('Invalid storage blob type defined.')
    except Exception as exc:
        self.fail('Error creating blob service client for storage account {0} - {1}'.format(storage_account_name, str(exc)))