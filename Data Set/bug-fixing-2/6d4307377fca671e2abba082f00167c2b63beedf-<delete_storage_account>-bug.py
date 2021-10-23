

def delete_storage_account(self, resource_group, name):
    self.log('Delete storage account {0}'.format(name))
    self.results['actions'].append('Deleted storage account {0}'.format(name))
    try:
        self.storage_client.storage_accounts.delete(self.resource_group, name)
    except Exception as exc:
        self.fail('Error deleting storage account {0} - {2}'.format(name, str(exc)))
    return True
