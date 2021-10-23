def check_storage_account_name(self, name):
    self.log('Checking storage account name availability for {0}'.format(name))
    try:
        response = self.storage_client.storage_accounts.check_name_availability(name)
    except Exception as exc:
        self.fail('Error checking storage account name availability for {0} - {1}'.format(name, str(exc)))
    return response.name_available