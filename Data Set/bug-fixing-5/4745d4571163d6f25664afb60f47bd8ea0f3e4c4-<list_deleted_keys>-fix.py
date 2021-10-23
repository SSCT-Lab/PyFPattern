def list_deleted_keys(self):
    '\n        Lists deleted keys in specific key vault.\n\n        :return: deserialized keys, includes key identifier, attributes and tags.\n        '
    self.log('Get the key vaults in current subscription')
    results = []
    try:
        response = self._client.get_deleted_keys(vault_base_url=self.vault_uri)
        self.log('Response : {0}'.format(response))
        if response:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(deletedkeyitem_to_dict(item))
    except KeyVaultErrorException as e:
        self.log('Did not find key vault in current subscription {0}.'.format(str(e)))
    return results