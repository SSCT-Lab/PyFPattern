def _get_instances(self, inkwargs):
    ' Make API calls '
    instances = []
    si = SmartConnect(**inkwargs)
    self.debugl('# retrieving instances')
    if (not si):
        print('Could not connect to the specified host using specified username and password')
        return (- 1)
    atexit.register(Disconnect, si)
    content = si.RetrieveContent()
    container = content.rootFolder
    viewType = [vim.VirtualMachine]
    recursive = True
    containerView = content.viewManager.CreateContainerView(container, viewType, recursive)
    children = containerView.view
    for child in children:
        if self.args.max_instances:
            if (len(instances) >= self.args.max_instances):
                break
        instances.append(child)
    self.debugl(('# total instances retrieved %s' % len(instances)))
    instance_tuples = []
    for instance in sorted(instances):
        ifacts = self.facts_from_vobj(instance)
        instance_tuples.append((instance, ifacts))
    return instance_tuples