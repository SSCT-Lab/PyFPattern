def _get_instances(self, inkwargs):
    ' Make API calls '
    instances = []
    try:
        si = SmartConnect(**inkwargs)
    except ssl.SSLError as connection_error:
        if (('[SSL: CERTIFICATE_VERIFY_FAILED]' in str(connection_error)) and self.validate_certs):
            sys.exit(('Unable to connect to ESXi server due to %s, please specify validate_certs=False and try again' % connection_error))
    except Exception as exc:
        self.debugl(('Unable to connect to ESXi server due to %s' % exc))
        sys.exit(('Unable to connect to ESXi server due to %s' % exc))
    self.debugl('retrieving all instances')
    if (not si):
        sys.exit('Could not connect to the specified host using specified username and password')
    atexit.register(Disconnect, si)
    content = si.RetrieveContent()
    self.debugl('creating containerview for virtualmachines')
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
    self.debugl(('%s total instances in container view' % len(instances)))
    if self.args.host:
        instances = [x for x in instances if (x.name == self.args.host)]
    instance_tuples = []
    for instance in sorted(instances):
        if self.guest_props:
            ifacts = self.facts_from_proplist(instance)
        else:
            ifacts = self.facts_from_vobj(instance)
        instance_tuples.append((instance, ifacts))
    self.debugl('facts collected for all instances')
    try:
        cfm = content.customFieldsManager
        if ((cfm is not None) and cfm.field):
            for f in cfm.field:
                if (f.managedObjectType == vim.VirtualMachine):
                    self.custom_fields[f.key] = f.name
            self.debugl(('%d custom fields collected' % len(self.custom_fields)))
    except vmodl.RuntimeFault as exc:
        self.debugl(('Unable to gather custom fields due to %s' % exc.msg))
    except IndexError as exc:
        self.debugl(('Unable to gather custom fields due to %s' % exc))
    return instance_tuples