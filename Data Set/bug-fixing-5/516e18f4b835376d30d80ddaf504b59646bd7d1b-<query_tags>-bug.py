def query_tags(self, resource, resource_type):
    args = {
        'resourceids': resource['id'],
        'resourcetype': resource_type,
    }
    tags = self.query_api('listTags', **args)
    return self.get_tags(resource=tags, key='tag')