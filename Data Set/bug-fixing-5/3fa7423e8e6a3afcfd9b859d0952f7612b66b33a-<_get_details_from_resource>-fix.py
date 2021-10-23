def _get_details_from_resource(self):
    resource = self.read_current_from_device()
    stats = resource['entries'].copy()
    if HAS_OBJPATH:
        tree = Tree(stats)
    else:
        raise F5ModuleError('objectpath module required, install objectpath module to continue. ')
    details = list(tree.execute('$..*["details"]["description"]'))
    result = details[::(- 1)]
    return result