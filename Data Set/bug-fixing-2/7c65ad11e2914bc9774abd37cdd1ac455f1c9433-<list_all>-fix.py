

def list_all(self):
    self.log('List all items')
    try:
        response = self.storage_client.storage_accounts.list()
    except Exception as exc:
        self.fail('Error listing all items - {0}'.format(str(exc)))
    return response
