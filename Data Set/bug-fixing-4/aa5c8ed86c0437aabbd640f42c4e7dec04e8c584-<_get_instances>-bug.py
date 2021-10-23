def _get_instances(self, inkwargs):
    ' Make API calls without VCR fixtures '
    instances = []
    si = SmartConnect(**inkwargs)
    if (not si):
        print('Could not connect to the specified host using specified username and password')
        return (- 1)
    atexit.register(Disconnect, si)
    content = si.RetrieveContent()
    for child in content.rootFolder.childEntity:
        instances += self._get_instances_from_children(child)
    if self.args.max_instances:
        if (len(instances) >= (self.args.max_instances + 1)):
            instances = instances[0:(self.args.max_instances + 1)]
    instance_tuples = []
    for instance in sorted(instances):
        ifacts = self.facts_from_vobj(instance)
        instance_tuples.append((instance, ifacts))
    return instance_tuples