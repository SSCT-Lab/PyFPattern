

def list_items(self):
    'Get all load balancers'
    self.log('List all load balancers')
    if self.resource_group:
        try:
            response = self.network_client.load_balancers.list(self.resource_group)
        except AzureHttpError as exc:
            self.fail('Failed to list items in resource group {} - {}'.format(self.resource_group, str(exc)))
    else:
        try:
            response = self.network_client.load_balancers.list_all()
        except AzureHttpError as exc:
            self.fail('Failed to list all items - {}'.format(str(exc)))
    results = []
    for item in response:
        if self.has_tags(item.tags, self.tags):
            results.append(self.serialize_obj(item, AZURE_OBJECT_CLASS))
    return results
