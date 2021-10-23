def list_items(self):
    'Get all load balancers'
    self.log('List all load balancers')
    try:
        response = self.network_client.load_balancers.list()
    except AzureHttpError as exc:
        self.fail('Failed to list all items - {}'.format(str(exc)))
    results = []
    for item in response:
        if self.has_tags(item.tags, self.tags):
            results.append(self.serialize_obj(item, AZURE_OBJECT_CLASS))
    return results