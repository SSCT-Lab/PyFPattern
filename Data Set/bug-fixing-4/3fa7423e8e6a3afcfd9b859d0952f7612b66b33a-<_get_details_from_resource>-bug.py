def _get_details_from_resource(self):
    resource = self.read_current_from_device()
    stats = resource['entries'].copy()
    tree = Tree(stats)
    details = list(tree.execute('$..*["details"]["description"]'))
    result = details[::(- 1)]
    return result