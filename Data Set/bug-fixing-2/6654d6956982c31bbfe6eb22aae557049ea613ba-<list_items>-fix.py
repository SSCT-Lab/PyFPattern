

def list_items(self):
    self.log('List all items')
    try:
        response = self.rm_client.resource_groups.list()
    except CloudError as exc:
        self.fail('Failed to list all items - {0}'.format(str(exc)))
    results = []
    for item in response:
        if self.has_tags(item.tags, self.tags):
            results.append(self.serialize_obj(item, AZURE_OBJECT_CLASS))
    return results
